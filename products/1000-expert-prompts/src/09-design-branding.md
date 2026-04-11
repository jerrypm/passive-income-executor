## Design, Branding & Visual Identity

### 1. Full Brand Identity System
**Prompt**: Act as a senior brand designer at a Pentagram-level studio with 12 years designing identity systems for Fortune 500 brands. Build a complete brand identity for [BRAND_NAME], a [INDUSTRY] company targeting [TARGET_USER] with a [BRAND_PERSONALITY] personality. Apply grid systems, golden ratio proportions, and WCAG AA color contrast. Output: brand positioning statement, logo concept rationale, primary + secondary color palette (hex + HSL), typography pairing with scale ratio, voice & tone guidelines, and three moodboard descriptors.

### 2. Brand Voice & Tone Guide
**Prompt**: Act as a brand strategist from Wolff Olins with deep copywriting DNA. Write a brand voice guide for [BRAND_NAME] in [INDUSTRY], personality [BRAND_PERSONALITY], targeting [TARGET_USER]. Define voice attributes (we are X, not Y), tone shifts across four contexts (marketing, product UI, support, crisis), signature words, banned words, and five before/after copy examples. Output: markdown document with headings, bullet lists, and a one-page cheat sheet at the end.

### 3. Typography Pairing System
**Prompt**: Act as a type designer trained at Reading University with 10 years specifying type systems for editorial and SaaS brands. Propose three typography pairings for [BRAND_NAME] in [INDUSTRY], personality [BRAND_PERSONALITY]. For each pairing specify display + body fonts (name + foundry), modular scale ratio (1.200, 1.250, 1.333), line-height, tracking, weights used, fallback stack, and rationale tied to brand personality. Output: table plus a recommended pairing with CSS @font-face snippet.

### 4. Color Palette With Accessibility
**Prompt**: Act as a color theorist grounded in Josef Albers and WCAG 2.2. Build a color system for [BRAND_NAME], [INDUSTRY], mood [BRAND_PERSONALITY]. Include 1 primary, 2 secondary, 3 accent, 2 neutrals, success/warning/error. Provide hex, HSL, and OKLCH, plus WCAG AA and AAA pass/fail against white, black, and primary. Describe usage rules, do/don'ts, and dark-mode variants. Output: markdown table plus a text-based swatch block.

### 5. Logo Concept Brief
**Prompt**: Act as a logo designer mentored by Michael Bierut. Write a creative brief for [BRAND_NAME] in [INDUSTRY], personality [BRAND_PERSONALITY], targeting [TARGET_USER]. Include objective, audience, competitive landscape (list 5 competitor marks and why they fail), three concept directions (wordmark, symbol+wordmark, monogram), construction grid notes, clear-space and min-size rules, and three rejected directions with reasoning. Output: structured brief in markdown.

### 6. Logo Critique Rubric
**Prompt**: Act as a design director running crit sessions at a top-10 branding agency. Critique my logo for [BRAND_NAME] using a 10-point rubric: distinctiveness, legibility at 16px, scalability, negative space, construction (golden ratio/grid), color independence (works in B&W), cultural/trademark risk, ownability, memorability after 5s, and alignment with [BRAND_PERSONALITY]. Score each 1-10 with rationale. Output: scorecard table, top 3 issues, and three concrete revision directions.

### 7. Monogram Logo Exploration
**Prompt**: Act as a lettering specialist inspired by Jessica Hische. Explore 8 monogram directions for initials [INITIALS] for [BRAND_NAME] in [INDUSTRY]. For each: describe construction (stacked, interlocked, ligature, negative-space, circular container), historical reference (Bauhaus, Art Deco, mid-century Swiss), ideal weight, and where it shines (app icon, embroidery, debossed). Output: numbered list with 2-3 sentence rationale each and one chosen direction with extended notes.

### 8. Wordmark Type Customization
**Prompt**: Act as a type customizer who ships wordmarks for Series-B SaaS brands. Given base typeface [TYPEFACE] for [BRAND_NAME], specify 6 custom modifications (optical adjustments, terminals, counters, ligatures, spacing) that make the wordmark ownable. Explain each modification, why it reinforces [BRAND_PERSONALITY], and tradeoffs at small sizes. Output: numbered modifications, before/after description, and final glyph-by-glyph spec note.

### 9. Logo Animation Direction
**Prompt**: Act as a motion brand designer from BUCK. Design a 2-3 second logo reveal animation for [BRAND_NAME]. Specify easing (cubic-bezier values), stagger timing, anticipation/overshoot, sound pairing suggestion, and three interpretations (playful, confident, minimal). Include a frame-by-frame timeline (0ms, 200ms, 600ms, 1200ms) and After Effects expression hint for the primary motion. Output: timeline table plus implementation notes.

### 10. Brand Application Mockup Brief
**Prompt**: Act as an art director preparing a brand launch deck. List 12 mockup scenes to showcase [BRAND_NAME] identity: business card, letterhead, signage, app icon, social avatar, tote, packaging, vehicle livery, wayfinding, merch, uniform, environmental. For each specify camera angle, lighting (studio, golden hour, overhead), material, and one-sentence art direction. Output: numbered shot list in a table with columns Scene | Angle | Lighting | Material | Notes.

### 11. Wireframe For SaaS Dashboard
**Prompt**: Act as a product design lead at a top-tier B2B SaaS (Linear/Vercel caliber). Produce low-fidelity wireframe specs for a [INDUSTRY] dashboard where [TARGET_USER] needs to [PRIMARY_ACTION]. Apply 8pt grid, F-pattern scanning, and Hick's Law for nav count. Specify layout regions (sidebar 240px, topbar 56px, content max 1280px), primary components, empty states, and data density tradeoffs. Output: ASCII wireframe sketch plus component inventory table.

