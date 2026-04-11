## AI, Automation & Productivity

### 1. Meta-Prompt Rewriter
**Prompt**: Act as a senior prompt engineer who has shipped production LLM agents at Anthropic scale. Take my raw prompt [INPUT_PROMPT] targeting [GOAL] and rewrite it using role-setting, explicit constraints [CONSTRAINTS], few-shot examples, and chain-of-thought scaffolding. Identify 3 ambiguity risks, 3 failure modes, and propose mitigations. Output as a markdown table with columns: Original, Rewritten, Rationale, Token Delta, Expected Quality Lift (1-10).

### 2. Few-Shot Example Generator
**Prompt**: Act as a prompt engineer specializing in in-context learning. For task [TASK_DESCRIPTION], generate 5 diverse few-shot examples covering edge cases, ambiguous inputs, and adversarial phrasing. Each example must show Input -> Reasoning -> Output. Use semantic diversity (not surface variations). Output as JSON array with fields: id, input, chain_of_thought, expected_output, difficulty (easy/medium/hard), edge_case_type.

### 3. Chain-of-Thought Scaffold
**Prompt**: Act as a reasoning systems researcher. Given problem [PROBLEM] with success metric [SUCCESS_METRIC], design a chain-of-thought scaffold that forces the model to: (1) decompose, (2) identify unknowns, (3) map to known patterns, (4) verify each step, (5) self-critique. Output as a reusable prompt template with [VARIABLES] and numbered thinking steps, plus a self-consistency voting rubric for N=5 samples.

### 4. Tree-of-Thought Planner
**Prompt**: Act as an AI agent architect implementing tree-of-thought reasoning. For decision [DECISION] with constraints [CONSTRAINTS], generate 3 branching strategies, evaluate each branch against [SUCCESS_METRIC] using a 1-10 rubric, prune dominated branches, then deepen the top branch two levels. Output as a markdown tree with evaluation scores, pruning rationale, and final recommended path with confidence interval.

### 5. ReAct Agent Blueprint
**Prompt**: Act as an agentic workflow designer. Build a ReAct (Reason + Act) loop for goal [GOAL] using tools [TOOLS_AVAILABLE]. Define: observation schema, reasoning template, action space, termination condition, max iterations, failure recovery. Include 2 worked examples showing Thought -> Action -> Observation -> Thought cycles. Output as a YAML config plus Python pseudocode for the agent loop with explicit state machine transitions.

### 6. Self-Consistency Voter
**Prompt**: Act as an LLM reliability engineer. Design a self-consistency pipeline for task [TASK] where N=5 reasoning samples are generated, normalized, then majority-voted. Specify: sampling temperature, normalization regex, tie-breaking rule, confidence threshold for escalation to human review. Output as a Python function signature with docstring, followed by a decision tree showing vote aggregation logic and abstention criteria.

### 7. Prompt Debugger
**Prompt**: Act as a prompt debugging specialist. My prompt [PROMPT] is producing output [ACTUAL_OUTPUT] but I expected [EXPECTED_OUTPUT]. Diagnose root cause using a 6-checkpoint framework: role clarity, instruction ordering, example quality, constraint conflicts, output format specification, implicit assumptions. Output as a diagnostic report with severity ratings, exact line-level fixes, and a regression test suite of 3 inputs to verify the fix.

### 8. System Prompt Architect
**Prompt**: Act as a system prompt architect for an AI product used by [USER_PERSONA] to accomplish [GOAL]. Design a system prompt covering: identity, capabilities, hard constraints, soft preferences, refusal policies, output format defaults, and escalation triggers. Keep under 500 tokens. Output as a numbered markdown spec plus the final compiled system prompt in a code block ready for API deployment.

### 9. Instruction Compression
**Prompt**: Act as a prompt optimization engineer focused on token efficiency. Compress my verbose prompt [INPUT_PROMPT] by 40-60% while preserving behavioral fidelity. Techniques allowed: remove hedging, consolidate redundant instructions, replace examples with schemas, use symbolic notation. Output original token count, compressed version, compressed token count, percentage reduction, and a behavioral equivalence checklist of 5 test inputs.

### 10. Prompt Evaluation Rubric
**Prompt**: Act as an LLM evaluation researcher. Build a prompt evaluation rubric for task [TASK_TYPE] scoring: correctness, completeness, format adherence, hallucination rate, instruction following, safety. Each dimension rated 1-5 with concrete anchors. Include inter-rater reliability guidance. Output as a markdown scorecard with rating anchors per dimension, aggregation formula, and a sample scored example showing how to apply the rubric.

### 11. Planner-Executor Split
**Prompt**: Act as an agentic systems architect. For complex goal [GOAL] requiring [TOOLS_AVAILABLE], split cognition across a planner LLM and executor LLM. Planner outputs a JSON plan with dependency graph; executor consumes subtasks and emits structured observations. Define interfaces, error handoff protocol, and replanning triggers. Output as 2 prompt templates (planner, executor) plus a message schema in JSON Schema format with required fields.

### 12. Tool Use Function Schemas
**Prompt**: Act as a function-calling API designer. Given task [TASK] requiring integrations with [TOOLS_AVAILABLE], generate OpenAI-style function schemas for each tool with strict parameter validation, enum constraints, and required/optional flags. Include a tool selection heuristic the LLM should follow. Output as JSON array of function definitions plus a router prompt that teaches the model when to call each tool versus answer directly.

