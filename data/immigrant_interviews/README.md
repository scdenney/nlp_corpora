# Immigrant Support Interviews

## Overview

This dataset contains short, open-text explanations provided by South Korean survey respondents who participated in an experiment on immigration preferences. After evaluating multiple pairs of hypothetical immigrant profiles — each varying in attributes such as country of origin, language ability, profession, employment plans, and ethnicity — respondents were asked to briefly explain *why* they selected one immigrant over the other. The responses in this corpus are those written, interview-like justifications in the respondents' own words.

These responses reflect how ordinary people articulate the reasoning behind their judgments about immigrant admission and support for immigration. While the experiment quantifies the influence of specific immigrant attributes on support for admission, the open-text responses provide qualitative/interpretive data, reflecting how respondents describe their priorities, what cues they consider most important, and which concerns or values they emphasize when thinking about immigration.

Because respondents were not constrained by preset answer choices, this dataset reveals the vocabulary, frames, and rationales people naturally draw upon when justifying their preferences. Users can read these responses to explore themes such as perceived economic contribution, cultural compatibility, language expectations, humanitarian considerations, and stereotypes or anxieties associated with different countries of origin.

**NOTE:** These responses accompany the published article's main experimental findings (article is included in this folder). It is **highly advisable** but not absolutely necessary to look at how immigrant profiles were created (i.e., what attributes were used to define them); see p. 129 of the article for this information.

---

## Variables Included

6 columns, 1,008 rows. Each row is one respondent (one response per person).

| Variable | Type | Description |
|----------|------|-------------|
| **respid** | integer | Anonymous respondent identifier. 1,008 unique values (one row per person). |
| **text** | string | The respondent's open-text explanation describing why they chose one immigrant over another. Median length: 11 characters; range: 1–271 characters. **2 missing values.** |
| **sex** | string | Respondent's self-reported sex. 2 values (see below). |
| **age_cohort** | string | Respondent's age group category. 5 values (see below). |
| **political_id3** | string | Political orientation based on self-reported placement on a 10-point ideological scale, recoded into 3 categories (see below). |
| **college** | string | University education attainment indicator. 2 values (see below). |

---

## `sex` Distribution

| Value | Count |
|-------|-------|
| Male | 505 |
| Female | 503 |

---

## `age_cohort` Distribution

| Value | Count |
|-------|-------|
| 18-29 | 172 |
| 30-39 | 192 |
| 40-49 | 212 |
| 50-59 | 212 |
| 60+ | 220 |

---

## `political_id3` Distribution

| Value | Count | Note |
|-------|-------|------|
| Centrist | 477 | Includes respondents who answered "don't know" on the ideology scale |
| Progressive | 303 | |
| Conservative | 228 | |

---

## `college` Distribution

| Value | Count |
|-------|-------|
| Some college or more | 775 |
| No college | 233 |

---

## Sample Responses with Translations

| Korean Text | English Translation | Illustrative Theme |
|------------|---------------------|-------------------|
| 동포이니까 | "Because they're a compatriot" | Ethnic solidarity / co-ethnicity |
| 유창한 한국어 | "Fluent Korean" | Language ability |
| 없음 | "None" / "No reason" | Non-substantive response |
| 국적 우선시 함 | "Prioritized nationality" | National origin preference |
| 동포 | "Compatriot" | Co-ethnicity |
| 구직활동이 등록되어 있음 | "Job-seeking activity is registered" | Employment / economic contribution |
| 한국의 국익과 인권을 위해 이민을 검토하면 될 것 같음 | "I think immigration should be considered for Korea's national interest and human rights" | Policy-oriented reasoning |
| 한국에 필요한사람같아서 | "Seems like someone Korea needs" | Perceived economic contribution |
| 여자이므로 | "Because she's a woman" | Gender preference |
| 같은 민족이라서 | "Because they're the same ethnicity" | Co-ethnicity |
| 북한사람이 우리나라 말을 더 잘하기 때문에 | "Because North Koreans speak our language better" | Language ability / co-ethnicity |
| 확실히 근면 성실한 신뢰성이 있는자 | "Someone clearly diligent, sincere, and reliable" | Character / work ethic |
| 언어구사력 | "Language proficiency" | Language ability |

Responses range from single-word labels (없음, 동포) to full sentences. The median length of 11 characters indicates most responses are brief, phrase-level justifications rather than extended explanations.

---

## Data Quality Notes

- **2 rows** have missing `text` (0.2%). All other columns are fully populated.
- Responses vary widely in specificity and length. Some are effectively non-responses (e.g., 없음 = "none").

---

## File Formats

- **immigrant_interview.csv** — UTF-8 CSV file containing the interview responses.

---

## Citation

Denney, S., & Green, C. K. (2020). *Who should be admitted? Conjoint analysis of South Korean attitudes toward immigrants*. **Ethnicities, 21**(1), 120–145. https://doi.org/10.1177/1468796820916609
