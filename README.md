# Mr. Prompter

> **Prompt engineering toolkit:** 7 specialized modes, 28 techniques, 58 ready-to-use prompts, security-first assessment, model selection framework.

Write prompts. Audit them. Fix broken sessions. Extract reusable templates from conversations. Pick the right AI model. All in one skill.

---

## tl;dr — 3 Steps to Your First Prompt

```
1. "Write me a prompt for [task]"          → GENERATE mode
2. Paste your existing prompt + "check this" → VERIFY mode  
3. Paste a conversation log + "what went wrong" → DIAGNOSE mode
```

That's it. No setup, no config files. Just describe what you need.

---

## What This Is (In Plain English)

You know how talking to AI sometimes feels like throwing spaghetti at the wall? You try different phrasings, correct misunderstandings, iterate until it works — then next time you start from scratch?

**This skill fixes that.**

It has 7 modes for different situations. You describe what you need, the skill picks the right approach and produces a production-quality prompt — or analyzes why your last session derailed.

### The Core Pattern

```
You describe the task → Skill builds the optimal prompt → You use the prompt with any AI
                                                        ↓
                                           Session went wrong? → DIAGNOSE
                                           Session went right? → EXTRACT (save it)
```

---

## 7 Modes at a Glance

| Mode | You say... | You get... | When to use |
|------|-----------|------------|-------------|
| **GENERATE** | "Write me a prompt for X" | Ready-to-use prompt + model recommendation + security check | Starting from scratch |
| **VERIFY** | "Check this prompt" / "Audit this" | Score (0-10) + specific issues + fixes | Before deploying a prompt |
| **IMPROVE** | "Make this prompt better" | Rewritten prompt + what changed + why | Iterating on existing prompt |
| **CHAIN** | "Deep analysis of X" / "Build a prompt chain" | Multi-phase analysis (2-4 sequential prompts) | Complex topics needing multiple angles |
| **MODEL SELECT** | "Which model for X?" | Primary + alternative + rationale | Choosing the right AI model |
| **DIAGNOSE** | "What went wrong?" / "Analyze this session" | Exact failure points + concrete patches + metrics | After a session derailed |
| **EXTRACT** | "Turn this chat into a prompt" | Reusable prompt from conversation | Saving successful patterns |

### Quick Decision Guide

```
Starting new task? ────────────────→ GENERATE
Have a prompt, want to check it? ──→ VERIFY
Have a prompt, want to improve it? → IMPROVE
Need deep multi-angle analysis? ───→ CHAIN
Don't know which AI to use? ───────→ MODEL SELECT
Session went wrong? ───────────────→ DIAGNOSE
Session went great, save it? ──────→ EXTRACT
```

---

## Examples

### Example 1: GENERATE — "I need a prompt for code review"

**You:** "Write me a prompt for an AI code reviewer that checks Python code for bugs, style issues, and performance problems"

**Skill does:**
1. Security scan (no injection risks detected)
2. Picks techniques: Role Prompting + Task Decomposition + Constrained Output
3. Recommends: Claude 4 Sonnet (primary) / DeepSeek R1 (alternative for speed)
4. Delivers 7-section output: Security Assessment → Prompt → Model Recommendation → Technique Analysis → Testing Guide → Questions → Save Pattern?

**You get:** A complete system prompt you paste into Claude/ChatGPT/whatever.

---

### Example 2: DIAGNOSE — "The AI keeps ignoring my instructions"

**You:** Paste a conversation log where you asked Claude to summarize articles in 3 bullet points, but it kept writing full paragraphs and adding opinions you didn't ask for.

**Skill does:**
1. Parses the log: 8 turns, 4 correction turns (50% wasted)
2. Identifies failure patterns:
   - **F01 Format drift**: Started with bullets, drifted to paragraphs
   - **H02 Hallucination**: Added analysis not present in source
   - **I02 Partial compliance**: Followed length rule but ignored format
3. Produces patches:
   ```
   [CRITICAL] F01 Format: Add "Output MUST be exactly 3 bullet points, 
   each under 15 words. No paragraphs. No analysis." after the task line.
   
   [HIGH] H02 Scope: Add "Use ONLY information from the provided text. 
   Do not infer, analyze, or add opinions not explicitly stated."
   ```
4. Delivers: Session metrics + chronological failures + prioritized patches + prevention guide

**You get:** Exact text to paste into your prompt to fix the issues.

---

### Example 3: EXTRACT — "This chat worked great, save it"

**You:** Paste a 12-turn conversation where you iteratively refined an image generation prompt with Midjourney. The final result was perfect but required a lot of back-and-forth.

**Skill does:**
1. Identifies pattern: Tone Calibration (D) + Format Negotiation (B)
2. Extracts: "You are a Midjourney prompt engineer specializing in [genre]..." + successful output format + 2 best examples + constraints learned from rejections
3. Validates: 640 tokens, covers all critical constraints, produces equivalent output
4. Labels what's variable (genre, subject, mood) vs constant (structure, style rules)

**You get:** A 640-token prompt you can reuse — just swap in new genre/subject/mood.

---

### Example 4: CHAIN — "Deep analysis of a market"

