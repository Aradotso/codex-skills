---
name: opencodex-gateway
description: Local gateway for Codex Desktop with custom API support, web dashboard, Computer Use engine, and Vision Bridge for text-only models
triggers:
  - "set up OpenCodex gateway for Codex Desktop"
  - "configure custom API models in OpenCodex"
  - "add a third-party model to Codex Desktop"
  - "enable Vision Bridge for text-only models"
  - "configure Computer Use with OpenCodex"
  - "manage OpenCodex dashboard settings"
  - "troubleshoot OpenCodex API integration"
  - "reset Codex to native configuration"
---

# OpenCodex Gateway

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

OpenCodex is a zero-config local gateway that enables Codex Desktop to use third-party APIs (OpenAI-compatible endpoints). It features a bilingual web dashboard for model management, a custom Computer Use engine with native macOS control, and Vision Bridge that lets text-only models handle visual tasks by automatically describing screenshots.

## Installation

```bash
git clone https://github.com/AITabby/opencodex.git
cd opencodex
npm install
npm start
```

The server starts on `http://localhost:8765` and automatically:
- Patches `~/.codex/config.toml` (creates backup)
- Opens the dashboard in your browser
- Enables the API gateway

## Architecture

OpenCodex sits between Codex Desktop and third-party APIs:

```
Codex Desktop → OpenCodex Gateway (localhost:8765) → Third-party API
                      ↓
                Vision Bridge (optional)
                Computer Use Engine
```

## Web Dashboard

Access at `http://localhost:8765/dashboard`

### Key Features

- **API Configuration**: Set base URL, API key, model names
- **Model Management**: Add/remove models, toggle visibility in Codex
- **Language Toggle**: Switch between English and Chinese
- **Live Logs**: SSE-streamed request/response logs
- **One-Click Actions**: Restart Codex, reset to native config

### Configuration Flow

1. Open dashboard
2. Enter API endpoint (e.g., `https://api.openai.com/v1` or `https://api.deepseek.com`)
3. Add API key (stored in `~/.codex/config.toml`)
4. Add model names (e.g., `gpt-4`, `deepseek-chat`)
5. Check boxes for models you want visible in Codex
6. Click "Save Configuration"

## Configuration Files

### Auto-Generated Config

OpenCodex modifies `~/.codex/config.toml`:

```toml
[api]
base_url = "http://localhost:8765/v1"
api_key = "your-actual-api-key"

[[models]]
name = "gpt-4"
enabled = true

[[models]]
name = "deepseek-chat"
enabled = true
```

Original config backed up to `~/.codex/config.toml.backup`

### Environment Variables

For development or custom deployments:

```bash
export OPENCODEX_PORT=8765
export OPENCODEX_API_KEY=sk-your-key-here
export OPENCODEX_BASE_URL=https://api.openai.com/v1
```

## Vision Bridge

Vision Bridge enables text-only models to handle Computer Use tasks by converting screenshots to text descriptions.

### How It Works

1. Codex sends Computer Use request with screenshot
2. OpenCodex detects text-only model
3. Screenshot compressed to 1200px with `sips`
4. Vision model describes the screenshot
5. Description injected into the prompt
6. Text-only model receives modified request

### Configuration

In the dashboard, configure Vision Bridge settings:

```json
{
  "vision_bridge": {
    "enabled": true,
    "endpoint": "https://api.openai.com/v1",
    "model": "gpt-4-vision-preview",
    "api_key": "process.env.VISION_API_KEY",
    "max_dimension": 1200
  }
}
```

### Programmatic Example

If extending OpenCodex, here's how Vision Bridge is invoked:

```typescript
import { VisionBridge } from './vision-bridge';

const bridge = new VisionBridge({
  endpoint: process.env.VISION_ENDPOINT,
  model: 'gpt-4-vision-preview',
  apiKey: process.env.VISION_API_KEY
});

// Automatically converts screenshot to description
const description = await bridge.describeImage(screenshotBase64);
// Injects into prompt for text-only model
const modifiedPrompt = bridge.injectDescription(originalPrompt, description);
```

## Computer Use Engine

OpenCodex implements custom Computer Use actions for macOS using native CGEvent APIs.

### Supported Actions

- **Mouse**: Click, move, drag, scroll
- **Keyboard**: Type text, press keys, shortcuts
- **Window**: Focus, resize, minimize
- **Screenshot**: Capture and compress

### Action Format

Codex sends tool calls in this format:

```json
{
  "type": "computer_use",
  "action": "mouse_click",
  "params": {
    "x": 500,
    "y": 300,
    "button": "left"
  }
}
```

### Example Actions

#### Mouse Click

```typescript
{
  "action": "mouse_click",
  "params": { "x": 500, "y": 300, "button": "left" }
}
```

#### Type Text

```typescript
{
  "action": "type_text",
  "params": { "text": "Hello, world!" }
}
```

#### Screenshot

```typescript
{
  "action": "screenshot",
  "params": { "max_dimension": 1200 }
}
```

Response includes base64 image:

```json
{
  "success": true,
  "image": "iVBORw0KGgoAAAANS..."
}
```

## API Reference

### Proxy Endpoint

All OpenAI-compatible requests go through:

```
POST http://localhost:8765/v1/chat/completions
```

Headers:
```
Authorization: Bearer <your-api-key>
Content-Type: application/json
```

### Dashboard API

#### Get Configuration

