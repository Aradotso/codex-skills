---
name: keep-codex-fast-maintenance
description: Safely inspect, backup, and maintain local Codex state to keep performance fast and clean
triggers:
  - "inspect my Codex local state"
  - "clean up old Codex sessions"
  - "make Codex faster"
  - "create handoff documents before archiving"
  - "archive old Codex chats safely"
  - "backup Codex state"
  - "maintain Codex performance"
  - "check for Codex bloat"
---

# keep-codex-fast-maintenance

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

A backup-first maintenance skill for keeping local Codex state fast, clean, and recoverable. When Codex starts feeling heavy after weeks of chats, terminals, logs, worktrees, and project history, this gives you a calm way to inspect what's going on and reduce local drag without losing context.

## Core Principle

**Make handoffs first. Archive, don't delete. Apply changes only when you are ready.**

All operations are read-only by default. Nothing is mutated until you explicitly use `--apply`.

## Installation

Clone or copy this repository into your Codex skills directory:

```bash
cd ~/.codex/skills  # or your Codex skills path
git clone https://github.com/vibeforge1111/keep-codex-fast.git
```

Or ask Codex directly:

```text
Install the keep-codex-fast skill from https://github.com/vibeforge1111/keep-codex-fast
```

## Three Modes

1. **Inspect** (default): Report-only, no writes, privacy-safe
2. **Maintain**: Backs up, archives old sessions, moves stale worktrees, rotates logs, prunes dead config
3. **Repair** (optional): Only with `--repair-thread-metadata-bloat` flag; trims oversized SQLite title/preview metadata after backup

## Key Commands

### Inspect Mode (Read-Only)

Basic inspection report:

```bash
python scripts/keep_codex_fast.py
```

Detailed inspection with thread IDs, titles, and paths:

```bash
python scripts/keep_codex_fast.py --details
```

### Backup Mode

Create backups only without changing local state:

```bash
python scripts/keep_codex_fast.py --backup-only
```

**Important**: Backup folders contain private local Codex metadata. Keep them on your machine and do not share publicly.

### Maintenance Mode

Apply core maintenance (archives sessions, moves worktrees, rotates logs):

```bash
python scripts/keep_codex_fast.py --apply
```

Customize retention periods:

```bash
python scripts/keep_codex_fast.py --apply \
  --archive-older-than-days 10 \
  --worktree-older-than-days 7
```

Wait for Codex to exit before applying:

```bash
python scripts/keep_codex_fast.py --apply --wait-for-codex-exit
```

### Repair Thread Metadata Bloat (Advanced)

Only use when the report shows unusually large title/preview metadata:

```bash
python scripts/keep_codex_fast.py --apply --repair-thread-metadata-bloat
```

This trims oversized SQLite title/preview fields that can slow chat navigation. The actual conversation transcript remains intact.

## Handoffs First: Create Continuity Documents

Before archiving any important active chats, create handoff documents. These let you archive heavy chat history and start fresh threads without losing context.

Paste this into each active repo chat you want to preserve:

```text
Create a comprehensive handoff document for this repo/session before I archive Codex history.

Include:
- repo/path and branch
- current goal
- what we already completed
- files touched or investigated
- commands/tests already run
- known errors, warnings, or failing checks
- open decisions
- constraints, user preferences, and do-not-touch areas
- the next 3-7 concrete steps

Also include a reactivation prompt I can paste into a fresh Codex chat so it can continue from this handoff without relying on the old chat context.

Save the handoff in a sensible repo-local place like docs/codex-handoffs/YYYY-MM-DD-topic.md unless this repo already has a better handoff location.
```

## Common Usage Patterns

### Pattern 1: Safe Inspection and Maintenance

```text
Use $keep-codex-fast to inspect my Codex local state and recommend a safe maintenance plan.
```

After reviewing the report:

```text
Use $keep-codex-fast to apply safe Codex maintenance.

Before changing anything, confirm that important active repo chats have handoff docs or do not need them.

Then back up first, archive instead of deleting, move stale worktrees, rotate large logs, prune dead config references, and verify the result.

If Codex is currently running, do not mutate local state. Tell me to close Codex first.
```

### Pattern 2: Weekly Maintenance Reminder

```text
Use $keep-codex-fast to create a recurring Codex maintenance reminder.

Schedule it weekly if I use Codex heavily, or biweekly if that seems safer.

The reminder should:
- run the keep-codex-fast report first
- never pass --apply or run mutating maintenance automatically
- never archive, move, prune, rotate, normalize, delete, or mutate local Codex state
- remind me to create comprehensive handoff docs and reactivation prompts for active repo chats before any manual apply
- summarize active session size, archived session size, extended path candidates, old session candidates, worktree candidates, log size, and top Node/dev processes
- report heavy Node/dev processes without killing them
- tell me that manual apply should only happen after I confirm handoffs exist or are not needed and Codex is closed
```

### Pattern 3: Backup Before Major Changes

```bash
# Create backup snapshot before applying any changes
python scripts/keep_codex_fast.py --backup-only

# Review what will change
python scripts/keep_codex_fast.py --details

# Apply changes with custom retention
python scripts/keep_codex_fast.py --apply \
  --archive-older-than-days 14 \
  --worktree-older-than-days 10
```

## What Gets Maintained

