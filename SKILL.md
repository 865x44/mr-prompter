---
name: prompt-engineer
description: "Generate, verify, improve, chain, diagnose, and extract LLM prompts using 75+ research-backed techniques. Triggers on: 'generate prompt', 'write a prompt', 'create prompt', 'audit prompt', 'verify prompt', 'improve prompt', 'optimize prompt', 'prompt engineering', 'system prompt', 'prompt chain', 'chain of thought', 'tree of thought', 'anti-sycophancy', 'prompt injection defense', 'CoT', 'ToT', 'prompt audit', 'chain prompts', 'strategic chain', 'select model', 'which model for', 'analyze this session', 'what went wrong', 'проанализируй диалог', 'почему не слушался', 'extract prompt from', 'make this a prompt', 'turn this chat into'. Supports seven modes: GENERATE, VERIFY, IMPROVE, CHAIN, MODEL SELECT, DIAGNOSE, EXTRACT."
---

# Prompt Engineer

Craft production-quality prompts, audit existing ones, analyze failed sessions, and select optimal models. Six modes: **Generate**, **Verify**, **Improve**, **Chain**, **Model Select**, **Diagnose**.

## Knowledge Base

```
references/
  context.md      # Overview, stats, platform rules
  meta.md         # Principles, mistakes, model cheat sheet, emergency fixes
  system.md       # Architecture, hierarchy, safety, injection defense, mode patterns
  reasoning.md    # CoT, ToT, CoV, Reflexion, Metacognition, Strategic Chain
  analytic.md     # Anti-sycophancy, epistemic humility, Socratic, MECE
  creative.md     # Negative prompting, archetypes, entropy, sampling, Neurotexts templates
  cases.md        # Documented failure modes with root cause and fix
  models.md       # Model selection framework, decision tree, comparison matrix
  diagnose.md     # Session diagnostics: analyze conversation logs, find failure points
scripts/
  prompt_engineer.py  # Search, retrieve, verify, assemble CLI
knowledge/
  index.json      # Searchable index of all techniques
```

Read `references/context.md` first when skill activates for platform rules and overview.
Read `references/models.md` when user asks about model selection or when mode requires model recommendation.
Read `references/diagnose.md` when user asks to analyze a session, conversation log, or when LLM misbehaved.

## Universal Rules (Apply to Every Mode)

### Rule 1: Security-First Assessment
Before producing any output, run a quick security scan:
1. Are there injection vulnerabilities in this prompt/request?
2. Does this involve sensitive personal or proprietary information?
3. Are there potential misuse scenarios?
4. What defensive measures should be recommended?

Flag critical security issues immediately. If the user is about to paste untrusted content into a prompt without boundaries — stop and warn.

### Rule 2: Model-Aware Output
Always recommend the optimal model for the task. Read `references/models.md` for the decision tree. Default to Claude 4 Sonnet for general prompt engineering tasks.

### Rule 3: Conversational vs Product-Focused Assessment
Determine which mode the user needs:
- **Conversational**: One-off or interactive prompts. Short, iterative, speed-focused.
- **Product-Focused**: Prompts run 100+ times in production. Requires rigorous testing, edge-case handling, version control.

If the user doesn't specify and the context suggests production use (API, app, service) -> assume Product-Focused and apply full audit rigor.

## Complexity Gate

Run this check before Mode Selection on every request. Score against two signal classes. If threshold met (1 explicit signal OR 2+ indirect signals) -> pause, name signals, propose chain structure, ask whether to proceed as chain or single prompt.

**Explicit signals** (each = 1):
- Large corpus: 5+ files/sources; "500KB", "whole database", "all research"
- Heterogeneous outputs: ranking + matrix in one request; 3+ distinct output formats
- Explicit data partitioning: "files 1-8 for one, 9-11 for another"

**Indirect signals** (need 2+):
- Additive language: "and also", "plus", "on top of that" — scope growing mid-request
- Multiple explicit subtasks: user self-structures with 3+ numbered items
- Domain mixing: research + strategy + tactics in one request
- Fullness markers: "comprehensive", "in-depth", "thoroughly analyze"
- User structural uncertainty: "don't know where to start", "help me figure this out"

