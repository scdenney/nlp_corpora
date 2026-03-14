# Korean Presidential Speeches

## Overview

This corpus contains a collection of Korean presidential speeches covering most of South Korea's history, from Syngman Rhee (이승만) through Moon Jae-in (문재인). The texts include a wide range of speech types — inaugural addresses, commemorative speeches, New Year's messages, policy statements, and more — delivered in domestic and international settings. Each speech is accompanied by metadata describing the speaker, date, location, and original speech classification.

---

## Variables Included

7 columns, 8,771 rows. Each row is one speech.

| Variable | Type | Description |
|----------|------|-------------|
| **division_number** | integer | Source document reference number. |
| **president** | string | Name of the president delivering the speech (in Korean). 12 unique values (see table below). |
| **title** | string | Speech title as provided by the original source (in Korean). See sample titles below. |
| **date** | string | Speech date. Formats vary (see note below). **208 missing values.** |
| **location** | string | Original location indicator (in Korean). 6 values (see table below). |
| **kind** | string | Speech type label (in Korean). 10 values (see table below). |
| **speech_text** | string | Full speech text in Korean. Median length: 1,777 characters / 402 tokens. Range: 104–57,481 characters. |

---

## Presidents (Chronological)

| Korean | Romanization | English Name | Speeches | Approximate Term |
|--------|-------------|--------------|----------|-----------------|
| 이승만 | Yi Sŭngman | Syngman Rhee | 998 | 1948–1960 |
| 윤보선 | Yun Posŏn | Yun Posun | 3 | 1960–1962 |
| 박정희 | Pak Chŏnghŭi | Park Chung-hee | 1,270 | 1963–1979 |
| 최규하 | Ch'oe Kyuha | Choi Kyu-hah | 58 | 1979–1980 |
| 전두환 | Chŏn Tuhwan | Chun Doo-hwan | 602 | 1980–1988 |
| 노태우 | No T'aeu | Roh Tae-woo | 601 | 1988–1993 |
| 김영삼 | Kim Yŏngsam | Kim Young-sam | 728 | 1993–1998 |
| 김대중 | Kim Taejung | Kim Dae-jung | 822 | 1998–2003 |
| 노무현 | No Muhyŏn | Roh Moo-hyun | 780 | 2003–2008 |
| 이명박 | Yi Myŏngbak | Lee Myung-bak | 1,027 | 2008–2013 |
| 박근혜 | Pak Kŭnhye | Park Geun-hye | 493 | 2013–2017 |
| 문재인 | Mun Chaein | Moon Jae-in | 1,389 | 2017–2022 |

---

## `kind` Values (Speech Type) with Translations

| Korean | English Translation | Count |
|--------|---------------------|-------|
| 기념사 | Commemorative address | 3,994 |
| 성명/담화문 | Statement / communiqué | 1,893 |
| 기타 | Other | 1,326 |
| 환영사 | Welcome address | 691 |
| 회의 | Meeting / conference remarks | 335 |
| 축사 | Congratulatory address | 232 |
| 신년사 | New Year's address | 152 |
| 국회연설 | National Assembly address | 119 |
| 취임사 | Inaugural address | 24 |
| 만찬사 | Banquet / dinner address | 5 |

---

## `location` Values with Translations

| Korean | English Translation | Count |
|--------|---------------------|-------|
| 국내 | Domestic | 7,524 |
| 국제 | International | 755 |
| 국외 | Overseas | 265 |
| 해외 | Abroad | 224 |
| 지역 | Regional | 2 |

Note: 국외 and 해외 both mean "overseas/abroad" and could be merged for analysis. One row has a leading-space data quality issue (` 국내` instead of `국내`).

---

## Speech Length by President

| President | Median Characters | Median Tokens |
|-----------|------------------|---------------|
| 이승만 (Rhee) | 1,166 | 272 |
| 박정희 (Park CH) | 1,960 | 451 |
| 전두환 (Chun) | 2,046 | 462 |
| 노태우 (Roh TW) | 2,803 | 638 |
| 김영삼 (Kim YS) | 1,695 | 382 |
| 김대중 (Kim DJ) | 2,142 | 488 |
| 노무현 (Roh MH) | 1,158 | 259 |
| 이명박 (Lee MB) | 1,444 | 331 |
| 박근혜 (Park GH) | 1,641 | 355 |
| 문재인 (Moon) | 1,695 | 375 |

