"""Build the hackathon textbook corpus: post-1945 Korean history in 25 high-school books, 1954-2025.

Every book is cut to the same span (liberation in 1945 to the end of its narrative) and split into
passages of whole sentences of about 400-700 characters. At most MAX_PER_BOOK passages are kept per
book, taken at even intervals across the span. The text is not preprocessed (no normalization,
stopwords or tokenization). clean() removes layout and OCR debris only: tables, chart values,
running heads with page numbers, captions, quiz blanks, box labels, bullet symbols and margin
line numbers; it rejoins words split by line breaks or stray spaces (Kiwi decides, see kiwi_join);
passages() drops exercise prompts. See build/notes/textbooks.md, "Transformations".

Needs pyarrow, so run it with the textbook project's environment:
  uv run --project ~/Documents/github/research/projects/kr-textbook-bias-2011 python build_textbooks.py
(that environment also has kiwipiepy, used by kiwi_join; the build takes about a minute).
"""
import csv
import json
import re
import unicodedata
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "textbooks" / "data.csv"
GH = Path.home() / "Documents/github"
TB = GH / "research/projects/kr-textbook-bias-2011/data"
NIKH = GH / "resources/nlp_corpora/data/nikh/nikh_corpus.csv"
MAX_PER_BOOK = 60
MIN_CHARS, TARGET, MAX_CHARS = 150, 400, 700

# book_id, title, publisher, year, curriculum, era, authorization, source, cut
BOOKS = [
    ("ta_h11", "우리 나라 문화사 (고등 국사)", "정음사 (홍이섭)", 1954, "1st", "authoritarian", "검인정", "nikh",
     ("3. 대한민국의 성립과 우리의 사명\n\n1945", "〔끝〕")),
    ("ta_h21", "국사", "문교부", 1963, "2nd", "authoritarian", "국정", "nikh",
     ("4. 대한 민국의 수립과 시련\n\n민족의 해방", "[판권]")),
    ("ta_h31", "고등학교 국사", "문교부", 1973, "3rd", "authoritarian", "국정", "parquet",
     ("Ⅴ. 현대 사회\n\n1\\.", "[판권]")),
    ("ta_h42", "고등학교 국사 (하)", "문교부", 1981, "4th", "authoritarian", "국정", "parquet",
     ("LAST:Ⅲ. 현대 사회의 발달", "[판권]")),
    ("ta_h52", "고등학교 국사 (하)", "교육부", 1987, "5th", "authoritarian", "국정", "parquet",
     ("LAST:Ⅳ. 현대 사회의 전개", "[판권]")),
    ("ta_h62", "고등학교 국사 (하)", "교육부", 1995, "6th", "democratic-state", "국정", "parquet", "spans"),
    ("ta_h71", "고등학교 국사", "교육인적자원부", 2002, "7th", "democratic-state", "국정", "parquet", "spans"),
    ("H-5(1,2007)", "한국근현대사", "금성출판사", 2007, "7th", "2000s-certified", "검정", "parquet", "spans"),
    ("H-6(1,2007)", "한국근현대사", "중앙교육진흥연구소", 2007, "7th", "2000s-certified", "검정", "parquet", "spans"),
    ("H-7(1,2007)", "한국근현대사", "법문사", 2007, "7th", "2000s-certified", "검정", "parquet", "spans"),
    ("H-8(1,2007)", "한국근현대사", "두산", 2007, "7th", "2000s-certified", "검정", "parquet", "spans"),
    ("H-9(5,2007)", "한국근현대사", "대한교과서", 2007, "7th", "2000s-certified", "검정", "parquet", "spans"),
    ("H-10(4,2007)", "한국근현대사", "천재교육", 2007, "7th", "2000s-certified", "검정", "parquet", "spans"),
    ("H11-mirae", "고등학교 한국사", "미래엔", 2011, "2009 revised", "2011+-certified", "검정", "ocr", "units"),
    ("H11-visang", "고등학교 한국사", "비상교육", 2011, "2009 revised", "2011+-certified", "검정", "ocr", "units"),
    ("H11-samhwa", "고등학교 한국사", "삼화출판사", 2011, "2009 revised", "2011+-certified", "검정", "ocr", "units"),
    ("H11-jihaksa", "고등학교 한국사", "지학사", 2011, "2009 revised", "2011+-certified", "검정", "ocr", "units"),
    ("H11-chunjae", "고등학교 한국사", "천재교육", 2011, "2009 revised", "2011+-certified", "검정", "ocr", "units"),
    ("H11-bubmunsa", "고등학교 한국사", "법문사", 2011, "2009 revised", "2011+-certified", "검정", "bubmunsa", None),
    ("H-54(2,2016)", "한국사", "금성출판사", 2016, "2009 revised", "2011+-certified", "검정", "parquet",
     ("6-1 8·15 광복과 대한민국 정부의 수립\n6-2", "되돌아보기")),
    ("H-57(1,2016)", "한국사", "지학사", 2016, "2009 revised", "2011+-certified", "검정", "parquet",
     ("01 광복과 대한민국 정부의 수립", "연표로 정리하기")),
    ("H25-visang-v2", "고등학교 한국사 2", "비상교육", 2025, "2022 revised", "2011+-certified", "검정", "ocr", (74, 157)),
    ("H25-cmass-v2", "고등학교 한국사 2", "씨마스", 2025, "2022 revised", "2011+-certified", "검정", "ocr", (68, 163)),
]

