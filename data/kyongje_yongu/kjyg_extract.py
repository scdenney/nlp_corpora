# -*- coding: utf-8 -*-
"""Extraction library for the 경제연구 (Kyongje Yongu) corpus update 2017-4..2020.

Two source types:
  - docx: one article per file (2017/4, 2018/*). Title+author in filename plus a
          저자/출처 metadata line in the body.
  - pdf : full-issue scans with an extractable text layer (2019/*, 2020/*).
          Segment by 16pt centered titles; authors matched from the TOC (차례).
          DPRK leader names render in a Private-Use-Area honorific font whose
          codepoints vary per file, so we derive a char->syllable map per file
          from epithet contexts.
"""
import re, os, glob, unicodedata
from collections import Counter
import fitz  # PyMuPDF
import docx as docxlib

TITLE_SIZE = 15.5          # body article titles render at 16pt
PAGE_MARKER = re.compile(r"^[－\-—–]\s*\d+\s*[－\-—–]$")
PAGENUM_RE = re.compile(r"[－\-—–]\s*(\d+)\s*[－\-—–]")
WS = re.compile(r"[ \t]+")

ACAD_PREFIX = ["교수", "박사", "준박사", "부교수", "학사", "원사", "후보원사",
               "연구사", "박사원", "원사후보", "겸임교수"]

# --- DPRK leader-name honorific font handling --------------------------------
PUA_RE = re.compile("[-]")
EPITHET_NAME = [
    ("경애하는 최고령도자", "김정은"),
    ("위대한 령도자", "김정일"),
    ("친애하는 지도자", "김정일"),
    ("위대한 수령", "김일성"),
]
# Fallback for codepoints observed across the 2019-2020 files (F0xx / F1xx ranges).
GLOBAL_PUA = {
    "": "김", "": "일", "": "성",
    "": "김", "": "정", "": "일",
    "": "김", "": "정", "": "은",
    "": "김", "": "일", "": "성",
    "": "김", "": "정", "": "일",
}
UNMAPPED_PUA = Counter()


def derive_pua_map(text):
    m = {}
    for ep, name in EPITHET_NAME:
        pat = re.escape(ep) + r"\s*((?:[-]\s*){%d})" % len(name)
        for mt in re.finditer(pat, text):
            puas = [c for c in mt.group(1) if PUA_RE.match(c)]
            if len(puas) == len(name):
                for c, syl in zip(puas, name):
                    m.setdefault(c, syl)
    return m


def clean_pua(text, pua_map):
    if not text:
        return text
    def repl(mo):
        c = mo.group(0)
        out = pua_map.get(c) or GLOBAL_PUA.get(c)
        if out is None:
            UNMAPPED_PUA[f"U+{ord(c):04X}"] += 1
            return ""
        return out
    return PUA_RE.sub(repl, text)


def norm(s):
    if s is None:
        return ""
    return unicodedata.normalize("NFC", str(s)).strip()


def despace(s):
    return re.sub(r"\s+", "", norm(s))


def strip_acad(s):
    s = norm(s)
    for p in sorted(ACAD_PREFIX, key=len, reverse=True):
        s = s.replace(p, "")
    return s.strip()


def collapse_author(a):
    a = norm(a)
    if a and len(a.replace(" ", "")) <= 6:
        a = re.sub(r"(?<=[가-힣])\s+(?=[가-힣])", "", a)
    return a.strip()


def word_count(text):
    return len(norm(text).split())


# --------------------------------------------------------------------------- #
# DOCX
# --------------------------------------------------------------------------- #
def parse_docx(path, year_issue):
    doc = docxlib.Document(path)
    paras = [norm(p.text) for p in doc.paragraphs]
    paras = [p for p in paras if p]

    stem = re.sub(r"\.docx?$", "", os.path.basename(path), flags=re.I)
    f_title, f_author = stem, ""
    if " - " in stem:
        f_title, f_author = stem.rsplit(" - ", 1)
    f_title, f_author = norm(f_title), norm(f_author)

    meta_idx, meta_author, meta_yi = None, "", ""
    for i, p in enumerate(paras):
        if ("저자" in p and "출처" in p) or "ISSN" in p or "정기간행물번호" in p:
            meta_idx = i
            m = re.search(r"저자\s*([^|]+)", p)
            if m:
                meta_author = norm(m.group(1))
            m = re.search(r"(\d{4})\s*년\s*(\d+)\s*호", p)
            if m:
                meta_yi = f"{m.group(1)}-{int(m.group(2))}"
            break

    author = f_author or meta_author
    yi = meta_yi or year_issue

    body = [p for j, p in enumerate(paras) if j != meta_idx]
    head, drop = "", 0
    for p in body[:4]:
        head = despace(head + p)
        drop += 1
        if f_title and despace(f_title) in head:
            break
    else:
        drop = 0
    content = "\n".join(body[drop:]).strip() or "\n".join(body).strip()

    return {
        "title": f_title,
        "author": author,
        "year_issue": yi,
        "word_count": word_count(content),
        "file_path": os.path.relpath(path).replace(os.sep, "/"),
        "content": content,
        "source_type": "docx",
    }


