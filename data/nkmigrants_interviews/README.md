# North Korean Migrant Support Interviews

## Overview

This corpus contains short, open-text explanations written by South Korean survey respondents after evaluating multiple hypothetical **North Korean migrant** profiles. In the original experiment, respondents made judgments about whether they would **vote for**, **hire**, or **prefer to have as a neighbor** a specific North Korean migrant presented in a profile. After making each choice, respondents were asked to briefly explain *why* they selected or preferred the migrant they did.

This file contains those open-text, interview-like explanations. They represent how ordinary South Koreans articulate the reasoning behind social, political, and interpersonal judgments toward co-ethnic migrants. Whereas the experimental design quantifies how profile attributes shape support (e.g., education, occupation, age, political history, skill match, or time spent in South Korea), these open-text responses reveal the language, frames, and rationales respondents naturally draw upon.

The responses in this corpus can be read together as a measure of overall preferences or users can look at responses per "integration type": political, economic, and social, corresponding to voting, hiring, and having as a neighbor.

**NOTE:** As argued in Denney & Green (2024; see article included in this folder), text-based explanations offer a complementary window into the mechanisms behind support for co-ethnic migrant integration. Users are **strongly advised** to see attributes used to define migrant profiles (pp. 2006–2007) from the article.

---

## Variables Included

7 columns, 6,027 rows. Each row is one respondent's explanation for one task. The file contains **one row per respondent per task**, meaning each respondent appears exactly 3 times (vote, hire, neighbor). There are **2,009 unique respondents**.

| Variable | Type | Description |
|----------|------|-------------|
| **respid** | integer | Anonymous respondent identifier. 2,009 unique values; each appears exactly 3 times. |
| **response_type** | string | The judgment task for which the explanation was written. 3 values: `vote`, `hire`, `neighbor` (2,009 each, perfectly balanced). See below. |
| **response_text** | string | The respondent's open-text explanation. Median length: 9 characters; range: 1–156 characters. **4 missing values.** |
| **sex** | string | Respondent's self-reported sex. 2 values: `Male` (3,087), `Female` (2,940). |
| **age_cohorts** | string | Age group categories. 4 values (see below). |
| **political_id3** | string | Three-category ideological identification. 3 values (see below). |
| **close_nkmigrants** | string | Respondent's stated level of closeness or social distance toward North Korean migrants. 5 values on an ordinal scale (see below). |

---

## `response_type` Values

| Value | Count | Integration Domain | Question Framing |
|-------|-------|-------------------|-----------------|
| `vote` | 2,009 | Political integration | "Would you vote for this person?" |
| `hire` | 2,009 | Economic integration | "Would you hire this person?" |
| `neighbor` | 2,009 | Social integration | "Would you want this person as a neighbor?" |

---

## `age_cohorts` Distribution

| Value | Count |
|-------|-------|
| 18-29 | 2,529 |
| 30-39 | 1,134 |
| 40-49 | 1,170 |
| 60+ | 1,194 |

Note: There is no `50-59` category in this dataset (unlike the immigrant interviews corpus, which has 5 age groups).

---

## `political_id3` Distribution

| Value | Count | Note |
|-------|-------|------|
| Centrist | 3,312 | Includes respondents who answered "don't know" on the ideology scale |
| Progressive | 1,380 | |
| Conservative | 1,335 | |

---

## `close_nkmigrants` Values (Ordinal Social Distance Scale)

| Value | Count | Direction |
|-------|-------|-----------|
| Very close | 108 | Most warm toward NK migrants |
| Somewhat close | 675 | |
| Neither close nor distant | 2,961 | Neutral (modal category) |
| Somewhat distant | 1,458 | |
| Very distant | 825 | Most cold toward NK migrants |

---

## Sample Responses with Translations by Task

### Vote (Political Integration)

| Korean Text | English Translation |
|------------|---------------------|
| 한국에 적응 | "Adapted to Korea" |
| 직업적으로 더 안정돼 보여서 | "Seemed more occupationally stable" |
| 체류기간 | "Length of stay" |
| 아는 지인이 많아서 | "Because they know many acquaintances" |
| 체류기간이 상대적으로 적은사람에게 이웃이 되어주고 싶어서 | "I wanted to be a neighbor to someone with a relatively short stay" |

### Hire (Economic Integration)

| Korean Text | English Translation |
|------------|---------------------|
| 연륜 | "Years of experience / maturity" |
| 직업도 있고 해서 | "Because they already have a job" |
| 한국 체류기간이 길어서 | "Because their time in Korea is long" |
| 자녀가 있고 체류기간도 있어서 | "Because they have children and time in Korea" |
| 정치를 하려면 기본적으로 어느정도 연령이 되어야할것같아서 | "I think you need to be a certain age to do politics" |

### Neighbor (Social Integration)

| Korean Text | English Translation |
|------------|---------------------|
| 한국에 적응 | "Adapted to Korea" |
| 직업적으로 좋아 보여서 | "Seemed good occupationally" |
| 체류기간, 한국인 동료 | "Length of stay, Korean colleagues" |
| 연령이 적합해서 | "Because the age is appropriate" |
| 아이가 없으면 일하는데 지장이 없을것같아서 | "Without children, I think there'd be no hindrance to working" |

Responses range from single-word labels (연륜, 체류기간) to short sentences. The median length of 9 characters indicates most are brief, phrase-level justifications.

---

## Data Quality Notes

- **4 rows** have missing `response_text` (0.07%). All other columns are fully populated.
- All 2,009 respondents have exactly 3 rows (one per task), so the dataset is perfectly balanced.
- Responses vary widely in specificity. Some are single-word references to a profile attribute; others are short explanations of reasoning.

---

## File Formats

- **nkmigrants_interviews.csv** — UTF-8 CSV file containing the interview responses.

---

## Citation

Denney, Steven & Christopher Green. 2024. **"Public attitudes towards co-ethnic migrant integration: evidence from South Korea."** *Journal of Ethnic and Migration Studies*, 50(8): 1998–2022. https://doi.org/10.1080/1369183X.2023.2286207