DROP_LINE = re.compile(r"^\s*(\||:?-{3}|https?://|.*https?://|[□✓√☐■▶▷◀※]|\[.{0,20}\]$|!\[)")
REVIEW_PAGE = re.compile(r"마무리|평가 문제|수행 평가|활동지|찾아보기|연표")

# ---- Layout and OCR repair (see the corpus card, "Transformations") ----
# Books typed from the printed page (NIKH state books): their line breaks fall between words.
TYPED = ("ta_",)
# Middle-dot look-alikes used by the sources for the Korean middle dot (8·15, 미·소).
MIDDOT = str.maketrans({"⋅": "·", "․": "·", "ㆍ": "·"})
SENT_END = re.compile(r"[.?!][\"'’”)\]」』]*(\s|$)")
# Running heads: "248 IV 현대 사회의 발전" (even pages) and "2. 민주주의의 시련과 발전 | 289" (odd pages).
SEP = r"\s*(?:\||_|•{1,2}|·|>{2,3}|\.)?\s*"
NUM = r"(?:\d{1,2}|[IVX]{1,4}|[Ⅰ-Ⅻ])"
UNITS = ["현대 사회의 발전", "대한민국의 발전과 국제 정세의 변화", "대한민국의 발전과 현대 세계의 변화",
         "냉전 체제와 대한민국 정부의 수립", "오늘날의 대한민국", "세계화와 우리의 미래", "대한민국의 발전"]


def loose(s: str) -> str:
    """Regex for s that tolerates any spacing between its characters."""
    return r"\s*".join(re.escape(c) for c in s.replace(" ", ""))


UNIT_HEAD = re.compile(r"(?<!\d)\d{2,3}" + SEP + r"(?:[IVX]{1,4}|[Ⅰ-Ⅻ]|\d)\s*[.·]?\s*(?:"
                       + "|".join(loose(u) for u in UNITS) + r")(?:\s*" + NUM + r"\s*-\s*\d(?!\d))?")
CHAP_NO = r"(?:" + NUM + r"\s*(?:장\s*/|[-.·]\s*\d{0,2}\s*\.?)?\s*)"
TITLE = r"([가-힣][가-힣0-9·,\s]{1,38}?)"
PAGE = r"(\d{2,3})(?!\d|\s*(?:년|월|일|명|개|만|억|%|여(?:\s|명)))"
CHAP_LINE = re.compile(r"^" + CHAP_NO + "?" + TITLE + SEP + r"(\d{2,3})$")       # a whole line
CHAP_START = re.compile(r"^" + CHAP_NO + TITLE + SEP + PAGE + r"(?=\s)")         # head, then body text
CHAP_END = re.compile(r"(?:^|\s)" + CHAP_NO + TITLE + SEP + r"(\d{2,3})$")      # body text, then head
CAPTION = re.compile(r"^[↑▲▼△]")                   # photo and map captions in the 2007 and OCR books
MARKER = re.compile(r"^[•●○◎◇◆■□▶▷►*>\-–]+\s*")     # bullets and markers at the start of a line
QUIZ = re.compile(r"_{3,}|□{2,}|\(\s*\)\s*(?:을|를)")
SYMBOLS = re.compile(r"[①-⑳㉠-㉿㈀-㈞•●◎◇◆■□▲△▼▽▶▷►◀※↑↓→←✓√☐▦*_]|>{2,}"
                     r"|(?<!\S)[>○](?!\S)|(?<![가-힣])\(?[ㄱ-ㅎ][.)]?(?![가-힣])")
