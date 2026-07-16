---
name: codex-dream-skin-theme-injector
description: Theme injection tool for Codex desktop using local CDP, adding custom skins without modifying app binaries
triggers:
  - how do I theme Codex desktop
  - install custom skin for Codex
  - change Codex appearance with Dream Skin
  - inject theme into Codex using CDP
  - customize Codex desktop background
  - apply Dream Skin to Codex
  - setup Codex theming tool
  - troubleshoot Codex Dream Skin
---

# Codex Dream Skin Theme Injector

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

Codex Dream Skin is a **local CDP (Chrome DevTools Protocol) injection tool** that applies custom visual themes to the Codex desktop application without modifying the official installation binaries, `.app` bundle, `app.asar`, or code signature.

**Key capabilities:**
- Inject custom CSS/background images into running Codex instance
- Bind CDP server to `127.0.0.1` only (local security boundary)
- One-click install, apply, restore scripts
- Platform-specific implementations for macOS and Windows
- Interactive UI elements remain native (not just a static overlay)

**Security model:**
- Does NOT modify official installation files
- Does NOT change API keys or base URLs
- CDP bound to localhost only
- Requires Codex to be launched with `--remote-debugging-port` flag

---

## Installation

### macOS (Apple Silicon & Intel)

Located in `macos/` directory.

**Quick install:**

```bash
cd macos
# Double-click or run:
./Install\ Codex\ Dream\ Skin.command
```

**Manual setup:**

```bash
# 1. Clone repo
git clone https://github.com/Fei-Away/Codex-Dream-Skin.git
cd Codex-Dream-Skin/macos

# 2. Make scripts executable
chmod +x scripts/*.sh
chmod +x *.command

# 3. Run installer
./Install\ Codex\ Dream\ Skin.command
```

The installer will:
- Check for Codex.app in `/Applications`
- Install helper scripts to `~/Library/Application Support/Codex-Dream-Skin/`
- Create launch wrappers
- Set up configuration directory

### Windows

Located in `windows/` directory.

**PowerShell setup:**

```powershell
# 1. Navigate to windows directory
cd windows

# 2. Install (sets up scripts and config)
.\scripts\install-dream-skin.ps1

# 3. Start Dream Skin with Codex
.\scripts\start-dream-skin.ps1
```

**What it does:**
- Locates Codex installation (typically in `%LOCALAPPDATA%\Programs\Codex`)
- Sets up helper scripts in `%APPDATA%\Codex-Dream-Skin`
- Configures CDP port (default 9222)
- Creates theme injection scripts

---

## Usage

### Starting Codex with Dream Skin

**macOS:**

```bash
# Use the installed launcher
~/Library/Application\ Support/Codex-Dream-Skin/launch-codex-with-skin.sh

# Or manually:
/Applications/Codex.app/Contents/MacOS/Codex --remote-debugging-port=9222 &
sleep 3
~/Library/Application\ Support/Codex-Dream-Skin/inject-theme.sh
```

**Windows:**

```powershell
# Use start script
.\scripts\start-dream-skin.ps1

# Or manually:
Start-Process "$env:LOCALAPPDATA\Programs\Codex\Codex.exe" -ArgumentList "--remote-debugging-port=9222"
Start-Sleep -Seconds 3
.\scripts\inject-theme.ps1
```

### Switching Themes

**Theme structure:**

```
themes/
  my-theme/
    config.json
    background.jpg
    custom.css
```

**config.json example:**

```json
{
  "name": "My Custom Theme",
  "background": "background.jpg",
  "css": "custom.css",
  "opacity": 0.85,
  "blur": 10
}
```

**Apply theme (macOS):**

```bash
# Edit config to point to your theme
vim ~/Library/Application\ Support/Codex-Dream-Skin/config.json

# Set theme path
{
  "theme": "~/Codex-Dream-Skin/themes/my-theme",
  "cdp_port": 9222
}

# Restart Codex with skin
~/Library/Application\ Support/Codex-Dream-Skin/launch-codex-with-skin.sh
```

**Apply theme (Windows):**

```powershell
# Edit config
notepad $env:APPDATA\Codex-Dream-Skin\config.json

# Set theme path
{
  "theme": "C:\\Users\\YourName\\Codex-Dream-Skin\\themes\\my-theme",
  "cdp_port": 9222
}

# Restart
.\scripts\start-dream-skin.ps1
```

