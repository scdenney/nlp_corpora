# NLP Corpora for Korean Studies

A curated collection of text corpora for digital humanities and computational social science research on Korea. These datasets support students, researchers, and instructors at the Leiden Institute for Area Studies and beyond who are interested in applying computational methods to Korean-language primary sources.

This repository is maintained by **Steven Denney** (Leiden University). Additional corpora will be added over time.

---

## Corpora

All corpora are located in the [`/data`](./data) folder. Each folder contains data files and documentation.

### Historical Sources

| Corpus | Description | Rows | Folder |
|--------|-------------|------|--------|
| **Korean Newspaper Archive (1883–1952)** | Articles from 39 Korean newspapers spanning the late Joseon, Korean Empire, colonial, and early Republic periods. Major titles include Hwangseong Sinmun, Daehan Maeil Sinbo, and Dongnip Sinmun. | 364,409 | [`korean_newspaper_archive`](./data/korean_newspaper_archive) |
| **Colonial-Era Magazines (1896–1943)** | Articles from 19 Korean magazines of the late Joseon and colonial periods, including Kaebyok, Samcheolli, Byeolgeongon, and Donggwang. Covers intellectual debate, nationalism, literature, and social reform. | 15,326 | [`colonial_magazines`](./data/colonial_magazines) |
| **NIKH History Textbooks** | Korean history textbooks from the National Institute of Korean History (NIKH) and additional sources, spanning late Joseon through contemporary national curricula. | 67 | [`nikh`](./data/nikh) |

### North Korean Texts

| Corpus | Description | Rows | Folder |
|--------|-------------|------|--------|
| **Rodong Sinmun (English)** | English-language articles from North Korea's *Rodong Sinmun* (Workers' Daily), the official newspaper of the Workers' Party of Korea (2018–2022). | 9,797 | [`rodong_sinmun`](./data/rodong_sinmun) |
| **Kyŏngje Yŏngu** | Articles from a North Korean economics journal (1987–2017). | 2,583 | [`kyongje_yongu`](./data/kyongje_yongu) |

### South Korean Politics

| Corpus | Description | Rows | Folder |
|--------|-------------|------|--------|
| **Presidential Speeches** | Korean presidential speeches from Rhee Syngman through Moon Jae-in. | 8,771 | [`president_speeches`](./data/president_speeches) |
| **Blue House Petitions** | Citizen petitions submitted to the Moon Jae-in administration's Blue House National Petition system (2017–2018). Includes petition text, category, vote count, and response status. 5% sample of the full corpus. | 18,077 | [`bluehouse_petitions`](./data/bluehouse_petitions) |
| **Inter-Korean Summit Corpus** | Newspaper article coverage of the 2000, 2007, and 2018 inter-Korean summits from *Chosun Ilbo* and *Hankyoreh*. | 455 | [`inter_korean_summit`](./data/inter_korean_summit) |

### Media & Social Media

| Corpus | Description | Rows | Folder |
|--------|-------------|------|--------|
| **Moon Jae-in Twitter** | Tweets from President Moon Jae-in's official account (2012–2020). | 3,148 | [`moon_twitter`](./data/moon_twitter) |
| **Korean Newspapers on Twitter** | Tweets from six major South Korean newspapers (July–August 2017). | 2,748 | [`kr_newspapers`](./data/kr_newspapers) |

### Literature

| Corpus | Description | Rows | Folder |
|--------|-------------|------|--------|
| **KPoEM** | Korean poetry by five canonical modern poets (Yun Dong-ju, Kim So-wol, Han Yong-un, Im Hwa, Yi Sang), annotated with 44 fine-grained emotion categories by five human annotators. Includes line-level and poem-level datasets. | 7,622 | [`kpoem`](./data/kpoem) |

### Survey & Interview Data

| Corpus | Description | Rows | Folder |
|--------|-------------|------|--------|
| **Immigrant Interviews** | Open-text survey responses from South Koreans explaining immigrant admission preferences. | 1,008 | [`immigrant_interviews`](./data/immigrant_interviews) |
| **North Korean Migrant Interviews** | Open-text explanations of attitudes toward North Korean migrant integration. | 6,027 | [`nkmigrants_interviews`](./data/nkmigrants_interviews) |

---

## External Resources

The following large-scale corpora are hosted externally and may be useful for Korean studies research. They are not included in this repository due to size and licensing constraints (all carry non-commercial licenses), but they are freely accessible for academic use.

| Corpus | Description | Size | License | Link |
|--------|-------------|------|---------|------|
| **Open Korean Historical Corpus (OKHC)** | A diachronic collection spanning 1,300 years of Korean textual production, drawn from 19 archives including the Annals of the Joseon Dynasty, Diaries of the Royal Secretariat, Korean Literary Collections (ITKC), colonial-era newspapers, and KCNA. Covers Korean (Middle, Early Modern, Modern, North Korean), Classical Chinese, and Japanese. Approximately 42% of documents include full text; the remainder are metadata with links to original sources. | 17.7M documents, 5.1B tokens | CC BY-NC 4.0 | [HuggingFace](https://huggingface.co/datasets/seyoungsong/Open-Korean-Historical-Corpus) |
| **LBOX OPEN** | Korean court precedents from the Supreme Court, appellate courts, and district courts. Includes case text, classification labels, and summarization data. Useful for studying judicial reasoning, legal language, and institutional change in South Korea. | 147K precedents, 259M tokens | CC BY-NC 4.0 | [HuggingFace](https://huggingface.co/datasets/lbox/lbox_open) |
| **Namuwiki Corpus** | Full text of Namuwiki, South Korea's most popular user-generated wiki. Far richer than Korean Wikipedia for Korean pop culture, politics, internet culture, and social issues. Written in informal contemporary Korean. | 867K articles, ~3GB | CC BY-NC-SA 2.0 | [HuggingFace](https://huggingface.co/datasets/heegyu/namuwiki) |

---

## Intended Audience

- Students in Korean Studies and related area studies programs
- Researchers in digital humanities and computational social science
- Instructors developing courses on text analysis or computational methods
- Graduate students working on theses or independent research

---

## Citation

If you use materials from this repository, please cite as:

> Denney, Steven. (2025). *NLP Corpora for Korean Studies*. GitHub repository. https://github.com/scdenney/nlp_corpora

For individual datasets, please also cite the original sources documented in each folder's README.

---

## License

See [LICENSE](./LICENSE) for details.

---

## Contact

Steven Denney, Leiden University (s.c.denney@hum.leidenuniv.nl)
