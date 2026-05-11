# KPoEM: Korean Poetry Emotion Mapping Dataset

## Overview

This corpus contains 615 poem-level annotation segments covering 483 unique poems by five canonical modern Korean poets, annotated with fine-grained emotion labels by five human annotators using the 44-category KOTE (Korean Online Text Emotions) framework. The dataset is provided at two levels of granularity: individual verse lines (7,007 entries) and poem segments (615 entries). Each row in the poem-level file is a poem segment; multi-stanza or multi-section poems may span several rows sharing the same poem_id.

The five poets span the colonial and post-liberation periods of Korean literary history:

| Poet | Korean | Period | Segments | Unique poems | Lines |
|------|--------|--------|----------|-------------|-------|
| Yun Dong-ju (윤동주) | 윤동주 | 1917–1945 | 114 | 112 | 1,111 |
| Kim So-wol (김소월) | 김소월 | 1902–1934 | 176 | 165 | 2,071 |
| Han Yong-un (한용운) | 한용운 | 1879–1944 | 138 | 117 | 1,198 |
| Im Hwa (임화) | 임화 | 1908–1953 | 110 | 43 | 2,163 |
| Yi Sang (이상) | 이상 | 1910–1937 | 77 | 45 | 464 |

The poems were sourced from Korean Wikisource and annotated as part of a project by the Academy of Korean Studies Digital Humanities Lab (한국학중앙연구원 디지털인문학연구소).

This data was sourced from the [KPoEM project](https://github.com/AKS-DHLAB/KPoEM) and the [HuggingFace dataset](https://huggingface.co/datasets/AKS-DHLAB/KPoEM) (MIT License).

---

## Files

- **kpoem_lines.tsv** — Line-level annotations (7,007 rows). Each row is a single verse line with emotion annotations.
- **kpoem_poems.tsv** — Poem-level annotations (616 rows). Each row is a poem segment; multi-stanza or multi-section poems may span several rows sharing the same poem_id.

---

## Variables: Line-Level Dataset

| Variable | Type | Description |
|----------|------|-------------|
| **line_id** | integer | Unique line identifier. |
| **poem_id** | integer | Links to the parent poem. |
| **text** | string | Korean text of the verse line. |
| **sub_title** | string | Subtitle, if any (often empty). |
| **title** | string | Poem title in Korean. |
| **poet** | string | Poet name in Korean. |
| **annotator_01–05** | string | Comma-separated Korean emotion labels from each of 5 human annotators. |

## Variables: Poem-Level Dataset

| Variable | Type | Description |
|----------|------|-------------|
| **seg_id** | integer | Unique segment identifier. |
| **poem_id** | integer | Poem identifier. |
| **text** | string | Full poem text in Korean. |
| **sub_title** | string | Subtitle, if any (often empty). |
| **title** | string | Poem title in Korean. |
| **poetry_book** | string | Source poetry collection name. |
| **poet** | string | Poet name in Korean. |
| **annotator_01–05** | string | Comma-separated Korean emotion labels from each of 5 human annotators. |

---

## Emotion Labels

The 44 emotion categories follow the KOTE framework. Examples include:

| Korean | English |
|--------|---------|
| 슬픔 | Sadness |
| 기쁨 | Joy |
| 화남/분노 | Anger |
| 불안/걱정 | Anxiety / Worry |
| 비장함 | Solemnity / Pathos |
| 서러움 | Sorrow |
| 감동/감탄 | Being moved / Admiration |
| 깨달음 | Realization |
| 부끄러움 | Shame |
| 존경 | Respect |

---

## Text Normalization Note

Yi Sang (이상) wrote many poems without standard Korean word spacing as a deliberate modernist stylistic choice. The upstream KPoEM source preserves this, resulting in 39 segments (poem-level) and 186 lines (line-level) with no inter-word spaces. These have been re-spaced in the `text` column using `kiwipiepy` (v0.22) automatic spacing correction to make the texts tokenizable. The normalization is imperfect for archaic or highly unusual vocabulary — users doing close literary analysis of Yi Sang's work should treat the spacing as an approximation and consult primary sources.

---

## License

MIT License. See the [original repository](https://github.com/AKS-DHLAB/KPoEM) for details.
