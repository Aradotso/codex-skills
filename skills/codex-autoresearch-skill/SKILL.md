---
name: codex-autoresearch-skill
description: Self-directed iterative improvement system for Codex that cycles through modify, verify, retain/discard indefinitely
triggers:
  - "improve test coverage automatically"
  - "reduce TypeScript any types"
  - "fix failing tests iteratively"
  - "optimize performance metrics"
  - "run autoresearch loop"
  - "eliminate lint warnings"
  - "improve code quality overnight"
  - "autonomous code improvement"
---

# Codex Autoresearch Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## What is Codex Autoresearch?

Codex Autoresearch is an autonomous goal-driven experimentation system for Codex that continuously cycles through: modify code → verify result → retain (if improved) or discard (if worse) → repeat indefinitely. Tell Codex what you want to improve, walk away, and come back to a log of experiments and a better codebase.

**Key capabilities:**
- Autonomous iteration loops (foreground or background)
- Git-based experiment tracking with automatic revert on failure
- Dual-gate verification (did it improve? did anything break?)
- Escalating retry strategies (REFINE → PIVOT → Web search → Stop)
- Cross-run learning from past experiments
- Multiple modes: loop, plan, debug, fix, security, ship, exec

## Installation

### Recommended: Skill Installer

```bash
# In Codex
$skill-installer install https://github.com/leo-lilinxiao/codex-autoresearch
```

Then restart Codex.

### Manual Installation

```bash
# Clone to Codex skills directory
cd ~/.config/codex/skills
git clone https://github.com/leo-lilinxiao/codex-autoresearch

# Or create a symlink
ln -s /path/to/codex-autoresearch ~/.config/codex/skills/codex-autoresearch
```

## Prerequisites for Full Functionality

**For background runs and unattended execution:**

```bash
# Start Codex with Goals, hooks, and Full Access enabled
codex --enable goals --enable hooks --dangerously-bypass-approvals-and-sandbox
```

**For foreground-only usage:** Standard Codex workspace permissions are sufficient.

## Core Command

```bash
$codex-autoresearch
```

This is the single entry point. Codex will infer the mode and configuration from your natural language goal.

## Basic Usage Patterns

### 1. Improve Test Coverage

```text
You:   $codex-autoresearch
       I want to improve test coverage to at least 80%

Codex: Current coverage: 62% (measured via pytest --cov)
       Target: ≥80%
       Verify: pytest --cov --cov-report=term
       Guard: pytest passes
       Results directory: ./autoresearch-results/
       Run mode: foreground or background?

You:   Foreground, go.

Codex: Starting iteration loop — baseline: 62%
```

**What happens:**
- Codex identifies untested files/functions
- Writes new tests or improves existing ones
- Commits each change
- Runs coverage check
- Keeps if coverage increases, reverts if it decreases or tests fail
- Repeats until target reached or interrupted

### 2. Eliminate TypeScript `any` Types

```text
You:   $codex-autoresearch
       Get rid of all the any types in my TypeScript code

Codex: Found 47 `any` occurrences in src/**/*.ts
       Metric: `any` count (current: 47), direction: lower
       Verify: grep -r "any" src | wc -l
       Guard: npm run type-check (tsc --noEmit)
       Run mode?

You:   Background, run overnight.

Codex: Starting background run — baseline: 47. Iterating.
```

**Background mode:**
- Runs in detached process
- Logs to `autoresearch-results/results.tsv`
- Can be stopped/resumed
- Check progress: `tail -f autoresearch-results/results.tsv`

### 3. Fix Failing Tests

```text
You:   $codex-autoresearch
       Fix the 12 failing tests

Codex: Detected 12 test failures via pytest
       Strategy: Repair one failure at a time
       Verify: pytest (exit code 0 = success)
       Mode?

You:   Foreground.

Codex: Iteration 1: test_auth_token_expiry
       Root cause: Clock skew in mock time...
```

### 4. Optimize Performance