BOX_LABEL = re.compile(r"(?:자료\s*\d*\s*)?(?:도움글|자료\s?읽기)\s*\||\|\s*자료\s*\d+\s*\||\[자료\s*\d+\]")
# Labels spelled out one syllable at a time: 자 / 료 / 읽 / 기, 역·사·의·현·장 (country lists such as
# 미·영·소·중 have at most four syllables and are kept).
SPELLED = re.compile(r"(?<![가-힣])[가-힣](?:\s?/\s?[가-힣]){2,}(?![가-힣])|(?<![가-힣])[가-힣](?:·[가-힣]){4,}(?![가-힣])")
SECTION_NO = re.compile(r"(?<!\S)(?:[IVX]{1,4}|[Ⅰ-Ⅻ])\s*-\s*\d(?!\S)")
# OCR books: the line numbers printed in the margin (5, 10, 15, 20) end up between two words.
MARGIN_NO = re.compile(r"(?<=[가-힣,.]) (?:5|10|15|20|25) (?=[가-힣])"
                       r"(?!천|백|위|건|배|번|회|호|등|세|살|척|대|곳|가지|퍼센트|인|여)")
NOT_MARGIN = re.compile(r"(?:(?:^|[\s(])(?:자료|주제|모둠|단계|세계|연간|무려|약|총|제|각|그|이|단|전|후)|\d\.)$")


def drop_margin_numbers(line: str) -> str:
    return MARGIN_NO.sub(lambda m: m.group() if NOT_MARGIN.search(line[:m.start()]) else " ", line)
# A number split from its counter: 1970 년대, 5 개년, 3 차 -> 1970년대, 5개년, 3차.
UNIT_SPACE = re.compile(r"(?<=\d) (?=(?:년|월|일|세기|명|개|대|차|만|억|원)(?!본|통령|한|주|조|관|령|혁|발|최|방|편|표|중|체|립|우|회|륙))")
# Recurring misreadings (ㅜ read as ㅗ) found in several books; each match was checked by hand.
MISREAD = [(re.compile(r"(?<=인도네시아 )반동|(?<=인도네시아의 )반동|반동(?= 회의)"), "반둥"),  # Bandung, 1955
           (re.compile(r"이기봉"), "이기붕")]                                               # Lee Ki-poong
# Textbook apparatus labels (feature boxes, exercises), removed wherever they occur ...
LABELS = re.compile(r"학습\s?목표\s*:?[^.?!]*[.?!]?|(?:주제|생각|탐구)\s?열기|(?:주제|모둠)\s\d{1,2}(?=\s)|탐구\s?(?:활동|과제)(?:\s*\d+)?|열린\s?과제|연구\s?과제"
                    r"|자기\s?주도\s?학습의\s?길잡이|개념\s?이해(?:\s*\d+)?|확인\s?학습|자료로\s?이해하기|역사\s?더\s?알기"
                    r"|더\s?알아보기|알아봅시다|심화\s?학습|사진\s?읽기|주요\s?용어|읽기\s?자료|자료\s?읽기|도움글"
                    r"|(?:대|중)?단원\s?(?:마무리(?:하기)?|개관)|【개요】|Step\s?\d")