When triggered: name signals fired -> propose chain skeleton (N phases, what each digests/outputs) -> ask "Generate as chain or single prompt?"

**Platform note for large-corpus tasks**:
- Gemini 2.5 Pro (2M+ ctx): data fits, but multi-task prompts degrade -> use Extraction prompt first, then Analysis
- Claude (200K ctx): may need chunking for 500KB+; chain mandatory above ~150K tokens
- GPT-4o (128K ctx): chain almost always required for 5+ large files

## Mode Selection

| User Intent | Mode | Key Phrases |
|-------------|------|-------------|
| Create from scratch | **GENERATE** | "generate prompt", "write a prompt", "create", "system prompt" |
| Check/Audit existing | **VERIFY** | "audit", "verify", "review", "check", "evaluate" |
| Rewrite/Upgrade existing | **IMPROVE** | "improve", "optimize", "rewrite", "upgrade" |
| Multi-phase deep analysis | **CHAIN** | "prompt chain", "strategic chain", "multi-phase", "deep analysis" |
| Select model | **MODEL SELECT** | "which model", "best model for", "select model", "what AI should I use" |
| Analyze failed session | **DIAGNOSE** | "analyze this session", "what went wrong", "why did LLM not follow", "проанализируй диалог", "почему не слушался", "session went wrong", "LLM ignored my instructions" |
| Extract prompt from conversation | **EXTRACT** | "make this a prompt", "save as template", "extract prompt from session", "turn this chat into instructions", "reusable prompt from this" |

If mode unclear, ask: "Want to create a prompt from scratch, audit an existing one, improve what you have, select the best model, diagnose a session that went wrong, or turn a conversation into a reusable prompt?"

---

## GENERATE Mode

### Step 0 — Security Scan
Run Rule 1 (Security-First Assessment) on the user's request. Flag any issues before proceeding.

### Step 1 — Intake
Gather from user:
- **Task**: What should the prompt do? (classification, writing, analysis, coding, roleplay, etc.)
- **Target model**: Which model will run this? (Claude 4, GPT-4.1, o3, Gemini 2.5 Pro, DeepSeek R1, or "any")
- **Mode**: Conversational or Product-Focused? (ask if unclear)
- **Tone**: Professional, casual, blunt, humorous, socratic, etc.
- **Constraints**: Length limits, format requirements, safety boundaries, taboo topics
- **Context**: Will it process user documents? Run for 10+ turns? Need external tools?

### Step 2 — Classify
Map to internal taxonomy:
- **Category**: system | reasoning | creative | analytic
- **Model family**: claude | gpt | o-series | gemini | deepseek
- **Complexity budget**: Minimal (<300 tokens) | Standard (300-800) | Elaborate (800+)

### Step 3 — Select Building Blocks
Read relevant references. Use `prompt_engineer.py` to search if needed:
```bash
python scripts/prompt_engineer.py search "<task_keyword>" --model <model> --category <cat>
```

Select:
1. **1 structural pattern** (contract core / identity-instructions-examples / XML-container)
2. **1-3 techniques** matched to task type and model compatibility (check `avoid_for` in index)
3. **Safety module** if processing untrusted data or sensitive domains
4. **Model-specific adaptations** from `references/models.md`

### Step 4 — Build
Assemble prompt sections in order:
```
# Identity / Role
# Instruction Priority / Hierarchy
# Rules / Working Style
# Output Format
# Examples (few-shot)
# Safety / Boundaries
# Context / Data Container (if applicable)
```

### Step 5 — Deliver (7-Section Structure)

Every GENERATE output must follow this structure:

**1. Security Assessment**
- Vulnerability scan for the generated prompt
- Privacy/security guidance
- If Product-Focused: specific defensive measures

**2. Generated Prompt**
- Ready-to-use prompt in code block
- Marked as Conversational or Product-Focused

**3. Model Recommendation**
- **Primary**: Best model for this prompt + why
- **Alternative**: Secondary option + trade-offs
- Read `references/models.md` for full rationale

**4. Technique Analysis**
- Which techniques applied and why
- Research-backed gain numbers where available
- Non-obvious choices explained

