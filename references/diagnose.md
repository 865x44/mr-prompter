# Session Diagnostics — Analyzing Past Conversations

Analyze completed LLM conversations to identify failure points, root causes, and produce concrete patches for the user's prompt/system setup.

## When to Use

- User pastes a log of a conversation that went wrong
- User says "LLM keeps ignoring my instructions"
- User wants to understand why a session derailed
- Post-mortem after a failed prompt engineering attempt
- User says "analyze this session", "what went wrong", "why didn't it follow", "почему не слушался", "проанализируй диалог"

## What This Is NOT

- NOT general prompt improvement (that's IMPROVE mode) — this analyzes BEHAVIOR in a real session
- NOT a critique of the user's prompting skill — this is blameless technical analysis
- NOT abstract advice — every finding must tie to a specific line/turn in the log

---

## Diagnostic Framework

### Step 1 — Parse the Log

Extract from the conversation:
- **Turn count**: How many back-and-forth exchanges
- **User messages**: What the user asked for
- **LLM responses**: What the LLM produced
- **Correction turns**: Where user had to say "no, wrong", "fix this", "that's not what I meant"
- **Clarification turns**: Where LLM asked "do you mean X or Y?"
- **Repetition loops**: Where same issue appears 2+ times

### Step 2 — Identify Failure Patterns

For each failure, classify by type. Use the taxonomy below.

| Code | Pattern | Signal in Log | Root Cause |
|------|---------|---------------|------------|
| **I01** | Instruction ignored | LLM does opposite of what was asked | Hierarchy ambiguity, conflicting instructions, instruction buried in middle |
| **I02** | Partial compliance | LLM follows 2 of 3 rules | Context window overload, rules not prioritized, too many constraints |
| **F01** | Format drift | Output starts right, drifts wrong | No format reinforcement, long response, missing schema example |
| **F02** | Wrong format entirely | Completely different structure | Format spec ambiguous, no example provided, conflicting format hints |
| **H01** | Hallucination (facts) | LLM invents data not in context | No "use only provided data" constraint, weak grounding, creative task bleed |
| **H02** | Hallucination (instructions) | LLM adds steps user didn't ask for | Over-eager helpfulness, no scope boundary, "be proactive" instruction |
| **C01** | Excessive clarification | LLM asks 3+ questions before acting | Ambiguous user request, missing defaults, over-cautious tone |
| **C02** | Wrong assumptions | LLM assumes context that wasn't given | Missing user profile, no state tracking, pronoun resolution failure |
| **R01** | Repetition loop | Same error fixed then reappears | No state carry between turns, context compression losing key rules |
| **R02** | Escalating scope | Task grows with each turn | No scope gate, user additions not bounded, "while you're at it" accumulation |
| **S01** | Safety misfire | Legitimate request refused | Overbroad safety filters, missing context, edge case not handled |
| **T01** | Tone mismatch | Wrong voice/persona | Tone spec missing, role description vague, contradictory examples |
| **T02** | verbosity explosion | Response 3x longer than needed | No length constraint, "detailed" interpreted as "comprehensive", missing calibration |

### Step 3 — Root Cause Analysis

For each failure pattern found, trace to root cause:

**Instruction hierarchy issues** -> Check `references/system.md` hierarchy section
**Format/schema issues** -> Check `references/system.md` output format patterns
**Context/state loss** -> Check `references/system.md` context anchoring, progressive disclosure
**Hallucination** -> Check `references/reasoning.md` chain-of-verification, anti-hallucination
**Safety** -> Check `references/system.md` injection defense, sandwich defense
**Tone/verbosity** -> Check `references/creative.md` negative prompting, volume control

### Step 4 — Generate Concrete Patches

For each root cause, produce:

1. **Patch description**: 1 sentence — what to add/change/remove
2. **Patch code**: Exact text to insert into the prompt (copy-paste ready)
3. **Location**: Where in the prompt to place it (beginning, before examples, after role, etc.)
4. **Priority**: Critical / High / Medium / Low
5. **Expected effect**: What behavior change to expect

Patch format:
```text
[PRIORITY] [CODE] [Location]: [Description]
--- PATCH ---
[exact text to insert]
--- END PATCH ---
Expected: [what changes in LLM behavior]
```

### Step 5 — Metrics & Summary

Calculate session health metrics:
- **Wasted turns**: (correction turns + clarification turns) / total turns * 100%
- **First-try success rate**: Turns where LLM got it right on first attempt / total turns
- **Repetition rate**: How many times same issue reappeared after correction
- **Scope creep turns**: Turns that added new requirements not in original ask

Interpretation:
- Wasted turns < 20%: Good session
- Wasted turns 20-40%: Needs tuning
- Wasted turns > 40%: Prompt needs significant rewrite

---

## Common Session Failure Archetypes

### Archetype A: "Death by a Thousand Corrections"
- Pattern: User corrects LLM every 2-3 turns, session never converges
- Root cause: Core prompt has structural flaw — usually hierarchy or missing constraints
- Fix: Don't patch individual responses. Rewrite the base prompt using Contract Core pattern.

### Archetype B: "Works Once, Breaks Twice"
- Pattern: First response good, second goes wrong, third completely off
- Root cause: Context compression — key rules lost as conversation grows
- Fix: Add Context_Anchor re-anchoring, compress earlier turns, move critical rules to top

### Archetype C: "Scope Creep Spiral"
- Pattern: Each turn adds new requirements, prompt grows, quality drops
- Root cause: No scope gate or boundaries defined
- Fix: Add explicit scope boundaries: "Do NOT add features beyond [list]. If user asks for more, confirm scope change explicitly."

### Archetype D: "Format Jenga"
- Pattern: Format starts correct, then wobbles, then collapses mid-response
- Root cause: Format spec too abstract, no reinforcement examples, response too long
- Fix: Add format example at beginning AND end, add `\n\n---\n\nFormat check: confirm all sections present` mid-prompt for long outputs

### Archetype E: "The Yes-Man"
- Pattern: LLM agrees with everything, doesn't challenge wrong premises, produces garbage
- Root cause: Missing anti-sycophancy, no critical analysis mode
- Fix: Inject anti-sycophancy module + toggle mode for critical analysis

### Archetype F: "Ghost Instructions"
- Pattern: User gave instruction in turn 3, LLM forgot it by turn 8
- Root cause: Instruction priority decay — older instructions lose weight
- Fix: Move critical instructions to system-level, use XML containers, add re-anchoring

---

## Diagnostic Output Structure

### 1. Session Summary
- Topic: what was the user trying to achieve
- Turns: total count
- Wasted turns ratio
- Session archetype (A-F above)

### 2. Failure Points (chronological)
For each failure:
- Turn number
- Pattern code (I01, F01, etc.)
- Quote from LLM showing the failure
- Root cause
- Patch

### 3. Priority Patch List
Sorted by priority (Critical first):
| Priority | Patch | Expected Effect |
|----------|-------|-----------------|

### 4. Metrics Dashboard
- Wasted turns: X% (Y of Z)
- First-try success: X%
- Repetition rate: X
- Scope creep turns: X

### 5. Prevention for Next Session
- 2-3 specific changes to make BEFORE starting similar session
- Template snippet if applicable

### 6. Questions
1-2 questions to clarify user's setup (system prompt? custom instructions? model used?)
