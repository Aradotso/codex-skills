---
name: open-computer-use-automation
description: AI-powered computer automation using MCP to control desktop apps, click elements, and interact with the UI on macOS, Linux, and Windows
triggers:
  - automate desktop tasks with computer use
  - control desktop applications programmatically
  - click UI elements using accessibility
  - interact with macOS apps via MCP
  - set up open-computer-use for AI agents
  - use computer use tools in my agent
  - automate GUI interactions across platforms
  - configure open-computer-use MCP server
---

# open-computer-use-automation

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

`open-computer-use` is an open-source Computer Use service wrapped as MCP (Model Context Protocol). It enables AI agents to interact with desktop applications through accessibility APIs on macOS, Linux, and Windows. Inspired by OpenAI's Codex Computer Use, it provides non-intrusive automation using native accessibility features.

The project exposes tools to:
- List running applications
- Get application UI state and elements
- Click elements, buttons, and UI components
- Type text and press keys
- Take screenshots
- Manage app focus and windows

## Installation

### Global Installation

```bash
npm i -g open-computer-use
```

### macOS Permissions

On first run, grant **Accessibility** and **Screen Recording** permissions:

```bash
open-computer-use
```

Follow the system prompts to enable permissions in System Settings.

### MCP Integration

Install into your AI agent:

```bash
# Codex
open-computer-use install-codex-mcp

# Claude Code
open-computer-use install-claude-mcp

# Gemini CLI (project scope)
open-computer-use install-gemini-mcp

# Gemini CLI (user scope)
open-computer-use install-gemini-mcp --scope user

# opencode
open-computer-use install-opencode-mcp
```

### Manual MCP Configuration

Add to your MCP client config (e.g., `~/.codex/config.toml`, `~/.claude.json`):

```json
{
  "mcpServers": {
    "open-computer-use": {
      "command": "open-computer-use",
      "args": ["mcp"]
    }
  }
}
```

### Skill Installation

```bash
# Install for Codex
npx skills add iFurySt/open-codex-computer-use -g -a codex --skill open-computer-use -y

# Install for Claude Code
npx skills add iFurySt/open-codex-computer-use -g -a claude-code --skill open-computer-use -y

# Update existing skill
npx skills update open-computer-use -g -y

# List installed skills
npx skills ls -g -a codex | rg 'open-computer-use'
```

## Core Commands

### CLI Usage

```bash
# Check permissions and system readiness
open-computer-use doctor

# Call a single tool (returns MCP JSON)
open-computer-use call list_apps

# Call with arguments
open-computer-use call get_app_state --args '{"app":"TextEdit"}'

# Run a sequence of operations (maintains element_index state)
open-computer-use call --calls '[
  {"tool":"get_app_state","args":{"app":"TextEdit"}},
  {"tool":"press_key","args":{"app":"TextEdit","key":"Return"}}
]'

# Run sequence from file with custom sleep between operations
open-computer-use call --calls-file sequence.json --sleep 0.5

# Show help
open-computer-use -h
```

### Codex Plugin Installation

For Codex App (macOS):

```bash
open-computer-use install-codex-plugin
```

## MCP Tools Reference

### list_apps

List all running applications.

**Arguments:** None

**Returns:** Array of app names

```json
{
  "apps": ["Safari", "TextEdit", "Terminal"]
}
```

### get_app_state

Get the UI element tree for an application.

**Arguments:**
- `app` (string, required): Application name
- `include_screenshot` (boolean, optional): Include base64 screenshot

**Returns:** UI hierarchy with element metadata

```json
{
  "app": "TextEdit",
  "elements": [
    {
      "element_index": 0,
      "role": "AXWindow",
      "title": "Untitled",
      "children": [...]
    }
  ],
  "screenshot": "data:image/png;base64,..."
}
```

### click_element

Click a UI element by index.

**Arguments:**
- `app` (string, required): Application name
- `element_index` (number, required): Element index from `get_app_state`
- `click_type` (string, optional): "single" (default) or "double"

**Returns:** Success confirmation

```json
{
  "success": true,
  "element_index": 5
}
```

### type_text

Type text into the focused field.

**Arguments:**
- `app` (string, required): Application name
- `text` (string, required): Text to type

**Returns:** Success confirmation

### press_key

Press a keyboard key or key combination.

**Arguments:**
- `app` (string, required): Application name
- `key` (string, required): Key name (e.g., "Return", "Tab", "Command+S")

**Supported keys:** Return, Tab, Space, Delete, Escape, Arrow keys, Command+[key], etc.

### take_screenshot

Capture the current screen.

**Arguments:**
- `app` (string, optional): Application name to focus

**Returns:** Base64-encoded PNG

### activate_app

Bring an application to the foreground.

**Arguments:**
- `app` (string, required): Application name

## Usage Patterns

### Basic App Interaction

```typescript
// From an MCP client or AI agent

// 1. List running apps
const apps = await call_tool("list_apps");

// 2. Get app UI state
const state = await call_tool("get_app_state", {
  app: "TextEdit",
  include_screenshot: true
});

// 3. Find and click a button
// (element_index 3 might be a "Save" button from state.elements)
await call_tool("click_element", {
  app: "TextEdit",
  element_index: 3
});

// 4. Type text
await call_tool("type_text", {
  app: "TextEdit",
  text: "Hello, world!"
});

// 5. Save with keyboard shortcut
await call_tool("press_key", {
  app: "TextEdit",
  key: "Command+S"
});
```