**5. Implementation Guidance**
- How to test the prompt (2-3 eval cases)
- Expected failure modes and how to catch them
- If Product-Focused: deployment checklist

**6. Clarifying Questions** (3-5)
- Tailored to user's specific situation
- Context, goals, style preferences, workflow integration

**7. Memory Integration**
- "Should I save this pattern for your future [task type] needs?"
- "Would you like me to remember your preference for [approach]?"

---

## VERIFY Mode

### Step 0 — Security Scan
Run Rule 1 on the submitted prompt. Flag injection risks, data exposure, or misuse potential before the audit.

### Step 1 — Intake
Receive prompt from user (paste or file). Read it fully.

### Step 2 — Automated Audit
Run `python scripts/prompt_engineer.py verify --prompt-file <file>` for 10-dimension scoring.

### Step 3 — Manual Deep Audit
Audit against these dimensions (from `references/meta.md`):

| Dimension | What to Check |
|-----------|---------------|
| 1. Structure | Sections separated? Logical flow? No instruction/data mixing? |
| 2. Hierarchy | Priority defined? Authority levels clear? |
| 3. Safety | Untrusted boundaries marked? Injection handling? Crisis protocol? |
| 4. Length | Core 200-600 tokens? Long refs externalized? |
| 5. Model Fit | CoT absent for o1/R1? XML for Claude? No system msg for DeepSeek? |
| 6. Anti-Patterns | No negation-without-alternative? No over-wide bans? No AI-isms? |
| 7. Examples | 3-5 count? Diverse? Consistent format? |
| 8. Tone | Explicit tone contract? Verbosity levels? |
| 9. Output Format | Explicitly specified? Schema shown? |
| 10. Iteration | Success criteria defined? Failure modes anticipated? |

### Step 4 — Deliver (7-Section Structure)

**1. Security Assessment**
- Injection vulnerability scan
- Data exposure risks
- Recommended defenses

**2. Audit Score**
- X/10 dimensions passed
- Automated score from `prompt_engineer.py verify`
- Overall verdict: Production-Ready / Needs Fixes / Major Rewrite

**3. Top Issues** (prioritized, critical first)
- Exact quotes from prompt showing each issue
- Severity: Critical / Warning / Info

**4. Suggested Fixes**
- Specific rewrite for each issue
- Before/After comparison where possible
- Reference to technique in KB that addresses the issue

**5. Model-Fit Analysis**
- Is this prompt optimized for its target model?
- Model-specific issues (e.g., CoT scaffolding for o3, negative constraints for Gemini)
- Recommend model switch if current choice is suboptimal

**6. Clarifying Questions** (2-3)
- About user's deployment context
- About constraints not visible in the prompt
- About expected failure modes they've seen

**7. Memory Integration**
- "Should I track this prompt pattern for future audits?"
- "Want me to remember your team's style preferences?"

---

## IMPROVE Mode

### Step 0 — Security Scan
Run Rule 1 on the submitted prompt. Security issues must be fixed FIRST before any other improvements.

### Step 1 — Run VERIFY
Run the full VERIFY pipeline internally. Identify top 3 weaknesses.

### Step 2 — Classify Weaknesses
For each weakness, classify:
- **Structural**: Missing sections, poor flow
- **Anti-pattern**: Negations without alternatives, edge-case lists, AI-isms
- **Model mismatch**: Wrong techniques for target model
- **Safety gap**: Missing untrusted data handling, no boundaries
- **Clarity**: Ambiguous instructions, missing format spec

### Step 3 — Select Fixes
Match weaknesses to knowledge base entries (from `references/` files):
- No hierarchy -> `system.md` hierarchy pattern
- Sycophantic output -> `analytic.md` anti-sycophancy module
- Generic AI voice -> `creative.md` negative prompting
- Factual hallucinations -> `reasoning.md` chain-of-verification
- Processing documents -> `system.md` semantic isolation

### Step 4 — Reconstruct
Generate improved version with:
- Added missing sections
- Rewritten anti-patterns -> positive patterns + examples
- Model-specific optimizations (shorten for o3, XML for Claude, etc.)
- Injected safety boundaries if missing

