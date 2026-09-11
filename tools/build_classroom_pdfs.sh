#!/bin/bash
# Regenerate the print-ready PDFs in curriculum/classroom/pdf/ from the Markdown
# originals in curriculum/classroom/.
#
#   Course_Overview.md          -> pdf/Course_Overview.pdf              (portrait)
#   Attendance_Signup.md        -> pdf/Attendance_Signup.pdf           (LANDSCAPE - wide table)
#   syllabi/Class_NN_*.md       -> pdf/syllabi/Class_NN_*.pdf          (portrait, one page each)
#   README.md                   -> pdf/README.pdf                      (portrait)
#
# Requires: pandoc, and Google Chrome (headless) for the HTML->PDF step.
#
# Usage:  bash tools/build_classroom_pdfs.sh          (run from anywhere in the repo)

set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$REPO/curriculum/classroom"
OUT="$SRC/pdf"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

CHROME="${CHROME:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
[ -x "$CHROME" ] || CHROME="$(command -v google-chrome || command -v chromium || true)"
[ -n "$CHROME" ] || { echo "Chrome not found; set \$CHROME to the browser binary."; exit 1; }
command -v pandoc >/dev/null || { echo "pandoc not found; brew install pandoc"; exit 1; }

rm -rf "$OUT"
mkdir -p "$OUT/syllabi"

# ---- shared CSS (portrait) --------------------------------------------------
common_css () {
cat <<'CSS'
* { box-sizing: border-box; }
#title-block-header { display: none; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: "Helvetica Neue", Arial, sans-serif; font-size: 10.5pt; line-height: 1.45; color: #111; margin: 0; max-width: none; }
h1 { font-size: 17pt; margin: 0 0 3pt; border-bottom: 2.5px solid #222; padding-bottom: 5pt; }
h2 { font-size: 12.5pt; margin: 14pt 0 4pt; border-bottom: 1px solid #bbb; padding-bottom: 2pt; page-break-after: avoid; }
h3 { font-size: 11pt; margin: 11pt 0 3pt; page-break-after: avoid; }
p { margin: 4pt 0; }
ul, ol { margin: 4pt 0; padding-left: 20pt; }
li { margin: 2.5pt 0; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 9.3pt; page-break-inside: avoid; }
th, td { border: 1px solid #999; padding: 3pt 5pt; text-align: left; vertical-align: top; }
th { background: #ececec; }
hr { border: none; border-top: 1.5px solid #bbb; margin: 12pt 0; }
blockquote { border-left: 3px solid #0E6E5A; margin: 6pt 0; padding: 3pt 10pt; color: #333; background: #f2f7f5; }
blockquote p { font-style: normal; }
strong { color: #000; }
del { color: #999; }
CSS
}

cat > "$WORK/head-portrait.html" <<CSS
<style>
@page { size: Letter; margin: 0.7in 0.65in; }
$(common_css)
</style>
CSS

cat > "$WORK/head-syllabus.html" <<CSS
<style>
@page { size: Letter; margin: 0.7in 0.7in; }
$(common_css)
body { font-size: 11pt; }
h1 { font-size: 18pt; }
</style>
CSS

# Landscape, small type, tight cells - the 18-date checkbox grid.
cat > "$WORK/head-landscape.html" <<CSS
<style>
@page { size: Letter landscape; margin: 0.45in 0.5in; }
$(common_css)
body { font-size: 9.5pt; }
h1 { font-size: 15pt; }
table { font-size: 8pt; table-layout: fixed; }
th, td { padding: 2pt 2pt; text-align: center; }
th:first-child, td:first-child { text-align: left; width: 150pt; font-size: 8pt; }
td { font-size: 11pt; }
/* the date-key table back to normal */
h3 + table, table:last-of-type { table-layout: auto; font-size: 8.5pt; }
h3 + table td, table:last-of-type td { text-align: left; font-size: 8.5pt; }
</style>
CSS

render () {  # <md> <out.pdf> <head.html>
  local md="$1" pdf="$2" head="$3" base title
  base="$(basename "$pdf" .pdf)"
  title="$(grep -m1 '^# ' "$md" | sed 's/^# //')"
  pandoc "$md" -f gfm -t html5 -s --metadata title="$title" -H "$head" -o "$WORK/$base.html"
  "$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --no-sandbox \
    --print-to-pdf="$pdf" "file://$WORK/$base.html" >/dev/null 2>&1
  echo "  $(basename "$pdf")"
}

render "$SRC/Course_Overview.md"   "$OUT/Course_Overview.pdf"    "$WORK/head-portrait.html"
render "$SRC/Attendance_Signup.md" "$OUT/Attendance_Signup.pdf"  "$WORK/head-landscape.html"
render "$SRC/README.md"            "$OUT/README.pdf"             "$WORK/head-portrait.html"

for md in "$SRC"/syllabi/*.md; do
  base="$(basename "$md" .md)"
  render "$md" "$OUT/syllabi/$base.pdf" "$WORK/head-syllabus.html"
done

# The fillable sign-up (real AcroForm checkboxes) lives in $OUT too but is built by a
# separate reportlab script, not this pandoc/Chrome pipeline - regenerate it here so a
# full rebuild never silently deletes it (this script's `rm -rf "$OUT"` above would).
python3 "$REPO/tools/build_fillable_signup.py"

echo "Done -> $OUT"
