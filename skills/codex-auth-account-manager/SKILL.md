---
name: codex-auth-account-manager
description: CLI tool to switch and manage multiple Codex accounts seamlessly
triggers:
  - how do I switch between Codex accounts
  - manage multiple Codex logins
  - codex-auth account switching
  - list my Codex accounts and usage
  - import Codex auth tokens
  - switch active Codex account
  - export Codex account credentials
  - remove old Codex accounts
---

# Codex Auth Account Manager

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

`codex-auth` is a command-line tool for switching between multiple Codex accounts. It works with Codex CLI, VS Code extension, and Codex App. This skill covers installation, account management, import/export workflows, and API vs local-only modes.

## What It Does

- **Account switching**: Seamlessly switch between multiple Codex accounts stored locally
- **Usage tracking**: View token usage and limits for each account (API-backed or local-only)
- **Import/Export**: Batch import auth files or export for backup
- **Multi-client support**: Works with Codex CLI, VS Code extension, and Codex App

**Important**: After switching accounts with Codex CLI or Codex App, you must restart the client for changes to take effect. For seamless switching without restarts, use the forked [`codext`](https://github.com/Loongphy/codext) CLI.

## Installation

Install globally via npm:

```bash
npm install -g @loongphy/codex-auth
```

Or run without installing:

```bash
npx @loongphy/codex-auth list
```

Supported platforms: Linux (x64, arm64), macOS (x64, arm64), Windows (x64, arm64).

### Uninstall

```bash
npm uninstall -g @loongphy/codex-auth
```

## Account Management Commands

### List Accounts

View all stored accounts with usage information:

```bash
# List accounts with API-backed usage refresh (default)
codex-auth list

# List with live TUI auto-refresh
codex-auth list --live

# Show only the active account
codex-auth list --active

# Skip API calls, use local rollout files only
codex-auth list --skip-api
```

**Usage Data Modes**:
- **Default (API)**: Makes HTTPS requests to OpenAI endpoints using access tokens for accurate usage/limit data
- **Local-only (`--skip-api`)**: Reads `~/.codex/sessions/**/rollout-*.jsonl` files; may show stale data (hours old) due to `rate_limits: null` in recent Codex builds

### Add Accounts

Login and add a new account:

```bash
# Interactive browser login
codex-auth login

# Device-code authentication
codex-auth login --device-auth
```

This runs `codex login` internally, then stores the account in `codex-auth`'s registry.

### Switch Accounts

Interactive account picker:

```bash
# Interactive selection with API-backed usage
codex-auth switch

# Interactive with live TUI refresh
codex-auth switch --live

# Interactive, skip API calls
codex-auth switch --skip-api
```

Direct selection by row number or query:

```bash
# Switch to account at row 02
codex-auth switch 02

# Switch by email/alias substring
codex-auth switch work
codex-auth switch personal@example.com
```

### Remove Accounts

Interactive removal:

```bash
# Interactive multi-select with API-backed data
codex-auth remove

# Interactive with local-only data
codex-auth remove --skip-api
```

Direct removal by query:

```bash
# Remove specific accounts by selector
codex-auth remove work personal@example.com 03

# Remove all stored accounts
codex-auth remove --all
```

## Import and Export

### Import Accounts

Import a single auth file:

```bash
# Import with auto-generated alias
codex-auth import /path/to/auth.json

# Import with custom alias
codex-auth import /path/to/auth.json --alias work-account
```

Batch import from a folder:

```bash
# Import all auth.json files in a directory
codex-auth import /path/to/auth-folder
```

Import CLIProxyAPI token JSON:

```bash
# Import from default ./token.json
codex-auth import --cpa

# Import from custom path
codex-auth import --cpa /path/to/token.json
```

Rebuild registry from existing auth files:

```bash
# Purge and rebuild registry.json from managed auth files
codex-auth import --purge

# Rebuild from custom auth directory
codex-auth import --purge /custom/auth/dir
```

### Export Accounts

Export all managed auth files:

```bash
# Export to current directory
codex-auth export

# Export to specific directory
codex-auth export /backup/codex-auth

# Export as CLIProxyAPI token.json format
codex-auth export --cpa
codex-auth export --cpa /backup/tokens
```

## Maintenance

### Clean Stale Files

Remove managed backup and stale account files:

```bash
codex-auth clean
```

This deletes:
- Managed backup files created during account switches
- Stale account auth files no longer in the registry

## Configuration

### Live TUI Refresh Interval

Configure auto-refresh interval for `--live` mode:

```bash
# Set refresh interval to 10 seconds
codex-auth config live --interval 10

# Set refresh interval to 30 seconds
codex-auth config live --interval 30
```

## Common Workflows

### Daily Account Switching

```bash
# Morning: check all accounts and switch to work
codex-auth list
codex-auth switch work

# Evening: switch back to personal
codex-auth switch personal

# Restart Codex CLI or App for changes to take effect
```

### Batch Account Setup

```bash
# Import multiple auth files from a backup folder
codex-auth import ~/codex-backups/auth-files

# Verify imports
codex-auth list

# Switch to preferred account
codex-auth switch 01
```

### Usage Monitoring

```bash
# Quick active account check
codex-auth list --active

# Monitor all accounts with live refresh
codex-auth list --live

# Check usage without API calls (faster but possibly stale)
codex-auth list --skip-api
```

### Cleanup and Backup

```bash
# Export all accounts before cleanup
codex-auth export ~/codex-backup-$(date +%Y%m%d)

# Remove unused accounts
codex-auth remove old-work abandoned-test

# Clean stale files
codex-auth clean
```

## Troubleshooting

### Usage Limits Not Refreshing

**Symptom**: Usage data appears hours out of date.

**Cause**: When using `--skip-api`, local `rollout-*.jsonl` files may contain `rate_limits: null` (Codex issue [#14880](https://github.com/openai/codex/issues/14880)).

**Solution**: Use API-backed refresh (default):

```bash
# Use API for accurate data
codex-auth list

# Verify with actual usage
codex exec "say hello"
```

### Account Switch Not Taking Effect

**Symptom**: After switching accounts, Codex still uses old account.

**Solution**: Restart Codex CLI or Codex App after switching. Or use `codext` for seamless switching:

```bash
npm install -g @loongphy/codext
codext  # Enhanced CLI with auto account switching
```

### Import Fails

**Symptom**: `codex-auth import` doesn't find auth files.

**Solution**: Ensure you're importing valid `auth.json` files from `~/.codex/` or exported backups:

```bash
# Verify file exists and is valid JSON
cat /path/to/auth.json | jq .

# Try absolute path
codex-auth import /absolute/path/to/auth.json
```

### API Calls vs Privacy

**Concern**: Don't want to send tokens to OpenAI endpoints.

**Solution**: Use `--skip-api` for all commands:

```bash
codex-auth list --skip-api
codex-auth switch --skip-api
codex-auth remove --skip-api
```

Note: Team names won't refresh and usage data may be stale, but no API calls are made.

## Security Notes

- **API Mode**: Sends access tokens to `chatgpt.com/backend-api/wham/usage` and `chatgpt.com/backend-api/accounts/check/v4-2023-04-27`. May violate OpenAI ToS.
- **Local Mode**: Reads local files only, safer but less accurate.
- **Auth Storage**: All auth files stored in `~/.codex-auth/` (platform-specific). Keep this directory secure.

## Platform-Specific Paths

Auth files are stored in:
- **Linux/macOS**: `~/.codex-auth/`
- **Windows**: `%USERPROFILE%\.codex-auth\`

Original Codex auth:
- **All platforms**: `~/.codex/auth.json`

Session rollout files:
- **All platforms**: `~/.codex/sessions/**/rollout-*.jsonl`
