#!/usr/bin/env python3
"""Generate the Google-Classroom-facing docs: course overview, attendance sign-up,
and a one-page syllabus per class. Writes Markdown into curriculum/classroom/.
Mirrors the sibling Disease-Detectives-Curriculum repo's tools/gen_classroom_docs.py.

Source of truth for the 2026-27 season: 12 teaching sessions + 3 practice-test
sessions, run on the same 15 of the 18 available Thursdays as the Disease
Detectives team (same calendar, different time slot) - keep in sync with
curriculum/sessions/README.md and curriculum/practice_tests/README.md if the
season plan changes."""
import os, csv, sys

REPO = "/Users/kxieztt/Documents/crimebuster"
OUT = os.path.join(REPO, "curriculum", "classroom")
SYL = os.path.join(OUT, "syllabi")
CSVDIR = os.path.join(OUT, "google_sheets_import")
for d in (OUT, SYL, CSVDIR):
    os.makedirs(d, exist_ok=True)

# Real team data (names, emails, Drive links) lives in the gitignored _team_roster.py,
# never in this tracked file - this repo is public. See curriculum/classroom/README.md.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from _team_roster import (
        STUDENTS, COACHES, CLASSROOM_DRIVE_URL,
        HOMEWORK_ASSIGNMENTS_URL, HOMEWORK_SUBMIT_URL, SYLLABUS_URL, QUIZ_URL,
        STUDENT_SIGNUP_URL, PARENT_SIGNUP_URL,
    )
except ImportError:
    sys.exit("tools/_team_roster.py not found (it's gitignored - not part of the public repo).\n"
             "Create it with your team's roster; see curriculum/classroom/README.md for the shape.")

# Exact filenames as they'd be uploaded to the homework-assignments Drive folder,
# matching curriculum/pdf/homework/*.pdf (student version, not the _KEY one).
HW_FILENAMES = {
    1: "Homework_01_What_The_Judges_Actually_Score.pdf",
    2: "Homework_02_Qualitative_Analysis_I_The_Workflow.pdf",
    3: "Homework_03_Qualitative_Analysis_II_The_Chemistry.pdf",
    4: "Homework_04_Qualitative_Analysis_III_Mixtures_And_Equations.pdf",
    5: "Homework_05_Liquids_And_pH.pdf",
    6: "Homework_06_Metals.pdf",
    7: "Homework_07_Hair_And_DNA_Evidence.pdf",
    8: "Homework_08_Fibers_And_Chromatography.pdf",
    9: "Homework_09_Plastics.pdf",
    10: "Homework_10_Blood.pdf",
    11: "Homework_11_Blood_Spatter_And_Glass.pdf",
    12: "Homework_12_Soil_Impressions_And_Advanced_Prints.pdf",
}
HW_TITLES = {
    1: "What the Judges Actually Score",
    2: "Qualitative Analysis I — The Workflow",
    3: "Qualitative Analysis II — The Chemistry",
    4: "Qualitative Analysis III — Mixtures & Equations",
    5: "Liquids & pH",
    6: "Metals",
    7: "Hair & DNA Evidence",
    8: "Fibers & Chromatography",
    9: "Plastics",
    10: "Blood",
    11: "Blood Spatter & Glass",
    12: "Soil, Impressions & Advanced Prints",
}

