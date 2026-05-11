# North Korean Economics Journal Corpus

## Overview

This corpus contains articles from a North Korean economics journal spanning **1987–2017**: the Kyŏngje Yŏngu (경제연구, "Economic Research"). It provides a rare, longitudinal window into how the Democratic People's Republic of Korea (DPRK) discusses economic policy, ideology, and development priorities. The journal functions as a key medium through which the state articulates economic doctrine and signals its official line on planning, production, foreign trade, technocratic reforms, and the relationship between economic goals and the ideological foundations of the regime.

Across this 30-year period, North Korea experienced dramatic transformations: the collapse of the socialist trading bloc, the "Arduous March" famine years, partial marketization and institutional adjustment, nuclear development under tightening sanctions, and shifting strategies under three different leaders. The texts in this corpus reflect these turning points through changes in terminology, framing, priorities, slogans, and emphases on self-reliance, science and technology, productivity, agriculture, or defense.

Read more about the journal at [38 North](https://www.38north.org/2025/05/in-memoriam-kyongje-yongu/).

---

## Variables Included

6 columns, 2,583 rows. Each row is one journal article. (1 true duplicate removed; 2,582 unique titles.)

| Variable | Type | Description |
|----------|------|-------------|
| **title** | string | Article title as published in the journal, in DPRK Korean orthography. 2,582 unique values. Title uniqueness is not guaranteed: 10 titles appear more than once across different years or authors. |
| **author** | string | Author(s) listed for the article. 1,619 unique authors. **21 missing values** (likely unsigned editorials). |
| **year_issue** | string | Combined year and quarterly issue number in `YYYY-N` format (e.g., `1987-1`, `2017-4`). 122 unique values spanning 31 years. The journal is published quarterly (4 issues per year). |
| **word_count** | integer | Approximate token/word count of the article text. Range: 0–3,346; median: 1,035; mean: 1,040. |
| **file_path** | string | Original Windows file path to the source JSON file. Retained as a provenance trail. |
| **content** | string | Full article text in Korean (DPRK orthography). Median length ~5,606 characters; max ~17,087 characters. **82 missing values.** |

---

## Temporal Distribution

The journal is quarterly, with steadily increasing output over the decades:

| Decade | Articles | Historical Context |
|--------|----------|--------------------|
| 1980s (1987–89) | 116 | Late socialist planning under Kim Il-sung (김일성, KIS) |
| 1990s | 591 | Soviet collapse; "Arduous March" famine (고난의 행군) under Kim Jong-il (김정일, KJI) |
| 2000s | 813 | Partial marketization and institutional adjustment (KJI) |
| 2010s | 1,063 | Kim Jong-un (김정은, KJU); *byungjin* (병진, "parallel development") line; sanctions era |

Articles per year ranged from 34 (1987) to 170 (2016, peak). The four quarterly issues are evenly distributed (616–666 articles each across the full corpus).

---

## Suggested Derived Variables

The following variables are not present in the CSV but can be straightforwardly derived from `year_issue` to support structured comparisons:

| Variable | How to Derive | Values |
|----------|---------------|--------|
| **year** | Split `year_issue` on `-`, take the first element | 1987–2017 (integer) |
| **issue** | Split `year_issue` on `-`, take the second element | 1, 2, 3, or 4 (integer) |
| **leader_period** | Based on year: ≤1994 → `KIS`, 1995–2011 → `KJI`, ≥2012 → `KJU` | `KIS` (Kim Il-sung), `KJI` (Kim Jong-il), `KJU` (Kim Jong-un) |
| **economic_era** | Based on year: 1987–1990 → `late_socialist_planning`, 1991–1998 → `collapse_arduous_march`, 1999–2011 → `marketization_adjustment`, 2012–2017 → `byungjin_sanctions` | 4 categories |
| **decade** | Based on year | `1980s`, `1990s`, `2000s`, `2010s` |
| **log_word_count** | `log1p(word_count)` | Continuous; useful for comparing article length |

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
| 1987 | 경제발전과 새로운 에네르기원천의 개발리용 | "Economic Development and the Development and Utilization of New Energy Sources" |
| 1987 | 협동적소유를 전인민적소유로 전환시키는것은 사회주의의 완전승리를 위한 기본문제해결의 근본방도 | "Converting Cooperative Ownership to Whole-People Ownership Is the Fundamental Method for Resolving the Basic Question of Complete Socialist Victory" |
| 1995 | 추가적인 로동보수형태를 잘 적용하는것은 근로자들의 생산적열의를 높이기 위한 중요담보 | "Properly Applying Supplementary Labor Compensation Forms Is an Important Guarantee for Raising Workers' Productive Enthusiasm" |
| 2005 | 독립채산제기업소자체충당금과 그 적립리용에서 나서는 중요문제 | "Important Issues Arising in the Accumulation and Use of Self-Financing Reserves at Independent Accounting Enterprises" |
| 2015 | 대외결제은행들에서 경영위험과 그 평가방법 | "Management Risk and Its Evaluation Methods in Foreign Settlement Banks" |
| 2015 | 대외경제교류의 경제적효과성타산에서 지켜야 할 중요원칙 | "Important Principles to Observe in Calculating the Economic Effectiveness of Foreign Economic Exchange" |

---

## Data Quality Notes

- **82 rows** have missing `content` (article text); **21 rows** have missing `author`.
- The `file_path` column contains original Windows paths (e.g., `C:\Users\steve\Documents\...`) and is retained for provenance only — it is not functional on other systems.

---

## File Formats

- **kjyg.csv** — UTF-8 CSV file containing the complete corpus.
