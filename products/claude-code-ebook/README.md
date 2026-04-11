# Mastering Claude Code — Ebook Product

## Product Info

| Field       | Detail |
|-------------|--------|
| Name        | Mastering Claude Code: From Zero to Expert |
| Launch price | **$19** |
| Full price  | $29 (after launch period) |
| Status      | In development — pending final build + upload |
| Gumroad URL | TBD (upload after PDF is built) |

---

## Package Contents

| File / Folder                    | Description                                      |
|----------------------------------|--------------------------------------------------|
| `mastering-claude-code.pdf`      | Final ebook PDF (primary deliverable)            |
| `mastering-claude-code.md`       | Combined Markdown source (all chapters merged)   |
| `src/00-intro.md` … `src/20-*.md`| 20 individual chapter source files               |
| `cover.html`                     | 1280×1600 HTML cover page (pure CSS/JS, no images) |
| `cover.png`                      | Rendered cover PNG (for Gumroad thumbnail)       |
| `ebook.css`                      | Stylesheet used by pandoc → HTML → PDF pipeline  |
| `build.sh`                       | Full build pipeline script                       |

---

## Build Commands

### Full pipeline (md → html → pdf → zip)
```bash
cd products/claude-code-ebook
bash build.sh all
```

### Individual steps
```bash
bash build.sh md     # concat src/*.md → mastering-claude-code.md
bash build.sh html   # md + pandoc → mastering-claude-code.html
bash build.sh pdf    # html + Chrome headless → mastering-claude-code.pdf
bash build.sh zip    # pdf + md + src/ → mastering-claude-code.zip
```

### Prerequisites
```bash
brew install pandoc   # required for html step
# Google Chrome must be at /Applications/Google Chrome.app/
```

---

## Cover Screenshot Command

Re-render cover.png from cover.html:
```bash
cd products/claude-code-ebook
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless=new --disable-gpu \
  --window-size=1280,1600 \
  --screenshot=cover.png \
  "file://$(pwd)/cover.html"
```

---

## Pre-Launch Checklist

- [ ] All 20 chapter source files present in `src/`
- [ ] `bash build.sh all` completes without errors
- [ ] PDF opens cleanly — fonts render, TOC links work
- [ ] Cover PNG looks correct (1280×1600, amber/dark theme)
- [ ] Ebook priced at $19 on Gumroad (launch price)
- [ ] Gumroad product description written
- [ ] Cover PNG uploaded as Gumroad thumbnail
- [ ] PDF uploaded as Gumroad file attachment
- [ ] Gumroad URL added to CLAUDE.md product list
- [ ] Tweet posted from @luffyselah (max 277 chars)
- [ ] Blogger article written + posted as draft → published
- [ ] Nostr post via `nak` CLI

---

## Revenue Projection

| Scenario         | Price | Sales/mo | Revenue/mo |
|------------------|-------|----------|------------|
| Launch period    | $19   | 20       | **$380**   |
| Post-launch      | $29   | 20       | **$580**   |
| Optimistic       | $29   | 40       | **$1,160** |

Combined with other Gumroad products (5 listed), monthly target: **$500–$900/mo** across all products.

---

## Related Files

- Source chapters: `src/`
- Stylesheet: `ebook.css`
- Build script: `build.sh`
- Cover: `cover.html` / `cover.png`
- Other products: `../nostr-ai-toolkit/`, `../ollama-api-monetizer/`, `../terminal-income-starter/`
