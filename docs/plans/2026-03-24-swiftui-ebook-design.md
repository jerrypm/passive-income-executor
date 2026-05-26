# SwiftUI Zero to Expert — E-book Design

## Overview
Convert the 100-article "SwiftUI Zero to Expert" series into a professional e-book in 2 formats (PDF + DOCX) for selling on Gumroad.

## Decisions
- **Scope:** Single e-book, all 100 articles
- **Format:** Proper book format (preface, about author, TOC, part intros, conclusion)
- **Tooling:** Pandoc + custom DOCX reference template
- **Title:** SwiftUI Zero to Expert
- **Author:** JR Dev Hub
- **Code styling:** Simple monospace with gray background

## Source
- Path: `~/Documents/14_Web-projects/00-medium-article-or-blog/swiftui-mastery-series/`
- 73 articles in `00-Done/` (articles 1-73)
- 27 articles in root (articles 74-100)
- ~68,000 lines total, estimated 400-500 pages

## Book Structure

```
SwiftUI Zero to Expert
├── Title Page
├── About the Author
├── Table of Contents (auto-generated)
├── Preface
├── Part 1: SwiftUI Fundamentals (Ch 1-15)
├── Part 2: Layouts & UI Components (Ch 16-30)
├── Part 3: State Management & Data Flow (Ch 31-45)
├── Part 4: Navigation & Architecture (Ch 46-60)
├── Part 5: Networking & Persistence (Ch 61-75)
├── Part 6: Advanced SwiftUI & Clean Code (Ch 76-90)
├── Part 7: Expert Level & Production Apps (Ch 91-100)
├── Conclusion & What's Next
└── (Cover — added manually in DOCX)
```

## Build Pipeline

### Script: `scripts/build-ebook.sh`

```
1. Collect all 100 .md files (sorted by number)
2. Generate front matter (title page, about, preface)
3. Generate part intro pages (7x)
4. Generate back matter (conclusion)
5. Concatenate into 1 combined .md
6. Clean up (strip series refs, social tags, normalize headings)
7. Pandoc → DOCX (using reference template)
8. Pandoc → PDF (via LibreOffice CLI from DOCX)
```

### Dependencies
- Pandoc: `brew install pandoc`
- LibreOffice (headless, DOCX→PDF): `brew install --cask libreoffice`

### Reference Template
- `templates/reference.docx` — predefined styles:
  - Heading 1 = Part title (page break before)
  - Heading 2 = Chapter title
  - Heading 3 = Section
  - Body Text = 11-12pt readable font
  - Code Block = Monospace, gray background
  - Page size = A4

### Content Cleanup
1. Strip `*Part X of 100 in the SwiftUI Zero to Expert Series*`
2. Strip social hashtags at end of articles
3. Normalize heading levels (H1 → H2 for chapters)
4. Keep code blocks and image refs as-is

### Front & Back Matter
- **Preface** (~150 words): target reader, how to use, overview
- **About the Author** (~50 words): JR Dev Hub, iOS & Web Dev
- **Part Intros** (~50 words each): overview per part
- **Conclusion** (~100 words): recap, next steps

### Output
```
output/
├── SwiftUI-Zero-to-Expert.docx
└── SwiftUI-Zero-to-Expert.pdf
```

## Estimate
- DOCX: ~2-5MB
- PDF: ~3-8MB
- 400-500 pages
