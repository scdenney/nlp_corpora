# North Korean Economics Journal Corpus

## Overview

This corpus contains articles from a North Korean economics journal spanning **1987–2020**: the Kyŏngje Yŏngu (경제연구, "Economic Research"). It provides a rare, longitudinal window into how the Democratic People's Republic of Korea (DPRK) discusses economic policy, ideology, and development priorities. The journal functions as a key medium through which the state articulates economic doctrine and signals its official line on planning, production, foreign trade, technocratic reforms, and the relationship between economic goals and the ideological foundations of the regime.

Across this period North Korea experienced dramatic transformations: the collapse of the socialist trading bloc, the "Arduous March" famine years, partial marketization and institutional adjustment, nuclear development under tightening sanctions, the *byungjin* (병진) line and its April 2018 pivot to "socialist economic construction," and shifting strategies under three different leaders. The texts in this corpus reflect these turning points through changes in terminology, framing, priorities, slogans, and emphases on self-reliance, science and technology, productivity, agriculture, or defense.

Read more about the journal at [38 North](https://www.38north.org/2025/05/in-memoriam-kyongje-yongu/).

> **2026 update.** The corpus was extended from 1987–2017 to **1987–2020** (+454 articles, 2,582 → 3,036). The 1987 to 2017-3 baseline is preserved verbatim; 2017-4 onward was newly extracted from the publisher's article files. A `source` column records the provenance of every row. See [Provenance and the 2017–2020 extension](#provenance-and-the-20172020-extension).

> **2026-09 update: version 2.** `kjyg_v2.parquet` / `kjyg_v2.csv` complete the corpus: **3,136 articles, all 136 issue-quarters**. The 82 articles with no text are filled from scans (81; one has no surviving scan) and the three missing issues 1995-4, 2019-4 and 2020-3 are added. Every v1 row is kept. The v1 files (`kjyg.parquet`, `kjyg.csv`) are unchanged. See [Version 2 (2026-09): the scan supplement](#version-2-2026-09-the-scan-supplement).

---

## Variables Included

7 columns, 3,036 rows. Each row is one journal article.

| Variable | Type | Description |
|----------|------|-------------|
| **title** | string | Article title as published in the journal, in DPRK Korean orthography. 3,019 unique values; titles are not guaranteed unique (a handful recur across years/authors). |
| **author** | string | Author(s) listed for the article. 1,847 unique authors. **38 missing values** (unsigned editorials, leader-tribute pieces, and short 상식/glossary entries). |
| **year_issue** | string | Combined year and quarterly issue number in `YYYY-N` format (e.g., `1987-1`, `2020-4`). 133 unique values. The journal is published quarterly (4 issues per year). |
| **word_count** | integer | Whitespace-delimited token (eojeol) count of the article text. Range 0–3,346; median 924; mean 974. Consistent across sources (~5.3 characters per token). |
| **file_path** | string | Original source path, retained as a provenance trail (Windows JSON paths for the baseline; relative docx/PDF paths for 2017–2020). Not functional on other systems. |
| **content** | string | Full article text in Korean (DPRK orthography). Median ~4,900 characters; max ~16,814. **82 missing values** (all in the baseline). |
| **source** | string | Extraction provenance: `original_json` (1987..2017-3 baseline), `docx` (2017-4, 2018), `pdf_text` (2019-1/2/3, 2020-1/2/4). Useful for quality weighting — see notes below. |

---

## Temporal Distribution

The journal is quarterly, with steadily increasing output over the decades:

| Decade | Articles | Historical Context |
|--------|----------|--------------------|
| 1980s (1987–89) | 116 | Late socialist planning under Kim Il-sung (김일성, KIS) |
| 1990s | 591 | Soviet collapse; "Arduous March" famine (고난의 행군) under Kim Jong-il (김정일, KJI) |
| 2000s | 813 | Partial marketization and institutional adjustment (KJI) |
| 2010s | 1,404 | Kim Jong-un (김정은, KJU); *byungjin* (병진) line; sanctions era |
| 2020s (2020) | 112 | Self-reliance / "frontal breakthrough" (정면돌파전) under intensified sanctions and COVID-19 border closure |

Article output peaks in 2016 (170 articles). The four quarterly issues are roughly evenly distributed.

**Coverage gaps.** Three quarterly issues are absent from the underlying materials: **1995-4** (already missing in the baseline), **2019-4**, and **2020-3** (the genuine 루계 188 — the file shipped under that name is a different journal; see below). The corpus therefore holds 133 of a possible 136 issue-quarters for 1987–2020.

---

## Provenance and the 2017–2020 extension

The 1987 to 2017-3 baseline (2,582 rows, `source = original_json`) is the originally published corpus, derived from per-article JSON files and left **unchanged**. The extension adds 454 articles from the publisher's article files:

| Period | Source files | `source` | Articles | Extraction |
|--------|--------------|----------|----------|------------|
| 2017-4, 2018-1..4 | one `.docx` per article | `docx` | 219 | Title/author from filename + the 저자/출처 metadata line; body text minus title echo and metadata. |
| 2019-1/2/3, 2020-1/2/4 | full-issue `.pdf` (digital text layer) | `pdf_text` | 235 | Articles segmented by 16pt centered titles; authors matched from the table of contents (차례) by printed page; two-column reading order reconstructed. |

The build is reproducible from `build_kjyg_2017_2020.py` (+ `kjyg_extract.py`); a machine-readable summary is in `kjyg_build_qa.json`. Raw docx/PDF sources are held in the research project, not in this repository, mirroring the baseline (which shipped processed text only).

**Quality note on `pdf_text`.** The 2019–2020 rows are extracted from the PDFs' embedded text layer (not OCR), and a completeness spot-check matched extracted characters to raw page characters to within rounding. They nonetheless carry the usual digital-typesetting artifacts (occasional missing spaces where lines wrapped). Researchers wanting the cleanest subset can filter to `source != "pdf_text"`.

**Leader-name honorific font.** DPRK journals render the names 김일성 / 김정일 / 김정은 in a special honorific font that maps to Private-Use-Area codepoints; these codepoints vary by file. They were decoded to plain text via per-file derivation from reliable epithet contexts (위대한 수령 → 김일성, 위대한 령도자 → 김정일, 경애하는 최고령도자 → 김정은). No PUA glyphs remain in the corpus.

**Excluded misfiled issue.** A file named `경제연구 2020-3.pdf` is in fact an issue of **력사과학 (Ryŏksa Kwahak, "Historical Science," 루계 255)** — its articles are on Goguryeo, Balhae, the Imjin War, etc. A journal-identity guard in the build script rejects it, so no history articles enter this economics corpus.

---

## Version 2 (2026-09): the scan supplement

Version 2 (`kjyg_v2.parquet`, `kjyg_v2.csv`) has the same seven columns as version 1 and keeps all 3,036 version-1 rows with their title, author, issue and file path. It changes the 81 empty rows it could fill and adds 100 articles:

| Change | Articles | `source` | Method |
|--------|----------|----------|--------|
| Empty v1 articles filled | 81 of 82 | `ocr_2026_09` | OCR of scans of the printed articles |
| Issue 1995-4 added | 16 | `ocr_2026_09` | OCR of a scan of the full issue; authors from its table of contents |
| Issue 2019-4 added | 47 | `pdf_text` | PDF text layer, same extractor as the other 2019–20 issues |
| Issue 2020-3 added | 37 | `pdf_text` | PDF text layer of the genuine 루계 188 |

Result: **3,136 articles; 136 of 136 issue-quarters.** `source`: `original_json` 2,501 · `docx` 219 · `pdf_text` 319 · `ocr_2026_09` 97. One article still has no text: 2011-3 「미국식금융방식의 부당성」 (리원경), for which no scan was found.

**OCR.** Scans were read at 300 dpi by a vision-language model, Qwen3.6-35B-A3B (FP8) served with vLLM, prompted with each page's year, issue, the leaders who can be named at that date, and (for single articles) the title and author. The text then went through four logged correction layers:

1. 89 spelling rules that convert South Korean forms the rest of the corpus never uses (화폐, 노동, 컴퓨터 …) to DPRK forms, and correct a leader's name that is impossible at the page's date. Run over all 15.4 million characters of version 1, they change 21.
2. 22 pairs of look-alike syllables (판/관, 전/건, 법/범 …), swapped only where the syllable as read makes a three-character sequence never seen in version 1 and the swap makes well-attested ones. Run over version 1, they change nothing.
3. 297 reviewed corrections: every word with an unattested three-character sequence that a second OCR model (dots.mocr) read differently was checked against that reading, the corpus and, where needed, the scan (by a language model, Claude Opus, not a person).
4. Six pages read in full against the scan replace the OCR text.

DPRK orthography is never normalized. **Accuracy:** character error rate on Hangul against pages read in full from the scans is about **0.2%** on two randomly drawn pages (0.79% before correction). The reference pages were themselves read by a model, so treat this as a close estimate.

**Text-layer note.** On about eight pages of 2019-4 and 2020-3 the PDF text layer holds passages in a different order from the printed page; the text is complete (checked against an OCR reading), only the order differs.

**Which file to use.** Version 2 for complete coverage. Version 1 stays unchanged so that work built on it remains reproducible. To exclude transcribed text, filter `source != "ocr_2026_09"`; to recover the version-1 composition, keep `source != "ocr_2026_09"` and drop the issues 1995-4, 2019-4 and 2020-3 (the 81 filled rows were empty in version 1).

| Decade | v2 articles |
|--------|-------------|
| 1980s (1987–89) | 116 |
| 1990s | 607 |
| 2000s | 813 |
| 2010s | 1,451 |
| 2020 | 149 |

A per-article build summary (which scan pages, where each article was cut, word counts) is in `kjyg_build_qa_v2.json`. The OCR pipeline and scans are held in the research project (Denney & Ward, *No Previews in Pyongyang*), not in this repository.

---

## Suggested Derived Variables

The following variables are not stored but are straightforward to derive from `year_issue`:

| Variable | How to Derive | Values |
|----------|---------------|--------|
| **year** | Split `year_issue` on `-`, take the first element | 1987–2020 (integer) |
| **issue** | Split `year_issue` on `-`, take the second element | 1, 2, 3, or 4 (integer) |
| **leader_period** | ≤1994 → `KIS`, 1995–2011 → `KJI`, ≥2012 → `KJU` | Kim Il-sung / Kim Jong-il / Kim Jong-un |
| **economic_era** | 1987–1990 `late_socialist_planning`; 1991–1998 `collapse_arduous_march`; 1999–2011 `marketization_adjustment`; 2012–2017 `byungjin_sanctions`; 2018–2020 `frontal_breakthrough` | 5 categories (the 2018–2020 boundary follows the April 2018 line change; refine to taste) |
| **decade** | Based on year | `1980s`–`2020s` |
| **log_word_count** | `log1p(word_count)` | Continuous |

---

## DPRK Orthographic Notes

North Korean texts use spelling conventions that differ from South Korean standard orthography. Key differences visible in this corpus include:

| DPRK Spelling | South Korean Equivalent | Meaning |
|---------------|------------------------|---------|
| 로동 | 노동 | Labor |
| 령도 | 영도 | Leadership |
| 에네르기 | 에너지 | Energy |
| 녀성 | 여성 | Women |
| 리용 | 이용 | Utilization |
| 동무 | — | Comrade (rarely used in the South) |

Researchers applying South Korean NLP tools (tokenizers, morphological analyzers) should be aware that these tools may not handle DPRK orthography well without adaptation.

---

## Sample Titles with Translations

| Year | Korean Title | English Translation |
|------|-------------|---------------------|
| 1987 | 친애하는 지도자 김정일동지의 세련된 령도밑에 보다 높은 단계에로 발전하고있는 우리 나라 경제 | "Our Nation's Economy Developing to a Higher Stage Under the Refined Leadership of Dear Leader Comrade Kim Jong-il" |
| 2005 | 독립채산제기업소자체충당금과 그 적립리용에서 나서는 중요문제 | "Important Issues Arising in the Accumulation and Use of Self-Financing Reserves at Independent Accounting Enterprises" |
| 2015 | 대외결제은행들에서 경영위험과 그 평가방법 | "Management Risk and Its Evaluation Methods in Foreign Settlement Banks" |
| 2020 | 과감한 정면돌파전으로 사회주의경제건설의 새로운 활로를 열어나가자 | "Open a New Path for Socialist Economic Construction Through a Bold Frontal Breakthrough" (editorial) |
| 2020 | 기업체들에 부여된 가격제정권을 활용하는데서 나서는 중요한 요구 | "Important Requirements in Utilizing the Price-Setting Authority Granted to Enterprises" |

---

## Data Quality Notes

- **82 rows** have missing `content` and **38 rows** have missing `author` (unsigned editorials, leader-tribute pieces, and short 상식/glossary entries).
- The `file_path` column is provenance only and is not functional on other systems.
- For the cleanest text subset, filter to `source != "pdf_text"`; for the original published corpus, filter to `source == "original_json"`.
- **Version 2:** 1 row has no text and 52 rows have no author; `ocr_2026_09` rows carry a residual character error rate of about 0.2%.

---

## File Formats

- **kjyg.parquet** — the complete corpus (recommended for analysis): `pd.read_parquet("kjyg.parquet")`.
- **kjyg.csv** — the same data as UTF-8 CSV.
- **build_kjyg_2017_2020.py**, **kjyg_extract.py** — reproducible build pipeline for the 2017–2020 extension.
- **kjyg_build_qa.json** — machine-readable build summary (counts, gaps, skipped files).
- **kjyg_v2.parquet**, **kjyg_v2.csv** — version 2 (2026-09): the complete corpus, 3,136 articles, all 136 issue-quarters.
- **kjyg_build_qa_v2.json** — version-2 build summary (per-article scan pages, cuts and word counts; the 1995-4 issue).
