---
name: fablecodex-workflow
description: Evidence-based workflow gates for Codex with goal ledgers, findings tracking, and Fable-inspired discipline.
triggers:
  - use fablecodex workflow
  - apply fable workflow discipline
  - track goals and findings
  - use evidence-based workflow
  - implement with goal ledger
  - review with findings gate
  - strict codex workflow
  - fable-style verification
---

# FableCodex Workflow

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

FableCodex is a Codex plugin that adds Fable-inspired operating habits: inspect first, track goals, record evidence, close review findings, and verify before claiming completion. It provides workflow discipline through local ledgers, evidence checkpoints, and verification gates.

**Key principle**: The skill improves discipline, not raw model capability. It's useful when the cost of a missed step is higher than the cost of a little process.

## Installation

Install stable release:

```bash
codex plugin marketplace add baskduf/FableCodex --ref v0.4.1
codex plugin add codex-fable5@fablecodex
```

Development version:

```bash
codex plugin marketplace add baskduf/FableCodex --ref main
codex plugin add codex-fable5@fablecodex
```

Local development:

```bash
codex plugin marketplace add ~/path/to/FableCodex
codex plugin add codex-fable5@fablecodex
```

Restart Codex after installation.

## Basic Usage

Invoke the skill in your Codex prompt:

```text
@codex-fable5 Use this skill to implement the change.
Create a goal ledger if the work has multiple steps.
Track findings before final completion.
Run the project tests before saying it is done.
```

Lighter review mode:

```text
@codex-fable5 Review this quickly.
Do not create a goal ledger. Check the key evidence and report only actionable findings.
```

## Workflow Gates

When you invoke `@codex-fable5`, Codex applies this workflow:

1. **Classify** the task before acting
2. **Inspect** workspace, files, tools, or cited sources
3. **Use Codex-native tools** instead of relying on memory
4. **Track goals** with evidence checkpoints for long work
5. **Track findings** for review-sensitive work
6. **Verify** with tests, lint, typecheck, screenshots, command output
7. **Report** what changed, what was verified, what risk remains

## Goal Ledger

For multi-step work, FableCodex maintains state in `.codex-fable5/goals.json`.

### Create Goal Ledger

```bash
# Add plugin bin to PATH
export PATH="$PWD/plugins/codex-fable5/bin:$PATH"

# Create goal ledger
codex-fable5 goals create --brief "Database migration" \
  --goal "inspect::Review current schema and migrations" \
  --goal "change::Add new migration file" \
  --goal "verify::Run migration and test queries"
```

### Work Through Goals

```bash
# Show next goal to work on
codex-fable5 goals next

# Mark goal complete with evidence
codex-fable5 goals checkpoint \
  --id G001 \
  --status complete \
  --evidence "Reviewed schema.sql and migrations/001_init.sql; current schema has users and posts tables."

# Move to next goal
codex-fable5 goals next
```

### Final Verification

Final goals require verification evidence:

```bash
codex-fable5 goals checkpoint \
  --id G003 \
  --status complete \
  --evidence "Created migration 002_add_comments.sql and ran against test DB." \
  --verify-cmd "psql test_db -f migrations/002_add_comments.sql && pytest tests/test_db.py -v" \
  --verify-evidence "Migration applied successfully, all 12 tests passed."
```

### Goal Statuses

- `pending`: Not started
- `active`: In progress
- `complete`: Done with evidence
- `failed`: Could not complete
- `blocked`: Waiting on external dependency

## Findings Gate

Findings are review issues that must not be lost. Stored in `.codex-fable5/findings.json`.

### Add Finding

```bash
codex-fable5 findings add \
  --title "SQL injection vulnerability in search" \
  --severity high \
  --source review \
  --location "src/db/queries.py:45" \
  --evidence "String concatenation used for WHERE clause instead of parameterized query."
```

Severity levels: `low`, `medium`, `high`, `critical`

### Resolve Finding

Only resolve after fix and verification:

```bash
codex-fable5 findings resolve \
  --id F001 \
  --evidence "Converted search query to use parameterized statements with cursor.execute(query, params)." \
  --verify-cmd "pytest tests/test_db_security.py -v -k test_sql_injection" \
  --verify-evidence "Security test passed: no injection detected."
```

### Show Next Finding

```bash
codex-fable5 findings next
```

