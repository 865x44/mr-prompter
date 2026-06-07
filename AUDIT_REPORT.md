# Mr. Prompter — Maintenance Release Audit Report

> Date: 2026-06-07
> Executors: Kimi (initial implementation), Codex (review and final hardening)
> Branch: `audit/consistency-recovery`
> Canonical baseline: GitHub `main` at `66013190`
> Status: **Maintenance release ready for review**

---

## 1. Scope

This is a **narrow maintenance release** (project 1 of 3). It fixes mechanically provable inconsistencies, adds regression protection, and removes unsupported exact claims. It does **not** salvage old knowledge, judge research quality, or redesign the product.

### In scope
- Correct false or contradictory counts and descriptions
- Remove or qualify unsupported marketing claims
- Define and enforce a small metrics contract
- Add a deterministic consistency audit
- Add focused tests for the audit and existing CLI
- Fix narrow, test-demonstrated CLI bugs
- Add a dependency-light GitHub Actions workflow
- Update this audit report with findings, changes, test results, and deferred issues

### Out of scope (deferred)
- Old corpus audit (`~/mr-prompter` granular knowledge base and 75-technique index)
- Research-backed evidence quality audit and citation repair
- Stale model recommendations refresh
- Prompt manifest / structured catalog migration
- Installation synchronization (Kimi/Claude skills)
- Product direction research

---

## 2. Changes Applied

### 2.1 `knowledge/index.json`
- `stats.research_backed`: 10 → 12
- Added `stats.model_profiles`: 6, matching the canonical model-profile section count

### 2.2 `README.md`
- Header: "58 ready-to-use prompts" → "58 prompt Markdown files"
- Stats table: techniques 28 → 31
- Stats table: research-backed 10 → 12
- Stats table: "Ready-to-use prompts | 58" → "Prompt Markdown files | 58"
- Changelog v1.0: "10 research-backed citations" → "12 research-backed flags"
- Stats table label: "Research-backed (with citations)" → "Research-backed (entries flagged `research_backed=true`)"

### 2.3 `SKILL.md`
- Frontmatter: "75+ research-backed techniques" → "31 techniques with 12 research-backed flags"
- Body: "Six modes" → "Seven modes"
- Onboarding: "6 distinct tasks" → "7 distinct tasks"
- Onboarding table: added EXTRACT mode row

### 2.4 `references/context.md`
- Header: "58 ready-to-use prompts" → "58 prompt Markdown files"
- Header: "10 research-backed citations" → "12 research-backed flags"
- Label: "## Stats (verified)" → "## Stats"
- Bullet: "10 research-backed" → "12 research-backed"
- Bullet: "58 ready-to-use prompts" → "58 prompt Markdown files"
- Removed unverified performance examples (CoT 13%→41%, ToT 4%→74%, CoV hallucinations ↓80%) from the stats bullet; retained only the flag count description

### 2.5 `scripts/prompt_engineer.py` (CLI fixes)
- `cmd_get`: replaced buggy `re.DOTALL` regex with exact header-line match + position-based extraction
- `cmd_search`: returns `sys.exit(1)` when no results found
- `cmd_get`: returns `sys.exit(1)` when technique ID not found
- `cmd_verify`: wrapped `Path.read_text()` in `try/except FileNotFoundError` with clean error message
- `cmd_verify`: returns `sys.exit(1)` when neither `--prompt-file` nor `--prompt-text` is provided

### 2.6 `scripts/audit_consistency.py` (new)
- Deterministic checks:
  - `knowledge/index.json` parses
  - IDs are unique across collections
  - Stored structural stats match computed array lengths
- Published exact claims in README.md / SKILL.md / references/context.md match computed metrics (techniques, research_backed, modes, prompt Markdown files)
- All retained metrics use one computed snapshot; missing canonical sources and stored-stat drift fail
- Published README/context metric claims are checked against canonical computed values
  - Seven modes are stated consistently wherever an exact mode count is published
  - Referenced local files exist
  - Adapters do not repeat stale exact counts covered by the contract
  - Python files compile
