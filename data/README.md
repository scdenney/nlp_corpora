# Data Catalog

This directory contains the local datasets included in the repository. Each corpus folder includes the data files plus a dataset-level `README.md` covering scope, variables, source attribution, and reuse notes.

## Recommended Workflow

1. Read the `README.md` in the dataset folder before working with the files.
2. Prefer Parquet or JSONL when you need speed, compression, or structured metadata.
3. Use CSV or TSV when you want broad compatibility across Python, R, spreadsheets, or annotation tools.
4. Check source and license notes before redistribution, publication, or classroom reuse.

## Primary Corpora

| Corpus                                                         | Theme                 | Coverage                | Main unit                       | Formats        |
|:---------------------------------------------------------------|:----------------------|:------------------------|:--------------------------------|:---------------|
| [Korean Newspaper Archive](./korean_newspaper_archive)         | Historical newspapers | 1883–1952               | 364,409 articles                | Parquet, CSV   |
| [Colonial-Era Magazines](./colonial_magazines)                 | Historical magazines  | 1896–1943               | 15,326 articles                 | Parquet, CSV   |
| [NIKH History Textbooks](./nikh)                               | Textbooks             | 1895–2016               | 67 textbooks                    | CSV            |
| [Korean Pseudohistory Primary Sources](./korean_pseudohistory) | Primary texts         | Premodern to modern     | 9 texts / 764 pages             | JSONL, Parquet |
| [Rodong Sinmun (English)](./rodong_sinmun)                     | DPRK media            | 2018–2022               | 9,797 articles                  | CSV            |
| [Kyŏngje Yŏngu](./kyongje_yongu)                               | DPRK journal          | 1987–2017               | 2,583 articles                  | CSV            |
| [Presidential Speeches](./president_speeches)                  | South Korean politics | 1948–2022               | 8,771 speeches                  | CSV            |
| [Blue House Petitions](./bluehouse_petitions)                  | Civic petitions       | 2017–2018               | 18,077 petitions                | CSV            |
| [Inter-Korean Summit Corpus](./inter_korean_summit)            | Newspaper coverage    | 2000, 2007, 2018        | 18,018 sentences / 455 articles | CSV            |
| [Moon Jae-in Twitter](./moon_twitter)                          | Social media          | 2012–2020               | 3,148 tweets                    | CSV            |
| [Korean Newspapers on Twitter](./kr_newspapers)                | Social media          | July–August 2017        | 2,748 tweets                    | CSV            |
| [Naver Movie Reviews (Classroom Edition)](./naver_movie_reviews) | Internet language     | Reviews to 2015         | 50,000 reviews                  | CSV            |
| [KPoEM](./kpoem)                                               | Literature            | Colonial to postwar era | 7,622 annotations               | TSV            |
| [Immigrant Interviews](./immigrant_interviews)                 | Survey text           | Cross-sectional         | 1,008 responses                 | CSV            |
| [North Korean Migrant Interviews](./nkmigrants_interviews)     | Survey text           | Cross-sectional         | 6,027 responses                 | CSV            |

## Focused Collection

| Collection                           | Coverage  | Main unit      | Format | Notes                                                  |
|:-------------------------------------|:----------|:---------------|:-------|:-------------------------------------------------------|
| [Kaebyok Magazine Corpus](./kaebyok) | 1920–1935 | 2,467 articles | CSV    | Standalone *Kaebyok* corpus for magazine-specific work |

## File Type Guide

| Format  | Use It When                                                | Typical Examples                                       |
|:--------|:-----------------------------------------------------------|:-------------------------------------------------------|
| CSV     | You want maximum interoperability and simple tabular reads | speeches, petitions, interviews, Twitter corpora       |
| TSV     | Text fields are dense or annotation-heavy                  | KPoEM line-level and poem-level emotion datasets       |
| Parquet | You want faster loading and smaller file sizes             | newspaper archive, colonial magazines, pseudohistory   |
| JSONL   | You need nested, document-level metadata                   | pseudohistory corpus with page arrays                  |
| PDF     | You need companion articles or source context              | survey and interview folders with related publications |

## Notes

- Large historical corpora are provided in Parquet where practical, with CSV alternatives for portability.
- Some folders include companion PDFs or markdown notes that provide methodological or bibliographic context.
- When a focused collection overlaps conceptually with a broader corpus, the folder README explains the relationship.