### 13. Multi-Agent Orchestration
**Prompt**: Act as a multi-agent systems designer. Design 3 specialized agents (Researcher, Critic, Synthesizer) collaborating on [GOAL]. Define each agent's system prompt, message format, turn-taking protocol, termination condition, and conflict resolution. Include a shared memory schema. Output as a sequence diagram in ASCII art, followed by YAML definitions for each agent and the orchestration loop in Python pseudocode.

### 14. Reflexion Loop Designer
**Prompt**: Act as an AI agent researcher implementing Reflexion-style self-improvement. After each attempt at [TASK], the agent writes a verbal self-reflection stored in episodic memory and used to improve the next attempt. Design the reflection prompt, memory schema, and retrieval strategy. Output as a 4-component spec: attempt prompt, evaluation prompt, reflection prompt, memory structure in JSON, plus a worked example over 3 iterations showing improvement.

### 15. Agentic RAG Pipeline
**Prompt**: Act as a RAG systems architect. Design an agentic RAG pipeline for knowledge base [KNOWLEDGE_BASE] answering queries like [SAMPLE_QUERY]. Include: query rewriting, hybrid search (BM25 + vectors), reranking, answer generation with inline citations, groundedness check, fallback to web search. Output as a flowchart in Mermaid syntax plus prompt templates for each stage with [VARIABLES] and stop conditions.

### 16. Agent Memory Design
**Prompt**: Act as a cognitive architecture designer for LLM agents. Design 3-tier memory (working, episodic, semantic) for an agent pursuing [LONG_HORIZON_GOAL]. Specify: what to store, retention policy, retrieval triggers, compression strategy, forgetting curve. Output as a memory schema in JSON, a retrieval prompt template, and a consolidation prompt that runs nightly to promote episodic to semantic memory with deduplication logic.

### 17. Agent Failure Recovery
**Prompt**: Act as a resilience engineer for AI agents. Enumerate 10 failure modes for an agent executing [TASK] (hallucinated tools, infinite loops, stale context, rate limits, partial outputs). For each, prescribe detection signal, recovery action, and escalation trigger. Output as a markdown table with columns: Failure Mode, Detection, Recovery, Escalation, Severity (1-5), plus a circuit breaker pattern in pseudocode.

### 18. Budget-Aware Agent
**Prompt**: Act as a cost optimization engineer for LLM agents. Design an agent for [GOAL] with a hard budget of [TOKEN_BUDGET] tokens and [DOLLAR_BUDGET]. Techniques: prompt caching, cheaper model for routing, summarization at thresholds, early termination. Output as a cost accounting table per step, a budget monitor prompt that runs every N turns, and a graceful degradation playbook when budget hits 70%, 90%, 100%.

### 19. Agent Observability Spec
**Prompt**: Act as an LLMOps engineer. Define an observability spec for production agent [AGENT_NAME] including: trace schema, span taxonomy, latency percentiles to track, quality signals, cost per conversation, golden test set, drift alerts. Output as a JSON schema for trace events, 5 dashboard widgets in specification form, and 3 alerting rules with thresholds and on-call runbooks.

### 20. Computer Use Agent Loop
**Prompt**: Act as a computer-use agent designer. Build a loop where the agent sees screenshots, reasons about UI elements, and issues mouse/keyboard actions to accomplish [TASK] on [APPLICATION]. Include: screenshot preprocessing, element grounding prompt, action schema, verification after each action, rollback on error. Output as a state machine diagram plus the core reasoning prompt template with chain-of-thought for visual grounding.

### 21. Weekly Review System
**Prompt**: Act as a GTD coach trained by David Allen. Facilitate my weekly review over [INPUT_DATA] consisting of last week's calendar, task list, and journal. Walk through the 11-step GTD review: collect loose papers, inbox zero, review waiting list, review projects, review someday-maybe. Output as a filled-in review template with: wins, stuck projects, next actions per project, someday items promoted, and 3 focus themes for next week.

### 22. Daily Planning Protocol
**Prompt**: Act as a time-blocking coach in the Cal Newport tradition. Given my top 3 priorities [PRIORITIES] and calendar [CALENDAR], design a time-blocked day from 7am to 9pm. Include deep work blocks (90 min), shallow batching, buffer time (15% slack), and a shutdown ritual. Output as an hourly schedule table with block type (deep/shallow/break/admin), priority served, and a contingency plan if any block is disrupted.

### 23. Eisenhower Matrix Triage
**Prompt**: Act as a productivity coach applying the Eisenhower matrix. Classify my task list [TASK_LIST] into 4 quadrants: Urgent-Important (do now), Not Urgent-Important (schedule), Urgent-Not Important (delegate), Not Urgent-Not Important (delete). For each task include estimated duration, energy level required, and 1-sentence rationale. Output as a 2x2 markdown table plus a prioritized action list for today with time estimates summing to under 6 hours.

### 24. Energy Management Plan
**Prompt**: Act as a peak performance coach applying ultradian rhythm science. Map my energy patterns from [ENERGY_LOG] (7-day self-report of alertness 1-10 hourly) and design a schedule aligning high-cognition work with peaks, admin with troughs, and recovery with valleys. Output as a personal chronotype profile, optimal windows for 4 task types (creative, analytical, social, routine), and a 1-week schedule template.

### 25. Pomodoro Variable Timer
**Prompt**: Act as a deep work researcher customizing Pomodoro technique for my context. Based on task type [TASK], cognitive load [LOAD_1_TO_10], and typical flow duration [FLOW_MINUTES], recommend optimal work/break cycles (classic 25/5, 50/10, 90/20 ultradian). Output as a protocol table with cycle length, break activity (movement/hydration/breath), total session length, and a fatigue escalation rule triggering a longer break.

