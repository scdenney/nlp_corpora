# NLP Corpora for Korean Studies

A curated collection of text corpora for digital humanities and computational social science research on Korea. These datasets support students, researchers, and instructors at the Leiden Institute for Area Studies and beyond who are interested in applying computational methods to Korean-language primary sources.

This repository is maintained by **Steven Denney** (Leiden University). Additional corpora will be added over time.

---

## Repository Structure

```
nlp_corpora/
├── data/                  # Research corpora with documentation
├── nikh/                  # NIKH History Textbook corpus
├── kaebyok/               # Kaebyok Magazine (1920–1935)
└── README.md
```

---

## Corpora

### NIKH History Textbooks

Korean history textbooks from the National Institute of Korean History, spanning late Joseon through contemporary national curricula. Includes book-level and sentence-level formats.

- **Location:** [`/nikh`](./nikh)
- **Documentation:** [`/nikh/README.md`](./nikh/README.md)
- **Online source:** [contents.history.go.kr](https://contents.history.go.kr/front/ta/main.do)

### Kaebyok Magazine (1920–1935)

Full-text articles from the interwar Korean magazine *Kaebyok*, reflecting cultural, intellectual, and political debates during the Japanese colonial period. Articles are organized by publication date.

- **Location:** [`/kaebyok`](./kaebyok)

### Research Corpora

The [`/data`](./data) folder contains six additional datasets, each with its own documentation:

| Corpus | Description | Folder |
|--------|-------------|--------|
| **Immigrant Interviews** | Open-text survey responses from South Koreans explaining immigrant admission preferences. | [`immigrant_interviews`](./data/immigrant_interviews) |
| **North Korean Migrant Interviews** | Open-text explanations of attitudes toward North Korean migrant integration. | [`nkmigrants_interviews`](./data/nkmigrants_interviews) |
| **Moon Jae-in Twitter** | Tweets from President Moon Jae-in's official account (2012–2020). | [`moon_twitter`](./data/moon_twitter) |
| **Korean Newspapers on Twitter** | Tweets from six major South Korean newspapers (July–August 2017). | [`kr_newspapers`](./data/kr_newspapers) |
| **Kyŏngje Yŏngu** | Articles from a North Korean economics journal (1987–2017). | [`kyongje_yongu`](./data/kyongje_yongu) |
| **Presidential Speeches** | Korean presidential speeches from Rhee Syngman through Moon Jae-in. | [`president_speeches`](./data/president_speeches) |

See the [data folder README](./data/README.md) for detailed information about each dataset.

---

## Getting Started

1. **Browse the corpora** using the tables above to identify datasets relevant to your research.
2. **Read the documentation** (`README.md` files in each folder) before working with any dataset.
3. **Download or clone** the repository to access the data files.

---

## Intended Audience

- Students in Korean Studies and related area studies programs
- Researchers in digital humanities and computational social science
- Instructors developing courses on text analysis or computational methods
- Graduate students working on theses or independent research

---

## Citation

If you use materials from this repository, please cite the repository and the original sources documented in each dataset folder.

---

## License

See [LICENSE](./LICENSE) for details.

---

## Contact

For questions or suggestions, contact Steven Denney at Leiden University or open an issue in this repository.
