# Crime Busters Curriculum — Year 2 (Advanced)

A coaching curriculum for Science Olympiad **Crime Busters (Division B)**, written
for a parent coach (not a professional teacher) running weekly practices for a
small team (2 or 4 kids, grades 5–6).

This is a **second-year** curriculum. It assumes the team has already had a full
first season covering the basics — fingerprint patterns, hair/fiber categories,
the plastics list, basic chromatography, DNA structure, the powder-ID lookup
table. Those topics are treated as **prerequisite review** (a fast recap at the
top of the relevant session), and the real teaching time goes to the material
that shows up on real invitational tests but was never taught in year one:
formula-level qualitative analysis, stoichiometry, blood typing and blood
chemistry, blood-spatter angle calculations, the soil texture triangle, the full
IAFIS fingerprint classification, hair growth phases and the medullary index,
thermoset vs. thermoplastic polymers, and glass-fracture analysis.

The design pattern is borrowed from a sibling project,
`Disease-Detectives-Curriculum`: a single reference **Knowledge Document**, plus
one full read-aloud **coach script** per practice, plus a standalone **quiz** and
a two-track **homework** set for each.

## Who this is for

- **Coach:** a parent with a general science background, no teaching experience.
  Every session script is written to be read from directly, with timed segments,
  exact talking points, hands-on lab stations sized for 2 or 4 kids, checkpoints,
  and a list of common kid mistakes at the end.
- **Team:** 2 or 4 students, grades 5–6. Crime Busters is a two-person event, so
  activities are built around pairs (with a 4-kid team running as two pairs).

## Repo structure

```
curriculum/
├── Crime_Busters_Knowledge_Document.md   ← the reference spine: every topic, at test depth
├── sessions/        ← 12 full coach scripts (90 min each), one per practice
├── quizzes/         ← one standalone review quiz per teaching session
├── homework/        ← one take-home per session: a paper track + a home-lab track
├── home_labs/       ← the home-lab program: safety agreement, kit contents, lab cards
└── practice_tests/  ← how to run the 3 practice-test sessions + an answer-review guide
```

Everything the curriculum was built and cross-checked from — real invitational
tests, answer keys, and topic slide decks — is **not** in this repo. It is
copyrighted material belonging to the schools and organizations that wrote it,
kept locally in an ignored `raw/` folder. This repo contains only original work
and is safe to be public.

## Season shape

~15 weekly 90-minute meetings: **12 teaching sessions + 3 practice-test sessions**
(after Session 6, after Session 10, and a final timed dry run before competition).
See [`curriculum/sessions/README.md`](curriculum/sessions/README.md) for the full
sequence.

## Safety

The home-lab homework track uses a coach-assembled kit of **food-grade powders
only** plus a few mild household reagents. No strong acids or bases ever go home.
The 1 M HCl test that the event supplies at competition is practiced **only at
in-person practice, with the coach present.** Every home lab requires a parent's
signature on the one-time
[Home Lab Safety Agreement](curriculum/home_labs/Home_Lab_Safety_Agreement.md).

## License

Curriculum content is released under [CC BY 4.0](LICENSE) — use it, adapt it, share
it, with attribution.
