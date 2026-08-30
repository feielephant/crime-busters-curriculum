# Project notes for Claude

## What this is

A year-2 (advanced) coaching curriculum for Science Olympiad Crime Busters
Division B. Modeled on `~/Documents/Disease-Detectives-Curriculum`. See `README.md`.

## Hard rules

- **This repo is PUBLIC.** Never commit anything from `raw/` or `planning/`, and
  never paste test questions, answer-key text, or slide content verbatim into
  tracked files. Homework and quiz questions must be *original constructions* in
  the style/format of real tests, not copies. Scenarios, suspect names, and
  numbers must be invented.
- **No student or family names, no team name, no school name** anywhere in
  tracked files. Keep it generic ("the team", "a kid", "your students").
- Source material (real tests/keys, topic decks, the rules PDF) lives in `raw/`,
  git-ignored. Design/analysis notes live in `planning/`, git-ignored.

## Audience calibration

- Coach: parent, general science background, zero teaching experience. Scripts are
  read-aloud with `COACH SCRIPT:` blocks, `[ASK THE TEAM]`, `[CHECKPOINT]`,
  `[ACTIVITY]`, timed segments, and a "common kid mistakes" list at the end.
- Kids: grades 5–6, team of 2 or 4. Two-person event → activities built around
  pairs; a 4-kid team runs as two pairs.
- Sessions are 90 minutes. Each has a "if you only have 60 minutes" cut path.

## The year-2 mandate

Year 1 already covered the basics (fingerprint patterns, hair/fiber categories,
plastics list, basic chromatography + Rf, DNA structure, a powder lookup table).
Do **not** re-teach those — open each session with a fast prerequisite recap, then
spend the session on the gap. The gap analysis is in
`planning/YEAR1_vs_TESTS_gap_analysis.md`. Headline gaps: formula-level qual
analysis, stoichiometry, blood (year 1 taught none), spatter angle calc, soil
texture triangle, IAFIS 8-pattern, hair growth phases + medullary index,
thermoset vs thermoplastic, glass fracture, the analysis-report scoring rubric.

## Build order

1. `curriculum/Crime_Busters_Knowledge_Document.md` — the spine (do first)
2. `curriculum/sessions/` — 12 scripts
3. `curriculum/quizzes/` + `curriculum/homework/` + `curriculum/home_labs/`
4. `curriculum/practice_tests/`
5. Field Guide HTML + slide-deck suggestions (later — user will decide on PPT after seeing the curriculum)

## Content accuracy

Ground every fact against the official 2025 Div B rules (`raw/Science_Olympiad_Div_B_Rules_2025_for_Web_Secured.pdf`,
event section) and what the real tests in `raw/` actually asked. When sources
disagree (e.g. fingerprint frequency percentages, Bradford-Hill-style list
counts), teach the range and note the disagreement.