# ... and numbered box labels at the start of a line (자료 3, 주제 05, 모둠 1).
LINE_LABEL = re.compile(r"^(?:자료|주제|모둠)\s*\d{1,2}(?:\s*[·,.~]\s*\d{1,2})*\.?(?=\s|$)")
# Exercise prompts, dropped as whole sentences: "~해 보자.", "~하시오.", questions about 자료 N.
PROMPT = re.compile(r"(?:보자|봅시다|시오)[.?!]?[\"'’”)]*$|자료\s*\d.*\?[\"'’”)]*$")
NUMBER_ONLY = re.compile(r"^[가-힣]{1,6}(?:\s[가-힣]{1,6})?\s\d{1,2}\.$")  # "열린 과제 1." left by the split


def running_heads(lines: list[str]) -> re.Pattern | None:
    """Chapter titles printed next to a page number twice, or once at the start of a line after a
    chapter number (2. 민주주의의 시련과 발전 267 장면 내각)."""
    pages: dict[str, set] = {}
    for line in lines:
        for pat in (CHAP_LINE, CHAP_START, CHAP_END):
            m = pat.search(line)
            if m:
                pages.setdefault(re.sub(r"\s+", "", m.group(1)), set()).add(m.group(2))
        m = CHAP_START.match(line)
        if m and len(m.group(1).replace(" ", "")) >= 6 and len(m.group(2)) == 3:
            pages.setdefault(re.sub(r"\s+", "", m.group(1)), set()).add("start")  # numbered head, then text
    titles = sorted((t for t, p in pages.items() if len(p) >= 2 and len(t) >= 4 and not re.search(r"[\d,]", t)),
                    key=len, reverse=True)
    if not titles:
        return None
    return re.compile(CHAP_NO + "?(?:" + "|".join(loose(t) for t in titles) + r")" + SEP + PAGE)


def table_row(line: str) -> bool:
    cells = [c.strip() for c in line.split("|") if c.strip()]
    return line.count("|") >= 2 and all(len(c) <= 30 for c in cells)


def mostly_numbers(line: str) -> bool:
    """Chart values, axis labels and timeline rows (not sentences; 4·19 and 6·25 count as words)."""
    if SENT_END.search(line):
        return False
    chars = re.sub(r"\s", "", re.sub(r"\d+·\d+", "가", line))
    letters = len(re.findall(r"[가-힣A-Za-z一-鿿]", chars))
    return bool(chars) and letters < 0.4 * len(chars)


def unwrap(lines: list[str]) -> list[str]:
    """Typed books wrap paragraphs at spaces: join each paragraph into one line (table rows apart)."""
    out, cur = [], []
    for line in lines + [""]:
        if line and "|" not in line and not line.startswith("---"):
            cur.append(line)
            continue
        if cur:
            out.append(" ".join(cur))
            cur = []
        out.append(line)
    return out


_kiwi = None


DEPENDENT = ("J", "E", "XSN", "XSV", "XSA", "VCP")  # particles, endings, suffixes, copula


def kiwi_join(x: str, y: str, cross: bool = True) -> bool:
    """True if the space between the words x and y splits one word: (1) y is a lone sentence-final 다 (었 다.);
    (2) Kiwi, reading "x y" with the space, still takes y to start with a particle, ending, suffix
    or copula (비판 하였다, 도구 였다); or (3) Kiwi scores the joined form at least 5 log-points
    higher (2 before the suffix 하/되) and the junction falls before such a morpheme or, if cross,
    cuts through a morpheme (요 청하였다, 이승 만)."""
    global _kiwi
    if re.fullmatch(r"다[.?!\"'’”)]+", y) or (y == "다" and re.search(r"[었였았했됐겠]$", x)):
        return True
    if _kiwi is None:
        from kiwipiepy import Kiwi
        _kiwi = Kiwi()
    spaced = _kiwi.analyze(x + " " + y, top_n=1)[0]
    first = next((t for t in spaced[0] if t.start >= len(x) + 1), None)
    if first is not None and first.start == len(x) + 1 and first.tag.startswith(DEPENDENT):
        return True
    joined = _kiwi.analyze(x + y, top_n=1)[0]
    gain = joined[1] - spaced[1]
    for t in joined[0]:
        if t.start < len(x) < t.start + t.len:
            return cross and gain >= 4.99
        if t.start == len(x):
            # 제정 하고, 실시 된: a verb-forming suffix needs a smaller gain.
            return t.tag.startswith(DEPENDENT) and gain >= (2 if t.tag in ("XSV", "XSA") else 4.99)
    return False


