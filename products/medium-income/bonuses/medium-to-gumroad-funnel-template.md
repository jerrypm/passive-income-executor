# Medium → Gumroad Funnel SOP

This is the standard operating procedure for turning a hit Medium article into a paid Gumroad PDF. Use it as a checklist every time a Medium article hits the criteria from Chapter 11. A worked example from the author's own catalog is included at the end — every step applied to a real product.

## Step 1: Identify A Hit Article

Not every article deserves a paid expansion. The criteria from Chapter 11 keep you from wasting time on articles that won't convert. A hit article has: read count above 1,500 in the first 30 days, reads-to-views ratio above 25%, at least five comments asking specific implementation questions, and a niche where buyers already exist — developer tools, productivity systems, or personal finance. Personal stories rarely convert, even with high views, because readers are there for the story, not the solution.

## Step 2: Plan The Expansion

1. Open the original article. Count the number of items (tips, tools, components, steps) and the total word count.
2. Set your ebook targets: 4–5× the original item count, and 5–10× the word count. A 12-item article becomes a 50–60 item ebook. A 1,200-word article becomes 8,000–12,000 words minimum.
3. Map the new sections to add: an introduction (the WHY behind the topic, written from experience), a worked example for each item, a glossary of key terms, and a closing "next steps" CTA that points readers to your other products and newsletter.
4. Estimate total length: 12,000–15,000 words renders to 80–120 pages in PDF — the right size for a $19 tier product.

## Step 3: Write The Expansion

1. Open a new Markdown file. Paste the original article at the top as your starting scaffold.
2. For each existing item, expand it to 200–300 words using four sub-elements: definition (what it is in plain terms), why it matters (the cost of ignoring it), a code or data example where applicable, and the common mistake most beginners make with it.
3. Add new items until you hit 4–5× the original count. Use the same four-element structure — consistency separates a well-edited ebook from a blog post collection.
4. Write the introduction separately — around 1,000 words on the WHY of the topic, who the reader is, and what they will be able to do when they finish.
5. Write the closing CTA section last. Point to two or three Gumroad products by name, mention your newsletter if you have one. One paragraph per product, no hard sell.

## Step 4: Cover Design

Your cover should match the visual brand of your existing Gumroad catalog. Consistency makes you look like a publisher rather than a one-off seller. Use 1280×1600 px — this works as both the Gumroad thumbnail and the PDF cover without resizing. The layout that holds up at thumbnail size: bold typography with the title dominating, a single bold number or keyword as the anchor, an accent line in your brand color, and your byline at the bottom. Avoid photographs. Test the cover at 300px wide before finalizing — that is roughly what buyers see in search results.

## Step 5: Build The PDF

1. Render your Markdown to HTML using pandoc with a custom CSS file that sets your font choices, line height, and code block styling.
2. Print the HTML to PDF using headless Chrome: `google-chrome --headless --disable-gpu --print-to-pdf=output.pdf input.html`
3. Open the PDF and verify the page count falls between 80–120 for a $19 tier product. If it is under 70, your expansions are too thin. If it is over 130, consider splitting into two products.
4. Embed cover.png as the first page of the PDF, or upload it separately as the Gumroad thumbnail — uploading separately gives cleaner control over the aspect ratio Gumroad displays.

## Step 6: Gumroad Listing Copy

Write the listing copy before you upload the file. Buyers decide in 10 seconds. Three templates cover everything.

**Tagline (under 150 chars):**
```
[Number/Hook from book title] — [Who it's for] in [time period]. [Unique angle / 1 receipt].
```
Example: `30 title templates that turned a $67 Medium article into a $190+ Gumroad guide. For beginners worldwide.`

**Description first paragraph (the hook):**
```
[Pain the reader is feeling]. This [pack / guide / system] gives you [outcome] using [proof from your own work]. No fluff, no theory — just the [N] [items] that [verb] [result].
```

**FAQ entry template (write 5 of these):**
```
**Q: [The objection most likely to stop a buyer]**
A: [The honest answer that addresses it without overselling].
```

Common objections to address: beginner-friendliness, file format, language or tool requirements, experience level, and whether it works outside the US. A short, direct answer to each builds more trust than a marketing paragraph.

## Step 7: Cross-Promo Loop

- Add a Friend Link footer to the original Medium article that mentions the Gumroad product by name: "Want the full expanded version with worked examples? See [Product Name] on Gumroad." The Friend Link bypasses the paywall so new readers land on the article first, then see the upsell.
- Update your Medium profile bio to include one link to your top-selling Gumroad product. Most readers who finish an article check your profile — that one link does quiet, ongoing work.
- Write a "behind the scenes" Medium article about how you turned the original into a paid product — the writing process, the page count, what you added, what you cut. This drives launch-week buzz and often becomes a second hit that feeds buyers into the same Gumroad listing.

## Worked Example: 12 SwiftUI Components → 1000 Expert Prompts

Here is how the SOP played out on a real product from this catalog:

1. **The original article:** "12 Powerful SwiftUI Components" — 5,800 views, 2,700 reads, 47% read ratio, $67.99 earned on Medium. Specific implementation questions in the comments pushed it past the hit threshold from Chapter 11.
2. **The expansion decision:** The obvious move was a SwiftUI ebook, but the niche is crowded with free Apple documentation and WWDC sessions. The comment patterns showed readers wanted productivity tools — workflows, not just code. That signal pointed sideways: a prompt-engineering pack the same audience would buy. The result was "1000 Expert Prompts" on Gumroad at the $9 tier — 10 categories × 100 prompts, role-based, framework-powered, variable-driven.
3. **Cover design:** Matched the catalog brand — same font stack, same color palette, same bold-number anchor layout.
4. **Build process:** Pandoc Markdown to HTML, headless Chrome to PDF, cover embedded as page one.
5. **Listing copy:** Led with the math — 1,000 prompts across 10 categories — because the number does the selling. Tagline under 100 characters.
6. **Cross-promo:** Every Gumroad product page links to the other products in the catalog. The Medium profile points to the top seller by name.

The takeaway: a hit article doesn't have to expand into the same niche. The read ratio and comment signal told the author what kind of buyer was reading — and that was more reliable than the topic itself.

The SOP is short. The work is the writing. Get one hit, then run this checklist.