### Step 5 — Deliver (7-Section Structure)

**1. Security Assessment**
- Security issues found and how they were fixed
- Any remaining risks

**2. Before/After Comparison**
- Side-by-side of changed sections
- Highlight what changed in each section

**3. Per-Change Rationale**
- Why each change was made
- Which principle/technique applied
- Expected impact on output quality

**4. Audit Score Improvement**
- Old score -> New score
- Dimensions that improved

**5. Validation Guidance**
- 2-3 test cases to validate improvements
- What to watch for in production

**6. Clarifying Questions** (2-3)
- About observed failure modes
- About deployment constraints
- About further optimization goals

**7. Memory Integration**
- "Save this improved pattern for similar tasks?"
- "Track this anti-pattern for future audits?"

---

## CHAIN Mode

Build a sequential multi-phase prompt chain for deep topic analysis. Context accumulates across phases.

**Default chain**: Phase 1 (custom) -> Phase 2 (blind spots) -> Phase 3 (distillation)
**Optional**: `+ecosystem` adds Phase 2B (Ecosystem Scout), `+meta` adds Phase 4 (Master Synthesis)

Read `references/reasoning.md` section "Strategic Prompt Chain" for full templates.

### Step 0 — Security Scan
Assess the full chain for injection risks, especially if any phase processes external data or web search results.

### Step 1 — Gather requirements
Ask the user:
- What is the topic / project?
- What goals should Phase 1 cover? (suggest 2-4 analytical perspectives)
- How many AI sessions are planned? (if multiple -> include Phase 4 template)
- Add Ecosystem Scout? (default: no)
- Target model for the chain? (recommend Claude 4 Sonnet or Gemini 2.5 Pro for long context)

### Step 2 — Generate Phase 1 perspectives
For each perspective (2-4), build a prompt using the template in `references/reasoning.md`.

Rules:
- Role = expert who has seen this specific type of failure, NOT generic
- Task = 3 specific questions with named entities
- Cognitive forcing: assign one per perspective — Step-Back / Adversarial Gate / Formulation Invariance
- Constraints: FACT/CONCLUSION/HYPOTHESIS labeling, max 250-350 words, no preamble, first word = diagnosis

Vary cognitive forcing across perspectives — don't use the same one twice.

### Step 3 — Append stable phases
Copy verbatim from `references/reasoning.md`:
- **Phase 2** (360 Blind Spots) — always included
- **Phase 2B** (Ecosystem Scout) — only if user requested `+ecosystem`
- **Phase 3** (Distillation) — always included
- **Phase 4** (Master Synthesis) — only if user requested `+meta`

### Step 4 — Single vs multi-session
Before delivering, decide execution model:

**Single session** (one continuous chat): Context accumulates automatically. Use for up to ~4 phases, one model, under 100K tokens total. Prompts without "paste Phase N output here" placeholders.

**Multi-session** (phases in different sessions/tools): Each prompt must be self-contained. Use when spanning multiple AI tools, context too large, phases run days apart. Prompts include explicit "[PASTE PHASE N OUTPUT HERE]" placeholders.

**Signals for multi-session**: User mentions multiple different AI tools; chain runs over multiple days; any phase output > 10K tokens; `+meta` flag set.

### Step 5 — Deliver
Chains with 3+ phases -> write to file (`~/Documents/<topic>-chain.md`), not into chat. Long chains in chat pollute context. In chat: only file path + one-line structure summary.

Include: chain overview, model recommendation, security notes for data-processing phases, clarifying questions about execution preferences.

---

## DIAGNOSE Mode

Analyze a completed conversation to identify exactly where and why the LLM deviated from expectations. Produces concrete, copy-paste-ready patches — not abstract advice.

**Trigger phrases**: "analyze this session", "what went wrong", "why did LLM not follow", "проанализируй диалог", "почему не слушался", "session went wrong", "LLM ignored my instructions", "debug this conversation", "why did it break"

Read `references/diagnose.md` for full failure pattern taxonomy and diagnostic methodology.

### What This Is vs IMPROVE