```text
You:   $codex-autoresearch
       Reduce API latency below 100ms

Codex: Current p95 latency: 247ms (from load test logs)
       Target: <100ms
       Verify: python benchmark.py --p95
       Guard: pytest integration tests
       Mode?

You:   Foreground.
```

### 5. Security Audit

```text
You:   $codex-autoresearch
       Is this code secure?

Codex: Mode: security audit
       Framework: STRIDE + OWASP Top 10
       Scope: src/**/*.py (detected Flask app)
       Findings will be logged with code evidence.
       Run mode?

You:   Foreground.

Codex: Finding 1/7: SQL Injection risk in user_search()
       Evidence: Line 42, raw string interpolation...
```

## Modes Reference

Codex infers the mode from your natural language, but understanding them helps you craft better prompts.

| Mode | Trigger Patterns | What It Does |
|------|-----------------|--------------|
| **loop** | "improve X", "reduce Y", "optimize Z" | Iterative improvement until target or interrupt |
| **plan** | "analyze", "what should I improve?", "suggest metrics" | Scans repo, proposes goals and metrics |
| **debug** | "why is X happening?", "diagnose", "root cause" | Hypothesis-driven debugging with falsifiable tests |
| **fix** | "fix the N failing tests", "repair", "make tests pass" | Sequential repair of known failures |
| **security** | "is this secure?", "audit", "STRIDE", "OWASP" | Security analysis with structured findings |
| **ship** | "ship it", "ready to release?", "pre-deploy check" | Release readiness verification |
| **exec** | (CI/CD usage, see below) | Non-interactive automation mode |

## Configuration

**You typically don't need to write config.** Codex infers from your repo and goal.

But if you want explicit control, Codex will show you the inferred config and let you adjust before starting:

```text
Codex: Inferred configuration:
       goal: "eliminate any types"
       scope: "src/**/*.ts"
       metric: any_count
       current_value: 47
       direction: lower
       verify_cmd: "grep -r 'any' src | wc -l"
       guard_cmd: "npm run type-check"
       
       Adjust anything?

You:   Change scope to include test files too.

Codex: Updated scope: "{src,test}/**/*.ts"
       Current value: 63 (including tests)
       Proceed?
```

### Explicit Config (Advanced)

For CI/CD or scripted use, you can provide a JSON config:

```json
{
  "goal": "Reduce bundle size",
  "metric": "bundle_kb",
  "current_value": 487,
  "target_value": 300,
  "direction": "lower",
  "verify_cmd": "npm run build && du -k dist/bundle.js | cut -f1",
  "guard_cmd": "npm test",
  "scope": "src/**/*.{ts,tsx}",
  "max_iterations": 50
}
```

```bash
# Save to file, then:
codex exec -f autoresearch_config.json
```

## Results and State Files

All runs create an `autoresearch-results/` directory in your workspace root:

```
autoresearch-results/
├── results.tsv          # Full experiment log (audit trail)
├── state.json           # Resume state (last consistent checkpoint)
├── lessons.json         # Cross-run learning (what worked/failed)
└── sessions/
    └── 2026-05-16_14-23-01/
        ├── experiment_1_keep.diff
        ├── experiment_2_discard.diff
        └── ...
```

### Reading the Results Log

```bash
# View all experiments
cat autoresearch-results/results.tsv

# Watch live (during background run)
tail -f autoresearch-results/results.tsv

# Filter successful improvements
grep "keep" autoresearch-results/results.tsv
```

**Example log:**

```
iteration	commit	metric	delta	status	description
0	a1b2c3d	47	0	baseline	initial any count
1	b2c3d4e	41	-6	keep	replace any in auth module
2	-	49	+8	discard	generic wrapper introduced new anys
3	d4e5f6g	38	-3	keep	type-narrow API response handlers
4	e5f6g7h	38	0	discard	refactor had no effect
5	f6g7h8i	35	-3	keep	infer types from JSON schema
```

## Escalation Strategy (When Stuck)

The loop doesn't blindly retry. It escalates:

