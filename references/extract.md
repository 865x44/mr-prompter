# Extract — Turn Conversation into Reusable Prompt

Convert a successful (or partially successful) conversation log into a standalone, reusable prompt. The user chatted with an LLM, got good results through iteration — now they want to capture that as a prompt they can reuse without re-explaining everything.

## When to Use

- User pastes a conversation and says "make this a prompt I can reuse"
- User says "I got great results from this chat, save it as a template"
- User says "extract prompt from this session", "turn this into instructions"
- After DIAGNOSE mode — once failures are fixed, EXTRACT captures the working version
- User keeps re-explaining the same task to LLM every session

## What This Is NOT

- NOT recording the conversation verbatim — that would be too long and noisy
- NOT a chat summary — it produces a single prompt that reproduces the desired behavior
- NOT a critique of what went wrong (that's DIAGNOSE) — this captures what WORKED

---

## Extraction Framework

### Step 1 — Parse the Log

Read the conversation and extract:

1. **Original ask**: What did the user want initially?
2. **Iterative refinements**: What did the user add/change/correct across turns?
3. **Successful outputs**: Which LLM responses matched what the user wanted?
4. **Correction signals**: What did the user reject or ask to change?
5. **Final state**: What was the last successful turn that produced the desired result?

### Step 2 — Identify Reusable Components

From the successful turns, extract these building blocks:

| Component | Source in Log | What to Capture |
|-----------|---------------|-----------------|
| **Role** | User's persona assignments | "You are a..." that produced best output |
| **Task** | Original ask + refinements | Core instruction, stripped of context |
| **Constraints** | Corrections where LLM went wrong | Boundaries that kept output on track |
| **Format** | Successful outputs | Output structure that worked |
| **Examples** | Best LLM responses | 2-3 examples of desired output |
| **Anti-patterns** | Rejected outputs | What NOT to do (from corrections) |
| **Tone** | User's style adjustments | Voice that matched expectations |

### Step 3 — Build the Prompt

Assemble in layered structure:

```
# Identity / Role
Who the model should be (from successful persona in log)

# Task
What to do (core ask, refined through iteration)

# Rules / Constraints
What the model learned NOT to do (from corrections)

# Output Format
Structure of successful outputs (with example)

# Context / Data Container
How to handle user inputs (if applicable)
```

Keep it minimal: include only what was NECESSARY to get good results. Strip conversational filler, iterative noise, and one-off context.

### Step 4 — Validate Coverage

Checklist: does the extracted prompt cover what the conversation taught?

- [ ] Would this prompt produce the final successful output without the conversation?
- [ ] Are all critical constraints from corrections included?
- [ ] Is the format specification clear enough to replicate?
- [ ] Would a new user get acceptable results from this prompt alone?
- [ ] Is it under 800 tokens? (If longer, consider externalizing examples)

If any check fails, add what's missing.

---

## Common Patterns

### Pattern A: Clarification Cascade
User had to clarify 3+ times before LLM understood.
**Extraction strategy**: Combine all clarifications into explicit constraints upfront. The prompt should state what took 3 turns to communicate.

### Pattern B: Format Negotiation
User kept correcting format until it worked.
**Extraction strategy**: Capture the final format exactly, add a schema example, and specify "always use this format" as a hard rule.

### Pattern C: Scope Drift Then Recovery
User had to pull LLM back to the original task.
**Extraction strategy**: Add scope boundaries: "Do ONLY X. Do NOT do Y, Z, or W unless explicitly asked."

### Pattern D: Tone Calibration
User adjusted tone across multiple turns.
**Extraction strategy**: Capture the final tone description explicitly. Add negative prompting if LLM kept defaulting to unwanted style.

### Pattern E: Context Accumulation
User added more context each turn to improve quality.
**Extraction strategy**: Consolidate all context into a single context block. If too long, use progressive disclosure or external memory.

---

## Output Structure

Every EXTRACT output follows this structure:

**1. Session Summary**
- Topic, turns count, what was achieved
- Pattern type (A-E above)

**2. Extracted Prompt**
- Ready-to-use prompt in code block
- Layered: Role → Task → Constraints → Format → Examples

**3. What Was Removed**
- Iterative noise that didn't make it into the prompt
- One-off context that's not reusable
- Conversational filler

**4. What's Needed for Reuse**
- What the user must provide each time (data, context, topic)
- What the prompt handles automatically

**5. Testing Checklist**
- 2-3 test cases to validate the extracted prompt works standalone

**6. Estimated Effectiveness**
- How many correction turns this prompt should eliminate
- Comparison: original session turns vs expected turns with prompt
