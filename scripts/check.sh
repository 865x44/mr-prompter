#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

echo "=== Python syntax check ==="
python3 -m py_compile scripts/prompt_engineer.py scripts/audit_consistency.py

echo "=== Consistency audit ==="
python3 scripts/audit_consistency.py

echo "=== Unit tests ==="
python3 -m unittest discover -s tests -v

echo "=== Git whitespace check ==="
git diff --check

echo ""
echo "All checks passed."