### 26. Inbox Zero Workflow
**Prompt**: Act as an email productivity coach trained on Merlin Mann's Inbox Zero and 43 Folders. Design a 5-action triage workflow for inbox [INBOX_STATE]: Delete, Delegate, Respond (under 2 min), Defer, Do. Include keyboard shortcuts for Gmail/Outlook, a batch processing schedule (3x daily), and a template library reference. Output as a flowchart plus a daily script naming when to process, for how long, and exit criteria.

### 27. Focus Protocol Design
**Prompt**: Act as an attention researcher combining insights from Cal Newport, Nir Eyal, and Andrew Huberman. Design a distraction-free focus protocol for [GOAL] incorporating: pre-session ritual, environment setup, phone in another room, website blockers, intention setting, post-session review. Output as a 10-step checklist with time estimates, a scoring rubric (1-10) for session quality, and a weekly aggregation template to track trends.

### 28. Habit Stacking Blueprint
**Prompt**: Act as a behavior designer trained at BJ Fogg's Stanford lab. Given my existing anchor habits [ANCHORS] and desired new habits [NEW_HABITS], design a habit stack using the formula "After [ANCHOR], I will [NEW HABIT]". Specify minimum viable dose, celebration, environmental trigger. Output as a habit recipe card for each pairing, a 30-day tracking sheet, and a troubleshooting guide for common failure patterns by day 7, 14, 21.

### 29. OKR Drafting Assistant
**Prompt**: Act as an OKR coach trained by Christina Wodtke. Given my aspiration [ASPIRATION] and current state [CURRENT], draft 1 Objective (inspirational, qualitative) and 3-5 Key Results (measurable, time-bound, stretch). Apply the "confidence level" check: KRs should feel 50% achievable. Output as a markdown OKR card with Objective, KRs, confidence %, leading indicators, and weekly check-in questions for progress tracking.

### 30. Personal Retrospective
**Prompt**: Act as an agile coach facilitating a personal retrospective over period [PERIOD]. Using the Start/Stop/Continue framework plus a "Mad/Sad/Glad" emotional check, walk me through reflection on [INPUT_DATA]. Extract 3 systemic insights, 1 experiment to try next period, and 1 belief to update. Output as a structured retro document with sections, plus a one-line commitment I can post as my north star for next period.

### 31. Email Triage Categorizer
**Prompt**: Act as an email automation specialist. Given inbox sample [EMAIL_LIST], classify each email into: Action Required, FYI, Newsletter, Spam, Client, Internal, Personal. For each, assign priority (P0/P1/P2/P3), estimated response time, and suggested action (reply/archive/delegate/schedule). Output as a JSON array ready to pipe into a Gmail filter or n8n workflow, with a summary of triage stats and recommended bulk actions.

### 32. Reply Template Library
**Prompt**: Act as an executive assistant who handles 500 emails/day. Generate 15 reusable email reply templates covering: meeting decline, meeting reschedule, polite no, information request, status update, intro request, follow-up, payment reminder, feedback request, out-of-office, escalation, thank you, delay notice, handoff, closing loop. Each under 80 words with [VARIABLES]. Output as a markdown snippet library with trigger keywords.

### 33. Cold Email Generator
**Prompt**: Act as a cold outreach strategist trained by Alex Berman and Josh Braun. Write 3 variant cold emails to [PROSPECT] working at [COMPANY] for goal [GOAL]. Each variant uses a different hook (observation, compliment, mutual connection). Rules: under 100 words, 1 CTA, no "hope you're well", personalize first line. Output as 3 email drafts plus subject line A/B variants and a predicted reply rate rationale.

### 34. Unsubscribe Automation
**Prompt**: Act as a digital declutter coach. Given my newsletter subscriptions [SUBSCRIPTIONS] with open rates [OPEN_RATES] and last-click dates, classify each as Keep/Unsubscribe/Downgrade-Frequency. For unsubscribes, draft a one-shot bulk action plan using Unroll.me or manual filters. Output as a decision table, a Gmail search query that surfaces unread newsletters older than 7 days, and a weekly "prune ritual" script of 15 minutes.

### 35. Email Follow-Up Sequencer
**Prompt**: Act as a sales enablement specialist designing follow-up cadences. For initial email to [PROSPECT] with goal [GOAL], design a 5-touch sequence over 14 days using varied channels and angles (value-add, case study, break-up, different stakeholder, soft ask). Output as a table with columns: Day, Channel, Subject, Body (80 words), CTA, then an "exit criteria" section for when to stop the sequence gracefully.

### 36. Meeting Decline Diplomat
**Prompt**: Act as a chief of staff protecting a founder's calendar. Given meeting request [REQUEST] and my calendar context [CALENDAR], draft a diplomatic decline that: acknowledges the requester, offers an async alternative (Loom, doc comments), proposes a different time if critical, or redirects to a better contact. Output as 3 tiered replies (soft decline, hard decline, redirect) each under 60 words with tone notes.

### 37. Email Summarizer Agent
**Prompt**: Act as a personal intelligence briefing agent. Given today's inbox [EMAIL_THREADS], produce a morning briefing with: 3 must-reply items (with draft replies), 5 FYI items (one-line summaries), 2 items requiring decisions (with options), commitments I made this week, and open questions awaiting me. Output as a markdown briefing under 500 words formatted for 30-second scan with inline [link] placeholders.

