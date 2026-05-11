# Korean Pseudohistory Primary Sources Corpus

![Sources](https://img.shields.io/badge/Sources-9%20texts-blue)
![Pages](https://img.shields.io/badge/Pages-764-green)
![Characters](https://img.shields.io/badge/Characters-1.07M-orange)
![Hangul](https://img.shields.io/badge/Hangul-527K-red)
![Hanja](https://img.shields.io/badge/Hanja-145K-purple)
![OCR Quality](https://img.shields.io/badge/OCR%20Quality-95.8%25%20clean-brightgreen)
![License](https://img.shields.io/badge/License-CC%20BY--NC%204.0-lightgrey)

## Overview

This corpus contains the **full OCR-extracted text** of 9 Korean primary source texts central to the study of pseudohistory (유사역사학) in Korea. These are the actual claimed historical documents themselves -- not secondary scholarship about them.

The texts include the core works cited by Korean pseudohistorians as evidence for an ancient Korean civilization predating established archaeological and historical evidence (환단고기, 규원사화, 단기고사, 부도지), a disputed Silla-era manuscript (화랑세기), a nationalist historiography appropriated by pseudohistorians (조선상고사), and two authentic historical texts included as reference points for genuine Joseon-era scholarly prose (동몽선습, 발해고).

All texts were OCR-extracted from Korean-language PDFs using **Qwen3-VL-32B-Instruct** (4-bit NF4 quantization) with rule-based post-processing. OCR quality is high: 95.8% of pages passed all quality checks with no issues detected.

---

## Documents

| doc_id | Title (Korean) | Title (English) | Author | Date | Pages | Chars | authenticity_status |
|--------|----------------|-----------------|--------|------|-------|-------|---------------------|
| DOC_0039 | 환단고기 | Record of Hwan and Dan | 계연수 (comp.) | Claimed 73–1520 CE; likely 20th c. | 151 | 194,342 | disputed_forgery |
| DOC_0040 | 규원사화 | Record of the Search for the Origin | 북애자 | Claimed 1675; likely 20th c. | 59 | 98,487 | disputed_forgery |
| DOC_0041 | 단기고사 원문 | Original Text of the Dangi Gosa | 대야발 | Claimed ancient; likely modern | 197 | 198,562 | disputed_forgery |
| DOC_0042 | 단기고사 | Dangi Gosa (alternate edition) | 대야발 | Claimed ancient; likely modern | 76 | 95,482 | disputed_forgery |
| DOC_0043 | 부도지 | Record of the Capital of the Buddha | 박제상 (attrib.) | Claimed 5th c.; published 1986 | 42 | 53,306 | disputed_forgery |
| DOC_0044 | 화랑세기 | Chronicle of the Hwarang | 김대문 (attrib.) | Claimed 8th c.; discovered 1989 | 26 | 22,488 | actively_debated |
| DOC_0046 | 조선상고사 | Ancient History of Korea | 신채호 | 1924–1931 | 149 | 338,659 | authentic_nationalist |
| DOC_0047 | 동몽선습 | Elementary Learning for Children | 박세무 | 1541 | 25 | 17,257 | authentic |
| DOC_0077 | 발해고 | Study of Balhae | 유득공 | 1784 | 39 | 51,876 | authentic |

---

## Variables Included

26 fields (JSONL) / 25 fields (Parquet, which omits the `pages` array) per document. Each row is one complete text.

| Variable | Type | Description |
|----------|------|-------------|
| **doc_id** | string | Unique document identifier (e.g., `DOC_0047`). |
| **title_ko** | string | Title in Korean. |
| **title_en** | string | Title in English (translated). |
| **title_romanized** | string | Romanized title (McCune-Reischauer or Revised Romanization). |
| **author_ko** | string | Author/compiler name in Korean with hanja where known. |
| **author_en** | string | Author name in English with life dates where known. |
| **author_romanized** | string | Romanized author name. |
| **attributed_date** | string | Date claimed by the text or tradition. |
| **composition_date** | string | Scholarly assessment of actual composition date. |
| **publication_date** | string | Date of the edition used in this corpus. |
| **language** | string | Language of the text (Korean, Mixed Korean/Classical Chinese). |
| **script** | string | Writing system (Hangul + Hanja, Hanja only, etc.). |
| **genre** | string | Genre classification (Historical chronicle, Cosmogonic narrative, etc.). |
| **authenticity_status** | string | Scholarly consensus on the text's authenticity. |
| **description_en** | string | English-language description of the text and its significance. |
| **description_ko** | string | Korean-language description. |
| **edition_notes** | string | Notes on the specific edition/copy used. |
| **source_pdf_provenance** | string | Provenance of the source PDF. |
| **page_count** | integer | Number of pages in the source PDF. |
| **total_chars** | integer | Total character count of extracted text. |
| **hangul_chars** | integer | Count of hangul characters (가–힣). |
| **hanja_chars** | integer | Count of hanja/Chinese characters (一–龥). |
| **ocr_quality_score** | float | Mean OCR quality score (0–1). |
| **ocr_model** | string | OCR model used (`Qwen3-VL-32B-Instruct (4-bit NF4)`). |
| **full_text** | string | Complete extracted text of the document. |
| **pages** | array | Per-page text array (JSONL only). |

---

## Character Composition

| Document | Total | Hangul | Hanja | Hangul % | Hanja % |
|----------|-------|--------|-------|----------|---------|
| 환단고기 | 194,342 | 108,064 | 11,739 | 55.6% | 6.0% |
| 규원사화 | 98,487 | 48,637 | 22,535 | 49.4% | 22.9% |
| 단기고사 원문 | 198,562 | 26,164 | 57,274 | 13.2% | 28.8% |
| 단기고사 | 95,482 | 56,640 | 6,668 | 59.3% | 7.0% |
| 부도지 | 53,306 | 30,779 | 4,711 | 57.7% | 8.8% |
| 화랑세기 | 22,488 | 13,941 | 2,098 | 62.0% | 9.3% |
| 조선상고사 | 338,659 | 210,418 | 21,636 | 62.1% | 6.4% |
| 동몽선습 | 17,257 | 8,999 | 3,923 | 52.1% | 22.7% |
| 발해고 | 51,876 | 23,767 | 14,313 | 45.8% | 27.6% |
| **Total** | **1,070,459** | **527,409** | **144,897** | **49.3%** | **13.5%** |

---

## Authenticity Classification

The texts fall into three categories:

**Disputed / widely considered forgeries (5 texts):** 환단고기, 규원사화, 단기고사 (both editions), and 부도지. These texts claim ancient authorship but are considered by mainstream Korean scholarship to be modern fabrications, most linked to Daejongism (대종교) and early 20th-century Korean nationalist movements.

**Actively debated (1 text):** 화랑세기. The manuscript was announced by Park Chang-hwa in 1989 and its authenticity remains an open question among Korean historians, with substantive arguments on both sides.

**Authentic texts included as reference (3 texts):** 조선상고사 (Sin Chae-ho's nationalist historiography, genuine authorship but appropriated by pseudohistorians), 동몽선습 (legitimate Joseon-era educational primer), and 발해고 (genuine 18th-century historical study). These provide baseline examples of authentic Korean historical prose for comparative analysis.

---

## File Formats

| File | Format | Size | Notes |
|------|--------|------|-------|
| `corpus.jsonl` | JSON Lines | 4.7 MB | One JSON object per document. Includes per-page text array. |
| `corpus.parquet` | Apache Parquet | 1.3 MB | Snappy compression. Document-level text only (no per-page array). |

**JSONL** is the recommended format for text analysis. Each line is a self-contained JSON document with all metadata and the `pages` array for page-level access.

**Parquet** is provided for fast loading in pandas/polars (`pd.read_parquet("corpus.parquet")`).

---

## OCR Pipeline

Texts were extracted from scanned and digital PDFs using a VLM-based OCR pipeline:

1. **Stage 1 (OCR):** PDF pages rendered at 200 DPI, processed with Qwen3-VL-32B-Instruct (4-bit NF4 quantization) on NVIDIA A40 GPU. ~75 seconds per page.
2. **Stage 2a (Diagnostics):** CPU-based regex quality scan flagging repetition artifacts, encoding issues, empty pages, and symbol density. 95.8% of pages passed all checks.
3. **Stage 2c (Rule fixes):** Deterministic cleanup (whitespace normalization, repetition collapse, control character removal, Unicode NFKC normalization). 98% of pages were unchanged.
4. **Stage 3 (Assembly):** Per-page markdown combined into full-document text files.

Pipeline code is available at: [`scdenney/psuedohistory_materials/ocr_pipeline/`](https://github.com/scdenney/psuedohistory_materials/tree/main/ocr_pipeline)

---

## Data Quality Notes

- OCR quality is high overall (mean quality score 0.993 across all pages), but some pages in scanned documents may contain minor character recognition errors, particularly for degraded hanja or mixed-script passages.
- 단기고사 원문 (DOC_0040) has the highest hanja density (28.8%) and 6 pages flagged for manual review, likely due to dense classical Chinese text on scanned pages.
- 동몽선습 (DOC_0042) has 1 page flagged for manual review (likely a blank or near-blank page in the source PDF).
- Per-page quality scores are available in the JSONL format for downstream filtering.
- The `total_chars`, `hangul_chars`, and `hanja_chars` values were recomputed after stripping LLM markdown fencing (` ```markdown ... ``` `) from all page texts; earlier pipeline versions may report slightly different counts.

---

## Sample Text

**환단고기 (Record of Hwan and Dan)** — Page 0 (title page):

> 환단고기(桓檀古記)
> (계언수 필사본 영인본)
>
> 안함로, 월동중, 이암, 범장, 이맥 편찬
> 계언수 합본, 이기 감수
> 김호영 해석
>
> 신교출판사

**발해고 (Study of Balhae)** — Opening passage:

> 渤海考序
>
> 余嘗西銜鴨綠道 邊 至遼陽 其間五六百里 大抵皆大山深谷 出狼子山 始見平原無際 混混茫茫
> 내가 일찍이 '암록도'를 지나 '애양'에 가 '오양'에 이르렀는데, 그 사이가 오욕맥리였다. 대개 큰산과 깊은 계곡인데 '남자산'에서 나온 것으로 처음으로 평평한 들들을 보니, 사이가 없이, 넓기만 하였다.

---

## License & Citation

This corpus is released under **CC BY-NC 4.0**. The underlying texts are either in the public domain or are reproductions of claimed historical documents circulating in public discourse.

If you use this corpus, please cite:

> Denney, Steven. (2026). Korean Pseudohistory Primary Sources Corpus. In *NLP Corpora for Korean Studies*. GitHub repository. https://github.com/scdenney/nlp_corpora

---

## Contact

Steven Denney, Leiden University (s.c.denney@hum.leidenuniv.nl)
