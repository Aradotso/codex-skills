---
name: codex-provider-sync-skill
description: Synchronize Codex session provider metadata across rollout files and SQLite state when switching providers
triggers:
  - "my codex sessions disappeared after switching providers"
  - "how do I restore codex session visibility"
  - "sync codex provider metadata"
  - "codex sessions not showing in desktop"
  - "switch codex model provider"
  - "fix codex session visibility issues"
  - "restore codex archived sessions"
  - "sync codex sqlite state"
---

# codex-provider-sync

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## What It Does

`codex-provider-sync` solves a specific Codex problem: when you switch `model_provider` (e.g., from OpenAI to Anthropic, or vice versa), historical sessions may become invisible in Codex Desktop or `/resume` — not because the session files are lost, but because provider/visibility metadata across rollout files, SQLite thread tables, and project path caches becomes inconsistent.

This tool synchronizes metadata in:
- `~/.codex/sessions` (rollout files)
- `~/.codex/archived_sessions`
- `~/.codex/state_5.sqlite` (threads table)
- `.codex-global-state.json` (project root path cache)

**Important limitations:**
- Does **not** modify session content, messages, or titles
- Does **not** handle authentication or `auth.json`
- Does **not** re-encrypt `encrypted_content` across providers
- Does **not** modify `updated_at` timestamps to change session ordering
- Sessions with `encrypted_content` may only regain list visibility; continuing them may still error with `invalid_encrypted_content`

## Installation

### Windows GUI (Recommended)

