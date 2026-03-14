# Rodong Sinmun English-Language Corpus

## Overview

This corpus contains 9,797 English-language articles from North Korea's *Rodong Sinmun* (로동신문, "Workers' Daily"), the official newspaper of the Central Committee of the Workers' Party of Korea. The articles span **January 2018 to June 2022**, a period covering the Trump-Kim diplomatic summits, the collapse of the Hanoi talks, COVID-era isolation, and intensified missile testing.

The *Rodong Sinmun* is the most authoritative daily newspaper in the DPRK, carrying editorials, policy pronouncements, propaganda, and state-approved reporting. The English-language edition provides access to how the DPRK presents itself to an international audience.

This data was sourced from the [NKLM project](https://github.com/cohml/nklm) (MIT License).

---

## Variables Included

4 columns, 9,797 rows. Each row is one article.

| Variable | Type | Description |
|----------|------|-------------|
| **date** | string | Publication date in `YYYY-MM-DD` format. Range: 2018-01-02 to 2022-06-03. |
| **title** | string | Article headline. Mean length ~54 characters. |
| **body** | string | Full article text in English. Mean length ~262 words; range 2–7,087 words. |
| **url** | string | Original URL on the Rodong Sinmun English-language website (`rodong.rep.kp/en/`). |

---

## Temporal Distribution

| Year | Articles |
|------|----------|
| 2018 | 2,628 |
| 2019 | 2,466 |
| 2020 | 2,136 |
| 2021 | 1,649 |
| 2022 | 918 |

The declining article count reflects reduced output from the English-language edition over time, particularly after the onset of COVID-19 border closures in early 2020.

---

## Cleaning Notes

The following cleaning was applied to the original data:

- **Title field repair**: ~20% of rows in the original data had body text erroneously concatenated into the title field. These were programmatically repaired by detecting where the body text began within the title string and extracting only the true headline.
- **Whitespace normalization**: Double spaces in article bodies were collapsed to single spaces.
- **Dropped rows**: 3 rows with embedded newlines and duplicated paragraph content (scraping artifacts) were removed. Original count: 9,800; cleaned count: 9,797.
- **Duplicate titles**: 836 titles appear more than once (e.g., "Editorial" appears 54 times). These are genuinely different articles with the same headline; all URLs are unique.

---

## License

MIT License. See the [original repository](https://github.com/cohml/nklm) for details.

---

## File Formats

- **rodong_sinmun_en.csv** -- UTF-8 CSV file containing the complete cleaned corpus.
