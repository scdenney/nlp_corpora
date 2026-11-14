# National Assembly Committee Speeches, 2001–2026

## Overview

This corpus holds **1,800 speaking turns** by members of South Korea's National Assembly (국회) in six standing committees, from September 2001 to September 2026. Each turn carries the speaker's party on the day of the meeting, the party's bloc, and whether that party was in government or opposition.

Most of the Assembly's work is done in its standing committees, where members question ministers and officials, review bills and budgets, and each autumn hold the audit of the government (국정감사). Every meeting is recorded word for word in the minutes (국회회의록). The corpus shows what ruling-party and opposition legislators asked the government about, and in what words, across defense, foreign affairs and unification, justice, labor and the environment, health and welfare, and gender and family policy.

The file is a balanced sample: **50 turns for each of six committees in each of six Assembly terms** (fixed seed). It was first prepared for the BA3 Text as Data hackathon at Leiden University (November 2026).

## Files

| File | Description |
|:-----|:------------|
| `assembly_committee_speeches.csv` | The corpus: 1,800 rows × 15 columns, UTF-8, 2.8 MB |
| `data_dictionary.csv` | Variable, type, description, example, and missingness for each column |
| `build/build_assembly.py` | Draws the sample from the full minutes harvest (see Source) |
| `build/build_assembly_parties.py` | Builds dated member–party spells from the Korean Wikipedia member lists |
| `build/assembly_party_spells.csv` | 1,732 dated member–party spells for the 16th–22nd Assemblies; reusable on its own |

The build scripts are kept for provenance. They read a local copy of the full harvest, which is not in this repository.

## Source and Selection

