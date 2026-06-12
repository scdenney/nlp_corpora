# Naver Movie Reviews (Classroom Edition)

## Overview

This corpus is a curated, classroom-safe subset of the **Naver Sentiment Movie Corpus (NSMC)**: 50,000 short Korean movie reviews posted by users of Naver Movies (collected 2015), balanced between strongly positive and strongly negative reviews. It is the working corpus behind *Feeling in Numbers* (<https://scdenney.github.io/feeling-in-numbers/>), the point-and-click text lab built for the Leiden University PRE-Class in Asian Studies, and doubles as a low-barrier teaching corpus for sentiment, internet language, and expressive Korean (emoticons, ideophones, exclamations).

Reviews are user-generated text: short (5–140 characters), colloquial, and full of jamo emoticons (ㅋㅋ, ㅠㅠ, ㄷㄷ), slang (꿀잼, 노잼, 대박), and ideophones (두근두근, 펑펑, 울컥). Each review carries a binary sentiment label derived from the original star rating, which makes word–feeling association analysis possible with nothing more than counting.

---

## Variables

### `naver_movie_reviews.csv` — 3 columns, 50,000 rows. Each row is one review.

| Variable | Type | Description |
|----------|------|-------------|
| **id** | integer | Stable row index (0–49999). Matches the review indices used by the *Feeling in Numbers* app and the translations file below. |
| **text** | string | Full review text as written, including emoticons, typos, and slang. 5–140 characters; always contains hangul. |
| **label** | integer | Sentiment from the original Naver star rating: `1` = positive (rating 9–10), `0` = negative (rating 1–4). Exactly 25,000 each. Neutral ratings (5–8) were excluded upstream by NSMC. |

### `example_translations.csv` — 3 columns, 398 rows.

| Variable | Type | Description |
|----------|------|-------------|
| **id** | integer | Row index into `naver_movie_reviews.csv`. |
| **text_ko** | string | The original review. |
| **text_en** | string | Hand-made English translation. Tone, sarcasm, and emoticons are preserved (ㅋㅋ stays ㅋㅋ). Useful as a parallel mini-corpus or for teaching with non-Korean-reading students. |

---

## Processing

Built from the NSMC `ratings_train.txt` + `ratings_test.txt` (200,000 reviews) by `prep/prep.py` in the [feeling-in-numbers](https://github.com/scdenney/feeling-in-numbers) repository:

1. Drop rows outside 5–140 characters or without hangul; deduplicate on whitespace-collapsed text.
2. **Safety filter** (the corpus is used with secondary-school students): reviews containing profanity, sexual content, or slurs are removed, including spaced and digit-obfuscated spellings (존.나, 시1발). The filter is deliberately aggressive — roughly 4,200 reviews blocked — and accepts rare false positives. It is best-effort, not a guarantee.
3. Balanced random sample (seed 42): 25,000 positive + 25,000 negative.
4. A re-sweep utility (`prep/sweep.py`) replaces any newly flagged review **in place**, so `id` values stay stable across filter updates.

## Suggested Uses

- First contact with text-as-data: word frequency and word–sentiment association via simple counting (no models needed — the labels do the work).
- Expressive language: distribution of emoticons, exclamations, and ideophones across positive/negative reviews (e.g., ㅠㅠ and 슬프다 skew strongly *positive* — Koreans rate tearjerkers highly).
- Internet Korean: orthographic play, intensifiers, slang lifecycles, register variation.
- A clean springboard before heavier corpora (NIKL Modu, KLUE) in BA teaching or thesis pilots.

## Source and License

Derived from the [Naver Sentiment Movie Corpus](https://github.com/e9t/nsmc) (Lucy Park, 2015), released under **CC0 1.0**. This derivative subset and the translations are likewise released under **CC0 1.0**. Note the safety filtering above before any reuse that assumes the full NSMC distribution.

> Park, Lucy. (2015). *Naver Sentiment Movie Corpus v1.0*. <https://github.com/e9t/nsmc>
