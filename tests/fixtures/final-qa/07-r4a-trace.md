# Final QA — 07 R4A trace (pin `dbd4588`, per-file take/reject)

Source: `anthropics/skills` @ pin `dbd4588` (read-only reference, NOT
vendored — license unestablished, no verbatim imports anywhere).
Raw file links (frozen pin):

- `https://raw.githubusercontent.com/anthropics/skills/dbd4588/skills/claude-api/shared/prompt-audit.md`
- `https://raw.githubusercontent.com/anthropics/skills/dbd4588/skills/claude-api/shared/agent-design.md`
- `https://raw.githubusercontent.com/anthropics/skills/dbd4588/skills/claude-api/shared/evals/eval-audit.md`
- `https://raw.githubusercontent.com/anthropics/skills/dbd4588/skills/claude-api/shared/evals/eval-hillclimb.md`
- `https://raw.githubusercontent.com/anthropics/skills/dbd4588/skills/claude-api/shared/evals/cost-hillclimb.md`

Local mirror (Primary, 2026-10-17, executor-local, not in repo):
`/tmp/r4a-links/` — prompt-audit.md (237 lines), agent-design.md (101),
evals_eval-audit.md (204), evals_eval-hillclimb.md (338),
evals_cost-hillclimb.md (442).

Take/reject is cumulative across W0→W1→W2 (already in wave reports;
recorded here, not re-absorbed). Product code FROZEN after W2 — no new
absorption in this wave.

| File (pin `dbd4588`) | Take (absorbed mechanism) | Reject (reason) |
|---|---|---|
| `shared/prompt-audit.md` | Migration-signal discipline behind `models.md` API-snapshot scoping (W1); "re-read ≠ independent verification" behind CHAIN preflight (W2); keep-list discipline — narrow, don't delete (W1) — and TRACKED instead of deletion (W2) | Bulk audit-checklist shape not adopted (own VERIFY L1/L2/L3 kept) |
| `shared/agent-design.md` | None (no agents/harness in this repo) | Rejected W0/W1/W2: no agents — PTC, caching, subagents inapplicable |
| `shared/evals/eval-audit.md` | Extrinsic/intrinsic split became VERIFY L1/L2/L3 (W1) and backs R-rules vs semantic-fraud split (W2); living-suite idea became fixtures + frozen runner expectations (W1/W2) | Full eval-harness shape not adopted (own twin runners kept) |
| `shared/evals/eval-hillclimb.md` | Frozen-set/by-case logging became per-pair runner expectations + dual detect/clean measurement (W1); frozen per-pair expectations + recorded (not demanded) outcomes in chain runner (W2) | Hill-climb optimization loop not adopted (no tuning runs) |
| `shared/evals/cost-hillclimb.md` | None (no budget/runs to spend in this repo) | Rejected W0/W1/W2: no budget/runs — nothing to spend |

No verbatim imports from any R4A file (upstream license still
unestablished). Absorption is mechanism-level only (own code throughout).
