#!/usr/bin/env bash
set -euo pipefail

# Resolve the arrays-skills repo root (this script lives in skills/arrays-eval-runner/scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
EVALS_DIR="$REPO_ROOT/evals"

if [ ! -f "$EVALS_DIR/run_tests.py" ]; then
    echo "ERROR: Cannot find evals/run_tests.py at $EVALS_DIR" >&2
    echo "Make sure this script is inside the arrays-skills repo." >&2
    exit 1
fi

# Load .env if it exists (auto-export all vars for child processes)
if [ -f "$REPO_ROOT/.env" ]; then
    set -a && source "$REPO_ROOT/.env" && set +a
fi

# Check required env var
if [ -z "${ARRAYS_API_KEY:-}" ]; then
    echo "ERROR: ARRAYS_API_KEY is not set." >&2
    echo "Set it with: export ARRAYS_API_KEY=your-key-here" >&2
    exit 1
fi

# Activate venv if it exists, otherwise use system Python
if [ -d "$EVALS_DIR/.venv" ]; then
    source "$EVALS_DIR/.venv/bin/activate"
elif [ -d "$REPO_ROOT/.venv" ]; then
    source "$REPO_ROOT/.venv/bin/activate"
fi

# Run the eval
cd "$EVALS_DIR"
exec python run_tests.py "$@"
