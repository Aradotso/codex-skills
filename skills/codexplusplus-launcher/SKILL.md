---
name: codexplusplus-launcher
description: Enhanced launcher for Codex App that unlocks plugins, enables session deletion, exports conversations, and syncs provider sessions via CDP injection
triggers:
  - how do I set up Codex++ to enhance my Codex App
  - install and configure the Codex++ launcher
  - enable session deletion in Codex App
  - unlock plugins in Codex API key mode
  - export Codex conversations to markdown
  - sync provider sessions in Codex++
  - troubleshoot Codex++ not launching
  - configure Codex++ settings and features
---

# Codex++ Launcher Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Codex++ is an external enhancement launcher for Codex App that doesn't modify the original installation. It uses Chromium DevTools Protocol (CDP) to inject enhancement scripts that unlock plugins in API key mode, enable session deletion, export conversations to Markdown, sync provider sessions, and add a timeline view.

## Installation

### Windows

**Quick setup using batch script:**

```bash
# Clone the repository
git clone https://github.com/BigPizzaV3/CodexPlusPlus.git
cd CodexPlusPlus

# Run setup.bat and select option [1]
setup.bat
```

**Command line installation:**

```bash
# Install dependencies
python -m pip install -e .

# Create shortcuts and uninstall entry
python -m codex_session_delete setup

# Launch Codex++
python -m codex_session_delete launch
```

After setup, double-click `Codex++.lnk` on the desktop to launch.

### macOS

```bash
# Install
python -m pip install -e .

# Create /Applications/Codex++.app bundle
python -m codex_session_delete setup

# Launch from Applications or command line
python -m codex_session_delete launch
```

## Key Commands

### Launch and Setup

```bash
# Launch Codex++ (with CDP injection)
python -m codex_session_delete launch

# Launch with custom ports
python -m codex_session_delete launch --debug-port 9229 --helper-port 57321

# Launch with specific Codex installation
python -m codex_session_delete launch \
  --app-dir "C:/Program Files/WindowsApps/OpenAI.Codex_xxx/app"

# Install shortcuts/app bundle
python -m codex_session_delete setup

# Uninstall (keeps logs and backups)
python -m codex_session_delete remove

# Uninstall and remove all data
python -m codex_session_delete remove --remove-data
```

### Updates

```bash
# Check for updates
python -m codex_session_delete check-update

# Update to latest version
python -m codex_session_delete update
```

### Windows Auto-Watcher (Optional)

Automatically intercept Codex launches and use Codex++ instead:

```bash
# Install watcher
python -m codex_session_delete watch-install

# Remove watcher
python -m codex_session_delete watch-remove

# Temporarily disable watcher
python -m codex_session_delete watch-disable

# Re-enable watcher
python -m codex_session_delete watch-enable
```

## Core Features

### 1. Plugin Unlock in API Key Mode

When using API Key authentication, Codex App normally disables plugin access. Codex++ unlocks this functionality.

**How it works:**
- Injects `renderer-inject.js` via CDP
- Patches frontend to enable plugin UI
- Allows force-installation of special plugins

### 2. Session Deletion

Codex natively only allows archiving. Codex++ adds true deletion with undo support.

**Features:**
- Delete button appears on hover in session list
- Confirmation dialog before deletion
- Undo capability via local backup
- SQLite database cleanup

**Data locations:**

```bash
# Main Codex database
~/.codex/state_5.sqlite

# Deletion backups
~/.codex-session-delete/backups/
```

### 3. Markdown Export

Export conversations with local rollout data and timestamps.

**Access:**
- Click `Codex++` menu → Export conversation
- Exports current session to timestamped `.md` file

### 4. Provider Sync

Syncs session metadata when switching model providers to prevent conversation loss.

**Enable in settings:**
1. Click `Codex++` menu
2. Open settings panel
3. Enable "Provider 同步" (Provider Sync)
4. Restart Codex++

**What it syncs:**
- Rollout files
- SQLite thread records
- Project path cache

**Backup location:**

```bash
~/.codex/backups_state/provider-sync/
```

### 5. Conversation Timeline

Shows a right-sidebar timeline of user questions with timestamps and summaries.

**Usage:**
- Automatically appears in conversation view
- Hover for message summary
- Click to jump to message

## Configuration

### Settings Panel

Access via `Codex++` menu in the top menu bar.

**Available settings:**
- Enable/disable Provider Sync
- Configure auto-launch behavior
- View backend status (green/red indicator)
- Check version and updates

### Environment Variables

```bash
# Set proxy for GitHub resource loading
export HTTP_PROXY="http://127.0.0.1:7897"
export HTTPS_PROXY="http://127.0.0.1:7897"

# Launch with proxy
python -m codex_session_delete launch
```

On Windows PowerShell:

```powershell
$env:HTTP_PROXY="http://127.0.0.1:7897"
$env:HTTPS_PROXY="http://127.0.0.1:7897"
python -m codex_session_delete launch
```

### Programmatic Launch

```python
from codex_session_delete.launcher import launch_codex_with_cdp

# Launch with custom configuration
launch_codex_with_cdp(
    app_dir="C:/Program Files/WindowsApps/OpenAI.Codex_1.2024.xxx/app",
    debug_port=9229,
    helper_port=57321,
    user_data_dir=None  # Uses default Codex user data
)
```

## Project Structure

