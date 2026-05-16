---
name: codexbar-menubar-ai-usage-tracker
description: Monitor AI coding assistant usage limits and token resets in the macOS menu bar with CodexBar
triggers:
  - show me my AI coding limits
  - track my Codex usage in the menu bar
  - monitor Claude and Cursor token limits
  - install CodexBar for AI usage tracking
  - configure CodexBar providers
  - check my AI assistant quotas
  - set up menu bar AI usage monitor
  - view my OpenAI and Anthropic limits
---

# CodexBar Menu Bar AI Usage Tracker

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

CodexBar is a macOS menu bar application that displays real-time usage statistics for AI coding assistants including OpenAI Codex, Claude, Cursor, Gemini, Copilot, and 25+ other providers. It shows token limits, credit balances, reset countdowns, and provider status without requiring separate logins. Built with Swift for macOS 14+, it includes both a GUI app and CLI for scripting.

## Installation

### Homebrew (Recommended)

```bash
brew install --cask steipete/tap/codexbar
```

### GitHub Releases

Download the latest `.dmg` from:
```
https://github.com/steipete/CodexBar/releases/latest
```

### CLI Only (macOS/Linux)

```bash
# macOS/Linux CLI via Homebrew
brew install steipete/tap/codexbar

# Or download tarballs from releases:
# CodexBarCLI-v<version>-macos-arm64.tar.gz
# CodexBarCLI-v<version>-linux-x86_64.tar.gz
```

### First Launch

1. Open CodexBar from Applications
2. Go to Settings → Providers
3. Enable the providers you use (Codex, Claude, Cursor, etc.)
4. Authenticate via the supported methods for each provider

## Requirements

- **macOS**: 14+ (Sonoma) for GUI app
- **Linux**: CLI only
- **Permissions** (optional, per provider):
  - Full Disk Access: for Safari cookie access
  - Keychain: for browser cookie decryption and OAuth tokens

## Configuration

### Using the GUI

Settings → Providers shows all available providers with toggles. Each provider has specific auth requirements listed in its documentation.

### Using the CLI

Configuration lives in `~/.codexbar/config.json`:

```bash
# List all providers
codexbar config providers

# Enable a provider
codexbar config enable --provider grok

# Disable a provider
codexbar config disable --provider cursor

# Set API key from environment variable
printf '%s' "$OPENROUTER_API_KEY" | codexbar config set-api-key --provider openrouter --stdin

# Set API key directly (not recommended for scripts)
codexbar config set-api-key --provider deepseek --api-key "sk-xxxxx"

# Set API key without enabling
printf '%s' "$VENICE_API_KEY" | codexbar config set-api-key --provider venice --stdin --no-enable
```

The `set-api-key` command:
- Trims input whitespace
- Sets restrictive file permissions on config
- Enables the provider by default (use `--no-enable` to prevent)

## Key Commands

### CLI Usage

```bash
# Show usage for a specific provider
codexbar usage --provider codex

# Check cost/usage for last 30 days (local scan)
codexbar cost --provider codex
codexbar cost --provider claude
codexbar cost --provider both

# Refresh all enabled providers
codexbar refresh

# Show app version
codexbar version

# Configuration commands
codexbar config providers
codexbar config enable --provider <name>
codexbar config disable --provider <name>
codexbar config set-api-key --provider <name> --stdin
```

### Exit Codes

- `0`: Success
- `1`: General error
- `2`: Authentication/configuration error
- `3`: Network/API error

## Provider Configuration Examples

### OpenAI Codex

**Authentication**: OAuth API or local Codex CLI

```bash
# Enable Codex provider
codexbar config enable --provider codex

# Optional: Add OpenAI web dashboard cookies for extras
# (code review remaining, usage breakdown, credits history)
# Configure via Settings → Providers → Codex → OpenAI cookies
```

### Claude (Anthropic)

**Authentication**: OAuth API, browser cookies, or CLI PTY fallback

```bash
# Enable Claude
codexbar config enable --provider claude

# Uses OAuth by default
# Falls back to browser cookies or Claude CLI if needed
```

### Cursor

**Authentication**: Browser session cookies

```bash
codexbar config enable --provider cursor

# Requires browser cookies from cursor.sh
# Shows plan, usage, and billing resets
```

### OpenRouter

**Authentication**: API token