**You:** "I need to understand the competitive landscape for AI coding assistants. Do a deep analysis."

**Skill does:**
1. Assesses complexity → triggers CHAIN mode
2. Builds 3-phase chain:
   - **Phase 1** (2 perspectives): Product Manager lens + Engineer lens, each with 3 specific questions
   - **Phase 2** (Blind Spots): Find what both perspectives missed
   - **Phase 3** (Distillation): Consolidate into actionable report
3. Writes chain to file `ai-coding-assistants-chain.md`

**You get:** A file with 3 prompts. Run them sequentially in one chat, each builds on the previous.

---

## Project Structure

```
prompt-engineer/
├── SKILL.md              # Core skill definition (entry point)
├── README.md             # This file
├── knowledge/
│   └── index.json        # Searchable index of 28 techniques
├── references/           # Knowledge base (loaded on demand)
│   ├── context.md        # Overview, platform rules, model quick-ref
│   ├── meta.md           # Principles, anti-patterns, emergency fixes
│   ├── system.md         # Architecture, hierarchy, safety, injection defense
│   ├── reasoning.md      # CoT, ToT, CoV, Reflexion, Strategic Chain
│   ├── analytic.md       # Anti-sycophancy, epistemic humility, Socratic
│   ├── creative.md       # Negative prompting, archetypes, entropy, Neurotexts
│   ├── cases.md          # Documented failure modes
│   ├── models.md         # Model selection framework + decision tree
│   ├── diagnose.md       # Session diagnostics methodology
│   └── extract.md        # Prompt extraction from conversations
└── scripts/
    └── prompt_engineer.py # CLI: search, verify, assemble
```

### Knowledge Base Stats

| Category | Count | What's inside |
|----------|-------|---------------|
| Techniques (total) | 28 | CoT, ToT, CoV, Reflexion, etc. across 4 categories |
| Research-backed (with citations) | 10 | Explicit citations from peer-reviewed papers |
| Ready-to-use prompts | 58 | System, task, chain, template, meta categories |
| Failure patterns (diagnostics) | 13 | Coded patterns (I01-T02) with root causes and patches |
| Session archetypes | 6 | Common failure modes (Death by Corrections, Format Jenga, etc.) |
| Model profiles | 6 | Full comparison matrix with do's and don'ts |
| Extraction patterns | 5 | Clarification Cascade, Format Negotiation, etc. |

---

## Key Design Decisions

**Security-first.** Every mode starts with a security scan. If you're about to paste untrusted content without boundaries — it stops you.

**Model-aware.** Recommends the right model for each task with rationale. Knows that o3 hates CoT scaffolding, DeepSeek needs everything in user prompt, and Gemini wants instructions after data.

**Progressive disclosure.** SKILL.md loads first (~400 lines). Reference files load only when needed. No knowledge base bloat in context.

**Concrete, not abstract.** Every patch in DIAGNOSE is copy-paste ready. Every recommendation in GENERATE includes exact text. No "consider adding more context" — it's "Add `<documents>` wrapper around user input."

---

## Common Confusion (We Learned From Real Users)

**"I thought this just improves text"**

Nope — it builds and analyzes *prompts* (instructions for AI). But it can analyze conversation logs to find what went wrong (DIAGNOSE) or capture what worked (EXTRACT).

**"It reads my whole chat context?"**

Only if you paste it. For GENERATE/VERIFY/IMPROVE, provide the prompt text. For DIAGNOSE/EXTRACT, paste the conversation you want analyzed.

**"When do I use this vs just asking the AI directly?"**

Use this skill when you want a **reusable, robust prompt** (runs 10+ times) or when something went wrong and you need to understand why. For one-off questions, just ask the AI.

---

## Installation

### For Kimi (Browser)

Upload the `.skill` file via Kimi's skill management interface.

### For Claude Code

```bash
cp -r prompt-engineer ~/.claude/skills/
```

Then invoke naturally: "write me a prompt for X", "check this prompt", "what went wrong with this session?"

---

## CLI Tools

```bash
# Search knowledge base
python scripts/prompt_engineer.py search "tree of thought" --model claude --category reasoning

# Verify prompt against checklist
python scripts/prompt_engineer.py verify --prompt-file my_prompt.md

# List all techniques
python scripts/prompt_engineer.py list --category reasoning
```

---

## Changelog

### v1.1 (Current)
- Added **DIAGNOSE** mode: analyze conversation logs, find failure points, produce concrete patches
- Added **EXTRACT** mode: turn successful conversations into reusable prompts
- Added **MODEL SELECT** mode: framework for choosing the right AI model
- Added security-first assessment to all modes
- Added 7-section output template for consistent deliverables
- Added onboarding section for first-time users
- Merged Urbans model selection framework
- Added session archetypes and 12 coded failure patterns

### v1.0
- Initial release: GENERATE, VERIFY, IMPROVE, CHAIN modes
- 28 techniques, 13 failure patterns, 10 research-backed citations, 58 prompts, CLI tools

---

**Built from:** Expert knowledge base (prompt_archive + Neurotexts) + Research synthesis (The Prompt Report, 200+ papers) + Real user feedback.