### Custom CSS Injection

**Example custom.css:**

```css
/* Background overlay */
body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('./background.jpg');
  background-size: cover;
  background-position: center;
  opacity: 0.15;
  z-index: -1;
  pointer-events: none;
}

/* Sidebar transparency */
.sidebar {
  background: rgba(255, 255, 255, 0.9) !important;
  backdrop-filter: blur(10px);
}

/* Input area styling */
.input-container {
  background: rgba(248, 249, 250, 0.95) !important;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* Accent color override */
:root {
  --accent-color: #ff6b9d;
  --accent-hover: #ff8fb3;
}
```

### CDP Injection Script (macOS)

**inject-theme.sh snippet:**

```bash
#!/bin/bash

CDP_PORT=${CDP_PORT:-9222}
CONFIG_DIR="$HOME/Library/Application Support/Codex-Dream-Skin"
THEME_DIR=$(jq -r '.theme' "$CONFIG_DIR/config.json")

# Wait for CDP to be available
timeout=10
while [ $timeout -gt 0 ]; do
  if curl -s "http://127.0.0.1:$CDP_PORT/json" >/dev/null; then
    break
  fi
  sleep 1
  ((timeout--))
done

# Get WebSocket URL
WS_URL=$(curl -s "http://127.0.0.1:$CDP_PORT/json" | jq -r '.[0].webSocketDebuggerUrl')

# Inject CSS
CSS_CONTENT=$(cat "$THEME_DIR/custom.css" | jq -Rs .)
wscat -c "$WS_URL" -x "{\"id\":1,\"method\":\"Runtime.evaluate\",\"params\":{\"expression\":\"const style=document.createElement('style');style.textContent=$CSS_CONTENT;document.head.appendChild(style);\"}}"
```

### CDP Injection Script (Windows)

**inject-theme.ps1 snippet:**

```powershell
$CDP_PORT = 9222
$ConfigPath = "$env:APPDATA\Codex-Dream-Skin\config.json"
$Config = Get-Content $ConfigPath | ConvertFrom-Json
$ThemeDir = $Config.theme

# Wait for CDP
$timeout = 10
while ($timeout -gt 0) {
    try {
        $response = Invoke-WebRequest -Uri "http://127.0.0.1:$CDP_PORT/json" -UseBasicParsing
        break
    } catch {
        Start-Sleep -Seconds 1
        $timeout--
    }
}

# Get WebSocket URL
$pages = Invoke-RestMethod -Uri "http://127.0.0.1:$CDP_PORT/json"
$wsUrl = $pages[0].webSocketDebuggerUrl

# Read CSS
$cssContent = Get-Content "$ThemeDir\custom.css" -Raw
$cssEscaped = $cssContent -replace '"', '\"' -replace "`r`n", "\n"

# Inject via WebSocket
$js = "const style=document.createElement('style');style.textContent=`"$cssEscaped`";document.head.appendChild(style);"
$payload = @{
    id = 1
    method = "Runtime.evaluate"
    params = @{ expression = $js }
} | ConvertTo-Json -Compress

# Send via WebSocket (requires WebSocket client)
# Use wscat or custom WebSocket implementation
```

---

## Configuration

### Main Config File

**Location:**
- macOS: `~/Library/Application Support/Codex-Dream-Skin/config.json`
- Windows: `%APPDATA%\Codex-Dream-Skin\config.json`

**Schema:**

```json
{
  "theme": "/path/to/theme/directory",
  "cdp_port": 9222,
  "auto_inject": true,
  "inject_delay": 3,
  "backup_enabled": true
}
```

**Fields:**
- `theme`: Absolute path to theme directory
- `cdp_port`: CDP debugging port (default 9222)
- `auto_inject`: Auto-inject on Codex launch
- `inject_delay`: Seconds to wait before injection
- `backup_enabled`: Keep backup of original state

### Environment Variables

```bash
# Override CDP port
export CDP_PORT=9223

# Custom config location
export CODEX_SKIN_CONFIG="$HOME/.config/codex-skin.json"

