# Sync president_speech_ko.csv with the Presidential Archive speech database
# (대통령기록관 연설기록, https://www.pa.go.kr/research/contents/speech/).
#
# The archive keeps adding digitized records, so this script:
#   1. crawls the full speech catalog (list pages),
#   2. diffs against the local CSV on source ID and legacy title/date keys,
#   3. fetches detail pages for new records and appends them.
#
# Notes
# - Record IDs (artid) on the current site are a different ID space from the
#   legacy division_number values in older rows; rows added by this script use
#   the current artid. Older rows still need (president, date, title) matching.
# - New archive records retain distinct artids even when date and title match.
#
# Usage:  python update_speeches.py [--probe ARTID] [--dry-run]

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import os
import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

BASE = "https://www.pa.go.kr"
LIST = BASE + "/research/contents/speech/index.jsp"
HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) corpus-sync (academic)"}
CSV_PATH = Path(__file__).with_name("president_speech_ko.csv")
SLEEP = 0.25

csv.field_size_limit(10_000_000)


def norm_title(t):
    return re.sub(r"[\s\W]+", "", t)[:30]


def key(president, date, title):
    return (president.strip(), date.strip(), norm_title(title))


def crawl_list(session, cache=None):
    import json
    if cache is not None and cache.exists():
        with open(cache, encoding="utf-8") as f:
            rows = json.load(f)
        print(f"  using cached list ({len(rows)} rows); delete {cache} to recrawl", file=sys.stderr)
        return rows
    rows, page = [], 1
    while True:
        r = session.get(LIST, params={"pageIndex": page, "pageUnit": 100}, headers=HEADERS, timeout=30)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        page_rows = []
        for tr in soup.select("table tbody tr"):
            tds = tr.find_all("td")
            if len(tds) < 6:
                continue
            a = tds[1].find("a")
            if not a or "artid=" not in (a.get("href") or ""):
                continue
            artid = re.search(r"artid=(\d+)", a["href"]).group(1)
            catid = re.search(r"catid=([\w]+)", a["href"]).group(1)
            page_rows.append({
                "artid": artid, "catid": catid,
                "president": tds[1].get_text(strip=True),
                "kind": tds[3].get_text(strip=True),
                "title": tds[4].get_text(strip=True),
                "date": tds[5].get_text(strip=True),
            })
        if not page_rows:
            break
        rows.extend(page_rows)
        print(f"  list page {page}: {len(page_rows)} rows (total {len(rows)})", file=sys.stderr)
        page += 1
        time.sleep(SLEEP)
    import json
    if cache is not None:
        with open(cache, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False)
    return rows


