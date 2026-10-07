"""Collect Lee Jae-myung speech texts from the government policy portal.

The portal's 연설문 list is broader than the presidential site's selected
speeches. Records whose text substantially duplicates an existing Lee speech
are skipped; distinct speeches with the same date or title are retained.
"""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
from datetime import date, datetime
import math
import os
from pathlib import Path
import re
import time

from bs4 import BeautifulSoup
from rapidfuzz.fuzz import ratio
import requests

BASE = "https://www.korea.kr"
LIST = BASE + "/briefing/speechList.do"
CSV_PATH = Path(__file__).with_name("president_speech_ko.csv")
START_DATE = "2025-06-04"
PAGE_SIZE = 30
# The first is available in full on president.go.kr; the other two portal
# entries contain only an image or a 38-character slogan, not a speech text.
EXCLUDE_SOURCE_IDS = {"132039070", "132038387", "132038307"}
# Although listed under 연설문, these detail pages are a third-person press
# briefing, translated newspaper features, a bilateral communiqué, or (in
# 132037592) an unrelated report under the wrong title. They are not a speech
# or first-person presidential statement.
EXCLUDE_NON_SPEECH_IDS = {"132038849", "132038186", "132038045",
                          "132037871", "132037782", "132037592"}
EXCLUDED_IDS = EXCLUDE_SOURCE_IDS | EXCLUDE_NON_SPEECH_IDS


def request_with_retry(method, url, **kwargs):
    for attempt in range(3):
        try:
            response = requests.request(method, url, timeout=30, **kwargs)
            response.raise_for_status()
            return response
        except requests.RequestException:
            if attempt == 2:
                raise
            time.sleep(2 ** attempt)


def list_page(page):
    form = {"pageIndex": str(page), "period": "direct", "startDate": START_DATE,
            "endDate": date.today().isoformat()}
    soup = BeautifulSoup(request_with_retry("POST", LIST, data=form).content, "lxml")
    result = soup.select_one(".result")
    if result is None:
        raise RuntimeError(f"Missing result count on page {page}")
    total = int(re.search(r"총\s*([\d,]+)\s*건", result.get_text(" ", strip=True))
                .group(1).replace(",", ""))
    rows = []
    for tr in soup.select(".table_list tbody tr"):
        cells = tr.find_all("td")
        if len(cells) < 3 or cells[0].get_text(" ", strip=True) != "대통령":
            continue
        link = cells[1].find("a", href=re.compile(r"speechView\.do"))
        if not link:
            continue
        url = requests.compat.urljoin(BASE, link["href"])
        source_id = re.search(r"newsId=(\d+)", url)
        if not source_id:
            continue
        rows.append({"source_id": source_id.group(1), "url": url,
                     "title": link.get_text(" ", strip=True),
                     "date": cells[2].get_text(" ", strip=True)})
    return page, total, rows


def list_all():
    first = list_page(1)
    page_count = math.ceil(first[1] / PAGE_SIZE)
    with ThreadPoolExecutor(max_workers=6) as pool:
        rest = list(pool.map(list_page, range(2, page_count + 1)))
    pages = [first, *rest]
    rows = [record for _, _, batch in sorted(pages) for record in batch]
    if len({r["source_id"] for r in rows}) != len(rows):
        raise RuntimeError("Duplicate source IDs in portal index")
    return rows, first[1]


def fetch_one(item):
    soup = BeautifulSoup(request_with_retry("GET", item["url"]).content, "lxml")
    content = soup.select_one(".view_cont")
    if content is None:
        raise RuntimeError(f"Missing speech body: {item['url']}")
    body = re.sub(r"\n{3,}", "\n\n", content.get_text("\n", strip=True))
    if len(body) < 50:
        raise RuntimeError(f"Short speech body ({len(body)} chars): {item['url']}")
    return {"division_number": "korea_" + item["source_id"],
            "president": "이재명", "title": item["title"], "date": item["date"],
            "location": "", "kind": "미분류", "speech_text": body}


def compact(text):
    return re.sub(r"[^\w가-힣]", "", text).lower()


def duplicate(candidate, previous):
    body = compact(candidate["speech_text"])
    candidate_date = datetime.strptime(candidate["date"], "%Y.%m.%d").date()
    for row in previous:
        other_date = datetime.strptime(row["date"], "%Y.%m.%d").date()
        if abs((candidate_date - other_date).days) > 3:
            continue
        other = compact(row["speech_text"])
        length_ratio = min(len(body), len(other)) / max(len(body), len(other))
        if length_ratio > 0.85 and ratio(body, other) >= 95:
            return row["division_number"]
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    index, all_count = list_all()
    with CSV_PATH.open(encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fields = reader.fieldnames
        existing = list(reader)
    presidential_site = [r for r in existing
                         if r["division_number"].startswith("president_go_")]
    redundant_ids = {r["division_number"] for r in existing
                     if r["division_number"].startswith("korea_")
                     and duplicate(r, presidential_site)}
    excluded_existing = {"korea_" + source_id for source_id in EXCLUDED_IDS}
    removed_ids = redundant_ids | excluded_existing
    removed_count = sum(r["division_number"] in removed_ids for r in existing)
    if removed_ids:
        existing = [r for r in existing if r["division_number"] not in removed_ids]
    have_ids = {row["division_number"] for row in existing}
    fresh = [r for r in index if r["source_id"] not in EXCLUDED_IDS
             and "korea_" + r["source_id"] not in have_ids]
    print(f"Portal: {all_count} speeches across ministries; {len(index)} presidential; "
          f"{len(fresh)} unseen source IDs; {len(redundant_ids)} previously duplicated; "
          f"{len(EXCLUDE_SOURCE_IDS)} without usable full text; "
          f"{len(EXCLUDE_NON_SPEECH_IDS)} non-speech source pages")
    if args.dry_run or (not fresh and not removed_ids):
        return

    fetched, errors = {}, []
    with ThreadPoolExecutor(max_workers=6) as pool:
        tasks = {pool.submit(fetch_one, item): item for item in fresh}
        for i, future in enumerate(as_completed(tasks), 1):
            item = tasks[future]
            try:
                fetched[item["source_id"]] = future.result()
            except Exception as error:
                errors.append((item["source_id"], str(error)))
            if i % 50 == 0 or i == len(fresh):
                print(f"  fetched {i}/{len(fresh)} ({len(errors)} failures)", flush=True)
    if errors:
        raise RuntimeError(f"Refusing partial CSV update: {errors}")

    added = []
    matched = []
    lee_rows = [r for r in existing if r["president"] == "이재명"]
    for item in fresh:
        candidate = fetched[item["source_id"]]
        match = duplicate(candidate, lee_rows + added)
        if match:
            matched.append((item["source_id"], match))
        else:
            added.append(candidate)

    output = CSV_PATH.with_suffix(".tmp")
    with output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(existing)
        writer.writerows(added)
    os.replace(output, CSV_PATH)
    print(f"Appended {len(added)} Lee speeches; skipped {len(matched)} text duplicates; "
          f"removed {removed_count} existing duplicates or non-speech rows")


if __name__ == "__main__":
    main()