```bash
# Set API key from environment
printf '%s' "$OPENROUTER_API_KEY" | codexbar config set-api-key --provider openrouter --stdin

# Or configure in GUI: Settings → Providers → OpenRouter
```

### DeepSeek

**Authentication**: API key

```bash
# Set API key securely
printf '%s' "$DEEPSEEK_API_KEY" | codexbar config set-api-key --provider deepseek --stdin
```

### Gemini

**Authentication**: OAuth via Gemini CLI credentials

```bash
codexbar config enable --provider gemini

# Uses gcloud OAuth, no browser cookies required
```

### GitHub Copilot

**Authentication**: GitHub device flow

```bash
codexbar config enable --provider copilot

# Uses GitHub device flow + Copilot internal usage API
```

## Swift Integration

CodexBar is built with Swift. To integrate provider parsing or usage tracking:

### Reading Configuration

```swift
import Foundation

struct CodexBarConfig: Codable {
    var providers: [String: ProviderConfig]
}

struct ProviderConfig: Codable {
    var enabled: Bool
    var apiKey: String?
}

func loadConfig() throws -> CodexBarConfig {
    let configPath = FileManager.default.homeDirectoryForCurrentUser
        .appendingPathComponent(".codexbar/config.json")
    let data = try Data(contentsOf: configPath)
    return try JSONDecoder().decode(CodexBarConfig.self, from: data)
}

// Usage
do {
    let config = try loadConfig()
    if config.providers["codex"]?.enabled == true {
        print("Codex provider is enabled")
    }
} catch {
    print("Failed to load config: \(error)")
}
```

### Calling CLI from Swift

```swift
import Foundation

func runCodexBarCLI(args: [String]) throws -> String {
    let process = Process()
    process.executableURL = URL(fileURLWithPath: "/opt/homebrew/bin/codexbar")
    process.arguments = args
    
    let pipe = Pipe()
    process.standardOutput = pipe
    
    try process.run()
    process.waitUntilExit()
    
    let data = pipe.fileHandleForReading.readDataToEndOfFile()
    return String(data: data, encoding: .utf8) ?? ""
}

// Get usage for a provider
do {
    let output = try runCodexBarCLI(args: ["usage", "--provider", "codex"])
    print(output)
} catch {
    print("CLI error: \(error)")
}
```

## Common Patterns

### Scripting Cost Tracking

```bash
#!/bin/bash
# Track AI coding costs daily

LOG_FILE="$HOME/ai-usage-log.txt"
DATE=$(date +%Y-%m-%d)

echo "=== $DATE ===" >> "$LOG_FILE"
codexbar cost --provider both >> "$LOG_FILE" 2>&1

# Alert if cost exceeds threshold
COST=$(codexbar cost --provider codex | grep -o '\$[0-9.]*' | head -1 | tr -d '$')
if (( $(echo "$COST > 50.0" | bc -l) )); then
    echo "Warning: Codex cost ($COST) exceeds $50" | mail -s "AI Cost Alert" user@example.com
fi
```

### Automated Provider Enablement

```bash
#!/bin/bash
# Enable all providers from environment

PROVIDERS=(
    "codex:$OPENAI_API_KEY"
    "openrouter:$OPENROUTER_API_KEY"
    "deepseek:$DEEPSEEK_API_KEY"
    "venice:$VENICE_API_KEY"
)

for entry in "${PROVIDERS[@]}"; do
    IFS=: read -r provider key <<< "$entry"
    if [ -n "$key" ]; then
        printf '%s' "$key" | codexbar config set-api-key --provider "$provider" --stdin
        echo "Enabled $provider"
    fi
done
```

### Menu Bar Icon Modes

CodexBar supports two display modes:

**Individual Icons** (default):
- One menu bar icon per enabled provider
- Each shows provider-specific usage bar

**Merge Icons Mode**:
- Single menu bar icon with all providers
- Click to switch between providers
- Enable in Settings → Display → Merge Icons

### Refresh Cadence

```bash
# Set refresh interval via GUI: Settings → Refresh
# Options: manual, 1m, 2m, 5m, 15m

# Or edit ~/.codexbar/config.json:
{
  "refreshInterval": 300  // 5 minutes in seconds
}
```

## Troubleshooting

### "Full Disk Access required" for Safari cookies

1. Open **System Settings** → **Privacy & Security** → **Full Disk Access**
2. Add `CodexBar.app`
3. Restart CodexBar