### 38. Newsletter Writer Assist
**Prompt**: Act as a B2B newsletter editor in the style of Morning Brew. Given raw input [RAW_NOTES] on topic [TOPIC] for audience [AUDIENCE], draft a 400-word newsletter with: witty subject line, 1-sentence hook, 3-beat narrative, 1 data point, 1 actionable takeaway, 1 CTA. Tone: smart-casual, pun-tolerant. Output as ready-to-send markdown plus 3 subject line variants with predicted open rate rationale.

### 39. Email Thread Summarizer
**Prompt**: Act as an executive briefing analyst. Given long email thread [THREAD], produce: 1-sentence TL;DR, chronological decision log, unresolved questions, commitments by person, next action owner, and a suggested reply continuing the thread. Flag any contradictions between participants. Output as a structured brief with sections and a JSON block of {person, commitment, due_date, status} for tracking in a task manager.

### 40. Bulk Reply Generator
**Prompt**: Act as a community manager handling [NUMBER] similar inbound emails on topic [TOPIC]. Generate 1 master reply template, then 5 personalized variants that adapt tone, length, and specific details based on sender signals [SIGNALS]. Include a classification rule for when to use each variant. Output as a routing table plus the master template with [PERSONALIZATION_VARIABLES] and a quality check against 3 sample inputs.

### 41. Meeting Prep Brief
**Prompt**: Act as a chief of staff preparing a principal for meeting [MEETING]. Given attendees [ATTENDEES], goal [GOAL], and background [CONTEXT], produce a 1-page brief containing: desired outcome, top 3 talking points, likely objections with pre-planned responses, questions to ask, decisions to make, 1-slide mental model, and post-meeting action commitments. Output as a structured markdown brief under 400 words.

### 42. Meeting Notes to Actions
**Prompt**: Act as a meeting scribe extracting structured signal from noise. Given raw transcript [TRANSCRIPT] of meeting about [TOPIC], extract: decisions made (with rationale), action items (owner + due date), open questions, parking lot items, and sentiment shifts. Output as a JSON object with arrays for each category, plus a human-readable summary under 200 words and 3 draft follow-up messages to action owners.

### 43. 1:1 Agenda Builder
**Prompt**: Act as an engineering manager coach. Build a 30-minute 1:1 agenda between [MANAGER] and [REPORT] given recent context [CONTEXT]. Structure: 5 min personal check-in, 10 min report's agenda, 10 min manager's agenda, 5 min feedback loop. Include 3 open-ended question prompts and a growth area touchpoint. Output as a shared doc template with time boxes, question bank, and a note-taking section for action items.

### 44. Meeting Decliner Rubric
**Prompt**: Act as a productivity auditor applying Jeff Bezos' "two-pizza" and "is this the best use of an hour?" tests. Given meeting [MEETING] with agenda [AGENDA], score on 5 criteria (clear goal, right attendees, prep material, decision needed, async alternative). If under 15/25, draft a decline email with async alternative. Output as a scorecard plus go/no-go recommendation and the decline email if applicable.

### 45. Stand-Up Summary Bot
**Prompt**: Act as a Scrum master automating daily stand-ups. Given yesterday's work [YESTERDAY], today's plan [TODAY], and blockers [BLOCKERS] from team [TEAM_MEMBERS], synthesize a single team-level stand-up summary highlighting cross-dependencies, shared blockers, and risks to sprint goal. Output as a Slack-ready markdown message under 300 words with @mentions for owners and a "needs attention" section for the Scrum master.

### 46. Retrospective Facilitator
**Prompt**: Act as an agile retrospective facilitator trained in Esther Derby's techniques. Given sprint data [SPRINT_DATA] and team feedback [FEEDBACK], run a "4 Ls" retro (Liked, Learned, Lacked, Longed For). Cluster themes, surface top 3 experiments for next sprint, and define success metrics for each. Output as a retro summary document with clustered themes, voted priorities, and a SMART experiment spec for each action item.

### 47. Action Item Enforcer
**Prompt**: Act as an accountability coach. Given my action items from last meeting [LAST_ACTIONS] and current status [STATUS], diagnose why incomplete items slipped (forgot, blocked, deprioritized, unclear). For each, prescribe recovery: reschedule, delegate, descope, or kill. Output as a status table with columns: Action, Status, Slip Reason, Recovery, New Due Date, Confidence, plus a systemic recommendation to prevent repeat patterns.

### 48. Async Meeting Converter
**Prompt**: Act as a remote work strategist in the GitLab handbook tradition. Given meeting [MEETING] with goal [GOAL], redesign it as an async-first workflow using: shared doc for context, Loom video for nuance, threaded comments for discussion, decision log for outcomes. Output as an async protocol with document template, contributor instructions, deadline, tie-breaker rule, and the Slack message inviting participation with clear expectations.

### 49. Stakeholder Update Draft
**Prompt**: Act as a product manager writing a weekly stakeholder update for [PROJECT]. Given progress [PROGRESS], blockers [BLOCKERS], and upcoming milestones [MILESTONES], draft an update using the "RAG + headline" format: traffic light status, 1-line headline, 3 bullets on progress, 3 bullets on risks, 1 ask. Output as a ready-to-send markdown under 250 words with a TL;DR at top and a metrics table.

### 50. Meeting ROI Calculator
**Prompt**: Act as a productivity economist. Given recurring meeting [MEETING] with [ATTENDEES] hourly rates averaging [RATE], duration [DURATION], and outcomes [OUTCOMES], compute cost per meeting, cost per decision, cost per action item produced. Benchmark against a 10x ROI threshold. Output as a cost-benefit table, a verdict (keep/shrink/kill), and 3 optimization levers ranked by savings potential with estimated dollar impact.