- **Source:** the National Assembly minutes system ([record.assembly.go.kr](https://record.assembly.go.kr)). A full-text harvest built on 2026-11-10 holds 50,423 sets of minutes; minutes from June 2000 on are split into 12.3 million speaker turns.
- **Speakers:** turns by Assembly members only (recorded position 위원 or 의원). The chair, ministers, officials, and witnesses are left out.
- **Meetings:** full meetings of six standing committees; subcommittees are left out.
- **Length:** turns of 300–1,500 characters, duplicates dropped. Shorter turns are mostly procedure or one-line exchanges.
- **Party match:** turns whose speaker could be matched to a member in the party lists (99.9%).
- **Unit:** one speaking turn, that is, what one member said before the next person spoke. The 1,800 turns come from 1,233 meetings and about 565 speakers; the median turn has 482 characters.

| `committee` | Policy area | Committee names in the minutes |
|:--|:--|:--|
| 국방 | defense | 국방위원회 |
| 외교통일 | foreign affairs and unification | 통일외교통상위원회, 외교통상통일위원회, 외교통일위원회 |
| 법제사법 | legislation and judiciary | 법제사법위원회 |
| 환경노동 | environment and labor | 환경노동위원회, 기후에너지환경노동위원회 (from October 2025) |
| 보건복지 | health and welfare | 보건복지위원회 |
| 여성가족 | gender equality and family | 여성위원회 (2002–2005), 여성가족위원회, 성평등가족위원회 (from October 2025) |

Dates by Assembly term: 16th, 2001-09 to 2004-04; 17th, 2004-07 to 2008-05; 19th, 2012-07 to 2016-05; 20th, 2016-06 to 2020-05; 21st, 2020-06 to 2024-05; 22nd, 2024-06 to 2026-09.

## Distributions

| President | Camp | Turns | Ruling party | Opposition | Independent |
|:--|:--|--:|--:|--:|--:|
| 김대중 (Kim Dae-jung) | progressive | 137 | 55 | 81 | 1 |
| 노무현 (Roh Moo-hyun) | progressive | 457 | 175 | 262 | 20 |
| 이명박 (Lee Myung-bak) | conservative | 70 | 25 | 43 | 2 |
| 박근혜 (Park Geun-hye) | conservative | 308 | 130 | 171 | 7 |
| 문재인 (Moon Jae-in) | progressive | 369 | 169 | 195 | 5 |
| 윤석열 (Yoon Suk-yeol) | conservative | 297 | 83 | 213 | 1 |
| 이재명 (Lee Jae-myung) | progressive | 162 | 82 | 78 | 2 |

| Bloc | Turns | Largest parties |
|:--|--:|:--|
| democratic | 879 | 더불어민주당 486, 열린우리당 117, 새천년민주당 93, 새정치민주연합 64, 민주당 45, 민주통합당 45 |
| conservative | 751 | 한나라당 305, 국민의힘 191, 새누리당 152, 자유한국당 88 |
| other party | 132 | 정의당 34, 국민의당 22, 민주노동당 20, 바른미래당 20, 조국혁신당 15 |
| independent | 38 | 무소속 |

An Assembly term does not line up with one government; most terms span two presidents.

## Variables

See `data_dictionary.csv` for the full list. The main ones:

- `text`: the turn as recorded, with surrounding whitespace trimmed. Not otherwise preprocessed.
- `party`: the member's party on the date of the meeting, from the Korean Wikipedia lists of members for each Assembly (party at election, party renamings, and dated switches). Checked against an independently coded Assembly file, the two agree on 99.7% of shared rows.
- `bloc`: party family: democratic (민주당 계열), conservative (보수 계열), other party, independent.
- `ruling_opposition`: whether the speaker's party was the president's party on that date. A president's party still counts as governing in months when the president had left it (김대중 from May 2002; 노무현 from September 2003 and from February 2007). 열린우리당 counts as governing from its founding on 2003-11-11; before that 새천년민주당 does, and members who had already left it are coded independent.
- `president`, `president_camp`: the president in office on the date. Acting presidencies are counted with the president they followed (December 2016 to May 2017; December 2024 to June 2025).
- `committee`, `committee_name`: a single policy-area label, and the name as recorded.
- `assembly_term`, `meeting_type`, `date`, `year`: terms begin on May 30; meeting types are 국정감사 (annual audit), 정기회 (regular session), and 임시회 (extraordinary session).
- `speaker`: name as printed; in hanja until about 2004.

## Known Limitations

- **The 18th Assembly is missing.** The source has no speaker turns from June 2008 to June 2012, so the Lee Myung-bak government has only 70 turns.
- **Equal cells, not proportions.** Every committee and term has 50 turns whatever its real volume. Counts across committees or terms are not estimates of how much was said.
- **Ruling and opposition change sides.** The democratic bloc governs under progressive presidents and is the opposition under conservative ones. Check both `bloc` and `ruling_opposition` before reading a bloc difference.
- **Party is matched by name.** A rare mistake is possible, above all for members who changed party. The same party name can mean different parties in different years (민주당 in 2005–2007 and 2013–2014), so `bloc` is safer for comparisons over time.
- **Turns, not speeches.** A turn may begin mid-argument, answer something not in the file, or be cut off.
- **Stage notes.** The minutes add notes in parentheses: 117 turns contain (발언시간 초과로 마이크 중단), 108 contain (영상자료를 보며). These words enter word counts and topic models.
- **Hanja names.** The same person can appear under a hanja and a Hangul spelling; 103 texts also contain hanja names.
- **Private individuals.** Members sometimes name private individuals. Do not quote their names or identifying details.

## License and Attribution

Statements made in the National Assembly are public record and may be used freely under Article 24 of the Korean Copyright Act. Party data come from Korean Wikipedia (CC BY-SA).

Suggested attribution: *National Assembly minutes (국회회의록, record.assembly.go.kr), with party from the Korean Wikipedia lists of Assembly members; sample prepared by Steven Denney, NLP Corpora for Korean Studies (2026).*

The full 12.3-million-turn harvest (about 2 GB) is too large for this repository; contact the maintainer about access.