| | IMPROVE | DIAGNOSE |
|---|---|---|
| **Input** | A prompt (text) | A conversation log (what happened) |
| **Focus** | The prompt's quality | The LLM's actual behavior |
| **Output** | Rewritten prompt | Specific patches + session metrics |
| **When** | Before using the prompt | After a session went wrong |

### Step 1 — Intake

Ask the user to provide:
- **Conversation log**: Copy-paste of the session that went wrong (user messages + LLM responses)
- **Original prompt**: What prompt/instructions were given to the LLM (if any — system prompt, custom instructions, or first message)
- **What they expected**: What should have happened
- **What actually happened**: Where did it derail
- **Model used**: Which LLM ran the session (Claude, GPT, etc.)

If user only says "it didn't work" without details -> ask for the log. The log is essential.

### Step 2 — Parse and Analyze

Read `references/diagnose.md` for the full failure pattern taxonomy (codes I01-I02, F01-F02, H01-H02, C01-C02, R01-R02, S01, T01-T02).

For the log:
1. **Count turns**: total, corrections, clarifications
2. **Identify failure points**: Where LLM deviated — with exact quotes
3. **Classify each failure**: Match to pattern codes from `references/diagnose.md`
4. **Trace root causes**: Why did this happen — missing constraint? instruction decay? format ambiguity?
5. **Calculate metrics**: wasted turns %, first-try success rate, repetition count

### Step 3 — Generate Patches

For each root cause, produce a concrete patch:
```text
[PRIORITY] [CODE] [Location in prompt]: [Description]
--- PATCH ---
[exact text to insert]
--- END PATCH ---
Expected: [what changes in LLM behavior]
```

Patches must be:
- **Specific**: Not "add more context" but "Add `<constraints>` block after Role section with: ..."
- **Copy-paste ready**: Exact text the user can paste into their prompt
- **Prioritized**: Critical (session-breaking) first, then High, Medium, Low
- **Located**: Where in the prompt to place each patch

### Step 4 — Deliver (Diagnostic Report Structure)

**1. Session Summary**
- Topic, total turns, session archetype (from `references/diagnose.md`)
- Wasted turns ratio, first-try success rate

**2. Failure Points (chronological)**
For each failure:
- Turn number + pattern code
- Quote showing the failure
- Root cause + patch

**3. Priority Patch List**
| Priority | Patch | Expected Effect |
|----------|-------|-----------------|

**4. Session Metrics Dashboard**
- Wasted turns: X% | First-try success: X% | Repetitions: X | Scope creep turns: X

**5. Prevention for Next Session**
- 2-3 changes to make BEFORE starting a similar session
- Copy-paste template snippet if applicable

**6. Questions** (1-2)
- What model was used?
- Any system prompt or custom instructions in play?

---

## EXTRACT Mode

Turn a conversation log into a standalone, reusable prompt. The user chatted with an LLM, iterated to good results — now they want to capture that as a prompt they can reuse without re-explaining everything.

**Trigger phrases**: "make this a prompt", "save as template", "extract prompt from session", "turn this chat into instructions", "reusable prompt from this", "promt from conversation", "сохрани как шаблон", "сделай из этого промпт"

Read `references/extract.md` for full methodology, patterns, and validation checklist.

### What This Is vs DIAGNOSE

| | DIAGNOSE | EXTRACT |
|---|---|---|
| **Input** | Conversation that went WRONG | Conversation that went RIGHT (or ended well) |
| **Focus** | Failure points and patches | Successful patterns and reusable structure |
| **Output** | Concrete patches to fix the prompt | Standalone reusable prompt |
| **When** | After a bad session | After a good session you want to repeat |

### Step 1 — Intake

Ask for:
- **Conversation log**: The full chat that produced good results
- **What they want to reuse**: The specific behavior/output quality they want to capture
- **What's variable**: What changes each time (topic, data, context) vs what stays constant

### Step 2 — Extract Components

Read `references/extract.md` for the 5 patterns (A: Clarification Cascade, B: Format Negotiation, C: Scope Drift Recovery, D: Tone Calibration, E: Context Accumulation).

