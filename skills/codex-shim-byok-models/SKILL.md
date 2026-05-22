---
name: codex-shim-byok-models
description: Run Codex Desktop with Factory BYOK models and ChatGPT GPT-5.5 via local API shim
triggers:
  - how do I use custom models in Codex Desktop
  - set up codex-shim with Factory models
  - expose my OpenAI API key to Codex
  - add custom models to Codex picker
  - route Codex through local shim server
  - patch Codex Desktop model allowlist
  - configure BYOK models for Codex
  - use ChatGPT subscription with Codex Desktop
---

# Codex Shim BYOK Models

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

**codex-shim** is a local Python API shim that intercepts Codex Desktop's model requests and routes them to:
- Any model in your `~/.factory/settings.json` (Factory BYOK)
- Your ChatGPT subscription GPT-5.5
- Custom OpenAI/Anthropic/generic chat completion endpoints

It exposes a local Responses API endpoint that Codex Desktop points to, bypassing Codex's server-side Statsig model allowlist.

**Key capabilities:**
- Use any OpenAI, Anthropic, DeepSeek, Gemini, OpenRouter, or Z.ai model
- Keep ChatGPT subscription GPT-5.5 alongside BYOK models
- No modification to `~/.codex/config.toml` (uses launch-time overrides)
- Translates between Codex Responses API ↔ upstream APIs (OpenAI chat completions, Anthropic messages)

## Installation

```bash
# Clone repository
git clone https://github.com/0xSero/codex-shim ~/Documents/codex-shim
cd ~/Documents/codex-shim

# Install Python dependencies (requires 3.11+)
python3 -m pip install --user aiohttp pytest

# Symlink commands to PATH
ln -s "$PWD/bin/codex-shim" ~/.local/bin/codex-shim
ln -s "$PWD/bin/codex-app"  ~/.local/bin/codex-app
ln -s "$PWD/bin/codex-model" ~/.local/bin/codex-model
```

Verify installation:
```bash
codex-shim --help
```

## Configuration

### Factory Settings File

The shim reads `~/.factory/settings.json` by default. Structure:

```json
{
  "customModels": [
    {
      "model": "gpt-5.5",
      "provider": "openai",
      "baseUrl": "https://api.openai.com/v1",
      "apiKey": "${OPENAI_API_KEY}",
      "displayName": "OpenAI GPT-5.5",
      "maxContextLimit": 400000
    },
    {
      "model": "claude-opus-4-7-20251109",
      "provider": "anthropic",
      "baseUrl": "https://api.anthropic.com/v1",
      "apiKey": "${ANTHROPIC_API_KEY}",
      "displayName": "Claude Opus 4.7"
    },
    {
      "model": "deepseek-v4-pro",
      "provider": "anthropic",
      "baseUrl": "https://api.deepseek.com/anthropic",
      "apiKey": "${DEEPSEEK_API_KEY}",
      "displayName": "DeepSeek V4 Pro",
      "noImageSupport": true
    }
  ]
}
```

**Supported providers:**
- `openai` → OpenAI `/v1/chat/completions`
- `generic-chat-completion-api` → OpenAI-compatible endpoints
- `anthropic` → Anthropic `/v1/messages`

### Custom Config Path

```bash
codex-shim --settings /path/to/custom-models.json generate
codex-shim --settings /path/to/custom-models.json start
```

### Environment Variables

Store API keys in environment:
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export DEEPSEEK_API_KEY="..."
```

## Key Commands

### Generate Catalog

Reads Factory settings and creates `.codex-shim/custom_model_catalog.json`:

```bash
codex-shim generate
```

### Start/Stop Daemon

```bash
# Start shim on 127.0.0.1:8765
codex-shim start

# Check status
codex-shim status

# Stop daemon
codex-shim stop

# Restart
codex-shim restart
```

### List Available Models

```bash
# Show all generated slugs and upstream routes
codex-shim list