Download `CodexProviderSync.exe` from the [Releases page](https://github.com/Dailin521/codex-provider-sync/releases):

1. Extract the release ZIP
2. Run `CodexProviderSync.exe`
3. Click **Refresh** to scan current state
4. Select target provider
5. Click **Execute** to sync

### CLI (macOS/Linux/Node.js)

Requires Node.js 24+ (due to `node:sqlite` dependency):

```bash
npm install -g git+https://github.com/Dailin521/codex-provider-sync.git
```

Or clone and run locally:

```bash
git clone https://github.com/Dailin521/codex-provider-sync.git
cd codex-provider-sync
npm install
npm link
```

## Key Commands

### Status Check (Dry Run)

Check current provider, rollout metadata, SQLite state, and project visibility without making changes:

```bash
codex-provider status
```

Sample output:
```
[INFO] Current provider: openai
[INFO] Rollout files: 127 (openai: 50, anthropic: 77)
[INFO] SQLite threads: 130
[INFO] Project visibility: 12/15 projects have visible sessions
[WARN] Project /home/user/my-project: first page 0/50, ranks 64-77 (Desktop likely won't show)
```

### Sync Metadata (No Provider Switch)

Synchronize all historical session metadata to the current provider **without** changing `config.toml`:

```bash
codex-provider sync
```

This updates:
- Rollout files `model_provider` field
- SQLite `threads.model_provider`
- Project root path caches in `.codex-global-state.json`

### Switch Provider & Sync

Change the root-level `model_provider` in `config.toml` and sync all metadata:

```bash
codex-provider switch anthropic
codex-provider switch openai
codex-provider switch apigather
```

This:
1. Updates `~/.codex/config.toml` `model_provider`
2. Syncs all rollout/SQLite/project metadata to the new provider

### Restore from Backup

Every `sync`/`switch` creates a timestamped backup in `~/.codex/backups_state/provider-sync/<timestamp>`.

Restore all:

```bash
codex-provider restore ~/.codex/backups_state/provider-sync/2026-05-16T123045
```

Restore selectively:

```bash
# Restore only config.toml
codex-provider restore <backup-dir> --no-db --no-sessions

# Restore only SQLite
codex-provider restore <backup-dir> --no-config --no-sessions

# Restore only session rollouts
codex-provider restore <backup-dir> --no-config --no-db
```

### Prune Old Backups

Keep only the last N backups created by this tool:

```bash
codex-provider prune-backups --keep 5
```

This only touches backups in `~/.codex/backups_state/provider-sync/`, not other Codex backups.

## Configuration

The tool reads from standard Codex config paths:

| File                          | Purpose                                      |
|-------------------------------|----------------------------------------------|
| `~/.codex/config.toml`        | Root-level `model_provider`                  |
| `~/.codex/state_5.sqlite`     | Threads table with `model_provider` column   |
| `~/.codex/sessions/*.rollout` | Active session rollout files                 |
| `~/.codex/archived_sessions/` | Archived session rollout files               |
| `.codex-global-state.json`    | Project root path cache (workspace metadata) |

No additional configuration needed. The tool auto-detects Codex home directory from:
- `CODEX_HOME` environment variable (if set)
- Default: `~/.codex` (macOS/Linux) or `%USERPROFILE%\.codex` (Windows)

## Code Examples (Node.js/JavaScript)

### Programmatic Status Check

```javascript
import { checkStatus } from 'codex-provider-sync';

async function diagnose() {
  const result = await checkStatus({
    codexHome: process.env.CODEX_HOME || require('os').homedir() + '/.codex',
    verbose: true
  });

  console.log('Current provider:', result.currentProvider);
  console.log('Rollout files:', result.rolloutStats);
  console.log('SQLite threads:', result.sqliteStats);
  console.log('Project issues:', result.projectDiagnostics);
}

diagnose().catch(console.error);
```

### Programmatic Sync

```javascript
import { syncProvider } from 'codex-provider-sync';

async function syncToAnthropic() {
  const backupPath = await syncProvider({
    targetProvider: 'anthropic',
    codexHome: process.env.CODEX_HOME,
    createBackup: true,
    verbose: true
  });

  console.log('Sync complete. Backup:', backupPath);
}

syncToAnthropic().catch(console.error);
```

### Programmatic Provider Switch

```javascript
import { switchProvider } from 'codex-provider-sync';

async function switchToOpenAI() {
  const result = await switchProvider({
    newProvider: 'openai',
    codexHome: process.env.CODEX_HOME,
    updateConfig: true, // Modify config.toml
    syncMetadata: true  // Sync all sessions
  });

  console.log('Switched to:', result.provider);
  console.log('Sessions synced:', result.sessionsUpdated);
  console.log('Backup:', result.backupPath);
}

switchToOpenAI().catch(console.error);
```

### Restore from Backup

```javascript
import { restoreBackup } from 'codex-provider-sync';

async function rollback() {
  await restoreBackup({
    backupDir: '/home/user/.codex/backups_state/provider-sync/2026-05-16T123045',
    restoreConfig: true,
    restoreDb: true,
    restoreSessions: true
  });

  console.log('Restore complete');
}

rollback().catch(console.error);
```

## Common Patterns

### Before/After Major Provider Switch

```bash
# 1. Check current state
codex-provider status

# 2. Switch and auto-backup
codex-provider switch anthropic

# 3. Verify sessions visible in Desktop
# If issues persist, restore:
codex-provider restore ~/.codex/backups_state/provider-sync/<latest>
```

### Manual Rollout File Inspection

Rollout files are newline-delimited JSON. Each session has metadata in the first line:

```bash
# Check first line of a rollout file
head -n 1 ~/.codex/sessions/<session-id>.rollout | jq .
```

Look for `model_provider` field:

```json
{
  "session_id": "abc123",
  "model_provider": "openai",
  "created_at": 1715900000000,
  "project_root": "/home/user/my-project"
}
```

If this doesn't match your current provider, sessions won't appear in Desktop.

### Sync Only Specific Provider (Not Implemented Yet)

Current tool syncs **all** sessions to the target provider. If you need selective sync (e.g., keep some sessions on OpenAI, others on Anthropic), you must manually edit rollout files or filter before sync.

## Codex Desktop 50-Session Limit

Codex Desktop currently loads only the **most recent 50 sessions** on first page load. This is an upstream limitation.

**Symptoms:**
- CLI `/resume` shows sessions that Desktop doesn't
- Project sidebar shows "No conversations" even after sync
- `codex-provider status` reports `ranks 64-77` (beyond first 50)

**Workarounds:**
- Use CLI `/resume` to access sessions beyond rank 50
- Wait for Codex Desktop to implement project-scoped pagination
- Don't modify `updated_at` to force old sessions into top 50 (not supported by this tool)

## Troubleshooting

### "Database is locked" / "SQLITE_BUSY"

**Cause:** Codex Desktop, Codex App, or `app-server` has `state_5.sqlite` open.

**Fix:**
1. Close all Codex applications
2. Kill `app-server` process if running:
   ```bash
   # macOS/Linux
   pkill -f app-server
   
   # Windows
   taskkill /IM codex.exe /F
   ```
3. Re-run `codex-provider sync`

### "Malformed database" / "Unreadable SQLite"

**Cause:** `state_5.sqlite` is corrupted.

**Fix:**
1. Check if a backup exists: `~/.codex/backups_state/`
2. Restore from backup:
   ```bash
   codex-provider restore <backup-dir> --no-config --no-sessions
   ```
3. If no backup, SQLite recovery is beyond this tool's scope

### Rollout File Locked (Session in Use)

**Symptom:** Tool skips certain `.rollout` files with "file locked" warning.

**Cause:** Active Codex session has the file open.

**Fix:**
1. Close the specific session in Codex
2. Re-run sync (tool will process previously skipped files)

### GUI EXE Won't Start (Windows)

**Symptoms:**
- Double-clicking `CodexProviderSync.exe` does nothing
- No window appears

**Diagnostics:**
1. Check `%AppData%\codex-provider-sync\startup-error.log`
2. Run from PowerShell to see console output:
   ```powershell
   cd C:\path\to\extracted\folder
   .\CodexProviderSync.exe
   ```
3. Verify all files were extracted (ZIP extraction issue)
4. Check Windows SmartScreen didn't block execution

### Sessions Still Invisible After Sync

**Checklist:**
1. Run `codex-provider status` — check provider matches config
2. Check session ranks — if beyond 50, Desktop won't show (see "50-Session Limit")
3. Verify `state_5.sqlite` `threads.model_provider` updated:
   ```bash
   sqlite3 ~/.codex/state_5.sqlite "SELECT model_provider, COUNT(*) FROM threads GROUP BY model_provider;"
   ```
4. Check project root path cache in `.codex-global-state.json`
5. If session has `encrypted_content`, it may not be continuable cross-provider

### Node Version Error (node:sqlite)

**Symptom:** `Cannot find module 'node:sqlite'`

**Cause:** Node.js <24 doesn't have built-in SQLite.

**Fix:** Upgrade to Node.js 24+:
```bash
# Using nvm
nvm install 24
nvm use 24

# Or download from nodejs.org
```

## Advanced: Manual Metadata Editing

If you need surgical changes (not recommended), rollout files are JSON-lines:

```javascript
// Read rollout file
const fs = require('fs');
const lines = fs.readFileSync('~/.codex/sessions/abc123.rollout', 'utf-8').split('\n');

// Parse first line (metadata)
const meta = JSON.parse(lines[0]);
console.log('Current provider:', meta.model_provider);

// Change provider (manual edit)
meta.model_provider = 'anthropic';
lines[0] = JSON.stringify(meta);

// Write back
fs.writeFileSync('~/.codex/sessions/abc123.rollout', lines.join('\n'));
```

**Warning:** Always backup before manual edits. Use the official CLI when possible.

## Safety & Backups

Every `sync`/`switch` automatically creates:

```
~/.codex/backups_state/provider-sync/<timestamp>/
  ├── config.toml
  ├── state_5.sqlite
  ├── sessions/
  └── archived_sessions/
```

**Backup retention:**
- Default: unlimited (manually prune with `prune-backups`)
- Recommended: `codex-provider prune-backups --keep 10`

**Restore example:**
```bash
# Full restore
codex-provider restore ~/.codex/backups_state/provider-sync/2026-05-16T123045

# Config only
codex-provider restore <backup> --no-db --no-sessions
```

## Testing

```bash
# JavaScript tests
npm test

# C# GUI tests (if contributing to desktop app)
dotnet test desktop/CodexProviderSync.Core.Tests/CodexProviderSync.Core.Tests.csproj
```

## License

MIT
