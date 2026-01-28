# Korean Presidential Speeches

## Overview

This corpus contains a collection of Korean presidential speeches covering most of South Korea's history (이승만-문재인). The texts include a wide range of speech types, such as inaugural addresses, commemorative speeches, New Year’s messages, and policy statements delivered in domestic and international settings. Each speech is accompanied by metadata describing the speaker, date, location, and original speech classification.

To support additional text analysis, the corpus has been augmented with several additional subgroup variables. These new features provide high-level indicators of political era, regime type, topical orientation, and speech genre, along with basic textual characteristics such as character and token counts. Together, these variables make it possible to explore differences in language use across historical periods, institutional contexts, and communicative purposes.

---

## Variables Included

### Original Metadata Columns

| Variable | Description |
|---------|-------------|
| **division_number** | Source document reference number. |
| **president** | Name of the president delivering the speech (in Korean). |
| **title** | Speech title as provided by the original source. |
| **date** | Speech date; formats vary (e.g., `YYYY`, `YYYY.MM.DD`). |
| **location** | Original location indicator, typically 국내 (domestic) or 국외 (foreign). |
| **kind** | Speech type label (e.g., 취임사, 기념사, 신년사). |
| **speech_text** | Full speech text in Korean. |

---

## Added Subgroup Variables

These variables were added to support additional text analysis. These added features are intentionally broad and interpretable rather than precise. 

| Variable | Description |
|---------|-------------|
| **era** | Broad historical/political era category based on the president (e.g., military_regime, democratization, modern liberal). |
| **regime_type** | Authoritarian / transitional / democratic regime classification. |
| **type_group** | Coarse, pattern-based speech-type grouping (inaugural, new_year, commemorative, policy_statement, other). |
| **n_chars** | Character count of the speech text. |
| **n_tokens** | Approximate token count based on whitespace segmentation. |
| **topic_scope** | High-level topical domain inferred from keyword patterns: domestic, foreign_or_security, or mixed_or_other. |

---

## File Formats

- **president_speech_ko.csv** — UTF-8 CSV file containing the complete corpus.  