# Theme directory
export CODEX_THEME_DIR="$HOME/my-themes/current"
```

---

## Key Commands

### macOS Scripts

Located in `macos/scripts/`:

```bash
# Install Dream Skin
./Install\ Codex\ Dream\ Skin.command

# Launch Codex with theming
~/Library/Application\ Support/Codex-Dream-Skin/launch-codex-with-skin.sh

# Inject theme into running instance
~/Library/Application\ Support/Codex-Dream-Skin/inject-theme.sh

# Restore original appearance
~/Library/Application\ Support/Codex-Dream-Skin/restore-original.sh

# Verify installation
./macos/tests/run-tests.sh

# Uninstall
./macos/scripts/uninstall.sh
```

### Windows Scripts

Located in `windows/scripts/`:

```powershell
# Install
.\scripts\install-dream-skin.ps1

# Start with theme
.\scripts\start-dream-skin.ps1

# Inject to running instance
.\scripts\inject-theme.ps1

# Restore original
.\scripts\restore-original.ps1

# Verify
.\scripts\verify-installation.ps1
```

---

## Common Patterns

### Pattern 1: Quick Theme Switch

**macOS:**

```bash
#!/bin/bash
# switch-theme.sh

THEME_NAME=$1
CONFIG="$HOME/Library/Application Support/Codex-Dream-Skin/config.json"
THEME_BASE="$HOME/Codex-Dream-Skin/themes"

# Update config
jq --arg theme "$THEME_BASE/$THEME_NAME" '.theme = $theme' "$CONFIG" > /tmp/config.json
mv /tmp/config.json "$CONFIG"

# Kill Codex
pkill -f "Codex.*remote-debugging"

# Restart with new theme
~/Library/Application\ Support/Codex-Dream-Skin/launch-codex-with-skin.sh
```

**Usage:**

```bash
./switch-theme.sh pink-custom
./switch-theme.sh hatsune-miku
```

### Pattern 2: Dynamic CSS Injection

**JavaScript injected via CDP:**

```javascript
// Inject with opacity control
const injectTheme = (cssUrl, opacity = 0.85) => {
  const link = document.createElement('link');
  link.rel = 'stylesheet';
  link.href = cssUrl;
  document.head.appendChild(link);
  
  const overlay = document.createElement('div');
  overlay.style = `
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background: url('${cssUrl.replace('.css', '.jpg')}');
    background-size: cover;
    opacity: ${opacity};
    z-index: -1;
    pointer-events: none;
  `;
  document.body.prepend(overlay);
};

injectTheme('http://localhost:8080/theme.css', 0.9);
```

**CDP command:**

```bash
# Evaluate JavaScript via CDP
curl -X POST http://127.0.0.1:9222/json/new
WS_URL=$(curl -s http://127.0.0.1:9222/json | jq -r '.[0].webSocketDebuggerUrl')

echo '{
  "id": 1,
  "method": "Runtime.evaluate",
  "params": {
    "expression": "/* JS code here */"
  }
}' | wscat -c "$WS_URL"
```

### Pattern 3: Theme with Local Asset Server

**Serve theme assets:**

```bash
#!/bin/bash
# serve-theme.sh

THEME_DIR="$1"
PORT=8765

cd "$THEME_DIR"
python3 -m http.server $PORT &
SERVER_PID=$!

echo "Theme server running on http://localhost:$PORT (PID: $SERVER_PID)"
echo $SERVER_PID > /tmp/theme-server.pid
```

**CSS references local server:**

```css
body::before {
  background-image: url('http://localhost:8765/background.jpg');
}

@font-face {
  font-family: 'CustomFont';
  src: url('http://localhost:8765/fonts/custom.woff2');
}
```

### Pattern 4: Automated Launch on System Startup

**macOS LaunchAgent:**

```xml
<!-- ~/Library/LaunchAgents/com.codex.dreamskin.plist -->
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.codex.dreamsin</string>
    <key>ProgramArguments</key>
    <array>
        <string>/Users/YOUR_USER/Library/Application Support/Codex-Dream-Skin/launch-codex-with-skin.sh</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
</dict>
</plist>
```

**Load agent:**

```bash
launchctl load ~/Library/LaunchAgents/com.codex.dreamkin.plist
```

**Windows Task Scheduler:**

```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "powershell.exe" `
  -Argument "-File `"$env:APPDATA\Codex-Dream-Skin\start-dream-skin.ps1`""