### 51. Project WBS Decomposer
**Prompt**: Act as a project manager certified in PMBOK. Decompose project [PROJECT] with goal [GOAL] into a work breakdown structure of at most 3 levels. Each leaf task must be 4-16 hours, have clear acceptance criteria, owner, dependencies, and effort estimate. Apply the 100% rule (children sum to parent). Output as an indented markdown tree plus a dependency graph in Mermaid syntax and a critical path highlight.

### 52. First Principles Decomposer
**Prompt**: Act as a first-principles thinker in the Elon Musk / Richard Feynman tradition. Given problem [PROBLEM], strip it to fundamental truths by asking "why" 5 times and "what must be true?" Identify assumptions, test each against physics/economics/logic, then rebuild a solution from atoms. Output as a 3-column table (Assumption, Challenge, First Principle) plus a reconstructed problem statement and a novel solution path.

### 53. MoSCoW Prioritizer
**Prompt**: Act as an agile product coach. Given backlog [BACKLOG] for sprint with capacity [CAPACITY], classify each item as Must/Should/Could/Won't using the MoSCoW method. For each Must, validate with the "release-breaking" test. For each Won't, add rationale for deferral. Output as a prioritized markdown table with effort estimates, cumulative capacity check, and a risk callout for any Musts exceeding 60% of capacity.

### 54. Pre-Mortem Analysis
**Prompt**: Act as a risk analyst running a Gary Klein-style pre-mortem. Imagine project [PROJECT] failed catastrophically 6 months from now. Brainstorm 15 plausible failure causes across 5 categories: technical, people, market, execution, external. Rank by likelihood x impact. For top 5, propose early warning indicators and mitigations. Output as a risk register with columns: Cause, Category, Likelihood (1-5), Impact (1-5), Signal, Mitigation, Owner.

### 55. Gantt Timeline Builder
**Prompt**: Act as a project scheduler. Given tasks [TASKS] with durations and dependencies [DEPENDENCIES], build a Gantt timeline starting [START_DATE] with a hard deadline [DEADLINE]. Apply critical path method, add 15% buffer, flag resource conflicts. Output as an ASCII Gantt chart, a critical path list, milestone dates, and a slippage playbook describing what to compress if the timeline slips by 1 week.

### 56. RACI Matrix Designer
**Prompt**: Act as an organizational design consultant. For project [PROJECT] with deliverables [DELIVERABLES] and stakeholders [STAKEHOLDERS], build a RACI matrix assigning Responsible, Accountable (exactly 1), Consulted, Informed. Apply validation rules: every deliverable has exactly one A, no person is over-allocated. Output as a markdown table with deliverables as rows, people as columns, plus a conflict report and redesign suggestions if any rule is violated.

### 57. User Story Writer
**Prompt**: Act as a senior product manager trained by Marty Cagan. For feature [FEATURE] serving user [PERSONA], write user stories using "As a [persona], I want [capability] so that [outcome]" plus Gherkin-format acceptance criteria (Given/When/Then). Include edge cases, error states, and non-functional requirements. Output as a user story card with title, narrative, 5 acceptance criteria, effort estimate, and definition-of-done checklist.

### 58. Scope Creep Defender
**Prompt**: Act as a project manager defending scope. Given original scope [ORIGINAL_SCOPE] and new request [NEW_REQUEST], run a scope impact analysis: does it serve the core goal? What gets delayed/cut? Estimate time/cost delta. Draft a stakeholder conversation script offering 3 options (absorb, trade-off, defer). Output as a scope change request form plus the verbal script with 3 pre-planned responses to pushback.

### 59. Dependency Mapper
**Prompt**: Act as a systems architect mapping project dependencies. Given tasks [TASKS], identify hard dependencies (must finish before), soft dependencies (preferred before), and parallel tracks. Detect cycles, bottlenecks, and single points of failure. Output as a directed graph in Mermaid syntax, a topological sort of execution order, a list of "unblocker" tasks that free the most downstream work, and a parallelization recommendation.

### 60. Milestone Retrospective
**Prompt**: Act as a project postmortem facilitator. Given completed milestone [MILESTONE] with data [ACTUAL_VS_PLAN], diagnose variance using the 5 Whys on any estimate miss greater than 20%. Extract lessons across people/process/tools. Output as a postmortem report with: timeline, key events, what went well, what didn't, root causes, action items with owners and due dates, and 3 process improvements to propagate to future projects.

### 61. Zettelkasten Atomizer
**Prompt**: Act as a knowledge management coach trained in the Zettelkasten method of Niklas Luhmann. Given source note [SOURCE_NOTE], atomize it into 3-7 permanent notes, each capturing exactly one idea in my own words, with a unique ID (YYYYMMDDHHMM), a descriptive title, and explicit [[wiki-links]] to related notes. Output as markdown files ready for Obsidian with frontmatter, body under 300 words each, and a link section suggesting 3 connections.

### 62. Second Brain PARA Setup
**Prompt**: Act as a productivity coach certified in Tiago Forte's Building a Second Brain. Given my current information chaos [CURRENT_STATE], design a PARA structure (Projects, Areas, Resources, Archive) for Notion/Obsidian. Define: what belongs where, capture workflow (progressive summarization), weekly maintenance ritual. Output as a folder tree, naming conventions, a CODE method checklist (Capture-Organize-Distill-Express), and a 14-day onboarding plan.