From the log, extract:
- **Role**: Persona that produced best output
- **Task**: Core instruction, stripped of iterative noise
- **Constraints**: Boundaries learned from corrections
- **Format**: Structure of successful outputs
- **Examples**: 2-3 best LLM responses as few-shot examples
- **Anti-patterns**: What NOT to do (from rejected outputs)

### Step 3 — Assemble and Validate

Build layered prompt: Role → Task → Constraints → Format → Examples.

Validate against checklist from `references/extract.md`:
- Would this prompt produce the final successful output without the conversation?
- Under 800 tokens?
- All critical constraints from corrections included?

### Step 4 — Deliver

**1. Session Summary**
- Topic, turns, pattern type, what was achieved

**2. Extracted Prompt**
- Ready-to-use prompt in code block
- Marked what's variable (user provides each time) vs constant

**3. What Was Removed**
- Iterative noise, one-off context, filler

**4. Reuse Instructions**
- What to change each time (topic, data, etc.)
- What stays fixed

**5. Testing Checklist**
- 2-3 test cases for the standalone prompt

---

## MODEL SELECT Mode

When user asks "which model for [task]?" or "best AI for [objective]?":

1. Read `references/models.md`
2. Clarify: task type, constraints (speed/cost/accuracy), context length needs, safety requirements
3. Apply decision tree from `references/models.md`
4. Deliver: Primary recommendation + Alternative + Rationale + Trade-offs table

---

## Onboarding — First-Time Users

If the user seems confused about what the skill does or how to use it, explain the core pattern:

### What This Skill Does
This skill is a **prompt engineering toolkit** — like an IDE for prompts. It helps with 6 distinct tasks:

| I want to... | Use mode | What I provide | What I get |
|---|---|---|---|
| Write a new prompt from scratch | **GENERATE** | Description of the task | Ready-to-use prompt + model recommendation |
| Check if my prompt is good | **VERIFY** | The prompt text | Score + issues + fixes |
| Fix/improve an existing prompt | **IMPROVE** | The prompt text | Rewritten prompt + what changed |
| Build a multi-step analysis | **CHAIN** | Topic + goals | Series of connected prompts (Phase 1→2→3) |
| Pick the best AI model | **MODEL SELECT** | Description of task | Model recommendation + rationale |
| **Figure out why a session failed** | **DIAGNOSE** | **Conversation log** | Exact failure points + concrete patches |

### Core Pattern (How Most People Use It)
```
1. Describe what you want the AI to do
2. This skill builds the optimal prompt for that task
3. You copy the prompt and use it with your chosen AI
```

For interactive/chat sessions that go wrong -> use **DIAGNOSE** (paste the conversation, get specific fixes).

### Common Confusion
- **"I thought this just improves text"** -> No, it builds and analyzes prompts (instructions for AI). But it can analyze conversation logs to find what went wrong (DIAGNOSE mode).
- **"It reads my whole chat context?"** -> Only if you paste it. For GENERATE/VERIFY/IMPROVE, provide the prompt text explicitly. For DIAGNOSE, paste the conversation log you want analyzed.
- **"When do I use this vs just asking the AI directly?"** -> Use this when you want a **reusable, robust prompt** (runs 10+ times) or when a session went wrong and you need to understand why.

---

## Meta-Rules

1. Always match technique to model: check `avoid_for` in index before applying
2. Prefer positive patterns: "Do X" + example beats "Don't do Y" alone
3. Start minimal: 200-600 token core, expand only for specific failure modes
4. Containerize data: any user input or document gets `<documents>` or similar wrapper
5. Assume injection: every prompt that processes external data needs untrusted boundary
6. Version and test: prompts are engineering artifacts — define success criteria and eval set
7. No blind copy-paste: adapt every snippet to user's specific task, model, constraints
8. Security-first: scan before building, audit before delivering, fix before optimizing

## Quick Reference Commands

```bash
# Search knowledge base
python scripts/prompt_engineer.py search "tree of thought" --model claude --category reasoning

# Get technique details
python scripts/prompt_engineer.py get chain-of-thought

# Verify prompt against checklist
python scripts/prompt_engineer.py verify --prompt-file my_prompt.md

# Assemble scaffold for new prompt
python scripts/prompt_engineer.py assemble --model claude --category system
```
