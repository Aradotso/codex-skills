---
name: feishu-codex-bridge
description: Run local Codex CLI from Feishu/Lark chat with sessions, attachments, and background service support
triggers:
  - how do I set up the Feishu Codex bridge
  - configure feishu codex bridge for my team
  - run codex commands from Lark chat
  - manage Feishu bot sessions and workspaces
  - troubleshoot feishu-codex-bridge connection
  - set up background service for Lark Codex bot
  - use codex CLI through Feishu messages
  - configure reasoning effort for Feishu Codex bridge
---

# Feishu Codex Bridge

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

A local bridge that connects Feishu/Lark chat to your local Codex CLI. Send messages in Feishu/Lark and the bridge runs `codex exec` on your machine, streaming results back to chat with session persistence, file attachments, and background service support.

## What It Does

- **Chat-to-CLI Bridge**: Converts Feishu/Lark messages into local `codex exec` commands
- **Session Management**: Maps each chat/topic to a persistent Codex session
- **Attachment Support**: Downloads images and files for Codex to process
- **Workspace Management**: Switch between named project directories
- **Background Service**: Runs as a macOS launchd service
- **Access Control**: Allowlist users, chats, and admin commands
- **Lark-CLI Integration**: Gives Codex API access to Lark messages, docs, calendars

## Installation

### Global NPM Install

```bash
npm i -g feishu-codex-bridge
feishu-codex-bridge --version
```

### First-Time Setup

```bash
feishu-codex-bridge start
```

This interactive setup will:
1. Find or install Codex CLI (`@openai/codex`)
2. Check `codex login` status and prompt if needed
3. Show a QR code for Feishu/Lark app creation
4. Create PersonalAgent app and save config
5. Install and initialize `lark-cli` with the same App ID
6. Start listening for chat events

After setup, test in Feishu/Lark DM:
```text
/status
Help me inspect this repo
```

## Requirements

- Node.js >= 20
- Network access to npm, OpenAI/Codex, and Feishu/Lark platform
- Terminal for QR scan and login prompts

### Custom Codex Binary

```bash
export CODEX_BIN="/path/to/codex"
```

Bridge checks these locations in order:
1. `$CODEX_BIN`
2. `codex` in `$PATH`
3. `~/.feishu-codex-bridge/codex-cli`
4. `/Applications/Codex.app/Contents/Resources/codex` (macOS)

## Configuration

### Directory Structure

```
~/.feishu-codex-bridge/
├── config.json              # App config and preferences
├── secrets.enc              # Encrypted App Secret store
├── sessions.json            # Chat-to-session mapping
├── workspaces.json          # Named workspaces
├── processes.json           # Live process registry
├── service.log              # Service stdout
├── service.err.log          # Service stderr
├── logs/YYYY-MM-DD.log      # Daily structured logs
├── media/<chatId>/          # Downloaded attachments (24h TTL)
├── codex-cli/               # Private Codex CLI install
└── lark-cli/                # Private Lark CLI install
```

### config.json Structure

```json
{
  "appId": "cli_a1234567890abcde",
  "tenant": "feishu",
  "preferences": {
    "codexReasoningEffort": "high",
    "timeout": 300,
    "replyMode": "stream",
    "allowedUsers": [],
    "allowedChats": [],
    "admins": []
  }
}
```

### Reasoning Effort

Set globally in `config.json` or per-chat via `/config`:

```json
{
  "preferences": {
    "codexReasoningEffort": "xhigh"
  }
}
```

Values: `minimal`, `low`, `medium`, `high`, `xhigh`. Omit to inherit from `~/.codex/config.toml`.

### Access Control

Restrict bot access in `config.json`:

```json
{
  "preferences": {
    "allowedUsers": ["ou_1234567890abcdef"],
    "allowedChats": ["oc_9876543210fedcba"],
    "admins": ["ou_1234567890abcdef"]
  }
}
```

Find IDs from logs:
```bash
grep '"event":"enter"' ~/.feishu-codex-bridge/logs/$(date +%Y-%m-%d).log | tail -5
```

## Chat Commands

### Status and Control

```text
/status                      # Show cwd, session, agent, reasoning effort
/help                        # Show help card with all commands
/stop                        # Stop current Codex run
/reconnect                   # Reconnect WebSocket
/ps                          # List bridge processes
/exit <id|#>                 # Stop a bridge process (admin)
/doctor [description]        # Diagnose bridge issues with Codex
```

### Session Management

```text
/new                         # Reset current chat's session
/reset                       # Alias for /new
/resume [N]                  # List and resume recent sessions in cwd
/timeout [N|off|default]     # Set idle timeout for current session
```

### Workspace Management

```text
/cd <path>                   # Change working directory (resets session)
/ws list                     # List named workspaces
/ws save <name> [path]       # Save workspace (defaults to current cwd)
/ws use <name>               # Switch to workspace
/ws remove <name>            # Delete workspace
```

Example workspace workflow:
```text
/cd ~/projects/api-server
/ws save api-server
/cd ~/projects/frontend
/ws save frontend
/ws list
/ws use api-server
```

### Configuration

```text
/config                      # Open interactive config menu
/account                     # View or change Feishu/Lark app (admin)
```

## Background Service

### Install and Manage (macOS launchd)

```bash
# Complete foreground setup first
feishu-codex-bridge start
# Test with /status in chat, then Ctrl+C

# Install service
feishu-codex-bridge service install launchd

# Check status
feishu-codex-bridge service status

# View logs
feishu-codex-bridge service logs --follow

# Restart
feishu-codex-bridge service restart

# Uninstall
feishu-codex-bridge service uninstall
```

### Service Logs