def fetch_detail(session, catid, artid):
    r = session.get(LIST, params={"spMode": "view", "catid": catid, "artid": artid},
                    headers=HEADERS, timeout=30)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "lxml")
    meta = {}
    view = soup.select_one(".board-view") or soup
    for th in view.find_all("th"):
        td = th.find_next_sibling("td")
        if td:
            meta[th.get_text(strip=True)] = td.get_text(" ", strip=True)
    # speech body: the content container inside the view block
    body = ""
    for sel in (".board-view .cont", ".board-view .view-cont", ".board-view .content",
                ".board-view pre", ".bd_view_cont"):
        el = soup.select_one(sel)
        if el and len(el.get_text(strip=True)) > 50:
            body = el.get_text("\n", strip=False)
            break
    if not body:
        # fallback: longest text block within the view area
        cands = [d.get_text("\n") for d in view.find_all(["div", "td", "pre"])]
        body = max(cands, key=len) if cands else ""
    return meta, body.strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", help="fetch one artid and print parsed output")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--use-cache", action="store_true",
                    help="use or create speech_list_cache.json instead of recrawling")
    args = ap.parse_args()

    s = requests.Session()

    if args.probe:
        meta, body = fetch_detail(s, "c_pa02062", args.probe)
        print("META:", meta)
        print("BODY[:300]:", body[:300].replace("\n", " ⏎ "))
        print("BODY length:", len(body))
        return

    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        existing = list(reader)
    print(f"local rows: {len(existing)}")

    # rows with missing dates can't full-key match; index them for repair
    from collections import Counter, defaultdict
    nodate = defaultdict(list)
    for r in existing:
        if not r["date"].strip():
            nodate[(r["president"].strip(), norm_title(r["title"]))].append(r)

    cache = Path(__file__).with_name("speech_list_cache.json") if args.use_cache else None
    archive = crawl_list(s, cache)
    print(f"archive rows: {len(archive)}")
    # c_pa02062 = speech texts; c_pa02063 = video records; c_pa02064 = audio
    # records. Only the text catalog belongs in this corpus.
    archive = [a for a in archive if a["catid"] == "c_pa02062"]
    print(f"text-catalog (c_pa02062) rows: {len(archive)}")
    archive_ids = {a["artid"] for a in archive}
    legacy_keys = Counter(key(r["president"], r["date"], r["title"])
                          for r in existing if r["date"].strip()
                          and r["division_number"].strip() not in archive_ids)

    fresh, repairs, ambiguous = [], 0, 0
    existing_ids = {r["division_number"].strip() for r in existing}
    seen_ids = set()
    for a in archive:
        if a["artid"] in existing_ids or a["artid"] in seen_ids:
            continue
        seen_ids.add(a["artid"])
        k = key(a["president"], a["date"], a["title"])
        if legacy_keys[k]:
            legacy_keys[k] -= 1
            continue
        nk = (a["president"].strip(), norm_title(a["title"]))
        if nk in nodate:
            rows = nodate[nk]
            if len(rows) == 1 and a["date"].strip():
                rows[0]["date"] = a["date"].strip()   # repair missing date in place
                repairs += 1
                nodate.pop(nk)
            else:
                ambiguous += 1
            continue
        fresh.append(a)

    print(f"date repairs: {repairs} | ambiguous (left alone): {ambiguous} | new records: {len(fresh)}")
    print(Counter(r["president"] for r in fresh))

    if args.dry_run:
        return

    def fetch_one(r):
        for attempt in range(3):
            try:
                meta, body = fetch_detail(requests.Session(), r["catid"], r["artid"])
                if len(body) < 50:
                    raise ValueError(f"short speech body ({len(body)} chars)")
                break
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)
        return {
            "division_number": r["artid"],
            "president": meta.get("대통령", r["president"]),
            "title": r["title"],
            "date": meta.get("연설일자", r["date"]),
            "location": meta.get("연설장소", ""),
            "kind": meta.get("유형", r["kind"]),
            "speech_text": body,
        }

    fetched, errors = {}, []
    with ThreadPoolExecutor(max_workers=6) as pool:
        tasks = {pool.submit(fetch_one, r): r for r in fresh}
        for i, future in enumerate(as_completed(tasks), 1):
            record = tasks[future]
            try:
                fetched[record["artid"]] = future.result()
            except Exception as e:
                errors.append((record["artid"], str(e)))
            if i % 50 == 0 or i == len(fresh):
                print(f"  fetched {i}/{len(fresh)} ({len(errors)} failures)", file=sys.stderr)

    if errors:
        for artid, error in errors:
            print(f"  ! {artid} failed: {error}", file=sys.stderr)
        raise RuntimeError(f"Refusing partial CSV update: {len(errors)} detail fetches failed")
    added = [fetched[r["artid"]] for r in fresh]

    # rewrite: existing rows (with repaired dates) + appended new rows
    temp_path = CSV_PATH.with_suffix(".tmp")
    with open(temp_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in existing:
            w.writerow(row)
        for row in added:
            w.writerow(row)
    os.replace(temp_path, CSV_PATH)
    print(f"rewrote {CSV_PATH}: {len(existing)} existing ({repairs} dates repaired) + {len(added)} new")


if __name__ == "__main__":
    main()
