---
name: codex-chatgpt-web-integration
description: Use ChatGPT Web (including Pro) as native models in Codex with full context, streaming, images, and MCP tool integration
triggers:
  - "set up chatgpt web in codex"
  - "integrate chatgpt web with codex"
  - "use chatgpt pro in codex"
  - "configure mcp harness for chatgpt"
  - "connect codex to chatgpt web"
  - "install chatgpt web bridge"
  - "enable chatgpt temporary chat in codex"
  - "troubleshoot codex chatgpt integration"
---

# Codex ChatGPT Web Integration

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

`codex-chatgpt-web` is a bridge that allows you to use ChatGPT Web (including Pro tier) as native models directly within Codex. It provides:

- **Native model integration**: ChatGPT appears in Codex's model picker (Instant, Medium, High, Extra High, Pro)
- **Full context streaming**: Complete task context, images, reasoning, and Markdown streamed back to Codex
- **MCP tool support**: In full mode, ChatGPT can use Codex's filesystem, shell, and configured tools via MCP
- **Temporary Chat privacy**: Each turn starts fresh without polluting ChatGPT history
- **Cross-platform**: macOS (arm64/x64), Windows x64, Linux x64

The bridge runs a local Responses API server that routes Codex tasks through an embedded Playwright browser to ChatGPT Web.

## Installation

### Quick Install (Launcher App)

**macOS or Linux:**
```bash
curl -fsSL https://github.com/miuuyy/codex-chatgpt-web/releases/latest/download/install-launcher.sh | sh
```

**Windows PowerShell:**
```powershell
irm https://github.com/miuuyy/codex-chatgpt-web/releases/latest/download/install-launcher.ps1 | iex
```

### From Source (Requires Bun 1.3.14+)

```bash
git clone https://github.com/miuuyy/codex-chatgpt-web.git
cd codex-chatgpt-web
bun install
bun run app
```

## Initial Setup

After installing the launcher, complete these three steps:

1. **Sign in to ChatGPT** in the embedded browser (Settings → ChatGPT browser)
2. **Run smoke test** to verify browser automation works
3. **Install models** in Codex (press the button, then restart Codex once)

After restart, ChatGPT Web models appear in the native Codex model picker:
- ChatGPT Web — Instant
- ChatGPT Web — Medium  
- ChatGPT Web — High
- ChatGPT Web — Extra High (Pro accounts only)
- ChatGPT Web — Pro (Pro accounts only)

## Configuration

### Browser-Only Mode (Default)

No additional setup required. Codex context is sent to ChatGPT but tools won't work (Codex shows a warning).

### Full Harness Mode (MCP Tools)

Enables ChatGPT to call back into Codex tools (filesystem, shell, etc.) via MCP. Requires OpenAI tunnel setup:

1. **Open MCP tab** in the launcher
2. **Create tunnel**: Go to OpenAI Platform → Tunnels, create one
3. **Create API key**: Same OpenAI account, regular API key (free, no model charges)
4. **Paste credentials** in launcher: Tunnel ID + API key
5. **Connect harness**: Click the button
6. **Enable Developer Mode** in ChatGPT settings
7. **Create connector**:
   - Type: Tunnel
   - Select your tunnel
   - Authentication: None
   - Name: **exactly** `Codex Native`
8. **Scan tools** and set permissions
9. **Verify runtime** in launcher

**Important**: Pro tier cannot initiate MCP calls due to ChatGPT limitations, but receives full context from prior turns.

## Architecture

```
Codex Task ──[Responses API + SSE]──▶ codex-chatgpt-web ──[Playwright]──▶ ChatGPT Web
     ▲                                       │                                  │
     └──────────── Streaming + Tool Results ────────────────────────────────────┘
```

Key components:

- **Launcher app**: Desktop GUI for setup, health checks, logs (Tauri-based)
- **Responses server**: Express server implementing Codex Responses API
- **Browser bridge**: Playwright automation for ChatGPT Web interaction
- **MCP proxy** (full mode): Routes tool calls through OpenAI tunnel to Codex

## Code Examples

### Running the Server Programmatically

```typescript
import { startServer } from './src/server';

// Start the Responses API server
const server = await startServer({
  port: 7878,
  browserProfilePath: './browser-profile',
  maxConcurrentSessions: 5,
  autoApproveMcpToolCalls: false, // Require explicit approval
  mcpProxyPort: 7879
});

console.log(`Server running on http://localhost:${server.port}`);
```

### Browser Automation Flow

```typescript
import { launchBrowser, navigateToTemporaryChat } from './src/browser';