| Trigger | Action |
|---------|--------|
| 3 consecutive failures | **REFINE** — Adjust within current strategy |
| 5 consecutive failures | **PIVOT** — Try fundamentally different approach |
| 2 PIVOTs without progress | **Web search** — Look for external solutions |
| 3 PIVOTs without progress | **STOP** — Report that human input needed |

**One success resets all counters.**

Example:

```text
Iteration 12: discard (3rd consecutive failure)
→ REFINE: Try smaller type changes, one file at a time

Iteration 17: discard (5th consecutive failure)
→ PIVOT: Switch from manual typing to codegen from OpenAPI spec

Iteration 23: discard (2nd PIVOT without progress)
→ Web search: "TypeScript eliminate any types best practices"
  Found: Use strictNullChecks + noImplicitAny...

Iteration 25: keep
→ Counters reset. Back to normal iteration.
```

## Stopping and Resuming

### Stop a Foreground Run

```text
You:   (interrupt Codex)

Codex: Autoresearch interrupted.
       State saved to autoresearch-results/state.json
       Resume with: $codex-autoresearch
```

### Stop a Background Run

```text
You:   $codex-autoresearch

Codex: Background run detected (PID 12345).
       Status: 15 iterations, metric improved 47→35
       
You:   Stop it.

Codex: Stopping background run...
       Final state saved. Resume anytime with $codex-autoresearch.
```

### Resume

```bash
$codex-autoresearch
```

Codex automatically detects `state.json` and offers to resume:

```text
Codex: Found interrupted session:
       Goal: eliminate any types
       Progress: 47→35 (12 iterations)
       Last commit: f6g7h8i
       Resume from iteration 13?

You:   Yes, continue.
```

## Dual-Gate Verification

Every iteration runs **two checks**:

1. **Verify** — Did the metric improve?
2. **Guard** — Did anything break?

```python
# Pseudocode of each iteration
git checkout -b experiment_N
modify_code()
git commit -m "experiment N: {hypothesis}"

verify_result = run(verify_cmd)
guard_result = run(guard_cmd)

if verify_result.improved and guard_result.passed:
    git merge experiment_N
    log("keep")
else:
    git reset --hard HEAD~1
    log("discard")
```

**Example:**

- **Verify:** `pytest --cov` (did coverage increase?)
- **Guard:** `pytest` (did all tests still pass?)

A change that increases coverage but breaks tests is **discarded**.

## CI/CD Mode (exec)

For automation pipelines, use `exec` mode:

```bash
# Non-interactive, JSON output, exit codes
codex exec -f config.json --max-iterations 20 --timeout 3600
```

**Exit codes:**
- `0` — Target reached
- `1` — Max iterations reached without target
- `2` — Error or guard failure

**Example config.json:**

```json
{
  "goal": "Reduce lint warnings to zero",
  "metric": "lint_warnings",
  "current_value": 34,
  "target_value": 0,
  "direction": "lower",
  "verify_cmd": "npm run lint -- --format json | jq '.length'",
  "guard_cmd": "npm test",
  "max_iterations": 30
}
```

**Output (JSON):**

```json
{
  "status": "success",
  "iterations": 18,
  "initial_value": 34,
  "final_value": 0,
  "improvements": 12,
  "discards": 6,
  "elapsed_seconds": 1847
}
```

## Advanced Features

### Parallel Experiments (Git Worktrees)

Test up to 3 hypotheses simultaneously:

```text
You:   $codex-autoresearch
       Try multiple approaches to reduce latency

Codex: Parallel mode enabled (3 worktrees).
       Hypothesis A: Database query optimization
       Hypothesis B: Response caching
       Hypothesis C: Async I/O refactor
       
       Testing in parallel...
       
       Results:
       A: -23ms (keep)
       B: -67ms (keep)  ← Best
       C: +12ms (discard)
       
       Merging B, continuing from new baseline.
```

### Cross-Run Learning

The `lessons.json` file accumulates knowledge:

