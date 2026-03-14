# Blue House National Petitions Corpus

## Overview

This corpus contains 18,077 citizen petitions submitted to the Moon Jae-in administration's Blue House (Cheong Wa Dae) National Petition system between **August 2017 and December 2018**. This is a 5% stratified sample of the full petition archive (~361,000 petitions).

The National Petition system was launched in August 2017 as a signature initiative of the Moon administration, allowing citizens to submit petitions on any topic. Petitions that gathered 200,000 or more signatures within 30 days received an official government response. The system became a major channel for Korean civic discourse, with petitions addressing political reform, human rights, gender equality, national security, education, and economic policy.

This data was sourced from the [akngs/petitions project](https://github.com/akngs/petitions). The petition data is released under the Korean Open Government License (KOGL) Type 1, which permits reuse, redistribution, and commercial use with attribution.

---

## Variables Included

8 columns, 18,077 rows. Each row is one petition.

| Variable | Type | Description |
|----------|------|-------------|
| **article_id** | integer | Unique petition identifier. Range: 58–468,651. |
| **start** | string | Petition start date in `YYYY-MM-DD` format. |
| **end** | string | Petition end date in `YYYY-MM-DD` format. |
| **category** | string | Petition category (Korean). 17 unique categories. |
| **title** | string | Petition title (Korean). Mean length ~23 characters. |
| **content** | string | Full petition text (Korean). Mean length ~514 characters; max ~112,825 characters. Escaped newlines (`\n`) represent line breaks in the original text. |
| **votes** | integer | Number of citizen signatures. Range: 0–296,330; median: 5. |
| **answered** | integer | Whether the petition received an official government response (0 = no, 1 = yes). Only 3 petitions in this sample were answered. |

---

## Categories

| Category (Korean) | English Translation | Count |
|--------------------|---------------------|-------|
| 정치개혁 | Political Reform | 2,845 |
| 기타 | Other | 2,189 |
| 인권/성평등 | Human Rights / Gender Equality | 1,611 |
| 안전/환경 | Safety / Environment | 1,350 |
| 외교/통일/국방 | Diplomacy / Unification / Defense | 1,262 |
| 교통/건축/국토 | Transportation / Architecture / Land | 1,262 |
| 육아/교육 | Childcare / Education | 1,219 |
| 보건복지 | Health / Welfare | 1,142 |
| 일자리 | Employment | 1,030 |
| 행정 | Administration | 944 |
| 문화/예술/체육/언론 | Culture / Arts / Sports / Media | 886 |
| 미래 | Future | 821 |
| 경제민주화 | Economic Democratization | 753 |
| 성장동력 | Growth Engine | 311 |
| 저출산/고령화대책 | Low Birthrate / Aging Policy | 192 |
| 반려동물 | Companion Animals | 177 |
| 농산어촌 | Agriculture / Fishery / Rural | 83 |

---

## Data Quality Notes

- This is a **5% sample** of the full corpus. The full dataset (~361,000 petitions, 517 MB) is available from the [original source](https://github.com/akngs/petitions).
- No missing values in any field.
- Content field uses escaped newlines (`\n` as literal two-character strings) to preserve CSV row structure. Convert to actual newlines if needed for display.
- Some petition content may include personal information (names, phone numbers, addresses) that petitioners voluntarily included. Exercise appropriate caution.

---

## License

Korean Open Government License (KOGL) Type 1. Attribution required. Commercial and non-commercial use permitted. Derivatives permitted. See [KOGL details](https://www.kogl.or.kr/info/license.do).

---

## File Formats

- **bluehouse_petitions.csv** -- UTF-8 CSV file containing the 5% sample corpus.
