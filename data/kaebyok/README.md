# Kaebyok Magazine Corpus (1920–1935)

## Overview

This corpus contains full-text articles from *Kaebyok* (開闢, "Creation" or "Genesis"), an influential Korean magazine published during the Japanese colonial period. The magazine served as a major forum for intellectual and cultural debate, covering nationalism, modernization, literature, social reform, religion, and political thought.

This folder presents *Kaebyok* as a standalone corpus for magazine-specific work. It complements the broader [`colonial_magazines`](../colonial_magazines) collection, but uses a simpler schema centered on issue date, article order, and full text.

## At a Glance

| Item       | Details                                                                |
|:-----------|:-----------------------------------------------------------------------|
| Coverage   | 1920–1935                                                              |
| Total size | 2,467 articles across 76 issues                                        |
| Main unit  | One row per article                                                    |
| Format     | UTF-8 CSV                                                              |
| Best use   | Close reading, full-text analysis, and issue-by-issue magazine studies |

## Files

| File                 | Description                                            |
|:---------------------|:-------------------------------------------------------|
| `kaebyok_corpus.csv` | Unified full-text corpus containing all 2,467 articles |

## Variables

4 columns. Each row represents one article.

| Variable      | Type    | Description                                                                                                  |
|:--------------|:--------|:-------------------------------------------------------------------------------------------------------------|
| `issue_date`  | string  | Publication date of the issue in `YYYY-MM-DD` format. 76 unique dates spanning `1920-06-25` to `1935-03-01`. |
| `year`        | integer | Publication year. 9 unique values: 1920–1926 and 1934–1935.                                                  |
| `article_num` | integer | Article number within the issue. Range: 1–55, with roughly 18 articles per issue on average.                 |
| `text`        | string  | Full article text in Korean, often in mixed Hangul-Hanja script and historical orthography.                  |

No missing values are documented in any column.

## Year Distribution

| Year      | Articles | Note                                          |
|:----------|---------:|:----------------------------------------------|
| 1920      |      248 | Founding year; first issue published June 25  |
| 1921      |      358 |                                               |
| 1922      |      361 |                                               |
| 1923      |      380 |                                               |
| 1924      |      382 | Peak year in the first publication run        |
| 1925      |      295 |                                               |
| 1926      |      229 | Last issue before suppression                 |
| 1927–1933 |        0 | Publication suspended by colonial authorities |
| 1934      |      107 | Revival after an eight-year hiatus            |
| 1935      |      107 | Final issues; last issue published March 1    |

## Historical Context

*Kaebyok* was one of the most significant Korean-language magazines of the colonial era. First published in 1920 by Ch'ŏndogyo affiliates, it provided a platform for Korean intellectuals to debate modernization, national identity, social reform, religion, literature, and contemporary politics under Japanese rule. The magazine was forcibly shut down in 1926 by colonial censors, briefly revived in 1934–1935, and then ceased publication permanently.

## Language Notes

- The corpus mixes **Hangul**, **Hanja**, and historical spelling conventions that differ from contemporary South Korean usage.
- Some articles are primarily or entirely in Classical Chinese.
- Researchers using modern Korean NLP pipelines should expect normalization, tokenization, and OCR-related challenges on early issues.

## Sample Article Titles with Translations

- `1920` `謝告`: "Notice of Apology"
- `1922` `朝鮮美術의 史的 考察`: "A Historical Study of Korean Art"
- `1922` `吳虞 氏의 儒敎破壞論`: "Mr. Wu Yu's Theory of Destroying Confucianism"
- `1924` `咸南列邑大觀`: "Grand View of Towns in South Hamgyŏng Province"
- `1924` `우리의 美術과 展覽會`: "Our Art and Exhibitions"
- `1925` `社會日誌`: "Social Diary"
- `1925` `花發多風雨`: "When Flowers Bloom, Many Winds and Rains"

## Working Notes

- Use this folder when you want a dedicated *Kaebyok* corpus rather than a multi-magazine comparison dataset.
- Use `issue_date` or `year` to study censorship, editorial shifts, and the publication hiatus.
- For cross-title comparisons, use [`../colonial_magazines`](../colonial_magazines) instead.

## Data Quality Notes

- **U+FFFD replacement characters:** 279 of 2,467 rows (11.3%) contain at least one U+FFFD replacement character in the `text` column (576 total occurrences). These are OCR failures at specific historical Hangul or Hanja glyphs where the source image could not be decoded. They occur mid-word and mark a specific textual lacuna — do not silently strip them, as their presence is informative. Years 1923–1926 are most affected (15–21% of rows); the revival period (1934–1935) has lower rates (2–8%). For downstream NLP, either filter affected rows or treat U+FFFD as an unknown-character token.

## License and Citation

The magazine content is in the public domain. When citing this corpus, cite the repository and note that this folder is the standalone *Kaebyok* collection within *NLP Corpora for Korean Studies*.
