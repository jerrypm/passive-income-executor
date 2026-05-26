# SwiftUI E-book Build System — Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a script that compiles 100 SwiftUI articles into a professional e-book (DOCX + PDF) for Gumroad.

**Architecture:** Shell script collects and cleans markdown files, generates front/back matter, then uses Pandoc + DOCX reference template to produce output. LibreOffice CLI converts DOCX→PDF.

**Tech Stack:** Bash, Pandoc, LibreOffice (headless), sed/awk for cleanup

---

### Task 1: Install Dependencies

**Step 1: Install Pandoc**

Run: `brew install pandoc`
Expected: Pandoc installed successfully

**Step 2: Verify Pandoc**

Run: `pandoc --version | head -1`
Expected: `pandoc X.X.X`

**Step 3: Verify LibreOffice**

Run: `ls /Applications/LibreOffice.app`
Expected: LibreOffice already installed (confirmed)

**Step 4: Commit — N/A (no code changes)**

---

### Task 2: Create Directory Structure

**Files:**
- Create: `ebook/templates/` (directory)
- Create: `ebook/output/` (directory)
- Create: `ebook/build/` (directory, temp files during build)

**Step 1: Create directories**

```bash
mkdir -p ebook/{templates,output,build}
```

**Step 2: Add .gitkeep and update .gitignore**

Create `ebook/output/.gitkeep` (empty)
Create `ebook/build/.gitkeep` (empty)

Add to `.gitignore`:
```
ebook/build/*.md
ebook/output/*.docx
ebook/output/*.pdf
```

**Step 3: Commit**

```bash
git add ebook/ .gitignore
git commit -m "chore: add ebook directory structure"
```

---

### Task 3: Create Pandoc Reference DOCX Template

**Files:**
- Create: `ebook/templates/reference.docx`

**Step 1: Generate default Pandoc reference**

```bash
pandoc -o ebook/templates/reference.docx --print-default-data-file reference.docx
```

**Step 2: Modify template styles via Python script**

Create `ebook/create-template.py` — a one-time script that modifies the reference.docx styles:
- Heading 1: 24pt, bold, page break before (Part titles)
- Heading 2: 18pt, bold (Chapter titles)
- Heading 3: 14pt, bold (Sections)
- Body Text / Normal: 11pt, line spacing 1.3
- Code: 10pt Courier New, background #f0f0f0, border
- Page: A4, margins 2.5cm

```python
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document('ebook/templates/reference.docx')

# Modify styles
for style in doc.styles:
    if style.name == 'Heading 1':
        style.font.size = Pt(24)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0x1a, 0x1a, 0x2e)
        style.paragraph_format.page_break_before = True
        style.paragraph_format.space_after = Pt(12)
    elif style.name == 'Heading 2':
        style.font.size = Pt(18)
        style.font.bold = True
        style.font.color.rgb = RGBColor(0x2d, 0x2d, 0x44)
        style.paragraph_format.space_before = Pt(18)
        style.paragraph_format.space_after = Pt(8)
    elif style.name == 'Heading 3':
        style.font.size = Pt(14)
        style.font.bold = True
        style.paragraph_format.space_before = Pt(12)
        style.paragraph_format.space_after = Pt(6)
    elif style.name == 'Normal':
        style.font.size = Pt(11)
        style.font.name = 'Georgia'
        style.paragraph_format.line_spacing = 1.3

# Set page size to A4
for section in doc.sections:
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)

doc.save('ebook/templates/reference.docx')
```

Run: `pip install python-docx && python ebook/create-template.py`
Expected: `reference.docx` updated with custom styles

**Step 3: Verify by opening template**

Run: `open ebook/templates/reference.docx`
Expected: Can see styled headings in Word/Pages

**Step 4: Commit**

```bash
git add ebook/templates/reference.docx ebook/create-template.py
git commit -m "feat: add DOCX reference template with custom styles"
```

---

### Task 4: Create Front Matter Markdown

**Files:**
- Create: `ebook/build/00-front-matter.md`

**Step 1: Write front matter content**

