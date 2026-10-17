# FQA-4 · Lane A — extracted prompt (EXTRACT, T7 dialogue)

> Blind label: **Lane A**. (Mapping sealed in `_blind-map.json`.)

## Session Summary
Topic: messy meeting notes → fixed brief. Turns: 4. Pattern: Format
Negotiation (headers locked in turn 3) over Scope Drift (snacks kept, not
dropped). Achieved: three-header format with owner → task actions.

## Extracted Prompt (generalizable core)

```
Turn raw meeting notes into exactly three headers, in order:
**Decisions:** — what was settled (omit header content, never the header,
when none stated: write "(none stated)").
**Actions:** — one line per action as "<owner> → <task>" plus "(due <date>)"
only when the notes state one.
**Parking lot:** — everything else worth keeping, one line per item.

Load-bearing constraints (WHY they stay):
- Exactly these headers, this order — the user locked the shape in turn 3;
  downstream readers parse on it.
- Every action names an owner mentioned in the notes — prevents assigning
  work to non-attendees (the failure the session avoided).
- Never invent dates, attendees, or decisions — the notes are the only
  source of truth; invention here is silent corruption.

Variable each run: the raw notes + attendee list.
Constant: headers, order, owner rule, no-invention rule.

Minimal example (format only — shape is declaratively specified):
Input: "maria to do pricing, deadline friday, also snacks"
**Decisions:** (none stated).
**Actions:** maria → pricing (due friday).
**Parking lot:** snacks.
```

## What Was Removed
Iterative noise ("my meeting notes are a mess", "Sure — paste them"),
session-specific bulk (ivan/maria/api/pricing instances — kept ONE as the
format example), one-off filler. Kept despite brevity pressure: the
"(none stated)" rule — without it, empty sections drift back into prose.

## Reuse Instructions
Change each time: notes + attendees. Keep fixed: headers, order, owner and
no-invention rules. If a team uses different headers, re-extract — do not
hand-edit the header names without re-running the checklist.

## Testing Checklist
1. Notes with no decisions → `(none stated)` under Decisions, no prose.
2. Action without a named owner → stays out of Actions (Parking lot or dropped).
3. New attendee names → carried into Actions verbatim, never normalized.

Validation status: **unvalidated draft** — no confirmed successful execution
behind it yet (downstream FQA-4 run is the validation attempt, not proof).
