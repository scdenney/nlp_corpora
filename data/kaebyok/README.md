# Kaebyok Magazine Corpus (1920–1935)

This corpus contains full-text articles from *Kaebyok* (開闢, lit. "Creation" or "Genesis"), an influential Korean magazine published during the Japanese colonial period. The magazine served as a major forum for intellectual and cultural debate, covering topics including nationalism, modernization, literature, social reform, and political thought.

---

## Files

| File | Description |
|------|-------------|
| **kaebyok_corpus.csv** | Unified corpus containing all 2,467 articles |

---

## Variables

4 columns. Each row represents one article.

| Variable | Type | Description |
|----------|------|-------------|
| **issue_date** | string | Publication date of the magazine issue (`YYYY-MM-DD` format). 76 unique dates. Range: `1920-06-25` to `1935-03-01`. |
| **year** | integer | Publication year. 9 unique values: 1920–1926, 1934–1935. |
| **article_num** | integer | Article number within the issue. Range: 1–55; mean ~18 articles per issue. |
| **text** | string | Full article text in Korean. Written in a mix of Hangul and Hanja (Chinese characters) with historical orthography conventions. |

No missing values in any column.

---

## Year Distribution

| Year | Articles | Note |
|------|----------|------|
| 1920 | 248 | Founding year (first issue: June 25) |
| 1921 | 358 | |
| 1922 | 361 | |
| 1923 | 380 | |
| 1924 | 382 | Peak first-run year |
| 1925 | 295 | |
| 1926 | 229 | Last issue before suppression |
| *1927–1933* | *—* | *Publication suspended by Japanese colonial authorities* |
| 1934 | 107 | Revival after 8-year hiatus |
| 1935 | 107 | Final issues (last: March 1) |

**Total articles:** 2,467 across **76 issues**.

---

## Historical Context

*Kaebyok* was one of the most significant Korean-language magazines of the colonial era. First published in 1920 by Ch'ŏndogyo (천도교, "Religion of the Heavenly Way") affiliates, it provided a platform for Korean intellectuals to discuss modernization, national identity, and social change under Japanese rule. The magazine featured essays, fiction, poetry, and commentary on contemporary events. It was forcibly shut down in 1926 by colonial censors, briefly revived in 1934–35, and then ceased publication permanently.

---

## Language Notes

The texts are written in Korean using a mix of:
- **Hangul** (Korean script)
- **Hanja** (Chinese characters) — used heavily, especially in earlier issues
- **Historical orthography** conventions that differ from modern Korean spelling

### Sample Article Titles with Translations

| Year | Korean Title | English Translation |
|------|-------------|---------------------|
| 1920 | 謝告 | "Notice of Apology" (editorial note on censored content) |
| 1922 | 朝鮮美術의 史的 考察 | "A Historical Study of Korean Art" |
| 1922 | 吳虞 氏의 儒敎破壞論 | "Mr. Wu Yu's Theory of Destroying Confucianism" |
| 1924 | 咸南列邑大觀 | "Grand View of Towns in South Hamgyŏng Province" |
| 1924 | 우리의 美術과 展覽會 | "Our Art and Exhibitions" |
| 1925 | 社會日誌 | "Social Diary" (a chronicle of current events) |
| 1925 | 花發多風雨 | "When Flowers Bloom, Many Winds and Rains" (essay on political movements) |

Researchers working with this corpus may need to account for historical spelling variations, mixed-script text, and the fact that some articles are primarily or entirely in Classical Chinese (Hanmun/漢文).
