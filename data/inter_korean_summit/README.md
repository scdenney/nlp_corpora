# Inter-Korean Summit Corpus

## Overview

This folder now contains **three complementary reconstructions** of Jin Hee Park's *Inter-Korean summit corpus*.

The **primary dataset in this folder** is:

- **`inter_korean_summit_full_sentences.csv`**: the canonical full-coverage reconstruction across **2000, 2007, and 2018**

The supporting datasets are:

- **`inter_korean_summit_full_article_candidates.csv`**: heuristic document-level grouping for exploratory article-style analysis
- **`inter_korean_summit_2018_articles.csv`**: high-confidence local 2018 article subset retained as a **reference/validation file**

The distinction matters:

- The upstream Mendeley files expose the full multi-year corpus, but they are **UTF-16, tokenized, and PoS-tagged sentence streams**, not clean article text.
- The sentence-level reconstruction preserves the full temporal coverage without inventing article boundaries, so it is the safest default.
- The article-candidate reconstruction is useful, but it remains **heuristic**, especially for **2000** and **2007**.
- The local 2018 files preserve article structure well enough for a conventional article-level CSV, so they are retained as a validation/reference layer rather than the main corpus.

---

## Files

| File | Role | Description | Rows |
|------|------|-------------|------|
| **inter_korean_summit_full_sentences.csv** | Primary | Full multi-year sentence-level reconstruction from the six upstream Mendeley files | 18,018 |
| **inter_korean_summit_full_article_candidates.csv** | Secondary | Heuristic all-years article-candidate reconstruction from the upstream annotated files | 455 |
| **inter_korean_summit_2018_articles.csv** | Reference | High-confidence article-level UTF-8 corpus generated from the local raw 2018 files in this repo | 252 |
| **corpus_manifest.json** | Metadata | Declares dataset roles so the canonical file is explicit | — |
| **build_inter_korean_summit.py** | Build script | Rebuilds the local 2018 article-level subset from the repo's raw UTF-16LE files | — |
| **build_inter_korean_summit_full.py** | Build script | Downloads the six upstream Mendeley files and rebuilds the full sentence and heuristic article-candidate corpora | — |
| **\*.txt** | Source files | Local raw 2018 source files already present in the repo; UTF-16LE encoded and grouped by newspaper, genre, and coverage date | 9 files |

Rebuild command:

```bash
python data/inter_korean_summit/build_inter_korean_summit.py
python data/inter_korean_summit/build_inter_korean_summit_full.py
```

---

## Variables Included

### `inter_korean_summit_full_sentences.csv` (Primary)

10 columns, 18,018 rows. Each row is one reconstructed sentence.

| Variable | Type | Description |
|----------|------|-------------|
| **sentence_id** | string | Stable sentence identifier derived from year, source, and sentence index |
| **source_file** | string | Upstream Mendeley filename |
| **newspaper** | string | English newspaper name |
| **newspaper_ko** | string | Korean newspaper name |
| **year** | string | Summit year from the upstream filename: `2000`, `2007`, `2018` |
| **summit_episode** | string | Year-level event grouping: `2000_june_summit`, `2007_october_summit`, `2018_multi_summit` |
| **sentence_index** | integer | Sentence order within the upstream file |
| **sentence_text** | string | Reconstructed sentence text after eojeol-level rejoining |
| **is_sentence_terminal** | boolean | Whether the source sentence block ends with sentence-final punctuation in the annotated file |
| **n_eojeols** | integer | Number of eojeol lines in the source sentence block |

### `inter_korean_summit_full_article_candidates.csv` (Secondary)

16 columns, 455 rows. Each row is one **heuristic article candidate** reconstructed from the upstream annotated files.

| Variable | Type | Description |
|----------|------|-------------|
| **doc_id** | string | Stable candidate-document identifier |
| **source_file** | string | Upstream Mendeley filename |
| **newspaper** | string | English newspaper name |
| **newspaper_ko** | string | Korean newspaper name |
| **year** | string | Summit year from the upstream filename |
| **summit_episode** | string | Year-level event grouping |
| **doc_index** | integer | Candidate-document order within the source file |
| **headline_candidate** | string | Headline-like string inferred from unpunctuated runs, if detected |
| **standfirst_candidate** | string | Additional inferred headline/deck lines, if detected |
| **text** | string | Reconstructed candidate-document text with sentence breaks preserved |
| **start_sentence_index** | integer | First sentence index in the source file assigned to this candidate document |
| **end_sentence_index** | integer | Last sentence index in the source file assigned to this candidate document |
| **n_sentences** | integer | Number of reconstructed sentences in the candidate document |
| **n_chars** | integer | Character count of `text` |
| **has_headline_candidate** | boolean | Whether a headline-like boundary cue was detected |
| **boundary_method** | string | Boundary rule used to start the candidate document |

### `inter_korean_summit_2018_articles.csv` (Reference)

14 columns, 252 rows. Each row is one article.

