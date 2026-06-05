---
name: codex-windows-fast-patch-skill
description: Guide agents to restore Codex Desktop local patches and feature toggles (Computer Use, plugins, Fast Mode) after upgrades on Windows
triggers:
  - "restore Codex Desktop patches after upgrade"
  - "fix Codex Fast Mode not working on Windows"
  - "repair Codex Computer Use missing helper"
  - "enable Codex plugins and marketplace"
  - "fix Codex browser_use or Chrome control disabled"
  - "restore Codex locale and language settings"
  - "patch Codex MSIX package on Windows"
  - "unlock Codex Any App computer control"
---

# Codex Windows Fast Patch Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

This skill guides AI agents to restore local patches and feature toggles in Codex Desktop on Windows after upgrades invalidate them. It handles Fast Mode, Computer Use, plugins, browser control, locale settings, and feature gates.

## What This Project Does

`codex-windows-fast-patch-skill` provides PowerShell workflows and scripts to:

- Re-apply Windows MSIX patches after Codex Desktop upgrades
- Restore Fast Mode (`service_tier=priority`) in both request paths and settings UI
- Keep locale/i18n enabled to prevent language resets
- Register and repair local plugin marketplace configurations
- Unlock in-app browser, browser pane, and Chrome/browser_use disabled by feature gates
- Refresh Windows Computer Use compatibility files
- Unlock "Any App" / "任意应用" in Computer Control when region/org-gated
- Fix Codex mobile/connection page remote control settings stuck on login
- Auto-backup `config.toml` before overwrites
- Auto-update skill from GitHub before each use

**Platform:** Windows only. Relies on MSIX package structure, PowerShell, `Get-AppxPackage`, `makeappx.exe`, `signtool.exe`, Windows environment variables, and Windows Computer Use helper paths.

## Installation

Clone the repository and copy skill files to Codex:

```powershell
$source = (Get-Location).ProviderPath
if (-not (Test-Path -LiteralPath (Join-Path $source 'SKILL.md'))) {
  throw 'Run this command in codex-windows-fast-patch-skill repository root.'
}

$dest = Join-Path $env:USERPROFILE '.codex\skills\codex-windows-fast-patch'
New-Item -ItemType Directory -Force -Path $dest | Out-Null

Copy-Item -Force -LiteralPath (Join-Path $source 'SKILL.md') -Destination $dest
Copy-Item -Recurse -Force -LiteralPath (Join-Path $source 'agents') -Destination $dest
Copy-Item -Recurse -Force -LiteralPath (Join-Path $source 'scripts') -Destination $dest
Copy-Item -Recurse -Force -LiteralPath (Join-Path $source 'references') -Destination $dest
```

Restart Codex Desktop to reload skill metadata.

## Key Scripts and Commands

### 1. Complete Repatch Workflow

Re-applies all patches (Fast Mode, locale, browser gates, marketplace, Computer Use):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\repatch-codex-windows.ps1"
```

**Parameters:**
- `-RegisterMarketplaceOnly`: Only fix marketplace config without MSIX patching
- `-SkipMarketplace`: Skip marketplace registration
- `-SkipComputerUse`: Skip Computer Use file refresh

### 2. Marketplace-Only Repair

Fix plugin marketplace without touching MSIX:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\repatch-codex-windows.ps1" -RegisterMarketplaceOnly
```

### 3. Computer Use Helper Installation

Install or verify Computer Use compatibility files:

```powershell
# Install/repair
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\install-computer-use-local.ps1"

# Verify only (no changes)
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\install-computer-use-local.ps1" -VerifyOnly
```

### 4. MSIX/ASAR Patching

Core patching logic for Fast Mode, locale, and browser gates:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\patch_codex_fast_mode_windows_msix.ps1"
```

This script:
1. Locates Codex MSIX package via `Get-AppxPackage`
2. Extracts MSIX to temp directory
3. Unpacks `resources/app.asar` using `npx asar`
4. Patches JavaScript files for Fast Mode UI, request paths, locale, and browser gates
5. Repacks ASAR, updates MSIX manifest version
6. Creates new MSIX package with `makeappx.exe`
7. Signs with development certificate via `signtool.exe`
8. Uninstalls old package, installs patched version

### 5. Backup Management

Create backup of Codex config, skills, MCP, and marketplaces:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\manage-codex-backups.ps1" -Action Backup
```

List existing backups:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\manage-codex-backups.ps1" -Action List
```

Restore from backup:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\manage-codex-backups.ps1" -Action Restore -BackupPath "C:\path\to\backup.zip"
```

**Backup options:**
- `-IncludeDependencyDirs`: Include `node_modules`, etc. (may be large)
- `-IncludePluginCache`: Include plugin cache directories
- `-IncludeTmpBundledMarketplaces`: Include `.tmp\bundled-marketplaces`

### 6. Skill Auto-Update

