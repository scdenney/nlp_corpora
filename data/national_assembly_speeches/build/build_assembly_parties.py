"""Party of South Korean National Assembly members on any date (16th, 17th, 19th-22nd).

Sources (downloaded once into ~/.cache/ba3tad/assembly-members/, then reused offline):
  - Korean Wikipedia member lists, "대한민국 제N대 국회의원 목록", wikitext via the MediaWiki API.
  - The lead paragraph of every member's own Wikipedia article (for the hanja name).
  - teampopong/data-assembly assembly.csv (hanja names; covers only the 20th Assembly).

Party on a date = party at election (or at by-election / succession), then the page's
table of party renames applied on their dates, then the member's dated notes (비고).

Outputs (next to this script):
  assembly_party_spells.csv     one row per speaker string, term and party spell
  assembly_party_unmatched.csv  candidate speaker-terms not resolved with confidence

Usage:  python3 build_assembly_parties.py [--refresh]
"""

import csv
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
CACHE = Path.home() / ".cache/ba3tad/assembly-members"
CANDIDATES = Path.home() / ".cache/ba3tad/assembly-corpus/candidate_speakers.csv"
GROUND_TRUTH = Path.home() / "Documents/github/courses/ba3tad-26/assets/data/assembly-nk-japan.csv"
OUT_SPELLS = HERE / "assembly_party_spells.csv"
OUT_UNMATCHED = HERE / "assembly_party_unmatched.csv"

UA = {"User-Agent": "course-data-check/1.0"}
API = "https://ko.wikipedia.org/w/api.php"
POPONG = "https://raw.githubusercontent.com/teampopong/data-assembly/master/assembly.csv"
UNIHAN = "https://www.unicode.org/Public/UCD/latest/ucd/Unihan.zip"
HAN = "[\u3400-\u9fff\uf900-\ufaff\U00020000-\U0003134f]"
TERMS = [16, 17, 19, 20, 21, 22]
TERM_START = {16: date(2000, 5, 30), 17: date(2004, 5, 30), 19: date(2012, 5, 30),
              20: date(2016, 5, 30), 21: date(2020, 5, 30), 22: date(2024, 5, 30)}
TERM_END = {16: date(2004, 5, 29), 17: date(2008, 5, 29), 19: date(2016, 5, 29),
            20: date(2020, 5, 29), 21: date(2024, 5, 29), 22: date(2028, 5, 29)}

# Party names as the ground truth writes them. Anything else is reported as new.
STANDARD_VOCAB = {
    "더불어민주당", "국민의힘", "한나라당", "새누리당", "열린우리당", "자유한국당", "새천년민주당",
    "새정치민주연합", "무소속", "민주통합당", "민주당", "국민의당", "대통합민주신당", "바른미래당",
    "자유민주연합", "민주노동당", "정의당", "미래통합당", "조국혁신당", "바른정당", "국민중심당",
    "진보당", "통합진보당", "민주평화당", "새진보연합", "시대전환", "개혁신당", "중도개혁통합신당",
    "민주국민당", "선진통일당", "민중당", "새로운보수당", "열린민주당",
}

# Typos on the Wikipedia pages, corrected here and reported (term, wrong text, corrected text).
WIKI_FIXUPS = [
    (20, "2016.12.2.7.", "2016.12.27."),
    # 박순자: 미래통합당 was founded on 2020-02-17; "2017" is a typo (the note follows 2017.5.12)
    (20, "2017.2.17. 미래통합당 합당", "2020.2.17. 미래통합당 합당"),
]

# Note verbs. The party named in the note becomes the member's party ...
JOIN_VERBS = {"입당", "복당", "창당", "합당", "합류"}
# ... or the member becomes an independent.
LEAVE_VERBS = {"탈당", "제명", "출당", "해산", "정당등록취소"}
START_NOTES = {"재보궐선거 당선", "의원직 승계"}
END_NOTES = {"의원직 상실", "의원직 사퇴", "사망", "선거무효"}


# ----------------------------------------------------------------------------- download

def fetch(url, retries=6):
    for k in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if k == retries - 1:
                raise
            wait = int(e.headers.get("Retry-After") or 0) if e.code == 429 else 0
            time.sleep(max(wait, 5 * (k + 1)))
        except Exception:
            if k == retries - 1:
                raise
            time.sleep(5 * (k + 1))


def page_path(term):
    return CACHE / f"wiki_{term}.json"


def download_pages(refresh):
    CACHE.mkdir(parents=True, exist_ok=True)
    for t in TERMS:
        p = page_path(t)
        if p.exists() and not refresh:
            continue
        title = f"대한민국 제{t}대 국회의원 목록"
        url = f"{API}?action=parse&page={urllib.parse.quote(title)}&prop=wikitext&format=json&redirects=1"
        p.write_bytes(fetch(url))
        time.sleep(1)
    p = CACHE / "popong_assembly.csv"
    if not p.exists() or refresh:
        p.write_bytes(fetch(POPONG))
    p = CACHE / "unihan_khangul.txt"
    if not p.exists() or refresh:
        import io
        import zipfile
        z = zipfile.ZipFile(io.BytesIO(fetch(UNIHAN)))
        lines = [x for x in z.read("Unihan_Readings.txt").decode().split("\n") if "\tkHangul\t" in x]
        p.write_text("\n".join(lines) + "\n")


