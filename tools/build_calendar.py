#!/usr/bin/env python3
"""Generate an .ics calendar for the 2026-27 Crime Busters season:
15 weekly Thursday classes (6:30-8:00 PM) + the 4 tournaments (assumed to match
the Disease Detectives team's schedule - confirm and fix if different).
Import the file into Google Calendar / Apple Calendar / Outlook."""
import datetime as dt
import os, sys

# Real team data (Drive/Sheet links, location) lives in the gitignored _team_roster.py,
# never in this tracked file - this repo is public. See curriculum/classroom/README.md.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from _team_roster import (
        HOMEWORK_ASSIGNMENTS_URL, HOMEWORK_SUBMIT_URL,
        STUDENT_SIGNUP_URL, PARENT_SIGNUP_URL, LOCATION,
    )
except ImportError:
    sys.exit("tools/_team_roster.py not found (it's gitignored - not part of the public repo).\n"
             "Create it with your team's data; see curriculum/classroom/README.md for the shape.")

OUT = "/Users/kxieztt/Documents/crimebuster/curriculum/classroom/CrimeBusters_Schedule.ics"
START_HM = (18, 30)
END_HM = (20, 0)

HW_FILENAMES = {
    # No key 1 - Session 1 is pure orientation, no homework assigned that week.
    2: "Homework_02_Powders_101_Workflow_And_Chemistry.pdf",
    3: "Homework_03_What_The_Judges_Actually_Score.pdf",
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
    2: "Powders 101 — The Workflow and the Chemistry",
    3: "What the Judges Actually Score",
    4: "Qualitative Analysis III — Mixtures & Equations",
    5: "Liquids & pH", 6: "Metals", 7: "Hair & DNA Evidence", 8: "Fibers & Chromatography",
    9: "Plastics", 10: "Blood", 11: "Blood Spatter & Glass", 12: "Soil, Impressions & Advanced Prints",
}

# (class #, date, title, homework # assigned at THIS class (None if none), one-line description)
CLASSES = [
    (1,  dt.date(2026, 9, 17),  "Orientation & Event Overview",
     None, "Class rules, safety rules, event format, test-scoring breakdown, sample-test walkthrough, season rubric, home practice kit + safety agreement handout. No forensic science content yet."),
    (2,  dt.date(2026, 9, 24),  "Powders 101 - The Workflow and the Chemistry (MERGED, long)",
     2, "A repeatable powder-testing sequence and dichotomous keys, plus the chemistry: formulas on demand, why each test works (starch-iodine, carbonate fizz, reducing-sugar), the harder powders."),
    (3,  dt.date(2026, 10, 1),  "What the Judges Actually Score",
     3, "Locard's principle, chain of custody, class vs. individual evidence, direct vs. circumstantial evidence, how the analysis report is scored."),
    (4,  dt.date(2026, 10, 8),  "Qualitative Analysis III — Mixtures & Equations (DENSE)",
     4, "Separating mixtures; writing and balancing reactions; moles and mass."),
    (5,  dt.date(2026, 10, 15), "Liquids & pH",
     5, "Liquid ID and formulas; the pH scale; acid/base; HCl safety."),
    (6,  dt.date(2026, 10, 22), "Metals",
     6, "Density calculation and unit conversion; atomic number; reaction types; oxide layers; alloys; magnetism."),
    (7,  dt.date(2026, 10, 29), "Practice Test #1 + Answer Review",
     None, "First full timed practice test (Sessions 1-6), then review - one 90-min sitting. Bring a calculator."),
    (8,  dt.date(2026, 11, 5),  "Hair & DNA Evidence",
     7, "Hair growth phases; medullary-index calculation; hair roots; poisoning timeline; reading a DNA gel."),
    (9,  dt.date(2026, 11, 12), "Fibers & Chromatography",
     8, "Burn-test flow chart; naming synthetic fibers; Rf value and phases; history of chromatography."),
    (10, dt.date(2026, 11, 19), "Plastics",
     9, "Thermoset vs. thermoplastic; resin codes; density-column ladder; polycarbonate; the Bakelite story."),
    (11, dt.date(2026, 12, 3),  "Blood (DENSE)",
     10, "ABO/Rh typing from an agglutination grid; donor/recipient; parental crosses; blood chemistry; presumptive tests."),
    (12, dt.date(2026, 12, 10), "Practice Test #2 + Answer Review",
     None, "Mid-season checkpoint - full timed practice test (Sessions 1-10), then review. Bring a calculator."),
    (13, dt.date(2026, 12, 17), "Blood Spatter & Glass",
     11, "Angle of impact by calculation; convergence and origin; velocity classes; glass fracture types; impact sequencing. Last class before winter break."),
    (14, dt.date(2027, 1, 7),   "Soil, Impressions & Advanced Prints",
     12, "Soil texture triangle; particle size/color; shoe/tire class vs. individual characteristics; full IAFIS pattern set; AFIS/CODIS/NCIC. First class back from break."),
    (15, dt.date(2027, 1, 14),  "Practice Test #3 — Final Dry Run + Review",
     None, "Final timed dry run under full competition conditions (goggles, aprons, 50-min clock, cleanup scored), then review. Last practice before competition."),
]

