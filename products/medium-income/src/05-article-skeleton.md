## 5 — The 7-Part Article Skeleton

### What This Chapter Covers

- The seven structural parts every Medium article needs, in order — and why skipping any one of them causes readers to drop off at a predictable point
- Worked examples for each part: what the technique looks like in an actual article, not a hypothetical description
- The most common structural mistake writers make at each part, so you can recognize and fix it before you publish
- Eight niche-specific micro-skeletons — quick-reference outlines for tech listicles, personal essays, tutorials, contrarian pieces, case studies, listicle reviews, how-tos, and stories — that apply the same seven-part logic to different article shapes

---

### Part 1: Opening (3–5 Sentences)

The opening is the only part of your article that every reader sees. Everything after it is conditional. The pattern that works on Medium in 2026 is the same one that worked in journalism fifty years ago: pain → promise → proof. State the pain the reader already feels. Promise the specific thing this article will do about it. Offer a brief proof that you have standing to make that promise.

Here is a worked opening for a hypothetical article titled "8 Xcode Shortcuts I Use Every Day to Ship Faster":

> You open Xcode, and thirty seconds later you are clicking through menus for something you know has a shortcut — you just cannot remember what it is. I spent five years as an iOS developer before I sat down and actually learned the eight commands I now use without thinking. This article is the list I wish I had on day one.

Three sentences: pain, proof, promise. Sentence one names what the reader already experiences. Sentence two delivers the author's standing to make a claim. Sentence three gives the article's value in a single line.

**Common mistake:** Opening with backstory before the pain. Any sentence that begins with vague generic preamble — 'today,' 'with the rise of,' or any framing that could open ten different articles — is filler. Delete it and start with the reader's problem.

---

### Part 2: Scannable Subheads

Every 200 to 300 words, your article needs a subhead. This is not aesthetic preference — it is function. Readers on Medium scan before they read. The subheads they see in those first three seconds determine whether they start reading at all. If your article runs 1,500 words with no subheads, a scanner sees a wall of text and moves on.

The format rule is sentence case, not Title Case. "How to set up your environment" reads as a guide. "How To Set Up Your Environment" reads like an SEO attempt from 2014. Medium readers register the difference even if they cannot name it. Sentence case is warmer; Title Case is corporate.

For the same hypothetical Xcode article, four subheads that follow the rules:

- "How I discovered most of these by accident"
- "The eight shortcuts, in the order I learned them"
- "Why the refactoring commands matter more than navigation"
- "How to make any shortcut stick in under a week"

Each subhead either promises information or names a topic the reader can decide to skip or read. None ends with a period. None tries to be clever at the expense of clarity.

**Common mistake:** Writing subheads as complete sentences with periods. "The navigation shortcuts are the ones most developers learn first." is a sentence from the article body, not a subhead. Subheads are labels or short promises — they do not end with punctuation.

---

### Part 3: Image Placement

One image per major section is the practical target. For a 1,500-word article with four or five sections, that means four or five images. This does not mean you must have that many — one well-placed image is better than three stock photos that add nothing — but it does mean you should not have a 600-word section with no visual break at all.

Use Unsplash for all images. Unsplash's license is free for commercial use, including use on paywalled Medium stories. Download the image, host it in your article, and add a caption that includes both a description of what the image shows and a photographer credit in the format: *Photo by [Name] on Unsplash.*

Caption format: *An Xcode project structure showing the file navigator, editor, and debug pane — the three areas covered in sections 2, 5, and 7. Photo by Luca Bravo on Unsplash.* The caption describes what is shown and credits the photographer — two jobs, one line.

**Common mistake:** Stock-photo clichés — a keyboard, a lightbulb, a generic laptop in a coffee shop. These add no information. If you cannot find an image that genuinely illustrates a section, use a screenshot from your own work, a diagram you made in Excalidraw, or skip the image for that section.

---

### Part 4: Code and Data Blocks

When your article includes code, data, terminal output, or command-line instructions, use triple-backtick fencing with a language tag. Medium renders these as formatted code blocks. Without the language tag, you lose syntax highlighting.

````markdown
```swift
let formatter = DateFormatter()
formatter.dateStyle = .medium
formatter.timeStyle = .none
let label = formatter.string(from: Date())
```
````

The rule is: explain in plain English before you paste the code. Not after. Readers who hit an unexplained code block without context have two options: skip it or close the tab. Neither helps your read ratio. A single sentence before the block — "Here is the formatter setup that handles both the date style and localization in one pass:" — turns a wall of syntax into something the reader understands immediately.

Keep blocks under 30 lines. If you need more than 30 lines to show a concept, split it into two blocks with a sentence between them. A 15-line block with a good explanation reads better than a 60-line block with inline comments.

**Common mistake:** Pasting 80 lines of code with no narrative. The writer assumes the reader will follow — the reader does not. A tutorial with three focused 15-line blocks outperforms a reference dump with one 100-line block, in both read ratio and earnings.

---

### Part 5: Pull-Quotes

Every article gets one pull-quote maximum. One. Not one per section — one per article.

A pull-quote is a `> blockquote` in Markdown that Medium renders as a visually distinct block. Its purpose is to highlight the single most important sentence in your article — the one sentence you want a skimmer to see and register before they decide whether to start reading from the top.

The ideal length is 12 to 20 words. Long enough to carry meaning on its own; short enough to land in one glance.

From the Xcode article:

> The shortcut you use without thinking is the one you learned under pressure, not from a tutorial.