### 63. Obsidian Graph Builder
**Prompt**: Act as an Obsidian power user. Given my notes on topic [TOPIC], design an MOC (Map of Content) note that serves as a curated entry point, plus suggested tags, dataview queries for dynamic sections, and a template for note frontmatter. Output as a ready-to-paste MOC markdown file with sections, inline dataview queries in code blocks, and 3 canvas layout suggestions for visual thinking.

### 64. Smart Note Taking
**Prompt**: Act as a researcher applying Sonke Ahrens' "How to Take Smart Notes". Given source [SOURCE], produce: fleeting notes (quick captures), literature notes (bibliographic summary in my words under 200 words), and permanent notes (atomic insights with links). Distinguish reference, claim, and my original thought. Output as 3 markdown sections with clear boundaries, citation in plain text, and 2 questions the source opens up.

### 65. Progressive Summarization
**Prompt**: Act as a knowledge distillation engineer. Given article [ARTICLE], apply 4 layers of progressive summarization: (1) highlight key passages, (2) bold the most important, (3) italicize the core claim, (4) write a 3-sentence executive summary. Each layer reduces by ~5x. Output as the full article with layer 1-3 markup preserved, followed by the level 4 summary and 1 "so what" action implication.

### 66. Literature Review Synthesizer
**Prompt**: Act as a PhD research assistant. Given papers [PAPERS] on topic [TOPIC], produce a literature review synthesizing: shared framings, points of disagreement, gaps in the field, methodological patterns, and open questions. Use thematic clustering, not chronological ordering. Output as a 500-word review with inline citations, a comparison matrix of papers on 5 dimensions, and 3 research questions worth pursuing next.

### 67. Knowledge Graph Query
**Prompt**: Act as a knowledge graph architect. Given my note corpus [CORPUS] and question [QUESTION], design a graph traversal that surfaces relevant notes via tag intersection, backlink density, and semantic similarity. Output as a pseudocode query, a ranked list of top 10 relevant notes with relevance scores and rationale, and a synthesis paragraph answering the question grounded in those notes with inline [[links]].

### 68. Daily Note Template
**Prompt**: Act as a journaling coach combining Bullet Journal and Morning Pages practices. Design a daily note template for Obsidian containing: 3-sentence intention, top 3 tasks, time log, gratitudes, wins, what I learned, tomorrow's focus, mood 1-10, energy 1-10. Include dataview queries to pull today's tasks from project notes. Output as a markdown template with frontmatter, sections, and inline queries ready to use in a daily note plugin.

### 69. Flashcard Generator
**Prompt**: Act as a learning scientist building spaced repetition decks. Given source material [SOURCE], generate 15 Anki-style flashcards using the minimum information principle (one fact per card), avoiding verbatim copying. Mix cloze deletions, Q&A, and image occlusion suggestions. Output as a CSV with columns Front, Back, Tags, Type, plus 3 sample cards in markdown preview showing front/back and a difficulty rating per card.

### 70. Commonplace Book Entry
**Prompt**: Act as Ryan Holiday's commonplace book curator. Given passage [PASSAGE] from author [AUTHOR], craft a commonplace entry containing: the quote verbatim, source citation, my paraphrase in plain language, 1 personal connection, 1 actionable principle, and 3 tags for future retrieval. Output as a markdown note with YAML frontmatter suitable for Obsidian, body under 300 words, and a "future trigger" note describing when to recall this.

### 71. Pros Cons Matrix
**Prompt**: Act as a decision analyst. For decision [DECISION] between options [OPTION_A] and [OPTION_B], build a weighted pros/cons matrix: list factors, assign weights (1-10) based on my values [VALUES], score each option per factor (-5 to +5), compute weighted totals. Include gut-check via premortem and reversibility test (one-way vs two-way door). Output as a markdown table, weighted score, and a narrative recommendation.

### 72. Decision Journal Entry
**Prompt**: Act as a decision coach trained on Annie Duke's "Thinking in Bets". For upcoming decision [DECISION], draft a decision journal entry capturing: situation, options considered, option chosen, expected outcome with probability, alternative I rejected and why, emotional state, what would change my mind. Output as a structured journal entry template in markdown with YAML frontmatter (date, stakes, confidence) for future review and learning.

### 73. Red Team Critique
**Prompt**: Act as a hostile red team attacking my plan [PLAN]. Steel-man 5 critiques: is the premise wrong? Is the evidence weak? Are assumptions hidden? Is the execution path flawed? What does the smartest opponent say? Be brutally honest, not polite. Output as 5 numbered critiques, each with: claim, evidence, severity (1-5), and a specific action I should take to address or dismiss the critique.

### 74. Inversion Thinking
**Prompt**: Act as Charlie Munger applying inversion. For goal [GOAL], flip the question: instead of "how do I achieve this?" ask "how would I guarantee failure?" Enumerate 10 failure paths, then invert each into an avoidance rule. Output as a 2-column table (Failure Path, Avoidance Rule) plus a top-3 priority list of avoidance rules ranked by likelihood and a daily checklist question to keep me aligned.

### 75. Opportunity Cost Calculator
**Prompt**: Act as an economist applying opportunity cost reasoning. Given choice [CHOICE] requiring time investment [TIME] and money [MONEY], enumerate the next 3 best alternatives, estimate their expected value, and compute opportunity cost as value forgone. Apply the "hell yes or no" filter from Derek Sivers. Output as a comparison table, an opportunity cost figure in dollars and hours, and a decision recommendation with confidence.