```markdown
---
title: "SwiftUI Zero to Expert"
author: "JR Dev Hub"
date: "2026"
---

\newpage

# About the Author

**JR Dev Hub** is an iOS and Web Developer from Indonesia with a passion for building clean, maintainable applications. Through years of hands-on experience with Swift and SwiftUI, JR Dev Hub shares practical knowledge to help developers at every level master Apple's modern UI framework.

Connect and follow for more content at jrdevhub.com

\newpage

# Preface

Welcome to **SwiftUI Zero to Expert** — a comprehensive guide that takes you from your very first SwiftUI view to building production-ready applications.

This book is organized into **7 parts** with **100 chapters**, designed to be read sequentially if you're a beginner, or used as a reference guide if you're more experienced:

- **Part 1 (Ch 1-15):** SwiftUI Fundamentals — the building blocks
- **Part 2 (Ch 16-30):** Layouts & UI Components — real-world UI patterns
- **Part 3 (Ch 31-45):** State Management & Data Flow — the heart of SwiftUI
- **Part 4 (Ch 46-60):** Navigation & Architecture — structuring real apps
- **Part 5 (Ch 61-75):** Networking & Persistence — connecting to the world
- **Part 6 (Ch 76-90):** Advanced SwiftUI & Clean Code — professional quality
- **Part 7 (Ch 91-100):** Expert Level & Production — shipping to the App Store

Every chapter includes conceptual explanations, practical code examples, and best practices drawn from real-world iOS development.

Let's begin your journey to SwiftUI mastery.

\newpage
```

**Step 2: Commit**

```bash
git add ebook/build/00-front-matter.md
git commit -m "feat: add e-book front matter (title, about, preface)"
```

---

### Task 5: Create Part Intro Pages

**Files:**
- Create: `ebook/build/part-intros.md` (7 part intro snippets, inserted during build)

**Step 1: Write part intro content**

Each part intro is an H1 heading + short description + page break.

```markdown
# Part 1: SwiftUI Fundamentals

*Chapters 1–15*

In this section, you'll learn the core building blocks of SwiftUI — from understanding the View protocol and modifiers to mastering layouts, navigation, animations, and gestures. By the end of Part 1, you'll be comfortable building complete screens with SwiftUI.

\newpage

# Part 2: Layouts & UI Components

*Chapters 16–30*

Now that you know the basics, it's time to build real-world UI components. You'll create custom shapes, reusable components, advanced lists, tab bars, onboarding flows, loading states, and bottom sheets — the patterns you'll use in every production app.

\newpage

# Part 3: State Management & Data Flow

*Chapters 31–45*

State is the heart of SwiftUI. In this section, you'll master @State, @Binding, @StateObject, @Observable, and Combine. You'll learn patterns like Redux, TCA, and dependency injection to manage complex state in large applications.

\newpage

# Part 4: Navigation & Architecture

*Chapters 46–60*

Learn to structure real apps with NavigationStack, deep linking, coordinator and router patterns, and proven architectures like MVVM, VIPER, and Clean Architecture. This section transforms you from building screens to building apps.

\newpage

# Part 5: Networking & Persistence

*Chapters 61–75*

Connect your app to the world. Master URLSession, async/await networking, error handling, authentication, caching, and offline support. Then persist data with Core Data, SwiftData, Keychain, and CloudKit.

\newpage

# Part 6: Advanced SwiftUI & Clean Code

*Chapters 76–90*

Level up with performance optimization, memory management, custom animations, Metal shaders, accessibility, localization, unit testing, UI testing, and clean code principles including SOLID and design patterns.

\newpage

# Part 7: Expert Level & Production Apps

*Chapters 91–100*

Ship with confidence. Cover App Store optimization, in-app purchases, analytics, crash reporting, CI/CD, security best practices, performance profiling, production debugging, and build a complete production app from scratch.

\newpage
```

**Step 2: Commit**

```bash
git add ebook/build/part-intros.md
git commit -m "feat: add part intro pages for e-book"
```

---

### Task 6: Create Back Matter Markdown

**Files:**
- Create: `ebook/build/99-back-matter.md`

**Step 1: Write conclusion**

```markdown
\newpage

# Conclusion: Your SwiftUI Journey Continues

Congratulations — you've completed all 100 chapters of **SwiftUI Zero to Expert**.

You started with a simple `Text("Hello, World!")` and now you can build production-ready iOS applications with clean architecture, robust networking, persistent storage, and professional-grade testing.

But this is just the beginning. SwiftUI evolves with every WWDC, and the best way to keep growing is to **build real projects**. Take what you've learned and ship something — whether it's a personal tool, an open-source library, or your first App Store submission.

**Keep building. Keep learning. Keep shipping.**

— JR Dev Hub
```

**Step 2: Commit**

```bash
git add ebook/build/99-back-matter.md
git commit -m "feat: add e-book back matter (conclusion)"
```

