# High-School History Textbooks on Post-1945 Korea, 1954–2025

## Overview

This corpus holds **1,208 passages from 23 South Korean high-school history textbooks**, 1954–2025. Each passage comes from the part of its book that covers the years after liberation in 1945. It extends the [NIKH textbook corpus](../nikh) (1895–2016) with the privately written, state-approved books of 2007–2025, so that state and approved books can be compared on the same period.

The books fall into four eras:

- **authoritarian (1954–1987).** Five books: four state books (국정), one book for every school, written under the ministry; and the 1954 book, privately written and approved under the 1950s 검인정 system.
- **democratic-state (1995, 2002).** After democratization, the single state book continued through the 6th and 7th curricula.
- **2000s-certified (2007).** Six approved (검정) books of 한국근현대사 by six publishers. The 금성 book in particular drew conservative criticism.
- **2011+-certified (2011–2025).** Ten approved 한국사 books. The 2011 round reopened the left–right dispute over post-1945 history, which led to the short-lived state book of 2015–2017 (not included). The 2016 books are later editions under the 2009 revised curriculum; the 2025 books follow the 2022 revised curriculum.

A book's coverage ends at its own present: the 1954 book covers nine years, the 2025 books eighty. The corpus was first prepared for the BA3 Text as Data hackathon at Leiden University (November 2026).

**Not included:** the 지학사 editions of 2020 and 2025. The publisher supplied them for research use only, without redistribution.

## Files

| File | Description |
|:-----|:------------|
| `history_textbooks_1954_2025.csv` | The corpus: 1,208 rows × 12 columns, UTF-8 |
| `data_dictionary.csv` | Variable, type, description, example, and missingness for each column |
| `build/build_textbooks.py` | Cleaning and passage-splitting script, kept for provenance; it reads local sources that are not in this repository |

## Source and Selection

- **Sources:** the NIKH textbook corpus (국사편찬위원회, contents.history.go.kr) for the state books; the comparison set of the `kr-textbook-bias-2011` research project for the 2007 and 2016 books; that project's OCR of the 2011 and 2025 books.
- **Span:** each book is cut at the chapter that opens the post-1945 period (such as 대한민국의 수립 or 현대 사회) and runs to the end of its narrative. Chronologies, indexes, colophons, and end-of-unit review pages are excluded.
- **Sampling:** at most 60 passages per book, taken at even intervals across the span. Shorter books are kept whole. **These are excerpts, not full books.**
- **Unit:** a passage of whole sentences, mostly 400–700 characters (median about 430).

| Era | Books | Passages |
|:--|--:|--:|
| authoritarian | 5 | 128 |
| democratic-state | 2 | 120 |
| 2000s-certified | 6 | 360 |
| 2011+-certified | 10 | 600 |
| **Total** | **23** | **1,208** |

| Year | Publishers (passages) |
|:--|:--|
| 1954 | 정음사 (홍이섭) (3) |
| 1963, 1973, 1981 | 문교부 (18, 23, 31) |
| 1987, 1995 | 교육부 (53, 60) |
| 2002 | 교육인적자원부 (60) |
| 2007 | 금성출판사, 대한교과서, 두산, 법문사, 중앙교육진흥연구소, 천재교육 (60 each) |
| 2011 | 미래엔, 법문사, 비상교육, 삼화출판사, 지학사, 천재교육 (60 each) |
| 2016 | 금성출판사, 지학사 (60 each) |
| 2025 | 비상교육, 씨마스 (60 each) |

## Variables

See `data_dictionary.csv`. The main ones: `text`; `era`; `year`; `publisher`; `curriculum`; `authorization` (국정, 검정, or 검인정); `book_id` and `title`; `passage_no`; and `share_of_span`, the passage's position in the book's post-1945 part from 0 (1945) to 1 (the end of the book).

## Cleaning

Layout and OCR debris was removed before the text was split into passages (`clean()` and `passages()` in the build script):

- table rows, chart values, timeline rows, captions marked ↑ ▲ ▼, quiz lines, URLs, and markdown marks;
- running heads with page numbers, box and exercise labels (자료 3, 탐구 활동, 주제 열기), bullets, arrows, and circled numbers;
- margin line numbers in the OCR books, and exercise prompts ending in 보자, 봅시다, or 시오;
- words split by a line break or stray space were rejoined where the Kiwi tokenizer judged them one word (`요 청하였다` → `요청하였다`). Two whole words written apart (`대한 민국`) were left as printed, and the typed state books were not respaced;
- look-alike dots normalized to `·`, and two recurring misreadings corrected (`반동 회의` → `반둥 회의`, `이기봉` → `이기붕`).

The text is not tokenized, normalized, or filtered for stopwords; hanja and each book's own spacing are kept.

## Known Limitations

- **OCR noise.** Some errors remain: spacing Kiwi left alone (`선포 하고`), single misread syllables (`거부장적` for 가부장적), and words cut by a sidebar.
- **Older spellings.** Older books use the spacing and transliterations of their time (`대한 민국`, `유우엔`, `마오 쩌둥`), which show up as separate tokens.
- **Boxes and exercises.** Unmarked captions, sidebars, glossary entries, source quotations, and study questions remain, most of all in the 2007 and 2016 books.
- **Unbalanced eras.** The pre-1995 state books say much less about post-1945 history (3 passages in 1954, 53 in 1987). Compare shares or means, not counts.
- **Different courses.** The 2007 books are 한국근현대사 (modern history only); the others are general 국사 or 한국사.
- **Sampling.** A topic covered in only a few pages of a long book may be missed.

## License and Attribution

The publishers hold copyright in the 2007–2025 books. This file contains excerpts (at most 60 passages per book) for non-commercial research and teaching under the repository's CC BY-NC 4.0 terms. Do not use it to reconstruct the books, and quote only short passages with book and year.

Suggested attribution: *High-school history textbooks on post-1945 Korea, 1954–2025, prepared by Steven Denney, NLP Corpora for Korean Studies (2026).*