# Assumed to match the Disease Detectives team's tournaments - confirm and fix if different.
TOURNAMENTS = [
    (dt.date(2027, 1, 9),  "Oak Valley Invitational @ Oak Valley Middle School (tentative, likely) - UNCONFIRMED for Crime Busters, assumed same as Disease Detectives"),
    (dt.date(2027, 1, 16), "UC Riverside Invitational @ Riverside (tentative) - UNCONFIRMED for Crime Busters, assumed same as Disease Detectives"),
    (dt.date(2027, 1, 23), "Carmel Valley Invitational @ Canyon Crest Academy (confirmed for Disease Detectives) - UNCONFIRMED for Crime Busters, assumed same"),
    (dt.date(2027, 2, 6),  "San Diego Regional @ Mira Mesa College (confirmed for Disease Detectives) - UNCONFIRMED for Crime Busters, assumed same - the target"),
]

DTSTAMP = "20260910T000000Z"
TZID = "America/Los_Angeles"


def esc(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def fold(line):
    out = []
    while len(line.encode("utf-8")) > 75:
        cut = 74
        while len(line[:cut].encode("utf-8")) > 74:
            cut -= 1
        out.append(line[:cut])
        line = " " + line[cut:]
    out.append(line)
    return "\r\n".join(out)


lines = [
    "BEGIN:VCALENDAR", "VERSION:2.0",
    "PRODID:-//Crime Busters Curriculum//Season 2026-27//EN",
    "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
    "X-WR-CALNAME:Crime Busters 2026-27",
    "X-WR-TIMEZONE:" + TZID,
    "BEGIN:VTIMEZONE", "TZID:" + TZID, "X-LIC-LOCATION:" + TZID,
    "BEGIN:DAYLIGHT", "TZOFFSETFROM:-0800", "TZOFFSETTO:-0700", "TZNAME:PDT",
    "DTSTART:19700308T020000", "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU", "END:DAYLIGHT",
    "BEGIN:STANDARD", "TZOFFSETFROM:-0700", "TZOFFSETTO:-0800", "TZNAME:PST",
    "DTSTART:19701101T020000", "RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU", "END:STANDARD",
    "END:VTIMEZONE",
]

by_num = {c[0]: c for c in CLASSES}

for n, d, title, hw_num, desc in CLASSES:
    assert d.weekday() == 3, f"Class {n} on {d} is not a Thursday"
    ds = f"{d:%Y%m%d}"
    st = f"{ds}T{START_HM[0]:02d}{START_HM[1]:02d}00"
    en = f"{ds}T{END_HM[0]:02d}{END_HM[1]:02d}00"
    description = f"{desc}\n\n(Class {n} of 15 - see the syllabus in Google Classroom.)"
    if hw_num is not None:
        description += (
            f"\n\nHomework {hw_num} assigned today: {HW_TITLES[hw_num]}"
            f"\nFile: {HW_FILENAMES[hw_num]}"
            f"\nAssignment folder: {HOMEWORK_ASSIGNMENTS_URL}"
            f"\nSubmit your completed work (in a folder named exactly after you): {HOMEWORK_SUBMIT_URL}"
            f"\nDue: 2 days before the next class."
        )
    lines += [
        "BEGIN:VEVENT",
        f"UID:cb-2627-class-{n:02d}@crime-busters-curriculum",
        f"DTSTAMP:{DTSTAMP}",
        f"DTSTART;TZID={TZID}:{st}",
        f"DTEND;TZID={TZID}:{en}",
        ("SUMMARY:" + esc(f"Crime Busters - Class {n}: {title}")),
        ("LOCATION:" + esc(LOCATION)),
        ("DESCRIPTION:" + esc(description)),
        "STATUS:CONFIRMED",
        "END:VEVENT",
    ]

for n, d, title, _hw_num, _desc in CLASSES:
    remind_date = d - dt.timedelta(days=2)
    prev = by_num.get(n - 1)
    prev_hw_num = prev[3] if prev else None
    summary_bits = ["update sign-up sheets"]
    if prev_hw_num is not None:
        summary_bits.insert(0, f"submit Homework {prev_hw_num}")
    summary = f"Reminder: {' + '.join(summary_bits)} (Class {n} is Thursday)"
    desc_lines = [
        f"Before Class {n} ({d:%a %b %-d}) this Thursday:",
        "",
        "1. Update your attendance on the sign-up sheets:",
        f"   - Student sign-up: {STUDENT_SIGNUP_URL}",
        f"   - Parent sign-up: {PARENT_SIGNUP_URL}",
    ]
    if prev_hw_num is not None:
        desc_lines += [
            "",
            f"2. Submit Homework {prev_hw_num}: {HW_TITLES[prev_hw_num]}",
            f"   File: {HW_FILENAMES[prev_hw_num]} (find it in the assignment folder: {HOMEWORK_ASSIGNMENTS_URL})",
            f"   Upload your completed work to: {HOMEWORK_SUBMIT_URL}",
            "   (create a folder there with your exact name if you don't have one yet)",
        ]
    lines += [
        "BEGIN:VEVENT",
        f"UID:cb-2627-reminder-{n:02d}@crime-busters-curriculum",
        f"DTSTAMP:{DTSTAMP}",
        f"DTSTART;VALUE=DATE:{remind_date:%Y%m%d}",
        f"DTEND;VALUE=DATE:{remind_date + dt.timedelta(days=1):%Y%m%d}",
        ("SUMMARY:" + esc("📋 " + summary)),
        ("DESCRIPTION:" + esc("\n".join(desc_lines))),
        "STATUS:CONFIRMED",
        "END:VEVENT",
    ]

for d, summary in TOURNAMENTS:
    lines += [
        "BEGIN:VEVENT",
        f"UID:cb-2627-tourn-{d:%Y%m%d}@crime-busters-curriculum",
        f"DTSTAMP:{DTSTAMP}",
        f"DTSTART;VALUE=DATE:{d:%Y%m%d}",
        f"DTEND;VALUE=DATE:{d + dt.timedelta(days=1):%Y%m%d}",
        ("SUMMARY:" + esc(f"Tournament (unconfirmed): {summary.split(' @ ')[0]}")),
        ("DESCRIPTION:" + esc(summary + "\n\nSaturday event - does not replace the Thursday class that week.")),
        "STATUS:TENTATIVE",
        "END:VEVENT",
    ]

lines.append("END:VCALENDAR")

with open(OUT, "w", newline="") as f:
    f.write("\r\n".join(fold(l) if not l.startswith(" ") else l for l in lines) + "\r\n")

print("wrote", OUT)
print(f"{len(CLASSES)} classes + {len(TOURNAMENTS)} tournaments")
