#!/usr/bin/env bash
#
# build-ebook.sh — Compile 100 SwiftUI articles into DOCX and PDF
#
# Usage: ./ebook/build-ebook.sh
#
set -euo pipefail

# ── Paths ────────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$SCRIPT_DIR/build"
OUTPUT_DIR="$SCRIPT_DIR/output"
TEMPLATE="$SCRIPT_DIR/templates/reference.docx"

ARTICLES_DONE="$HOME/Documents/14_Web-projects/00-medium-article-or-blog/swiftui-mastery-series/00-Done"
ARTICLES_REST="$HOME/Documents/14_Web-projects/00-medium-article-or-blog/swiftui-mastery-series"

FRONT_MATTER="$BUILD_DIR/00-front-matter.md"
BACK_MATTER="$BUILD_DIR/99-back-matter.md"
PART_INTROS="$BUILD_DIR/part-intros.md"
COMBINED="$BUILD_DIR/combined.md"

OUTPUT_NAME="SwiftUI-Zero-to-Expert"

# ── Pre-flight checks ───────────────────────────────────────────────────────
echo "=== SwiftUI Zero to Expert — E-book Build ==="
echo ""

for f in "$FRONT_MATTER" "$BACK_MATTER" "$PART_INTROS" "$TEMPLATE"; do
    if [[ ! -f "$f" ]]; then
        echo "ERROR: Missing required file: $f"
        exit 1
    fi
done

if ! command -v pandoc &>/dev/null; then
    echo "ERROR: pandoc is not installed. Run: brew install pandoc"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

# ── Parse part intros into an associative array ──────────────────────────────
# Part intros are separated by \newpage in part-intros.md
# Parts map to chapter numbers: 1, 16, 31, 46, 61, 76, 91
PART_BOUNDARIES=(1 16 31 46 61 76 91)

declare -a PART_INTRO_TEXTS
current_part=0
current_text=""

while IFS= read -r line; do
    if [[ "$line" == '\newpage' ]]; then
        if [[ -n "$current_text" ]]; then
            PART_INTRO_TEXTS[$current_part]="$current_text"
            ((current_part++))
        fi
        current_text=""
    else
        current_text+="$line"$'\n'
    fi
done < "$PART_INTROS"

# Capture any trailing text (in case the file doesn't end with \newpage)
if [[ -n "$current_text" ]]; then
    PART_INTRO_TEXTS[$current_part]="$current_text"
fi

echo "Loaded ${#PART_INTRO_TEXTS[@]} part intros."