- Four known missing technique-to-reference-section mappings are treated as **documented deferred warnings**, not failures:
  - `forced-domain-shift`
  - `toggle-mode-pattern`
  - `injection-defense`
  - `progressive-disclosure`
- Any **additional** missing mapping causes a hard failure.
- Supports `AUDIT_INDEX_OVERRIDE` and `AUDIT_REPO_ROOT` env vars for hermetic drift testing.

### 2.7 `tests/test_audit_consistency.py` (new)
- `test_audit_exits_zero`: requires current repository audit to pass cleanly
- `test_audit_exits_nonzero_on_drift`: proves fabricated count drift causes nonzero exit
- `test_audit_exits_nonzero_on_published_claim_drift`: proves a changed README claim fails while
  index stats remain unchanged

### 2.8 `tests/test_prompt_engineer_cli.py` (new)
- `test_search_chain_of_thought`
- `test_search_no_results`
- `test_list_reasoning`
- `test_get_strategic_chain` (verifies correct section, not Chain of Thought)
- `test_get_not_found`
- `test_get_all_techniques` (with known exemptions)
- `test_verify_no_input`
- `test_verify_missing_file`
- `test_verify_valid_prompt`
- `test_assemble_basic`

### 2.9 `scripts/check.sh` (new)
- Local entry point: `py_compile` → audit → unit tests → `git diff --check`

### 2.10 `.github/workflows/consistency.yml` (new)
- Runs the tracked local `scripts/check.sh` entry point on push/PR to `main`

### 2.11 `docs/metrics-contract.md` (new)
- Defines every exact number that may appear in published claims
- Excludes ambiguous metrics (ready-to-use prompt entries, citation quality, matrix columns)

### 2.12 `.gitignore` (new)
- Excludes Python bytecode and `__pycache__/` generated by local checks

---

## 3. Deferred Content Issues

These techniques exist in `knowledge/index.json` but have **no matching `## ` section** in their canonical reference file. They were **not fixed** in this maintenance release because no matching content exists in the current repository.

| Technique ID | Category | Reference File | Reason Deferred |
|--------------|----------|----------------|-----------------|
| `forced-domain-shift` | reasoning | `references/reasoning.md` | No section exists in current monolithic references |
| `toggle-mode-pattern` | system | `references/system.md` | Toggle mode discussed in adapters but not as formal reference section |
| `injection-defense` | system | `references/system.md` | Distinct from `safety-injection-defense` which HAS a section; no separate section for this ID |
| `progressive-disclosure` | system | `references/system.md` | Mentioned in adapters but no formal reference section |

**Action required:** Either add matching reference sections from validated sources, or remove these technique entries from `index.json` in a future content-focused release.

---

## 4. Historical Notes (Previously Gate A / Salvage)

The following analysis was produced during early discovery but is **not part of the maintenance release** and should not block it.

- `docs/salvage-matrix.md` and `docs/salvage-summary.md` are **deferred working notes**. They are **excluded** from the maintenance commit.
- The old `~/mr-prompter` repository (granular knowledge base, 75 technique entries, unrelated history) remains a **read-only archive** for a future corpus audit.
- Selective salvage recommendations (e.g. porting `forced-domain-shift`, `mckinsey-mece`, `cognitive-forcing-functions` from the old repo) are **deferred to a future content release**, not this maintenance release.
- No content from the old repository was imported.

---

## 5. Verification Results

