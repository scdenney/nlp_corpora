# Inter-Korean Summit Corpus

This folder contains newspaper coverage of the 2000, 2007, and 2018 inter-Korean summits from *Chosun Ilbo* and *Hankyoreh*. It is based on Jin Hee Park's *Inter-Korean summit corpus* and includes one main sentence-level file plus reconstructed article-level files.

---

## Files

| File | Description | Rows |
|------|-------------|------|
| **inter_korean_summit_sentences.csv** | Main corpus. One row per sentence, with newspaper, year, summit episode, and text. | 18,018 |
| **inter_korean_summit_articles.csv** | Reconstructed article-level corpus for the full dataset. | 455 |
| **inter_korean_summit_articles_chosun_ilbo.csv** | Reconstructed articles from *Chosun Ilbo* only. | 235 |
| **inter_korean_summit_articles_hankyoreh.csv** | Reconstructed articles from *Hankyoreh* only. | 220 |
| **inter_korean_summit_2018_articles.csv** | Cleaner 2018 article-level subset built from local source files. | 252 |

---

## Coverage Summary

### Reconstructed Articles by Year

| Year | Sentences | Articles |
|------|-----------|----------------|
| **2000** | 2,435 | 14 |
| **2007** | 5,075 | 42 |
| **2018** | 10,508 | 399 |

### Reconstructed Articles by Newspaper

| Newspaper | Sentences | Articles |
|-----------|-----------|----------------|
| **Chosun Ilbo** | 6,455 | 235 |
| **Hankyoreh** | 11,563 | 220 |

### 2018 Reference File

| Coverage Date | Articles |
|---------------|----------|
| **2018-04-27** | 194 |
| **2018-05-26** | 13 |
| **2018-05-27** | 45 |

---

## Notes

- Start with **`inter_korean_summit_sentences.csv`** for most analysis.
- **`inter_korean_summit_articles.csv`** and the newspaper-specific article files are reconstructed from sentence streams. They are usable, but article boundaries are inferred rather than preserved in the original source, especially for **2000** and **2007**.
- **`inter_korean_summit_2018_articles.csv`** is a cleaner reference file because the local 2018 source files preserve article boundaries.
- All files are UTF-8 CSVs.

---

## Source and Attribution

This corpus is reconstructed from:

> Park, Jin Hee. (2020). *Inter-Korean summit corpus* (Version 1) [Data set]. Mendeley Data. https://doi.org/10.17632/mp3drsh4hs.1

The original corpus covers summit-related newspaper text from 2000, 2007, and 2018 and is attributed here to Jin Hee Park. The upstream Mendeley record lists the dataset under **CC BY 4.0**, with a note that third-party newspaper content may require additional permission.
