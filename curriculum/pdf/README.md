# Print-ready PDFs

Print-and-distribute copies of every quiz and homework set, generated from the
Markdown originals in `../quizzes/` and `../homework/`. The Markdown files are the
source of truth — regenerate these PDFs with `tools/build_pdfs.sh` after editing.

```
pdf/
├── quizzes/     Quiz_01 … Quiz_12  (.pdf)
└── homework/    Homework_01 … Homework_14  (.pdf)
```

**Each PDF contains the answer key on its own page(s) at the end.** When handing a
quiz or homework to a student, print only the question pages (the answer key is
always the last section, starting on a fresh page). A coach-facing "with answers"
copy and a student-facing "questions only" copy can both come from the same file
this way.

Letter size, 0.7" margins.