// Launch persistent browser context
const browser = await launchBrowser({
  profilePath: './browser-profile',
  headless: false
});

// Navigate to temporary chat
const page = await browser.newPage();
await navigateToTemporaryChat(page);

// Send message and stream response
await page.fill('[data-testid="prompt-textarea"]', 'Explain TypeScript generics');
await page.click('[data-testid="send-button"]');

// Listen for streaming chunks
page.on('response', async (response) => {
  if (response.url().includes('/backend-api/conversation')) {
    const stream = await response.body();
    // Process SSE stream
  }
});
```

### Responses API Request Format

```typescript
// POST http://localhost:7878/v1/responses
{
  "model": "chatgpt-web-instant", // or medium, high, extra-high, pro
  "messages": [
    {
      "role": "user",
      "content": [
        { "type": "text", "text": "Analyze this image" },
        { 
          "type": "image", 
          "source": {
            "type": "base64",
            "media_type": "image/png",
            "data": "iVBORw0KGgoAAAANSUhEUg..."
          }
        }
      ]
    }
  ],
  "stream": true,
  "metadata": {
    "taskId": "task-123",
    "mcpConnections": [/* MCP server configs */]
  }
}
```

### Handling Streamed Responses

```typescript
import { EventSource } from 'eventsource';

const eventSource = new EventSource('http://localhost:7878/v1/responses', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(request)
});

eventSource.addEventListener('message_start', (e) => {
  const data = JSON.parse(e.data);
  console.log('Message ID:', data.message.id);
});

eventSource.addEventListener('content_block_delta', (e) => {
  const data = JSON.parse(e.data);
  if (data.delta.type === 'text_delta') {
    process.stdout.write(data.delta.text);
  }
});

eventSource.addEventListener('message_stop', () => {
  eventSource.close();
});
```

### MCP Tool Call Handling

```typescript
// Tool call request from ChatGPT
{
  "type": "tool_use",
  "id": "toolu_123",
  "name": "read_file",
  "input": {
    "path": "src/main.ts"
  }
}

// Response sent back to ChatGPT
{
  "role": "user",
  "content": [
    {
      "type": "tool_result",
      "tool_use_id": "toolu_123",
      "content": "export function main() { ... }"
    }
  ]
}
```

## CLI Commands

The launcher provides these operations:

```bash
# Launch the desktop GUI
codex-chatgpt-web

# Run from source
bun run app

# Package native apps
bun run app:package

# Run verification tests
bun run verify

# Development mode with hot reload
bun run dev
```

## Environment Variables

```bash
# Server configuration
PORT=7878                          # Responses API port
MCP_PROXY_PORT=7879               # MCP proxy port
BROWSER_PROFILE_PATH=~/.codex-chatgpt-web/browser
MAX_CONCURRENT_SESSIONS=5

# Full harness mode
OPENAI_API_KEY=                   # From OpenAI Platform
TUNNEL_ID=                        # From OpenAI Tunnels
AUTO_APPROVE_TOOL_CALLS=false     # Dangerous: auto-approve writes

# Browser automation
HEADLESS=false                    # Show browser during automation
SLOW_MO=0                         # Milliseconds to slow automation
```

## Common Patterns

### Switching Between Models

Users can change models mid-task in Codex. Each model selection starts a fresh browser session:

```typescript
// Codex automatically sends model in request
// User switches: Instant → Pro in UI
{
  "model": "chatgpt-web-pro",
  "messages": [/* accumulated context */]
}
// Bridge starts new temporary chat with Pro model
```

### Image Analysis with Context

```typescript
const request = {
  model: "chatgpt-web-high",
  messages: [
    {
      role: "user",
      content: [
        { type: "text", text: "Compare these two screenshots" },
        { type: "image", source: { type: "base64", media_type: "image/png", data: img1 }},
        { type: "image", source: { type: "base64", media_type: "image/png", data: img2 }}
      ]
    }
  ]
};
```

### Cancellation

```typescript
// User cancels in Codex UI
// Server receives DELETE to session endpoint
DELETE http://localhost:7878/v1/sessions/{sessionId}