Shows highest-priority open finding.

### Run Findings Gate

```bash
codex-fable5 findings gate
```

Gate fails while `open` or `blocked` findings remain. Use before final completion.

## Status Overview

Check overall progress:

```bash
codex-fable5 status
```

Shows:
- Current goal state
- Open findings count by severity
- Blocked items

## Prompt Patterns

### Strict Implementation

```text
@codex-fable5 Run this strictly.
Use a goal ledger, record any review findings, and do not finish until tests and findings gate pass.

Task: Migrate authentication from JWT to OAuth2
```

### Analysis Only

```text
@codex-fable5 Analyze only.
Do not edit files. Give findings with file and line references.

Review the payment processing code for security issues.
```

### Implementation with Limits

```text
@codex-fable5 Implement the fix.
Do not commit, push, or delete branches.
Run unit tests and report any residual risk.

Fix the memory leak in the worker pool.
```

### Debugging

```text
@codex-fable5 Debug this failure.
Reproduce it first, keep multiple hypotheses, gather disconfirming evidence, then fix and verify.

CI failing on test_concurrent_writes
```

### Quick Review

```text
@codex-fable5 Review this PR quickly.
Focus on security and correctness. Report high/critical findings only.
```

## Command Reference

| Command | Purpose |
|---------|---------|
| `codex-fable5 status` | Show findings and goal progress |
| `codex-fable5 goals create` | Create multi-step goal ledger |
| `codex-fable5 goals next` | Start or resume next goal |
| `codex-fable5 goals checkpoint` | Mark goal status with evidence |
| `codex-fable5 findings add` | Record review finding |
| `codex-fable5 findings next` | Show highest-priority open finding |
| `codex-fable5 findings resolve` | Close finding with verification |
| `codex-fable5 findings gate` | Fail if open/blocked findings remain |

## Local State Files

FableCodex writes local state under `.codex-fable5/`:

- `goals.json`: Goal plan and evidence
- `findings.json`: Review findings and closeout
- `ledger.jsonl`: Append-only event history

These files are local working state. Add `.codex-fable5/` to `.gitignore` unless you want to preserve task transcripts.

## Python API

The helpers are Python scripts with stdlib-only dependencies.

### Goals Helper

```python
# From plugins/codex-fable5/skills/codex-fable5/scripts/codex_goals.py
import json
import sys
from pathlib import Path

# Create goal ledger
goals_data = {
    "brief": "API refactor",
    "goals": [
        {
            "id": "G001",
            "phase": "inspect",
            "description": "Review existing API endpoints",
            "status": "pending"
        }
    ]
}

goals_file = Path(".codex-fable5/goals.json")
goals_file.parent.mkdir(parents=True, exist_ok=True)
goals_file.write_text(json.dumps(goals_data, indent=2))

# Checkpoint goal
data = json.loads(goals_file.read_text())
for goal in data["goals"]:
    if goal["id"] == "G001":
        goal["status"] = "complete"
        goal["evidence"] = "Reviewed 12 endpoints in api/v1/"
        goal["completed_at"] = "2026-06-17T10:30:00Z"
goals_file.write_text(json.dumps(data, indent=2))
```

### Findings Helper

```python
# From plugins/codex-fable5/skills/codex-fable5/scripts/codex_findings.py
import json
from pathlib import Path

# Add finding
findings_data = {
    "findings": [
        {
            "id": "F001",
            "title": "Missing error handling",
            "severity": "medium",
            "status": "open",
            "source": "review",
            "location": "src/api/handlers.py:89",
            "evidence": "No try-except around database call",
            "created_at": "2026-06-17T10:45:00Z"
        }
    ]
}

findings_file = Path(".codex-fable5/findings.json")
findings_file.parent.mkdir(parents=True, exist_ok=True)
findings_file.write_text(json.dumps(findings_data, indent=2))

# Resolve finding
data = json.loads(findings_file.read_text())
for finding in data["findings"]:
    if finding["id"] == "F001":
        finding["status"] = "resolved"
        finding["resolution"] = "Added try-except with proper error logging"
        finding["verify_cmd"] = "pytest tests/test_error_handling.py -v"
        finding["verify_evidence"] = "All error handling tests passed"
        finding["resolved_at"] = "2026-06-17T11:00:00Z"
findings_file.write_text(json.dumps(data, indent=2))
```

