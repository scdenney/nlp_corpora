# Korean Presidential Speeches

`president_speech_ko.csv` contains **9,883 full-text records from 14 presidents**, from Syngman Rhee through Lee Jae-myung. Last updated **2026-10-07**. Each row has `division_number`, `president`, `title`, `date`, `location`, `kind`, and `speech_text`.

| President | Records | President | Records |
|---|---:|---|---:|
| 이승만 (Syngman Rhee) | 998 | 윤보선 (Yun Posun) | 3 |
| 박정희 (Park Chung-hee) | 1,270 | 최규하 (Choi Kyu-hah) | 58 |
| 전두환 (Chun Doo-hwan) | 602 | 노태우 (Roh Tae-woo) | 601 |
| 김영삼 (Kim Young-sam) | 728 | 김대중 (Kim Dae-jung) | 822 |
| 노무현 (Roh Moo-hyun) | 780 | 이명박 (Lee Myung-bak) | 1,027 |
| 박근혜 (Park Geun-hye) | 493 | 문재인 (Moon Jae-in) | 1,392 |
| 윤석열 (Yoon Suk-yeol) | 721 | 이재명 (Lee Jae-myung) | 388 |

## Sources and coverage

- **Presidential Archive** ([연설기록](https://www.pa.go.kr/research/contents/speech/index.jsp), text category `c_pa02062`): 9,477 rows, including all 703 currently indexed Yoon text records. Its current Kim Young-sam text catalog contains 728 records, matching the 728 already in this CSV. Archive IDs newly collected from the site are numeric `artid` values; older numeric `division_number` values come from an earlier archive export and use a different ID space. The archive also has video and audio catalog categories without transcripts; those are excluded.
- **Presidential website** ([연설문](https://www.president.go.kr/speeches)): 103 Lee texts. IDs start `president_go_` and use the site's `BBS_CD`.
- **Government policy portal** ([연설문](https://www.korea.kr/briefing/speechList.do)): 18 additional Yoon texts and 285 additional Lee texts, with IDs beginning `korea_` followed by the portal `newsId`. Its 622 Yoon-labeled entries include 601 archived duplicates or text variants, one entry without usable text, and two consciously excluded variants of the same archived event. The Yoon additions are predominantly 2022–23 remarks and ministry briefings. Of 392 Lee-labeled entries from 2025-06-04 through the sync date, 98 substantially duplicated presidential-site texts, three lacked a usable text body, and six were third-person briefings, newspaper articles, or a joint communiqué rather than presidential speech text. Omitted Lee IDs are documented in `collect_korea_lee_speeches.py`; one body is available in full on the presidential website.

The Lee collection spans **2025-06-04 to 2026-10-02**. It includes all full texts currently available from those two public lists but does not establish that every spoken remark appears there. The Yoon collection spans **2022-05-10 to 2024-12-14**. Future Archive additions may extend it. Some portal entries in the speech list are first-person statements or remarks read by another official; filter by genre for analyses of spoken words only.

`source_manifest.csv` gives direct source URLs for all 1,109 Yoon and Lee records added in this update. The older export's numeric IDs are from a different Archive ID space, so direct links for those legacy rows cannot be reconstructed reliably from the CSV alone.

## Schema and quality

| Column | Meaning |
|---|---|
| `division_number` | Source record ID. Numeric for Archive rows; `president_go_` or `korea_` prefix for the other sources. All 9,883 values are unique. |
| `president` | Korean speaker name. |
| `title` | Source title, in Korean. |
| `date` | Source speech date. 9,555 full dates use `YYYY.MM.DD`; 82 have year only, 38 have year and month, and 208 legacy records lack a date. |
| `location` | Source location label. Blank on 406 Yoon and Lee portal/site rows because the newer sites do not provide the same field. |
| `kind` | Source speech category. The newer Yoon and Lee portal/site rows use `미분류` because those sites do not provide the Archive's category. |
| `speech_text` | Full Korean text as published on the source page. |

The Archive contains a few legacy duplicate texts and inconsistent location labels (`국외` and `해외` both mean abroad). Preserve source text and labels when running the collectors; normalize these in downstream analysis. Date parsing must handle all four levels of precision. Seven Lee presidential-site records were dated from an event date in the title because they were posted one to three days later. Government portal dates are its listing dates and can be one or more days after an event, especially for overseas remarks. Some Archive titles are generic or reused across distinct records; the Yoon collector therefore checks actual text before importing a portal entry.

## Updating

From the repository root, run the four collectors in order. Each checks source IDs, fetches full pages, and rewrites the CSV only after its batch succeeds. A fresh Archive crawl is the default; `--use-cache` is only for repeat development runs.

```bash
uv run --with requests --with beautifulsoup4 --with lxml data/president_speeches/update_speeches.py
uv run --with requests --with beautifulsoup4 --with lxml --with rapidfuzz data/president_speeches/collect_korea_yoon_speeches.py
uv run --with requests --with beautifulsoup4 --with lxml data/president_speeches/collect_lee_speeches.py
uv run --with requests --with beautifulsoup4 --with lxml --with rapidfuzz data/president_speeches/collect_korea_lee_speeches.py
python data/president_speeches/build_source_manifest.py
```

Run with `--dry-run` to check the available source records without writing the CSV. The portal collectors compare normalized full text within three days of the event date, keeping distinct remarks with similar titles.
