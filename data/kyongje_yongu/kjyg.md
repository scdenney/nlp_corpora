# North Korean Economics Journal Corpus (Augmented)

## Overview

This corpus contains articles from a North Korean economics journal spanning **1987–2017**: the Kyŏngje Yŏngu (경제연구). It provides a rare, longitudinal window into how the Democratic People’s Republic of Korea (DPRK) discusses economic policy, ideology, and development priorities. The journal functions as a key medium through which the state articulates economic doctrine and signals its official line on planning, production, foreign trade, technocratic reforms, and the relationship between economic goals and the ideological foundations of the regime.

Across this 30-year period, North Korea experienced dramatic transformations: the collapse of the socialist trading bloc, the “Arduous March” famine years, partial marketization and institutional adjustment, nuclear development under tightening sanctions, and shifting strategies under three different leaders. The texts in this corpus reflect these turning points through changes in terminology, framing, priorities, slogans, and emphases on self-reliance, science and technology, productivity, agriculture, or defense.

The augmented dataset includes additional variables that can help users explore how economic discourse evolves across leaders, eras, and decades, and how the structure, length, or thematic emphasis of articles changes over time.

Read more about the journal at [38 North](https://www.38north.org/2025/05/in-memoriam-kyongje-yongu/).

---

## Variables Included

### Core Metadata

| Variable | Description |
|----------|-------------|
| **title** | Article title as published in the journal. |
| **author** | Author(s) listed for the article. |
| **year** | Publication year extracted from the issue code. |
| **issue** | Within-year issue number (e.g., 1–4), based on the original `year_issue` string. |
| **word_count** | Approximate token/word count of the article text. |
| **content** | Full article text written in Korean. May include editorial conventions and ideological terminology characteristic of DPRK publications. |

---

## Augmented Subgroup Variables

These variables were added to support structured comparisons across political, historical, and economic contexts.

| Variable | Description |
|----------|-------------|
| **leader_period** | Leadership period corresponding to publication year: `KIS` (Kim Il-sung, ≤1994), `KJI` (Kim Jong-il, 1995–2011), `KJU` (Kim Jong-un, ≥2012). |
| **economic_era** | Historically grounded economic period: `late_socialist_planning` (1987–1990), `collapse_arduous_march` (1991–1998), `marketization_adjustment` (1999–2011), `byungjin_sanctions` (2012–2017). |
| **decade** | Decade grouping (e.g., “1980s”, “1990s”, “2000s”, “2010s”) for coarse temporal analysis. |
| **log_word_count** | Natural log of article length (using log1p), useful for comparing article size. |

These grouping variables are meant to allow users to look at how economic rhetoric shifts during major political transitions or economic crises, and whether article content or structure varies systematically by leader or era.

---

## File Formats

- **kjyg.csv** — UTF-8 CSV file containing the complete corpus.  