$trigger = New-ScheduledTaskTrigger -AtLogOn

Register-ScheduledTask -TaskName "Codex Dream Skin" `
  -Action $action -Trigger $trigger -RunLevel Highest
```

---

## Troubleshooting

### Issue: CDP Port Already in Use

**Symptoms:** `Error: Address already in use` when starting Codex with `--remote-debugging-port`

**Solution:**

```bash
# Find process using port 9222
lsof -i :9222  # macOS/Linux
netstat -ano | findstr :9222  # Windows

# Kill the process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows

# Or use a different port
export CDP_PORT=9223
```

### Issue: Theme Not Applying

**Check CDP availability:**

```bash
curl http://127.0.0.1:9222/json
```

**Expected output:**

```json
[
  {
    "description": "",
    "devtoolsFrontendUrl": "/devtools/inspector.html?ws=127.0.0.1:9222/devtools/page/...",
    "id": "...",
    "title": "Codex",
    "type": "page",
    "webSocketDebuggerUrl": "ws://127.0.0.1:9222/devtools/page/..."
  }
]
```

**If empty or error:**
- Codex not started with `--remote-debugging-port` flag
- Wrong port number
- Firewall blocking localhost

**Manual injection test:**

```bash
# Get WebSocket URL
WS_URL=$(curl -s http://127.0.0.1:9222/json | jq -r '.[0].webSocketDebuggerUrl')

# Test injection
echo '{"id":1,"method":"Runtime.evaluate","params":{"expression":"alert(\"Test\")"}}' | \
  wscat -c "$WS_URL"
```

### Issue: Codex Won't Start

**Check Codex path:**

```bash
# macOS
ls -la /Applications/Codex.app/Contents/MacOS/Codex

# Windows
ls "$env:LOCALAPPDATA\Programs\Codex\Codex.exe"
```

**Try manual launch:**

```bash
# macOS
/Applications/Codex.app/Contents/MacOS/Codex --remote-debugging-port=9222 --verbose

# Windows
& "$env:LOCALAPPDATA\Programs\Codex\Codex.exe" --remote-debugging-port=9222 --verbose
```

**Check logs:**

```bash
# macOS
~/Library/Logs/Codex/
~/Library/Application Support/Codex-Dream-Skin/logs/

# Windows
%APPDATA%\Codex\logs\
%APPDATA%\Codex-Dream-Skin\logs\
```

### Issue: CSS Not Loading

**Verify theme directory structure:**

```bash
# Should contain:
ls -la ~/Codex-Dream-Skin/themes/my-theme/
# config.json
# custom.css
# background.jpg (or other assets)
```

**Check CSS syntax:**

```bash
# Use CSS linter
npx stylelint ~/Codex-Dream-Skin/themes/my-theme/custom.css
```

**Test CSS injection manually:**

```javascript
// Via browser DevTools (connect to localhost:9222)
const style = document.createElement('style');
style.textContent = `
  body { background: red !important; }
`;
document.head.appendChild(style);
```

### Issue: Theme Reverts After Update

**Symptoms:** After Codex updates, theme stops working

**Solution:**

```bash
# Re-verify installation
./macos/tests/run-tests.sh  # macOS
.\windows\scripts\verify-installation.ps1  # Windows

# Re-install if needed
./Install\ Codex\ Dream\ Skin.command  # macOS
.\scripts\install-dream-skin.ps1  # Windows
```

**Prevent auto-updates (optional, not recommended):**

```bash
# macOS: Disable auto-update in Codex settings
# Or block update domain (use at own risk)
echo "0.0.0.0 update.codex.app" | sudo tee -a /etc/hosts
```

### Issue: Security Warning on macOS

**Symptoms:** "Codex Dream Skin.command cannot be opened because it is from an unidentified developer"

**Solution:**

```bash
# Remove quarantine attribute
xattr -d com.apple.quarantine ./Install\ Codex\ Dream\ Skin.command

# Or bypass via System Preferences
# Right-click → Open → Open anyway
```

### Issue: PowerShell Execution Policy (Windows)

**Symptoms:** `cannot be loaded because running scripts is disabled`