def extract_docx_dir(root, year_issue_map):
    rows = []
    for rel, yi in year_issue_map.items():
        for f in sorted(glob.glob(os.path.join(root, rel, "*.docx"))):
            if os.path.basename(f).startswith("~$"):
                continue
            rows.append(parse_docx(f, yi))
    return rows


# --------------------------------------------------------------------------- #
# PDF
# --------------------------------------------------------------------------- #
def _page_blocks(page):
    out = []
    for b in page.get_text("dict")["blocks"]:
        if "lines" not in b:
            continue
        spans = [s for l in b["lines"] for s in l["spans"]]
        txt = "".join(s["text"] for s in spans)
        if not txt.strip():
            continue
        x0, y0, x1, y1 = b["bbox"]
        out.append({"x0": x0, "y0": y0, "x1": x1, "y1": y1,
                    "cx": (x0 + x1) / 2, "w": x1 - x0,
                    "size": max(s["size"] for s in spans),
                    "text": txt,
                    "is_title": max(s["size"] for s in spans) >= TITLE_SIZE})
    return out


def _reading_order(blocks, page_w):
    mid = page_w / 2
    full = lambda b: b["is_title"] or b["w"] > 0.5 * page_w
    blocks = sorted(blocks, key=lambda b: b["y0"])
    order, twocol = [], []

    def flush():
        order.extend(sorted([b for b in twocol if b["cx"] < mid], key=lambda b: b["y0"]))
        order.extend(sorted([b for b in twocol if b["cx"] >= mid], key=lambda b: b["y0"]))
        twocol.clear()

    for b in blocks:
        if full(b):
            flush()
            order.append(b)
        else:
            twocol.append(b)
    flush()
    return order


def _toc_pages(doc):
    """Front-matter pages (index < 6) carrying the dotted-leader table of contents."""
    pages = []
    for pi in range(min(6, doc.page_count)):
        t = doc[pi].get_text()
        leaders = len(re.findall(r"[.…·．]{4,}", t))
        if leaders >= 4 or (re.search(r"차\s*례", t) and len(re.findall(r"\(\s*\d+\s*\)", t)) >= 4):
            pages.append(pi)
    return pages


def _parse_toc(doc, toc_pages, pua_map):
    """Return list of (despaced_title, author, page_int)."""
    entries = []
    raw = "\n".join(clean_pua(doc[pi].get_text(), pua_map) for pi in toc_pages)
    # drop page markers, masthead, and slogan lines (slogans end with ！/!)
    keep = []
    for ln in raw.split("\n"):
        s = ln.strip()
        if PAGE_MARKER.match(s) or re.search(r"[！!]\s*$", s):
            continue
        if re.search(r"^경제연구|차\s*례|주체\d|루계", s):
            continue
        keep.append(ln)
    raw = " ".join(keep)
    for m in re.finditer(r"([^()]+?)\(\s*(\d+)\s*\)", raw):
        seg = re.sub(r"[.…·．]{2,}", " ", m.group(1))
        # strip any residual leading page-marker fragment ("－ 2 －")
        seg = re.sub(r"^.*?[－\-—–]\s*\d+\s*[－\-—–]\s*", "", seg)
        seg = WS.sub(" ", norm(seg)).strip()
        page = int(m.group(2))
        if not seg or "차례" in seg:
            continue
        toks = seg.split()
        author, title = "", seg
        # peel academic prefixes + trailing hangul name from the end
        if toks and re.fullmatch(r"[가-힣]{2,4}", toks[-1]) and toks[-1] not in ACAD_PREFIX:
            author, title = toks[-1], " ".join(toks[:-1])
        entries.append((despace(strip_acad(title)), author, page))
    return entries


