"""Build the hackathon National Assembly corpus: a small sample of members' committee speeches.

Source (read-only): the full-text harvest of record.assembly.go.kr built 2026-11-10 (50,423 sets
of minutes; turns.parquet holds 12.3 million speaker turns, 2000-06 to 2026-09). The master copy
is on the Mac in ~/Downloads/assembly-corpus. Point ASSEMBLY_CORPUS at a folder that holds
documents.parquet and turns.parquet.

    ASSEMBLY_CORPUS=~/.cache/ba3tad/assembly-corpus \
      uv run --with duckdb --with pandas --with pyarrow python build/build_assembly.py

Selection: one row per speaking turn of an Assembly member (position 위원 or 의원) in a full
meeting of one of six standing committees, 300-1,500 characters long, with exact duplicate texts
dropped. A random sample of 50 turns per committee and Assembly term, with a fixed seed. The text
is left as written: only surrounding whitespace is trimmed.

Party: assembly_party_spells.csv (written by build_assembly_parties.py from the Korean Wikipedia
member lists) gives each speaker's party on the date of the meeting. Turns whose speaker could not
be matched to a member are left out before sampling. The party family (bloc) and the ruling or
opposition status follow the coding of the Session 5 file assembly-nk-japan.csv.
"""
import os
from pathlib import Path

import duckdb
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "assembly-speeches"
SRC = Path(os.environ.get("ASSEMBLY_CORPUS", Path.home() / "Downloads/assembly-corpus")).expanduser()
SEED = 20261113
PER_CELL = 50
MIN_CHARS, MAX_CHARS = 300, 1500

# Committee names as recorded -> one label per policy area. Three of the six were renamed: foreign
# affairs and unification twice, and in October 2025 environment and labor (기후에너지환경노동위원회) and
# gender equality and family (성평등가족위원회). 여성위원회 (2002-2005) preceded 여성가족위원회.
COMMITTEES = {
    "국방위원회": "국방",
    "통일외교통상위원회": "외교통일",
    "외교통상통일위원회": "외교통일",
    "외교통일위원회": "외교통일",
    "법제사법위원회": "법제사법",
    "환경노동위원회": "환경노동",
    "기후에너지환경노동위원회": "환경노동",
    "보건복지위원회": "보건복지",
    "여성위원회": "여성가족",
    "여성가족위원회": "여성가족",
    "성평등가족위원회": "여성가족",
}
MEMBER_POSITIONS = ("위원", "委員", "의원", "議員")

# Assembly terms start on May 30. The 18th (2008-05-30 to 2012-05-29) is not in the source.
TERMS = [("2000-05-30", 16), ("2004-05-30", 17), ("2008-05-30", 18), ("2012-05-30", 19),
         ("2016-05-30", 20), ("2020-05-30", 21), ("2024-05-30", 22)]
TERM_LABEL = {16: "16th", 17: "17th", 18: "18th", 19: "19th", 20: "20th", 21: "21st", 22: "22nd"}
# President in office on the date of the meeting. An acting presidency is counted with the
# president it followed (2017-03-10 to 2017-05-09, and 2025-04-04 to 2025-06-03).
GOVERNMENTS = [("1998-02-25", "김대중", "progressive"), ("2003-02-25", "노무현", "progressive"),
               ("2008-02-25", "이명박", "conservative"), ("2013-02-25", "박근혜", "conservative"),
               ("2017-05-10", "문재인", "progressive"), ("2022-05-10", "윤석열", "conservative"),
               ("2025-06-04", "이재명", "progressive")]

# Party families and the president's party by date, coded as in the Session 5 Assembly file.
BLOC = {
    "conservative": {"한나라당", "새누리당", "자유한국당", "미래통합당", "미래한국당", "국민의힘", "바른정당",
                     "새로운보수당", "자유민주연합"},
    "democratic": {"새천년민주당", "열린우리당", "대통합민주신당", "중도개혁통합신당", "중도통합민주당", "통합민주당",
                   "민주당", "민주통합당", "새정치민주연합", "더불어민주당", "더불어시민당"},
}
RULING = [("1998-02-25", {"새천년민주당"}), ("2003-11-11", {"열린우리당"}), ("2007-08-20", {"대통합민주신당", "통합민주당"}),
          ("2008-02-25", {"한나라당", "새누리당"}), ("2013-02-25", {"새누리당", "자유한국당"}),
          ("2017-05-10", {"더불어민주당", "더불어시민당"}), ("2022-05-10", {"국민의힘"}),
          ("2025-06-04", {"더불어민주당"})]


def bloc(party: str) -> str:
    if party == "무소속":
        return "independent"
    return next((b for b, parties in BLOC.items() if party in parties), "other party")


def ruling_opposition(party: str, ruling: set) -> str:
    if party == "무소속":
        return "independent"
    return "ruling party" if party in ruling else "opposition"


