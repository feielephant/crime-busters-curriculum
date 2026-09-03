#!/bin/bash
# Regenerate the print-ready PDFs in curriculum/pdf/ from the Markdown originals.
#
#   curriculum/quizzes/   -> pdf/quizzes/    (split at "## Answer Key")
#   curriculum/homework/   -> pdf/homework/   (split at "## Answer Key")
#   curriculum/home_labs/  -> pdf/home_labs/  (Lab_* split at "## Coach notes";
#                                              the safety agreement + kit guide
#                                              are single full PDFs)
#
# For split docs it produces TWO PDFs:
#   <name>.pdf       - hand-out copy: everything before the split heading
#   <name>_KEY.pdf   - full document, including the answer key / coach notes
#
# Requires: pandoc, and Google Chrome (headless).
#   brew install pandoc
#
# Usage:  bash tools/build_pdfs.sh          (run from anywhere in the repo)

set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
CUR="$REPO/curriculum"
OUT="$CUR/pdf"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
[ -x "$CHROME" ] || CHROME="$(command -v google-chrome || command -v chromium || true)"
[ -n "$CHROME" ] || { echo "Chrome not found; set \$CHROME to the browser binary."; exit 1; }
command -v pandoc >/dev/null || { echo "pandoc not found; brew install pandoc"; exit 1; }

rm -rf "$OUT/quizzes" "$OUT/homework" "$OUT/home_labs"
mkdir -p "$OUT/quizzes" "$OUT/homework" "$OUT/home_labs"

cat > "$WORK/head.html" <<'CSS'
<style>
@page { size: Letter; margin: 0.7in 0.65in; }
* { box-sizing: border-box; }
#title-block-header { display: none; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Helvetica Neue", Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #111; margin: 0; max-width: none; }
h1 { font-size: 17pt; margin: 0 0 3pt; border-bottom: 2.5px solid #222; padding-bottom: 5pt; }
h2 { font-size: 12.5pt; margin: 15pt 0 4pt; border-bottom: 1px solid #bbb; padding-bottom: 2pt; page-break-after: avoid; }
h3 { font-size: 11pt; margin: 11pt 0 3pt; page-break-after: avoid; }
p { margin: 4pt 0; }
ul, ol { margin: 4pt 0; padding-left: 20pt; }
li { margin: 2.5pt 0; }
code { font-family: "SF Mono", Consolas, monospace; font-size: 9.5pt; background: #f0f0f0; padding: 0.5pt 3pt; border-radius: 2pt; }
pre { background: #f6f6f6; border: 1px solid #ddd; padding: 6pt 9pt; border-radius: 3pt; font-size: 8.8pt; line-height: 1.35; white-space: pre-wrap; page-break-inside: avoid; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 9.3pt; page-break-inside: avoid; }
th, td { border: 1px solid #999; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #ececec; }
hr { border: none; border-top: 1.5px solid #bbb; margin: 14pt 0; }
blockquote { border-left: 3px solid #ccc; margin: 6pt 0; padding: 2pt 10pt; color: #444; font-style: italic; }
strong { color: #000; }
h2#answer-key, h2#coach-notes { page-break-before: always; }
</style>
CSS

render () {  # <md> <out.pdf>
  local md="$1" pdf="$2" base; base="$(basename "$pdf" .pdf)"
  local title; title="$(grep -m1 '^# ' "$md" | sed 's/^# //')"
  pandoc "$md" -f gfm -t html5 -s --metadata title="$title" -H "$WORK/head.html" -o "$WORK/$base.html"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --no-sandbox \
    --print-to-pdf="$pdf" "file://$WORK/$base.html" >/dev/null 2>&1
}

build_split () {  # <srcdir> <outdir> <split-heading-regex>
  local srcdir="$1" outdir="$2" marker="$3" n=0
  for md in "$srcdir"/*.md; do
    base="$(basename "$md" .md)"
    [ "$base" = "README" ] && continue
    if grep -qE "$marker" "$md"; then
      awk -v m="$marker" '$0 ~ m {exit} {print}' "$md" > "$WORK/$base.student.md"
      render "$WORK/$base.student.md" "$outdir/$base.pdf"
      render "$md"                    "$outdir/${base}_KEY.pdf"
      echo "  $base.pdf  +  ${base}_KEY.pdf"
    else
      render "$md" "$outdir/$base.pdf"
      echo "  $base.pdf"
    fi
    n=$((n+1))
  done
  echo "  ($n source files)"
}

echo "quizzes:";   build_split "$CUR/quizzes"   "$OUT/quizzes"   '^## Answer Key[[:space:]]*$'
echo "homework:";  build_split "$CUR/homework"  "$OUT/homework"  '^## Answer Key[[:space:]]*$'
echo "home_labs:"; build_split "$CUR/home_labs" "$OUT/home_labs" '^## Coach notes[[:space:]]*$'
echo "Done -> $OUT"
