#!/usr/bin/env python3
"""Fillable-PDF version of the attendance sign-up: real AcroForm checkbox fields
that click and save in any normal PDF viewer (Preview, Acrobat, Chrome's viewer).
Two pages: students, then parents. Mirrors the sibling Disease-Detectives-Curriculum
repo's tools/build_fillable_signup.py."""
import os, sys
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white

# Real team data lives in the gitignored _team_roster.py, never in this tracked file -
# this repo is public. See curriculum/classroom/README.md.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    from _team_roster import STUDENTS as _STUDENTS
except ImportError:
    sys.exit("tools/_team_roster.py not found (it's gitignored - not part of the public repo).\n"
             "Create it with your team's roster; see curriculum/classroom/README.md for the shape.")

REPO = "/Users/kxieztt/Documents/crimebuster"
OUT = os.path.join(REPO, "curriculum", "classroom", "pdf", "Attendance_Signup_fillable.pdf")

STUDENTS = [name for name, _email in _STUDENTS]
DATES = ["9/17", "9/24", "10/1", "10/8", "10/15", "10/22", "10/29", "11/5", "11/12",
         "11/19", "12/3", "12/10", "12/17", "1/7", "1/14"]
LESSONS = ["S1 Judges", "S2 QualI", "S3 QualII", "S4 QualIII", "S5 Liquids/pH",
           "S6 Metals", "Practice Test 1", "S7 Hair/DNA", "S8 Fibers/Chrom",
           "S9 Plastics", "S10 Blood", "Practice Test 2", "S11 Spatter/Glass",
           "S12 Soil/Prints", "Practice Test 3"]

PAGE = landscape(letter)              # 792 x 612
W, H = PAGE
ML, MR = 34, 34
NAME_W = 168
GRID_X = ML + NAME_W
COL_W = (W - MR - GRID_X) / len(DATES)
ROW_H = 40
HDR_H = 24
ACCENT = HexColor("#1F3A5F")  # navy, distinct from the Disease Detectives teal

c = canvas.Canvas(OUT, pagesize=PAGE)
c.setTitle("Crime Busters Practice Attendance Sign-Up 2026-27 (fillable)")
form = c.acroForm


def page(title, subtitle, row_labels, field_prefix):
    c.setFillColor(black)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(ML, H - 40, "Crime Busters Attendance Sign-Up  —  2026–27")
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(ACCENT)
    c.drawString(ML, H - 58, title)
    c.setFont("Helvetica", 9)
    c.setFillColor(HexColor("#333333"))
    c.drawString(ML, H - 72, subtitle)

    y = H - 88
    c.setFillColor(ACCENT)
    c.rect(ML, y - HDR_H, W - ML - MR, HDR_H, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(ML + 5, y - HDR_H + 8, "Name")
    c.setFont("Helvetica-Bold", 8)
    for i, d in enumerate(DATES):
        c.drawCentredString(GRID_X + i * COL_W + COL_W / 2, y - HDR_H + 8, d)
    y -= HDR_H

    for r, label in enumerate(row_labels):
        ry = y - (r + 1) * ROW_H
        c.setStrokeColor(HexColor("#999999"))
        c.setLineWidth(0.6)
        c.rect(ML, ry, W - ML - MR, ROW_H, fill=0, stroke=1)
        c.setStrokeColor(HexColor("#bbbbbb"))
        c.setLineWidth(0.4)
        c.line(GRID_X, ry, GRID_X, ry + ROW_H)
        c.setFillColor(black)
        c.setFont("Helvetica", 9)
        c.drawString(ML + 5, ry + ROW_H / 2 - 3, label)
        for i in range(len(DATES)):
            cx = GRID_X + i * COL_W
            if i:
                c.line(cx, ry, cx, ry + ROW_H)
            form.checkbox(
                name=f"{field_prefix}_{r}_{i}",
                x=cx + COL_W / 2 - 7, y=ry + ROW_H / 2 - 7,
                size=14, borderWidth=1,
                borderColor=HexColor("#555555"), fillColor=white, checked=False,
            )

    c.setFont("Helvetica", 7.5)
    c.setFillColor(HexColor("#555555"))
    half = 8
    line1 = "   ".join(f"{d} = {l}" for d, l in zip(DATES[:half], LESSONS[:half]))
    line2 = "   ".join(f"{d} = {l}" for d, l in zip(DATES[half:], LESSONS[half:]))
    c.drawString(ML, 30, line1)
    c.drawString(ML, 20, line2)
    c.showPage()


page("Students — click a box for every date you can attend",
     "One row per student. Save the file when you're done so your checks stick.",
     STUDENTS, "stu")

page("Parents / Guardians — we need one parent on site every practice",
     "Type your name over the underline, then check the dates you can be the on-site parent (in addition to the two coaches).",
     [f"________________   (parent of {s.split()[0]})" for s in STUDENTS], "par")

c.save()
print("wrote", OUT, os.path.getsize(OUT), "bytes")
