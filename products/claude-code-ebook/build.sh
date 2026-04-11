#!/usr/bin/env bash
set -euo pipefail

# ─── Config ───────────────────────────────────────────────────────────────────
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$DIR/src"
CSS="$DIR/ebook.css"
MD_OUT="$DIR/mastering-claude-code.md"
HTML_OUT="$DIR/mastering-claude-code.html"
PDF_OUT="$DIR/mastering-claude-code.pdf"
ZIP_OUT="$DIR/mastering-claude-code.zip"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# ─── Helpers ──────────────────────────────────────────────────────────────────
info()  { echo "  → $*"; }
ok()    { echo "  ✓ $*"; }
fail()  { echo "  ✗ $*" >&2; exit 1; }

# ─── Build steps ──────────────────────────────────────────────────────────────

build_md() {
  info "Concatenating source files..."
  # Gather files in numeric order (00 through 20)
  local files
  files=$(ls "$SRC_DIR"/*.md 2>/dev/null | sort) || fail "No .md files found in $SRC_DIR"
  > "$MD_OUT"
  local count=0
  for f in $files; do
    cat "$f" >> "$MD_OUT"
    printf "\n\n" >> "$MD_OUT"
    count=$((count + 1))
  done
  ok "Combined $count file(s) → mastering-claude-code.md"
}

build_html() {
  build_md
  info "Running pandoc → HTML..."
  command -v pandoc &>/dev/null || fail "pandoc not found — install with: brew install pandoc"
  pandoc "$MD_OUT" \
    --standalone \
    --toc \
    --toc-depth=2 \
    --embed-resources \
    --css="$CSS" \
    --metadata title="Mastering Claude Code" \
    --from markdown \
    --to html5 \
    -o "$HTML_OUT"
  ok "HTML generated → mastering-claude-code.html"
}

build_pdf() {
  build_html
  info "Running Chrome headless → PDF..."
  [[ -f "$CHROME" ]] || fail "Chrome not found at: $CHROME"
  "$CHROME" \
    --headless=new \
    --no-pdf-header-footer \
    --print-to-pdf="$PDF_OUT" \
    --print-to-pdf-no-header \
    --no-margins \
    --run-all-compositor-stages-before-draw \
    --disable-gpu \
    "file://$HTML_OUT" 2>/dev/null
  ok "PDF generated → mastering-claude-code.pdf"
}

build_zip() {
  build_pdf
  info "Creating ZIP bundle..."
  cd "$DIR"
  zip -r "$ZIP_OUT" \
    mastering-claude-code.pdf \
    mastering-claude-code.md \
    src/ \
    -x "*.DS_Store"
  ok "ZIP created → mastering-claude-code.zip"
}

# ─── Dispatch ─────────────────────────────────────────────────────────────────
TARGET="${1:-all}"

case "$TARGET" in
  md)   build_md   ;;
  html) build_html ;;
  pdf)  build_pdf  ;;
  zip)  build_zip  ;;
  all)
    echo "Building all targets..."
    build_zip
    echo ""
    echo "Build complete:"
    for f in "$MD_OUT" "$HTML_OUT" "$PDF_OUT" "$ZIP_OUT"; do
      [[ -f "$f" ]] && echo "  $(du -sh "$f" | cut -f1)  $(basename "$f")"
    done
    ;;
  *)
    echo "Usage: $0 [md|html|pdf|zip|all]"
    echo "  md   — concat src/*.md → mastering-claude-code.md"
    echo "  html — md + pandoc → mastering-claude-code.html"
    echo "  pdf  — html + Chrome headless → mastering-claude-code.pdf"
    echo "  zip  — pdf + md + src/ → mastering-claude-code.zip"
    echo "  all  — full pipeline (default)"
    exit 1
    ;;
esac