**Solution:**

```powershell
# Check current policy
Get-ExecutionPolicy

# Set to RemoteSigned (for current user)
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or bypass for single script
powershell -ExecutionPolicy Bypass -File .\scripts\install-dream-skin.ps1
```

---

## Advanced: Creating Custom Themes

### Minimal Theme Structure

```
my-awesome-theme/
├── config.json
├── custom.css
└── assets/
    └── background.png
```

**config.json:**

```json
{
  "name": "My Awesome Theme",
  "version": "1.0.0",
  "author": "Your Name",
  "background": "assets/background.png",
  "css": "custom.css",
  "settings": {
    "opacity": 0.8,
    "blur": 8,
    "accentColor": "#6366f1"
  }
}
```

**custom.css template:**

```css
/* Main background */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background: url('./assets/background.png') center/cover;
  opacity: 0.8;
  filter: blur(8px);
  z-index: -2;
}

/* Overlay tint */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1), rgba(168, 85, 247, 0.1));
  z-index: -1;
}

/* Glassmorphism panels */
.panel, .sidebar, .chat-container {
  background: rgba(255, 255, 255, 0.7) !important;
  backdrop-filter: blur(12px) saturate(180%);
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

/* Accent color */
:root {
  --accent: #6366f1;
  --accent-hover: #818cf8;
}

button.primary, .link-active {
  background: var(--accent) !important;
}

button.primary:hover {
  background: var(--accent-hover) !important;
}
```

### Testing Theme Locally

```bash
# 1. Create theme directory
mkdir -p ~/Codex-Dream-Skin/themes/test-theme
cd ~/Codex-Dream-Skin/themes/test-theme

# 2. Add files (config.json, custom.css, assets)

# 3. Update main config
jq '.theme = "'$HOME'/Codex-Dream-Skin/themes/test-theme"' \
  ~/Library/Application\ Support/Codex-Dream-Skin/config.json > /tmp/cfg.json
mv /tmp/cfg.json ~/Library/Application\ Support/Codex-Dream-Skin/config.json

# 4. Launch
~/Library/Application\ Support/Codex-Dream-Skin/launch-codex-with-skin.sh
```

---

## API Reference (CDP Injection)

### Core CDP Methods Used

**1. Runtime.evaluate**

```json
{
  "id": 1,
  "method": "Runtime.evaluate",
  "params": {
    "expression": "console.log('Injected!')",
    "returnByValue": true
  }
}
```

**2. Page.addScriptToEvaluateOnNewDocument**

```json
{
  "id": 2,
  "method": "Page.addScriptToEvaluateOnNewDocument",
  "params": {
    "source": "const style = document.createElement('style'); style.textContent = '/* CSS */'; document.head.appendChild(style);"
  }
}
```

**3. CSS.createStyleSheet (if supported)**

```json
{
  "id": 3,
  "method": "CSS.createStyleSheet",
  "params": {
    "frameId": "main-frame-id"
  }
}
```

### Helper Functions

**WebSocket message sender (Node.js):**

```javascript
const WebSocket = require('ws');

async function sendCDP(wsUrl, method, params) {
  const ws = new WebSocket(wsUrl);
  
  return new Promise((resolve, reject) => {
    ws.on('open', () => {
      ws.send(JSON.stringify({
        id: Date.now(),
        method,
        params
      }));
    });
    
    ws.on('message', (data) => {
      const response = JSON.parse(data);
      ws.close();
      resolve(response);
    });
    
    ws.on('error', reject);
  });
}

// Usage
const wsUrl = 'ws://127.0.0.1:9222/devtools/page/...';
await sendCDP(wsUrl, 'Runtime.evaluate', {
  expression: 'document.title'
});
```

---

## Reference Documentation

- Platform paths: `docs/platforms.md`
- Project structure: `docs/PROJECT.md`
- macOS details: `macos/README.md`
- Windows details: `windows/SKILL.md`
- License: `macos/LICENSE` (MIT)
- Notices: `macos/NOTICE.md`

---

**Remember:** This tool modifies the visual appearance only via runtime injection. It does NOT change API configurations, credentials, or application binaries. Always launch Codex from trusted locations and keep CDP bound to `127.0.0.1`.
