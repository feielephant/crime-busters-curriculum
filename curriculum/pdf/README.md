# Print-ready PDFs

Print-and-distribute copies of the quizzes, homework, and home-lab cards,
generated from the Markdown originals in `../quizzes/`, `../homework/`, and
`../home_labs/`. The Markdown files are the source of truth — regenerate these
PDFs with `tools/build_pdfs.sh` after editing.

Most items come in two versions:

| File | Contents | Give to |
|---|---|---|
| `<name>.pdf` | the hand-out — questions / lab steps only | students & families |
| `<name>_KEY.pdf` | plus the answer key / coach notes | the coach |

```
pdf/
├── quizzes/     Quiz_01 … Quiz_12          (.pdf + _KEY.pdf)
├── homework/    Homework_01 … Homework_14  (.pdf + _KEY.pdf)
└── home_labs/   Lab_02 … Lab_12            (.pdf + _KEY.pdf)
                 Home_Lab_Safety_Agreement.pdf   (single — the form parents sign)
                 Kit_Assembly_Guide.pdf          (single — coach shopping/prep)
```

Letter size, 0.7" margins. In the `_KEY` versions the answer key / coach notes
start on their own page, so you can also just print pages 1–N of that file.
