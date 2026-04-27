# OCR cleanup v2 report

- Input:  `/Users/scdenney/Documents/GitHub/resources/nlp_corpora/data/nikh/nikh_corpus.csv`
- Output: `/Users/scdenney/Documents/GitHub/resources/nlp_corpora/data/nikh/nikh_corpus.csv`
- Rows:   67
- Chars:  12,988,638 -> 11,287,661 (-1,700,977, 13.1%)

## Per-book deltas (top 20 by chars removed)

| book_id | before | after | removed | % |
|---|---:|---:|---:|---:|
| H-54(2,2016) | 958,329 | 610,392 | 347,937 | 36.3% |
| H-2(2,2006) | 582,470 | 420,440 | 162,030 | 27.8% |
| H-1(1,2006) | 388,925 | 270,784 | 118,141 | 30.4% |
| H-20(1,2001)1 | 305,489 | 197,468 | 108,021 | 35.4% |
| H-8(1,2007) | 464,772 | 364,374 | 100,398 | 21.6% |
| H-57(1,2016) | 610,206 | 513,608 | 96,598 | 15.8% |
| H-7(1,2007) | 481,301 | 386,135 | 95,166 | 19.8% |
| H-2(1,2002) | 518,581 | 425,523 | 93,058 | 17.9% |
| H-10(4,2007) | 545,971 | 460,172 | 85,799 | 15.7% |
| H-39(1,2002) | 341,494 | 264,498 | 76,996 | 22.5% |
| H-19(1,90)1 | 194,366 | 117,879 | 76,487 | 39.4% |
| H-9(5,2007) | 469,840 | 399,755 | 70,085 | 14.9% |
| H-5(1,2007) | 505,151 | 444,881 | 60,270 | 11.9% |
| H-6(1,2007) | 475,365 | 415,154 | 60,211 | 12.7% |
| H-18(1,90)1 | 231,194 | 171,999 | 59,195 | 25.6% |
| H-21(1,2001)1 | 175,162 | 137,250 | 37,912 | 21.6% |
| ta_h71 | 346,937 | 342,251 | 4,686 | 1.4% |
| ta_p81r | 152,053 | 149,248 | 2,805 | 1.8% |
| ta_p71r | 154,436 | 152,236 | 2,200 | 1.4% |
| ta_m71 | 229,973 | 227,780 | 2,193 | 1.0% |

## Step-level removal totals

| step | total chars removed |
|---|---:|
| strip_excessive_repetitions | 879,669 |
| strip_html_tags | 365,152 |
| strip_html_tables | 200,869 |
| strip_page_markers | 90,160 |
| normalize_whitespace | 78,771 |
| collapse_identical_lines | 70,988 |
| strip_standalone_short_hanja | 7,357 |
| strip_standalone_pagenum_lines | 4,107 |
| strip_pipeline_header | 1,816 |
| strip_gei_library_blocks | 1,132 |
| strip_empty_or_numeric_headers | 915 |
| strip_latex | 28 |
| strip_decorative_symbol_lines | 13 |
