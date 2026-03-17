# Korean Newspapers Twitter Corpus

## Overview

This corpus contains tweets from six major South Korean newspapers' Twitter accounts over a short but politically notable period in mid-2017. The data covers posts made between **2017-07-21** and **2017-08-11** (~3 weeks), during the early months of the Moon Jae-in presidency.

This period of coverage was a moment marked by active debate on inter-Korean relations, the THAAD missile-defense deployment, evolving U.S.–Korea diplomatic dynamics under the first Trump administration, domestic economic concerns surrounding job creation and labor reforms, and continued political fallout from the impeachment of former president Park Geun-hye. News outlets during this period were highly engaged in framing policy announcements, interpreting early approval-rating trends, and responding to rapid developments on the Korean Peninsula, making this a rich snapshot of contemporary political communication across ideologically diverse media organizations.

Each row represents a single tweet from one of the following outlets:

- **chosun** (조선일보, *Chosun Ilbo*)
- **dongamedia** (동아일보, *Dong-A Ilbo*)
- **joongangilbo** (중앙일보, *JoongAng Ilbo*)
- **hankyungmedia** (한국경제, *Korea Economic Daily*)
- **hanitweet** (한겨레, *Hankyoreh*)
- **kyunghyang** (경향신문, *Kyunghyang Shinmun*)

The corpus combines tweet text with basic engagement metrics and a coarse but accurate left–right classification at the outlet level added by the curator (Dr. Denney). This makes it suitable for comparative analysis of framing, issue emphasis, and tone across ideologically distinct media sources.

---

## Variables Included

7 columns, 2,748 rows. Each row is one tweet. No missing values in any column.

### Core Metadata

| Variable | Type | Description |
|----------|------|-------------|
| **paper_name** | string | Normalized identifier for the newspaper's Twitter account (e.g., `chosun`, `hanitweet`). 6 unique values. |
| **text** | string | Full tweet text as posted by the outlet. Typically includes a headline-style summary and one or more shortened `t.co` URLs. Written in Korean. |
| **favoriteCount** | integer | Number of likes at the time of data collection. Range: 0–2,416; median: 7; mean: 19. Heavily right-skewed. |
| **created** | string | Date and time the tweet was created (`YYYY-MM-DD HH:MM:SS`). Range: 2017-07-21 to 2017-08-11. |
| **id** | integer | Unique tweet identifier (64-bit numeric ID). |
| **retweetCount** | integer | Number of retweets at the time of data collection. Range: 0–12,622; median: 12; mean: 75. Heavily right-skewed. |
| **pol_id** | string | Coarse ideological label for the outlet: `left` or `right`. See mapping below. |

---

## Outlet Ideology Mapping (`pol_id`)

The `pol_id` variable provides a simple, outlet-level ideological classification:

### Left (1,497 tweets, ~54.5%)

| `paper_name` | Korean Name | English Name | Tweets | Ideological Position |
|--------------|-------------|--------------|--------|----------------------|
| `hanitweet` | 한겨레 | Hankyoreh | 771 | Progressive |
| `kyunghyang` | 경향신문 | Kyunghyang Shinmun | 726 | Progressive-leaning |

### Right (1,251 tweets, ~45.5%)

| `paper_name` | Korean Name | English Name | Tweets | Ideological Position |
|--------------|-------------|--------------|--------|----------------------|
| `joongangilbo` | 중앙일보 | JoongAng Ilbo | 440 | Center-right |
| `hankyungmedia` | 한국경제 | Korea Economic Daily | 331 | Conservative / business-oriented |
| `dongamedia` | 동아일보 | Dong-A Ilbo | 270 | Center-right |
| `chosun` | 조선일보 | Chosun Ilbo | 210 | Conservative |

Note: The dataset is somewhat skewed toward left-leaning outlets, which tweeted more frequently during this period.

---

## Sample Tweets

| Outlet | Korean Text | Translation |
|--------|------------|-------------|
| chosun | 구리~포천 고속도로 개통 한 달… 인근 지역 집값 들썩 | "One month since the Guri–Pocheon highway opened... nearby home prices stirring" |
| chosun | '석방' 조윤선 "오해를 풀어줘서 감사" | "'Released' Cho Yoon-sun: 'Thank you for clearing the misunderstanding'" |
| dongamedia | 개천에서 난 CEO, 성공의 원인도, 갑질 이유도 바로 이것 | "CEOs from humble origins: both the cause of success and reason for power abuse are this" |

---

## File Formats

- **korean_newspapers_twitter.csv** — UTF-8 CSV version compatible with Orange Data Mining.
