# Print-ready PDFs

Print-and-distribute copies of every quiz and homework set, generated from the
Markdown originals in `../quizzes/` and `../homework/`. The Markdown files are the
source of truth — regenerate these PDFs with `tools/build_pdfs.sh` after editing.

Two versions of each:

| File | Contents | Give to |
|---|---|---|
| `<name>.pdf` | **questions only** | the students |
| `<name>_KEY.pdf` | questions **+ answer key** | the coach |

```
pdf/
├── quizzes/     Quiz_01 … Quiz_12   (.pdf + _KEY.pdf)
└── homework/    Homework_01 … Homework_14   (.pdf + _KEY.pdf)
```

Letter size, 0.7" margins. In the `_KEY` version the answer key starts on its own
page, so you can also just print page 1–N of that file if you prefer working from
one document.