Eighteen words. It stands alone, carries the article's central idea, and gives a scanner a reason to start reading from the top.

**Common mistake:** Pull-quoting something that is already a heading. If the subhead says "Why refactoring commands matter more than navigation," do not also blockquote a restatement of that idea. Both devices become weaker. The pull-quote should say something the headings do not — the insight, the claim, the line that earns the read.

---

### Part 6: The CTA

Your article gets exactly one call to action. Choose one of these two options: a link to your most relevant other article, or a link to your newsletter. Not both. One.

The decision between them depends on what the reader needs next. If you have a closely related article — a natural next step in the same subject — link to that. The reader who just finished your Xcode shortcuts article is a candidate for your "8 Swift Extensions I Use in Production" article. Give them the next link.

If you do not have a closely related article yet, link to your newsletter (if you have one). This is the slower path, but it builds a list that is independent of Medium's algorithm.

Place the CTA in the second-to-last paragraph, not the last paragraph. The last paragraph is the article's actual ending — the closing thought, the reflection, the summary. If the CTA is the last thing the reader sees, the article ends on a transaction. That registers as pushy. Put the CTA one step before the end, and let the article end on its own terms.

**Common mistake:** Stacking CTAs at the bottom — "Subscribe to my newsletter / Follow me on Medium / Buy my course / Share this on Twitter." Readers click none of these. The more choices you offer, the fewer actions anyone takes. One CTA means one clear direction for the reader who wants to keep engaging with your work. Three CTAs means the reader picks none and closes the tab.

---

### Part 7: Friend-Link Footer

Every published story on Medium should end with a friend-link note. Always. Even stories you think do not need one.

The format is a short note at the very bottom of the article, after the article content has finished. One to two sentences:

> Not a Medium member? Read this story for free using my friend link: [paste your friend link URL here]

You generate the friend link from your story's settings panel before publishing. It is a unique URL that lets non-members read your full article without hitting the paywall.

When a non-member reads your story via a friend link and then subscribes during that session, you receive the conversion bonus covered in Chapter 8. Without the friend link, Medium shows the subscribe prompt immediately — before the reader has finished the article. The friend link lets them read first, which converts at a much higher rate.

**Common mistake:** Omitting the friend link for non-paywalled stories on the grounds that "everyone can already read it." Non-paywalled stories can still trigger conversion bonuses. Add it to every story, paywalled or not.

---

### 8 Niche-Specific Micro-Skeletons

These are quick-reference outlines. They apply the seven-part skeleton to eight common article shapes. Each section header is the part of the article; the one-line description is what goes there. Full templates are in the bonus file — this is the at-a-glance version to reference while drafting.

**1. Tech listicle**
- Hook: Pain or gap the list solves (1–2 sentences)
- Why this list now: What made this the right moment to write it
- Items 1–N: Consistent format per item — name, what it does, when to use it
- Bonus item: The one most readers will not have heard of
- Footer: Friend link + one related article link

**2. Personal essay**
- Hook moment: Drop the reader into the scene — no backstory yet
- Backstory in 2 lines: Just enough context to make the scene make sense
- The conflict: What was at stake or what had to be decided
- The choice: What you actually did
- The lesson: What it taught you that you did not expect
- Reflection: How you think about it now

**3. Tutorial**
- Outcome promise: Exactly what the reader will have working at the end
- Prerequisites: What the reader needs before starting (versions, tools, accounts)
- Step 1: First action — command, click, or concept
- Step 2: Second action
- Step 3: Third action (add more steps as needed, keep each focused)
- Verify it worked: How to confirm the outcome was achieved
- Troubleshooting: Two or three common failure points and fixes

**4. Contrarian opinion**
- The widely-held belief: State it fairly — do not strawman it
- Why it is wrong: Your specific objection, not a vague alternative
- Evidence: Data, personal experience, or cited source that supports your objection
- What to do instead: The concrete alternative you are recommending
- Caveat: Where the conventional wisdom still holds — this is what makes the piece credible

**5. Case study**
- Subject and situation: Who or what this is about, and the starting context
- The before state: Measurable or observable condition before the change
- What was done: The specific actions taken, in order
- The after state: Measurable or observable result
- Lessons: What this tells us that generalizes beyond this one case
- How to apply it: One or two steps the reader can take based on this case

**6. Listicle review (book or tool round-up)**
- Why this round-up: What gap this fills that other lists do not
- Criteria: How you evaluated each item — be specific
- Item 1 through N: For each — verdict in one sentence, then when to use it
- Final verdict: If you could only pick one item from the list, which and why

**7. How-to**
- Problem: The specific situation the reader is in
- Promise: The exact thing they will be able to do after reading
- Step 1: First action
- Step 2: Second action
- Step 3: Third action (extend as needed)
- Result: What the completed outcome looks like
- Variations: Alternate paths for common edge cases

**8. Story**
- Situation: Where and when — set the scene in one or two sentences
- Conflict: What went wrong, what was missing, or what created pressure
- Choice: What decision was made at the turning point
- Outcome: What actually happened as a result
- Lesson: The single thing this story demonstrates that the reader can take away

---

Chapter 6 takes the skeleton you have now and puts it on a calendar. The 14-day plan covers exactly which article type to write first, how many hours to budget per piece, and how to sequence your initial catalog so that each new story builds on the last — rather than sitting as an isolated post with no internal links. The micro-skeleton that fits your niche is already in this chapter; Chapter 6 is where you schedule it.