### 76. Second Order Thinking
**Prompt**: Act as Howard Marks applying second- and third-order thinking. For action [ACTION], trace consequences across orders: first (immediate), second (reactions), third (systemic), fourth (long tail). For each order, identify stakeholder reactions and feedback loops. Output as a cascading markdown outline with orders as headers, consequences as bullets, and a summary of "what most people miss" plus a decision modifier if any order reveals hidden risk.

### 77. Expected Value Calculator
**Prompt**: Act as a poker player applying expected value math. Given bet [BET] with outcomes [OUTCOMES], probabilities [PROBABILITIES], and payoffs [PAYOFFS], compute EV, variance, and Kelly criterion bet size relative to bankroll [BANKROLL]. Apply the "resulting" check (good decision vs good outcome). Output as a calculation table, a narrative explaining whether the bet is +EV, and a recommended action with position sizing.

### 78. Moral Compass Check
**Prompt**: Act as an ethics advisor applying multiple frameworks. For dilemma [DILEMMA], evaluate under 4 lenses: consequentialism (outcomes), deontology (duties), virtue ethics (character), care ethics (relationships). Note where they converge and diverge. Output as a 4-column analysis plus a reconciled recommendation with the dominant framework justified, a "stranger test" (would I be comfortable if this were front-page news), and a reversibility clause.

### 79. Pre-Commitment Device
**Prompt**: Act as a behavioral economist in the Ulysses contract tradition. Given temptation [TEMPTATION] that undermines goal [GOAL], design a pre-commitment device: stake (money, reputation), referee, verification method, reward/punishment schedule, exit conditions. Tools: Beeminder, StickK, accountability partner. Output as a contract document with stake amount, verification rule, weekly check-in schedule, and an "if-then" escape clause for legitimate exceptions.

### 80. Sunk Cost Escape
**Prompt**: Act as a rationality coach identifying sunk cost fallacy. Given commitment [COMMITMENT] with [SUNK_INVESTMENT] already spent, evaluate forward-only: if I were starting today with current information, would I make this investment? Apply the "freshman year" test. Output as a 3-step analysis (forget past, assess present, project future EV), a verdict (continue/quit/pivot), and a narrative script to communicate the decision to stakeholders.

### 81. Zapier Workflow Blueprint
**Prompt**: Act as an automation architect specializing in Zapier. Design a zap for goal [GOAL] connecting [APPS]. Specify: trigger, filters, paths, formatter steps, action apps, error handling, testing plan. Estimate task consumption per month. Output as a step-by-step blueprint in a numbered list, field-level mapping for the first and last step, a JSON-like pseudocode of the workflow, and a cost estimate on the relevant Zapier plan.

### 82. n8n Node Chain
**Prompt**: Act as an n8n workflow engineer. Build a workflow for [TASK] using trigger [TRIGGER] and actions [ACTIONS]. Specify: node types, expressions for data mapping (JavaScript), conditional branches (IF nodes), error workflow, credentials required. Self-host recommendation if volume is high. Output as a numbered node list with expressions, a JSON export snippet for the key nodes, and a test payload to verify the workflow end-to-end.

### 83. Make Scenario Design
**Prompt**: Act as a Make.com (Integromat) power user. Design a scenario automating [PROCESS] with modules [MODULES]. Use aggregators, iterators, routers, data stores. Specify operation cost, error handlers, scheduling. Output as a module-by-module spec with connection notes, a flow diagram in ASCII showing routers and aggregators, an operation count estimate, and 3 optimization tips to reduce operations consumed per run.

### 84. Apple Shortcuts Recipe
**Prompt**: Act as an Apple Shortcuts power user. Build a Shortcut for [TASK] usable from Siri, Share Sheet, or Widget. Use actions: Get Contents of URL, Scripting, Conditional, Dictionary. Include a settings variable for customization. Output as a step-by-step action list with parameters, a test case, the Siri phrase to invoke, a home-screen icon suggestion, and a fallback if a required service is unavailable.

### 85. Raycast Script Command
**Prompt**: Act as a Raycast extension developer. Build a script command in Bash or Node.js for task [TASK] with arguments [ARGS]. Follow Raycast conventions: schema version, title, mode (silent/fullOutput/inline), refreshTime. Handle errors gracefully. Output as the full script file content with the required metadata comment header, error handling, a usage example, and installation instructions for dropping into ~/.config/raycast/scripts.

### 86. Cron + Shell Pipeline
**Prompt**: Act as a devops engineer scheduling a daily automation. For task [TASK], write a shell script that runs reliably from cron on macOS/Linux: PATH handling, logging with timestamp, lock file to prevent overlap, failure alerts via email or webhook. Output as a complete bash script with shebang, a crontab line specifying schedule, a logrotate suggestion, and a manual test command with expected output.

### 87. GitHub Actions Workflow
**Prompt**: Act as a CI/CD engineer writing a GitHub Actions workflow for task [TASK] triggered on [TRIGGER]. Include: matrix builds, caching, secrets management, concurrency control, artifact upload, failure notifications. Output as a complete workflow YAML file saved to .github/workflows/[name].yml with comments explaining each step, a test branch strategy, and a cost estimate in minutes per month under normal load.

### 88. iOS Shortcuts Automation
**Prompt**: Act as an iOS automation expert. Build a personal automation triggered by [TRIGGER] (time, arrival, app open, focus mode) that performs [ACTIONS]. Use Shortcuts' Automation tab, not manual invocation. Include guard conditions to avoid spam. Output as a step-by-step action list, trigger configuration, test plan, and a privacy note on what data the automation accesses plus a disable/snooze plan for edge cases.