// Response:
{ "status": "cancelled" }
```

### Tool Call Approval Flow

```typescript
// 1. ChatGPT requests tool call
// 2. Bridge checks AUTO_APPROVE_TOOL_CALLS
// 3. If false and action=write, fails with error:
{
  "error": {
    "type": "tool_approval_required",
    "message": "Write action requires explicit approval"
  }
}
// 4. If approved, forwards to MCP → Codex → returns result
```

## Troubleshooting

### Models Don't Appear in Codex

**Solution**: Click "Install models" in launcher, then **restart Codex completely** (Cmd+Q/Alt+F4, not just reload).

**Verify**: Check Codex config directory for `miuuyy.codex-chatgpt-web` entry:
```bash
# macOS
cat ~/Library/Application\ Support/Codex/responses/models.json

# Linux  
cat ~/.config/codex/responses/models.json

# Windows
type %APPDATA%\Codex\responses\models.json
```

### Smoke Test Fails

**Check**:
1. Sign in status: Open ChatGPT browser tab, verify you're logged in
2. Network: Ensure ChatGPT.com is reachable
3. Browser profile: Settings → Clear browser data, sign in again

**Logs**: Activity tab shows detailed browser automation errors

### Tool Calls Fail

**Full mode not configured**: Codex shows warning. Complete MCP setup.

**Connector name mismatch**: Must be **exactly** `Codex Native` (case-sensitive).

**Verify**:
```bash
# Check tunnel is running
curl http://localhost:7879/health
# Should return: {"status":"ok","tunnelId":"..."}
```

**Permission errors**: Read-only actions work on personal Pro; write actions require workspace admin policy.

### Pro Model Missing

**Cause**: Signed-in account doesn't have ChatGPT Pro subscription.

**Solution**: Subscribe to ChatGPT Pro, sign out/in in launcher browser.

### "Unexpected approval prompt" Error

**Cause**: Tool requested write permission without `--auto-approve-tool-calls`.

**Solution**: Either enable auto-approve (risky) or grant permission in ChatGPT UI before the call.

### Browser Gets Stuck

**Recovery**:
1. Settings → Cancel retained browser turn
2. If persists: Settings → Clear browser data
3. Last resort: Delete `~/.codex-chatgpt-web/browser` and sign in again

### Rate Limiting

ChatGPT Web has usage limits per tier. Spread work across models or wait for limit reset.

**Monitor**: Activity tab shows rate limit errors from ChatGPT

## Security Considerations

- **Browser profile is sensitive**: Contains login session. Never share or commit.
- **Localhost exposure**: Server binds to 127.0.0.1, reachable by local user processes.
- **Temporary Chat**: Prompts sent to OpenAI, subject to their policies.
- **MCP tunnel**: Outbound only, no public IP exposed.
- **Auto-approve**: `--auto-approve-tool-calls` bypasses safety checks—use only in trusted environments.

Before production use, review:
- [Security model](https://github.com/miuuyy/codex-chatgpt-web/blob/main/docs/security-model.md)
- [Architecture docs](https://github.com/miuuyy/codex-chatgpt-web/blob/main/docs/architecture.md)

## Advanced Configuration

### Custom MCP Servers in Codex

ChatGPT can use any MCP servers configured in your Codex workspace:

```json
// codex.config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "mcp-server-filesystem",
      "args": ["--root", "/path/to/project"]
    },
    "github": {
      "command": "mcp-server-github",
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

All servers forward through the bridge when `Codex Native` connector is active.

### Multiple Concurrent Sessions

Up to 5 parallel browser tabs supported:

```typescript
// Automatically managed by server
// Each Codex task gets isolated browser context
// Caps at 5 to avoid account throttling
```

### Custom Server Port

```bash
# If 7878 conflicts with other services
PORT=8080 bun run app

# Update Codex responses config to match
```

## Contributing

```bash
# Run tests
bun test

# Lint
bun run lint

# Type check
bun run typecheck

# Full verification
bun run verify
```

See [CONTRIBUTING.md](https://github.com/miuuyy/codex-chatgpt-web/blob/main/CONTRIBUTING.md) for guidelines.

## Resources

- **GitHub**: https://github.com/miuuyy/codex-chatgpt-web
- **Architecture**: https://github.com/miuuyy/codex-chatgpt-web/blob/main/docs/architecture.md
- **Security**: https://github.com/miuuyy/codex-chatgpt-web/blob/main/SECURITY.md
- **OpenAI Tunnels**: https://platform.openai.com/docs/guides/tunnels
- **MCP Protocol**: https://modelcontextprotocol.io
