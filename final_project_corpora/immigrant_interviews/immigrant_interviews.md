# Immigrant Support Interviews

## Overview

This dataset contains short, open-text explanations provided by South Korean survey respondents who participated in an experiment on immigration preferences. After evaluating multiple pairs of hypothetical immigrant profiles—each varying in attributes such as country of origin, language ability, profession, employment plans, and ethnicity, respondents were asked to briefly explain *why* they selected one immigrant over the other. The responses in this corpus are those written, interview-like justifications -- in the respondents’ own words.

These responeses reflect how ordinary people articulate the reasoning behind their judgments about immigrant admission and support for immigration. While the experiment quantifies the influence of specific immigrant attributes on support for admission, the open-text responses provide qualitative/interpretive data, reflecting how respondents describe their priorities, what cues they consider most important, and which concerns or values they emphasize when thinking about immigration.

Because respondents were not constrained by preset answer choices, this dataset reveals the vocabulary, frames, and rationales people naturally draw upon when justifying their preferences. Users can read these responses to explore themes such as perceived economic contribution, cultural compatibility, language expectations, humanitarian considerations, and stereotypes or anxieties associated with different countries of origin. 

**NOTE:** These responses accompany the published article’s main experimental findings (article is included in this folder). It is **highly advisible** but not absolutely necessary to look at how immigrant profiles were created (i.e., what attributes were used to define them); see p. 129 of the article for this information.

---

## Variables Included

### Core Metadata

| Variable | Description |
|----------|-------------|
| **respid** | Anonymous respondent identifier. Each ID corresponds to a unique survey participant. |
| **text** | The respondent’s open-text explanation describing why they chose one immigrant over another. This is the main qualitative content of the dataset. |
| **sex** | Respondent’s self-reported sex (*Male*, *Female*). |
| **age_cohort** | Respondent’s age group category (*18-29*, *30-39*, *40-49*, *50-59*, *60+*). |
| **political_id3** | Political orientation based on self-reported placement on a 10-point ideological scale. Values are recoded into *Conservative*, *Centrist* (includes those unsure), and *Progressive*. |
| **college** | University education attainment indicator (*No college*, *Some college or more*). |

These variables provide basic demographic and attitudinal context, enabling analysis of how different types of respondent subgroups articulate support for immigrant admission and immigration generally.

---

## File Formats

- **immigrant_interview.csv** — UTF-8 CSV file containing the interview responses.  

---

## Citation

Denney, S., & Green, C. K. (2020). *Who should be admitted? Conjoint analysis of South Korean attitudes toward immigrants*. **Ethnicities, 21**(1), 120–145. https://doi.org/10.1177/1468796820916609
