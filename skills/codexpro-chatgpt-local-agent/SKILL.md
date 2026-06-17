---
name: codexpro-chatgpt-local-agent
description: Use ChatGPT Developer Mode as a local coding agent for your repo through MCP
triggers:
  - set up CodexPro to connect ChatGPT to my local repo
  - use ChatGPT web as a local coding agent
  - configure MCP bridge for ChatGPT Developer Mode
  - let ChatGPT read and edit my local files
  - create a handoff plan for local agent execution
  - export pro context for ChatGPT models without MCP
  - start CodexPro with a stable tunnel URL
  - watch for handoff plans and execute them locally
---

# CodexPro — ChatGPT Local Coding Agent

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## What It Does

CodexPro bridges ChatGPT Developer Mode to your local repository through the Model Context Protocol (MCP). It exposes your repo's context (AGENTS.md, .ai-bridge files, git status, source files) and gives ChatGPT tools to read, write, edit, search, and run safe verification commands locally.

**Key capabilities:**
- ChatGPT web can act as a local coding agent with full file system access
- Supports three workflows: normal coding, handoff to local agents (Codex/Pi/OpenCode), and pro context export
- Uses MCP app infrastructure with safety defaults (workspace-only writes, allowlisted bash)
- Stable tunnel URLs via ngrok or Cloudflare for persistent ChatGPT app configuration

**Not a bypass:** CodexPro uses official ChatGPT Developer Mode and does not modify rate limits, unlock models, or provide account access.

## Installation

### Requirements
- Node.js 20+
- ChatGPT Plus or Pro with Apps/Developer Mode access
- Developer mode enabled: Settings → Apps → Advanced settings
- Tunnel: Cloudflare quick tunnel, ngrok free dev domain, or Cloudflare named tunnel

### Global Install

```bash
npm install -g codexpro
```

### First-Time Setup

Navigate to your project directory:

```bash
cd /path/to/your/project
codexpro setup
```

This interactive setup:
1. Creates `.codexpro-config.json` with workspace path
2. Generates a random auth token
3. Starts the MCP server with a tunnel
4. Copies the Server URL to clipboard
5. Prompts you to paste it into ChatGPT → Apps → Create App

**ChatGPT App Setup:**
- Open ChatGPT → Settings → Apps → Create App
- Paste the Server URL
- Name it "CodexPro Local"
- Enable the app

## Daily Usage

### Start the Server

```bash
codexpro start
```

Options:
- `--mode handoff` - Include handoff/execute tools for local agent workflows
- `--mode default` - Standard coding tools (default)
- `--tunnel none` - Disable public tunnel (localhost only)
- `--tunnel cloudflare` - Use Cloudflare quick tunnel
- `--tunnel ngrok` - Use ngrok with free dev domain
- `--tool-mode minimal` - Smallest tool set (demo/testing)
- `--tool-mode standard` - Normal coding + handoff (default)
- `--tool-mode full` - All compatibility and debugging tools

### Stable URL Setup

**Ngrok (recommended for persistent URLs):**

```bash
# Get a free static domain at https://dashboard.ngrok.com/cloud-edge/domains
export NGROK_AUTHTOKEN=your_token_here
export NGROK_DOMAIN=your-subdomain.ngrok-free.app
codexpro start --tunnel ngrok
```

**Cloudflare Named Tunnel:**

```bash
# Install cloudflared and authenticate
cloudflared tunnel login
cloudflared tunnel create codexpro-tunnel

# Set environment variables
export CLOUDFLARE_TUNNEL_NAME=codexpro-tunnel
codexpro start --tunnel cloudflare-named
```

