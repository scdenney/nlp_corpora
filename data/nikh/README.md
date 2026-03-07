# NIKH History Textbook Corpus

This folder contains the National Institute of Korean History (NIKH; 국사편찬위원회) history textbook corpus, a collection of Korean history textbooks produced under successive national curricula from the late Joseon and Korean Empire through the Japanese colonial period, liberation, and contemporary postwar curricula — including the revised 7th Curriculum textbooks used through 2016.

An online-navigable version of the original textbooks is available through the National Institute of Korean History: [contents.history.go.kr](https://contents.history.go.kr/front/ta/main.do)

---

## Files

| File | Description | Rows |
|------|-------------|------|
| **nikh_corpus.csv** | Full textbook corpus with book-level metadata and text | 67 |
| **nikh_sentences.csv** | Corpus split into individual sentences (kiwipiepy) | 188,259 |
| **nikh_sentences_25percent.csv** | 25% stratified random sample of sentences | 47,065 |
| **code_book.csv** | Variable definitions for the corpus | — |

---

## Variables in `nikh_corpus.csv`

14 columns. Each row is one textbook (67 books total).

| Variable | Type | Description |
|----------|------|-------------|
| **book_id** | string | Unique identifier for each textbook. Two formats: `ta_*` for the original NIKH digitized series (51 books, 1895–2002); `H-*` for newer textbooks added in the revised 7th Curriculum era (16 books, 2002–2016). Primary key for joining with sentence-level data. |
| **title** | string | Full title of the textbook in Korean. See sample titles below. |
| **curriculum** | string | National curriculum period or pre-modern series code. 19 unique values (see value table below). |
| **nikh_period** | string | Source-assigned period in which the textbook was published. 10 unique values (see value table below). |
| **period** | string | Curator-assigned historical era. 5 values: `Late Choson`, `Colonial`, `Postwar`, `Authoritarian`, `Democratic`. |
| **level** | string | Educational level. 4 values: `Elementary`, `Middle School`, `High School`, `Public schools`. |
| **publisher** | string | Publishing institution or company (Korean). 5 missing values for pre-modern books. |
| **year** | float | Year of textbook publication. Range: 1895–2016. 9 missing values for pre-modern books. |
| **num_sections** | integer | Number of structural sections (chapters, units). |
| **full_text** | string | Full digitized text with no preprocessing. |
| **authors** | string | Author(s) or editor(s) listed for the textbook. Currently unpopulated (67 missing). |
| **notes** | string | Curatorial notes, e.g., provenance or inferences about metadata. 51 missing. |
| **num_pages** | float | Total number of pages in the textbook. Available for H-series books only; 51 missing. |
| **processed_text** | string | Preprocessed text: POS-filtered nouns (NNG, NNP), stopwords removed, min 2-char tokens, numbers removed. Produced via Kiwi morphological analysis. Ready for TF-IDF and topic modeling. |

---

## `period` Values

| Value | Approximate Years | Context |
|-------|-------------------|---------|
| `Late Choson` | 1895–1910 | Late Joseon reform era and Korean Empire |
| `Colonial` | 1910–1945 | Japanese colonial rule |
| `Postwar` | 1945–1954 | U.S. Military Government and early republic |
| `Authoritarian` | 1954–1992 | 1st through 5th Curricula; Park Chung-hee (incl. Yushin), Chun Doo-hwan, and transition period |
| `Democratic` | 1992–2016 | 6th Curriculum onward; Kim Young-sam through Park Geun-hye |

---

## `nikh_period` Values (Chronological)

| Value | Approximate Years |
|-------|-------------------|
| Enlightenment & Daehan Empire (1895-1910) | Late Joseon reform era and Korean Empire |
| Japanese Colonial (1910-1945) | Colonial occupation period |
| US Military Govt & Syllabus Period (1945-1954) | Post-liberation, pre-curriculum era |
| 1st National Curriculum (1954-1963) | — |
| 2nd National Curriculum (1963-1973) | — |
| 3rd National Curriculum (1973-1981) | — |
| 4th National Curriculum (1981-1987) | — |
| 5th National Curriculum (1987-1992) | — |
| 6th National Curriculum (1992-2002) | — |
| 7th National Curriculum (2002–) | Includes original (2002) and revised editions (2006–2016) |

---

## `curriculum` Values

19 unique values:

- **Named curricula:** `1st Curriculum` through `7th Curriculum`, plus `7th Curriculum (Revised)` and `5th-6th Transition`
- **Pre-modern series codes:** `p11 Series` through `p101 Series`

---

## `book_id` Format

| Format | Example | Count | Source | Years |
|--------|---------|-------|--------|-------|
| `ta_*` | `ta_m71`, `ta_e51`, `ta_p11r` | 51 | Original NIKH digitized collection | 1895–2002 |
| `H-*` | `H-1(1,2006)`, `H-54(2,2016)` | 16 | Revised 7th Curriculum textbooks | 2002–2016 |

The `H-*` identifiers encode publisher ID and edition year in parentheses.

---

## `publisher` Translations

| Korean | English | Era |
|--------|---------|-----|
| 학부 편집국 | Bureau of Education Editorial Office | Korean Empire (1895) |
| 개인출판 | Private/individual publication | Korean Empire |
| 문부성 | Japanese Ministry of Education | Colonial period |
| 진단학회 | Chindan Society (academic body) | U.S. Military Government |
| 문교부 | Ministry of Education (pre-1990 name) | 1st–4th Curricula (1954–1987) |
| 교육부 | Ministry of Education | 5th–6th Curricula (1987–2002) |
| 교육인적자원부 | Ministry of Education & Human Resources Development | 7th Curriculum (2002–) |

---

## Sample Titles (with Translations)

| book_id | Title (Korean) | Translation | Period | Level | Year |
|---------|---------------|-------------|--------|-------|------|
| ta_p11r | 조선역사 상 | History of Joseon, Vol. 1 | Late Choson | Public schools | 1895 |
| ta_p91r | 초등대한역사 | Elementary Korean History | Late Choson | Elementary | 1908 |
| ta_p31r | 심상소학국사보충아동용 - 1 | Supplementary National History for Elementary Children, Vol. 1 | Colonial | — | — |
| ta_p51r | 국사교본 | National History Textbook | Postwar | — | — |
| ta_e11 | 초등학교 사회생활 6-1(1차) | Elementary School Social Life 6-1 (1st Curriculum) | Authoritarian | Elementary | 1954 |
| ta_m31 | 중학교 국사 3차 | Middle School National History, 3rd Curriculum | Authoritarian | Middle School | 1973 |
| ta_h71 | 고등학교 국사 7차 | High School National History, 7th Curriculum | Democratic | High School | 2002 |
| H-10(4,2007) | 한국근현대사 | Korean Modern and Contemporary History | Democratic | High School | 2008 |
| H-54(2,2016) | 한국사 | Korean History | Democratic | High School | 2016 |

---

## Variables in `nikh_sentences.csv`

5 columns. Each row is one sentence extracted from a textbook (188,259 sentences total, from 67 books). Sentences were split using kiwipiepy's `split_into_sents` method and filtered to a minimum length of 2 characters.

| Variable | Type | Description |
|----------|------|-------------|
| **book_id** | string | Textbook identifier. Joins to `nikh_corpus.csv`. 67 unique values. |
| **nikh_period** | string | Source-assigned historical period. |
| **period** | string | Curator-assigned era. Same 5 values as the corpus file. |
| **level** | string | Educational level of the source textbook. |
| **sentence** | string | Individual sentence extracted from the textbook. |

---

## Data Quality Notes

- `authors` is unpopulated (67 missing) — no author-level data has been scraped yet.
- `notes` is populated for 16 H-series books and empty for the original ta-series.
- `num_pages` is available for H-series books only; the ta-series books have `NaN`.
- Some pre-modern textbooks (Korean Empire and Colonial eras) have `NaN` for `year`, `level`, and/or `publisher`.

---

## Usage Notes

- Use **nikh_corpus.csv** for book-level analysis (topic modeling across textbooks, comparing curricula, etc.)
- Use **processed_text** for ready-to-use noun tokens (TF-IDF, LDA, etc.)
- Use **nikh_sentences.csv** for sentence-level analysis (sentiment, keyword extraction, etc.)
- Use **nikh_sentences_25percent.csv** for prototyping or when working with limited computational resources
- See **code_book.csv** for the original variable definitions