Update skill from GitHub before use (called automatically by workflow):

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\update-skill-from-github.ps1"
```

## Configuration

### Config.toml Backup

Before modifying `~/.codex/config.toml`, scripts automatically create timestamped backup in `~/.codex/backups/config/`.

### Marketplace Configuration

Local plugin marketplace registered in `config.toml`:

```toml
[plugin_marketplaces]
local = "file://C:/Users/YourUser/.codex/.agents/plugins"
```

Marketplace manifest structure:

```
~/.codex/.agents/plugins/
├── marketplace.json          # Required root manifest
└── manifests/
    ├── plugin1.json
    └── plugin2.json
```

### Computer Use Paths

Windows Computer Use helper paths in environment variables:

```powershell
$env:COMPUTER_USE_HELPER_PATH = "C:\path\to\computer-use-helper.exe"
```

Or in Codex config:

```toml
[computer_use]
helper_path = "C:\\path\\to\\computer-use-helper.exe"
```

## Usage Patterns

### Pattern 1: Quick Computer Use Fix

User reports: "Computer Use shows missing-helper-path error"

Agent should:

```powershell
# Verify current state
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\install-computer-use-local.ps1" -VerifyOnly

# If verification fails, install/repair
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\install-computer-use-local.ps1"
```

Restart Codex Desktop after fix.

### Pattern 2: Marketplace Corruption

User reports: "`codex plugin list` throws marketplace manifest error"

Agent should:

```powershell
# Repair marketplace only (safe to run in current Codex session)
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\repatch-codex-windows.ps1" -RegisterMarketplaceOnly
```

Check if `~/.codex/.agents/plugins/marketplace.json` exists and is valid JSON.

### Pattern 3: Fast Mode Not Working

User reports: "Fast Mode toggle missing or requests don't include service_tier=priority"

Agent should use **external agent or PowerShell session** (not current Codex Desktop):

```powershell
# Run full repatch (will stop and reinstall Codex)
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\repatch-codex-windows.ps1"
```

After patching, verify in Codex Desktop:
1. Check Fast Mode toggle appears in settings
2. Capture network request to `/v1/responses` and confirm `service_tier=priority` parameter

### Pattern 4: Language Reset to English

User reports: "Codex resets to English after restart despite language setting"

Agent should:

```powershell
# Repatch includes locale/i18n fix
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\repatch-codex-windows.ps1"
```

Patch log should show: `locale i18n patch result: patched` or `already-patched`

### Pattern 5: Browser Control Disabled

User reports: "Chrome browser_use grayed out or browser pane missing"

Agent should:

```powershell
# Repatch includes browser gate unlocking
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\repatch-codex-windows.ps1"
```

After restart, check Codex Desktop logs for:
```
browser_use_availability_resolved: available=true, reason=local-patched
```

Verify Chrome plugin:
```powershell
codex plugin list
# Should show: chrome@openai-bundled - installed, enabled
```

Check native messaging host manifest exists at path referenced in registry or manifest file.

### Pattern 6: Pre-Upgrade Backup

Before major Codex upgrade:

```powershell
# Create full backup including dependencies
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\manage-codex-backups.ps1" -Action Backup -IncludeDependencyDirs
```

After upgrade issues, restore:

```powershell
# List backups to find pre-upgrade timestamp
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\manage-codex-backups.ps1" -Action List

# Restore
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\manage-codex-backups.ps1" -Action Restore -BackupPath "C:\path\to\codex-backup-20260520-143022.zip"
```

## Verification Examples

### Verify Fast Mode Patch

After patching, capture network traffic in Codex Desktop:

```javascript
// In browser DevTools or network capture
// Look for POST to /v1/responses or similar
// Request body should contain:
{
  "service_tier": "priority",
  // ... other params
}
```

Or check patch log output:

```
fast-mode UI patch result: patched
fast-mode request patch result: patched
cable-verification: service_tier=priority detected in request
```

### Verify Computer Use

```powershell
# Check helper path in environment
$env:COMPUTER_USE_HELPER_PATH

# Or check Codex logs for
# computer_use_helper_path_resolved: C:\path\to\helper.exe

# Verify file exists
Test-Path $env:COMPUTER_USE_HELPER_PATH
```

### Verify Browser Control

```powershell
# Check plugin
codex plugin list | Select-String "chrome"
# Expected: chrome@openai-bundled - installed, enabled

# Check native messaging host manifest
# Windows: Check registry key or manifest file referenced by Codex
# Should point to existing chrome-native-host.json
```

Real smoke test:

```javascript
// In Codex Desktop, trigger browser control
// Should successfully read tab title like "Example Domain"
```

### Verify Marketplace

```powershell
# Check marketplace.json exists
Test-Path "$env:USERPROFILE\.codex\.agents\plugins\marketplace.json"

# List plugins
codex plugin list

# Check config.toml
Get-Content "$env:USERPROFILE\.codex\config.toml" | Select-String "plugin_marketplaces"
# Should show: [plugin_marketplaces]
#              local = "file://C:/Users/..."
```

## Troubleshooting

### Issue: "makeappx.exe not found"

Install Windows SDK or locate makeappx:

```powershell
# Search Windows SDK paths
Get-ChildItem -Recurse -Path "C:\Program Files (x86)\Windows Kits" -Filter "makeappx.exe" -ErrorAction SilentlyContinue

