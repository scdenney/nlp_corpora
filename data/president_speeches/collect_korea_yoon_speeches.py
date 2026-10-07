"""Add Yoon speeches absent from the Presidential Archive text catalog.

The government portal publishes presidential remarks alongside other
ministries' speeches. Its titles and posting dates sometimes differ from the
Archive, so comparison uses text within a three-day date window.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor
import csv
from datetime import datetime
import json
import math
import os
from pathlib import Path
import re
import time

from bs4 import BeautifulSoup
from rapidfuzz.fuzz import ratio
import requests

BASE = "https://www.korea.kr"
CSV_PATH = Path(__file__).with_name("president_speech_ko.csv")
START, END = "2022-05-10", "2025-04-04"
# These are rewritten or shorter variants of an archived speech at the same
# event, rather than another speech.
EXCLUDE_VARIANT_IDS = {"132034848", "132034727"}


def request(method, url, **kwargs):
    for attempt in range(4):
        try:
            response = requests.request(method, url, timeout=35, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException:
            if attempt == 3:
                raise
            time.sleep(2 ** attempt)


def list_page(number):
    soup = BeautifulSoup(request("POST", BASE + "/briefing/speechList.do",
        data={"pageIndex": str(number), "period": "direct", "startDate": START,
              "endDate": END}).content, "lxml")
    result = soup.select_one(".result")
    if result is None:
        raise RuntimeError(f"No result count on portal page {number}")
    total = int(re.search(r"총\s*([\d,]+)\s*건",
        result.get_text(" ", strip=True)).group(1).replace(",", ""))
    rows = []
    for tr in soup.select(".table_list tbody tr"):
        cells = tr.select("td")
        if len(cells) < 3 or cells[0].get_text(" ", strip=True) != "대통령":
            continue
        link = cells[1].find("a", href=re.compile("speechView"))
        if link is None:
            continue
        match = re.search(r"newsId=(\d+)", link["href"])
        if match:
            rows.append({"id": match.group(1), "date": cells[2].get_text(" ", strip=True),
                         "title": link.get_text(" ", strip=True)})
    return number, total, rows


def list_all():
    first = list_page(1)
    count = math.ceil(first[1] / 30)
    with ThreadPoolExecutor(max_workers=5) as pool:
        rest = list(pool.map(list_page, range(2, count + 1)))
    rows = [row for _, _, page in sorted([first, *rest]) for row in page]
    if len(rows) != len({row["id"] for row in rows}):
        raise RuntimeError("Duplicate government portal IDs")
    return rows


def detail(item, cache_dir=None):
    path = cache_dir / (item["id"] + ".json") if cache_dir else None
    if path and path.exists():
        body = json.loads(path.read_text(encoding="utf-8"))["body"]
    else:
        url = BASE + "/briefing/speechView.do?newsId=" + item["id"]
        soup = BeautifulSoup(request("GET", url).content, "lxml")
        element = soup.select_one(".view_cont")
        if element is None:
            raise RuntimeError(f"Missing speech body: {url}")
        body = re.sub(r"\n{3,}", "\n\n", element.get_text("\n", strip=True))
    return {"division_number": "korea_" + item["id"], "president": "윤석열",
            "title": item["title"], "date": item["date"], "location": "",
            "kind": "미분류", "speech_text": body}


def compact(value):
    return re.sub(r"[^\w가-힣]", "", value).lower()


def same_speech(candidate, others):
    day = datetime.strptime(candidate["date"], "%Y.%m.%d").date()
    body = compact(candidate["speech_text"])
    title = compact(candidate["title"])
    shingles = [body[i:i + 30] for i in range(0, len(body) - 29, 30)]
    for other in others:
        other_day = datetime.strptime(other["date"], "%Y.%m.%d").date()
        if abs((day - other_day).days) > 3:
            continue
        other_body = compact(other["speech_text"])
        body_ratio = ratio(body, other_body)
        coverage = sum(s in other_body for s in shingles) / len(shingles)
        title_ratio = ratio(title, compact(other["title"]))
        if body_ratio >= 85 or coverage >= 0.5 or (title_ratio >= 75 and body_ratio >= 60):
            return other["division_number"]
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--index-json", type=Path, help="Previously crawled portal index")
    parser.add_argument("--details-dir", type=Path, help="Previously crawled detail JSON files")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    index = json.loads(args.index_json.read_text(encoding="utf-8")) if args.index_json else list_all()
    with CSV_PATH.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fields = reader.fieldnames
        existing = list(reader)
    have = {row["division_number"] for row in existing}
    fresh = [item for item in index if "korea_" + item["id"] not in have
             and item["id"] not in EXCLUDE_VARIANT_IDS]
    with ThreadPoolExecutor(max_workers=6) as pool:
        fetched = list(pool.map(lambda item: detail(item, args.details_dir), fresh))
    archive = [row for row in existing if row["president"] == "윤석열"]
    added, duplicates, short = [], 0, []
    for row in fetched:
        if len(row["speech_text"]) < 50:
            short.append(row["division_number"])
            continue
        if same_speech(row, archive + added):
            duplicates += 1
        else:
            added.append(row)
    print(f"Portal presidential entries: {len(index)}; new texts: {len(added)}; "
          f"text duplicates/variants: {duplicates}; short/unusable: {short}")
    print("New IDs:", [row["division_number"] for row in added])
    if args.dry_run or not added:
        return
    output = CSV_PATH.with_suffix(".tmp")
    with output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(existing)
        writer.writerows(added)
    os.replace(output, CSV_PATH)


if __name__ == "__main__":
    main()