# 15 class slots: (n, date_long, date_short, kind, session_no, title, blurb, vocab, homework, tournament)
CLASSES = [
    (1,  "Thu Sep 17, 2026", "9/17", "lesson", 1, "What the Judges Actually Score",
     "Locard's principle, chain of custody, class vs. individual evidence, direct vs. circumstantial evidence, and how the written analysis report is scored point-by-point.",
     "Locard's exchange principle, chain of custody, class evidence, individual evidence, direct evidence, circumstantial evidence",
     "Homework 1", None),
    (2,  "Thu Sep 24, 2026", "9/24", "lesson", 2, "Qualitative Analysis I — The Workflow",
     "A repeatable powder-testing sequence; building and running a dichotomous key to identify an unknown powder.",
     "qualitative analysis, dichotomous key, powder ID workflow",
     "Homework 2", None),
    (3,  "Thu Oct 1, 2026",  "10/1", "lesson", 3, "Qualitative Analysis II — The Chemistry",
     "DENSE SESSION — chemical formulas on demand; why each test actually works (starch-iodine, carbonate fizz, reducing-sugar tests); the harder powders.",
     "chemical formulas, starch-iodine test, carbonate fizz test, reducing sugar test",
     "Homework 3", None),
    (4,  "Thu Oct 8, 2026",  "10/8", "lesson", 4, "Qualitative Analysis III — Mixtures & Equations",
     "DENSE SESSION — separating mixtures; writing and balancing chemical reactions; a first look at moles and mass.",
     "mixture separation, balanced equations, moles, molar mass",
     "Homework 4", None),
    (5,  "Thu Oct 15, 2026", "10/15", "lesson", 5, "Liquids & pH",
     "Liquid ID and formulas; \"potential hydrogen\"; the acid/base scale; HCl safety rules.",
     "pH scale, acid, base, HCl safety",
     "Homework 5", None),
    (6,  "Thu Oct 22, 2026", "10/22", "lesson", 6, "Metals",
     "Density calculation and unit conversion; atomic number; reaction types; oxide layers; alloys; magnetism.",
     "density, atomic number, oxide layer, alloy, magnetism",
     "Homework 6", None),
    (7,  "Thu Oct 29, 2026", "10/29", "testprep", None, "Practice Test #1 + Answer Review",
     "First full timed practice test (Sessions 1-6 content) under real conditions, then the answer-review routine as a team, all in one 90-minute sitting — expect this to feel rough, the goal is learning the routine, not the score.",
     "—", "Review whatever felt shaky", None),
    (8,  "Thu Nov 5, 2026",  "11/5", "lesson", 7, "Hair & DNA Evidence",
     "Hair growth phases; the medullary-index calculation; hair roots; the poisoning timeline; reading a gel for DNA band matches.",
     "growth phases, medullary index, hair root, gel electrophoresis, band matching",
     "Homework 7", None),
    (9,  "Thu Nov 12, 2026", "11/12", "lesson", 8, "Fibers & Chromatography",
     "The burn-test flow chart as a procedure; naming specific synthetic fibers; Rf value, mobile/stationary phases, and the history of chromatography.",
     "burn test, synthetic fiber, Rf value, chromatography",
     "Homework 8", None),
    (10, "Thu Nov 19, 2026", "11/19", "lesson", 9, "Plastics",
     "Thermoset vs. thermoplastic; resin codes and their uses; building a density-column ladder; polycarbonate; the Bakelite story.",
     "thermoset, thermoplastic, resin code, density column, polycarbonate",
     "Homework 9", None),
    (11, "Thu Dec 3, 2026",  "12/3", "lesson", 10, "Blood",
     "DENSE SESSION — ABO/Rh typing from an agglutination grid; donor/recipient compatibility; parental crosses; blood chemistry; presumptive tests.",
     "ABO blood type, Rh factor, agglutination, donor/recipient, presumptive blood test",
     "Homework 10", None),
    (12, "Thu Dec 10, 2026", "12/10", "testprep", None, "Practice Test #2 + Answer Review",
     "Mid-season checkpoint — full timed practice test (Sessions 1-10 content) plus review, one 90-minute sitting. Most topics are now taught; look for which stations are slow and which knowledge gaps are real.",
     "—", "Review whatever felt shaky", None),
    (13, "Thu Dec 17, 2026", "12/17", "lesson", 11, "Blood Spatter & Glass",
     "Angle of impact by calculation; convergence and area of origin; velocity classes; radial/concentric/cone glass fracture; impact sequencing. Last class before winter break.",
     "angle of impact, convergence, area of origin, velocity class, radial fracture, concentric fracture, cone fracture",
     "Homework 11", None),
    (14, "Thu Jan 7, 2027",  "1/7", "lesson", 12, "Soil, Impressions & Advanced Prints",
     "The soil texture triangle; particle size and color; shoe/tire class vs. individual characteristics; the full IAFIS fingerprint pattern set; AFIS/CODIS/NCIC. First class back from break.",
     "soil texture triangle, class vs. individual characteristics, IAFIS, AFIS, CODIS, NCIC",
     "Homework 12", None),
    (15, "Thu Jan 14, 2027", "1/14", "testprep", None, "Practice Test #3 — Final Dry Run + Review",
     "Final timed dry run under full competition conditions (goggles, aprons, the 50-minute clock, cleanup scored), then review. Last practice before competition.",
     "—", "Rest up for competition", None),
]

