# Inter-Korean Summit Corpus

## Overview

This folder contains newspaper coverage of the 2000, 2007, and 2018 inter-Korean summits from *Chosun Ilbo* and *Hankyoreh*. It is based on Jin Hee Park's *Inter-Korean summit corpus* and combines a sentence-level master file with reconstructed article-level files for researchers who need both granular text analysis and article-oriented views.

## At a Glance

| Item            | Details                                                    |
|:----------------|:-----------------------------------------------------------|
| Coverage        | 2000, 2007, and 2018 inter-Korean summits                  |
| Sources         | *Chosun Ilbo* and *Hankyoreh*                              |
| Main file       | `inter_korean_summit_sentences.csv`                        |
| Total size      | 18,018 sentences and 455 reconstructed articles            |
| Format          | UTF-8 CSV                                                  |
| Upstream source | Jin Hee Park, *Inter-Korean summit corpus* (Mendeley Data) |

## Files

| File                                           | Description                                                                      |   Rows |
|:-----------------------------------------------|:---------------------------------------------------------------------------------|-------:|
| `inter_korean_summit_sentences.csv`            | Main corpus. One row per sentence with newspaper, year, summit episode, and text | 18,018 |
| `inter_korean_summit_articles.csv`             | Reconstructed article-level corpus for the full dataset                          |    455 |
| `inter_korean_summit_articles_chosun_ilbo.csv` | Reconstructed article-level file for *Chosun Ilbo*                               |    235 |
| `inter_korean_summit_articles_hankyoreh.csv`   | Reconstructed article-level file for *Hankyoreh*                                 |    220 |
| `inter_korean_summit_2018_articles.csv`        | Cleaner 2018 article-level subset built from local source files                  |    252 |

## Coverage Summary

### By Year

| Year | Sentences | Articles |
|-----:|----------:|---------:|
| 2000 |     2,435 |       14 |
| 2007 |     5,075 |       42 |
| 2018 |    10,508 |      399 |

### By Newspaper

| Newspaper     | Sentences | Articles |
|:--------------|----------:|---------:|
| *Chosun Ilbo* |     6,455 |      235 |
| *Hankyoreh*   |    11,563 |      220 |

### 2018 Reference File

| Coverage date | Articles |
|:--------------|---------:|
| 2018-04-27    |      194 |
| 2018-05-26    |       13 |
| 2018-05-27    |       45 |

## Recommended Starting Point

Start with `inter_korean_summit_sentences.csv` for most analysis. The article-level files are reconstructed from sentence streams and are useful for article-oriented reading, but article boundaries for 2000 and 2007 are inferred rather than preserved in the original source. The 2018 article file is cleaner because the local source material preserved article boundaries.

## Notes

- All files are UTF-8 CSVs.
- The article-level files are best treated as research conveniences rather than archival originals.
- The sentence-level file remains the most stable, analysis-ready version of the corpus.

## Source and Attribution

This corpus is reconstructed from:

> Park, Jin Hee. (2020). *Inter-Korean summit corpus* (Version 1) [Data set].
> Mendeley Data. <https://doi.org/10.17632/mp3drsh4hs.1>

The upstream Mendeley record lists the dataset under **CC BY 4.0**, with a note that third-party newspaper content may require additional permission.