# Google Classroom — posting materials

Mirrors the sibling `Disease-Detectives-Curriculum` repo's `curriculum/classroom/` setup.
Everything here is written to be posted to Google Classroom for the Crime Busters students
and parents.

## Still needs the coach to do (placeholders in the generated files until then)

Unlike Disease Detectives, this team's Drive/Sheets/Classroom infrastructure is brand new —
these still need to be created, then the placeholder URLs below need to be filled in:

1. **Get the shareable link** for the `CrimeBuster 2026-2027` Drive folder (already created,
   with `Syllabus/`, `Homework /`, `Homework upload/`, and `quiz and answer key/` subfolders
   inside it) — right-click the folder in Drive → Share → copy link. Put it in
   `CLASSROOM_DRIVE_URL` in `tools/_team_roster.py`.
2. **Create two Google Sheets** for attendance sign-up (student + parent). The PDF sign-up
   didn't work out, so skip that — `students_signup.csv` and `parents_signup.csv` are already
   sitting at the top level of the `CrimeBuster 2026-2027` Drive folder: right-click each →
   **Open with → Google Sheets** → **File → Save as Google Sheets** → select the `FALSE` cells
   → **Insert → Checkbox** → **Share → Anyone with the link → Editor**. Put the two resulting
   links in `STUDENT_SIGNUP_URL` / `PARENT_SIGNUP_URL` in `tools/_team_roster.py`.
3. **Get a shareable link for `Homework /`** (assignments, read-only) and for
   `Homework upload/` (submissions) specifically, and put them in
   `HOMEWORK_ASSIGNMENTS_URL` / `HOMEWORK_SUBMIT_URL` in `tools/_team_roster.py`.
4. **Confirm the practice location** — currently "TBD - same location as Disease Detectives?
   confirm" — fix the `LOCATION` constant in `tools/_team_roster.py`.
5. **Confirm the tournament dates** — the calendar currently assumes Crime Busters attends the
   exact same 4 tournaments as the Disease Detectives team (same Division B competitions
   likely host both events, but this hasn't been confirmed). Fix `TOURNAMENTS_OVERVIEW` in
   `tools/_team_roster.py` and the `TOURNAMENTS` list in `tools/build_calendar.py` if wrong.

**All of the real data above (`tools/_team_roster.py`) is gitignored — this repo is public.**
If it's ever missing (fresh clone, new machine), recreate it; the required shape is at the top
of `tools/gen_classroom_docs.py`'s import.

After filling those in, regenerate everything:
```
python3 tools/gen_classroom_docs.py
python3 tools/build_calendar.py
bash tools/build_classroom_pdfs.sh
bash tools/sync_to_drive.sh
```

## Files

| File | What it is |
|---|---|
| `Course_Overview.md` (+ PDF) | The whole season on one page — roster, all 15 class dates, tournaments (assumed), pacing |
| `google_sheets_import/students.csv`, `parents.csv` | Sign-up tables, synced as `students_signup.csv`/`parents_signup.csv` to the top of the Drive folder, ready to become a live Google Sheet (see step 2 above). **The PDF sign-up (`Attendance_Signup.md`/`.pdf`/`_fillable.pdf`) is generated but not synced or used — it didn't work out for this team.** |
| `CrimeBusters_Schedule.ics` | Calendar file — all 15 classes (with homework + links, once filled in) + 15 "2 days before" reminders + the 4 assumed tournaments |
| `syllabi/Class_01…Class_15` (+ PDFs) | One-page syllabus per class |

## Keeping it up to date

The Markdown files here are the source of truth. Regenerate with:
- `tools/build_classroom_pdfs.sh` — Course Overview, sign-up sheet, and the 15 syllabus PDFs
- `tools/build_fillable_signup.py` — the fillable-checkbox PDF
- `tools/build_calendar.py` — `CrimeBusters_Schedule.ics`
- `tools/sync_to_drive.sh` — copies anything new/changed into the mapped `CrimeBuster 2026-2027`
  Drive folder (see the repo's `CLAUDE.md`)
