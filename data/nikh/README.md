# NIKH History Textbook Corpus

This folder contains the National Institute of Korean History (NIKH; 국사편찬위원회) history textbook corpus, a collection of Korean history textbooks produced under successive national curricula from the late Joseon and Korean Empire through the Japanese colonial period, liberation, and contemporary postwar curricula.

An online-navigable version of the original textbooks is available through the National Institute of Korean History: [contents.history.go.kr](https://contents.history.go.kr/front/ta/main.do)

---

## Files

| File | Description | Rows |
|------|-------------|------|
| **nikh_corpus.csv** | Full textbook corpus with book-level metadata and text | 51 |
| **nikh_sentences.csv** | Corpus split into individual sentences | 86,740 |
| **nikh_sentences_25percent.csv** | 25% random sample of sentences (for faster processing) | ~21,685 |
| **code_book.csv** | Variable definitions for the corpus | 12 |

---

## Variables in `nikh_corpus.csv`

12 columns. Each row is one textbook (51 books total).

| Variable | Type | Description |
|----------|------|-------------|
| **book_id** | string | Unique identifier for each textbook, derived from NIKH filenames (e.g., `ta_m71`, `ta_e51`, `ta_p11r`). Primary key for joining with sentence-level data. 51 unique values. |
| **title** | string | Full title of the textbook in Korean. See sample titles below. |
| **curriculum** | string | National curriculum period or pre-modern series code. 17 unique values (see value table below). |
| **nikh_period** | string | Source-assigned period in which the textbook was published. 10 unique values (see value table below). |
| **period** | string | Curator-assigned historical era of production. 8 unique values (see value table below). |
| **level** | string | Educational level. 4 values: `Elementary`, `Middle School`, `High School`, `Public schools`. |
| **publisher** | string | Publishing institution or company (in Korean). 7 unique values (see translations below). Some `NaN` for pre-modern books. |
| **year** | float | Year of textbook publication. 11 unique values ranging from 1895 to 2002. `NaN` for some pre-modern books. |
| **num_sections** | integer | Number of structural sections (chapters, units) in the book. |
| **full_text** | string | Full digitized text with no preprocessing. |
| **clean_text** | string | Text with moderate preprocessing applied. |
| **period_ordered** | string | Same as `period` but prefixed with a sort number (e.g., `1. Late Choson / Korean Empire`). |

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
| 7th National Curriculum (2002-) | — |

---

## `period` Values (Curator-Assigned Historical Eras)

| Value | Approximate Years | Context |
|-------|-------------------|---------|
| Late Choson / Korean Empire | 1895–1910 | Reforms, sovereignty under threat |
| Colonial Period | 1910–1945 | Japanese rule; textbooks published by 문부성 (Japanese Ministry of Education) |
| U.S. Military Government | 1945–1948 | Post-liberation transition; textbooks published by 진단학회 (Chindan Society) |
| Postwar Authoritarian | 1954–1972 | Rhee Syngman and early Park Chung-hee; 1st–2nd Curricula |
| Yushin Era | 1972–1981 | Park's authoritarian Yushin constitution; 3rd Curriculum |
| Chun/Roh Transitional | 1981–1992 | Military-to-civilian transition; 4th–5th Curricula |
| Early Democratic | 1992–2002 | Kim Young-sam and Kim Dae-jung presidencies; 6th Curriculum |
| Democratic Consolidation | 2002– | 7th Curriculum onward |

---

## `curriculum` Values

The 17 unique values fall into two groups:

- **Named curricula:** `1st Curriculum` through `7th Curriculum` — corresponding to postwar national curricula.
- **Pre-modern series codes:** `p11 Series` through `p101 Series` — corresponding to pre-1945 textbook groupings in the NIKH catalog.

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

| book_id | Title (Korean) | Translation | Period | Level |
|---------|---------------|-------------|--------|-------|
| ta_p11r | 조선역사 상 | History of Joseon, Vol. 1 | Late Choson / Korean Empire | Public schools |
| ta_p21r | 조선역대사략 권1 | Abridged Dynastic History of Joseon, Vol. 1 | Late Choson / Korean Empire | Public schools |
| ta_p71r | 보통교과 동국역사(1권) | Standard Curriculum: History of the Eastern Country, Vol. 1 | Late Choson / Korean Empire | Elementary |
| ta_p91r | 초등대한역사 | Elementary Korean History | Late Choson / Korean Empire | Elementary |
| ta_p31r | 심상소학국사보충아동용 - 1 | Supplementary National History for Elementary Children, Vol. 1 | Colonial Period | — |
| ta_p51r | 국사교본 | National History Textbook | U.S. Military Government | — |
| ta_e11 | 초등학교 사회생활 6-1(1차) | Elementary School Social Life 6-1 (1st Curriculum) | Postwar Authoritarian | Elementary |
| ta_m31 | 중학교 국사 3차 | Middle School National History, 3rd Curriculum | Yushin Era | Middle School |
| ta_h71 | 고등학교 국사 7차 | High School National History, 7th Curriculum | Democratic Consolidation | High School |

---

## Variables in `nikh_sentences.csv`

5 columns. Each row is one sentence extracted from a textbook (86,740 sentences total, drawn from 51 books).

| Variable | Type | Description |
|----------|------|-------------|
| **period_ordered** | string | Numbered historical era for sort ordering (e.g., `6. Chun / Roh Transitional`). 8 unique values. |
| **book_id** | string | Textbook identifier. Joins to `nikh_corpus.csv`. 51 unique values. |
| **nikh_period** | string | Source-assigned historical period. Same 10 values as the corpus file. |
| **level** | string | Educational level of the source textbook. Same 4 values as the corpus file. |
| **sentence** | string | Individual sentence extracted from the textbook. |

---

## Data Quality Notes

- Some pre-modern textbooks (Korean Empire and Colonial eras) have `NaN` for `year`, `level`, and/or `publisher`.
- The `period_ordered` column in `nikh_sentences.csv` uses slightly different labels from `period` in `nikh_corpus.csv` (e.g., "Colonial" vs. "Colonial Period"), but the mapping is straightforward.

---

## Usage Notes

- Use **nikh_corpus.csv** for book-level analysis (topic modeling across textbooks, comparing curricula, etc.)
- Use **nikh_sentences.csv** for sentence-level analysis (sentiment, keyword extraction, etc.)
- Use **nikh_sentences_25percent.csv** for prototyping or when working with limited computational resources
- See **code_book.csv** for the original variable definitions
