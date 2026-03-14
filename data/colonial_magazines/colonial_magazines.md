# Colonial-Era Korean Magazines Corpus (1896–1943)

## Overview

This corpus contains 15,326 articles from 19 Korean magazines published during the late Joseon, Korean Empire, and Japanese colonial periods (1896–1943). The articles cover intellectual debate, political thought, nationalism, literature, social reform, modernization, and cultural commentary. These periodicals were central venues for Korean public discourse during a period of rapid change, foreign domination, and anti-colonial resistance.

The data was extracted from the [Open Korean Historical Corpus (OKHC)](https://huggingface.co/datasets/seyoungsong/Open-Korean-Historical-Corpus), which sourced it from the National Institute of Korean History (NIKH). All articles are in the **public domain**.

---

## Variables Included

10 columns, 15,326 rows. Each row is one article.

| Variable | Type | Description |
|----------|------|-------------|
| **id** | string | Unique document identifier from the OKHC. |
| **year** | integer | Publication year. Range: 1896–1943. |
| **date** | string | Publication date as recorded in the source (Korean date format). |
| **magazine** | string | Magazine name in Korean. 19 unique titles. |
| **article_type** | string | Article genre (e.g., 논설 "editorial," 소설 "fiction," 시 "poetry"). |
| **author** | string | Author name, where recorded. |
| **title** | string | Article title. |
| **text** | string | Full article text. |
| **language** | string | Primary language of the article. |
| **url** | string | URL to the original on the NIKH website. |

---

## Magazines Included

### Major Magazines (individual CSV files)

| Magazine | Korean | Years | Articles | Description |
|----------|--------|-------|----------|-------------|
| **Samcheolli** | 삼천리 | 1929–1942 | 4,093 | "Three Thousand Li" — the most popular general-interest magazine of the late colonial period. Wide-ranging coverage of politics, culture, literature, celebrity, and social issues. |
| **Byeolgeongon** | 별건곤 | 1926–1934 | 2,847 | "Another World" — popular culture, entertainment, social commentary, and human-interest stories. Sister publication to Kaebyok. |
| **Kaebyok** | 개벽 | 1920–1926, 1934–1935 | 2,462 | "Creation/Genesis" — influential intellectual magazine published by Ch'ondogyo affiliates. Forum for nationalism, modernization, and social reform debates. Suppressed by colonial censors in 1926; briefly revived 1934–35. |
| **Donggwang** | 동광 | 1926–1933 | 1,434 | "Eastern Light" — intellectual journal covering philosophy, social science, and Korean cultural identity. |

### Smaller Journals (combined in `other_magazines.csv`)

| Magazine | Korean | Years | Articles | Description |
|----------|--------|-------|----------|-------------|
| Taegeuk Hakbo | 태극학보 | 1906–1908 | 658 | Academic journal of Korean students in Tokyo |
| Seobuk Hakhoe Wolbo | 서북학회월보 | 1908–1910 | 483 | Northwest Academic Society monthly |
| Daehan Hyeophoe Hoebo | 대한협회회보 | 1908–1909 | 446 | Korean Association bulletin |
| Giho Heunghakhoe Wolbo | 기호흥학회월보 | 1908–1909 | 396 | Giho Region Education Society monthly |
| Seou | 서우 | 1906–1908 | 378 | "Western Friends" — educational journal |
| Daedong Hakhoe Wolbo | 대동학회월보 | 1908–1909 | 362 | Great Eastern Academic Society monthly |
| Daehan Heunghakbo | 대한흥학보 | 1909–1910 | 335 | Korean Education Promotion bulletin |
| Daehan Jaganghoe Wolbo | 대한자강회월보 | 1906–1907 | 333 | Korean Self-Strengthening Society monthly |
| Daehan Hakhoe Wolbo | 대한학회월보 | 1908 | 287 | Korean Academic Society monthly |
| Daejoseon Dongnip Hyeophoe Hoebo | 대조선독립협회회보 | 1896–1897 | 257 | Independence Club bulletin — Korea's first modern political organization |
| Honam Hakbo | 호남학보 | 1908–1909 | 179 | Honam (Jeolla) Region academic journal |
| Daehan Yuhaksaenghoe Hakbo | 대한유학생회학보 | 1907 | 122 | Korean Overseas Students' Association bulletin |
| Daedonga | 대동아 | 1942–1943 | 120 | "Greater East Asia" — late colonial wartime publication |
| Samcheolli Munhak | 삼천리문학 | 1938 | 94 | Literary supplement to Samcheolli |
| Manguk Buin | 만국부인 | 1932 | 40 | "Women of All Nations" — women's magazine |

---

## Language Notes

Most articles are in Modern Korean, often with heavy use of Hanja (Chinese characters) and historical orthography that differs from contemporary South Korean spelling. Some articles, particularly from the earlier journals (1896–1910), are primarily or entirely in Classical Chinese (Hanmun). Researchers applying modern Korean NLP tools should expect higher error rates on these texts.

---

## File Formats

**Parquet (full corpus):**
- **colonial_magazines.parquet** — All 15,326 articles in Apache Parquet format with zstd compression (56 MB). Use `pandas.read_parquet()` in Python or `arrow::read_parquet()` in R.

**CSV files (split by magazine):**

| File | Magazine | Rows | Size |
|------|----------|------|------|
| `kaebyok.csv` | 개벽 (Kaebyok) | 2,462 | 30 MB |
| `samcheolli.csv` | 삼천리 (Samcheolli) | 4,093 | 36 MB |
| `byeolgeongon.csv` | 별건곤 (Byeolgeongon) | 2,847 | 23 MB |
| `donggwang.csv` | 동광 (Donggwang) | 1,434 | 12 MB |
| `other_magazines.csv` | 15 smaller journals | 4,490 | 18 MB |

---

## License

The magazine articles are in the **public domain**. The OKHC dataset from which this corpus was extracted is licensed under CC BY-NC 4.0. If you use this data, please cite both the OKHC and this repository.

---

## Citation

> Song, Seyoung, et al. (2025). *Open Korean Historical Corpus*. HuggingFace. https://huggingface.co/datasets/seyoungsong/Open-Korean-Historical-Corpus
