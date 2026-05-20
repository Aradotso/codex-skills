---
name: codexisland-macos-notch
description: CodexIsland - Display AI usage limits (Claude Code & Codex) in your MacBook notch with Dynamic Island-style UI
triggers:
  - how do I install and use CodexIsland
  - set up CodexIsland to monitor my AI usage
  - troubleshoot CodexIsland authentication issues
  - configure CodexIsland chart styles and refresh intervals
  - understand CodexIsland cost tracking and token counting
  - build CodexIsland from source
  - customize CodexIsland provider visibility settings
  - fix CodexIsland auth required errors
---

# CodexIsland macOS Notch

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

CodexIsland is a native macOS overlay that transforms your MacBook notch into a Dynamic Island-style live activity display for Claude Code and Codex usage limits. It shows 5-hour and weekly usage windows for both providers, estimates dollar spend and token throughput from local session logs, and provides a swipeable Cost screen—all while remaining local-first and credential-free.

## What CodexIsland Does

- **Dual-provider monitoring**: Tracks Claude (5h + 7d) and Codex (5h + 7d) usage limits in one notch overlay
- **Notch-native overlay**: Black pill aligned to the physical notch with squircle corners; falls back to menu-bar pill on non-notched Macs
- **Hover to peek**: Shows 5-hour percentage and reset headline for visible providers
- **Click to expand**: Opens full Usage/Cost panel with provider columns and chart controls
- **Swipeable screens**: Usage screen (live limits) + Cost screen (local log analysis for $ spend & tokens)
- **Five chart styles**: Ring, Bar, Stepped, Numeric, Sparkline
- **Local-first privacy**: Reads existing credentials from Claude Code/Codex; no API keys stored; no telemetry

## Installation

### Homebrew (Recommended)

```bash
brew install --cask ericjypark/tap/codexisland
```

The cask automatically strips the Gatekeeper quarantine attribute.

### Direct Download