### Active Sessions
- **Default retention**: 7 days
- Non-pinned sessions older than threshold are archived
- Pinned sessions are never archived
- Archives stored in timestamped backup folders

### Worktrees
- **Default retention**: 7 days
- Stale worktrees moved to archive location
- Active worktrees preserved
- Worktree references updated in config

### Logs
- Large `logs_2.sqlite*` files rotated
- Old logs compressed and archived
- Current logs preserved at manageable size

### Config
- Dead/temporary project entries pruned
- Windows extended paths (`\\?\C:\...`) normalized
- Invalid references cleaned up

### Thread Metadata (Optional)
- Only with `--repair-thread-metadata-bloat`
- Trims oversized title/preview fields in `state_5.sqlite`
- Conversation transcripts remain intact
- Repair manifest created for restore capability

## Configuration

The script uses sensible defaults. Override via command-line flags:

```python
# Default thresholds
ARCHIVE_OLDER_THAN_DAYS = 7
WORKTREE_OLDER_THAN_DAYS = 7
LOG_SIZE_THRESHOLD_MB = 100

# Override example
python scripts/keep_codex_fast.py --apply \
  --archive-older-than-days 14 \
  --worktree-older-than-days 10
```

## Real Code Example: Custom Maintenance Script

```python
#!/usr/bin/env python3
"""
Custom Codex maintenance wrapper
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def run_maintenance(dry_run=True):
    """Run Codex maintenance with custom settings"""
    
    # Create timestamped log
    log_dir = Path.home() / ".codex" / "maintenance-logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"maintenance-{datetime.now():%Y%m%d-%H%M%S}.log"
    
    # Build command
    cmd = [
        sys.executable,
        "scripts/keep_codex_fast.py",
    ]
    
    if not dry_run:
        cmd.append("--apply")
        cmd.extend([
            "--archive-older-than-days", "14",
            "--worktree-older-than-days", "10",
        ])
    else:
        cmd.append("--details")
    
    # Run with logging
    print(f"Running maintenance (dry_run={dry_run})...")
    print(f"Logging to: {log_file}")
    
    with open(log_file, "w") as f:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        f.write(result.stdout)
        print(result.stdout)
    
    return result.returncode == 0

if __name__ == "__main__":
    # First inspect
    print("=== INSPECTION PHASE ===")
    if not run_maintenance(dry_run=True):
        sys.exit(1)
    
    # Confirm before applying
    response = input("\nApply maintenance changes? (yes/no): ")
    if response.lower() == "yes":
        print("\n=== MAINTENANCE PHASE ===")
        run_maintenance(dry_run=False)
    else:
        print("Maintenance cancelled.")
```

## Troubleshooting

### "Codex is currently running"

Close Codex before applying changes:

```bash
# Wait for Codex to exit automatically
python scripts/keep_codex_fast.py --apply --wait-for-codex-exit

# Or manually close Codex first
```

### Backup folders growing large

Backups contain full session data and metadata. Clean old backups manually:

```bash
# List backups
ls -lh ~/.codex/backups/  # or wherever backups are stored

# Remove old backups (review first!)
find ~/.codex/backups -type d -mtime +30 -exec rm -rf {} +
```

### Thread metadata repair needed

When the report shows large title/preview metadata:

```text
Warning: Found threads with title/preview metadata > 10KB
Consider using --repair-thread-metadata-bloat
```

Apply the repair:

```bash
python scripts/keep_codex_fast.py --apply --repair-thread-metadata-bloat
```

Keep the repair manifest private. It contains the original full title/preview text.

### Restore from backup

If you need to restore state after applying changes:

1. Locate the backup folder (timestamped in output)
2. Follow instructions in `restore-instructions.txt` within backup
3. For thread metadata repairs, use `restore-thread-metadata.py`

### Process reporting without killing

The script reports heavy Node/dev processes but never kills them:

```bash
# Just inspect processes
python scripts/keep_codex_fast.py --details
```

You decide whether to stop processes manually.

## Mental Model

- **Chats** are for execution
- **Handoff docs** are for memory
- **Archives** are for history
- **Fresh threads** are for speed

## Safety Guarantees

1. **Read-only by default**: No writes without `--apply`
2. **Backup first**: All changes create timestamped backups
3. **Archive, don't delete**: Sessions and worktrees moved, not removed
4. **Restore artifacts**: Every change includes restore instructions
5. **Handoff prompts**: Preserve context before archiving
6. **Process detection**: Warns when Codex is running, never force-kills

## Advanced: Direct Script Integration

```python
from pathlib import Path
import sys

# Add keep-codex-fast to path
skill_path = Path(__file__).parent / "keep-codex-fast"
sys.path.insert(0, str(skill_path / "scripts"))

from keep_codex_fast import (
    inspect_codex_state,
    create_backup,
    apply_maintenance,
)

# Use as library
state = inspect_codex_state()
print(f"Active sessions: {state['active_session_count']}")
print(f"Total size: {state['total_size_mb']:.1f}MB")

# Create backup before custom operation
backup_path = create_backup()
print(f"Backup created: {backup_path}")
```

## When to Use This Skill

- Codex feels slower after weeks of heavy use
- Many long chat threads accumulated
- Working across multiple repos and worktrees
- Frequent terminal/dev server usage
- Want safe, reversible maintenance
- Need to reduce local state without losing context
