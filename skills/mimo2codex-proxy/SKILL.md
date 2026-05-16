---
name: mimo2codex-proxy
description: Local proxy that lets OpenAI Codex CLI/desktop talk to MiMo, DeepSeek, and other LLMs via Responses API translation
triggers:
  - set up mimo2codex to use MiMo with Codex
  - configure Codex to use DeepSeek through mimo2codex
  - start the mimo2codex proxy server
  - add a custom provider to mimo2codex
  - use MiMo models in Codex CLI
  - troubleshoot mimo2codex reasoning_content errors
  - enable web search in mimo2codex
  - switch Codex models with mimo2codex webui
---

# mimo2codex Proxy Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

**mimo2codex** is a local proxy server that translates between OpenAI Codex's Responses API (`wire_api = "responses"`) and upstream LLM providers using Chat Completions API. It enables the latest Codex CLI and desktop app to work with:

- **Xiaomi MiMo** (V2.5 Pro, V2 Flash, V2 Omni)
- **DeepSeek** (V4 Pro, V4 Flash, Reasoner)
- **Generic OpenAI-compatible providers** (Qwen, GLM, Kimi, Ollama, vLLM, LM Studio)

**Key features:**
- Per-request model routing (send `mimo-v2.5-pro` → MiMo, `deepseek-v4-pro` → DeepSeek)
- Automatic MiMo `reasoning_content` round-trip handling (v0.2.3+)
- Built-in admin webui at `http://127.0.0.1:8788/admin/`
- Tool calling, web search, vision (model-dependent)
- sqlite persistence for logs and token stats

## Installation

### npm (recommended)

```bash
npm install -g mimo2codex
```

### curl one-liner

```bash
# macOS/Linux
curl -fsSL https://raw.githubusercontent.com/7as0nch/mimo2codex/main/scripts/install.sh | bash

# Windows PowerShell
irm https://raw.githubusercontent.com/7as0nch/mimo2codex/main/scripts/install.ps1 | iex
```

### Git clone (for development)

```bash
git clone https://github.com/7as0nch/mimo2codex
cd mimo2codex
npm install
npm run build
npm link  # registers `mimo2codex` globally
```

**Requirements:** Node.js ≥ 18

## Quick Start

### 1. Get API Keys

