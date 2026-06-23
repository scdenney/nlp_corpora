# -*- coding: utf-8 -*-
"""Extend the 경제연구 (Kyŏngje Yŏngu) corpus from 1987–2017 to 1987–2020.

Inputs
------
  kjyg.csv                       the published 1987..2017-3 baseline (this folder)
  <SOURCE_DIR>/2017/4/*.docx     2017-4 articles (one per file)
  <SOURCE_DIR>/2018/{1..4}/*.docx
  <SOURCE_DIR>/2019/KPJ_*.pdf    full-issue PDFs (text layer), 2019-1/2/3
  <SOURCE_DIR>/2020/경제연구 2020-*.pdf   full-issue PDFs, 2020-1/2/4

The raw docx/PDF sources are held in the research project, not in this public
repository (mirroring the original corpus, which shipped processed text only).
Point SOURCE_DIR at them via argv[1] or the KJYG_SOURCE environment variable.

Method
------
  - docx: title+author from filename and the 저자/출처 metadata line; body text
          minus the title echo and metadata line.
  - pdf : segment by 16pt centered titles; authors matched from the TOC (차례) by
          printed page number; DPRK leader names (rendered in a Private-Use-Area
          honorific font whose codepoints vary per file) decoded via per-file
          epithet-context derivation (위대한 수령→김일성, 위대한 령도자→김정일,
          경애하는 최고령도자→김정은).

Data notes
----------
  - '경제연구 2020-3.pdf' is a MISFILED issue of 력사과학 (Historical Science,
    루계 255) and is rejected by the journal-identity guard.
  - Source gaps (absent from the supplied materials): 2019-4 and the genuine
    2020-3 (루계 188). 1995-4 was already absent in the baseline.
  - Existing 2017-1/2/3 are kept from the baseline; only 2017-4 onward is added.

Usage
-----
  python build_kjyg_2017_2020.py [SOURCE_DIR]
"""
import os, re, sys, json
import pandas as pd
import kjyg_extract as E

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_DIR = (sys.argv[1] if len(sys.argv) > 1
              else os.environ.get("KJYG_SOURCE",
                   os.path.expanduser("~/Documents/github/research/projects/kjyg/data/raw/For the love of 경제연구")))
BASELINE = os.path.join(HERE, "kjyg.csv")
COLS = ["title", "author", "year_issue", "word_count", "file_path", "content", "source"]
despace = lambda s: re.sub(r"\s+", "", str(s)) if pd.notna(s) else ""


def main():
    ex = pd.read_csv(BASELINE)
    if "source" not in ex.columns:
        ex["source"] = "original_json"
    baseline_max = sorted(ex.year_issue.unique())[-1]
    print(f"baseline: {len(ex)} rows, ..{baseline_max}")

    # docx 2017-4 + 2018 (2017-1/2/3 already in baseline)
    yimap = {"2017/4": "2017-4"}
    yimap.update({f"2018/{i}": f"2018-{i}" for i in (1, 2, 3, 4)})
    docx = pd.DataFrame(E.extract_docx_dir(SOURCE_DIR, yimap))
    docx = docx.rename(columns={"source_type": "source"}).assign(source="docx")
    print(f"docx: {len(docx)} | {dict(docx.year_issue.value_counts().sort_index())}")

    # pdf 2019-1/2/3 + 2020-1/2/4 (journal-guarded; 2020-3 = 력사과학 is skipped)
    pdfmap = {
        f"{SOURCE_DIR}/2019/KPJ_69584.pdf": "2019-1",
        f"{SOURCE_DIR}/2019/KPJ_69627.pdf": "2019-2",
        f"{SOURCE_DIR}/2019/KPJ_70923.pdf": "2019-3",
        f"{SOURCE_DIR}/2020/경제연구 2020-1.pdf": "2020-1",
        f"{SOURCE_DIR}/2020/경제연구 2020-2.pdf": "2020-2",
        f"{SOURCE_DIR}/2020/경제연구 2020-3.pdf": "2020-3",
        f"{SOURCE_DIR}/2020/경제연구 2020-4.pdf": "2020-4",
    }
    pdf_rows, skipped = [], []
    for path, yi in pdfmap.items():
        try:
            pdf_rows += E.extract_pdf(path, yi)[0]
        except (ValueError, FileNotFoundError) as e:
            skipped.append(str(e))
    pdf = pd.DataFrame(pdf_rows).rename(columns={"source_type": "source"}).assign(source="pdf_text")
    print(f"pdf: {len(pdf)} | {dict(pdf.year_issue.value_counts().sort_index())}")
    for s in skipped:
        print("  SKIPPED:", s)
    if E.UNMAPPED_PUA:
        print("  WARNING unmapped PUA:", dict(E.UNMAPPED_PUA))

    # merge: preserve baseline verbatim, dedupe only the new rows
    new = pd.concat([docx, pdf], ignore_index=True)
    new["author"] = new["author"].replace("", pd.NA)
    ex_keys = set(ex.year_issue.astype(str) + "::" + ex.title.map(despace))
    new["_k"] = new.year_issue.astype(str) + "::" + new.title.map(despace)
    new = new[~new._k.isin(ex_keys)].drop_duplicates("_k").drop(columns="_k")

    out = pd.concat([ex[COLS], new[COLS]], ignore_index=True)
    out["_y"] = out.year_issue.str.split("-").str[0].astype(int)
    out["_i"] = out.year_issue.str.split("-").str[1].astype(int)
    out = out.sort_values(["_y", "_i", "source"]).drop(columns=["_y", "_i"]).reset_index(drop=True)

    out.to_parquet(os.path.join(HERE, "kjyg.parquet"), index=False)
    out.to_csv(os.path.join(HERE, "kjyg.csv"), index=False)

    yrs = out.year_issue.str.split("-").str[0].astype(int)
    expected = {f"{y}-{i}" for y in range(1987, 2021) for i in (1, 2, 3, 4)}
    qa = {
        "total_articles": int(len(out)),
        "by_source": {k: int(v) for k, v in out.source.value_counts().items()},
        "year_range": [int(yrs.min()), int(yrs.max())],
        "missing_author": int(out.author.isna().sum()),
        "missing_content": int(out.content.isna().sum()),
        "missing_issues": sorted(expected - set(out.year_issue)),
        "skipped_files": skipped,
    }
    json.dump(qa, open(os.path.join(HERE, "kjyg_build_qa.json"), "w"),
              ensure_ascii=False, indent=2)
    print("\nFINAL:", json.dumps(qa, ensure_ascii=False))


if __name__ == "__main__":
    main()
