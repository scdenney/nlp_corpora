# NLP Corpora for Korean Studies

A curated collection of text corpora for digital humanities and computational social science research on Korea. These datasets are intended for students, researchers, and instructors at the Leiden Institute for Area Studies and beyond who are interested in applying computational methods to Korean-language primary sources.

This repository is maintained by **Steven Denney** (Leiden University). Additional corpora will be added over time.

---

## Repository Contents

### Primary Corpora

| Corpus | Description | Location |
|--------|-------------|----------|
| **NIKH History Textbooks** | Korean history textbooks from the National Institute of Korean History, spanning late Joseon through contemporary national curricula. Includes book-level and sentence-level formats. | [`/nikh`](./nikh) |
| **Kaebyok Magazine (1920–1935)** | Full-text articles from the interwar Korean magazine reflecting cultural, intellectual, and political debates during the colonial period. Organized by publication date. | [`/kaebyok`](./kaebyok) |

### Research Corpora

The [`/final_project_corpora`](./final_project_corpora) folder contains six additional datasets suitable for text analysis:

| Corpus | Description | Data File |
|--------|-------------|-----------|
| **Immigrant Interviews** | Open-text survey responses from South Koreans explaining their preferences regarding immigrant admission. | `immigrant_interview.csv` |
| **North Korean Migrant Interviews** | Open-text explanations of South Korean attitudes toward North Korean migrant integration (voting, hiring, neighbor preferences). | `nkmigrants_interviews.csv` |
| **Moon Jae-in Twitter** | Tweets from President Moon Jae-in's official account (2012–2020), spanning pre-presidency through his administration. | `moon_twitter.csv` |
| **Korean Newspapers on Twitter** | Tweets from six major South Korean newspapers (July–August 2017), with left–right ideological classification. | `korean_newspapers_twitter.csv` |
| **Kyŏngje Yŏngu** | Articles from a North Korean economics journal (1987–2017), documenting economic discourse across three leadership periods. | `kjyg.csv` |
| **Presidential Speeches** | Korean presidential speeches from Rhee Syngman through Moon Jae-in, with metadata on era, regime type, and speech category. | `president_speech_ko.csv` |

Each dataset includes a Markdown documentation file (`.md`) with variable definitions, context, and suggested uses. See the [Corpora Guide](./final_project_corpora/final_project_guide.md) for details.

### Supplementary Resources

| Resource | Description | Location |
|----------|-------------|----------|
| **Korean Sentiment Dictionaries** | Positive and negative word lists for Korean sentiment analysis. | [`/sentiment_dic_kor`](./sentiment_dic_kor) |
| **Korean Stopwords** | Curated stopword list for Korean text preprocessing. | `stopwords_ko_ba3.txt` |
| **NK Migrant Data (Wide Format)** | Alternative format of the North Korean migrant interview responses with columns for each task type. | [`/nk_migrant`](./nk_migrant) |
| **Preprocessing Scripts** | Python scripts for text cleaning and preprocessing (Mac and Windows versions). | Root directory |

---

## Getting Started

1. **Browse the corpora** using the tables above to identify datasets relevant to your research interests.
2. **Read the documentation** (`.md` and `README.md` files) before working with any dataset. These files explain the variables, data sources, and any preprocessing that has been applied.
3. **Download or clone** the repository to access the data files directly.

---

## Intended Audience

These corpora are designed for:

- Students in Korean Studies and related area studies programs
- Researchers in digital humanities and computational social science with an interest in Korea
- Instructors developing courses on text analysis, NLP, or computational methods for Korean-language materials
- Graduate students and advanced undergraduates working on theses or independent research projects

---

## Citation

If you use materials from this repository in your research or teaching, please cite the repository and, where applicable, the original sources documented in each dataset's `.md` file.

---

## License

See [LICENSE](./LICENSE) for details.

---

## Contact

For questions, suggestions, or contributions, please contact Steven Denney at Leiden University or open an issue in this repository.
