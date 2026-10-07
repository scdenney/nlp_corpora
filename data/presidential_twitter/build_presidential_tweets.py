"""Combine the existing Moon dataset with Xcavator account captures."""

import csv
from datetime import datetime
import json
from pathlib import Path
import re

HERE = Path(__file__).parent
MOON = HERE.parent / "moon_twitter" / "moon_twitter.csv"
RAW = HERE / "raw"
OUTPUT = HERE / "presidential_tweets.csv"
FIELDS = ["president", "username", "tweet_id", "tweet_date", "tweet_time",
          "time_zone", "text", "link", "favorites", "retweets",
          "career_period", "source", "truncated", "captured_at"]
ACCOUNTS = {"sukyeol__yoon": "윤석열", "jaemyung_lee": "이재명"}


def moon_rows():
    with MOON.open(encoding="utf-8-sig", newline="") as file:
        for row in csv.DictReader(file):
            match = re.search(r"/status/(\d+)", row["link"])
            if not match:
                raise ValueError(f"Moon row has no post ID: {row['link']}")
            yield {"president": "문재인", "username": row["username"],
                   "tweet_id": match.group(1), "tweet_date": row["tweet_date"],
                   "tweet_time": row["tweet_time"], "time_zone": "unknown",
                   "text": "" if row["text"] == "NA" else row["text"],
                   "link": row["link"], "favorites": row["favorites"],
                   "retweets": row["retweets"], "career_period": row["period3"],
                   "source": "Moon Kaggle snapshot", "truncated": "",
                   "captured_at": ""}


def period(president, day):
    if president == "윤석열":
        return "presidency" if "2022-05-10" <= day <= "2025-04-04" else "other"
    return "presidency" if day >= "2025-06-04" else "pre_presidency"


def capture_rows():
    for username, president in ACCOUNTS.items():
        path = RAW / f"{username}.jsonl"
        if not path.exists():
            continue
        records = {}
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            record = json.loads(line)
            id_ = str(record["id"])
            if not re.fullmatch(r"\d{10,25}", id_):
                raise ValueError(f"Invalid post ID in {path}: {id_}")
            if record["username"].lower() != username:
                raise ValueError(f"Wrong account in {path}: {record['username']}")
            old = records.get(id_)
            if old is None or (old.get("truncated") and not record.get("truncated")) or (
                bool(old.get("truncated")) == bool(record.get("truncated"))
                and len(record["text"]) > len(old["text"])):
                records[id_] = record
        for record in records.values():
            posted = datetime.fromisoformat(record["date"].replace("Z", "+00:00"))
            day = posted.date().isoformat()
            yield {"president": president, "username": record["username"],
                   "tweet_id": record["id"], "tweet_date": day,
                   "tweet_time": posted.strftime("%H:%M:%S"), "time_zone": "UTC",
                   "text": re.sub(r"\s*Show more\s*$", "", record["text"])
                   if record.get("truncated") else record["text"],
                   "link": record["link"],
                   "favorites": "", "retweets": "",
                   "career_period": period(president, day),
                   "source": "Xcavator browser capture",
                   "truncated": str(bool(record.get("truncated"))).lower(),
                   "captured_at": record.get("captured_at", "")}


def main():
    rows = [*moon_rows(), *capture_rows()]
    ids = [(row["username"].lower(), row["tweet_id"]) for row in rows]
    if len(ids) != len(set(ids)):
        raise RuntimeError("Duplicate account/post IDs in combined dataset")
    with OUTPUT.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    from collections import Counter
    print(f"Wrote {len(rows)} posts to {OUTPUT}")
    print(Counter(row["president"] for row in rows))


if __name__ == "__main__":
    main()