def pdf_journal(path):
    """Return (journal_name, ruge_number) from masthead/colophon for verification."""
    doc = fitz.open(path)
    name = ""
    for pi in range(min(4, doc.page_count)):
        for b in doc[pi].get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    t = s["text"].strip()
                    if s["size"] >= 24 and re.fullmatch(r"[가-힣]{2,6}", t) and not name:
                        name = t
    full = "\n".join(doc[pi].get_text() for pi in range(doc.page_count))
    m = re.search(r"\(루계\s*제?\s*(\d+)\s*호\)", full)
    ruge = m.group(1) if m else None
    doc.close()
    return name, ruge


def extract_pdf(path, year_issue, require="경제연구"):
    journal, ruge = pdf_journal(path)
    if require and journal and require not in journal:
        raise ValueError(f"journal mismatch: {os.path.basename(path)} is '{journal}' "
                         f"(루계 {ruge}), not '{require}' — skipping")
    doc = fitz.open(path)
    page_w = doc[0].rect.width
    full_text = "\n".join(doc[pi].get_text() for pi in range(doc.page_count))
    pua_map = derive_pua_map(full_text)

    toc_pages = _toc_pages(doc)
    first_content = (max(toc_pages) + 1) if toc_pages else 2
    toc = _parse_toc(doc, toc_pages, pua_map)
    toc_by_dtitle = {}
    toc_by_page = {}
    for dtitle, author, page in toc:
        if dtitle:
            toc_by_dtitle.setdefault(dtitle, author)
        toc_by_page.setdefault(page, author)

    # printed page number per PDF page (from the "－ N －" marker)
    printed_of = {}
    for pi in range(doc.page_count):
        mk = PAGENUM_RE.search(doc[pi].get_text())
        printed_of[pi] = int(mk.group(1)) if mk else -1

    # flat reading-order stream
    stream = []
    for pi in range(doc.page_count):
        for b in _reading_order(_page_blocks(doc[pi]), page_w):
            b["pdf_page"] = pi
            b["printed"] = printed_of[pi]
            stream.append(b)

    # group consecutive title blocks (multi-line titles) into article anchors
    articles, i, N = [], 0, len(stream)
    while i < N:
        b = stream[i]
        if b["is_title"] and b["pdf_page"] >= first_content:
            j, parts = i, []
            while j < N and stream[j]["is_title"] and stream[j]["pdf_page"] == b["pdf_page"]:
                parts.append(stream[j]["text"])
                j += 1
            title = WS.sub(" ", clean_pua(norm("".join(parts)), pua_map)).strip()
            if title and not re.search(r"경제연구|루계|주체\d", title):
                articles.append({"title": title, "start": j, "printed": b["printed"]})
            i = j
        else:
            i += 1

    acad = "|".join(map(re.escape, ACAD_PREFIX))
    byline_re = re.compile(r"^(?:(?:%s)\s*)+[가-힣]{2,4}$" % acad)

    rows = []
    for k, art in enumerate(articles):
        seg = stream[art["start"]:(articles[k + 1]["start"] if k + 1 < len(articles) else N)]
        body, author_body = [], ""
        for idx, blk in enumerate(seg):
            txt = clean_pua(norm(blk["text"]), pua_map)
            if PAGE_MARKER.match(txt.strip()):
                continue
            if idx == 0 and len(despace(txt)) <= 8 and re.fullmatch(r"[가-힣\s]+", txt):
                author_body = collapse_author(txt)
                continue
            body.append(txt)

        title = title_clean(art["title"])
        dkey = despace(strip_acad(title))
        # page-number match is primary (printed marker -> TOC author); then title; then body
        author = toc_by_page.get(art["printed"], "") or toc_by_dtitle.get(dkey) or author_body

        # drop byline lines (academic prefix + name, or exactly the author) that
        # the column reading order placed inside the body — but never section heads
        adk = despace(author)
        kept = []
        for ln in body:
            s = ln.strip()
            if byline_re.match(s) or (adk and 2 <= len(adk) <= 4 and despace(s) == adk):
                continue
            kept.append(ln)
        content = "\n".join(kept)
        content = re.sub(r"[－—–]\s*\d+\s*[－—–]", "", content)  # embedded page markers
        content = re.sub(r"[ \t]+\n", "\n", re.sub(r"\n{3,}", "\n\n", content)).strip()

        rows.append({
            "title": title,
            "author": author,
            "year_issue": year_issue,
            "word_count": word_count(content),
            "file_path": os.path.relpath(path).replace(os.sep, "/"),
            "content": content,
            "source_type": "pdf",
        })
    doc.close()
    return rows, toc


def title_clean(t):
    t = clean_pua(norm(t), {})
    t = re.sub(r"^[―—–\-]*\s*사설\s*[―—–\-]*\s*", "", t)
    return t.strip()
