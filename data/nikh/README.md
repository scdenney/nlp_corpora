# NIKH History Textbook Corpus

This folder contains the National Institute of Korean History (NIKH) history textbook corpus, a collection of Korean history textbooks produced under successive national curricula from the late Joseon and Korean Empire through the Japanese colonial period, liberation, and contemporary postwar curricula.

An online-navigable version of the original textbooks is available through the National Institute of Korean History: [contents.history.go.kr](https://contents.history.go.kr/front/ta/main.do)

---

## Files

| File | Description | Rows |
|------|-------------|------|
| **nikh_corpus.csv** | Full textbook corpus with book-level metadata and text | 176,881 |
| **nikh_sentences.csv** | Corpus split into individual sentences | 189,293 |
| **nikh_sentences_25percent.csv** | 25% random sample of sentences (for faster processing) | 46,424 |
| **code_book.csv** | Variable definitions for the corpus | 12 |

---

## Variables in nikh_corpus.csv

| Variable | Description |
|----------|-------------|
| **book_id** | Unique identifier for each textbook, derived from NIKH filenames (e.g., `ta_m71_gh`). Primary key for joining with other data. |
| **title** | Full title of the textbook. Often includes school level or historical focus. |
| **curriculum** | National curriculum period (e.g., '5th Curriculum', '7th Curriculum'). |
| **nikh_period** | Source-assigned period in which the textbook was published. |
| **period** | Historical period of production (e.g., 'Colonial', 'Postwar', 'Democratic'). |
| **level** | Educational level: 'Elementary', 'Middle School', or 'High School'. |
| **publisher** | Publishing institution or company. |
| **year** | Year of textbook publication. |
| **num_sections** | Number of structural sections (chapters, units) in the book. |
| **full_text** | Full digitized text with no preprocessing. |
| **clean_text** | Text with moderate preprocessing applied. |

---

## Variables in nikh_sentences.csv

| Variable | Description |
|----------|-------------|
| **period_ordered** | Numerical ordering of historical periods for sorting. |
| **book_id** | Textbook identifier (joins with nikh_corpus.csv). |
| **nikh_period** | Source-assigned historical period. |
| **level** | Educational level of the source textbook. |
| **sentence** | Individual sentence extracted from the textbook. |

---

## Usage Notes

- Use **nikh_corpus.csv** for book-level analysis (topic modeling across textbooks, comparing curricula, etc.)
- Use **nikh_sentences.csv** for sentence-level analysis (sentiment, keyword extraction, etc.)
- Use **nikh_sentences_25percent.csv** for prototyping or when working with limited computational resources
- See **code_book.csv** for detailed variable definitions