# Show models currently in Codex Desktop picker
codex-model list
```

### Launch Codex Desktop

```bash
# Launch with shim wired in (doesn't modify ~/.codex/config.toml)
codex-app

# Launch and open specific path
codex-app /path/to/project

# Equivalent long form
codex-shim app /path/to/project
```

### Switch Active Model

```bash
# List available slugs
codex-model list

# Set default model for next launch
codex-model openai-gpt-5-5

# Relaunch Codex
codex-app
```

### Run Codex CLI Through Shim

```bash
codex-shim codex -- chat "explain this code"
codex-shim codex -- edit main.py "add error handling"
```

## Model Routing Architecture

```
Codex Desktop → /v1/responses → codex-shim (127.0.0.1:8765)
                                   ┃
                    ┏━━━━━━━━━━━━━━╋━━━━━━━━━━━━━━┓
                    ┃              ┃              ┃
         slug "openai-gpt-5-5"    provider       provider
                    ┃            "openai"      "anthropic"
                    ┃              ┃              ┃
         chatgpt.com/backend-api  baseUrl/       baseUrl/
         /codex/responses         chat/          messages
         (Bearer token)           completions    (x-api-key)
```

The shim:
1. Receives Codex Responses API request
2. Looks up slug in catalog
3. Translates to upstream format (OpenAI chat completions or Anthropic messages)
4. Streams upstream response
5. Translates back to Responses API format

## Code Examples

### Python: Implementing Custom Provider Translation

```python
# codex_shim/translator.py example pattern

async def translate_to_openai(responses_request):
    """Convert Codex Responses API → OpenAI chat completions."""
    return {
        "model": responses_request["model"],
        "messages": responses_request["messages"],
        "stream": True,
        "temperature": responses_request.get("temperature", 1.0),
        "max_tokens": responses_request.get("max_tokens"),
    }

async def translate_to_anthropic(responses_request):
    """Convert Codex Responses API → Anthropic messages."""
    messages = []
    system = None
    
    for msg in responses_request["messages"]:
        if msg["role"] == "system":
            system = msg["content"]
        else:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
    
    body = {
        "model": responses_request["model"],
        "messages": messages,
        "stream": True,
        "max_tokens": responses_request.get("max_tokens", 4096),
    }
    
    if system:
        body["system"] = system
    
    return body
```

### Python: Adding Custom Model Programmatically

```python
import json
from pathlib import Path

def add_custom_model(model_config):
    """Add model to Factory settings."""
    settings_path = Path.home() / ".factory" / "settings.json"
    
    if settings_path.exists():
        with open(settings_path) as f:
            settings = json.load(f)
    else:
        settings = {"customModels": []}
    
    settings["customModels"].append(model_config)
    
    with open(settings_path, "w") as f:
        json.dump(settings, f, indent=2)

# Example: Add OpenRouter model
add_custom_model({
    "model": "anthropic/claude-3.5-sonnet",
    "provider": "openai",
    "baseUrl": "https://openrouter.ai/api/v1",
    "apiKey": "${OPENROUTER_API_KEY}",
    "displayName": "Claude 3.5 Sonnet (OpenRouter)",
    "maxContextLimit": 200000
})
```

### Shell: Automated Setup Script

```bash
#!/bin/bash
# setup-codex-shim.sh

set -e

CODEX_SHIM_DIR="$HOME/Documents/codex-shim"

# Clone and install
if [ ! -d "$CODEX_SHIM_DIR" ]; then
    git clone https://github.com/0xSero/codex-shim "$CODEX_SHIM_DIR"
fi

cd "$CODEX_SHIM_DIR"
python3 -m pip install --user aiohttp

# Symlink commands
mkdir -p "$HOME/.local/bin"
ln -sf "$CODEX_SHIM_DIR/bin/codex-shim" "$HOME/.local/bin/"
ln -sf "$CODEX_SHIM_DIR/bin/codex-app" "$HOME/.local/bin/"
ln -sf "$CODEX_SHIM_DIR/bin/codex-model" "$HOME/.local/bin/"