Overall: min 104 characters, max 57,481 characters, median 1,777 characters.

---

## Sample Titles with Translations

| President | Korean Title | English Translation | Kind | Date |
|-----------|-------------|---------------------|------|------|
| 박정희 | 제5대 대통령 취임식 대통령 취임사 | Inaugural Address at the 5th Presidential Inauguration | 취임사 (Inaugural) | 1963.12.17 |
| 박정희 | 신년 메시지 | New Year's Message | 신년사 (New Year's) | 1964.01.01 |
| 최규하 | 국가비상시국에 관한 대통령권한대행 특별담화 | Special Address by the Acting President on the National Emergency | 성명/담화문 (Statement) | 1979.10.27 |
| 전두환 | 제11대 대통령 취임사 | Inaugural Address of the 11th President | 취임사 (Inaugural) | 1980.09.01 |
| 노태우 | 제69주년 3·1절 기념사 | Commemorative Address for the 69th March 1st Movement Anniversary | 기념사 (Commemorative) | 1988.03.01 |
| 김영삼 | 제14 대통령 취임사(우리 다 함께 신한국으로) | 14th Presidential Inaugural ("Together Toward a New Korea") | 취임사 (Inaugural) | 1993.02.25 |
| 김대중 | 제15 대통령 취임사(국난극복과 재도약의 새시대를 엽시다) | 15th Presidential Inaugural ("Let Us Open a New Era of Overcoming National Crisis and Renewed Leap Forward") | 취임사 (Inaugural) | 1998.02.25 |
| 노무현 | 고급공무원에게 보내는 서신 | Letter to Senior Civil Servants | 기타 (Other) | — |
| 문재인 | 제74주년 광복절 경축사 | Congratulatory Address for the 74th Liberation Day | 기념사 (Commemorative) | 2019.08.15 |

---

## Date Format Notes

The `date` column uses three different formats:

| Format | Example | Count | Note |
|--------|---------|-------|------|
| `YYYY.MM.DD` | `1963.12.17` | 8,443 | Full date (vast majority) |
| `YYYY` | `1964` | 82 | Year only |
| `YYYY.MM` | `1981.12` | 38 | Year and month only |
| Missing | — | 208 | No date recorded |

Parsing requires handling all three formats. The full date range spans **1948-07-24** (Rhee) to **2022-03-30** (Moon).

---

## Suggested Derived Variables

The following variables are not present in the CSV but can be derived to support structured comparisons:

| Variable | How to Derive | Suggested Values |
|----------|---------------|-----------------|
| **era** | Based on president | `founding` (Rhee, Yun), `military_regime` (Park CH, Choi, Chun), `democratization` (Roh TW, Kim YS), `modern_liberal` (Kim DJ, Roh MH), `modern_conservative` (Lee MB, Park GH), `modern_progressive` (Moon) |
| **regime_type** | Based on president | `authoritarian` (Rhee through Chun), `transitional` (Roh TW), `democratic` (Kim YS onward) |
| **type_group** | Pattern-match on `kind` | `inaugural`, `new_year`, `commemorative`, `policy_statement`, `other` |
| **n_chars** | `len(speech_text)` | Integer |
| **n_tokens** | `len(speech_text.split())` | Integer (whitespace-based approximation) |
| **topic_scope** | Keyword pattern matching | `domestic`, `foreign_or_security`, `mixed_or_other` |

---

## Data Quality Notes

- **208 rows** have missing `date` (2.4%); all other columns are fully populated.
- The `location` column has one row with a leading space (` 국내` instead of `국내`).
- 국외 and 해외 are synonymous ("overseas") and appear as separate values; consider merging for analysis.
- Date formats are inconsistent (3 granularities); automated parsing requires handling all three.

---

## File Formats

- **president_speech_ko.csv** — UTF-8 CSV file containing the complete corpus.