def respace(line: str) -> str:
    """Rejoin words split by a stray space inside a line (non-typed books only). Two words of two
    or more syllables are joined only before a particle or ending, so that the source's own
    spacing of compounds (대한 민국, 사회 단체) is kept."""
    words = line.split(" ")
    out = words[:1]
    for w in words[1:]:
        x = out[-1]
        if re.search(r"[가-힣]$", x) and re.match(r"[가-힣]", w):
            short = len(re.search(r"[가-힣]+$", x).group()) == 1 or len(re.match(r"[가-힣]+", w).group()) == 1
            if kiwi_join(x, w, cross=short):
                out[-1] = x + w
                continue
        out.append(w)
    return " ".join(out)


def clean(text: str, book_id: str = "") -> str:
    typed = book_id.startswith(TYPED)
    lines = [re.sub(r"^#+\s*", "", l).replace("\\.", ".").replace("**", "").translate(MIDDOT).strip()
             for l in text.splitlines()]
    if typed:
        lines = unwrap(lines)
    heads = running_heads(lines)
    paras: list[list[str]] = [[]]
    for line in lines:
        if heads:
            line = heads.sub(" ", line).strip()
        line = UNIT_HEAD.sub(" ", line).strip()
        if not line:
            paras.append([])  # a blank line ends the paragraph
            continue
        if (DROP_LINE.match(line) or table_row(line) or mostly_numbers(line) or QUIZ.search(line)
                or CAPTION.match(line) or CHAP_LINE.match(line)):
            continue
        if MARKER.match(line) and not SENT_END.search(line) and len(line) <= 40:
            continue  # a marked heading or label without a sentence
        line = BOX_LABEL.sub(" ", line)
        line = LINE_LABEL.sub(" ", LABELS.sub(" ", line)).strip()
        line = re.sub(r"[①-⑳](?=[가-힣,])", lambda m: unicodedata.normalize("NFKC", m.group()), line)  # ①이 -> 1이
        line = SYMBOLS.sub(" ", line).replace("|", " ")
        line = SECTION_NO.sub(" ", line)
        line = re.sub(r"(?<=[가-힣0-9]) *· *(?=[가-힣0-9])", "·", line)  # 6 · 25 -> 6·25
        line = SPELLED.sub(" ", line)
        line = re.sub(r"(?<=[가-힣0-9)]) +(?=[.,?!])", "", line)        # 되었다 . -> 되었다.
        line = re.sub(r"\( +", "(", re.sub(r" +\)", ")", line))
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            continue
        if not typed:
            line = UNIT_SPACE.sub("", line)
            line = drop_margin_numbers(line)
            line = respace(line)
        paras[-1].append(line)
    out = []
    for para in paras:
        if not para:
            continue
        text = para[0]
        for nxt in para[1:]:
            x, y = text.rsplit(" ", 1)[-1], nxt.split(" ", 1)[0]
            glue = (not typed and not SENT_END.search(text[-3:] + " ")
                    and re.search(r"[가-힣]$", x) and re.match(r"[가-힣]", y) and kiwi_join(x, y))
            text = text + ("" if glue else " ") + nxt
        out.append(text)
    text = re.sub(r"(?<=[가-힣0-9]) *· *(?=[가-힣0-9])", "·", " ".join(out))  # also across line breaks
    text = UNIT_HEAD.sub(" ", heads.sub(" ", text) if heads else text)       # heads split over two lines
    for pat, right in MISREAD:
        text = pat.sub(right, text)
    return re.sub(r"\s+", " ", text).strip()


def passages(text: str) -> list[str]:
    sentences = [s.strip() for s in re.split(r"(?<=[.?!])\s+", text) if s.strip()]
    sentences = [s for s in sentences if not PROMPT.search(s) and not NUMBER_ONLY.match(s)]
    out, cur = [], ""
    for s in sentences:
        if cur and len(cur) + len(s) + 1 > MAX_CHARS:
            out.append(cur)
            cur = ""
        cur = f"{cur} {s}".strip()
        if len(cur) >= TARGET:
            out.append(cur)
            cur = ""
    if cur:
        out.append(cur)
    return [p for p in out if len(p) >= MIN_CHARS]


