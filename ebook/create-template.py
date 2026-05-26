#!/usr/bin/env python3
"""
Create custom Pandoc reference DOCX template for SwiftUI Zero to Expert e-book.

Modifies the default Pandoc reference.docx with custom styles:
- Heading 1-4 with branded colors and spacing
- Body text with Georgia 11pt, 1.3 line spacing
- A4 page size with 2.5cm margins
- Code block styling (if style exists)
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
REFERENCE_PATH = os.path.join(TEMPLATE_DIR, "reference.docx")

# Colors
DARK_PRIMARY = RGBColor(0x1A, 0x1A, 0x2E)    # #1a1a2e
DARK_SECONDARY = RGBColor(0x2D, 0x2D, 0x44)  # #2d2d44
BLACK = RGBColor(0x00, 0x00, 0x00)


def set_page_setup(doc):
    """Set A4 page size and 2.5cm margins on all sections."""
    for section in doc.sections:
        section.page_width = Cm(21)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)


def set_page_break_before(style):
    """Set page break before on a paragraph style."""
    pPr = style.paragraph_format._element.get_or_add_pPr()
    page_break = OxmlElement("w:pageBreakBefore")
    page_break.set(qn("w:val"), "true")
    pPr.append(page_break)


def style_heading_1(doc):
    """Heading 1: 24pt, bold, #1a1a2e, page break before, space after 12pt."""
    style = doc.styles["Heading 1"]
    font = style.font
    font.size = Pt(24)
    font.bold = True
    font.color.rgb = DARK_PRIMARY
    font.name = "Georgia"

    pf = style.paragraph_format
    pf.space_after = Pt(12)
    pf.space_before = Pt(0)

    set_page_break_before(style)


def style_heading_2(doc):
    """Heading 2: 18pt, bold, #2d2d44, space before 18pt, space after 8pt."""
    style = doc.styles["Heading 2"]
    font = style.font
    font.size = Pt(18)
    font.bold = True
    font.color.rgb = DARK_SECONDARY
    font.name = "Georgia"

    pf = style.paragraph_format
    pf.space_before = Pt(18)
    pf.space_after = Pt(8)


def style_heading_3(doc):
    """Heading 3: 14pt, bold, space before 12pt, space after 6pt."""
    style = doc.styles["Heading 3"]
    font = style.font
    font.size = Pt(14)
    font.bold = True
    font.color.rgb = BLACK
    font.name = "Georgia"

    pf = style.paragraph_format
    pf.space_before = Pt(12)
    pf.space_after = Pt(6)


def style_heading_4(doc):
    """Heading 4: 12pt, bold, space before 10pt, space after 4pt."""
    style = doc.styles["Heading 4"]
    font = style.font
    font.size = Pt(12)
    font.bold = True
    font.color.rgb = BLACK
    font.name = "Georgia"

    pf = style.paragraph_format
    pf.space_before = Pt(10)
    pf.space_after = Pt(4)


def style_body_text(doc):
    """Normal/Body Text: 11pt Georgia, line spacing 1.3."""
    # Style the Normal style
    style = doc.styles["Normal"]
    font = style.font
    font.size = Pt(11)
    font.name = "Georgia"
    font.color.rgb = BLACK

    pf = style.paragraph_format
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.line_spacing = 1.3

    # Also style Body Text if it exists
    try:
        body_style = doc.styles["Body Text"]
        body_font = body_style.font
        body_font.size = Pt(11)
        body_font.name = "Georgia"
        body_font.color.rgb = BLACK

        body_pf = body_style.paragraph_format
        body_pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        body_pf.line_spacing = 1.3
    except KeyError:
        pass

    # Also style First Paragraph if it exists (Pandoc uses this)
    try:
        fp_style = doc.styles["First Paragraph"]
        fp_font = fp_style.font
        fp_font.size = Pt(11)
        fp_font.name = "Georgia"
        fp_font.color.rgb = BLACK

        fp_pf = fp_style.paragraph_format
        fp_pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        fp_pf.line_spacing = 1.3
    except KeyError:
        pass


def style_code_blocks(doc):
    """Source Code / Verbatim Char: 9pt Courier New (if style exists)."""
    code_style_names = [
        "Source Code",
        "Verbatim Char",
        "Source Code Char",
    ]

    for name in code_style_names:
        try:
            style = doc.styles[name]
            style.font.name = "Courier New"
            style.font.size = Pt(9)
            print(f"  Styled '{name}': 9pt Courier New")
        except KeyError:
            print(f"  Style '{name}' not found, skipping")


def main():
    print(f"Loading reference template: {REFERENCE_PATH}")

    if not os.path.exists(REFERENCE_PATH):
        print("ERROR: reference.docx not found! Generate it first with:")
        print("  pandoc -o ebook/templates/reference.docx --print-default-data-file reference.docx")
        return

    doc = Document(REFERENCE_PATH)

    print("Applying custom styles...")

    print("  Setting A4 page size with 2.5cm margins")
    set_page_setup(doc)

    print("  Styling Heading 1: 24pt bold #1a1a2e, page break before")
    style_heading_1(doc)

    print("  Styling Heading 2: 18pt bold #2d2d44")
    style_heading_2(doc)

    print("  Styling Heading 3: 14pt bold")
    style_heading_3(doc)

    print("  Styling Heading 4: 12pt bold")
    style_heading_4(doc)

    print("  Styling body text: 11pt Georgia, 1.3 line spacing")
    style_body_text(doc)

    print("  Checking code block styles...")
    style_code_blocks(doc)

    doc.save(REFERENCE_PATH)
    print(f"\nTemplate saved: {REFERENCE_PATH}")

    # Print all available styles for reference
    print("\nAll styles in template:")
    for style in doc.styles:
        print(f"  - {style.name} ({style.type})")


if __name__ == "__main__":
    main()
