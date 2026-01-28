# President Moon Jae-in Twitter Corpus

## Overview

This corpus contains metadata and text fields from the official Twitter account of South Korean President **Moon Jae-in**, covering the period **2012-01-01 through 2020-06-16**. It includes tweets posted before, during, and after Moon’s presidency, offering a timeline for examining changes in communication patterns, issue emphasis, and tone across political contexts.

Each tweet is accompanied by core platform metadata (e.g., creation time, retweet count, favorite count, unique tweet ID), along with additional subgroup variables designed to facilitate analysis. These additional variables identify the political period in which each tweet was posted, extract the year for temporal analysis, and categorize tweets into analytically meaningful periods surrounding the presidency.

## Variables Included

### Core Metadata

| Variable        | Description |
|----------------|-------------|
| **username**   | Twitter handle associated with the account (`moonriver365`). |
| **tweet_date** | Calendar date of the tweet in `YYYY-MM-DD` format. |
| **tweet_time** | Time of day the tweet was posted (`HH:MM:SS`). |
| **text**       | Full tweet text. May include URLs, hashtags, emojis, or line breaks. |
| **favorites**  | Number of likes at the time of data collection. |
| **retweets**   | Number of retweets at the time of data collection. |
| **link**       | Full URL linking to the original tweet on Twitter/X. |

---

## Augmented Subgroup Variables

These variables were added during to support (additional) analysis:

| Variable        | Description |
|----------------|-------------|
| **tweet_year** | Four-digit year extracted from `tweet_date`. Useful for grouping and plotting tweets over time. |
| **period3**    | Three-category political period indicator based on tweet date: `pre_presidency` (before 2016-12-01), `transition` (2016-12-01 to 2017-05-09), and `presidency` (2017-05-10 onward). |

---

## File Formats

- **moon_twitter.csv** — UTF-8 CSV version compatible with Orange Data Mining.  

---

## Source

The original dataset was obtained from:

**https://www.kaggle.com/datasets/kihunkim/south-korea-president-moon-moon-jaein-twitter/data**