# Generate catalog and start
codex-shim generate
codex-shim start

echo "✓ Shim installed and running"
codex-shim status
```

## macOS Picker Patch

Codex Desktop's Statsig config hides models not on a server-side allowlist. Apply this one-time ASAR patch to bypass:

```bash
APP=/Applications/Codex.app

# Backup
sudo cp -R "$APP" "$APP.unpatched-$(date +%Y%m%d-%H%M%S)"

# Extract ASAR
cd /tmp && rm -rf codex-asar-patch && mkdir codex-asar-patch && cd codex-asar-patch
npx --yes @electron/asar extract "$APP/Contents/Resources/app.asar" extracted

# Patch picker filter (disables useHiddenModels check)
PATCH_FILE=$(grep -RIl 'useHiddenModels' extracted/webview/assets/model-queries-*.js | head -n1)
sed -i.bak -E 's/let u=c\.useHiddenModels&&o!==`amazonBedrock`,d;/let u=!1,d;/' "$PATCH_FILE"

# Verify exactly one change
diff "$PATCH_FILE.bak" "$PATCH_FILE" && echo "ERROR: No changes made" && exit 1
rm "$PATCH_FILE.bak"

# Repack
npx --yes @electron/asar pack extracted app.asar.new
sudo cp app.asar.new "$APP/Contents/Resources/app.asar"

# Recompute ASAR header hash for Electron integrity check
HEADER_HASH=$(python3 - "$APP/Contents/Resources/app.asar" <<'PY'
import struct, hashlib, sys
with open(sys.argv[1], 'rb') as f:
    data_size, header_size, _, json_size = struct.unpack('<4I', f.read(16))
    header_json = f.read(json_size)
print(hashlib.sha256(header_json).hexdigest())
PY
)

# Update Info.plist
sudo /usr/libexec/PlistBuddy -c \
  "Set :ElectronAsarIntegrity:Resources/app.asar:hash $HEADER_HASH" \
  "$APP/Contents/Info.plist"

# Re-sign (ad-hoc)
sudo codesign --force --deep --sign - "$APP"

echo "✓ Patch applied. Launch Codex Desktop."
```

**Rollback:**
```bash
sudo rm -rf "$APP"
sudo mv "$APP.unpatched-YYYYMMDD-HHMMSS" "$APP"
```

## ChatGPT GPT-5.5 Passthrough

If `~/.codex/auth.json` exists with `auth_mode: chatgpt`, the shim auto-generates a synthetic slug `openai-gpt-5-5` that proxies to:

```
https://chatgpt.com/backend-api/codex/responses
Authorization: Bearer <access_token from auth.json>
```

This bypasses Factory and uses your ChatGPT subscription quota.

**Disable:**
```bash
# Remove from catalog after generation
jq 'del(.models[] | select(.slug == "openai-gpt-5-5"))' \
  .codex-shim/custom_model_catalog.json > tmp.json && mv tmp.json .codex-shim/custom_model_catalog.json