# ── Function: clean an article ───────────────────────────────────────────────
# 1. Strip series reference line (line 3: *Part X of 100 ...*)
# 2. Strip the --- separator after it (line 5)
# 3. Strip footer lines (--- + *Follow...* + *Next up...* + #hashtags)
# 4. Shift headings: # → ##, ## → ###, ### → #### (outside code blocks)
# 5. Convert H1 (title) to H2 (chapter title)
clean_article() {
    local file="$1"

    awk '
    BEGIN {
        in_code_block = 0
        line_num = 0
        # We collect all lines first, then strip footer from the end
    }
    {
        lines[NR] = $0
        total = NR
    }
    END {
        # --- Strip footer from the end ---
        # Find where footer starts: look backwards for the --- separator
        footer_start = total + 1  # default: no footer

        for (i = total; i >= 1 && i >= total - 15; i--) {
            # Look for the --- line near the end that starts the footer
            if (lines[i] == "---") {
                # Check if lines after it look like footer content
                is_footer = 0
                for (j = i + 1; j <= total; j++) {
                    if (lines[j] ~ /^\*.*\*$/ || lines[j] ~ /^#[A-Z]/ || lines[j] ~ /^$/) {
                        is_footer = 1
                    }
                }
                if (is_footer) {
                    footer_start = i
                    break
                }
            }
        }

        # Also strip trailing blank lines before the footer
        content_end = footer_start - 1
        while (content_end >= 1 && lines[content_end] ~ /^[[:space:]]*$/) {
            content_end--
        }

        # --- Process lines 1 to content_end ---
        in_code = 0
        for (i = 1; i <= content_end; i++) {
            line = lines[i]

            # Skip series reference (line 3): *Part X of 100 in the SwiftUI...*
            if (i == 3 && line ~ /^\*Part [0-9]+ of 100/) {
                continue
            }

            # Skip the blank line after series ref (line 4) and --- separator (line 5)
            if (i == 4 && line ~ /^[[:space:]]*$/) {
                continue
            }
            if (i == 5 && line == "---") {
                continue
            }

            # Skip the blank line after --- (line 6)
            if (i == 6 && line ~ /^[[:space:]]*$/) {
                continue
            }

            # Track code blocks
            if (line ~ /^```/) {
                in_code = !in_code
                print line
                continue
            }

            # Shift headings only outside code blocks
            if (!in_code) {
                # Shift ### → #### (do this first to avoid double-shifting)
                if (line ~ /^### [^#]/) {
                    sub(/^### /, "#### ", line)
                }
                # Shift ## → ###
                else if (line ~ /^## [^#]/) {
                    sub(/^## /, "### ", line)
                }
                # Shift # → ## (the title)
                else if (line ~ /^# [^#]/) {
                    sub(/^# /, "## ", line)
                }
            }

            print line
        }
    }
    ' "$file"
}

# ── Function: resolve article file path ──────────────────────────────────────
find_article() {
    local num="$1"
    local padded

    if [[ "$num" -eq 100 ]]; then
        padded="100"
    else
        padded=$(printf "%02d" "$num")
    fi

    # Look in 00-Done first (articles 1-73), then in main folder (74-100)
    local match
    match=$(find "$ARTICLES_DONE" -maxdepth 1 -name "${padded}-*.md" 2>/dev/null | head -1)
    if [[ -n "$match" ]]; then
        echo "$match"
        return
    fi

    match=$(find "$ARTICLES_REST" -maxdepth 1 -name "${padded}-*.md" 2>/dev/null | head -1)
    if [[ -n "$match" ]]; then
        echo "$match"
        return
    fi

    echo ""
}

# ── Build combined markdown ──────────────────────────────────────────────────
echo ""
echo "Building combined markdown..."

# Start with front matter
cat "$FRONT_MATTER" > "$COMBINED"

part_index=0
missing_count=0

for num in $(seq 1 100); do
    # Insert part intro at boundary chapters
    if [[ $part_index -lt ${#PART_BOUNDARIES[@]} ]] && [[ "$num" -eq "${PART_BOUNDARIES[$part_index]}" ]]; then
        echo "" >> "$COMBINED"
        echo "\\newpage" >> "$COMBINED"
        echo "" >> "$COMBINED"
        echo "${PART_INTRO_TEXTS[$part_index]}" >> "$COMBINED"
        ((part_index++))
    fi

    # Find article file
    article_path=$(find_article "$num")

    if [[ -z "$article_path" ]]; then
        echo "  WARNING: Article $num not found — skipping"
        ((missing_count++))
        continue
    fi

    echo "  Processing article $num: $(basename "$article_path")"

    # Add page break before chapter
    echo "" >> "$COMBINED"
    echo "\\newpage" >> "$COMBINED"
    echo "" >> "$COMBINED"

    # Clean and append article
    clean_article "$article_path" >> "$COMBINED"
done

# Append back matter
echo "" >> "$COMBINED"
cat "$BACK_MATTER" >> "$COMBINED"

echo ""
echo "Combined markdown: $COMBINED"
if [[ $missing_count -gt 0 ]]; then
    echo "WARNING: $missing_count articles were missing!"
fi

# ── Generate DOCX with Pandoc ────────────────────────────────────────────────
echo ""
echo "Generating DOCX with Pandoc..."

pandoc "$COMBINED" \
    -o "$OUTPUT_DIR/$OUTPUT_NAME.docx" \
    --reference-doc="$TEMPLATE" \
    --toc \
    --toc-depth=2 \
    --number-sections \
    -f markdown \
    --wrap=none

echo "DOCX: $OUTPUT_DIR/$OUTPUT_NAME.docx"

# ── Generate PDF with LibreOffice ────────────────────────────────────────────
SOFFICE="/Applications/LibreOffice.app/Contents/MacOS/soffice"

if [[ -x "$SOFFICE" ]]; then
    echo ""
    echo "Generating PDF with LibreOffice..."

    "$SOFFICE" \
        --headless \
        --convert-to pdf \
        --outdir "$OUTPUT_DIR" \
        "$OUTPUT_DIR/$OUTPUT_NAME.docx"

    echo "PDF: $OUTPUT_DIR/$OUTPUT_NAME.pdf"
else
    echo ""
    echo "WARNING: LibreOffice not found at $SOFFICE"
    echo "Skipping PDF generation. Install LibreOffice to enable PDF output."
    echo "  brew install --cask libreoffice"
fi

# ── Done ─────────────────────────────────────────────────────────────────────
echo ""
echo "=== Build complete ==="
echo "  DOCX: $OUTPUT_DIR/$OUTPUT_NAME.docx"
if [[ -f "$OUTPUT_DIR/$OUTPUT_NAME.pdf" ]]; then
    echo "  PDF:  $OUTPUT_DIR/$OUTPUT_NAME.pdf"
fi