See [DOMAIN_SETUP.md](https://github.com/rebel0789/codexpro/blob/main/DOMAIN_SETUP.md) for full guide.

## Core Workflows

### 1. Normal Coding Mode

ChatGPT acts directly on your repo:

**User:** "Add input validation to src/api.js"

ChatGPT will:
- Read `src/api.js`
- Edit it with exact text replacement
- Show a diff card
- Run verification commands if needed

**User:** "Show me what changed since last commit"

ChatGPT calls `show_changes` and renders a review card with git status and diff.

### 2. Handoff Mode

ChatGPT writes a plan for a local agent to execute:

```bash
# Terminal 1: Start with handoff mode
codexpro start --mode handoff

# Terminal 2: Watch for plans and auto-execute
codexpro watch-handoff --agent opencode --model anthropic/claude-3.5-sonnet --yes
```

**In ChatGPT:**
"Create a plan to refactor auth.js for better error handling, then hand off to OpenCode"

ChatGPT writes `.ai-bridge/current-plan.md`, the watcher detects it, and OpenCode executes locally.

**Review results:**
```bash
cat .ai-bridge/agent-status.md
cat .ai-bridge/implementation-diff.patch
```

### 3. Pro Context Export

For ChatGPT sessions that can't call MCP tools:

**User:** "Export pro context for this workspace"

ChatGPT writes `.ai-bridge/pro-context.md` with:
- AGENTS.md instructions
- Git status and diff
- File tree
- Current .ai-bridge state

Copy/paste this into a new ChatGPT session.

## Configuration

### Config File: `.codexpro-config.json`

```json
{
  "workspace": "/absolute/path/to/project",
  "token": "generated-random-token",
  "port": 3456,
  "tunnel": "cloudflare",
  "toolMode": "standard",
  "writeMode": "allow",
  "bashMode": "safe",
  "maxFileReadBytes": 524288,
  "allowedBashCommands": [
    "npm test",
    "git status",
    "eslint ."
  ]
}
```

### Environment Variables

```bash
# Tunnel configuration
export NGROK_AUTHTOKEN=your_token
export NGROK_DOMAIN=your-subdomain.ngrok-free.app
export CLOUDFLARE_TUNNEL_NAME=codexpro-tunnel

# Safety controls
export CODEXPRO_WRITE_MODE=allow          # allow | off
export CODEXPRO_BASH_MODE=safe            # safe | off
export CODEXPRO_TOOL_MODE=standard        # minimal | standard | full

# Widget rendering (for app submission)
export CODEXPRO_WIDGET_DOMAIN=https://your-widgets-domain.com
```

### Safety Defaults

**Write protection:**
- Only writes inside configured workspace
- Blocks: `node_modules/`, `.git/`, `.env*`, `*.key`, `*.pem`
- Set `CODEXPRO_WRITE_MODE=off` to disable all writes

**Bash allowlist (safe mode):**
```javascript
[
  "npm test", "npm run test", "npm run lint",
  "git status", "git diff", "git log",
  "node --version", "npm --version",
  "cat package.json", "ls -la"
]
```

Custom commands:
```bash
export CODEXPRO_ALLOWED_BASH_COMMANDS='["make test","cargo check"]'
```

Set `CODEXPRO_BASH_MODE=off` to disable bash entirely.

## Tool Reference

### Standard Mode Tools (Default)

**Workspace:**
- `open_current_workspace` - Open default workspace (safest first call)
- `open_workspace` - Open by path, returns git status, AGENTS.md, discovered skills

**File operations:**
- `read` - Read files with line numbers
- `write` - Create/overwrite files, returns diff
- `edit` - Exact text replacement, returns diff
- `tree` - Inspect file structure
- `search` - Code search with ripgrep

**Execution:**
- `bash` - Run allowlisted commands
- `show_changes` - Visual review card with git status/diff

**Handoff/Export:**
- `handoff_to_agent` - Write `.ai-bridge/current-plan.md`
- `export_pro_context` - Write `.ai-bridge/pro-context.md`
- `read_handoff` - Read .ai-bridge files
- `load_skill` - Load discovered SKILL.md instructions

**Server:**
- `server_config` - Show safety settings and limits

### Minimal Mode (`--tool-mode minimal`)

Only: `server_config`, `open_current_workspace`, `open_workspace`, `read`, `write`, `edit`, `bash`, `show_changes`

### Full Mode (`--tool-mode full`)

Adds debugging/compatibility tools:
- `codexpro_inventory` - List discovered skills and MCP servers
- `list_workspaces` - Show opened workspaces
- `workspace_snapshot` - Full project status
- `git_status`, `git_diff` - Granular git inspection
- `codex_context` - Load Codex-style context in one call
- `handoff_to_codex` - Legacy handoff wrapper

## Real-World Examples

### Example 1: Add Feature with ChatGPT

```
User: "Open my current workspace"
→ ChatGPT calls open_current_workspace, shows project card

User: "Add a /health endpoint to src/server.js"
→ ChatGPT reads src/server.js
→ ChatGPT edits it with new route
→ Shows diff card

User: "Test it"
→ ChatGPT calls bash with "npm test"
→ Shows test output
```

### Example 2: Handoff to OpenCode

**Terminal setup:**
```bash
# Terminal 1
codexpro start --mode handoff

# Terminal 2
codexpro watch-handoff \
  --agent opencode \
  --model anthropic/claude-3.5-sonnet \
  --yes \
  --poll-interval-ms 2000
```

**ChatGPT conversation:**
```
User: "Refactor the auth module to use async/await. Create a plan and hand off to OpenCode."

→ ChatGPT analyzes code
→ Writes .ai-bridge/current-plan.md with:
  - Goal
  - Files to modify
  - Step-by-step instructions
  - Verification commands

→ Watcher detects new plan
→ Runs: opencode --model anthropic/claude-3.5-sonnet --task-file .ai-bridge/current-plan.md

→ OpenCode executes locally
→ Writes: .ai-bridge/agent-status.md, .ai-bridge/implementation-diff.patch
```

**Review:**
```bash
cat .ai-bridge/agent-status.md
git diff
```

### Example 3: Custom Agent Handoff

**Custom agent script (agent.js):**
```javascript
#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const taskFile = process.argv.find(arg => arg.startsWith('--task-file='))?.split('=')[1];
if (!taskFile) {
  console.error('Missing --task-file');
  process.exit(1);
}

const plan = fs.readFileSync(taskFile, 'utf8');
console.log('Custom agent executing plan:', plan);

// Your agent logic here
// Read plan, execute changes, write status

fs.writeFileSync('.ai-bridge/agent-status.md', `# Custom Agent Status\n\nCompleted: ${new Date().toISOString()}`);
```

**Watch for plans:**
```bash
codexpro watch-handoff \
  --agent custom \
  --command "node ./agent.js --task-file {{plan_file}}" \
  --yes
```

### Example 4: Export Context for Pro Model

**ChatGPT can't call MCP tools:**
```
User: "Export pro context"
→ ChatGPT writes .ai-bridge/pro-context.md with:
  - AGENTS.md instructions
  - Git status, diff stats
  - File tree
  - .ai-bridge state
```

**Use in new session:**
```bash
cat .ai-bridge/pro-context.md
# Copy content, paste into new ChatGPT Pro session
```

## Troubleshooting

### ChatGPT Says "Server Offline"

```bash
# Check server is running
curl http://localhost:3456/health

# Restart with tunnel
codexpro start --tunnel ngrok

# Verify token matches
cat .codexpro-config.json
# Compare token in ChatGPT app settings
```

### Write/Edit Not Working

```bash
# Check write mode
codexpro start
# Should show: Write mode: allow

# Check file not blocked
# Blocked: node_modules/, .git/, .env*, *.key, *.pem

# Enable writes if disabled
export CODEXPRO_WRITE_MODE=allow
codexpro start
```

### Bash Commands Failing

```bash
# Check bash mode
codexpro start
# Should show: Bash mode: safe

# Add custom command to allowlist
export CODEXPRO_ALLOWED_BASH_COMMANDS='["make test","npm run build"]'

# Or disable bash restriction (caution)
export CODEXPRO_BASH_MODE=off
```

### Handoff Watcher Not Executing

```bash
# Check watcher is running
codexpro watch-handoff --agent opencode --dry-run

# Verify plan file exists and is new
cat .ai-bridge/current-plan.md

# Check state file
cat .ai-bridge/watch-handoff-state.json

# Force re-execution
rm .ai-bridge/watch-handoff-state.json
codexpro watch-handoff --agent opencode --once
```

### Tunnel URL Changed

**Ngrok free tier:**
- URL changes each restart unless you use a paid static domain

**Solution:**
```bash
# Get free static domain at ngrok.com
export NGROK_DOMAIN=your-subdomain.ngrok-free.app
codexpro start --tunnel ngrok
```

**Cloudflare named tunnel:**
```bash
cloudflared tunnel create codexpro-tunnel
export CLOUDFLARE_TUNNEL_NAME=codexpro-tunnel
codexpro start --tunnel cloudflare-named
```

### Widget Cards Not Showing

```bash
# Refresh ChatGPT app
# Go to: ChatGPT → Settings → Apps → CodexPro Local → Refresh actions

# Check widget domain
export CODEXPRO_WIDGET_DOMAIN=https://rebel0789.github.io
codexpro start
```

## Security Notes

- CodexPro is **not sandboxed**. It gives ChatGPT write access to your workspace.
- Use `CODEXPRO_WRITE_MODE=off` for read-only sessions.
- Use `CODEXPRO_BASH_MODE=safe` to restrict shell commands.
- Tunnel URLs are token-protected but public. Use firewall rules for extra safety.
- Never expose `.codexpro-config.json` (contains auth token).
- See [SECURITY.md](https://github.com/rebel0789/codexpro/blob/main/SECURITY.md) for full guide.

## Integration Patterns

### With Codex

```bash
# CodexPro for ChatGPT web planning
codexpro start

# Codex for local execution
codex execute .ai-bridge/current-plan.md
```

### With CI/CD

```javascript
// .github/workflows/test.yml
- name: Test with CodexPro plan
  run: |
    npm install -g codexpro
    codexpro execute-handoff --agent opencode --review-only
    cat .ai-bridge/agent-status.md
```

### With Docker

```dockerfile
FROM node:20
RUN npm install -g codexpro
WORKDIR /workspace
COPY . .
CMD ["codexpro", "start", "--tunnel", "none"]
```

```bash
docker run -p 3456:3456 -v $(pwd):/workspace codexpro-image
```

## Further Resources

- **Documentation:** https://rebel0789.github.io/codexpro/
- **Stable URL Guide:** [DOMAIN_SETUP.md](https://github.com/rebel0789/codexpro/blob/main/DOMAIN_SETUP.md)
- **FAQ:** [FAQ.md](https://github.com/rebel0789/codexpro/blob/main/FAQ.md)
- **Security:** [SECURITY.md](https://github.com/rebel0789/codexpro/blob/main/SECURITY.md)
- **GitHub:** https://github.com/rebel0789/codexpro
- **npm:** https://www.npmjs.com/package/codexpro

---

**This skill enables agents to guide users through setting up and using CodexPro to bridge ChatGPT Developer Mode to local repositories via MCP, including normal coding, handoff workflows, and pro context export.**
