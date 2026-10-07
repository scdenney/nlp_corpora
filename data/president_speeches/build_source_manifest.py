"""Build direct source links for the records added in the 2026 update."""

import csv
import os
from pathlib import Path

HERE = Path(__file__).parent
CORPUS = HERE / "president_speech_ko.csv"
OUTPUT = HERE / "source_manifest.csv"
FIELDS = ["division_number", "president", "source", "source_url"]


def source(row):
    identifier = row["division_number"]
    if identifier.startswith("president_go_"):
        key = identifier.removeprefix("president_go_")
        return "president.go.kr", f"https://www.president.go.kr/speeches/{key}"
    if identifier.startswith("korea_"):
        key = identifier.removeprefix("korea_")
        return "korea.kr", f"https://www.korea.kr/briefing/speechView.do?newsId={key}"
    if row["president"] == "윤석열":
        return "Presidential Archive", (
            "https://www.pa.go.kr/research/contents/speech/index.jsp"
            f"?spMode=view&catid=c_pa02062&artid={identifier}"
        )
    return None


def main():
    with CORPUS.open(encoding="utf-8", newline="") as file:
        records = list(csv.DictReader(file))
    rows = []
    for row in records:
        value = source(row)
        if value:
            rows.append({"division_number": row["division_number"],
                         "president": row["president"],
                         "source": value[0], "source_url": value[1]})
    if len(rows) != len({r["division_number"] for r in rows}):
        raise RuntimeError("Source manifest has duplicate IDs")
    temp = OUTPUT.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temp, OUTPUT)
    print(f"Wrote {len(rows)} source links to {OUTPUT}")


if __name__ == "__main__":
    main()