```json
{
  "successful_patterns": [
    {
      "goal": "reduce any types",
      "approach": "infer from JSON schema",
      "success_rate": 0.83,
      "avg_improvement": 4.2
    }
  ],
  "failed_patterns": [
    {
      "goal": "reduce any types",
      "approach": "generic type wrappers",
      "failure_rate": 0.91,
      "reason": "introduced more anys downstream"
    }
  ]
}
```

Future runs bias toward proven approaches and away from known failures.

### Session Hooks (Auto-Persistence)

Hooks keep Codex on track across session boundaries:

```bash
# Auto-installed with skill
~/.config/codex/hooks/post-session.sh
```

On every Codex session end:
1. Saves current state to `state.json`
2. Commits results log to git (if repo)
3. Backs up lessons learned

**Manual hook setup (if needed):**

```bash
chmod +x ~/.config/codex/skills/codex-autoresearch/hooks/post-session.sh
ln -s ~/.config/codex/skills/codex-autoresearch/hooks/post-session.sh \
      ~/.config/codex/hooks/post-session.sh
```

## Real-World Examples

### Python: Improve Type Coverage

```python
# Before autoresearch
def process_data(data):  # No types
    result = []
    for item in data:
        result.append(item['value'] * 2)
    return result

# After 8 iterations
from typing import List, Dict, Any

def process_data(data: List[Dict[str, Any]]) -> List[float]:
    result: List[float] = []
    for item in data:
        result.append(float(item['value']) * 2)
    return result
```

**Command:**
```text
$codex-autoresearch
Improve type hints coverage to 90% with mypy strict mode
```

### JavaScript: Reduce Bundle Size

```javascript
// Before (487kb)
import _ from 'lodash';
import moment from 'moment';
import * as utils from './utils';

// After 12 iterations (312kb)
import { debounce, throttle } from 'lodash-es';  // Tree-shakeable
import { formatDate } from 'date-fns/formatDate';  // Targeted import
import { parseJSON, validateEmail } from './utils';  // Explicit imports
```

**Command:**
```text
$codex-autoresearch
Reduce production bundle size below 350kb
```

### Rust: Eliminate Clippy Warnings

```rust
// Before (23 clippy warnings)
fn calculate(x: i32, y: i32) -> i32 {
    let mut result = 0;
    for i in 0..x {
        result = result + y;  // clippy: use += instead
    }
    result
}

// After 5 iterations (0 warnings)
fn calculate(x: i32, y: i32) -> i32 {
    x * y  // Direct multiplication, clippy-clean
}
```

**Command:**
```text
$codex-autoresearch
Eliminate all clippy warnings with default lints
```

## Troubleshooting

### "Background run failed to start"

**Cause:** Codex not started with `--dangerously-bypass-approvals-and-sandbox`

**Fix:**
```bash
# Restart Codex with Full Access
codex --enable goals --enable hooks --dangerously-bypass-approvals-and-sandbox
```

Or use foreground mode instead.

### "Verify command failed"

**Cause:** The verify command isn't executable or returns unexpected format

**Fix:**
```text
You:   Test the verify command manually.

Codex: Running: grep -r "any" src | wc -l
       Output: "      47"  ← Extra spaces

You:   Adjust to: grep -r "any" src | wc -l | xargs

Codex: Updated verify_cmd. Baseline: 47 (clean integer).
```

### "All experiments discarded, no progress"

**Cause:** Guard too strict (e.g., flaky tests) or goal unachievable

**Check results log:**
```bash
grep "discard" autoresearch-results/results.tsv
```

**Common reasons:**
- Guard fails even on unchanged code (flaky tests)
- Metric can't be improved with current tooling
- Scope too broad (try narrowing)

**Fix:**
```text
You:   Run guard manually: npm test

Codex: Tests fail intermittently (test_cache_timeout).
       Recommendation: Fix flaky test or exclude from guard.

You:   Exclude that test from guard.

Codex: Updated guard: npm test -- --ignore test_cache_timeout
```

### "State file corrupted"

**Cause:** Interrupted during JSON write