```
codex_session_delete/
  cli.py                 # CLI entry point
  launcher.py            # Launch Codex with CDP injection
  cdp.py                 # CDP communication and bridge
  helper_server.py       # Local helper HTTP server
  storage_adapter.py     # SQLite deletion/undo operations
  provider_sync.py       # Provider metadata sync
  settings_store.py      # Settings persistence
  windows_installer.py   # Windows shortcuts and uninstaller
  macos_installer.py     # macOS app bundle generation
  watcher.py             # Windows auto-watcher (optional)
  inject/
    renderer-inject.js   # Frontend injection script
tests/                   # Test suite
```

## Common Patterns

### Custom Installation Path

```bash
# When Codex is installed in non-standard location
python -m codex_session_delete launch \
  --app-dir "/custom/path/to/Codex/app"
```

### Proxy Configuration for GitHub Resources

```bash
# Auto-detection (tries common ports: 7890, 7897, 1080, 10809, 10908)
python -m codex_session_delete launch

# Manual proxy specification
export HTTP_PROXY="http://127.0.0.1:7897"
export HTTPS_PROXY="http://127.0.0.1:7897"
python -m codex_session_delete launch
```

### Backup and Recovery

```python
from codex_session_delete.storage_adapter import LocalStorageAdapter

adapter = LocalStorageAdapter()

# Delete a session (creates backup)
adapter.delete_session(session_id="abc123")

# Undo deletion (restores from backup)
adapter.undo_delete(session_id="abc123")
```

### Provider Sync Automation

```python
from codex_session_delete.provider_sync import ProviderSync

sync = ProviderSync()

# Sync before launch
sync.sync_all_providers()
```

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/BigPizzaV3/CodexPlusPlus.git
cd CodexPlusPlus

# Install with test dependencies
python -m pip install -e .[test]

# Run tests
python -m pytest -q
```

### Testing CDP Injection

```python
import asyncio
from codex_session_delete.cdp import CDPClient

async def test_injection():
    client = CDPClient(port=9229)
    await client.connect()
    
    # Inject custom script
    await client.inject_script("console.log('Test injection');")
    
    await client.close()

asyncio.run(test_injection())
```

## Troubleshooting

### Codex++ Doesn't Launch

**Check logs:**

```bash
# Windows
type %USERPROFILE%\.codex-session-delete\launcher.log

# macOS/Linux
cat ~/.codex-session-delete/launcher.log
```

**Common issues:**
- Codex App not installed
- Port 9229 already in use
- Python environment not accessible
- Codex path changed after update

**Solution:**

```bash
# Find Codex installation
# Windows: typically in %LOCALAPPDATA%\Programs or WindowsApps
# Specify path manually
python -m codex_session_delete launch --app-dir "path/to/Codex/app"
```

### Codex++ Menu Not Appearing

**Verify launch method:**
- Must launch from `Codex++` shortcut, not original Codex
- Check if Codex is running with `--remote-debugging-port=9229`

**Check CDP connection:**

```bash
# Should return JSON if CDP is active
curl http://127.0.0.1:9229/json
```

### Plugin Loading Failed or GitHub Resource Errors

**Cause:** Network cannot reach GitHub directly.

**Solutions:**

```bash
# 1. Use system proxy (auto-detected)
python -m codex_session_delete launch

# 2. Specify proxy manually
export HTTP_PROXY="http://127.0.0.1:7897"
export HTTPS_PROXY="http://127.0.0.1:7897"
python -m codex_session_delete launch

# 3. Check proxy is running
curl --proxy http://127.0.0.1:7897 https://github.com
```

### Sessions Disappear After Provider Switch

**Enable Provider Sync:**
1. Click `Codex++` menu
2. Open settings panel
3. Enable "Provider 同步"
4. Restart Codex++

**Manual sync:**

```bash
python -m codex_session_delete launch  # Syncs on startup if enabled
```

### Port Already in Use

```bash
# Use different ports
python -m codex_session_delete launch \
  --debug-port 9230 \
  --helper-port 57322

# Find what's using port 9229
# Windows
netstat -ano | findstr :9229

# macOS/Linux
lsof -i :9229
```

### Watcher Not Working (Windows)

**Check watcher status:**

```bash
# View watcher log
type %USERPROFILE%\.codex-session-delete\watcher.log

# Reinstall watcher
python -m codex_session_delete watch-remove
python -m codex_session_delete watch-install
```

### SQLite Database Locked

**Cause:** Codex is still running or file is locked.

**Solution:**

```bash
# Close Codex completely
taskkill /F /IM Codex.exe  # Windows
killall Codex              # macOS

# Then retry operation
python -m codex_session_delete launch
```

## Data Locations Reference

```bash
# Codex main database
~/.codex/state_5.sqlite

# Session deletion backups
~/.codex-session-delete/backups/

# Provider sync backups
~/.codex/backups_state/provider-sync/

# Launch logs
~/.codex-session-delete/launcher.log

# Watcher logs (Windows only)
%USERPROFILE%\.codex-session-delete\watcher.log

# Settings
~/.codex-session-delete/settings.json
```

## Security Notes

- Codex++ runs a local HTTP helper server (default port 57321)
- Only accepts connections from `localhost` by default
- Does not expose delete/undo endpoints to prevent accidental triggers
- All operations require CDP bridge authentication
- No modification of original Codex App files
- Backups are stored locally and not transmitted