```bash
curl http://localhost:8765/api/config
```

#### Update Configuration

```bash
curl -X POST http://localhost:8765/api/config \
  -H "Content-Type: application/json" \
  -d '{
    "base_url": "https://api.deepseek.com",
    "api_key": "sk-...",
    "models": [
      {"name": "deepseek-chat", "enabled": true}
    ]
  }'
```

#### Restart Codex

```bash
curl -X POST http://localhost:8765/api/restart-codex
```

#### Reset to Native

```bash
curl -X POST http://localhost:8765/api/reset-native
```

### Live Logs (SSE)

```bash
curl -N http://localhost:8765/api/logs
```

Stream format:
```
data: {"timestamp": "2026-06-04T10:30:00Z", "level": "info", "message": "Request to gpt-4"}

data: {"timestamp": "2026-06-04T10:30:01Z", "level": "info", "message": "Response 200"}
```

## Common Patterns

### Adding Multiple Models

```typescript
const models = [
  { name: 'gpt-4-turbo', enabled: true },
  { name: 'gpt-4', enabled: true },
  { name: 'claude-3-opus', enabled: false }
];

await fetch('http://localhost:8765/api/config', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ models })
});
```

### Switching Providers

To switch from OpenAI to DeepSeek:

1. Open dashboard
2. Change base URL to `https://api.deepseek.com`
3. Update API key
4. Change model name to `deepseek-chat`
5. Enable Vision Bridge (DeepSeek is text-only)
6. Save configuration

### Custom Vision Model

Use a different vision model for Vision Bridge:

```json
{
  "vision_bridge": {
    "enabled": true,
    "endpoint": "https://api.anthropic.com/v1",
    "model": "claude-3-opus-20240229",
    "api_key": "process.env.ANTHROPIC_API_KEY"
  }
}
```

## Troubleshooting

### Codex Not Connecting

**Symptom**: Codex shows "API Error" or "Connection Failed"

**Solution**:
1. Verify OpenCodex is running: `curl http://localhost:8765/health`
2. Check `~/.codex/config.toml` has `base_url = "http://localhost:8765/v1"`
3. Restart Codex via dashboard or manually
4. Check logs: `http://localhost:8765/dashboard` → scroll to logs

### Models Not Appearing

**Symptom**: Added models don't show in Codex

**Solution**:
1. Ensure model checkbox is **checked** in dashboard
2. Click "Save Configuration"
3. Restart Codex (one-click button in dashboard)
4. Verify `~/.codex/config.toml` includes the model with `enabled = true`

### Vision Bridge Not Working

**Symptom**: Text-only model fails on Computer Use tasks

**Solution**:
1. Enable Vision Bridge in dashboard
2. Configure vision model endpoint and API key
3. Test vision model separately: `curl -X POST <vision_endpoint>/chat/completions`
4. Check OpenCodex logs for vision errors
5. Ensure screenshot compression succeeds: verify `sips` is available (`which sips`)

### Rate Limiting

**Symptom**: 429 errors in logs

**Solution**:
- OpenCodex passes through rate limits from upstream API
- Reduce request frequency in Codex
- Check API provider's rate limits
- Consider adding retry logic (upstream API responsibility)

### Port Already in Use

**Symptom**: `Error: listen EADDRINUSE: address already in use :::8765`

**Solution**:
```bash
# Find process on port 8765
lsof -i :8765
# Kill it
kill -9 <PID>
# Or change port
export OPENCODEX_PORT=8766
npm start
```

### Config Corruption

**Symptom**: Codex behaves unexpectedly after config changes

**Solution**:
1. Click "Reset to Native Codex" in dashboard
2. Restores `~/.codex/config.toml.backup`
3. Restart Codex
4. Reconfigure OpenCodex carefully

### Screenshot Too Large

**Symptom**: Vision API rejects screenshots

**Solution**:
- Default max dimension: 1200px
- Reduce in Vision Bridge settings:
```json
{ "max_dimension": 800 }
```
- Verify compression: check OpenCodex logs for `sips` output

## Development

### Project Structure

```
opencodex/
├── src/
│   ├── server.ts          # Main Express server
│   ├── vision-bridge.ts   # Vision Bridge logic
│   ├── computer-use.ts    # macOS automation
│   └── config.ts          # Config patching
├── public/
│   └── dashboard.html     # Web UI
└── package.json
```

### Running in Dev Mode

```bash
npm run dev  # Enables hot-reload
```

### Adding Custom Actions

Extend Computer Use engine:

```typescript
// src/computer-use.ts
export async function customAction(params: any) {
  // Use node-mac-automation or applescript
  const result = execSync(`osascript -e 'tell application "Finder" to ...'`);
  return { success: true, result: result.toString() };
}
```

Register in action handler:

```typescript
case 'custom_action':
  return await customAction(params);
```

### Logging

Add custom logs visible in dashboard:

```typescript
import { logger } from './logger';

logger.info('Custom event', { data: someData });
logger.error('Something failed', { error });
```

## Integration with OpenCodexBar

For the ultimate experience, pair with [OpenCodexBar](https://github.com/AITabby/opencodex-bar):

1. Run OpenCodex gateway: `npm start`
2. Clone and compile OpenCodexBar
3. Launch bar app
4. Press `Option + Space` for system-wide voice activation
5. Enjoy real-time audio VAD and cinematic visualizer

Both projects work independently but are designed to complement each other.
