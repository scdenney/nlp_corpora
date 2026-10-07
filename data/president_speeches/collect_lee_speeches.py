"""Append Lee Jae-myung speeches from the presidential website.

The site's list endpoint supplies metadata and a short preview; full text is
read from each public detail page. Re-running this script adds only new IDs.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from datetime import datetime, timedelta
import os
from pathlib import Path
import re
import time

import requests
from bs4 import BeautifulSoup

BASE = "https://www.president.go.kr"
INDEX = BASE + "/ajaxf/frBoard/bbsViewGalleryList.do"
CSV_PATH = Path(__file__).with_name("president_speech_ko.csv")
FORM = {
    "pageNo": "1", "pagePerCnt": "500", "MENU_CD": "puvIc0NF",
    "CONTENTS_CD": "vqNUjDNc", "pSiteNo": "2", "pBoardSeq": "12",
    "SHORT_URL": "speeches", "sSearchGbn": "", "sSearchTxt": "",
}


def speech_date(item):
    """Use the event date in a title when publication followed by 1–3 days."""
    published = datetime.strptime(item["WRITE_DATE"], "%Y.%m.%d").date()
    match = re.match(r"^(\d{1,2})/(\d{1,2})(?:\([^)]*\))?", item["SUBJECT"])
    if not match:
        return item["WRITE_DATE"]
    month, day = map(int, match.groups())
    for year in (published.year, published.year - 1):
        try:
            event = published.replace(year=year, month=month, day=day)
        except ValueError:
            continue
        if timedelta(0) <= published - event <= timedelta(days=3):
            return event.strftime("%Y.%m.%d")
    return item["WRITE_DATE"]


def get_with_retry(url, *, method="get", **kwargs):
    for attempt in range(3):
        try:
            response = requests.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def list_speeches():
    data = get_with_retry(INDEX, method="post", data=FORM).json()["data"]
    records = data["list"]
    if len(records) != int(data["totalRecordCount"]):
        raise RuntimeError("Index was truncated; adjust pagePerCnt or paginate")
    if len({r["BBS_CD"] for r in records}) != len(records):
        raise RuntimeError("Duplicate source IDs in index")
    return records


def fetch_speech(item):
    source_id = item["BBS_CD"]
    url = f"{BASE}/speeches/{source_id}"
    soup = BeautifulSoup(get_with_retry(url).content, "lxml")
    contents = soup.select(".view_txt .txtArea")
    if not contents:
        raise RuntimeError(f"No full-text element at {url}")
    body = "\n\n".join(part.get_text("\n", strip=True) for part in contents
                       if part.get_text(" ", strip=True))
    body = re.sub(r"\n{3,}", "\n\n", body)
    if len(body) < 50:
        raise RuntimeError(f"Short speech body at {url}: {len(body)} chars")
    return {
        "division_number": f"president_go_{source_id}",
        "president": "이재명",
        "title": item["SUBJECT"].strip(),
        "date": speech_date(item),
        "location": "",
        "kind": "미분류",
        "speech_text": body,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    index = list_speeches()
    with CSV_PATH.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fields = reader.fieldnames
        existing = list(reader)
    source_dates = {f"president_go_{r['BBS_CD']}": speech_date(r) for r in index}
    repairs = 0
    for row in existing:
        corrected = source_dates.get(row["division_number"])
        if corrected and row["date"] != corrected:
            row["date"] = corrected
            repairs += 1
    have = {row["division_number"] for row in existing}
    fresh = [r for r in index if f"president_go_{r['BBS_CD']}" not in have]
    print(f"Presidential site: {len(index)} speeches; {len(fresh)} new; {repairs} dates corrected")
    if args.dry_run or (not fresh and not repairs):
        return

    fetched = {}
    errors = []
    if fresh:
        with ThreadPoolExecutor(max_workers=4) as pool:
            tasks = {pool.submit(fetch_speech, item): item for item in fresh}
            for i, future in enumerate(as_completed(tasks), 1):
                item = tasks[future]
                try:
                    fetched[item["BBS_CD"]] = future.result()
                except Exception as error:
                    errors.append((item["BBS_CD"], str(error)))
                if i % 25 == 0 or i == len(fresh):
                    print(f"  fetched {i}/{len(fresh)} ({len(errors)} failures)")
    if errors:
        raise RuntimeError(f"Refusing partial CSV update: {errors}")

    output = CSV_PATH.with_suffix(".tmp")
    with output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(existing)
        writer.writerows(fetched[r["BBS_CD"]] for r in fresh)
    os.replace(output, CSV_PATH)
    print(f"Appended {len(fresh)} Lee speeches; corrected {repairs} dates in {CSV_PATH}")


if __name__ == "__main__":
    main()