| Variable | Type | Description |
|----------|------|-------------|
| **doc_id** | string | Stable article identifier derived from date, source, genre, and source block index |
| **source_file** | string | Raw source filename from which the article was parsed |
| **block_index** | integer | Article position within the raw source file after splitting on blank-line boundaries |
| **newspaper** | string | English newspaper name: `Chosun Ilbo` or `Hankyoreh` |
| **newspaper_ko** | string | Korean newspaper name: `조선일보` or `한겨레` |
| **genre** | string | Source genre from filename: `news` or `editorial` |
| **coverage_date** | string | Date encoded in the raw source filename (`YYYY-MM-DD`) |
| **summit_episode** | string | Curator-assigned event grouping. Current values: `2018_april_summit`, `2018_may_summit` |
| **headline** | string | Article headline |
| **standfirst** | string | Short summary/deck lines between headline and body, if present. Multi-line values are newline-separated |
| **body** | string | Main article text with paragraph breaks preserved |
| **full_text** | string | `headline`, `standfirst`, and `body` combined into a single text field |
| **n_paragraphs** | integer | Number of body paragraphs after parsing |
| **n_chars** | integer | Character count of the `body` field |

---

## Coverage Summary

### Primary Sentence Reconstruction

| Year | Sentences |
|------|-----------|
| **2000** | 2,435 |
| **2007** | 5,075 |
| **2018** | 10,508 |

| Newspaper | Sentences |
|-----------|-----------|
| **Chosun Ilbo** | 6,455 |
| **Hankyoreh** | 11,563 |

### Secondary Heuristic Article Candidates

| Year | Candidate Documents |
|------|---------------------|
| **2000** | 14 |
| **2007** | 42 |
| **2018** | 399 |

| Newspaper | Candidate Documents |
|-----------|---------------------|
| **Chosun Ilbo** | 235 |
| **Hankyoreh** | 220 |

### Reference 2018 Article Subset

| Coverage Date | Articles | Notes |
|---------------|----------|-------|
| **2018-04-27** | 194 | First 2018 summit coverage |
| **2018-05-26** | 13 | Same-day coverage of the second 2018 summit |
| **2018-05-27** | 45 | Follow-up coverage after the second 2018 summit |

### By Newspaper

| Newspaper | Articles |
|-----------|----------|
| **Chosun Ilbo** | 108 |
| **Hankyoreh** | 144 |

### By Genre

| Genre | Articles |
|-------|----------|
| **news** | 242 |
| **editorial** | 10 |

---

## Recommended Use

- Start with **`inter_korean_summit_full_sentences.csv`** if you want the canonical, full-coverage corpus.
- Use **`inter_korean_summit_full_article_candidates.csv`** only when you need document-like groupings and can tolerate heuristic article boundaries.
- Use **`inter_korean_summit_2018_articles.csv`** as a validation/reference layer when checking the quality of article-boundary heuristics against the locally preserved 2018 raw files.

---

## Reconstruction Notes

- The raw source files are **UTF-16LE**; the cleaned CSV is written as **UTF-8**.
- The local repo files preserve blank-line article separation well enough for the 2018 article-level subset.
- Short pre-body lines were extracted into `standfirst` when they behave like summary/deck text rather than article prose.
- **6 bodyless/title-only blocks** were dropped during cleaning:
  - 2 from `Chosun news 2018 April 27 corpus.txt`
  - 4 from `Chosun news 2018 May 27 corpus.txt`
- The upstream Mendeley files are **annotated sentence streams** using the Trends 21 PoS tagset.
- The sentence-level reconstruction uses **eojeol-level rejoining** with `kiwipiepy` plus a small compatibility-jamo recomposition pass to recover cleaner surface forms such as `열린다`, `한다`, and `올림`.
- The all-years article-candidate file uses **headline-like unpunctuated runs** as document-boundary cues. This is useful for exploration, but it is **not a gold-standard article segmentation**.
- Some source artifacts remain in the upstream reconstruction, including occasional `?` characters and imperfect spacing inherited from the annotated source.

---

## Source and Attribution

This cleaned subset is derived from the following upstream dataset:

> Park, Jin Hee. (2020). *Inter-Korean summit corpus* (Version 1) [Data set]. Mendeley Data. https://doi.org/10.17632/mp3drsh4hs.1

The Mendeley record states that the original corpus was compiled for:

> Park, J. (2020). *Discourse Construction of Inter-Korean Summits in South Korean Newspapers*.

According to the upstream record, the original full dataset includes six diachronic corpora spanning the 2000, 2007, and 2018 summits and was released under **CC BY 4.0**. The Mendeley public API exposes six downloadable files:

- `Chosun 2000 annotated text file unicode.txt`
- `Chosun 2007 annotated text file unicode.txt`
- `Chosun 2018 total annotated text file unicode.txt`
- `Hankyoreh 2000 annotated text file unicode.txt`
- `Hankyoreh 2007 annotated text file unicode.txt`
- `Hankyoreh 2018 total annotated text file unicode.txt`

The upstream license note also states that additional permission may be required for third-party newspaper content identified within the dataset.