def load_readings():
    """Hanja character -> set of hangul readings (Unihan kHangul, incl. initial-sound-law forms)."""
    out = {}
    for ln in (CACHE / "unihan_khangul.txt").read_text().splitlines():
        cp, _, val = ln.split("\t")
        out[chr(int(cp[2:], 16))] = {v.split(":")[0] for v in val.split()}
    return out


def readings_of(hanja, table):
    """All hangul spellings a hanja name can be read as (empty if a character is unknown)."""
    acc = {""}
    for ch in hanja:
        rs = ({ch} if "\uac00" <= ch <= "\ud7a3"
              else table.get(ch) or table.get(unicodedata.normalize("NFKC", ch)))
        if not rs:
            return set()
        acc = {a + r for a in acc for r in rs}
    return acc


def download_leads(titles, refresh):
    """Plain-text lead paragraph of each member article, for the hanja name."""
    p = CACHE / "member_leads.json"
    leads = json.loads(p.read_text()) if p.exists() and not refresh else {}
    todo = sorted(t for t in set(titles) if t not in leads)
    for i in range(0, len(todo), 20):
        batch = todo[i:i + 20]
        q = urllib.parse.urlencode({
            "action": "query", "prop": "extracts", "exintro": 1, "explaintext": 1,
            "exlimit": 20, "redirects": 1, "format": "json", "titles": "|".join(batch)})
        d = json.loads(fetch(f"{API}?{q}"))["query"]
        alias = {}
        for key in ("normalized", "redirects"):
            for r in d.get(key, []):
                alias[r["from"]] = r["to"]
        found = {pg["title"]: pg.get("extract", "") for pg in d["pages"].values()}
        for t in batch:
            tgt = t
            while tgt in alias:
                tgt = alias[tgt]
            leads[t] = found.get(tgt, "")
        p.write_text(json.dumps(leads, ensure_ascii=False))
        time.sleep(2)
    return leads


# ----------------------------------------------------------------------------- parse pages

def norm_party(name):
    """Plain party name without Wikipedia's disambiguating year (민주당2000 -> 민주당)."""
    name = name.strip()
    return re.sub(r"\d{4}$", "", name).strip()


def party_template(cell):
    m = re.search(r"정당=([^}|]*)", cell)
    return m.group(1).strip() if m else None