### 12. User Flow Diagram Spec
**Prompt**: Act as a UX architect trained in service design. Map the user flow for [TARGET_USER] to complete [PRIMARY_ACTION] on [PLATFORM] for [BRAND_NAME]. Include entry points, happy path, error branches, edge cases, and exit points. Annotate each step with UX law applied (Miller's 7+/-2, Peak-End, Aesthetic-Usability). Output: mermaid flowchart syntax plus a 5-row table mapping Step | Goal | UX Law | Friction | Fix.

### 13. Component Library Spec
**Prompt**: Act as a design system engineer from Shopify Polaris team. Spec a Button component for [BRAND_NAME] design system. Define variants (primary, secondary, tertiary, destructive, ghost), sizes (sm 32px, md 40px, lg 48px), states (default, hover, active, focus, disabled, loading), tokens (color, radius, shadow, spacing), and accessibility (focus ring, aria-label, keyboard). Output: JSON token definition plus Figma layer structure and code pseudo-snippet.

### 14. Accessibility Audit Checklist
**Prompt**: Act as an accessibility specialist certified in WCAG 2.2 AA/AAA. Audit [PLATFORM] for [BRAND_NAME] against a 25-point checklist covering color contrast, keyboard nav, focus indicators, ARIA, alt text, semantic HTML, reduced motion, target size (44x44), error messaging, form labels, and screen reader order. For each point: pass/fail heuristic and fix priority (P0-P2). Output: checklist table with Criterion | Test | Status | Fix | Priority.

### 15. Empty State Design Brief
**Prompt**: Act as a UX writer-designer hybrid from Intercom. Design 4 empty states for a [INDUSTRY] app where [TARGET_USER] is the user: first-time use, no results, error, no permission. Each must include headline (max 6 words), subcopy (max 14 words), primary action, illustration concept, and emotional tone. Apply Peak-End Rule and Von Restorff effect. Output: table plus one hero empty state fully fleshed out with Figma frame notes.

### 16. Dark Mode Conversion Guide
**Prompt**: Act as a UI engineer who shipped dark mode at a Fortune 500. Convert [BRAND_NAME] light theme to dark for [PLATFORM]. Define elevation layers (background, surface, overlay, modal) with hex values, avoid pure #000, desaturate primary colors, preserve WCAG AA contrast, handle brand color shift, and address shadow replacement with borders. Output: paired color token table (light/dark) plus 6 gotchas and solutions.

### 17. Landing Page Hero Spec
**Prompt**: Act as a conversion-focused landing page designer with 200+ shipped pages averaging 8% conversion. Design a hero section for [BRAND_NAME], an [INDUSTRY] product for [TARGET_USER] to [PRIMARY_ACTION]. Apply F-pattern, 5-second test, and above-the-fold clarity. Specify headline (max 10 words, benefit-driven), subhead (20 words), primary CTA label, social proof element, and hero visual direction. Output: wireframe sketch plus 3 headline variants and rationale.

### 18. Landing Page Conversion Audit
**Prompt**: Act as a CRO designer trained by Unbounce and Peep Laja. Audit the landing page at [URL_OR_DESCRIPTION] for [BRAND_NAME] against 15 heuristics: clarity, value prop, CTA contrast, Fitts's Law, social proof placement, form friction, loading perf, mobile thumb zone, trust signals, urgency, objection handling, copy scannability, visual hierarchy, whitespace, consistency. Output: scored audit table plus top 5 fixes ranked by expected lift.

### 19. Pricing Page Design Spec
**Prompt**: Act as a SaaS pricing page designer who studied Stripe, Linear, and Notion layouts. Design a 3-tier pricing page for [BRAND_NAME] in [INDUSTRY]. Apply anchoring, decoy effect, and Hick's Law. Specify tier names, recommended tier highlight, feature comparison table structure, toggle (monthly/annual), FAQ placement, and objection-killing social proof. Output: wireframe plus copy for each tier (name, price, tagline, 5 bullets, CTA).

### 20. Mobile App Onboarding Flow
**Prompt**: Act as a product designer who shipped onboarding for a top-50 App Store app. Design a 4-screen onboarding for [BRAND_NAME] iOS app where [TARGET_USER] wants to [PRIMARY_ACTION]. Follow Apple HIG, progressive disclosure, and Zeigarnik effect. Each screen: illustration concept, headline (max 5 words), body (max 18 words), primary action, skip affordance. Include permission priming strategy. Output: screen-by-screen spec table plus copy variants.

### 21. iOS App Screen Spec Sheet
**Prompt**: Act as an iOS designer fluent in Apple HIG and SF Symbols. Spec a [SCREEN_TYPE] screen for [BRAND_NAME] app. Specify safe area (top 47pt, bottom 34pt), nav bar style, SF Symbol choices, dynamic type scaling, haptic feedback moments, dark mode tokens, and VoiceOver labels. Apply 44pt touch targets. Output: annotated spec list plus SwiftUI view pseudo-snippet with accessibilityLabel.

### 22. Material 3 Android Screen
**Prompt**: Act as a Google-certified Material 3 designer. Spec a [SCREEN_TYPE] screen for [BRAND_NAME] Android app for [TARGET_USER] to [PRIMARY_ACTION]. Apply Material 3 tokens (md.sys.color, elevation levels), dynamic color from wallpaper, FAB placement, app bar behavior, and target size 48dp. Include motion spec (standard easing, 300ms duration). Output: component list with Material tokens, spacing in dp, and a Jetpack Compose layer sketch.

### 23. Mobile Tab Bar Design
**Prompt**: Act as a mobile IA specialist. Design a 5-tab bar for [BRAND_NAME] app in [INDUSTRY]. Apply Hick's Law and thumb-zone heatmap. Name each tab (max 8 characters), select icon style (filled vs outlined for selected state), justify each tab against jobs-to-be-done for [TARGET_USER], and flag any removed candidates. Output: tab list with Label | Icon | JTBD | Thumb-zone priority plus alternate 4-tab variant.

### 24. Midjourney Product Photo Prompt
**Prompt**: Act as a Midjourney prompt engineer specializing in commercial product photography. Write a v6 prompt for a product photo of [PRODUCT] for [BRAND_NAME], mood [BRAND_PERSONALITY]. Specify subject, material, surface, lighting (softbox, rim light, hard shadow), camera (85mm macro, f/2.8), background, color palette, composition, and style references. End with --ar 4:5 --style raw --v 6 parameters. Output: final prompt plus 2 variations.

### 25. DALL-E Illustration Prompt
**Prompt**: Act as an illustration art director with DALL-E 3 expertise. Write a prompt to generate a hero illustration for [BRAND_NAME] landing page depicting [CONCEPT]. Specify art style (flat, isometric, editorial, risograph), color palette with hex codes, composition rule (rule of thirds, centered), character style, texture, and mood. Avoid photorealism unless needed. Output: 3-sentence prompt plus 2 style variations and a negative prompt list.

### 26. Stable Diffusion Brand Photography
**Prompt**: Act as a Stable Diffusion XL prompt engineer shooting brand photography. Write a prompt + negative prompt for [BRAND_NAME], [INDUSTRY], scene: [SCENE_DESCRIPTION]. Specify checkpoint recommendation, sampler (DPM++ 2M Karras), steps, CFG, seed strategy, LoRA suggestions, and camera/lens. Match mood to [BRAND_PERSONALITY]. Output: prompt block, negative prompt block, and settings table (sampler/steps/CFG/ratio).

### 27. Midjourney Character Design
**Prompt**: Act as a character designer working with Midjourney for brand mascots. Write a prompt for a mascot for [BRAND_NAME] in [INDUSTRY], personality [BRAND_PERSONALITY]. Specify species/form, silhouette, outfit, expression, pose turnaround (front, 3/4, side), color palette, line weight, and influences (Pixar, Cartoon Network, Ghibli, vintage mascot). Output: full Midjourney v6 prompt with --ar 1:1 --style raw and two alternate mood variants.

### 28. AI Moodboard Generation Prompt
**Prompt**: Act as a brand designer building a moodboard in Midjourney. Write 6 prompts forming a cohesive moodboard for [BRAND_NAME], [INDUSTRY], personality [BRAND_PERSONALITY]. Each prompt targets one moodboard tile: hero texture, color story, typography feel, human moment, product detail, environment. Keep stylistic coherence via shared color + lighting. Output: 6 numbered prompts with --ar 1:1 --v 6 and a one-line note on what each tile communicates.

### 29. AI Pattern & Texture Prompt
**Prompt**: Act as a surface pattern designer using Midjourney. Write prompts for 4 seamless patterns for [BRAND_NAME] packaging/apparel, tied to [BRAND_PERSONALITY]. Specify motif, scale, repeat logic, color palette, printing method (risograph, foil, screen print), and reference (William Morris, Memphis, Bauhaus). Add --tile --ar 1:1 --v 6. Output: 4 prompts with style notes and a primary pattern recommendation.

### 30. Illustration Style Guide
**Prompt**: Act as an illustration director shaping a proprietary illustration style for [BRAND_NAME] in [INDUSTRY]. Define style DNA in 6 rules (line weight, shape language, color palette, shading technique, character proportions, composition). Provide do/don't examples in prose. Include a spec for 3 illustration types: spot, hero, empty-state. Output: rules list plus spec table with Type | Size | Usage | Complexity.

### 31. Icon System Spec
**Prompt**: Act as an icon designer behind a top design system (Phosphor/Lucide caliber). Spec an icon system for [BRAND_NAME]: grid (24x24), stroke width (1.5px or 2px), corner radius (2px), terminals (rounded/square), optical balance rules, and pixel-snapping. Define 4 states (regular, bold, fill, duotone). Output: spec sheet plus sample icon descriptions for home, search, settings, notification, user — each with construction notes.

### 32. Custom Icon Brief
**Prompt**: Act as a senior icon designer. Design 10 custom icons for [BRAND_NAME] in [INDUSTRY] for actions: [ACTION_LIST]. Each icon must follow the system grid 24x24, 2px stroke, and convey meaning in under 300ms (pre-attentive). For each icon describe metaphor, construction notes, potential confusion risk, and cultural considerations. Output: table with Icon name | Metaphor | Construction | Risk | Alternate.

### 33. Pitch Deck Visual System
**Prompt**: Act as a presentation designer at a top Sand Hill Road VC shop. Design a visual system for [BRAND_NAME] seed pitch deck, [INDUSTRY], audience top-tier VCs. Specify 16:9 master grid, safe margins, type scale (title 48/subtitle 24/body 18), color palette (3 colors), chart style, icon treatment, and slide templates (title, problem, solution, market, traction, team, ask). Output: system spec plus storyboard list of 12 slides.

### 34. Keynote Slide Redesign
**Prompt**: Act as a slide doctor who rescues exec decks. Redesign a slide titled "[SLIDE_TITLE]" for [BRAND_NAME] in [INDUSTRY]. Apply Assertion-Evidence structure, Tufte data-ink ratio, 6x6 rule, and visual hierarchy via contrast + scale. Describe layout (left/right split, z-pattern), typography, chart or visual, and takeaway at bottom. Output: before/after description plus a text-based layout sketch and speaker-note hint.

### 35. Data Visualization Design
**Prompt**: Act as a data viz designer trained by Edward Tufte and Giorgia Lupi. Design a chart to show [DATA_STORY] for [BRAND_NAME]. Pick chart type justified by data shape (trend, comparison, composition, distribution, relationship), apply pre-attentive attributes, remove chartjunk, and include annotation strategy and color for colorblind users. Output: chart spec (type, axes, colors, annotations) plus the single-sentence takeaway title.

### 36. Book Cover Design Brief
**Prompt**: Act as a book cover designer at Penguin Random House with 15 years on bestsellers. Design a cover for "[BOOK_TITLE]" by [AUTHOR], genre [GENRE], target reader [TARGET_USER]. Reference 3 category leaders, propose 3 distinct directions (type-driven, photographic, illustrated), specify trim size, spine treatment, back cover layout, and finish (matte, foil, deboss). Output: 3 direction descriptions plus recommended direction with full spec.

### 37. Packaging Design Concept
**Prompt**: Act as a packaging designer from Turner Duckworth. Concept packaging for [PRODUCT] from [BRAND_NAME] in [INDUSTRY], personality [BRAND_PERSONALITY]. Specify structure (carton, pouch, bottle), material, print method, dieline notes, front panel hierarchy (brand, product name, descriptor, size, imagery), back panel, unboxing moment, and sustainability angle. Output: concept brief plus front/back panel text-based layout sketch.

### 38. Poster Design Direction
**Prompt**: Act as a Swiss-school poster designer influenced by Josef Muller-Brockmann. Design a poster for [EVENT/CAMPAIGN] for [BRAND_NAME]. Use a 12-column grid, asymmetric balance, scale contrast, and one hero element. Specify format (A2, 594x420mm), typography (one family, 3 weights), color (2 colors max), and printing method. Output: layout description with grid coordinates plus typographic hierarchy spec.

### 39. Business Card System
**Prompt**: Act as a stationery designer. Design a business card system for [BRAND_NAME], personality [BRAND_PERSONALITY]. Specify dimensions (85x55mm), paper (GSM, texture, color), printing (letterpress, foil, thermography), front/back layout, typographic hierarchy (name, role, contact), QR placement, and 3 variants per role. Output: layout spec plus paper/printing recommendation with rationale tied to brand.

### 40. Merchandise Design Brief
**Prompt**: Act as a merch director for a design-forward brand. Plan a capsule merch drop of 6 items for [BRAND_NAME] targeting [TARGET_USER]. Items should span apparel, accessory, print, and utility. For each: item, material, print method (screen, embroidery, DTG), placement, colorway, SRP, and brand alignment score. Output: table with Item | Material | Print | Placement | Colorway | SRP plus launch story in 2 sentences.

### 41. Signage & Wayfinding System
**Prompt**: Act as an environmental graphic designer who shipped wayfinding for airports and campuses. Design a signage system for [LOCATION_TYPE] for [BRAND_NAME]. Apply pictogram standards, viewing distance typography (1in per 25ft), contrast ratios, materiality, and mounting heights. Spec primary, directional, identification, regulatory, and information signs. Output: sign inventory table with Type | Size | Material | Mount | Copy.

### 42. Figma File Structure Spec
**Prompt**: Act as a Figma ops lead at a design team of 30. Define a scalable file structure for [BRAND_NAME] design team in [INDUSTRY]. Specify team organization, project naming, file naming (semver), page structure (Cover, Changelog, Explorations, Final, Archive), component library split, variable collections, and handoff conventions. Output: folder tree plus naming convention table and a 5-rule governance cheat sheet.

### 43. Design Token Architecture
**Prompt**: Act as a design systems engineer fluent in Style Dictionary and DTCG tokens. Architect a 3-tier token system (primitive, semantic, component) for [BRAND_NAME]. Include color, spacing, radius, shadow, typography, and motion. Show naming (color.brand.500, spacing.md, radius.lg) and cross-platform transforms (CSS, iOS, Android). Output: JSON token schema plus naming rules and 3 worked examples.

### 44. Handoff Documentation Template
**Prompt**: Act as a design-to-dev handoff specialist. Write a handoff doc template for [FEATURE] for [BRAND_NAME] on [PLATFORM]. Include overview, user story, acceptance criteria, screens list, interaction states, edge cases, accessibility notes, analytics events, copy sheet, asset export list, and open questions. Output: markdown template with filled placeholder example and a PR checklist block at the end.

### 45. Design Critique Framework
**Prompt**: Act as a design director running weekly crits. Write a crit framework for reviewing [ARTIFACT_TYPE] for [BRAND_NAME]. Structure: context (2 min), walkthrough (5 min), clarifying questions (3 min), feedback rounds (10 min) using "I like / I wish / What if", director synthesis (5 min). Include 10 feedback questions grounded in UX laws. Output: agenda table plus 10 questions and three anti-patterns to avoid.

### 46. Portfolio Case Study Template
**Prompt**: Act as a portfolio reviewer at Google Material. Write a case study template for [DESIGNER_ROLE] applying to senior roles. Sections: context, role, problem, constraints, research, process, key decisions (with tradeoffs), final design, measured outcomes, learnings, credits. Add guidance for length, image captions, and storytelling hooks. Output: annotated template plus a filled micro-example for a [FEATURE] project.

### 47. Personal Brand Identity
**Prompt**: Act as a personal branding consultant for creatives. Build a personal brand system for [YOUR_NAME], a [ROLE] in [INDUSTRY], personality [BRAND_PERSONALITY]. Deliver: positioning statement (I help X do Y by Z), 3 brand adjectives, monogram concept, color palette (3 colors), typography pairing, bio template (140, 280, 500 chars), and 5 signature content themes. Output: one-page brand doc.

### 48. Brand Architecture Map
**Prompt**: Act as a brand strategist from Interbrand. Map brand architecture for [PARENT_BRAND] with sub-brands [SUB_BRANDS]. Choose model (monolithic, endorsed, hybrid, house of brands), justify with pros/cons, define naming conventions, visual relationship (shared vs distinct identity), and migration roadmap. Output: architecture diagram description, decision matrix, and rollout plan in 3 phases.

### 49. Naming Exploration
**Prompt**: Act as a brand namer behind 20+ shipped company names. Generate 30 name candidates for [COMPANY_DESCRIPTION] in [INDUSTRY], personality [BRAND_PERSONALITY]. Split across 5 buckets: descriptive, suggestive, experiential, evocative, invented. For each name note pronunciation, etymology, domain likelihood, trademark risk (low/med/high), and emotional hook. Output: table with 30 rows plus top 5 recommended with rationale.

### 50. Tagline Generator
**Prompt**: Act as a copywriter with Ogilvy lineage. Write 15 tagline options for [BRAND_NAME] in [INDUSTRY] targeting [TARGET_USER], mood [BRAND_PERSONALITY]. Mix styles: benefit, imperative, witty, metaphorical, minimal. Keep under 7 words each. For each tagline note angle and memorability score (1-10). Output: table with Tagline | Angle | Score | Notes plus top 3 recommended with rationale.

### 51. Social Media Template Kit
**Prompt**: Act as a social content designer for a brand shipping 200 posts/month. Design a template kit for [BRAND_NAME] on [PLATFORM]. Include 6 templates: quote, stat, announcement, carousel cover, carousel body, testimonial. Spec aspect ratio, grid, type scale, color roles, safe zones, and brand-lock placement. Output: template list with dimensions and a text-based layout sketch for each plus Figma variable suggestions.

### 52. Instagram Grid Layout
**Prompt**: Act as an Instagram grid designer who ships brand feeds. Design a 9-post rolling grid plan for [BRAND_NAME] with content pillars [PILLARS]. Specify grid pattern (checkerboard, row, column, mosaic), color rhythm, content type rotation, and aesthetic glue. Apply gestalt similarity/proximity. Output: 3x3 grid text sketch labeling each tile with content type and color note plus a monthly rotation rule.

### 53. Email Template Design
**Prompt**: Act as an email designer fluent in bulletproof email HTML and dark-mode quirks. Design a responsive email template for [BRAND_NAME] for [EMAIL_TYPE] (welcome, newsletter, promo, transactional). Specify 600px width, single column mobile, hero, body modules, CTA, footer with unsubscribe. Apply WCAG AA contrast and alt text. Output: module list with dimensions plus inline-style snippet hints and subject-line formula.

### 54. App Icon Design Brief
**Prompt**: Act as an app icon designer whose icons sit on home screens of top-100 apps. Design an app icon for [BRAND_NAME] in [INDUSTRY], personality [BRAND_PERSONALITY]. Follow iOS 1024x1024 rules and Android adaptive icon foreground/background. Propose 3 directions (monogram, symbol, pictorial), specify color, shadow/gradient use, corner radius behavior, and test at 60x60. Output: 3 concepts plus recommended direction with spec.

### 55. Favicon & Browser Icon Set
**Prompt**: Act as a web identity specialist. Design a favicon system for [BRAND_NAME]. Provide sizes (16, 32, 48, 180 apple-touch, 192, 512, maskable 512), SVG source rule, dark/light scheme with prefers-color-scheme, manifest.webmanifest spec, and Safari pinned-tab monochrome version. Output: asset inventory table plus HTML head snippet pseudo-code and a 3-rule optical-adjustment note.

### 56. Error & 404 Page Design
**Prompt**: Act as a UX designer known for delightful error states. Design a 404 page for [BRAND_NAME] in [INDUSTRY]. Include headline with brand voice, apology tone, recovery actions (search, home, popular links), illustration concept, and personality moment. Apply Peak-End Rule and preserve trust. Output: layout sketch plus headline options (3 tones), body copy, and illustration prompt for Midjourney.

### 57. Brand Guidelines Document
**Prompt**: Act as a brand guidelines author trained at &Walsh. Write a guidelines outline for [BRAND_NAME] covering: story, logo rules, color, typography, imagery, iconography, voice, motion, layout, applications, do/don'ts. For each section note 3 must-include subsections. Apply "show, don't tell" principle. Output: full outline as a table of contents with page estimates and 5 opinion-rules the guide should enforce.

### 58. Rebrand Rollout Plan
**Prompt**: Act as a brand rollout PM who shipped 3 public rebrands. Plan a 90-day rollout for [BRAND_NAME] rebrand across digital, print, physical, and internal touchpoints. Define phases (pre-launch, launch day, post-launch), owner matrix (RACI), risk log, and internal comms plan. Apply change management principles. Output: Gantt-style timeline table plus RACI plus top 5 risks with mitigation.

### 59. Competitive Visual Audit
**Prompt**: Act as a brand strategist running a visual audit. Audit 5 competitors of [BRAND_NAME] in [INDUSTRY]: [COMPETITOR_LIST]. For each capture logo style, color palette, typography, photography, tone, and distinctive device. Plot them on a 2x2 matrix (traditional/modern x serious/playful). Output: audit table with columns Brand | Logo | Color | Type | Photo | Device | Quadrant plus a whitespace recommendation for [BRAND_NAME].

### 60. Category Design Direction
**Prompt**: Act as a category designer a la Play Bigger. Define a category position for [BRAND_NAME] in [INDUSTRY]. Name the category, describe the problem it names, the villain it opposes, the POV, and the visual language that signals the category. Output: category brief plus 3 visual language cues (color, type, imagery) that break from [INDUSTRY] norms and a one-sentence manifesto.

### 61. Typographic Hierarchy Scale
**Prompt**: Act as a type system designer. Define a 7-step typographic scale for [BRAND_NAME] on [PLATFORM]. Choose ratio (1.125, 1.200, 1.250, 1.333, golden), base size (16px web / 17pt iOS / 14sp Android). Define display, h1-h4, body, small, caption with size, line-height, weight, tracking, and usage example. Output: scale table plus CSS variable block pseudo-code and accessibility note for min readable size.

### 62. Grid System Spec
**Prompt**: Act as a grid-discipline designer trained in Swiss typographic tradition. Spec a responsive grid for [BRAND_NAME] on [PLATFORM]: columns (4/8/12), gutters, margins, container max-width, and breakpoints (sm 640, md 768, lg 1024, xl 1280). Define row rhythm (8pt baseline) and alignment rules. Output: grid table per breakpoint plus a 1-paragraph philosophy note on why this grid fits [BRAND_PERSONALITY].

### 63. Motion Design Principles
**Prompt**: Act as a motion designer from Google Material motion team. Define motion principles for [BRAND_NAME] in [PLATFORM] covering easing curves (standard, decelerate, accelerate, sharp), durations (100ms micro, 200ms small, 300ms medium, 500ms large), choreography (stagger, parent/child), and meaning (cause/effect, hierarchy, state). Output: principles doc plus a tokens table with Easing | Duration | Use case.

### 64. Microinteraction Spec
**Prompt**: Act as a UX engineer specializing in microinteractions a la Dan Saffer. Spec a microinteraction for [TRIGGER] in [BRAND_NAME] app. Define trigger, rules, feedback (visual, audio, haptic), loops/modes, and failure state. Apply Aesthetic-Usability and Peak-End. Specify animation timing and easing. Output: spec in Saffer's 4-part structure plus a 5-frame timeline and code pseudo-snippet.

### 65. UX Writing Microcopy
**Prompt**: Act as a UX writer from MailChimp's content design team. Write microcopy for [FLOW] in [BRAND_NAME] app. Cover 10 moments: empty state, loading, success, error, confirmation, onboarding tip, permission request, paywall, logout, undo. Apply voice [BRAND_PERSONALITY], max 8 words per string, plain language. Output: table with Moment | Copy | Rationale plus 2 alternate variants for top 3 moments.

### 66. Design QA Checklist
**Prompt**: Act as a design QA lead reviewing a shipped build of [BRAND_NAME] on [PLATFORM]. Write a 30-point checklist covering spacing, alignment, type fidelity, color, iconography, copy, states, empty/error/loading, accessibility, motion, responsiveness, and edge content (long names, RTL, zero data). For each: what to check and how. Output: checklist table with Area | Check | Severity | Fix.

### 67. Figma Auto Layout Recipe
**Prompt**: Act as a Figma power user teaching auto-layout mastery. Write a recipe to build a responsive [COMPONENT] in Figma using auto-layout, variants, and component properties. Specify direction, spacing, padding, resize rules (hug/fill/fixed), and min/max. Include variant matrix (state x size x style). Output: step-by-step recipe plus variant matrix table and 3 common pitfalls.

### 68. Design System Versioning
**Prompt**: Act as a design system maintainer adopting semver for components. Define versioning rules for [BRAND_NAME] design system: what counts as major (breaking), minor (additive), patch (fix). Include deprecation policy (warn, sunset, remove), changelog format, migration guides, and release cadence. Output: policy doc plus changelog template and a sample v2.0.0 release note for a Button update.

### 69. Style Guide Cheat Sheet
**Prompt**: Act as a design ops lead turning a 200-page guideline into a 1-page cheat sheet for [BRAND_NAME]. Include logo clear space, primary color, primary + secondary type, body text rules, headline rules, photography mood, voice snippet, and don'ts. Optimize for glanceability. Output: cheat sheet text layout with sections labeled and a 5-second test rationale.

### 70. Brand Photography Direction
**Prompt**: Act as a photography art director shooting brand campaigns for magazines. Direct a photo shoot for [BRAND_NAME] in [INDUSTRY]. Specify mood (color, lighting, energy), location type, subjects, wardrobe, props, lens (35mm, 50mm, 85mm), camera settings, shot list (10 shots), and 3 reference photographers. Output: brief plus shot list table with Shot | Subject | Lens | Lighting | Notes.

### 71. Illustration Brief For Hero
**Prompt**: Act as an illustration director commissioning a hero illustration for [BRAND_NAME] landing page. Write a brief: concept, metaphor, audience, usage context, dimensions (3200x1800), color palette tied to brand, style references (3 illustrators), do/don'ts, and delivery format (SVG, PNG). Output: complete brief plus a 1-sentence alt-text example and 3 Midjourney prompts that match the direction.

### 72. Infographic Design Direction
**Prompt**: Act as an information designer inspired by David McCandless. Design an infographic explaining [CONCEPT] for [BRAND_NAME]. Define structure (story arc), visual metaphors, data sources, chart mix, typography, color, and footnote rules. Apply Tufte small multiples where useful. Output: wireframe description with section flow plus a takeaway headline for each section.

### 73. Presentation Template System
**Prompt**: Act as a Keynote/Figma slide systems designer. Build a 20-slide template kit for [BRAND_NAME] to use internally. Slides: cover, agenda, section divider, 2 bullets variants, 2-column, quote, big number, chart, image full, image+text, team, timeline, table, thanks. Each slide: layout note, type hierarchy, and spacing. Output: slide inventory table plus a file naming convention for the deck.

### 74. Webflow Landing Page Spec
**Prompt**: Act as a Webflow designer who ships 5-section landing pages for startups. Design a landing page spec for [BRAND_NAME] for [PRIMARY_ACTION]. Sections: hero, logo bar, feature 3-up, testimonial, pricing, FAQ, CTA, footer. For each: layout, copy length, interactions, breakpoint behavior. Apply F-pattern and progressive disclosure. Output: section-by-section spec table plus a CMS collection plan.

### 75. Conversion Audit For SaaS
**Prompt**: Act as a CRO lead who shipped 40+ experiments at B2B SaaS. Audit [BRAND_NAME] signup funnel from landing to activated. Identify drop-off risks at each step using heuristic eval and Fogg's B=MAT. Prioritize 10 fixes by ICE (Impact, Confidence, Ease). Output: funnel table with Step | Risk | Fix | ICE plus top 3 experiments with hypothesis and metric.

### 76. Hero Image Midjourney Prompt
**Prompt**: Act as a Midjourney art director generating hero images for SaaS landing pages. Write a prompt for [BRAND_NAME] hero image depicting [CONCEPT]. Specify style (editorial, abstract, 3D render, photography), lighting (cinematic, soft window, studio), color palette, composition, subject. Include negative terms to avoid generic AI look. Output: final prompt with --ar 16:9 --style raw --v 6 plus 2 alternates.

### 77. Abstract 3D Render Prompt
**Prompt**: Act as a 3D artist using Midjourney for brand imagery. Write a prompt for an abstract 3D render for [BRAND_NAME] conveying [BRAND_PERSONALITY]. Specify material (glass, chrome, soft matte, liquid), lighting (HDRI, rim, volumetric), shapes (organic blobs, hard surface, geometric), color palette, and renderer reference (Octane, Redshift, Blender cycles). Output: prompt with --ar 16:9 --v 6 plus 3 variations (cool, warm, neutral).

### 78. Editorial Layout Design
**Prompt**: Act as an editorial designer from Bloomberg Businessweek. Design a feature article layout for [BRAND_NAME] publication, topic [TOPIC]. Apply 12-column grid, pull quotes, drop caps, sidebars, caption rules, and photo grid. Specify type pairing, baseline grid, and reading rhythm. Output: page-by-page wireframe description for 6 spreads plus a style rules cheat sheet.

### 79. Annual Report Design Direction
**Prompt**: Act as an annual report designer for a listed company. Direct an annual report for [BRAND_NAME] FY[YEAR], theme [THEME]. Define cover concept, section structure (letter, highlights, strategy, financials), data viz style, photography treatment, infographic approach, and print spec (cover stock, body stock, binding). Output: section outline plus a 2-paragraph concept pitch and photography brief.

### 80. Swag & Print Collateral Kit
**Prompt**: Act as a producer sourcing print and swag for a brand launch. Plan a launch collateral kit for [BRAND_NAME] with 10 items: letterhead, envelope, business card, notebook, sticker sheet, tote, tee, mug, poster, lanyard. For each specify size, material, print method, MOQ, SRP, and lead time. Output: table with Item | Spec | Method | MOQ | SRP | Lead.

### 81. Portfolio Review Critique
**Prompt**: Act as a design hiring manager at a FAANG design team. Review a portfolio for [DESIGNER_ROLE] level [LEVEL]. Score 6 dimensions: craft, problem framing, process, decisions, outcomes, storytelling (1-5 each). Flag 3 strengths and 3 gaps. Suggest specific improvements tied to role expectations. Output: scorecard table plus 5 actionable fixes ranked by expected interview lift.

### 82. Design Career Narrative
**Prompt**: Act as a design career coach who placed 50+ designers at top SaaS. Help [DESIGNER_NAME] craft a career narrative for [TARGET_ROLE]. Define their superpower, 3 story arcs (problem, process, outcome), evidence bank, and 2 elevator pitches (30s, 90s). Tie to [TARGET_COMPANY] values. Output: narrative one-pager plus 3 interview answers to "Tell me about yourself" in escalating depth.

### 83. Client Discovery Questions
**Prompt**: Act as a brand strategist running a discovery workshop. Write 25 discovery questions to ask [CLIENT_NAME] before designing their brand in [INDUSTRY]. Cover business model, audience, competitors, personality, legacy, taboos, metrics. Prioritize questions that surface tension. Output: 25 numbered questions grouped into 5 themes plus a 90-minute workshop agenda.

### 84. Design Sprint Plan
**Prompt**: Act as a GV Design Sprint facilitator. Plan a 5-day sprint for [BRAND_NAME] to solve [CHALLENGE] for [TARGET_USER]. Define goal, sprint questions, long-term goal, participants, daily agenda (Understand, Sketch, Decide, Prototype, Test), decider, and success metrics. Output: day-by-day agenda table plus a pre-sprint checklist and a post-sprint next-steps list.

### 85. Usability Test Script
**Prompt**: Act as a UX researcher running moderated usability tests. Write a test script for [PROTOTYPE] for [BRAND_NAME], targeting [TARGET_USER] performing [PRIMARY_ACTION]. Include intro, warm-up, 4 tasks with success criteria, probing questions, SUS survey, and wrap-up. Apply think-aloud protocol. Output: 45-minute script timeline plus task observation sheet template.

### 86. A/B Test Design Variant
**Prompt**: Act as a conversion designer running A/B tests. Design a variant B for [PAGE] of [BRAND_NAME] to test against control. State hypothesis (If X then Y because Z), change one major variable, predict lift, define primary metric, sample size heuristic, and risks. Output: hypothesis block plus variant spec sketch and success/fail decision rules.

### 87. Landing Page Copy Direction
**Prompt**: Act as a landing page copywriter in the Joanna Wiebe lineage. Write copy for [BRAND_NAME] landing page hero (headline, subhead, CTA), feature section (3 features), and social proof. Use the PAS or Jobs-to-be-Done framework. Match [BRAND_PERSONALITY] voice. Output: structured copy doc plus 3 alternate headlines with angle notes (benefit, emotional, contrarian).

### 88. Pitch Deck Storyboard
**Prompt**: Act as a pitch deck storyteller trained by Reid Hoffman and Sequoia. Storyboard a 12-slide seed deck for [BRAND_NAME] in [INDUSTRY] raising [AMOUNT]. Slides: title, mission, problem, why now, solution, demo, market, business model, traction, team, ask, vision. For each slide write the single takeaway sentence. Output: slide-by-slide storyboard table plus a 60-second verbal pitch script.

### 89. Brand Audit Scorecard
**Prompt**: Act as a brand auditor from a top consultancy. Audit [BRAND_NAME] across 10 dimensions: clarity, distinctiveness, consistency, emotional resonance, relevance, internal alignment, digital presence, messaging, visual system, employee advocacy. Score each 1-10 with evidence. Output: scorecard table plus a SWOT plus top 5 interventions ranked by impact/effort.

### 90. Visual Identity Moodboard
**Prompt**: Act as a brand designer building a moodboard deck for [BRAND_NAME] in [INDUSTRY], personality [BRAND_PERSONALITY]. Describe 12 moodboard tiles covering color, texture, type, photo, graphic, human moment, environment, object, pattern, light, motion, sound. Pull cohesive references (not random Pinterest). Output: tile list with Tile | Reference style | Role in story plus a 2-sentence moodboard narrative.

### 91. Wayfinding Pictogram Set
**Prompt**: Act as a pictogram designer influenced by Otl Aicher (1972 Munich Olympics). Design 12 pictograms for [LOCATION_TYPE] for [BRAND_NAME]: entrance, exit, restroom, info, cafe, elevator, stairs, parking, wifi, accessible, emergency, lost-and-found. Use 24pt grid, 2px stroke, universal metaphors. Output: list with each pictogram's construction notes and a consistency rule sheet.

### 92. Tradeshow Booth Design
**Prompt**: Act as an experiential designer who built booths for SaaStr and CES. Design a 10x20 booth for [BRAND_NAME] in [INDUSTRY]. Define booth goal, brand statement wall, product demo zone, lounge, capture moment (photo op), wayfinding, lighting, signage, and swag station. Apply AIDA. Output: layout sketch plus staff script and 3 lead-capture experiments.

### 93. Photography Retouching Brief
**Prompt**: Act as a retoucher for editorial and product. Write a retouching brief for [PHOTO_SET] for [BRAND_NAME]. Specify skin treatment rules, color grading look, contrast curve, grain, vignette, crop rules, and style reference (3 photographers). Include do/don'ts and dodge/burn guidance. Output: brief plus a LUT/preset spec description and a before/after checkpoint list.

### 94. AI Upscale & Cleanup Prompt
**Prompt**: Act as a photo editor using AI tools (Topaz, Adobe Firefly, Photoshop Generative Fill). Write an editing plan for [PHOTO] for [BRAND_NAME]: upscale target resolution, noise reduction, cleanup targets, background extension, color matching to brand palette, and consistency across set. Output: step-by-step plan plus a prompt for Generative Fill and a QA checklist.

### 95. Product UI Empty State Illustration
**Prompt**: Act as a product illustrator building empty-state art for [BRAND_NAME] app. Brief 5 empty-state illustrations: no messages, no notifications, no search results, no team members, no data yet. For each: metaphor, composition, palette (brand-tied), character usage, and emotional tone. Output: brief table plus one Midjourney prompt per illustration matching the established style.

### 96. Design Mentorship 1:1 Agenda
**Prompt**: Act as a design mentor to junior designers at a growing SaaS. Write a 30-minute 1:1 agenda for [MENTEE_NAME] focused on [TOPIC]. Include check-in, wins, blockers, work review, learning topic, homework, and followups. Provide 5 reflection questions grounded in growth mindset. Output: agenda timetable plus 5 questions and a template for mentee prep notes.

### 97. Design Leadership North Star
**Prompt**: Act as a head of design at a 300-person SaaS. Write a design team north star for [BRAND_NAME] covering mission, values, 3 yearly goals, rituals (crit, research readouts, demos), hiring bar, and operating principles. Tie to [BUSINESS_GOAL]. Output: one-page doc plus a quarterly OKR template and a 5-rule operating principles list.

### 98. Style Exploration With AI
**Prompt**: Act as a creative director using Midjourney to explore brand style for [BRAND_NAME] in [INDUSTRY]. Generate 6 divergent style directions via prompts: minimal, maximal, editorial, retro, futurist, hand-crafted. For each write a full Midjourney v6 prompt and a 1-sentence rationale tied to [BRAND_PERSONALITY]. Output: 6 prompts plus a decision matrix scoring fit, distinctiveness, scalability.

### 99. Design Hiring Rubric
**Prompt**: Act as a design hiring manager at a Series-C startup. Write a hiring rubric for [DESIGN_ROLE] across 6 competencies: craft, product thinking, collaboration, communication, leadership, growth. Define 4 levels (IC3, IC4, IC5, IC6) with behavioral indicators per level. Output: rubric matrix (6 competencies x 4 levels) plus 3 sample interview questions per competency and a calibration rule.

### 100. Design Retrospective Facilitation
**Prompt**: Act as an agile design coach facilitating a quarterly retro for [BRAND_NAME] design team. Plan a 90-minute retro: safety check, timeline recap, What Went Well / What Didn't / Ideas / Actions, dot voting, and commitments. Apply Prime Directive. Output: minute-by-minute agenda plus 10 prompt questions, a template for action items (owner, due, metric), and 3 facilitation anti-patterns to avoid.
