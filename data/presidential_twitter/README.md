# Presidential X posts

`presidential_tweets.csv` joins the existing [Moon Jae-in Twitter corpus](../moon_twitter) with Xcavator captures from [Yoon Suk-yeol](https://x.com/sukyeol__yoon) and [Lee Jae-myung](https://x.com/Jaemyung_Lee). As of **2026-10-07**, it contains **3,531 distinct posts**:

| President | Posts | Observed date range | Full text status |
|---|---:|---|---|
| Moon Jae-in | 3,148 | 2012-01-01–2020-06-15 | 20 source rows have missing text |
| Yoon Suk-yeol | 141 | 2022-05-19–2024-11-19 | All captured text complete |
| Lee Jae-myung | 242 | 2025-06-08–2026-10-07 | All captured texts complete |

The Yoon rows came from a scroll of the account's visible profile in signed-in Zen. The Lee rows came from the visible profile and `from:Jaemyung_Lee` searches in monthly windows from June 2025 through October 2026. We visited individual post pages to replace shortened Lee timeline previews with full text. The observed ranges describe **captured coverage**, not complete account histories. Search can omit posts; media-only posts are outside this text corpus. Lee's pre-presidency history and Moon's post-June-2020 posts have not been collected here.

The source account and post ID identify each row. `tweet_date` and `tweet_time` on the new captures are UTC, decoded from the X snowflake post ID when the page does not expose a machine-readable timestamp. The original Moon dates retain the source dataset's unknown time zone. New captures do not include engagement counts; empty `favorites` and `retweets` mean unavailable, not zero. `career_period` marks whether a Yoon or Lee post falls within the presidency; Moon's original period label is retained. The `truncated` column is `false` for all captured Yoon and Lee rows; future captures can use it to flag text awaiting a post-page visit.

`build_presidential_tweets.py` builds the combined CSV from `../moon_twitter/moon_twitter.csv` and JSONL files under `raw/`. The raw captures include appended improved versions of some post IDs; the builder selects the best version per ID. To rebuild after another capture:

```bash
python data/presidential_twitter/build_presidential_tweets.py
```

See [the Xcavator adapter](../../tools/xcavator) for collection and retry instructions. It reads visible pages in a signed-in browser and saves them locally, without X's official developer API.
