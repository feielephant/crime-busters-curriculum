# Google Classroom — posting materials

Mirrors the sibling `Disease-Detectives-Curriculum` repo's `curriculum/classroom/` setup.
Everything here is written to be posted to Google Classroom for the Crime Busters students
and parents.

## Setup status

As of 2026-09-12, everything lives in the **official school-created Google Classroom Drive
folder**, `Classroom/Crime Busters CRIME` (migrated there from an earlier personal
`CrimeBuster 2026-2027` folder — same file/folder IDs, so all links below kept working
across the move). `Syllabus/`, `Homework /`, `Homework upload/`, and `quiz and answer key/`
live directly inside it, along with the calendar, course overview, and both sign-up sheets.

**Done:** `CLASSROOM_DRIVE_URL`, `HOMEWORK_ASSIGNMENTS_URL`, `HOMEWORK_SUBMIT_URL`,
`SYLLABUS_URL`, `QUIZ_URL`, `STUDENT_SIGNUP_URL`, and `PARENT_SIGNUP_URL` are all real values
in `tools/_team_roster.py` now — not placeholders.

**Still open:**
1. **Confirm the practice location** — currently assumed to be Ocean Air PTA Room (same as
   the Disease Detectives team, same coach) but not actually confirmed. Fix the `LOCATION`
   constant in `tools/_team_roster.py` if wrong.
2. **Confirm the tournament dates** — the calendar currently assumes Crime Busters attends the
   exact same 4 tournaments as the Disease Detectives team (same Division B competitions
   likely host both events, but this hasn't been confirmed). Fix `TOURNAMENTS_OVERVIEW` in
   `tools/_team_roster.py` and the `TOURNAMENTS` list in `tools/build_calendar.py` if wrong.
3. **Clean up two orphaned duplicate Sheets** left behind in the old `CrimeBuster 2026-2027`
   folder (`parents_signup (1).gsheet` and `parents_signup (2).gsheet`) — extra Sheets created
   from repeat CSV imports, not referenced anywhere; safe to delete after a quick look, or keep
   if either turns out to have real data in it.

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
- `tools/sync_to_drive.sh` — copies anything new/changed into the mapped `Crime Busters CRIME`
  Drive folder (see the repo's `CLAUDE.md`)
