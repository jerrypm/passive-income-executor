# How to Use 1000 Expert Prompts
### A 15-minute guide to getting boardroom-quality output every time

---

## The 60-second version

1. Pick a prompt from any category.
2. Replace every `[BRACKET]` with your own specifics.
3. Paste into ChatGPT-4o, Claude 3.5 Sonnet, Gemini 1.5 Pro, or any frontier model.
4. Read the output. If it's 90% there, refine the brackets and re-run. If it's 50% there, pick a different prompt.
5. Save the winners. Build your personal prompt library.

That's it. Everything below is optional but will 10x your results.

---

## The Four Pillars Behind Every Prompt In This Pack

Every prompt in this pack was engineered around four pillars. Once you internalize them, you can write your own pro-grade prompts for any situation.

### Pillar 1 — Role Specificity

**Weak:** "Act as a copywriter."
**Strong:** "Act as a senior direct-response copywriter who has written $100M+ in control-beating sales letters for Agora and Boardroom."

Why it matters: LLMs are trained on the average of the internet. "Copywriter" gives you the average copywriter. Specifying *which kind*, *at what level*, and *from which school* anchors the model to a specific mental model with specific biases, frameworks, and vocabulary.

**Rule of thumb:** If a human reading the role couldn't picture a specific person, the model can't either.

### Pillar 2 — Named Frameworks

**Weak:** "Give me a marketing message."
**Strong:** "Use the Donald Miller StoryBrand 7-part BrandScript: Character, Problem (external/internal/philosophical), Guide, Plan, CTA, Success, Failure stakes."

Why it matters: Frameworks are compressed expertise. When you name a framework, the model doesn't have to invent structure — it inherits decades of practitioner thinking and fills in the fields.

**Frameworks used heavily in this pack:**
- **Marketing:** AIDA, PAS, BAB, StoryBrand, JTBD, Blue Ocean, Positioning (Moore, Dunford), Value Prop Canvas
- **Business:** Lean Canvas, BMC, Porter's 5 Forces, OKRs, North Star Metric, Ansoff, Wardley Maps
- **Engineering:** SOLID, DRY, YAGNI, DDD, CQRS, Event Sourcing, Hexagonal, 12-Factor, OWASP Top 10
- **Writing:** Hero's Journey, 3-Act, Save the Cat, Story Circle, Freytag, Snowflake
- **SEO:** Skyscraper, E-E-A-T, Topic Clusters, Hub-and-Spoke, Pillar Pages
- **Coaching:** STAR, CAR, SMART, GROW, SBI, Ikigai, Wheel of Life

If you don't know a framework by name, Google it *before* running the prompt — you'll understand the output 10x better.

### Pillar 3 — Concrete Variables

**Weak:** "Write a pitch for my startup."
**Strong:** "Write a 150-word elevator pitch for [STARTUP_NAME], a [STAGE] company in [INDUSTRY] serving [TARGET_CUSTOMER]. Our wedge is [UNIQUE_INSIGHT]. We've achieved [TRACTION_METRIC]."

Why it matters: Specificity forces you to clarify what you actually know. If you can't fill in `[UNIQUE_INSIGHT]`, you don't have a pitch problem — you have a positioning problem. The prompt exposes the gap *before* you waste time generating copy.

**Pro move:** Before running a prompt, fill every `[BRACKET]` in a scratchpad. If you can't fill one, that's the work you need to do first.

### Pillar 4 — Defined Output Structure

**Weak:** "Tell me about pricing strategy."
**Strong:** "Output as a 3-column comparison table: Strategy / When to Use / Risk. Then a 100-word recommendation paragraph and 3 alternative moves ranked by expected revenue lift."

Why it matters: Without structure, LLMs default to wall-of-text prose. Structured output is scannable, actionable, and easy to dump into a doc or a ticket. Every prompt in this pack ends with an "Output as..." clause for exactly this reason.

---

## Which AI Model Should I Use?

Short answer: **Claude 3.5 Sonnet** for thinking-heavy tasks (architecture, strategy, long writing). **GPT-4o** for speed, creative brainstorms, and image generation. **Gemini 1.5 Pro** for long context (paste an entire codebase or book).

All prompts in this pack work on any of these. For best results:

| Task | Recommended Model |
|------|------|
| Sales copy, VSL scripts, email sequences | Claude 3.5 Sonnet |
| Code review, architecture, debugging | Claude 3.5 Sonnet |
| Long-form content, SEO briefs | Claude 3.5 Sonnet or Gemini 1.5 Pro |
| Brainstorming, quick ideation | GPT-4o |
| Image-generation prompt design | GPT-4o (with DALL-E) or any + Midjourney |
| Large document analysis (100+ pages) | Gemini 1.5 Pro |

---

## Power Workflow: The 3-Pass Refine

For any high-stakes output (a sales page, a system design, a pitch deck), don't accept the first response. Run 3 passes:

**Pass 1 — Raw generation.** Run the prompt as-is. Read the output. Ignore the parts you like; focus on the weakest section.

**Pass 2 — Critique.** Paste the output back with: *"You are now a senior critic in this domain. Tear apart the output above. What are the 5 weakest arguments or sections, and why would a skeptical expert reject them?"*

**Pass 3 — Rewrite.** Paste the critique back with: *"Now rewrite the original output fixing all 5 weaknesses. Keep what was strong; replace what was weak."*

This 3-pass loop routinely produces output that's 2-3x better than single-shot prompting. Takes 5 extra minutes. Worth it.

---

## How to Chain Prompts

Many prompts in this pack work as a pipeline. For example, launching a new product:

1. **Business Strategy → Lean Canvas Fill** (understand the model)
2. **Business Strategy → Jobs-To-Be-Done Interview Script** (run customer interviews)
3. **Marketing → StoryBrand BrandScript Generator** (distill the message)
4. **Marketing → Landing Page Conversion Rewrite** (write the page)
5. **Content → Content Brief & Outline** (write the launch blog)
6. **Social Media → Twitter Launch Thread** (promote)
7. **Social Media → LinkedIn Long-Form Post** (promote)
8. **Data → A/B Test Design** (measure)

Build your own pipelines and save them. That's the compounding value of owning a prompt library.

---

## Common Mistakes to Avoid

**1. Leaving brackets empty.** The model will make up content if you leave `[AUDIENCE]` as "general". Be specific or don't run the prompt.

**2. Not reading the framework.** If a prompt mentions "Hexagonal Architecture" and you don't know what that is, you can't evaluate the output. Look it up.

**3. Accepting hedged language.** If the output says "it depends" or "there are many approaches," push back: *"Pick one and defend it. What's your strongest recommendation and why?"*

**4. Mixing categories in one session.** Running a marketing prompt followed by a coding prompt in the same conversation dilutes context. Start a new chat for each domain.

**5. Treating output as truth.** Every prompt output needs human review — especially anything legal, medical, financial, or that will be seen by customers. LLMs hallucinate. You are the senior editor.

---

## Your First 10 Minutes

1. Pick **one category** most relevant to your current project (2 min)
2. Skim the titles and pick **3 prompts** that match an actual task on your plate today (3 min)
3. Fill in the `[BRACKETS]` for the first one and run it (3 min)
4. Read the output and decide: keep, refine, or try a different prompt (2 min)

After that first win, you'll trust the pack enough to use it daily.

---

## Support

Found a prompt that's unclear? Found a framework used that isn't named? Want to request a category for a future update?

Reply to your Gumroad receipt. I read every email.

---

**Now go make something.**
