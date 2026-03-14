# Korean Newspaper Archive Corpus

## Overview

This corpus contains 364,409 articles from 39 Korean newspapers published between **1883 and 1952**, extracted from the Korean Newspaper Archive (대한민국 신문 아카이브) of the National Library of Korea. The data was obtained via the [Open Korean Historical Corpus (OKHC)](https://huggingface.co/datasets/seyoungsong/Open-Korean-Historical-Corpus), which aggregated and standardized these records from the National Library's digital archive.

The corpus covers a transformative period in Korean history: the late Joseon dynasty, the opening of Korea, the Protectorate era, the Japanese colonial period (1910–1945), and the early years of the Republic of Korea. The newspapers provide a direct window into political discourse, intellectual debate, social change, and the development of modern Korean prose during these decades.

All documents are in the **public domain**.

---

## Variables Included

8 columns, 364,409 rows. Each row is one newspaper article.

| Variable | Type | Description |
|----------|------|-------------|
| **id** | string | Unique document identifier from the OKHC (e.g., `news_archive:CNTS-00048673224`). |
| **year** | integer | Publication year. Range: 1883–1952. 983 rows have missing year values. |
| **newspaper** | string | Newspaper name in Korean. 39 unique titles. 17,828 rows have empty newspaper values. |
| **language** | string | Primary language of the article: Modern Korean, Hanmun (Classical Chinese), English, Early Modern Korean, or other. |
| **script** | string | Writing system used (e.g., Hanja, Hangeul, Hanja-Hangeul mixed). |
| **title** | string | Article title, where available. |
| **text** | string | Full article text. Median length 108 characters; mean 211 characters; max 15,473 characters. No empty values. |
| **url** | string | URL to the original article on the National Library of Korea website. |

---

## Major Newspapers

| Newspaper | Korean | Years | Articles | Notes |
|-----------|--------|-------|----------|-------|
| Hwangseong Sinmun | 황성신문 | 1898–1910 | 188,607 | "Capital Gazette"; leading newspaper of the Korean Empire |
| Daehan Maeil Sinbo | 대한매일신보 | 1904–1910 | 104,936 | Anti-Japanese newspaper; published in Korean, English, and mixed script |
| Dongnip Sinmun | 독립신문(서재필) | 1896–1899 | 19,636 | "The Independent"; founded by Seo Jae-pil; first Korean-language newspaper in modern format |
| Namjoseon Minbo | 남조선민보 | — | 15,026 | Southern Korea newspaper |
| Maeil Sinmun | 매일신문 | — | 6,842 | Daily newspaper |
| Masan Ilbo | 마산일보 | — | 6,220 | Masan regional daily |
| Hanseong Sunbo | 한성순보 | 1883–1884 | 1,652 | Korea's first modern newspaper (10-day periodical, in Classical Chinese) |
| Hanseong Jubo | 한성주보 | 1886–1888 | 1,561 | Successor to Hanseong Sunbo; introduced Hangul alongside Classical Chinese |

Plus 31 additional smaller newspapers.

---

## Language Distribution

| Language | Articles |
|----------|----------|
| Modern Korean | 315,645 |
| Hanmun (Classical Chinese) | 26,995 |
| English | 17,681 |
| Early Modern Korean | 3,102 |
| Korean (unspecified) | 964 |
| Japanese | 22 |

---

## Data Notes

- **Text length is generally short**: median 108 characters, reflecting the telegraphic style of early Korean journalism and the fact that many entries represent brief notices, advertisements, or editorial fragments rather than full-length articles.
- **983 rows** have missing year values; **17,828 rows** have empty newspaper names.
- The corpus includes articles in multiple scripts and languages reflecting the linguistic complexity of colonial-era Korea.
- Original source URLs link to the National Library of Korea's digital archive where scanned images of the original newspapers can be viewed.

---

## File Formats

The full corpus is available as a single Parquet file and also as CSV files split by newspaper for accessibility.

**Parquet (full corpus):**
- **korean_newspaper_archive.parquet** — All 364,409 articles in Apache Parquet format with zstd compression (75 MB). Use `pandas.read_parquet()` in Python or `arrow::read_parquet()` in R.

**CSV files (split by newspaper):**

| File | Newspaper | Years | Rows | Size |
|------|-----------|-------|------|------|
| `hwangseong_sinmun_1898-1904.csv` | Hwangseong Sinmun (황성신문) | 1898–1904 | 68,210 | 44 MB |
| `hwangseong_sinmun_1905-1910.csv` | Hwangseong Sinmun (황성신문) | 1905–1910 | 120,397 | 74 MB |
| `daehan_maeil_sinbo.csv` | Daehan Maeil Sinbo (대한매일신보) | 1900–1910 | 104,936 | 66 MB |
| `dongnip_sinmun.csv` | Dongnip Sinmun (독립신문) | 1896–1899 | 19,636 | 14 MB |
| `other_newspapers.csv` | 36 other newspapers | 1883–1952 | 51,230 | 43 MB |

---

## License

The newspaper articles are in the **public domain**. The OKHC dataset from which this corpus was extracted is licensed under CC BY-NC 4.0. If you use this data, please cite both the OKHC and this repository.

---

## Citation

> Song, Seyoung, et al. (2025). *Open Korean Historical Corpus*. HuggingFace. https://huggingface.co/datasets/seyoungsong/Open-Korean-Historical-Corpus
