# North Korean Migrant Support Interviews

## Overview

This corpus contains short, open-text explanations written by South Korean survey respondents after evaluating multiple hypothetical **North Korean migrant** profiles. In the original experiment, respondents made judgments about whether they would **vote for**, **hire**, or **prefer to have as a neighbor** a specific North Korean migrant presented in a profile. After making each choice, respondents were asked to briefly explain *why* they selected or preferred the migrant they did.

This file contains those open-text, interview-like explanations. They represent how ordinary South Koreans articulate the reasoning behind social, political, and interpersonal judgments toward co-ethnic migrants. Whereas the experimental design quantifies how profile attributes shape support (e.g., education, occupation, age, political history, skill match, or time spent in South Korea), these open-text responses reveal the language, frames, and rationales respondents naturally draw upon.

The responses in this corpus can be read together as a measure of overall preferences or users can look at responses per 'integration type': political, economic, and social, corresponding to voting, hiring, and having as a neighbor.

**NOTE:** As argued in Denney & Green (2024; see article included in this folder), text-based explanations offer a complementary window into the mechanisms behind support for co-ethnic migrant integration. Users are **strongly advised** to see attributes used to define migrant profiles (pp. 2006-2007) from the article.

---

## Variables Included

### Core Metadata

| Variable | Description |
|----------|-------------|
| **respid** | Anonymous respondent identifier. Each ID corresponds to a unique survey participant. |
| **response_type** | The judgment task for which the explanation was written: **vote**, **hire**, or **neighbor**. |
| **response_text** | The respondent’s open-text explanation describing *why* they selected or preferred a given North Korean migrant profile. |
| **sex** | Respondent’s self-reported sex (*Male*, *Female*). |
| **age_cohorts** | Age group categories derived from age: *18–29*, *30–39*, *40–49*, *50–59*, *60+*. |
| **political_id3** | Three-category ideological identification derived from a 10-point ideology scale: **Conservative**, **Centrist** (includes “Don’t know”), **Progressive**. |
| **close_nkmigrants** | Respondent’s stated level of closeness or social distance toward North Korean migrants (e.g., *Very close*, *Somewhat distant*, *Neither close nor distant*). |

Note: The file contains **one row per respondent per task**, meaning each respondent can appear up to three times (vote, hire, neighbor).

---

## File Formats

- **nkmigrants_interviews.csv** — UTF-8 CSV file containing the interview responses. 

---

## Citation

Denney, Steven & Christopher Green. 2024. **“Public attitudes towards co-ethnic migrant integration: evidence from South Korea.”** *Journal of Ethnic and Migration Studies*, 50(8): 1998–2022. https://doi.org/10.1080/1369183X.2023.2286207
