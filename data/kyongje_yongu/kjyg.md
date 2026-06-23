# Kyŏngje Yŏngu (경제연구) — Data Card

North Korean economics journal *Kyŏngje Yŏngu* (경제연구, "Economic Research"), **1987–2020**. One row per article. See **[README.md](./README.md)** for full documentation, provenance, methods, and caveats.

| | |
|---|---|
| **Rows** | 3,036 articles |
| **Coverage** | 1987–2020 (quarterly; 133 of 136 issue-quarters — gaps at 1995-4, 2019-4, 2020-3) |
| **Columns** | `title`, `author`, `year_issue`, `word_count`, `file_path`, `content`, `source` |
| **Primary file** | `kjyg.parquet` (also `kjyg.csv`) |
| **Provenance** | `source`: `original_json` (1987..2017-3, 2,582) · `docx` (2017-4, 2018, 219) · `pdf_text` (2019, 2020, 235) |
| **Build** | `build_kjyg_2017_2020.py` + `kjyg_extract.py`; summary in `kjyg_build_qa.json` |
| **Language** | Korean, DPRK orthography (e.g., 로동/령도/리용); leader-name honorific PUA glyphs decoded to plain text |

```python
import pandas as pd
df = pd.read_parquet("data/kyongje_yongu/kjyg.parquet")
df["year"] = df["year_issue"].str.split("-").str[0].astype(int)
```

**Quick caveats.** 38 missing authors and 82 missing contents (unsigned editorials / glossary entries / baseline gaps). For the cleanest text, filter `source != "pdf_text"`. A misfiled `력사과학` (Historical Science) issue shipped as `경제연구 2020-3.pdf` is excluded by a journal-identity guard.