**Fix:**
```bash
# Restore from git (if committed)
git restore autoresearch-results/state.json

# Or start fresh (loses resume state, keeps logs)
rm autoresearch-results/state.json
$codex-autoresearch
```

### "Infinite loop, no termination"

**Cause:** No target value set, or metric unstable

**Fix:**
```text
You:   Set max_iterations to 50 and stop.

Codex: Updated config: max_iterations = 50
       Will stop after 50 iterations regardless of target.
```

Or add explicit target:
```text
You:   Target is 80% coverage, stop when reached.

Codex: Updated target_value: 80
       Will stop when coverage ≥80%.
```

## Best Practices

### 1. Start with Small, Measurable Goals

❌ "Make the code better"
✅ "Reduce ESLint warnings from 42 to 0"

### 2. Verify Your Verify Command First

```bash
# Before starting autoresearch, confirm the metric works
pytest --cov --cov-report=term | grep TOTAL
# Should output a parseable percentage
```

### 3. Use Foreground for New Goals

Run foreground first to watch the loop and verify behavior. Switch to background once confident.

### 4. Let Codex Infer, Then Adjust

Don't write config upfront. Let Codex propose, then refine:

```text
Codex: Proposed verify: npm run test:coverage
You:   Change to: npm run test:coverage -- --json
Codex: Updated. Baseline: 62%
```

### 5. Check Results Log After Each Run

```bash
tail -20 autoresearch-results/results.tsv
```

Understand what worked and what didn't. This informs your next goal.

### 6. Use Git Strategically

Autoresearch commits every experiment. Your git log becomes the audit trail:

```bash
git log --oneline --grep="autoresearch"
```

To squash experiments into clean commits after the run:

```bash
git rebase -i HEAD~20  # Interactive rebase last 20 autoresearch commits
```

## Environment Variables

Autoresearch respects standard tool configs via environment:

```bash
# Example: Use specific Python for pytest
export PYTHON=/usr/bin/python3.11
$codex-autoresearch

# Example: Increase test timeout
export PYTEST_TIMEOUT=300
$codex-autoresearch
```

No secrets needed — autoresearch runs local tools, no external API calls.

## Integration with Other Codex Skills

Combine autoresearch with other skills:

```text
You:   $code-review
       Review the autoresearch improvements from last night.

Codex: Reviewing 12 commits in autoresearch-results/sessions/...
       
       Summary:
       - 8 type improvements: Good, no regressions detected
       - 3 test additions: Coverage gaps filled correctly
       - 1 refactor: Extracted helper, maintains behavior
       
       Recommendation: Merge to main.
```

```text
You:   $codex-autoresearch
       Optimize performance
       
       Then:
       $benchmark
       Compare before/after with flamegraphs
```

## Limitations

1. **Requires git** — All experiments are git-based (commit/revert cycle)
2. **Local tools only** — Verify and guard must be executable commands in your environment
3. **No multi-repo (yet)** — Operates within a single workspace root
4. **Deterministic metrics work best** — Flaky metrics lead to false discards

## Getting Help

If autoresearch behaves unexpectedly:

1. **Check the results log:** `cat autoresearch-results/results.tsv`
2. **Review state file:** `cat autoresearch-results/state.json`
3. **Run verify manually:** Test your verify command outside autoresearch
4. **Ask Codex to explain:** `$codex-autoresearch` then "explain the last 5 iterations"

## Summary

Codex Autoresearch is a single-command autonomous improvement loop:

```bash
$codex-autoresearch
```

You describe the goal in natural language. Codex infers the config, confirms with you, then iterates:

**modify → commit → verify → keep or discard → repeat**

Foreground for interactive runs. Background for overnight. Results logged, state resumable, lessons learned across runs.

**Most common workflow:**

```text
$codex-autoresearch
I want to [measurable goal]
→ Codex proposes config
→ You confirm or adjust
→ Choose foreground/background
→ Walk away or watch
→ Review results.tsv
→ Merge improvements
```

That's it. Autonomous iteration with human-in-the-loop goal-setting.
