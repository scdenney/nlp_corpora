# Korean Newspapers Twitter Corpus

## Overview

This corpus contains tweets from six major South Korean newspapers’ Twitter accounts over a short but politically notable period in mid-2017. The data covers posts made between **2017-07-21** and **2017-08-11**, during the early months of the Moon Jae-in presidency. 

Thperiod of coverage was a moment marked by active debate on inter-Korean relations, the THAAD missile-defense deployment, evolving U.S.–Korea diplomatic dynamics under the first Trump administration, domestic economic concerns surrounding job creation and labor reforms, and continued political fallout from the impeachment of former president Park Geun-hye. News outlets during this period were highly engaged in framing policy announcements, interpreting early approval-rating trends, and responding to rapid developments on the Korean Peninsula, making this a rich snapshot of contemporary political communication across ideologically diverse media organizations.

Each row represents a single tweet from one of the following outlets:

- **chosun** (조선일보)  
- **dongamedia** (동아일보)  
- **joongangilbo** (중앙일보)  
- **hankyungmedia** (한국경제)  
- **hanitweet** (한겨레)  
- **kyunghyang** (경향신문)  

The corpus combines tweet text with basic engagement metrics and a coarse but accurate left–right classification at the outlet level added by the curator (Dr. Denney). This makes it suitable for comparative analysis of framing, issue emphasis, and tone across ideologically distinct media sources.

---

## Variables Included

### Core Metadata

| Variable          | Description |
|------------------|-------------|
| **paper_name**   | Normalized identifier for the newspaper’s Twitter account (e.g., `chosun`, `hanitweet`). |
| **text**         | Full tweet text as posted by the outlet, usually including a headline-style summary and one or more URLs. |
| **favoriteCount**| Number of likes at the time of data collection. |
| **created**      | Date and time the tweet was created (`YYYY-MM-DD HH:MM:SS`). |
| **id**           | Unique tweet identifier (64-bit numeric ID). |
| **retweetCount** | Number of retweets at the time of data collection. |
| **pol_id**       | Coarse ideological label for the outlet: `left` or `right`. See mapping below. |

---

## Outlet Ideology Mapping (`pol_id`)

The `pol_id` variable provides a simple, outlet-level ideological classification:

- **left**  
  - `hanitweet` (한겨레)  
  - `kyunghyang` (경향신문)  

- **right/center-right**  
  - `chosun` (조선일보)  
  - `dongamedia` (동아일보)  
  - `joongangilbo` (중앙일보)  
  - `hankyungmedia` (한국경제)  

---

## File Formats

- **korean_newspapers_twitter.csv** — UTF-8 CSV version compatible with Orange Data Mining.  