### 89. Webhook Middleware Design
**Prompt**: Act as a serverless architect. Design a webhook middleware that receives events from [SOURCE] and dispatches to [DESTINATIONS]. Use Cloudflare Workers, Deno Deploy, or AWS Lambda. Handle: signature verification, idempotency, retries with exponential backoff, dead letter queue. Output as a pseudocode function, the endpoint contract in OpenAPI snippet form, a retry policy table, and an alerting rule for the DLQ hitting a threshold.

### 90. RSS to Action Pipeline
**Prompt**: Act as a content automation engineer. Build a pipeline that watches RSS feed [FEED] for keyword [KEYWORD] and triggers action [ACTION] (email, Notion page, Slack message). Use RSS.app, n8n, or a cron Python script. Include dedupe via GUID store. Output as a workflow blueprint with components, a Python implementation skeleton (50 lines), state storage schema, and a backfill strategy for the first run.

### 91. Feynman Technique Coach
**Prompt**: Act as a Feynman Technique coach. I want to learn [TOPIC] by teaching it to a 12-year-old. Step 1: ask me 5 probing questions to find gaps in my current understanding. Step 2: grade my explanation attempt [ATTEMPT] on simplicity, accuracy, and analogy quality. Step 3: point to exactly where I leaned on jargon and suggest plain-language alternatives. Output as a graded rubric plus a rewritten 200-word explanation.

### 92. Spaced Repetition Planner
**Prompt**: Act as a learning scientist applying SM-2 spaced repetition to material [MATERIAL]. Given my study time [DAILY_MINUTES] and deadline [DEADLINE], build a review schedule across 7 intervals (1d, 3d, 7d, 14d, 30d, 60d, 120d). Include new-card introduction rate and retention target. Output as a daily schedule table for the next 30 days with cards to review, cards to introduce, and estimated time per session.

### 93. Skill Roadmap Builder
**Prompt**: Act as a skill acquisition coach applying Josh Kaufman's "First 20 Hours" and K. Anders Ericsson's deliberate practice. Given target skill [SKILL] and current level [LEVEL], build a 20-hour roadmap with: decomposition into sub-skills, order of learning by leverage, practice drills with feedback loops, plateaus to expect. Output as a milestone-based plan, a daily drill template, and a self-assessment rubric with 5 levels.

### 94. Learning Contract
**Prompt**: Act as a self-directed learning coach applying Malcolm Knowles' andragogy. For goal [LEARNING_GOAL] over period [TIMEFRAME], draft a learning contract covering: objectives, resources, strategies, evidence of completion, evaluation criteria. Include an accountability partner clause and a weekly reflection prompt. Output as a signed-ready contract document in markdown with sections, measurable outcomes, and a midpoint checkpoint review plan.

### 95. Deliberate Practice Session
**Prompt**: Act as a deliberate practice coach. Design a 60-minute practice session for skill [SKILL] at level [LEVEL]. Include: warm-up (5 min), targeted drill on weakness [WEAKNESS] (30 min) with immediate feedback loops, integration exercise (15 min), cool-down reflection (10 min). Output as a timed session plan with drill specifications, success criteria per segment, a feedback capture template, and the next session's focus area based on today's results.

### 96. Reading Note Protocol
**Prompt**: Act as a power reader applying Mortimer Adler's "How to Read a Book". For book [BOOK], run the 4 levels: elementary (scan), inspectional (preview TOC and conclusions), analytical (structured notes), syntopical (compare with other books on the topic). Output as a pre-read 15-minute inspection note, a reading plan with time budget per chapter, and a template for analytical notes with pillars: structure, key claims, evidence, objections.

### 97. Question-Led Learning
**Prompt**: Act as a Socratic tutor. I want to learn [TOPIC] by answering questions rather than consuming content. Generate a 10-question curriculum from beginner to expert, each question designed to force a concept discovery, with a hint unlocked after 2 minutes of thinking. Output as a numbered question list, difficulty progression, hint bank, and a self-grading rubric for when I should move to the next question.

### 98. Teaching Doc Generator
**Prompt**: Act as a technical writer. Transform my rough notes on [TOPIC] into a teaching document for audience [AUDIENCE]. Use the "inverted pyramid" plus Diataxis framework: is this a tutorial, how-to, explanation, or reference? Structure accordingly. Output as a markdown document with TOC, prerequisites, learning outcomes, worked example, exercises with solutions, further reading, and a self-check quiz of 5 questions.

### 99. Mental Model Index Builder
**Prompt**: Act as a polymath building a personal mental model latticework in the Munger tradition. Given my field [FIELD] and current models [CURRENT_MODELS], identify 10 high-leverage models missing from my latticework across disciplines (physics, biology, economics, psychology, math). For each, provide: 1-sentence definition, when to apply, canonical example, link to related models. Output as an indexed markdown database ready for Obsidian.

### 100. Meta-Learning Retrospective
**Prompt**: Act as a meta-learning coach. Over the last month I learned [WHAT] via [METHOD] with results [RESULTS]. Diagnose what worked, what wasted time, and which techniques to double down on. Apply Scott Young's ultralearning principles (directness, drill, feedback, retrieval). Output as a meta-learning retrospective report with: method scorecard, time audit, retention check via recall test, and a revised learning protocol for the next month with 3 experiments.