- **MiMo**: [platform.xiaomimimo.com](https://platform.xiaomimimo.com) → Console → API Keys (`sk-` or `tp-` prefix)
- **DeepSeek**: [api-docs.deepseek.com](https://api-docs.deepseek.com) → API Keys (`sk-` prefix)

### 2. Configure Environment Variables

**Built-in loader (v0.2.8+, recommended):**

```bash
# Initialize .env file in ~/.mimo2codex/
mimo2codex init

# Edit ~/.mimo2codex/.env and add your keys:
# MIMO_API_KEY=sk-your-mimo-key
# DS_API_KEY=sk-your-deepseek-key

# Start (auto-loads .env)
mimo2codex
```

**Manual environment variables:**

```bash
# MiMo only
export MIMO_API_KEY=sk-your-mimo-key
mimo2codex

# DeepSeek only
export DS_API_KEY=sk-your-deepseek-key
mimo2codex --model ds

# Both providers (per-request routing)
export MIMO_API_KEY=sk-your-mimo-key
export DS_API_KEY=sk-your-deepseek-key
mimo2codex
```

### 3. Configure Codex

The startup banner prints the required snippets. Copy them to:

**macOS/Linux:**
- `~/.codex/auth.json`
- `~/.codex/config.toml`

**Windows:**
- `%USERPROFILE%\.codex\auth.json`
- `%USERPROFILE%\.codex\config.toml`

**Example `auth.json`:**

```json
{
  "base_url": "http://127.0.0.1:8788",
  "api_key": "fake_api_key"
}
```

**Example `config.toml`:**

```toml
wire_api = "responses"
model = "mimo-v2.5-pro"
```

### 4. Start Codex

```bash
codex
```

## CLI Commands

### Core Commands

```bash
# Start proxy (MiMo default)
mimo2codex

# Start with DeepSeek as default
mimo2codex --model ds

# Custom port
mimo2codex --port 9000

# Custom data directory
mimo2codex --data-dir /path/to/data

# Disable reasoning display (still round-trips for MiMo)
mimo2codex --no-reasoning

# Disable .env auto-loading
mimo2codex --no-load-env
```

### Utility Commands

```bash
# Initialize .env file
mimo2codex init

# Print cc-switch snippets
mimo2codex print-cc-switch

# Show version
mimo2codex --version

# Show help
mimo2codex --help
```

## Configuration

### Environment Variables

| Variable | Provider | Required |
|----------|----------|----------|
| `MIMO_API_KEY` | MiMo | For MiMo models |
| `DS_API_KEY` or `DEEPSEEK_API_KEY` | DeepSeek | For DeepSeek models |
| `QWEN_API_KEY` | Qwen | For Qwen models |
| `GLM_API_KEY` | GLM | For GLM models |
| `KIMI_API_KEY` | Kimi | For Kimi models |
| `OPENAI_API_KEY` | OpenAI | For OpenAI models |
| `CODEX_HOME` | - | Custom Codex config directory |

### CLI Flags

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | `8788` | Proxy server port |
| `--host` | `127.0.0.1` | Proxy server host |
| `--model` | `mimo` | Default provider (`mimo` or `ds`) |
| `--data-dir` | `~/.mimo2codex` | Data/logs directory |
| `--no-reasoning` | `false` | Hide reasoning from terminal |
| `--no-load-env` | `false` | Disable .env auto-loading |
| `--log-level` | `info` | Log level (debug/info/warn/error) |

## Model Routing

### Built-in Model IDs

**MiMo:**
- `mimo-v2.5-pro` (default)
- `mimo-v2-flash`
- `mimo-v2.5` (vision)
- `mimo-v2-omni` (vision)

**DeepSeek:**
- `deepseek-v4-pro` (default)
- `deepseek-v4-flash`
- `deepseek-chat`
- `deepseek-reasoner`

### Routing Logic

1. **Explicit match**: If client sends `mimo-v2.5-pro`, routes to MiMo (if key configured)
2. **Fallback**: If client sends unknown model (e.g. `gpt-4o`), routes to `--model` provider's default
3. **Provider disabled**: If client sends `qwen3-max` but no `QWEN_API_KEY`, falls back to `--model` provider

Example routing with both keys configured:

```bash
export MIMO_API_KEY=sk-mimo-key
export DS_API_KEY=sk-deepseek-key
mimo2codex  # default fallback: mimo

# In Codex config.toml:
# model = "deepseek-v4-pro"  → Routes to DeepSeek
# model = "mimo-v2.5-pro"    → Routes to MiMo
# model = "gpt-4o"           → Falls back to mimo-v2.5-pro
```

## Admin Web UI

Access at `http://127.0.0.1:8788/admin/` (port matches `--port`)

### Features

- **Dashboard**: Token usage charts, cache hit rates, request stats
- **Models**: View all available models, test with ⚡Probe button
- **Providers**: View/edit provider configs from `providers.json`
- **Logs**: Browse chat logs with filtering
- **Settings**: Configure Codex paths, manage aliases
- **Codex Enable**: One-click write of `auth.json` and `config.toml` (replaces cc-switch)

### Codex Enable (v0.2.6+)

1. Open `http://127.0.0.1:8788/admin/`
2. Click "Codex Enable" tab
3. Select model and click "Apply"
4. Automatically backs up existing configs (first OpenAI backup preserved permanently)

**Runtime override mode**: Switch models without restarting Codex (experimental)

## Adding Custom Providers

Edit `~/.mimo2codex/providers.json` (created after first run):

```json
{
  "providers": [
    {
      "name": "qwen",
      "baseUrl": "https://dashscope.aliyuncs.com/compatible-mode/v1",
      "apiKeyEnvVar": "QWEN_API_KEY",
      "defaultModel": "qwen3-max",
      "models": ["qwen3-max", "qwen-turbo"],
      "aliases": {
        "qwen3": "qwen3-max"
      },
      "supportsWebSearch": true
    }
  ]
}
```

**Provider schema:**

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique provider identifier |
| `baseUrl` | string | OpenAI-compatible base URL |
| `apiKeyEnvVar` | string | Environment variable name |
| `defaultModel` | string | Model ID for fallback |
| `models` | string[] | Supported model IDs |
| `aliases` | object | Model alias mappings |
| `supportsWebSearch` | boolean | Enable web search tool |

### Example: Ollama

```json
{
  "name": "ollama",
  "baseUrl": "http://localhost:11434/v1",
  "apiKeyEnvVar": "OLLAMA_API_KEY",
  "defaultModel": "llama3.2",
  "models": ["llama3.2", "qwen2.5-coder"],
  "aliases": {
    "llama": "llama3.2"
  },
  "supportsWebSearch": false
}
```

```bash
export OLLAMA_API_KEY=ollama  # Any non-empty value
mimo2codex
```

In Codex `config.toml`:

```toml
model = "llama3.2"
```

## Tool Calling

### Supported Tools

- **Function tools**: Custom JSON schemas
- **local_shell**: Execute shell commands
- **MCP tools**: Via `namespace` parameter
- **web_search**: MiMo native (auto-enabled for MiMo, skipped for DeepSeek)

### Web Search

**MiMo**: Translates Codex's `web_search` tool to MiMo's native builtin. Requires plugin activation in MiMo console.

**DeepSeek**: Web search not supported — tool calls are stripped.

### Example Tool Call

```typescript
// Codex sends:
{
  "model": "mimo-v2.5-pro",
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_weather",
        "parameters": {
          "type": "object",
          "properties": {
            "location": { "type": "string" }
          }
        }
      }
    }
  ]
}

// mimo2codex translates to MiMo Chat Completions:
{
  "model": "mimo-v2.5-pro",
  "tools": [
    {
      "type": "function",
      "function": { ... }
    }
  ]
}
```

## Vision Support

**Supported models:**
- `mimo-v2.5` (MiMo)
- `mimo-v2-omni` (MiMo)

**Non-vision models** (`mimo-v2.5-pro`, `mimo-v2-flash`, DeepSeek models): Images are auto-stripped with placeholder text.

### Example Vision Request

In Codex `config.toml`:

```toml
model = "mimo-v2.5"
```

```bash
codex
> Describe this image: /path/to/image.jpg
```

mimo2codex forwards the image URL/base64 to MiMo's vision model.

## MiMo reasoning_content Round-Trip

**Problem**: MiMo requires every assistant message with `tool_calls` to echo back its `reasoning_content` on the next turn. Without this, MiMo returns 400 errors or hallucinates.

**Solution**: mimo2codex ≥ 0.2.3 automatically stores and re-inserts `reasoning_content` on subsequent turns.

### Example

```typescript
// Turn 1: MiMo returns
{
  "role": "assistant",
  "content": "",
  "tool_calls": [...],
  "reasoning_content": "I need to search the web"
}

// Turn 2: mimo2codex auto-injects reasoning_content
{
  "role": "assistant",
  "content": "",
  "tool_calls": [...],
  "reasoning_content": "I need to search the web"  // ← auto-added
}
```

**Flag**: `--no-reasoning` hides reasoning from terminal but preserves round-trip.

## Common Patterns

### Multi-Provider Setup

```bash
# .env file (~/.mimo2codex/.env)
MIMO_API_KEY=sk-mimo-key
DS_API_KEY=sk-deepseek-key
QWEN_API_KEY=sk-qwen-key

# Start proxy
mimo2codex

# Codex config.toml - switch models dynamically:
# model = "mimo-v2.5-pro"
# model = "deepseek-v4-pro"
# model = "qwen3-max"
```

### Testing Model Connections

Use the admin UI's **⚡Probe** button:

1. Open `http://127.0.0.1:8788/admin/`
2. Go to "Codex Enable" or "Models" tab
3. Click ⚡Probe next to any model
4. Validates key, baseUrl, and model ID end-to-end

### Token Usage Tracking

```bash
# Start proxy
mimo2codex

# View stats at http://127.0.0.1:8788/admin/
# - Dashboard: Charts with cache hit overlay
# - Green bars: Cache hits
# - Gray ghosts: Prompt token totals
# - Window-wide hit rate summary
```

### Custom Codex Directory

```bash
# Via environment variable
export CODEX_HOME=/custom/path
mimo2codex

# Via admin UI settings
# Navigate to Settings → Codex Path
```

## Troubleshooting

### 400 Errors with MiMo (Tool Calls)

**Symptom**: MiMo returns 400 or agent rambles instead of calling tools.

**Cause**: Missing `reasoning_content` round-trip.

**Fix**: Upgrade to mimo2codex ≥ 0.2.3

```bash
npm update -g mimo2codex
```

### Provider Not Routing

**Check**:
1. API key is set: `echo $MIMO_API_KEY`
2. Provider is enabled in startup banner
3. Model ID matches provider's catalog (case-sensitive)

```bash
# Debug with log level
mimo2codex --log-level debug
```

### Port Already in Use

```bash
# Change port
mimo2codex --port 9000

# Update auth.json:
# "base_url": "http://127.0.0.1:9000"
```

### Web Search Not Working

**MiMo**: Activate the web search plugin in [MiMo Console](https://platform.xiaomimimo.com) → Plugins.

**DeepSeek**: Not supported (tool calls are stripped).

### Image Generation (/hatch)

Codex's `/hatch` command calls OpenAI's `image_gen` client-side — mimo2codex cannot intercept this. Workaround: Use `mimoskill/` (see project README).

### .env Not Loading

```bash
# Verify file location
ls ~/.mimo2codex/.env

# Check file syntax (no spaces around =)
cat ~/.mimo2codex/.env

# Disable auto-loading if needed
mimo2codex --no-load-env
```

### Windows PowerShell Execution Policy

If `irm | iex` fails:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

## Integration with cc-switch

Generate cc-switch snippets:

```bash
mimo2codex print-cc-switch
```

Output example:

```toml
[mimo-v2.5-pro]
model = "mimo-v2.5-pro"
wire_api = "responses"
base_url = "http://127.0.0.1:8788"
api_key = "fake_api_key"
```

Copy to cc-switch config and use `cc mimo-v2.5-pro` to switch.

## Data Persistence

**Default location**: `~/.mimo2codex/data.db` (sqlite)

**Stored data**:
- Chat logs (request/response pairs)
- Token usage stats
- Cache hit metrics
- Model mappings

**Custom location**:

```bash
mimo2codex --data-dir /custom/path
```

## TypeScript API (for embedding)

```typescript
import { startServer } from 'mimo2codex';

const server = await startServer({
  port: 8788,
  host: '127.0.0.1',
  dataDir: '~/.mimo2codex',
  logLevel: 'info',
  noReasoning: false,
  loadEnv: true
});

// Server running at http://127.0.0.1:8788
```

## Project Links

- **GitHub**: https://github.com/7as0nch/mimo2codex
- **npm**: https://www.npmjs.com/package/mimo2codex
- **Issues**: https://github.com/7as0nch/mimo2codex/issues
- **Docs**: 
  - [.env Setup](https://github.com/7as0nch/mimo2codex/blob/main/doc/env-setup.md)
  - [Codex Enable](https://github.com/7as0nch/mimo2codex/blob/main/doc/codex-enable.md)
  - [Generic Providers](https://github.com/7as0nch/mimo2codex/blob/main/doc/generic-providers.md)
  - [mimoskill](https://github.com/7as0nch/mimo2codex/blob/main/doc/mimoskill.md)
