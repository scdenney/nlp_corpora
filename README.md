# NLP Corpora for Korean Studies

![Collections](https://img.shields.io/badge/Collections-16-blue)
![Primary Rows](https://img.shields.io/badge/Primary%20Rows-470K%2B-green)
![Coverage](https://img.shields.io/badge/Coverage-1883%20to%202022-orange)
![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey)

A curated collection of Korean-language and Korea-focused text corpora for digital humanities, Korean studies, and computational social science. The repository brings together historical newspapers and magazines, political speech and petition data, social media, literary corpora, and survey text in a single, well-documented working collection.

Maintained by **Steven Denney** (Leiden University). Each dataset folder includes a `README.md` with source notes, variable descriptions, file details, and reuse guidance.

[Browse the data catalog](./data) · [External resources](#external-resources) · [Citation](#citation) · [Contact](#contact)

## At a Glance

| Scope                 | Details                                                                                   |
|:----------------------|:------------------------------------------------------------------------------------------|
| Local collections     | 16 dataset folders: 15 primary corpora plus a dedicated *Kaebyok* collection              |
| Coverage              | Late Joseon to the 2020s, with premodern reference texts in the pseudohistory corpus      |
| Scale                 | 470,052 records across the 15 primary corpora, counted at each corpus's main working unit |
| Formats               | CSV, TSV, Parquet, JSONL, and companion PDFs                                              |
| Languages and scripts | Korean, mixed Hangul-Hanja, Classical Chinese, Japanese, and English                      |

## Why This Repository

- Brings together corpora that are usually scattered across archives, project repositories, and personal research workflows.
- Keeps dataset-level documentation close to the data so users can move from discovery to analysis without guesswork.
- Favors analysis-ready formats such as Parquet, CSV, TSV, and JSONL while preserving context about sources, licenses, and limitations.

## How to Use This Repository

1. Start with the [`data/`](./data) catalog to identify the corpus that matches your topic, period, or format needs.
2. Open the dataset-level `README.md` inside the corpus folder before using the files.
3. Use Parquet for large-scale analysis when available, and CSV or TSV when you need maximum interoperability.
4. Check the source and license notes in the dataset folder before redistribution or publication.

```python
import pandas as pd

df = pd.read_parquet("data/korean_newspaper_archive/korean_newspaper_archive.parquet")
```

## Corpus Catalog

| Corpus                                                              | Theme                 | Coverage                            | Scale                           | Formats        | Highlights                                                                      |
|:--------------------------------------------------------------------|:----------------------|:------------------------------------|:--------------------------------|:---------------|:--------------------------------------------------------------------------------|
| [Korean Newspaper Archive](./data/korean_newspaper_archive)         | Historical newspapers | 1883–1952                           | 364,409 articles                | Parquet, CSV   | 39 newspapers from the late Joseon period through the early Republic            |
| [Colonial-Era Magazines](./data/colonial_magazines)                 | Historical magazines  | 1896–1943                           | 15,326 articles                 | Parquet, CSV   | 19 magazines including *Kaebyok*, *Samcheolli*, *Byeolgeongon*, and *Donggwang* |
| [NIKH History Textbooks](./data/nikh)                               | Textbooks             | 1895–2016                           | 67 textbooks                    | CSV            | Curriculum-linked history textbook corpus with sentence-level derivatives       |
| [Korean Pseudohistory Primary Sources](./data/korean_pseudohistory) | Primary texts         | Premodern claims to modern editions | 9 texts / 764 pages             | JSONL, Parquet | OCR-extracted source texts with document-level metadata                         |
| [Rodong Sinmun (English)](./data/rodong_sinmun)                     | DPRK media            | 2018–2022                           | 9,797 articles                  | CSV            | English-language DPRK state newspaper coverage                                  |
| [Kyŏngje Yŏngu](./data/kyongje_yongu)                               | DPRK journal          | 1987–2017                           | 2,583 articles                  | CSV            | North Korean economics journal                                                  |
| [Presidential Speeches](./data/president_speeches)                  | South Korean politics | 1948–2022                           | 8,774 speeches                  | CSV            | Rhee Syngman to Moon Jae-in; synced to the Presidential Archive June 2026 with updater script |
| [Blue House Petitions](./data/bluehouse_petitions)                  | Civic petitions       | 2017–2018                           | 18,077 petitions                | CSV            | 5% stratified sample with petition text, votes, and response status             |
| [Inter-Korean Summit Corpus](./data/inter_korean_summit)            | Newspaper coverage    | 2000, 2007, 2018                    | 18,018 sentences / 455 articles | CSV            | *Chosun Ilbo* and *Hankyoreh* summit coverage                                   |
| [Moon Jae-in Twitter](./data/moon_twitter)                          | Social media          | 2012–2020                           | 3,148 tweets                    | CSV            | Official account history with derived period variables                          |
| [Korean Newspapers on Twitter](./data/kr_newspapers)                | Social media          | July–August 2017                    | 2,748 tweets                    | CSV            | Six major newspaper accounts with ideology mapping                              |
| [Naver Movie Reviews (Classroom Edition)](./data/naver_movie_reviews) | Internet language     | Reviews to 2015                     | 50,000 reviews                  | CSV            | Balanced sentiment labels, classroom-safe filtering, 398 hand-translated examples, companion [point-and-click app](https://scdenney.github.io/feeling-in-numbers/) |
| [KPoEM](./data/kpoem)                                               | Literature            | Colonial and post-liberation era    | 7,622 annotations               | TSV            | Poem-level and line-level emotion annotations; Yi Sang texts re-spaced for tokenization (see README) |
| [Immigrant Interviews](./data/immigrant_interviews)                 | Survey text           | February 2019                       | 1,008 responses                 | CSV            | Open-text explanations for immigrant preference choices                         |
| [North Korean Migrant Interviews](./data/nkmigrants_interviews)     | Survey text           | August–September 2021               | 6,027 responses                 | CSV            | Vote, hire, and neighbor tasks on co-ethnic migrant integration                 |

## Focused Collection

| Collection                                | Coverage  | Scale          | Format | Notes                                                               |
|:------------------------------------------|:----------|:---------------|:-------|:--------------------------------------------------------------------|
| [Kaebyok Magazine Corpus](./data/kaebyok) | 1920–1935 | 2,467 articles | CSV    | Standalone *Kaebyok* corpus with issue-level metadata and full text |

## External Resources

Corpora, archives, and databases useful for Korean studies that are hosted elsewhere due to size or licensing constraints. Organized by theme; all entries verified June 2026 unless noted.

### National corpus platforms

| Resource                                                                                                          | Coverage                                | Scale                        | Access       |
|:------------------------------------------------------------------------------------------------------------------|:----------------------------------------|:-----------------------------|:-------------|
| [NIKL Modu Corpus (모두의 말뭉치)](https://kli.korean.go.kr)                                                        | Official national corpora: newspaper, spoken, web, messenger | Billions of words, themed releases | Free; registration plus per-corpus application |
| [NIKL Korean Learner Corpus (학습자 말뭉치)](https://kcorpus.korean.go.kr)                                          | L2 Korean writing with morphological and error annotation, by learner L1 (2015–2023) | Hundreds of thousands of samples | Free search; application for bulk download |
| [AI Hub](https://www.aihub.or.kr)                                                                                 | Government AI training data: dialogue, summarization, parallel and domain corpora | Hundreds of Korean datasets | Free; Korean account verification (overseas access can be limited) |

### News and contemporary media

| Resource                                                                                                          | Coverage                                | Scale                        | Access       |
|:------------------------------------------------------------------------------------------------------------------|:----------------------------------------|:-----------------------------|:-------------|
| [BigKinds (뉴스빅데이터)](https://www.bigkinds.or.kr)                                                              | Korea Press Foundation news analysis platform, 1990s–present | 116M+ articles, ~13K added daily | Free registration; search, analytics, Excel export |
| [Korean Newspaper Archive (NLK)](https://nl.go.kr/newspaper/)                                                     | Digitized newspapers, 1883 to the 1960s | 108 titles, 8.67M articles | Web viewer with full-text search; no bulk download |
| [Naver News Library](https://newslibrary.naver.com)                                                               | Major dailies 1920–1999, page images with OCR text | Four major dailies and more | Web viewer; no bulk download |
| [KcBERT Pretraining Corpus](https://www.kaggle.com/datasets/junbumlee/kcbert-pretraining-corpus-korean-news-comments) | Portal-news comments (2019–2020), raw internet Korean at scale | Tens of millions of comments | Kaggle download |

### Politics and government

| Resource                                                                                                          | Coverage                                | Scale                        | Access       |
|:------------------------------------------------------------------------------------------------------------------|:----------------------------------------|:-----------------------------|:-------------|
| [Presidential Archive Speech Records (대통령기록관 연설기록)](https://www.pa.go.kr/research/contents/speech/)      | Speeches of all completed presidencies, Rhee through Moon | ~9,000 speeches with metadata | Web; source of this repo's local corpus (see `data/president_speeches`) |
| [National Assembly Open Data (열린국회정보)](https://open.assembly.go.kr)                                          | Plenary and committee minutes, bills, members, votes | Open API plus bulk downloads | Free; API key registration |
| [Blue House Petitions Archive](https://github.com/lovit/petitions_archive)                                        | Full 청와대 national petitions, Aug 2017–2019 (complements this repo's 5% sample) | ~277K petitions | GitHub + Python package |
| [Manifesto Project (MARPOR)](https://manifesto-project.wzb.eu)                                                    | Human-coded party election programs, 67 countries incl. South Korea | 5,285 manifestos, 3.3M coded quasi-sentences | Free academic registration; API + manifestoR |
| [Policy Briefings (대한민국 정책브리핑)](https://www.korea.kr)                                                     | Government press releases, briefings, and speech texts incl. presidential statements | Continuous since the 2000s | Web; KOGL-licensed government content |
| [LBOX OPEN](https://huggingface.co/datasets/lbox/lbox_open)                                                       | South Korean court precedents           | 147K precedents, 259M tokens | Hugging Face |

### History and classics

| Resource                                                                                                          | Coverage                                | Scale                        | Access       |
|:------------------------------------------------------------------------------------------------------------------|:----------------------------------------|:-----------------------------|:-------------|
| [Korean History Database (NIKH)](https://db.history.go.kr)                                                        | Primary sources from antiquity to the contemporary period incl. the Joseon Annals | Dozens of collections | Web interface; bulk access by arrangement |
| [ITKC Korean Classics DB (한국고전종합DB)](https://db.itkc.or.kr)                                                  | Classical texts and Korean translations: Sillok, Seungjeongwon Ilgi, munjip collections | 1,250+ authors' collected works; 260 translated titles | Free web + OpenAPI |
| [Open Korean Historical Corpus (OKHC)](https://huggingface.co/datasets/seyoungsong/Open-Korean-Historical-Corpus) | Diachronic Korean textual production    | 17.7M documents, 5.1B tokens | Hugging Face |
| [Wilson Center Digital Archive](https://digitalarchive.wilsoncenter.org)                                          | Declassified Cold War documents on Korea (incl. the North Korea International Documentation Project), English translations | Thousands of documents | Free web access (site blocks some automated fetchers; verified by reputation) |

### Culture, literature, and language variety

| Resource                                                                                                          | Coverage                                | Scale                        | Access       |
|:------------------------------------------------------------------------------------------------------------------|:----------------------------------------|:-----------------------------|:-------------|
| [Gongu Madang (공유마당)](https://gongu.copyright.or.kr)                                                           | Public-domain and freely licensed Korean works incl. expired-copyright literature | Tens of thousands of items | Free download; KOGL / CC / donation licenses |
| [Encyclopedia of Korean Culture (한국민족문화대백과사전)](https://encykorea.aks.ac.kr)                              | Scholarly encyclopedia of Korean history and culture (AKS) | 70K+ entries (History alone 25K) | Free web access |
| [Jejueo Datasets (JIT/JSS)](https://github.com/kakaobrain/jejueo)                                                 | Jejueo–Korean parallel sentences + single-speaker speech for the endangered Jeju language | 170K+ sentence pairs; 10K audio clips | Kaggle, Apache-2.0 |
| [Korean Parallel Corpora](https://github.com/jungyeul/korean-parallel-corpora)                                    | KO–EN/FR parallel text incl. a North Korean–English news corpus | 31K-sentence bible corpus + news sets | GitHub, CC BY-SA 3.0 |

### Benchmarks and web-scale text

| Resource                                                                                                          | Coverage                                | Scale                        | Access       |
|:------------------------------------------------------------------------------------------------------------------|:----------------------------------------|:-----------------------------|:-------------|
| [KLUE Benchmark](https://huggingface.co/datasets/klue/klue)                                                       | Contemporary Korean NLU tasks incl. news-headline topic classification | 8 tasks, 9K–55K rows each | Hugging Face, CC BY-SA 4.0 |
| [Korean HateSpeech Dataset](https://github.com/kocohub/korean-hate-speech)                                        | Entertainment-news comments annotated for bias and toxicity | 9,381 labeled + 2M unlabeled comments | GitHub, CC BY-SA 4.0; handle with care in teaching |
| [Namuwiki Corpus](https://huggingface.co/datasets/heegyu/namuwiki)                                                | Contemporary user-generated Korean wiki | 867K articles, ~3 GB         | Hugging Face |
| [OPUS](https://opus.nlpl.eu)                                                                                      | Parallel corpora with Korean pairs (subtitles, web crawls, TED) | Varies by corpus | Free downloads; per-corpus licenses |

## Teaching With These Corpora

Companion repositories that put these corpora to work in the classroom:

| Repository                                                                  | What it is                                                                                                          |
|:-----------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------|
| [feeling-in-numbers](https://github.com/scdenney/feeling-in-numbers)         | Point-and-click text lab over the Naver Movie Reviews corpus, [live on GitHub Pages](https://scdenney.github.io/feeling-in-numbers/) — built for the Leiden PRE-Class in Asian Studies |
| [ba2-final-paper-data](https://github.com/scdenney/ba2-final-paper-data)     | Curated 10-corpus menu with samples, data dictionaries, and an example paper for the BA2 Digital Korea final paper    |
| [ba2_digital-korea](https://github.com/scdenney/ba2_digital-korea)           | Course materials introducing digital humanities and computational text analysis                                      |
| [ba3_text_as_data](https://github.com/scdenney/ba3_text_as_data)             | The digital-humanities strand of BA3 Contemporary Korea and Digital Humanities                                        |
| [corpus-building](https://github.com/scdenney/corpus-building)               | Wizard, skills, and scripts that turn a folder of PDFs into an analysis-ready text corpus                             |

## Intended Audience

- Students in Korean studies and related area studies programs
- Researchers in digital humanities and computational social science
- Instructors building courses on text analysis or computational methods
- Graduate students working on theses, replication studies, and independent projects

## Citation

If you use this repository, cite the repository-level [`CITATION.cff`](./CITATION.cff) file or use the reference below:

> Denney, Steven. (2026). *NLP Corpora for Korean Studies*. GitHub repository.
> <https://github.com/scdenney/nlp_corpora>

For dataset-specific attribution, also cite the original source or publication documented in the dataset folder.

## License

This repository is released under [CC BY-NC 4.0](./LICENSE). Some individual corpora carry their own upstream licenses or public-domain status, so always check the dataset-level `README.md` before reuse.

## Contact

Steven Denney, Leiden University (<s.c.denney@hum.leidenuniv.nl>)