def add_party(cand: pd.DataFrame) -> pd.DataFrame:
    """Attach the speaker's party on the meeting date; drop turns with no matched member."""
    spells = pd.read_csv(HERE / "assembly_party_spells.csv", dtype=str)
    spells["assembly_term"] = spells.assembly_term.astype(int)
    m = cand.merge(spells[["speaker", "assembly_term", "party", "start_date", "end_date"]],
                   on=["speaker", "assembly_term"], how="left")
    m = m[(m.date >= m.start_date) & (m.date <= m.end_date)]
    assert not m.duplicated(["mnts_id", "turn_i"]).any(), "overlapping party spells"
    print(f"turns with a party: {len(m)} of {len(cand)} ({len(m) / len(cand):.1%})")
    lost = cand.merge(m[["mnts_id", "turn_i"]], how="left", indicator=True).query("_merge == 'left_only'")
    print("unmatched turns by term:", lost.groupby("assembly_term").size().to_dict())
    return m.drop(columns=["start_date", "end_date"])


def lookup(dates: pd.Series, table: list, col: int) -> pd.Series:
    starts = [row[0] for row in table]
    idx = pd.Index(starts).searchsorted(dates.values, side="right") - 1
    return pd.Series([table[i][col] for i in idx], index=dates.index)


def main() -> None:
    con = duckdb.connect()
    cand = con.execute(
        f"""
        SELECT t.mnts_id, t.turn_i, t.speaker, d.date, d.body, d.session_type, trim(t.text) AS text
        FROM read_parquet('{SRC / "turns.parquet"}') t
        JOIN read_parquet('{SRC / "documents.parquet"}') d USING (mnts_id)
        WHERE t.pos IN {MEMBER_POSITIONS}
          AND d.body IN {tuple(COMMITTEES)}
          AND d.date IS NOT NULL
          AND length(trim(t.text)) BETWEEN {MIN_CHARS} AND {MAX_CHARS}
        ORDER BY t.mnts_id, t.turn_i
        """
    ).df()
    print(f"candidate turns: {len(cand)}")
    cand = cand.drop_duplicates("text")
    # A few turns share one turn number in the source (a turn split around a video or a chart).
    # They are left out, so that every id names one turn.
    cand = cand[~cand.duplicated(["mnts_id", "turn_i"], keep=False)]
    cand["committee"] = cand.body.map(COMMITTEES)
    cand["speaker"] = cand.speaker.str.strip()
    cand["assembly_term"] = lookup(cand.date, TERMS, 1)
    cand = add_party(cand)
    print(cand.groupby(["committee", "assembly_term"]).size().unstack(fill_value=0).to_string())

    parts = [g.sample(n=min(len(g), PER_CELL), random_state=SEED)
             for _, g in cand.groupby(["committee", "assembly_term"], sort=True)]
    s = pd.concat(parts).sort_values(["date", "mnts_id", "turn_i"])
    df = pd.DataFrame({
        "id": ("na-" + s.mnts_id.astype(str) + "-" + s.turn_i.astype(str)).values,
        "date": s.date.values,
        "year": s.date.str[:4].astype(int).values,
        "assembly_term": s.assembly_term.map(TERM_LABEL).values,
        "president": lookup(s.date, GOVERNMENTS, 1).values,
        "president_camp": lookup(s.date, GOVERNMENTS, 2).values,
        "committee": s.committee.values,
        "committee_name": s.body.values,
        "meeting_type": s.session_type.str.replace("·폐회중", "", regex=False).values,
        "speaker": s.speaker.values,
        "party": s.party.values,
        "bloc": s.party.map(bloc).values,
        "ruling_opposition": [ruling_opposition(p, r) for p, r in zip(s.party, lookup(s.date, RULING, 1))],
        "text": s.text.values,
    })
    df["n_chars"] = df["text"].str.len()
    OUT.mkdir(exist_ok=True)
    path = OUT / "data.csv"
    df.to_csv(path, index=False, encoding="utf-8")

    print(f"\n== assembly-speeches: {len(df)} rows, {path.stat().st_size / 1e6:.2f} MB")
    print("   n_chars:", df.n_chars.describe().round().to_dict())
    print("   empty:", (df.text == "").sum(), " duplicate texts:", df.text.duplicated().sum(),
          " duplicate ids:", df.id.duplicated().sum())
    print("   meetings:", s.mnts_id.nunique(), " speakers:", df.speaker.nunique())
    print("   texts with a line break:", df.text.str.contains("\n").sum(),
          " with hanja:", df.text.str.contains("[一-龥]").sum())
    for col in ["committee", "assembly_term", "president", "president_camp", "meeting_type", "committee_name",
                "party", "bloc", "ruling_opposition"]:
        print(f"\n{df[col].value_counts(sort=False).to_string()}")
    print("\n" + pd.crosstab(df.president, df.ruling_opposition).to_string())
    print("\n" + pd.crosstab(df.assembly_term, df.bloc).to_string())
    print("\n" + pd.crosstab([df.president, df.party], df.ruling_opposition).to_string())


if __name__ == "__main__":
    main()
