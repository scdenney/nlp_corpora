# North Korean Economics Journal Corpus

## Overview

This corpus contains articles from a North Korean economics journal spanning **1987–2020**: the Kyŏngje Yŏngu (경제연구, "Economic Research"). It provides a rare, longitudinal window into how the Democratic People's Republic of Korea (DPRK) discusses economic policy, ideology, and development priorities. The journal functions as a key medium through which the state articulates economic doctrine and signals its official line on planning, production, foreign trade, technocratic reforms, and the relationship between economic goals and the ideological foundations of the regime.

Across this period North Korea experienced dramatic transformations: the collapse of the socialist trading bloc, the "Arduous March" famine years, partial marketization and institutional adjustment, nuclear development under tightening sanctions, the *byungjin* (병진) line and its April 2018 pivot to "socialist economic construction," and shifting strategies under three different leaders. The texts in this corpus reflect these turning points through changes in terminology, framing, priorities, slogans, and emphases on self-reliance, science and technology, productivity, agriculture, or defense.

Read more about the journal at [38 North](https://www.38north.org/2025/05/in-memoriam-kyongje-yongu/).

> **2026 update.** The corpus was extended from 1987–2017 to **1987–2020** (+454 articles, 2,582 → 3,036). The 1987 to 2017-3 baseline is preserved verbatim; 2017-4 onward was newly extracted from the publisher's article files. A `source` column records the provenance of every row. See [Provenance and the 2017–2020 extension](#provenance-and-the-20172020-extension).

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

---

## File Formats

- **kjyg.parquet** — the complete corpus (recommended for analysis): `pd.read_parquet("kjyg.parquet")`.
- **kjyg.csv** — the same data as UTF-8 CSV.
- **build_kjyg_2017_2020.py**, **kjyg_extract.py** — reproducible build pipeline for the 2017–2020 extension.
- **kjyg_build_qa.json** — machine-readable build summary (counts, gaps, skipped files).