def parse_date(s):
    m = re.fullmatch(r"\s*(\d{4})\.\s*(\d{1,2})\.\s*(\d{1,2})\.?\s*", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return None


def tables(txt):
    """Yield (section heading, list of rows); a row is a list of (marker, cell text)."""
    sec, rows, intable = None, None, False
    for ln in txt.split("\n"):
        m = re.match(r"^(=+)\s*(.*?)\s*\1\s*$", ln)
        if m:
            sec = m.group(2)
            continue
        if ln.startswith("{|"):
            intable, rows = True, []
            continue
        if ln.startswith("|}"):
            if rows:
                yield sec, rows
            intable, rows = False, None
            continue
        if not intable:
            continue
        if ln.startswith("|-"):
            rows.append([])
        elif ln[:1] in ("|", "!"):
            if not rows:
                rows.append([])
            rows[-1].append((ln[0], ln[1:].strip()))


def parse_renames(txt, issues, term):
    """Table of party renames at the top of the page: list of (date, old, new)."""
    out = []
    for sec, rows in tables(txt):
        if sec is not None:
            break  # the rename table sits above the first heading
        for r in rows:
            cells = [c for k, c in r if k == "|"]
            if len(cells) >= 3 and "년" in cells[0]:
                m = re.match(r"(\d{4})년 (\d{1,2})월 (\d{1,2})일", cells[0])
                old, new = party_template(cells[1]), party_template(cells[2])
                if not (m and old and new):
                    issues.append(f"{term}: rename row not parsed: {cells}")
                    continue
                out.append((date(*map(int, m.groups())), norm_party(old), norm_party(new),
                            f"{old}->{new}"))
    return out


def parse_name(cell):
    m = re.search(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", cell)
    if m:
        target = m.group(1).strip()
        label = (m.group(2) or re.sub(r"\s*\(.*\)$", "", target)).strip()
        return label, target
    plain = re.sub(r"<[^>]+>|'''?", "", cell).strip()
    return plain, None


def parse_notes(cell, term, name, issues):
    """Return list of (date, kind, party, raw text)."""
    cell = re.sub(r"\{\{글 숨김\|?\}\}|\{\{?글 숨김 끝\}\}", "", cell)
    out = []
    for part in re.split(r"<br\s*/?>", cell):
        part = re.sub(r"<[^>]+>", "", part).strip()
        if not part:
            continue
        m = re.match(r"^(\d{4}\.\s*\d{1,2}\.\s*\d{1,2}\.?)\s*(.*)$", part)
        if not m:
            m2 = re.match(r"^(\d{4})\.\s*(\d{1,2})\.\s+(.*)$", part)
            if m2:  # month-only date: keep, flagged as imprecise
                y, mo, rest = int(m2.group(1)), int(m2.group(2)), m2.group(3)
                out.append((date(y, mo, 1), "month-only", rest, part))
                continue
            issues.append(f"{term} {name}: note without a date: {part!r}")
            continue
        d = parse_date(m.group(1))
        rest = re.sub(r"\[\[(?:[^\]|]*\|)?([^\]]+)\]\]", r"\1", m.group(2)).strip()
        out.append((d, None, rest, part))
    events = []
    for d, flag, rest, raw in out:
        precise = flag is None
        if rest in START_NOTES:
            events.append((d, "start", None, raw, precise))
        elif rest in END_NOTES:
            events.append((d, "end", None, raw, precise))
        elif rest == "제명무효 가처분 인용":
            events.append((d, "unexpel", None, raw, precise))
        else:
            m = re.fullmatch(r"(\S+)\s+(\S+)", rest)
            if m and m.group(2) in JOIN_VERBS:
                events.append((d, "join", norm_party(m.group(1)), raw, precise))
            elif m and m.group(2) in LEAVE_VERBS:
                events.append((d, "leave", norm_party(m.group(1)), raw, precise))
            else:
                issues.append(f"{term} {name}: note not understood: {raw!r}")
                events.append((d, "unparsed", None, raw, precise))
    return events


def parse_members(term, txt, issues):
    for wrong, right in [(w, r) for t, w, r in WIKI_FIXUPS if t == term]:
        if wrong in txt:
            txt = txt.replace(wrong, right)
            issues.append(f"{term}: corrected page typo {wrong!r} -> {right!r}")
    renames = parse_renames(txt, issues, term)
    members = []
    for sec, rows in tables(txt):
        if sec is None or sec in ("같이 보기", "의석 변동"):
            continue
        for r in rows:
            cells = [c for k, c in r if k == "|"]
            if not cells or (r and r[0][0] == "!" and r[0][1] in ("선거구", "순번")):
                continue
            if any("공석" in c for c in cells):
                continue
            parties = [party_template(c) for c in cells if "정당색과 연결" in c]
            if len(parties) != 2:
                issues.append(f"{term} [{sec}]: row skipped, {len(parties)} party cells: {cells[:2]}")
                continue
            label, target = parse_name(cells[0])
            notes_cell = cells[-1]
            if re.fullmatch(r"(초선|재선|\d+선)", notes_cell):
                notes_cell = ""
            events = parse_notes(notes_cell, term, label, issues)
            members.append({
                "term": term, "section": sec, "name": label, "article": target,
                "elected_party": norm_party(parties[0]), "elected_template": parties[0],
                "end_party": norm_party(parties[1]) if parties[1] else "",
                "end_template": parties[1], "events": events,
                "is_pr": bool(r[0][0] == "!" and re.match(r"^'*\d+번", r[0][1])),
            })
    return members, renames


# ----------------------------------------------------------------------------- party timeline

def month_end(d):
    return date(d.year + (d.month == 12), d.month % 12 + 1, 1) - timedelta(days=1)


def build_timeline(m, renames, inferred, issues, quiet=False):
    """Party history of one member in one term.

    Sets m["spells"]  [(start, end, party, basis)] over the member's time in office,
          m["hist"]    [(date, party)] every party change, including those before entry,
          m["windows"] [(start, end, reason)] date ranges where the page's record does not
                       settle the party (these dates get no party in the output).
    """
    term = m["term"]
    start, end = TERM_START[term], TERM_END[term]
    for d, kind, _, _, _ in m["events"]:
        if kind == "start":
            start = max(start, d)
        elif kind == "end":
            end = min(end, d)
    warn = (lambda x: None) if quiet else issues.append
    windows = []
    ev = m["events"]
    # notes out of chronological order: the order of changes in between is unknown
    for i in range(len(ev)):
        for j in range(i + 1, len(ev)):
            if ev[j][0] < ev[i][0]:
                lo, hi = ev[j][0], ev[i][0]
                later = [e[0] for e in ev if e[0] > hi and e[1] in ("join", "leave")]
                stop = min(later) - timedelta(days=1) if later else end
                windows.append((lo, stop, f"notes out of date order ({ev[i][3]!r} before {ev[j][3]!r})"))
                warn(f"{term} {m['name']}: notes out of date order: {ev[i][3]!r} before {ev[j][3]!r}")
    for d, kind, _, raw, precise in ev:
        if kind == "unparsed":
            windows.append((d, end, f"note not understood: {raw!r}"))
        elif not precise:
            windows.append((d, month_end(d), f"note dated to the month only: {raw!r}"))

    basis = (f"party at entry ({m['elected_template']})" if start > TERM_START[term]
             else f"election party ({m['elected_template']})")
    changes = []  # (date, order, change, basis); same-day order: notes, inferred mergers, renames
    for i, (d, kind, p, raw, precise) in enumerate(ev):
        if kind in ("join", "leave", "unexpel"):
            changes.append((d, i, (kind, p), raw))
    for d, p, label in inferred:
        changes.append((d, 1000, ("join", p), label))
    for d, old, new, label in renames:
        # renames from other pages only near this term: names recur across eras
        # (미래한국당 2008 vs 2020, 민주당 2000/2007/2011/2014)
        if not (TERM_START[term] - timedelta(days=365) <= d <= TERM_END[term]):
            continue
        changes.append((d, 2000, ("rename", old, new), f"rename {label} {d.isoformat()}"))
    changes.sort(key=lambda x: (x[0], x[1]))

    cur_party, cur_basis, cur_since = m["elected_party"], basis, None
    hist = [(None, cur_party)]
    spells = []
    expelled_on = None
    for d, _, ch, label in changes:
        if ch[0] == "rename":
            if cur_party != ch[1]:
                continue
            new_party = ch[2]
        elif ch[0] == "join":
            new_party = ch[1]
        elif ch[0] == "leave":
            if ch[1] != cur_party:
                warn(f"{term} {m['name']}: leaves {ch[1]} but is in {cur_party} ({label})")
                windows.append((max(cur_since or start, start), d - timedelta(days=1),
                                f"page says the member left {ch[1]} on {d} but the record has {cur_party} before"))
            new_party = "무소속"
            if "제명" in label:
                expelled_on = d
        else:  # unexpel: a court voided the expulsion; the page's end party applies afterwards
            new_party = m["end_party"]
            if expelled_on:
                windows.append((expelled_on, d - timedelta(days=1),
                                f"expulsion of {expelled_on} later voided by court injunction ({label})"))
        if new_party == cur_party:
            continue
        hist.append((d, new_party))
        if d > end:
            break
        if d <= start:
            cur_party, cur_basis, cur_since = new_party, label, d
            continue
        spells.append([cur_since if cur_since and cur_since > start else start,
                       d - timedelta(days=1), cur_party, cur_basis])
        cur_party, cur_basis, cur_since = new_party, label, d
    spells.append([cur_since if cur_since and cur_since > start else start, end, cur_party, cur_basis])
    final = cur_party
    if m["end_party"] and final != m["end_party"] and end == TERM_END[term]:
        last = max([d for d, *_ in changes if d <= end and d >= start] or [start])
        warn(f"{term} {m['name']}: computed end party {final} != page end party {m['end_party']}")
        windows.append((last, end, f"party after {last} disagrees with the page's end party "
                                   f"({final} vs {m['end_party']})"))
    m["end_check"] = (final == m["end_party"]) if m["end_party"] else None
    m["start"], m["end"] = start, end
    m["spells"], m["hist"] = spells, hist
    m["windows"] = [(max(a, start), min(b, end), r) for a, b, r in windows if a <= end and b >= start and a <= b]


def subtract(ranges, holes):
    """Inclusive date ranges minus inclusive holes."""
    out = list(ranges)
    for h0, h1 in holes:
        nxt = []
        for a, b in out:
            if h1 < a or h0 > b:
                nxt.append((a, b))
                continue
            if a < h0:
                nxt.append((a, h0 - timedelta(days=1)))
            if b > h1:
                nxt.append((h1 + timedelta(days=1), b))
        out = nxt
    return out


def party_before(m, d):
    """Party held on the day before d, from the full history (also before entry)."""
    p = m["hist"][0][1]
    for dd, pp in m["hist"][1:]:
        if dd < d:
            p = pp
    return p


# ----------------------------------------------------------------------------- hanja

def lead_hanja(lead):
    """Hanja name from an article lead such as '이낙연(李洛淵, 1952년 12월 20일 ~ )은 ...'."""
    head = lead[:200]
    m = re.search(r"[(\uff08]\s*(?:[^()\uff08\uff09]*?[:,]\s*)?(" + HAN + r"{2,5})\s*[,\uff0c)\uff09]", head)
    if not m:
        m = re.search("(" + HAN + "{2,5})", head)
    return unicodedata.normalize("NFKC", m.group(1)) if m else None


# ----------------------------------------------------------------------------- main

def main():
    refresh = "--refresh" in sys.argv
    download_pages(refresh)
    issues = []
    members, renames_by_term = [], {}
    for t in TERMS:
        txt = json.loads(page_path(t).read_text())["parse"]["wikitext"]["*"]
        ms, rn = parse_members(t, txt, issues)
        members.extend(ms)
        renames_by_term[t] = rn
    leads = download_leads([m["article"] for m in members if m["article"]], refresh)
    readings = load_readings()
    popong = pd.read_csv(CACHE / "popong_assembly.csv", dtype=str)
    popong_hanja = defaultdict(set)
    for _, r in popong.iterrows():
        if isinstance(r["name_cn"], str):
            popong_hanja[r["name_kr"].strip()].add(r["name_cn"].strip())

    # Renames from every page apply in every term (a rename on the 21st page, such as
    # 2024-05-09 새진보연합 -> 기본소득당, also governs members of the 22nd).
    all_renames = sorted({r for rn in renames_by_term.values() for r in rn})

    # Pass 1: timelines from each member's own notes plus renames.
    for m in members:
        build_timeline(m, all_renames, [], issues, quiet=True)
        lead = leads.get(m["article"] or "", "") or ""
        m["hanja"] = lead_hanja(lead)
        m["lead_is_mp"] = "국회의원" in lead
        m["id"] = f"{m['term']}:{m['article'] or m['name']}"

    # Party-wide mergers. When several members' notes record "<X> 합당" on the same date,
    # the whole party they came from merged into X on that date; members of that party who
    # lack the note (e.g. 박지원 and 김승남 for 2014-03-26 새정치민주연합) get it inferred.
    groups = defaultdict(list)
    for m in members:
        for d, kind, p, raw, _ in m["events"]:
            if kind == "join" and raw.endswith("합당"):
                groups[(m["term"], d, p)].append(m)
    inferred = defaultdict(list)
    for (t, d, p), ms in sorted(groups.items()):
        if len(ms) < 2:
            continue
        priors = {party_before(m, d) for m in ms} - {"무소속", p}
        # A party that merged away on d cannot be joined or left afterwards: drop any prior
        # party that a note on this page names within 180 days after d (unless a rename
        # re-creates that name in between, as 2007-08-13 중도통합민주당 -> 민주당 did).
        for q in sorted(priors):
            recreated = min([rd for rd, _, new_, _ in all_renames if new_ == q and rd > d] or [d + timedelta(days=180)])
            later = [(m2["name"], raw2) for m2 in members if m2["term"] == t
                     for d2, k2, p2, raw2, _ in m2["events"]
                     if k2 in ("join", "leave") and p2 == q and d < d2 < min(recreated, d + timedelta(days=180))]
            if later:
                priors.discard(q)
                issues.append(f"{t} merger '{p} 합당' {d}: not inferred for members of {q}, which notes "
                              f"still name afterwards (e.g. {later[0][0]}: {later[0][1]!r})")
        for m in members:
            if m["term"] != t or m in ms or d > m["end"]:
                continue
            if any(k == "join" and pp == p for _, k, pp, _, _ in m["events"]):
                continue
            if party_before(m, d) in priors:
                label = (f"inferred merger: {len(ms)} members' notes record '{p} 합당' on "
                         f"{d.isoformat()} (from {'/'.join(sorted(priors))})")
                inferred[id(m)].append((d, p, label))
                issues.append(f"{t} {m['name']}: {label}")
    # Pass 2: final timelines.
    for m in members:
        build_timeline(m, all_renames, inferred[id(m)], issues)

    # One person can hold two rows in a term (proportional seat, then a by-election seat:
    # 전재희 in the 16th, 유승민 in the 17th). Merge rows that link the same article.
    merged = {}
    for m in members:
        if m["id"] in merged:
            a = merged[m["id"]]
            a["spells"] = sorted(a["spells"] + m["spells"], key=lambda s: s[0])
            a["windows"] += m["windows"]
            a["start"], a["end"] = min(a["start"], m["start"]), max(a["end"], m["end"])
            a["is_pr"] = a["is_pr"] or m["is_pr"]
            a["section"] += " + " + m["section"]
            issues.append(f"{m['term']} {m['name']}: two rows for one article merged "
                          f"({[(s[0].isoformat(), s[1].isoformat(), s[2]) for s in a['spells']]})")
        else:
            merged[m["id"]] = m
    members = list(merged.values())

    # ------------------------------------------------------------------ resolve speakers
    cand = pd.read_csv(CANDIDATES, dtype=str)
    cand["assembly_term"] = cand["assembly_term"].astype(int)
    cand["n_turns"] = cand["n_turns"].astype(int)
    n20 = Counter(m["name"] for m in members if m["term"] == 20)
    by_name = defaultdict(list)
    by_hanja = defaultdict(list)
    for m in members:
        by_name[(m["term"], m["name"])].append(m)
        if m["hanja"]:
            by_hanja[(m["term"], m["hanja"])].append(m)
        # popong covers the 20th Assembly only; used where the hangul name is unique there
        if m["term"] == 20 and m["name"] in popong_hanja and n20[m["name"]] == 1:
            for h in popong_hanja[m["name"]]:
                h = unicodedata.normalize("NFKC", h)
                if h != m["hanja"]:
                    by_hanja[(20, h)].append(m)

    # mem_id is NOT stable across terms in this corpus (no id appears in two terms), so it
    # can only separate people within one term.
    def party_on(m, d):
        for a, b, p, _ in m["spells"]:
            if a <= d <= b:
                return p
        return None

    def candidates_for(row):
        t, s = row.assembly_term, row.speaker
        # NFKC folds CJK compatibility ideographs (U+F90A 金 -> U+91D1 金) that the minutes mix in
        base = unicodedata.normalize("NFKC", re.sub(r"\(.*\)$", "", s).strip())
        if re.search(HAN, base):
            hits = by_hanja.get((t, base), [])
            how = "hanja"
            if not hits:
                # Fallback: the hangul reading of the hanja matches exactly one member of the
                # term, and that member's article gives no hanja that contradicts it.
                rd = readings_of(base, readings)
                by_reading = [m for m in members if m["term"] == t and m["name"] in rd]
                if len({m["id"] for m in by_reading}) == 1:
                    m0 = by_reading[0]
                    if m0["hanja"] and m0["hanja"] != base and m0["lead_is_mp"]:
                        return [], f"hanja reading {m0['name']}, but that member's article gives {m0['hanja']}", base
                    note = ("article gives no hanja" if not m0["hanja"] else
                            f"linked article {m0['article']!r} gives {m0['hanja']} but its lead never says 국회의원")
                    hits, how = by_reading, f"hanja reading ({m0['name']}; {note})"
                elif len(by_reading) > 1:
                    hits, how = by_reading, "hanja reading"
        else:
            hits = by_name.get((t, base), [])
            how = "name"
        uniq = {m["id"]: m for m in hits}
        return list(uniq.values()), how, base

    pending = []
    resolved = {}  # (speaker, term) -> (member, evidence)
    unmatched = []
    for row in cand.itertuples(index=False):
        hits, how, base = candidates_for(row)
        first, last = date.fromisoformat(row.first_date), date.fromisoformat(row.last_date)
        key = (row.speaker, row.assembly_term)
        if not hits:
            unmatched.append((row, f"not found on the {row.assembly_term}th Assembly list (by {how})"
                              if how in ("name", "hanja") else how))
            continue
        if len(hits) == 1:
            resolved[key] = (hits[0], how)
            continue
        pending.append((row, hits, how, base, first, last))

    # Namesakes. Pass 1: a suffix printed in the minutes. Pass 2: elimination (a plain string
    # whose mem_id differs from a suffixed string already pinned to one namesake) and
    # membership dates (only one namesake in office on the first and last date).
    pinned = defaultdict(list)  # (term, base) -> [(member id, mem_id)]
    for passno in (1, 2):
        for row, hits, how, base, first, last in pending:
            key = (row.speaker, row.assembly_term)
            suf = re.search(r"\((.+)\)$", row.speaker)
            if (passno == 1) != bool(suf):
                continue
            choice, evidence = None, None
            if suf:
                s = suf.group(1)
                if s == "비":
                    pick = [m for m in hits if m["is_pr"]]
                    evidence = "suffix (비) in the minutes = the proportional-list member"
                else:
                    pick = [m for m in hits if any(s in (party_on(m, d) or "") for d in (first, last))]
                    evidence = f"suffix ({s}) in the minutes matches the party of this namesake only"
                if len(pick) == 1:
                    choice = pick[0]
                    pinned[(row.assembly_term, base)].append((choice["id"], row.mem_id))
            else:
                rest = hits
                for mid_, memid in pinned.get((row.assembly_term, base), []):
                    if memid != "0" and row.mem_id != "0" and memid != row.mem_id:
                        rest = [m for m in rest if m["id"] != mid_]
                if len(rest) == 1 and len(rest) < len(hits):
                    choice = rest[0]
                    evidence = (f"elimination: the suffixed namesake string has another mem_id "
                                f"(this string's mem_id {row.mem_id})")
                else:
                    live = [m for m in rest if m["start"] <= first and m["end"] >= last]
                    if len(live) == 1:
                        choice = live[0]
                        evidence = (f"only namesake in office over the whole {first}..{last} range (the other "
                                    f"entered or left inside it); the string has one mem_id ({row.mem_id})")
            if choice is None:
                names = "; ".join(f"{m['name']} [{m['section']}, elected {m['elected_party']}]" for m in hits)
                parties = {tuple((max(a, first), min(b, last), p) for a, b, p, _ in m["spells"]
                                 if a <= last and b >= first) for m in hits}
                same = ""
                if len(parties) == 1:
                    ps = sorted({p for _, _, p in next(iter(parties))})
                    same = f" (all namesakes are in {'/'.join(ps)} on the same dates over {first}..{last}: party is certain, identity is not)"
                unmatched.append((row, f"{len(hits)} members share the {how} in this term, no evidence to tell them apart: {names}{same}"))
            else:
                resolved[key] = (choice, evidence)

    # ------------------------------------------------------------------ write spells
    out_rows = []
    for row in cand.itertuples(index=False):
        key = (row.speaker, row.assembly_term)
        if key not in resolved:
            continue
        m, how = resolved[key]
        first, last = date.fromisoformat(row.first_date), date.fromisoformat(row.last_date)
        pieces = []
        for a, b, p, basis in m["spells"]:
            a, b = max(a, first), min(b, last)
            if a > b:
                continue
            for x, y in subtract([(a, b)], [(w0, w1) for w0, w1, _ in m["windows"]]):
                pieces.append((x, y, p, basis))
        pieces.sort()
        gaps = subtract([(first, last)], [(x, y) for x, y, _, _ in pieces])
        if gaps:
            why = []
            for g0, g1 in gaps:
                ws = sorted({r for w0, w1, r in m["windows"] if w0 <= g1 and w1 >= g0})
                inside = any(a <= g1 and b >= g0 for a, b, _, _ in m["spells"])
                if not inside:
                    ws.append(f"outside {m['name']}'s membership "
                              f"({'; '.join(f'{a}..{b}' for a, b, _, _ in m['spells'])})")
                why.append(f"{g0}..{g1}: {' | '.join(ws)}")
            tag = "PARTIAL, no party for " if pieces else "no party for any date: "
            unmatched.append((row, tag + " ; ".join(why)))
        if not pieces:
            del resolved[key]
            continue
        for x, y, p, basis in pieces:
            out_rows.append({
                "speaker": row.speaker, "assembly_term": row.assembly_term,
                "member_name": m["name"], "party": p,
                "start_date": x.isoformat(), "end_date": y.isoformat(),
                "basis": basis if how in ("name", "hanja") else f"{basis}; matched by {how}",
            })
    spells = pd.DataFrame(out_rows)
    spells.to_csv(OUT_SPELLS, index=False)
    um = pd.DataFrame([{"speaker": r.speaker, "assembly_term": r.assembly_term,
                        "n_turns": r.n_turns, "reason": reason} for r, reason in unmatched])
    um = um.sort_values(["assembly_term", "n_turns"], ascending=[True, False])
    um.to_csv(OUT_UNMATCHED, index=False)

    report(cand, spells, um, members, issues, resolved)


def party_at(spells, speaker, term, d):
    s = spells[(spells.speaker == speaker) & (spells.assembly_term == term)]
    s = s[(s.start_date <= d) & (s.end_date >= d)]
    return s.party.iloc[0] if len(s) == 1 else None


def report(cand, spells, um, members, issues, resolved):
    print("== Parse issues ==")
    for i in issues:
        print("  " + i)
    ec = Counter((m["term"], m["end_check"]) for m in members)
    print("\n== Members parsed; computed final party == page's end party ==")
    for t in TERMS:
        print(f"  {t}: {sum(v for (tt, _), v in ec.items() if tt == t)} members, "
              f"agree {ec[(t, True)]}, disagree {ec[(t, False)]}")

    print("\n== 1. Coverage ==")
    print("  resolved = speaker-term has spells; full = spells cover first..last; partial = some")
    print("  dates left without a party (listed in the unmatched file as PARTIAL)")
    keys = cand.set_index(["speaker", "assembly_term"]).index
    partial_keys = set(zip(um.speaker[um.reason.str.startswith("PARTIAL")],
                           um.assembly_term[um.reason.str.startswith("PARTIAL")]))
    cand = cand.assign(resolved=keys.isin(list(resolved.keys())),
                       partial=keys.isin(list(partial_keys)))
    def cov(g):
        r = g.resolved
        return pd.Series({
            "speakers": len(g), "resolved": int(r.sum()), "of_which_partial": int(g.partial.sum()),
            "share_speakers": round(r.mean(), 3), "turns": int(g.n_turns.sum()),
            "turns_resolved": int(g.n_turns[r].sum()),
            "share_turns": round(g.n_turns[r].sum() / g.n_turns.sum(), 3)})
    tab = cand.groupby("assembly_term")[["resolved", "partial", "n_turns"]].apply(cov)
    tab.loc["all"] = cov(cand)
    print(tab.astype({"share_speakers": float, "share_turns": float}).to_string())

    print("\n== 2. Agreement with ground truth ==")
    gt = pd.read_csv(GROUND_TRUTH, dtype=str)
    gt = gt[gt.role == "legislator"].copy()
    gt["assembly_term"] = gt.assembly_term.astype(int)
    # Ground-truth speakers are hangul and its dates often fall outside the first..last range
    # of the candidate strings, so compare on the resolved member's full-term timeline: the
    # GT speaker is matched to the member resolved for the same string, else to resolved
    # members whose Wikipedia name equals it (hanja strings). A match by name in a term with
    # namesakes is a possible collision and is listed, not scored.
    namesakes = Counter((m["term"], m["name"]) for m in members)
    by_spk = {k: m for k, (m, _) in resolved.items()}
    by_mname = defaultdict(dict)
    for (s, t), m in by_spk.items():
        by_mname[(m["name"], t)][m["id"]] = m
    rows = []
    for r in gt.itertuples(index=False):
        via = "string"
        if (r.speaker, r.assembly_term) in by_spk:
            ms = {0: by_spk[(r.speaker, r.assembly_term)]}
        else:
            ms = by_mname.get((r.speaker, r.assembly_term), {})
            via = "name, namesakes in term" if namesakes[(r.assembly_term, r.speaker)] > 1 else "name"
        if not ms:
            continue
        d = date.fromisoformat(r.date)
        ours = set()
        for m in ms.values():
            ps = [p for a, b, p, _ in m["spells"] if a <= d <= b]
            if any(w0 <= d <= w1 for w0, w1, _ in m["windows"]):
                ours.add("(uncertain)")
            else:
                ours.add(ps[0] if ps else "(not in office)")
        mine = ours.pop() if len(ours) == 1 else "AMBIGUOUS"
        rows.append({"term": r.assembly_term, "date": r.date, "speaker": r.speaker,
                     "gt_party": r.party, "ours": mine, "via": via,
                     "member": ",".join(m["id"] for m in ms.values())})
    cmp_ = pd.DataFrame(rows)
    cmp_["agree"] = cmp_.gt_party == cmp_.ours
    scored = cmp_[(cmp_.via != "name, namesakes in term") & (cmp_.ours != "(uncertain)")]
    gtn = gt.groupby("assembly_term").size()
    agg = scored.groupby("term").agg(gt_rows_compared=("agree", "size"), agree=("agree", "sum"))
    agg.insert(0, "gt_rows", gtn.reindex(agg.index))
    agg["share"] = (agg.agree / agg.gt_rows_compared).round(3)
    agg.loc["all"] = [len(gt), len(scored), int(scored.agree.sum()), round(scored.agree.mean(), 3)]
    print(agg.astype({"gt_rows": int, "gt_rows_compared": int, "agree": int}).to_string())
    print(f"  not scored: {int((cmp_.ours == '(uncertain)').sum())} rows on dates we leave without a party; "
          f"{int((cmp_.via == 'name, namesakes in term').sum())} rows matched only by a name two members share")
    dis = cmp_[~cmp_.agree].groupby(["term", "speaker", "gt_party", "ours", "via"], dropna=False).agg(
        n=("date", "size"), dates=("date", lambda s: ",".join(sorted(set(s))[:4]))).reset_index()
    print(f"\nRows that differ or are not scored ({int((~cmp_.agree).sum())} rows, {len(dis)} groups):")
    print(dis.to_string(index=False))
    cmp_.to_csv(CACHE / "gt_comparison.csv", index=False)

    print("\n== 3. Integrity ==")
    bad_overlap = bad_cover = 0
    for (s, t), g in spells.groupby(["speaker", "assembly_term"]):
        g = g.sort_values("start_date")
        ds = [(date.fromisoformat(a), date.fromisoformat(b)) for a, b in zip(g.start_date, g.end_date)]
        for (a1, b1), (a2, b2) in zip(ds, ds[1:]):
            if a2 <= b1:
                bad_overlap += 1
        c = cand[(cand.speaker == s) & (cand.assembly_term == t)].iloc[0]
        gap = any(a2 != b1 + timedelta(days=1) for (a1, b1), (a2, b2) in zip(ds, ds[1:]))
        if gap or ds[0][0].isoformat() != c.first_date or ds[-1][1].isoformat() != c.last_date:
            bad_cover += 1
    print(f"  overlapping spells: {bad_overlap}; speaker-terms with a coverage gap or ends not matching "
          f"first/last date: {bad_cover} (expected = the PARTIAL rows: {len(partial_keys)})")
    new = sorted(set(spells.party) - STANDARD_VOCAB)
    print(f"  party names not in the ground-truth vocabulary: {new}")
    tmpl = defaultdict(set)
    for m in members:
        for p, tp in ((m["elected_party"], m["elected_template"]), (m["end_party"], m["end_template"])):
            if p in new:
                tmpl[p].add(tp)
    for p in new:
        print(f"    {p}: template {sorted(tmpl[p]) or '(from a note in the 비고 column)'}; "
              f"{int((spells.party == p).sum())} spells")
    print(f"\nWrote {OUT_SPELLS} ({len(spells)} rows) and {OUT_UNMATCHED} ({len(um)} rows)")


if __name__ == "__main__":
    main()