---

### Task 7: Build the Main Script

**Files:**
- Create: `ebook/build-ebook.sh`

**Step 1: Write the build script**

```bash
#!/bin/bash
set -euo pipefail

# === CONFIG ===
SERIES_DIR="$HOME/Documents/14_Web-projects/00-medium-article-or-blog/swiftui-mastery-series"
DONE_DIR="$SERIES_DIR/00-Done"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BUILD_DIR="$SCRIPT_DIR/build"
OUTPUT_DIR="$SCRIPT_DIR/output"
TEMPLATE="$SCRIPT_DIR/templates/reference.docx"
COMBINED="$BUILD_DIR/combined.md"
OUTPUT_NAME="SwiftUI-Zero-to-Expert"

echo "=== SwiftUI Zero to Expert — E-book Builder ==="
echo ""

# === STEP 1: Verify source files ===
echo "[1/6] Verifying source files..."
DONE_COUNT=$(ls "$DONE_DIR"/*.md 2>/dev/null | grep -v "00-series-index" | wc -l | tr -d ' ')
ROOT_COUNT=$(ls "$SERIES_DIR"/*.md 2>/dev/null | wc -l | tr -d ' ')
TOTAL=$((DONE_COUNT + ROOT_COUNT))
echo "  Found $DONE_COUNT articles in 00-Done/, $ROOT_COUNT in root ($TOTAL total)"

if [ "$TOTAL" -lt 100 ]; then
    echo "  WARNING: Expected 100 articles, found $TOTAL"
fi

# === STEP 2: Start with front matter ===
echo "[2/6] Assembling front matter..."
cp "$BUILD_DIR/00-front-matter.md" "$COMBINED"
echo "" >> "$COMBINED"

# === STEP 3: Assemble chapters with part intros ===
echo "[3/6] Assembling chapters..."

# Part boundaries: which chapter starts each part
declare -a PART_STARTS=(1 16 31 46 61 76 91)
declare -a PART_NAMES=(
    "Part 1: SwiftUI Fundamentals"
    "Part 2: Layouts & UI Components"
    "Part 3: State Management & Data Flow"
    "Part 4: Navigation & Architecture"
    "Part 5: Networking & Persistence"
    "Part 6: Advanced SwiftUI & Clean Code"
    "Part 7: Expert Level & Production Apps"
)

CURRENT_PART=0

for i in $(seq 1 100); do
    # Check if we need a part intro
    for p in "${!PART_STARTS[@]}"; do
        if [ "$i" -eq "${PART_STARTS[$p]}" ]; then
            CURRENT_PART=$p
            echo "  Inserting ${PART_NAMES[$p]} intro..."
            # Extract the relevant part intro from part-intros.md
            # Each part intro starts with "# Part N:" and ends before next "# Part" or EOF
            PART_NUM=$((p + 1))
            sed -n "/^# Part $PART_NUM:/,/^# Part $((PART_NUM + 1)):/{ /^# Part $((PART_NUM + 1)):/d; p; }" "$BUILD_DIR/part-intros.md" >> "$COMBINED"
            # Handle last part (no next part marker)
            if [ "$PART_NUM" -eq 7 ]; then
                sed -n "/^# Part 7:/,\$p" "$BUILD_DIR/part-intros.md" >> "$COMBINED"
            fi
            echo "" >> "$COMBINED"
        fi
    done

    # Find the article file
    PADDED=$(printf "%02d" "$i")
    # Try 00-Done/ first, then root
    ARTICLE=$(ls "$DONE_DIR"/${PADDED}-*.md 2>/dev/null | head -1)
    if [ -z "$ARTICLE" ]; then
        ARTICLE=$(ls "$SERIES_DIR"/${PADDED}-*.md 2>/dev/null | head -1)
    fi
    # Try without padding (for 100)
    if [ -z "$ARTICLE" ]; then
        ARTICLE=$(ls "$DONE_DIR"/${i}-*.md 2>/dev/null | head -1)
    fi
    if [ -z "$ARTICLE" ]; then
        ARTICLE=$(ls "$SERIES_DIR"/${i}-*.md 2>/dev/null | head -1)
    fi

    if [ -z "$ARTICLE" ]; then
        echo "  WARNING: Article $i not found, skipping"
        continue
    fi

    echo "  Chapter $i: $(basename "$ARTICLE")"

    # Clean and append article
    {
        # Read article, apply cleanups:
        cat "$ARTICLE" | \
            # 1. Strip series reference line
            sed '/^\*Part [0-9]* of 100 in the SwiftUI Zero to Expert Series\*$/d' | \
            # 2. Strip social hashtags at end (lines starting with #SwiftUI or similar tags)
            sed '/^#SwiftUI/d' | \
            sed '/^#iOS/d' | \
            # 3. Strip "Follow me" / "clap" / "Found this helpful" footer lines
            sed '/^\*Follow me for more/d' | \
            sed '/^\*Found this helpful/d' | \
            sed '/^\*Next up:/d' | \
            sed '/^\*Thank you for completing/d' | \
            # 4. Convert H1 to H2 (# Title → ## Title) for chapter titles
            sed 's/^# /## /' | \
            # 5. Shift all sub-headings down one level
            sed 's/^## /### /' | \
            sed 's/^### /#### /'

        # Add page break after each chapter
        echo ""
        echo "\\newpage"
        echo ""
    } >> "$COMBINED"
done

# === STEP 4: Append back matter ===
echo "[4/6] Appending back matter..."
cat "$BUILD_DIR/99-back-matter.md" >> "$COMBINED"

# === STEP 5: Generate DOCX ===
echo "[5/6] Generating DOCX..."
pandoc "$COMBINED" \
    -o "$OUTPUT_DIR/$OUTPUT_NAME.docx" \
    --reference-doc="$TEMPLATE" \
    --toc \
    --toc-depth=2 \
    --number-sections \
    -f markdown \
    --wrap=none

DOCX_SIZE=$(du -h "$OUTPUT_DIR/$OUTPUT_NAME.docx" | cut -f1)
echo "  Created: $OUTPUT_DIR/$OUTPUT_NAME.docx ($DOCX_SIZE)"

# === STEP 6: Generate PDF from DOCX via LibreOffice ===
echo "[6/6] Generating PDF..."
/Applications/LibreOffice.app/Contents/MacOS/soffice \
    --headless \
    --convert-to pdf \
    --outdir "$OUTPUT_DIR" \
    "$OUTPUT_DIR/$OUTPUT_NAME.docx"

PDF_SIZE=$(du -h "$OUTPUT_DIR/$OUTPUT_NAME.pdf" | cut -f1)
echo "  Created: $OUTPUT_DIR/$OUTPUT_NAME.pdf ($PDF_SIZE)"

echo ""
echo "=== BUILD COMPLETE ==="
echo "  DOCX: $OUTPUT_DIR/$OUTPUT_NAME.docx ($DOCX_SIZE)"
echo "  PDF:  $OUTPUT_DIR/$OUTPUT_NAME.pdf ($PDF_SIZE)"
echo ""
echo "Next steps:"
echo "  1. Open DOCX and add your cover page"
echo "  2. Review formatting and adjust if needed"
echo "  3. Upload to Gumroad!"
```

