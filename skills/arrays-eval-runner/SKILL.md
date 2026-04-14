---
name: arrays-eval-runner
description: >
  Runs the Arrays Skills evaluation pipeline and analyzes results. Use this skill whenever
  the user asks to run evals, run tests, test skills, check eval scores, benchmark skills,
  run specific test cases, compare eval results, investigate test failures, or check the
  eval pass rate. Also use when the user mentions run_tests.py or simple-tests.csv.
---

# Arrays Eval Runner

Wraps `evals/run_tests.py` — a 4-step evaluation pipeline that tests how well LLMs use Arrays Data API skills:

1. **Skill Routing** — LLM selects which `arrays-data-api-*` skill handles the question
2. **Code Generation** — LLM writes Python code to call the REST API
3. **Code Execution** — Generated code runs against the live API
4. **LLM-as-Judge** — LLM scores the output against the expected answer (0.0–1.0, pass ≥ 0.7)

Test data: `evals/datasets/simple-tests.csv` (146 confirmed cases).

## Workflow

Follow these steps in order every time you run the eval. Do not skip any step.

### Step 0: Pre-flight checks (mandatory — do not skip)

Run these checks before executing run_tests.py. If any check fails, stop immediately and tell the user what to fix. Do not proceed to Step 1 until all checks pass.

**Check 0 — Load .env** (auto-load API keys from repo root):
```bash
if [ -f .env ]; then set -a && source .env && set +a && echo ".env loaded"; else echo "No .env file found (optional)"; fi
```
This exports all variables in `.env` so child processes (python) inherit them. Supported vars: `ARRAYS_API_KEY`, `ARRAYS_API_BASE_URL` (defaults to production if unset), `ANTHROPIC_API_KEY`. If `.env` doesn't exist, the user must have exported the keys manually.

**Check 1 — ARRAYS_API_KEY** (required for API calls in step 3):
```bash
echo "${ARRAYS_API_KEY:?ARRAYS_API_KEY is not set. Create .env with: echo 'ARRAYS_API_KEY=your-key' > .env}" > /dev/null
```

**Check 2 — LLM backend** (pick one):
- When running from Claude Code, use `--backend cli`. Verify the CLI exists:
  ```bash
  which claude > /dev/null 2>&1 && echo "claude CLI: OK" || echo "ERROR: claude CLI not found in PATH"
  ```
- If using `--backend api` instead, verify the API key:
  ```bash
  echo "${ANTHROPIC_API_KEY:?ANTHROPIC_API_KEY is not set}" > /dev/null
  ```

**Check 3 — Python dependencies**:
```bash
python -c "import anthropic, yaml" 2>/dev/null && echo "deps: OK" || echo "ERROR: Missing deps. Run: pip install -r evals/requirements.txt"
```

If any check prints an ERROR, tell the user the exact command to fix it and stop. Do not run run_tests.py.

### Step 1: Run the eval

All commands run from the repo root. Prefer `--backend cli` when running from Claude Code.

**Run all tests:**
```bash
python evals/run_tests.py --backend cli -v -o evals/results.json
```
Warning: 146 cases × ~35s each ≈ 85 minutes. Use `--limit` for faster feedback.

**Run specific cases:**
```bash
python evals/run_tests.py --backend cli --cases 196,198 -v
```

**Quick smoke test:**
```bash
python evals/run_tests.py --backend cli --limit 5 -v
```

**Dry run (routing + codegen only, no execution or judging):**
```bash
python evals/run_tests.py --backend cli --dry-run --limit 3 -v
```

**Using the wrapper script** (handles venv activation automatically):
```bash
bash skills/arrays-eval-runner/scripts/run_eval.sh --backend cli --limit 5 -v
```

## CLI Reference

| Flag | Description | Default |
|------|-------------|---------|
| `--backend api\|cli` | LLM backend | `api` |
| `--model <name>` | Model alias: `sonnet`, `haiku`, `opus` | `claude-sonnet` |
| `--cases <ids>` | Comma-separated case IDs (e.g. `38,57,123`) | all |
| `--limit <n>` | Max cases to evaluate | unlimited |
| `--dry-run` | Skip execution and judging | false |
| `-v, --verbose` | Print per-step details | false |
| `-o, --output <path>` | Save results JSON to path | `evals/simple-test-results.json` |
| `--base-url <url>` | Arrays API base URL | env `ARRAYS_API_BASE_URL` or production |
| `--api-key <key>` | Arrays API key | env `ARRAYS_API_KEY` |
| `--resume <path>` | Resume from a previous results JSON, skipping completed cases | none |

### Step 2: Parse and present results

The output JSON has this structure:

```
{
  "meta": { "timestamp", "backend", "model", "base_url", "total_cases", "elapsed_seconds" },
  "summary": {
    "total", "scored",
    "tool_accuracy",        // fraction of correct skill routing
    "code_success_rate",    // fraction of successful code execution
    "overall_pass_rate",    // fraction scoring >= 0.7
    "avg_overall_score"     // mean judge score
  },
  "by_tool": { "<api_name>": { "count", "tool_pass", "code_ok", "overall_pass" } },
  "cases": [
    {
      "case_id", "question", "api_names", "expected_answer",
      "tool_expected", "tool_actual", "tool_match",
      "code", "code_success", "code_output",
      "overall_score", "passed", "judge_reason"
    }
  ]
}
```

After running, present results as:

1. **Summary table**: tool_accuracy, code_success_rate, overall_pass_rate, avg_overall_score
2. **Failure list**: for each case where `passed=false`, show case_id, question (truncated), overall_score, and judge_reason
3. **Known issue flag**: mark failures that match known-issue case IDs (see below) — these are expected and not regressions
4. **Actionable failures**: failures NOT in the known-issues list — these need investigation

## Comparing Runs

To compare two result files:
```bash
python skills/arrays-eval-runner/scripts/diff_results.py evals/old-results.json evals/new-results.json
```

Add `--json` for machine-readable output. The diff shows:
- Summary metric deltas (pass rate, tool accuracy, etc.)
- New passes (previously failing, now passing)
- Regressions (previously passing, now failing)
- Per-case score changes

## Known Issues

Read `references/known-issues.md` for details. Summary:

| Type | Case IDs | Count |
|------|----------|-------|
| Unfixable | 38, 57, 60, 123, 197, 213, 239, 265 | 8 |
| Stochastic | 10, 598 | 2 |

Structural ceiling: ~83.3%. When analyzing failures, always cross-reference this list before flagging a case as a regression.

## Troubleshooting

| Error | Fix |
|-------|-----|
| `ARRAYS_API_KEY not set` | `export ARRAYS_API_KEY=<your-key>` |
| `ANTHROPIC_API_KEY env var is required` | Use `--backend cli` instead, or set the key |
| `TIMEOUT` in code execution | API may be slow; re-run the specific case with `--cases <id>` |
| `No skill documentation found` | Routing picked a nonexistent skill; check if skill SKILL.md exists |
| `claude CLI failed` | Ensure `claude` is in PATH and not blocked by session nesting |