TOURNAMENTS_NOTE = (
    "Assumed to match the Disease Detectives team's tournament schedule "
    "(same Division B competitions likely host both events) - confirm and correct if different."
)
TOURNAMENTS = [
    (1, "Sat Jan 9, 2027",  "Oak Valley Invitational @ Oak Valley MS", "tentative, likely"),
    (2, "Sat Jan 16, 2027", "UC Riverside Invitational @ Riverside", "tentative"),
    (3, "Sat Jan 23, 2027", "Carmel Valley Invitational @ CCA", "confirmed"),
    (4, "Sat Feb 6, 2027",  "San Diego Regional @ Mira Mesa College", "confirmed — the target"),
]


def course_overview():
    lines = []
    lines.append("# Crime Busters (Division B) — 2026–27 Course Overview\n")
    lines.append("**Practice:** Thursdays, 6:30–8:00 PM (90 min). **First class:** Thursday, September 17, 2026.\n")
    lines.append(f"**Coaches:** {COACHES}.\n")
    lines.append("**Target competition:** San Diego Regional @ Mira Mesa College, Saturday February 6, 2027 (see tournament note below).\n")
    lines.append("\n---\n")
    lines.append("## Key links\n")
    lines.append("| What | Link |")
    lines.append("|---|---|")
    lines.append(f"| Syllabus (all 15 classes) | {SYLLABUS_URL} |")
    lines.append(f"| Homework assignments (read/download) | {HOMEWORK_ASSIGNMENTS_URL} |")
    lines.append(f"| Submit completed homework (upload to your own named folder) | {HOMEWORK_SUBMIT_URL} |")
    lines.append(f"| Quizzes (answer keys posted separately by the coach after each class) | {QUIZ_URL} |")
    lines.append(f"| Student attendance sign-up sheet | {STUDENT_SIGNUP_URL} |")
    lines.append(f"| Parent attendance sign-up sheet | {PARENT_SIGNUP_URL} |")
    lines.append("\n*(The sign-up sheet links above are still placeholders until those two Google Sheets are created — see the coach's own README for the checklist.)*\n")
    lines.append("\n---\n")
    lines.append("## Team roster\n")
    lines.append("| Student | Email |")
    lines.append("|---|---|")
    for name, email in STUDENTS:
        lines.append(f"| {name} | {email} |")
    lines.append("\n---\n")
    lines.append("## The 15 class dates\n")
    lines.append("| Class | Date | Focus |")
    lines.append("|---|---|---|")
    for (n, dl, ds, kind, sn, title, *_rest) in CLASSES:
        tag = "" if kind == "lesson" else " *(practice test)*"
        lines.append(f"| {n} | {dl} | {title}{tag} |")
    for d, why in [("Thu Nov 26, 2026", "Thanksgiving"), ("Thu Dec 24, 2026", "Christmas Eve"), ("Thu Dec 31, 2026", "New Year's Eve")]:
        lines.append(f"| — | ~~{d}~~ | **NO CLASS — {why}** |")
    lines.append("\nThree more Thursdays are available after Jan 14 (1/21, 1/28, 2/4) and are intentionally left open as buffer/makeup weeks before the regional.\n")
    lines.append("\n---\n")
    lines.append(f"## Tournaments — *{TOURNAMENTS_NOTE}*\n")
    lines.append("| Date | Event | Status |")
    lines.append("|---|---|---|")
    for _n, d, ev, status in TOURNAMENTS:
        lines.append(f"| {d} | {ev} | {status} |")
    lines.append("\n---\n")
    lines.append("## How it's paced\n")
    lines.append("Classes 1-6, 8-10, and 11-14 are new teaching content (12 sessions total). Classes 7, 12, and 15 are full timed practice tests, each with its own answer-review built into the same 90-minute sitting.\n")
    lines.append("\n**Sessions 3, 4, and 10 are the densest** — the curriculum itself says not to add anything extra to those three weeks.\n")
    lines.append("\n---\n")
    lines.append("## Homework\n")
    lines.append("Each of Classes 1-6 and 8-14 has a matching take-home Homework set plus a matching Quiz usable as warm-up review. Two additional general-knowledge homework sets (13 and 14) aren't tied to a specific week — assign them whenever makes sense (e.g., around a practice test). PDFs of every quiz and homework (student version + answer-key version) are in `curriculum/pdf/`.\n")
    return "\n".join(lines) + "\n"