Alternative: Use Chrome/Brave/Arc cookies or API keys instead.

### Keychain prompts for browser cookies

1. Open **Keychain Access.app**
2. Search for "Chrome Safe Storage" (or your browser)
3. Double-click → **Access Control** tab
4. Click **+** and add `CodexBar.app`
5. Save and restart CodexBar

### Keychain prompts for Claude OAuth

1. Open **Keychain Access.app**
2. Search for "Claude Code-credentials"
3. Double-click → **Access Control** tab
4. Click **+** and add `CodexBar.app`
5. Save and restart CodexBar

### Provider shows "stale" or "error"

```bash
# Check provider status via CLI
codexbar usage --provider <name>

# Force refresh
codexbar refresh

# Check logs (GUI app)
# Console.app → search for "CodexBar"

# Verify authentication
codexbar config providers
```

### CLI not found after Homebrew install

```bash
# Ensure Homebrew bin is in PATH
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify installation
which codexbar
codexbar version
```

### "Permission denied" on config file

```bash
# Fix permissions
chmod 600 ~/.codexbar/config.json
```

### Provider authentication issues

**Codex/OpenAI**:
- Ensure `openai` CLI is installed and authenticated: `openai auth login`
- Or configure API key in Settings

**Claude**:
- Install Claude CLI: `brew install anthropics/claude/claude`
- Authenticate: `claude auth login`

**Cursor**:
- Sign in to cursor.sh in browser
- CodexBar will read session cookies

**Gemini**:
- Install `gcloud` CLI
- Authenticate: `gcloud auth login`

## Advanced Usage

### Local Cost Scanning

CodexBar can scan local JSONL logs for Codex and Claude usage over the last 30 days:

```bash
# Scan Codex local logs
codexbar cost --provider codex

# Scan Claude local logs
codexbar cost --provider claude

# Scan both
codexbar cost --provider both
```

Logs locations:
- **Codex**: `~/Library/Application Support/Code/User/globalStorage/openai.codex/logs/`
- **Claude**: `~/Library/Application Support/Claude/claude_desktop_config.json` (log path)

### Provider Status Polling

CodexBar polls provider status pages and shows incident badges:

- Green: Operational
- Yellow: Degraded performance
- Red: Outage
- Overlay indicator on menu bar icon

Configure in Settings → Status Polling.

### Widgets (macOS)

CodexBar includes WidgetKit widgets for supported providers:

1. Right-click Desktop → Edit Widgets
2. Search "CodexBar"
3. Add provider widgets to desktop or Notification Center

Supported: Codex, Claude, Cursor, Copilot, OpenRouter

### Notifications

Enable quota notifications in Settings:

- Session quota warnings
- Weekly reset notifications
- Optional confetti effect on reset 🎉

## Environment Variables

```bash
# Provider API keys (examples)
export OPENAI_API_KEY="sk-proj-xxxxx"
export ANTHROPIC_API_KEY="sk-ant-xxxxx"
export OPENROUTER_API_KEY="sk-or-xxxxx"
export DEEPSEEK_API_KEY="sk-xxxxx"
export VENICE_API_KEY="xxxxx"
export MOONSHOT_API_KEY="sk-xxxxx"
export ZAI_API_TOKEN="xxxxx"
export WARP_API_TOKEN="xxxxx"

# Set all at once
cat > ~/.codexbar.env << 'EOF'
export OPENROUTER_API_KEY="sk-or-xxxxx"
export DEEPSEEK_API_KEY="sk-xxxxx"
EOF

source ~/.codexbar.env
```

## Resources

- **Documentation**: `docs/` directory in repository
- **Provider details**: `docs/providers.md`
- **CLI reference**: `docs/cli.md`
- **Development guide**: `docs/DEVELOPMENT.md`
- **Architecture**: `docs/architecture.md`
- **Issue tracker**: GitHub Issues with labels (see `docs/ISSUE_LABELING.md`)

## Privacy & Security

- **No password storage**: CodexBar reuses browser sessions, OAuth tokens, and API keys
- **On-device parsing**: Usage data stays local
- **Restrictive permissions**: Config file has `600` permissions
- **Known locations only**: Reads specific config files, not filesystem crawling
- **Open source**: Full audit available at `github.com/steipete/CodexBar`

See privacy discussion: [Issue #12](https://github.com/steipete/CodexBar/issues/12)