# Add to PATH or update script with full path
```

### Issue: "Certificate not trusted"

Create and trust development certificate:

```powershell
# Create certificate
$cert = New-SelfSignedCertificate -Type CodeSigningCert -Subject "CN=Codex Dev" -CertStoreLocation "Cert:\CurrentUser\My"

# Export and import to Trusted Root
Export-Certificate -Cert $cert -FilePath "codex-dev.cer"
Import-Certificate -FilePath "codex-dev.cer" -CertStoreLocation "Cert:\LocalMachine\Root"
```

### Issue: "ASAR unpack failed"

Ensure `npx` and `asar` package available:

```powershell
# Check Node.js installed
node --version

# Check asar
npx asar --version

# If missing, install
npm install -g asar
```

### Issue: "Codex won't start after patch"

Restore from backup:

```powershell
# Find backup
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\manage-codex-backups.ps1" -Action List

# Restore config only
$backupPath = "C:\path\to\backup.zip"
Expand-Archive -Path $backupPath -DestinationPath "$env:TEMP\codex-restore"
Copy-Item "$env:TEMP\codex-restore\config.toml" -Destination "$env:USERPROFILE\.codex\config.toml"
```

Or reinstall original Codex MSIX from Windows Store.

### Issue: "Fast Mode still not working after patch"

1. Verify patch log shows `patched` not `already-patched` (confirms changes were made)
2. Completely restart Codex Desktop (kill all processes)
3. If using CPA upstream, ensure CPA override rule forces `service_tier=priority` for Codex model
4. Capture network request and verify `service_tier=priority` in request body
5. Check Codex subscription status (Fast Mode requires valid subscription)

### Issue: "Skill updates fail from GitHub"

Skill auto-updates require network access to `https://github.com`. If behind firewall or VPN:

```powershell
# Manually update skill
cd $env:USERPROFILE\.codex\skills\codex-windows-fast-patch
git pull origin main

# Or re-run installation steps from fresh clone
```

Auto-update failures won't block skill usage; agent will continue with current local version.

## CPA Upstream Configuration

If Codex uses CPA as upstream proxy, local `service_tier=priority` patch alone is insufficient. Configure CPA override rule:

- **Model**: The model name handling Codex requests (e.g., `gpt-4-0125-preview`)
- **Parameter**: `service_tier`
- **Type**: String
- **Value**: `priority`

This ensures upstream processes requests via Fast/Priority path.

## When to Use This Skill

### Safe for Current Codex Session

- Computer Use helper missing or invalid path
- Plugin marketplace config corrupted
- Marketplace manifest structure broken
- Verifying patch status without changes

Run these from within current Codex Desktop session.

### Requires External Agent

- Fast Mode toggle missing or requests lack `service_tier=priority`
- Plugin install buttons grayed out
- Computer Control "Any App" disabled
- Browser/Chrome/browser_use disabled by feature gates
- Language resets to English after restart
- Codex mobile/connection page stuck on login
- Goal entry point missing

These require MSIX/ASAR modification. Run from **external PowerShell or different agent** to avoid current Codex session stopping itself mid-operation.

## Real-World Example Workflow

User says: "Use codex-windows-fast-patch skill to check and fix Codex Desktop Fast Mode, locale, Chrome browser_use, plugin marketplace, and Computer Use on this Windows machine."

Agent should:

1. **Check if skill is up to date:**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\update-skill-from-github.ps1"
```

2. **Verify current issues:**

```powershell
# Check Computer Use
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\install-computer-use-local.ps1" -VerifyOnly

# Check marketplace
Test-Path "$env:USERPROFILE\.codex\.agents\plugins\marketplace.json"
codex plugin list
```

3. **Run full repatch (warn user Codex will restart):**

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File "$env:USERPROFILE\.codex\skills\codex-windows-fast-patch\scripts\repatch-codex-windows.ps1"
```

4. **After Codex restarts, verify results:**

```powershell
# Check patch log contains:
# - fast-mode UI patch result: patched
# - fast-mode request patch result: patched
# - locale i18n patch result: patched
# - browser-use gate patch result: patched

# Verify Fast Mode request
# Capture /v1/responses request and confirm service_tier=priority

# Verify browser availability
# Check Codex logs for browser_use_availability_resolved: available=true, reason=local-patched

# Verify Chrome plugin
codex plugin list | Select-String "chrome"
# Expected: chrome@openai-bundled - installed, enabled

# Verify native messaging host
# Check manifest path exists and points to valid chrome-native-host.json

# Smoke test browser control
# Try to read controlled tab title, expect "Example Domain" or similar
```

5. **If issues persist, check upstream CPA config if applicable.**

---

**Note:** These scripts are reference implementations and operation templates, not one-size-fits-all solutions. Before execution, agent should read `SKILL.md`, inspect current machine's Codex installation method, MSIX package paths, ASAR contents, signing tools, plugin directories, and Computer Use file status, then decide whether to execute, modify, or only reference the provided steps.