```bash
# Stdout
tail -f ~/.feishu-codex-bridge/service.log

# Stderr
tail -f ~/.feishu-codex-bridge/service.err.log

# Structured daily logs
tail -f ~/.feishu-codex-bridge/logs/$(date +%Y-%m-%d).log
```

## Platform Configuration

After QR setup, configure in Feishu/Lark Developer Console:

### Required Permission Scopes

- `im:message`
- `im:message:send_as_bot`
- `im:resource`
- `im:chat` (for group creation)
- `drive:drive` (for cloud-doc comments)

### Event Subscriptions (Long-Connection Mode)

- `im.message.receive_v1`
- `card.action.trigger`
- `drive.notice.comment_add_v1` (for `@bot` in docs)
- `im.message.reaction.created_v1` (optional)
- `im.message.reaction.deleted_v1` (optional)
- `im.chat.member.bot.added_v1` (optional)

**Important**: Bridge and `lark-cli` must use the **same** App ID. Do not run `lark-cli config init --new` after bridge setup.

## User OAuth

Required only for accessing personal resources (user's docs, calendar, chat history):

```bash
export PATH="$HOME/.feishu-codex-bridge/lark-cli/node_modules/.bin:$PATH"
lark-cli auth login --recommend
```

Bot identity works for tenant/bot APIs. User OAuth needed for personal resource access.

## Development

### From Source

```bash
git clone https://github.com/QQQingyu/feishu-codex-bridge.git
cd feishu-codex-bridge
npx pnpm@10.20.0 install
npx pnpm@10.20.0 build
node bin/feishu-codex-bridge.mjs --help
```

### Type Checking and Tests

```bash
npx pnpm@10.20.0 typecheck
npx pnpm@10.20.0 test
```

## Troubleshooting

### Bot is Silent

```bash
# Check process state
feishu-codex-bridge ps
feishu-codex-bridge service status

# Follow logs
feishu-codex-bridge service logs --follow

# Check today's structured logs
tail -f ~/.feishu-codex-bridge/logs/$(date +%Y-%m-%d).log
```

If process is running but bot doesn't respond, verify:
- Permission scopes in Developer Console
- Event subscriptions are enabled
- Long-connection mode is active

### Codex CLI Issues

```bash
# Auto-diagnose
feishu-codex-bridge doctor

# Rerun setup
feishu-codex-bridge start
```

Common fixes:
- Codex not in PATH: Bridge auto-installs to `~/.feishu-codex-bridge/codex-cli`
- Not logged in: Setup prompts for `codex login`
- App mismatch: Ensure bridge and lark-cli use same App ID

### Lark CLI Path Issues

Add to shell profile for direct terminal usage:

```bash
export PATH="$HOME/.feishu-codex-bridge/lark-cli/node_modules/.bin:$PATH"
```

For Codex runs, bridge handles PATH automatically.

### App ID Mismatch

If `lark-cli` was initialized with a different app:

```bash
feishu-codex-bridge start
# Follow prompt to switch lark-cli back to bridge app
```

Never run `lark-cli config init --new` after bridge setup.

### Hanging Codex Runs

```text
# In chat:
/stop

# Set idle timeout globally
/config
# Or for current session only:
/timeout 10
```

### Process Conflicts

Only one bridge instance per Feishu/Lark app. Stop foreground before installing service:

```bash
# Stop all bridge processes
feishu-codex-bridge ps
feishu-codex-bridge exit <id>

# Or kill directly
pkill -f feishu-codex-bridge
```

### Log Analysis

```bash
# Recent events
grep '"event":"enter"' ~/.feishu-codex-bridge/logs/$(date +%Y-%m-%d).log | tail -10

# Errors
grep '"level":"error"' ~/.feishu-codex-bridge/logs/$(date +%Y-%m-%d).log | tail -10

# Specific chat
grep '"chatId":"oc_..."' ~/.feishu-codex-bridge/logs/$(date +%Y-%m-%d).log
```

## Common Patterns

### Multi-Project Workspace Setup

```typescript
// Save workspaces for quick switching
/cd ~/work/backend-api
/ws save backend
/cd ~/work/frontend-app
/ws save frontend
/cd ~/work/docs
/ws save docs

// Switch between projects
/ws use backend
Help me add rate limiting to the auth endpoint

/ws use frontend
Update the login form to show better errors

/ws use docs
Generate API docs from the OpenAPI spec
```

### Session Resume After Restart

```text
# List recent sessions in current directory
/resume

# Resume specific session (shows last 10)
/resume 3
```

### Per-Chat Reasoning Effort

```text
# High effort for complex refactoring
/config
# Select "Reasoning Effort" > "xhigh"

# In different chat, use default
/config
# Select "Reasoning Effort" > "default"
```

### Access Control Setup

```json
{
  "preferences": {
    "allowedUsers": [
      "ou_dev_team_member_1",
      "ou_dev_team_member_2"
    ],
    "allowedChats": [
      "oc_dev_team_group"
    ],
    "admins": [
      "ou_dev_team_member_1"
    ]
  }
}
```

### Debugging Bridge Behavior

```text
# In chat:
/doctor The bot isn't responding to file attachments

# Codex will analyze recent logs and suggest fixes
```

## Architecture

```text
Feishu/Lark Chat
  ↓ WebSocket
Bridge Process
  ↓ spawn
codex exec/resume
  ↓ optional
lark-cli API calls
  ↓
Streaming Card Reply
```

Responsibilities:
- **Bridge**: Event handling, session mapping, attachment downloads, card rendering, process lifecycle
- **Codex CLI**: Code reasoning, file editing, command execution, session resume
- **Lark CLI**: API tool for messages, docs, calendars, groups, OAuth

## License

MIT