```bash
$ python3 -m unittest discover -s tests -v
test_audit_exits_nonzero_on_drift (test_audit_consistency.TestAuditConsistency.test_audit_exits_nonzero_on_drift) ... ok
test_audit_exits_nonzero_on_published_claim_drift (test_audit_consistency.TestAuditConsistency.test_audit_exits_nonzero_on_published_claim_drift) ... ok
test_audit_exits_zero (test_audit_consistency.TestAuditConsistency.test_audit_exits_zero) ... ok
test_assemble_basic (test_prompt_engineer_cli.TestAssemble.test_assemble_basic) ... ok
test_get_all_techniques (test_prompt_engineer_cli.TestGet.test_get_all_techniques) ... ok
test_get_not_found (test_prompt_engineer_cli.TestGet.test_get_not_found) ... ok
test_get_strategic_chain (test_prompt_engineer_cli.TestGet.test_get_strategic_chain) ... ok
test_list_reasoning (test_prompt_engineer_cli.TestList.test_list_reasoning) ... ok
test_search_chain_of_thought (test_prompt_engineer_cli.TestSearch.test_search_chain_of_thought) ... ok
test_search_no_results (test_prompt_engineer_cli.TestSearch.test_search_no_results) ... ok
test_verify_missing_file (test_prompt_engineer_cli.TestVerify.test_verify_missing_file) ... ok
test_verify_no_input (test_prompt_engineer_cli.TestVerify.test_verify_no_input) ... ok
test_verify_valid_prompt (test_prompt_engineer_cli.TestVerify.test_verify_valid_prompt) ... ok

----------------------------------------------------------------------
Ran 13 tests
OK

$ python3 scripts/audit_consistency.py
RESULT: 0 errors, 1 warning(s)
Audit PASSED

$ bash scripts/check.sh
=== Python syntax check ===
=== Consistency audit ===
RESULT: 0 errors, 1 warning(s)
Audit PASSED
=== Unit tests ===
Ran 13 tests
OK
=== Git whitespace check ===
All checks passed.

$ python3 scripts/prompt_engineer.py search "chain of thought"
# Returns results, exit 0

$ python3 scripts/prompt_engineer.py list --category reasoning
# Returns list, exit 0

$ python3 scripts/prompt_engineer.py get strategic-chain
# Returns Strategic Prompt Chain section, exit 0

$ python3 scripts/prompt_engineer.py get does-not-exist
# Returns "not found", exit 1

$ python3 scripts/prompt_engineer.py verify --prompt-file /does/not/exist
# Returns "File not found", exit 1

$ python3 -m py_compile scripts/prompt_engineer.py scripts/audit_consistency.py
# No output = success

$ git diff --check
# No output = success
```

---

## 6. Proposed Commit

```
Audit metrics and harden consistency checks

- Fix contradictory counts: techniques 28→31, research-backed 10→12
- Remove false "75+" claim; align mode counts to 7 everywhere
- Qualify ambiguous prompt counts as "prompt Markdown files"
- Remove "Stats (verified)" misleading label
- Remove unverified performance examples from research-backed stats claim
- Describe research-backed only as entries flagged research_backed=true
- Fix CLI get/search/verify exit codes and error handling
- Fix get-section regex to match exact header lines
- Add scripts/audit_consistency.py with deterministic checks
- Add tests/ for CLI regression and audit behavior
- Add scripts/check.sh local entry point
- Add .github/workflows/consistency.yml CI
- Add docs/metrics-contract.md
- Add .gitignore for generated Python cache files
- Record 4 deferred technique-to-reference mapping issues
```

---

## 7. Files Changed

- Published claims: `README.md`, `SKILL.md`, `references/context.md`
- Canonical stats: `knowledge/index.json`
- CLI fixes: `scripts/prompt_engineer.py`
- Audit and local gate: `scripts/audit_consistency.py`, `scripts/check.sh`
- Regression tests: `tests/test_audit_consistency.py`, `tests/test_prompt_engineer_cli.py`
- CI and generated-file hygiene: `.github/workflows/consistency.yml`, `.gitignore`
- Contract and report: `docs/metrics-contract.md`, `AUDIT_REPORT.md`

### Proposed files to exclude from commit
- `docs/salvage-matrix.md`
- `docs/salvage-summary.md`

*No changes to active installations (`~/projects/prompt-engineer`, `~/.claude/skills/prompt-engineer`) or old repository (`~/mr-prompter`).*
