# Documented Failure Cases

## Case Template

```yaml
---
model: 
date: YYYY-MM-DD
pattern: <slug from common-mistakes>
status: unverified
---

## Symptom
What went wrong — one sentence from user perspective.

## Context
Task type (chain / single-shot / system prompt), phase if chain, data source.

## Root Cause
1-2 sentences. What exactly in the prompt triggered the behavior.

## Fix
What was changed (minimal surgery — quote before/after if short).

## Result
worked / didn't work / awaiting verification
```

## Case: 2026-06-04 — Gemini Chain Exclusion Propagation

```yaml
---
model: gemini-2.0-pro
date: 2026-06-04
pattern: exclusion-not-propagated
status: verified
---
```

**Symptom**: Habr appeared in P0 ranked list despite being explicitly excluded in Phase 1.

**Context**: 4-phase multi-session chain (timurok-chain.md). Phase 1 extracted data from 11 files with instruction "Files 12-15 — ignore completely". Phase 2 — blind spots research with Google Search. Phase 3 — analysis and platform ranking.

**Root Cause**: Phase 1 correctly excluded Habr. Phase 2 searched for platforms NOT in Phase 1 table — Habr wasn't there, so web search found it as a "new" platform. Phase 3 received it as valid data and ranked P0 (Habr is objectively relevant to audience).

**Fix**: Propagate exclusion rules to ALL subsequent phases:
- Phase 2: "Habr — never include under any circumstances, even if Google Search suggests it."
- Phase 3: "Habr — exclude from all tables and outputs."

General rule: Any exclusion rule from Phase 1 must be duplicated in ALL subsequent phases, especially before web-search phases. Prefer positive form: "Process only: X, Y, Z" instead of "don't include A."

**Result**: Awaiting verification (Phase 4 fix sent to user in separate chat).