**Step 2: Make executable**

```bash
chmod +x ebook/build-ebook.sh
```

**Step 3: Commit**

```bash
git add ebook/build-ebook.sh
git commit -m "feat: add main e-book build script"
```

---

### Task 8: Run the Build

**Step 1: Run the build script**

```bash
cd /Users/jeripurnamamaulid/Documents/14_Web-projects/passive-income-executor
bash ebook/build-ebook.sh
```

Expected: Both DOCX and PDF generated in `ebook/output/`

**Step 2: Verify output**

```bash
ls -lh ebook/output/
```

Expected: Two files — `SwiftUI-Zero-to-Expert.docx` and `SwiftUI-Zero-to-Expert.pdf`

**Step 3: Quick visual check**

```bash
open ebook/output/SwiftUI-Zero-to-Expert.docx
open ebook/output/SwiftUI-Zero-to-Expert.pdf
```

Expected: Both files open, chapters visible, formatting looks clean

**Step 4: Commit**

```bash
git add ebook/
git commit -m "feat: complete e-book build system for SwiftUI Zero to Expert"
```

---

## Summary

| Task | Description | Est. |
|------|-------------|------|
| 1 | Install Pandoc | 2 min |
| 2 | Create directory structure | 1 min |
| 3 | Create DOCX reference template | 3 min |
| 4 | Create front matter | 2 min |
| 5 | Create part intro pages | 2 min |
| 6 | Create back matter | 1 min |
| 7 | Build main script | 5 min |
| 8 | Run and verify | 3 min |
| **Total** | | **~19 min** |