def signup_sheet():
    dates_short = [c[2] for c in CLASSES]
    box = "☐"
    lines = []
    lines.append("# Practice Attendance Sign-Up — 2026–27\n")
    lines.append("Check the box under each date you (or your student) plan to be there. Update it any time as plans change.\n")
    lines.append("- **Students:** we practice best with the whole team — check every date you can make it.\n")
    lines.append("- **Parents:** we need **one parent volunteer at every practice** (in addition to the two coaches). "
                 "Please check the dates you can cover. One check per date across all parents is enough.\n")
    lines.append("\n> This printout is a snapshot. Set up a live Google Sheet from the CSVs in "
                 "`google_sheets_import/` for a version everyone can check online (see classroom/README.md).\n")
    lines.append("\n---\n")
    hdr = "| Name | " + " | ".join(dates_short) + " |"
    sep = "|---|" + "|".join([":-:"] * len(dates_short)) + "|"
    lines.append("## Students\n")
    lines.append(hdr)
    lines.append(sep)
    for name, _email in STUDENTS:
        lines.append(f"| {name} | " + " | ".join([box] * len(dates_short)) + " |")
    lines.append("\n## Parents / Guardians\n")
    lines.append("*(Write your name in; you don't need to fill every row — just the dates you can be the parent on site.)*\n")
    lines.append(hdr.replace("| Name |", "| Parent (of student) |"))
    lines.append(sep)
    for name, _email in STUDENTS:
        lines.append(f"| ________ (of {name}) | " + " | ".join([box] * len(dates_short)) + " |")
    lines.append("\n---\n")
    lines.append("### Date key\n")
    lines.append("| Short | Full date | Class |")
    lines.append("|---|---|---|")
    for (n, dl, ds, kind, sn, title, *_r) in CLASSES:
        lines.append(f"| {ds} | {dl} | Class {n}: {title} |")
    return "\n".join(lines) + "\n"


def syllabus(c):
    (n, dl, ds, kind, sn, title, blurb, vocab, hw, tourn) = c
    lines = []
    lines.append(f"# Class {n} Syllabus — {title}\n")
    tagname = f"**Curriculum Session {sn} of 12**" if kind == "lesson" else "**Practice-test session**"
    lines.append(f"**Date:** {dl} &nbsp;|&nbsp; **Time:** 6:30–8:00 PM &nbsp;|&nbsp; {tagname}")
    if tourn:
        lines.append(f"\n> \U0001f3c6 **Coming up:** {tourn}")
    lines.append("\n---\n")
    lines.append("## What we'll cover\n")
    lines.append(blurb + "\n")
    if vocab and vocab != "—":
        lines.append("## Key vocabulary\n")
        lines.append(vocab + "\n")
    lines.append("## Homework\n")
    if kind == "testprep":
        lines.append(f"{hw}.\n")
    else:
        lines.append(f"**{hw}** — do it on your own before the next class. (The matching **Quiz {sn}** in {QUIZ_URL} is a lighter review you can also use — the answer key gets posted there separately after class.)\n")
        lines.append(f"\n- File: **{HW_FILENAMES[sn]}**")
        lines.append(f"- Assignment folder: {HOMEWORK_ASSIGNMENTS_URL}")
        lines.append(f"- Submit your completed work (in a folder named exactly after you): {HOMEWORK_SUBMIT_URL}\n")
    lines.append("## Bring\n")
    lines.append("Safety goggles and an apron/old clothes — most weeks involve a hands-on lab station. Bring a non-graphing calculator on math-heavy weeks (3, 4, 6, 10, and all practice tests).\n")
    lines.append("\n---\n")
    lines.append("*Part of the Crime Busters (Division B) 2026–27 season. Full course overview and all 15 class syllabi are posted in Google Classroom.*\n")
    return "\n".join(lines) + "\n"


with open(os.path.join(OUT, "Course_Overview.md"), "w") as f:
    f.write(course_overview())

with open(os.path.join(OUT, "Attendance_Signup.md"), "w") as f:
    f.write(signup_sheet())

dates_short = [c[2] for c in CLASSES]
with open(os.path.join(CSVDIR, "students.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Student", "Email"] + dates_short)
    for name, email in STUDENTS:
        w.writerow([name, email] + ["FALSE"] * len(dates_short))
with open(os.path.join(CSVDIR, "parents.csv"), "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Parent / Guardian", "Student", "Email"] + dates_short)
    for name, email in STUDENTS:
        w.writerow(["", name, ""] + ["FALSE"] * len(dates_short))

for c in CLASSES:
    n = c[0]
    slug = c[5].lower()
    slug = "".join(ch if ch.isalnum() or ch == " " else "" for ch in slug).strip().replace("  ", " ").replace(" ", "_")
    fn = f"Class_{n:02d}_{slug[:48].rstrip('_')}.md"
    with open(os.path.join(SYL, fn), "w") as f:
        f.write(syllabus(c))

print("Wrote classroom docs.")