def ocr_pages(book_id: str) -> dict[int, dict]:
    path = TB / "ocr_pages/corrected" / f"{book_id}.jsonl"
    if not path.exists():
        path = TB / "ocr_pages" / f"{book_id}.jsonl"
    pages: dict[int, dict] = {}
    for line in path.open(encoding="utf-8"):
        r = json.loads(line)
        if r["page"] not in pages or r.get("attempt", 1) >= pages[r["page"]].get("attempt", 1):
            pages[r["page"]] = r
    return pages


def ocr_span(book_id: str, first: int, last: int) -> str:
    pages = ocr_pages(book_id)
    parts = []
    for p in range(first, last + 1):
        r = pages.get(p)
        if not r or r["page_type"] != "body":
            continue
        main = r["text"].split("=== BOXES ===")[0]
        if REVIEW_PAGE.search(main.strip()[:60]):
            continue
        parts.append(main)
    return "\n".join(parts)


def main() -> None:
    comp = pd.read_parquet(TB / "comparison/comparison_books.parquet").set_index("book_id").full_text
    nikh = pd.read_csv(NIKH).set_index("book_id").full_text
    spans = pd.read_csv(TB / "derived/ext/unit_spans.csv")
    units = pd.read_csv(TB / "derived/unit_map.csv")

    rows = []
    for book_id, title, publisher, year, curriculum, era, auth, source, cut in BOOKS:
        if source == "bubmunsa":
            lines = (TB / "texts/H11-bubmunsa.txt").read_text(encoding="utf-8").splitlines()
            start = next(i for i, l in enumerate(lines) if l.startswith("Ⅷ 냉전 체제와 대한민국"))
            raw = "\n".join(lines[start:])
        elif source == "ocr" and cut == "units":
            u = units[(units.book_id == book_id) & units.unit.isin(["Ⅷ", "Ⅸ"])]
            raw = ocr_span(book_id, int(u.start_page.min()), int(u.end_page.max()))
        elif source == "ocr":
            raw = ocr_span(book_id, *cut)
        elif cut == "spans":
            full = comp[book_id]
            s = spans[(spans.source_id == book_id) & spans.labels.str.contains("Ⅷ|Ⅸ")]
            raw = "\n".join(full[a:b] for a, b in zip(s.start, s.end))
        else:
            full = (nikh if source == "nikh" else comp)[book_id]
            a = full.rindex(cut[0][5:]) if cut[0].startswith("LAST:") else full.index(cut[0])
            b = full.index(cut[1], a) if cut[1] else len(full)
            raw = full[a:b]
        ps = passages(clean(raw, book_id))
        n_all = len(ps)
        if n_all > MAX_PER_BOOK:
            idx = np.unique(np.linspace(0, n_all - 1, MAX_PER_BOOK).round().astype(int))
        else:
            idx = np.arange(n_all)
        safe = re.sub(r"[^A-Za-z0-9]+", "-", book_id).strip("-").lower()
        for i in idx:
            rows.append({
                "id": f"{safe}-{i + 1:03d}", "book_id": book_id, "title": title, "publisher": publisher,
                "year": year, "curriculum": curriculum, "era": era, "authorization": auth,
                "passage_no": int(i) + 1, "share_of_span": round(i / max(n_all - 1, 1), 3),
                "text": ps[i], "n_chars": len(ps[i]),
            })
        print(f"{book_id:16} {year} {era:17} span {len(raw):>7} chars  passages {n_all:>4}  kept {len(idx)}")

    df = pd.DataFrame(rows)
    df.to_csv(OUT, index=False, encoding="utf-8", quoting=csv.QUOTE_MINIMAL)
    print(f"\n{len(df)} rows, {OUT.stat().st_size / 1e6:.2f} MB")
    print(df.groupby("era", sort=False).agg(books=("book_id", "nunique"), rows=("id", "size")).to_string())
    print("n_chars:", df.n_chars.describe().round().to_dict(), " duplicates:", df.text.duplicated().sum())


if __name__ == "__main__":
    main()