```

## Common Patterns

### Multi-Provider Setup

```json
{
  "customModels": [
    {
      "model": "gpt-5.5",
      "provider": "openai",
      "baseUrl": "https://api.openai.com/v1",
      "apiKey": "${OPENAI_API_KEY}",
      "displayName": "GPT-5.5"
    },
    {
      "model": "claude-opus-4-7-20251109",
      "provider": "anthropic",
      "baseUrl": "https://api.anthropic.com/v1",
      "apiKey": "${ANTHROPIC_API_KEY}",
      "displayName": "Claude Opus 4.7"
    },
    {
      "model": "gemini-2.0-flash-exp",
      "provider": "openai",
      "baseUrl": "https://generativelanguage.googleapis.com/v1beta/openai",
      "apiKey": "${GOOGLE_API_KEY}",
      "displayName": "Gemini 2.0 Flash"
    }
  ]
}
```

### OpenRouter Aggregation

```json
{
  "model": "meta-llama/llama-3.3-70b-instruct",
  "provider": "openai",
  "baseUrl": "https://openrouter.ai/api/v1",
  "apiKey": "${OPENROUTER_API_KEY}",
  "displayName": "Llama 3.3 70B (OpenRouter)"
}
```

### DeepSeek with Anthropic-Style Thinking

```json
{
  "model": "deepseek-v4-pro",
  "provider": "anthropic",
  "baseUrl": "https://api.deepseek.com/anthropic",
  "apiKey": "${DEEPSEEK_API_KEY}",
  "displayName": "DeepSeek V4 Pro",
  "noImageSupport": true
}
```

The shim translates extended thinking blocks from `thinking` items to `reasoning.encrypted_content`.

## Troubleshooting

### Models Don't Appear in Picker

**Cause:** Statsig allowlist still active.

**Solution:** Apply macOS picker patch (see section above).

### "Connection refused" When Launching Codex

**Cause:** Shim daemon not running.

```bash
codex-shim status  # Check if running
codex-shim start   # Start if stopped
```

### 401 Unauthorized Errors

**Cause:** API key not found or invalid.

**Check environment variables:**
```bash
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY
```

**Verify settings file:**
```bash
cat ~/.factory/settings.json | jq '.customModels[].apiKey'
```

**Test upstream directly:**
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### ChatGPT Passthrough Not Working

**Verify auth.json exists:**
```bash
cat ~/.codex/auth.json | jq '.auth_mode'
# Should output: "chatgpt"
```

**Check access token validity:**
```bash
TOKEN=$(jq -r '.access_token' ~/.codex/auth.json)
curl https://chatgpt.com/backend-api/me \
  -H "Authorization: Bearer $TOKEN"
```

### Shim Logs

```bash
# Tail daemon logs
tail -f ~/.codex-shim/codex-shim.log

# Check last 50 lines
tail -n 50 ~/.codex-shim/codex-shim.log
```

### Port Already in Use

```bash
# Change default port (8765)
codex-shim --port 9876 start
codex-shim --port 9876 app
```

### Extended Thinking Not Appearing

**For Anthropic-shaped providers** (Claude, DeepSeek), thinking blocks appear as `reasoning.encrypted_content` items in Codex UI.

**Verify provider is set to `anthropic`:**
```bash
jq '.customModels[] | select(.model=="deepseek-v4-pro") | .provider' \
  ~/.factory/settings.json
```

Should return `"anthropic"`, not `"openai"`.

## Testing

Run test suite:
```bash
cd ~/Documents/codex-shim
python3 -m pytest tests/ -v
```

Test specific translation:
```python
# tests/test_translation.py
import pytest
from codex_shim.translator import translate_to_anthropic

@pytest.mark.asyncio
async def test_system_message_extraction():
    request = {
        "model": "claude-opus-4-7",
        "messages": [
            {"role": "system", "content": "You are helpful"},
            {"role": "user", "content": "Hello"}
        ]
    }
    
    result = await translate_to_anthropic(request)
    assert result["system"] == "You are helpful"
    assert len(result["messages"]) == 1
```

## MCP Tool Forwarding

Codex Desktop forwards three generic MCP tools to **all models** (built-in and shim-routed):

- `list_mcp_resources`
- `list_mcp_resource_templates`
- `read_mcp_resource`

These are available in the function calling schema for every routed model. The model calls `list_mcp_resources` to discover available resources.

**Note:** Codex Desktop does **not** flatten individual MCP server tools. That's a Codex client behavior, not a shim limitation.

---

**Official Repository:** https://github.com/0xSero/codex-shim  
**License:** MIT  
**Requires:** Python 3.11+, aiohttp