### Sequence Execution

Create a JSON sequence file `automation.json`:

```json
[
  {
    "tool": "activate_app",
    "args": {"app": "TextEdit"}
  },
  {
    "tool": "get_app_state",
    "args": {"app": "TextEdit"}
  },
  {
    "tool": "type_text",
    "args": {
      "app": "TextEdit",
      "text": "This is automated text."
    }
  },
  {
    "tool": "press_key",
    "args": {
      "app": "TextEdit",
      "key": "Return"
    }
  },
  {
    "tool": "take_screenshot",
    "args": {"app": "TextEdit"}
  }
]
```

Run it:

```bash
open-computer-use call --calls-file automation.json --sleep 1
```

### Finding Elements

When you call `get_app_state`, inspect the returned elements to find the one you need:

```json
{
  "elements": [
    {
      "element_index": 0,
      "role": "AXWindow",
      "title": "Document",
      "children": [
        {
          "element_index": 1,
          "role": "AXButton",
          "title": "Close",
          "enabled": true
        },
        {
          "element_index": 2,
          "role": "AXTextArea",
          "value": "Current text content"
        }
      ]
    }
  ]
}
```

Use `element_index` from this tree when calling `click_element`.

### Cross-Platform Considerations

- **macOS**: Requires Accessibility and Screen Recording permissions
- **Linux**: Uses AT-SPI (accessibility toolkit)
- **Windows**: Uses UI Automation API

All platforms use the same MCP interface, but element roles and properties may differ slightly.

## Configuration

### Environment Variables

No environment variables required for basic operation. Permissions are handled at the OS level.

### Custom Sleep Between Operations

Default sleep is 1 second. Customize with `--sleep`:

```bash
open-computer-use call --calls-file seq.json --sleep 0.5
```

### MCP Server Args

When configuring MCP manually, you can pass custom args:

```json
{
  "mcpServers": {
    "open-computer-use": {
      "command": "open-computer-use",
      "args": ["mcp"],
      "env": {}
    }
  }
}
```

## Troubleshooting

### Permission Denied (macOS)

**Symptom:** Cannot access UI elements or take screenshots.

**Solution:**
1. Run `open-computer-use doctor` to check permissions
2. Grant **Accessibility** permission in System Settings → Privacy & Security
3. Grant **Screen Recording** permission
4. Restart the terminal or agent

### App Not Found

**Symptom:** `list_apps` doesn't show the target application.

**Solution:**
- Ensure the app is running
- Check exact app name (case-sensitive): `open-computer-use call list_apps`
- Some apps use different process names (e.g., "Google Chrome" vs "Chrome")

### Element Index Invalid

**Symptom:** `click_element` fails with invalid index.

**Solution:**
- Refresh app state with `get_app_state` before clicking
- Element indices can change when UI updates
- Use sequences to maintain state across operations

### MCP Server Not Starting

**Symptom:** Agent can't connect to `open-computer-use`.

**Solution:**
```bash
# Verify installation
which open-computer-use

# Test manual MCP mode
open-computer-use mcp

# Reinstall globally
npm i -g open-computer-use

# Check agent config file syntax
cat ~/.codex/config.toml  # or relevant config
```

### Linux: AT-SPI Not Available

**Symptom:** Tools fail on Linux with accessibility errors.

**Solution:**
```bash
# Install AT-SPI dependencies (Ubuntu/Debian)
sudo apt-get install at-spi2-core

# Enable accessibility
gsettings set org.gnome.desktop.interface toolkit-accessibility true
```

## Advanced Usage

### Programmatic Integration (TypeScript)

If building a custom MCP client or agent:

```typescript
import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

async function automateApp(appName: string) {
  // Get app state
  const { stdout } = await execAsync(
    `open-computer-use call get_app_state --args '{"app":"${appName}"}'`
  );
  
  const state = JSON.parse(stdout);
  
  // Find button with specific title
  const button = state.elements
    .flatMap(e => e.children || [])
    .find(e => e.role === 'AXButton' && e.title === 'Submit');
  
  if (button) {
    // Click it
    await execAsync(
      `open-computer-use call click_element --args '{"app":"${appName}","element_index":${button.element_index}}'`
    );
  }
}

await automateApp('Safari');
```

### Custom Skill Integration

When writing agent prompts or skills that use `open-computer-use`:

```markdown
To interact with desktop apps:
1. Always list apps first to verify the target is running
2. Get app state to find element indices
3. Use element_index from state when clicking
4. Add small delays between operations (1s default)
5. Take screenshots to verify results

Example workflow:
- list_apps → verify "Safari" is running
- get_app_state(app="Safari") → find address bar element_index
- click_element(element_index=X) → focus address bar
- type_text(text="https://example.com") → enter URL
- press_key(key="Return") → navigate
```

## Related Tools

- **Cursor Motion**: Separate macOS app for smooth cursor animations (download from releases page)
- **open-browser-use**: Companion project for browser-specific automation

## Resources

- [GitHub Repository](https://github.com/iFurySt/open-codex-computer-use)
- [Releases](https://github.com/iFurySt/open-codex-computer-use/releases)
- [Demo Videos](https://youtu.be/2s6aVpGiwaQ)