## When to Use FableCodex

✅ **Use for:**
- Multi-step implementation or refactoring
- Debugging where root cause is not obvious
- CI failures, release work, migrations
- Security-sensitive changes
- Reviews where unresolved findings should block completion
- Converting Claude/Fable-style prompts to Codex

❌ **Skip for:**
- Short answers
- Tiny single-file edits
- Brainstorming
- Tasks where ledger process is heavier than the work

## Configuration

No configuration file required. Control behavior through prompt instructions.

### Environment Variables

If using optional provider bridge:

```bash
export ANTHROPIC_API_KEY=your_key_here
export LITELLM_GATEWAY_URL=http://localhost:8000
```

See `plugins/codex-fable5/skills/codex-fable5/references/provider-bridge.md` for routing setup.

## Testing

Run the test suite:

```bash
python3 -m unittest discover -s tests -v
```

Test individual helpers:

```bash
python3 -m unittest tests.test_goals
python3 -m unittest tests.test_findings
```

## Coverage Accounting

Check source-heading coverage against CLAUDE-FABLE-5.md:

```bash
python3 plugins/codex-fable5/skills/codex-fable5/scripts/fable_coverage.py \
  --source /path/to/CLAUDE-FABLE-5.md
```

Target is 100% source-heading accounting (not model-weight parity).

## Troubleshooting

### Command not found

If `codex-fable5` is not found:

```bash
# Option 1: Add to PATH
export PATH="$PWD/plugins/codex-fable5/bin:$PATH"

# Option 2: Use full path
plugins/codex-fable5/bin/codex-fable5 status
```

### Goals file corrupted

```bash
# Backup and recreate
cp .codex-fable5/goals.json .codex-fable5/goals.json.bak
codex-fable5 goals create --brief "Recovery" --goal "inspect::Assess state"
```

### Findings gate failing

Check open findings:

```bash
codex-fable5 status
codex-fable5 findings next
```

Resolve all findings before running gate.

### Plugin not loading

```bash
# Restart Codex
codex restart

# Check plugin list
codex plugin list

# Reinstall if needed
codex plugin remove codex-fable5
codex plugin add codex-fable5@fablecodex
```

## Real-World Example

Complete workflow for a database migration:

```bash
# 1. Create goal ledger
codex-fable5 goals create --brief "Add user roles" \
  --goal "inspect::Review schema and existing migrations" \
  --goal "design::Plan role system design" \
  --goal "change::Create migration and update models" \
  --goal "verify::Test migration and queries"

# 2. Work through goals
codex-fable5 goals next
# ... do inspection work ...
codex-fable5 goals checkpoint --id G001 --status complete \
  --evidence "Reviewed schema.sql; users table has no role column. Last migration is 005_add_indexes.sql"

codex-fable5 goals next
# ... design role system ...
codex-fable5 goals checkpoint --id G002 --status complete \
  --evidence "Designed enum role type (admin, user, guest) and roles table with foreign key to users"

# 3. Add finding during implementation
codex-fable5 findings add \
  --title "Migration needs rollback path" \
  --severity high \
  --source self \
  --location "migrations/006_add_roles.sql" \
  --evidence "No down migration provided for role changes"

# 4. Complete implementation
codex-fable5 goals checkpoint --id G003 --status complete \
  --evidence "Created 006_add_roles.sql with up and down migrations. Updated User model."

# 5. Resolve finding
codex-fable5 findings resolve --id F001 \
  --evidence "Added down migration that drops roles table and removes role column" \
  --verify-cmd "psql test_db -f migrations/006_add_roles.sql && psql test_db -f migrations/006_add_roles_down.sql" \
  --verify-evidence "Both up and down migrations ran successfully"

# 6. Final verification
codex-fable5 goals checkpoint --id G004 --status complete \
  --evidence "Ran migration against test database and verified role queries" \
  --verify-cmd "pytest tests/test_user_roles.py -v" \
  --verify-evidence "All 8 role tests passed"

# 7. Run gates
codex-fable5 findings gate
codex-fable5 status
# All complete, ready to commit
```

## License

AGPL-3.0-or-later. See project LICENSE and NOTICE files.

---

FableCodex adds workflow discipline to Codex without changing model weights or capabilities. It's a procedural skill for higher-stakes work where verification and evidence matter.