1. Download `CodexIsland-X.Y.Z.dmg` from [GitHub Releases](https://github.com/ericjypark/codex-island/releases)
2. Drag `CodexIsland.app` to `/Applications`
3. Remove quarantine attribute (app is unsigned):

```bash
xattr -dr com.apple.quarantine /Applications/CodexIsland.app
```

### Manual Gatekeeper Bypass (No Terminal)

1. Drag app to `/Applications`
2. Try to open (macOS will block it)
3. Open **System Settings → Privacy & Security**
4. Scroll to bottom, find blocked CodexIsland message
5. Click **Open Anyway**, then re-launch

## First Run Authentication

CodexIsland reads existing credentials—no manual API key entry needed.

### Claude Setup

CodexIsland tries these sources in order:

1. `CLAUDE_CODE_OAUTH_TOKEN` environment variable
2. macOS Keychain item `Claude Code-credentials`
3. Refresh token from Anthropic's OAuth endpoint

**Prerequisites**:
```bash
# Run Claude CLI once to populate credentials
claude

# OR open Claude Desktop app
```

If authentication fails, the panel shows `auth required — run claude`.

### Codex Setup

CodexIsland reads `~/.codex/auth.json` created by the Codex CLI.

**Prerequisites**:
```bash
# Sign in to Codex/ChatGPT CLI
codex auth login
```

If the file or token is missing, the panel shows `no codex auth`.

## Using the App

### Basic Interaction

| Action | Result |
|--------|--------|
| Hover notch | Peek at current 5-hour usage |
| Click island | Expand full Usage/Cost panel |
| Swipe horizontally | Switch between Usage and Cost screens |
| Move away | Collapse island |
| Cmd-click panel | Cycle chart styles (Usage: Ring/Bar/Stepped/Numeric/Sparkline; Cost: USD/VALUE/TOKENS/TREND) |
| Click "synced Xs ago" | Force immediate refresh |
| Click gear icon | Open Settings |

### Chart Styles

**Usage Screen**:
- **Ring**: Circular progress indicator
- **Bar**: Horizontal bar chart
- **Stepped**: Stepped area chart
- **Numeric**: Large percentage numbers
- **Sparkline**: Minimal line chart

**Cost Screen**:
- **USD**: Dollar spend (today + month-to-date)
- **VALUE**: Spend vs. subscription value
- **TOKENS**: Total token throughput
- **TREND**: Token usage trend over time

### Token Counting Modes

**All Tokens** (default, matches `ccusage`):
- Counts every token type that crossed the wire
- Includes cache reads/writes

**Billable Only** (matches claude.ai stats):
- Input + output tokens only
- Excludes cache tokens

Toggle in Settings → Token Counting.

## Configuration

### Settings Panel

Access via gear icon in expanded panel. All settings persist to `UserDefaults`.

| Setting | Key | Values | Default |
|---------|-----|--------|---------|
| Chart Style | `MacIsland.chartStyle` | `ring`, `bar`, `stepped`, `numeric`, `spark` | `ring` |
| Cost Style | `MacIsland.costStyle` | `dollar`, `multi`, `tokens`, `spark` | `dollar` |
| Token Counting | `MacIsland.tokenCountMode` | `all`, `billable` | `all` |
| Refresh Interval | `MacIsland.refreshInterval` | `300`, `900`, `1800` (seconds) | `300` (5 min) |
| Low Power Mode | `MacIsland.lowPowerMode` | Boolean | `false` |
| Claude Visible | `MacIsland.claudeVisible` | Boolean | `true` |
| Codex Visible | `MacIsland.codexVisible` | Boolean | `true` |
| Launch at Login | Managed by `SMAppService` | Boolean | `false` |

### Refresh Intervals

Choose from Settings:
- **5 minutes** (default)
- **15 minutes**
- **30 minutes**

**Note**: Sub-5-minute polling is not available due to Anthropic's rate limits on `/api/oauth/usage`.

### Provider Visibility

Hide/show providers in Settings:
- Removes provider logo and column from island
- Keeps latest usage values in memory
- Re-showing does not require re-authentication

## Building from Source

### Requirements

- macOS 13+
- Xcode or Command Line Tools (Swift toolchain)

### Build Steps

```bash
git clone https://github.com/ericjypark/codex-island
cd codex-island
./build.sh
open build/CodexIsland.app
```

**No Xcode project or SwiftPM package**. `build.sh` compiles with `swiftc`, creates universal binary (arm64 + x86_64), and assembles `.app` bundle.

### Verification

Smoke test the build:

```bash
./scripts/verify.sh
```

Launches the binary for 1 second, then kills it if still alive.

### Release Packaging

```bash
npm install --global create-dmg
./release.sh
```

Creates `dist/CodexIsland-X.Y.Z.dmg` with ad-hoc codesigning.

## Code Architecture

### Key Components

```
Sources/
├── App.swift                    # SwiftUI app entry point
├── Cost/                        # Local log cost + token aggregation
├── Model/                       # Data models for usage/cost
├── Theme/                       # UI theming and colors
├── Update/                      # Sparkle auto-update wrapper
├── Usage/
│   └── UsageFetcher.swift      # Network fetcher for provider APIs
├── Views/                       # SwiftUI views for island/panels
└── Window/                      # Custom window management
```

### Network Surface (Privacy)

All network requests are in `Sources/Usage/UsageFetcher.swift`:

- **Claude**: `https://api.anthropic.com/api/oauth/usage`
- **Codex**: `https://chatgpt.com/api/usage`

Tokens are sent only as `Authorization` headers. No proxy server.

### Local Log Reading (Cost Screen)

Cost screen reads local session logs:

**Claude Code**:
- `~/.claude/projects/**/*.jsonl`
- `~/.config/claude/**/*.jsonl`
- `$CLAUDE_CONFIG_DIR/**/*.jsonl` (if set)

**Codex**:
- `~/.codex/sessions/`

All aggregation happens on-device. No log content is uploaded.

## Troubleshooting

### Authentication Issues

**Claude shows "auth required — run claude"**

```bash
# Option 1: Run Claude CLI
claude

# Option 2: Open Claude Desktop app (no command needed)

# Option 3: Set environment variable
export CLAUDE_CODE_OAUTH_TOKEN="your_token_here"
```

**Codex shows "no codex auth"**

```bash
# Sign in to Codex CLI
codex auth login

# Verify auth file exists
ls -la ~/.codex/auth.json
```

### Stale Values After Error

**Expected behavior**: `UsageStore` retains previous good values when a refresh fails (e.g., 429 rate limit). Prevents panel from showing 0% during temporary errors.

**Force refresh**:
- Click "synced Xs ago" in panel header
- Or wait for next scheduled poll (respects refresh interval setting)

### Rate Limiting

If you see persistent authentication errors:

1. Check refresh interval (Settings → Refresh Interval)
2. Increase to 15m or 30m to avoid Anthropic's rate limits
3. Click "synced Xs ago" to manually refresh when needed

### macOS Compatibility

**Non-notched Macs**: Falls back to 200×28 menu-bar pill
**Multiple monitors**: Prefers first display with safe-area insets (partial support)

### Gatekeeper Warnings

CodexIsland is unsigned (free open-source project):

```bash
# Remove quarantine attribute
xattr -dr com.apple.quarantine /Applications/CodexIsland.app

# Verify removal
xattr -l /Applications/CodexIsland.app
```

Or use manual bypass via System Settings (see Installation section).

## Advanced Usage

### Programmatic Access to Settings

Settings are stored in `UserDefaults` with domain `MacIsland`:

```bash
# Read current chart style
defaults read MacIsland chartStyle

# Set refresh interval to 15 minutes
defaults write MacIsland refreshInterval -int 900

# Enable Low Power Mode
defaults write MacIsland lowPowerMode -bool true

# Hide Codex provider
defaults write MacIsland codexVisible -bool false
```

### Auto-Updates (Sparkle)

CodexIsland uses Sparkle for auto-updates:
- Checks on launch + once per day
- EdDSA signature verification (no Apple Developer ID required)
- Toggle in Settings → Auto-Update

Appcast: `https://github.com/ericjypark/codex-island/releases`

### Launch at Login

Managed by `SMAppService.mainApp`:

```bash
# Enable via Settings UI or Terminal
# (No direct command-line control for SMAppService)
```

Access via Settings → Launch at Login toggle.

## Privacy Guarantees

- ✅ No app telemetry
- ✅ No crash reporting
- ✅ No third-party analytics
- ✅ No proxy server
- ✅ Credentials never stored by CodexIsland
- ✅ Tokens leave machine only as `Authorization` headers to official provider APIs
- ✅ Cost screen log aggregation is 100% on-device

## Example Workflow

```bash
# 1. Install
brew install --cask ericjypark/tap/codexisland

# 2. Authenticate Claude
claude

# 3. Authenticate Codex
codex auth login

# 4. Launch app
open /Applications/CodexIsland.app

# 5. Configure settings
# - Hover notch → Click island → Click gear icon
# - Set refresh interval: 15 minutes
# - Set chart style: Bar
# - Enable Launch at Login
# - Enable Low Power Mode (hides steady-state glow)

# 6. Use the island
# - Hover to peek at 5-hour usage
# - Click to expand full panel
# - Swipe right to see Cost screen ($ spend + tokens)
# - Cmd-click to cycle chart styles
# - Click "synced Xs ago" to force refresh
```

## Contributing

Repository: `https://github.com/ericjypark/codex-island`

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/codex-island
cd codex-island

# Build
./build.sh

# Test
./scripts/verify.sh

# Package DMG
./release.sh
```

CI/CD: `.github/workflows/release.yml` builds DMG and updates Homebrew tap on `v*` tags.
