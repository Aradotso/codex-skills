---
name: codex-router-external-models
description: Route external AI models (Kimi, DeepSeek, Claude, Grok) through local proxy into Codex and Cursor
triggers:
  - set up external models in Codex
  - install codex-router for external providers
  - add Kimi or DeepSeek to my Codex
  - configure external model routing
  - troubleshoot codex-router setup
  - enable Claude or Grok in Codex
  - manage external model providers
  - fix missing models in Codex catalog
---

# Codex Router External Models

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

Codex Router is a local credential-isolating proxy that enables Anthropic Claude, Kimi, DeepSeek, Grok, and other external models inside Codex App/CLI and Cursor. It:

- Merges external models into the native Codex picker
- Isolates API keys and OAuth sessions per provider
- Preserves existing Codex GPT models, profiles, and ChatGPT login
- Runs as a background service on localhost
- Supports safe migration from older versions with rollback

**Targets:**
- **Codex App/CLI**: Responses API with native catalog merge (stable)
- **Cursor**: Manual OpenAI-compatible base URL (experimental)

**Requirements:**
- Node.js 22.19+ (24 LTS recommended)
- `uv` or Python 3.10+ with `venv`
- Git (for managed checkout/rollback)
- Target app installed (Codex or Cursor)

## Installation

### Guided Installation (Recommended)

**macOS/Linux:**
```bash
curl -fsSL https://raw.githubusercontent.com/duolahypercho/codex-router/main/install.sh \
  | sh -s -- --target codex --guided
```

**Windows PowerShell:**
```powershell
$installer = Join-Path $env:TEMP "codex-router-install.ps1"
Invoke-WebRequest https://raw.githubusercontent.com/duolahypercho/codex-router/main/install.ps1 -OutFile $installer
powershell.exe -NoProfile -ExecutionPolicy Bypass -File $installer -Target codex -Guided
```

The guided installer:
- Detects existing authentication (OAuth sessions, API keys)
- Prompts invisibly for new API keys (no echo)
- Installs background service
- Verifies all layers
- Never makes paid test requests unless `--smoke-test` is explicitly added

### Manual Clone

```bash
git clone https://github.com/duolahypercho/codex-router.git
cd codex-router
```

## Key Commands

All commands use `./bin/model-router` (or `./model-router.ps1` on Windows).

### Provider Management

```bash
# List all providers and their status
./bin/model-router codex providers

# Enable a provider
./bin/model-router codex providers enable deepseek
./bin/model-router codex providers enable kimi-oauth

# Disable a provider
./bin/model-router codex providers disable anthropic-api

# Set API key (invisible prompt)
./bin/model-router codex provider-key deepseek set
./bin/model-router codex provider-key anthropic-api set
./bin/model-router codex provider-key ollama-cloud set

# Remove API key
./bin/model-router codex provider-key deepseek remove
```

### Diagnostics

```bash
# Run comprehensive health check
./bin/model-router codex doctor

# Refresh merged catalog (after provider changes)
./bin/refresh-catalog

# Check service status
./bin/model-router codex status
```

### Model Curation (Catalog-Only Providers)

For providers without preselected models (Groq, OpenRouter, Together AI, etc.):

```bash
# Add provider key
./bin/model-router codex provider-key groq set

# Curate models from live catalog
./bin/curate-models groq

# Test a curated model before using
./bin/test-model 'groq/llama-3.3-70b-versatile' --live --yes
```

### Control Commands

```bash
# Toggle authentication mode
./bin/control auth-mode on   # Require native GPT models
./bin/control auth-mode off  # Allow external-only usage

# Restart service
./bin/model-router codex restart
```

## Configuration

### Codex Integration

The installer adds these blocks to `~/.codex/config.toml`:

```toml
# BEGIN codex-router-managed
openai_base_url = "http://127.0.0.1:4102/_codex-router/<capability-token>/v1"
model_catalog_json = "/absolute/path/.codex/codex-router/merged-models.json"
# END codex-router-managed

# BEGIN codex-router-provider-managed
[model_providers.codex-router]
name = "Codex Router (external models)"
base_url = "http://127.0.0.1:4102/_codex-router/<capability-token>/v1"
wire_api = "responses"
# END codex-router-provider-managed
```

**Never edit these blocks manually.** Use router commands to modify configuration.

### Available Providers and Models

**OAuth Providers (use existing CLI sessions):**
```javascript
// Kimi OAuth (requires: kimi login)
'kimi-oauth/kimi-for-coding-highspeed'  // K2.7 Coding Highspeed
'kimi-oauth/kimi-for-coding'            // K2.7 Coding
'kimi-oauth/k3'                         // Kimi K3

// Grok OAuth (requires: grok login --oauth)
'grok-oauth/grok-4.5'
```

**API Key Providers:**
```javascript
// Kimi Platform (separate from OAuth)
'kimi-api/kimi-k3'

// DeepSeek
'deepseek/deepseek-v4-flash'
'deepseek/deepseek-v4-pro'

// xAI
'grok-api/grok-4.5'

// Anthropic
'anthropic-api/claude-opus-4.8'

// Ollama Cloud
'ollama-cloud/glm-5.2'
'ollama-cloud/kimi-k2.7-code'
'ollama-cloud/minimax-m3'
'ollama-cloud/deepseek-v4-pro'

// MiniMax Token Plan
'minimax-token-plan/minimax-m3'

// Qwen Plan
'qwen-plan/qwen3.7-max'
'qwen-plan/qwen3.7-plus'

// Z.ai GLM Coding Plan
'zai-coding/glm-5.2'
'zai-coding/glm-5-turbo'
```

**Catalog-Only Providers (curate models manually):**
- `groq` - Groq
- `openrouter` - OpenRouter
- `together` - Together AI
- `fireworks` - Fireworks AI
- `cerebras` - Cerebras
- `mistral` - Mistral AI
- `nvidia-nim` - NVIDIA NIM
- `siliconflow` - SiliconFlow
- `huggingface` - Hugging Face Router
- `gemini-api` - Google Gemini API

### Environment Variables

Override provider base URLs:

```bash
# Qwen regional endpoint
export QWEN_PLAN_BASE_URL="https://dashscope-intl.aliyuncs.com/compatible-mode/v1"

# Groq custom gateway
export GROQ_BASE_URL="https://custom-groq-endpoint.example.com/v1"
```

State directory override:

```bash
export CODEX_ROUTER_STATE_DIR="$HOME/.codex/codex-router"
```

## Real Usage Examples

### Setting Up DeepSeek

```bash
# Enable provider
./bin/model-router codex providers enable deepseek

# Add API key (get from platform.deepseek.com)
./bin/model-router codex provider-key deepseek set
# Paste key at invisible prompt: sk-...

# Verify
./bin/model-router codex providers
# Should show: deepseek [SHOW] ready

# Refresh catalog and restart Codex
./bin/refresh-catalog
# Quit Codex completely, reopen
# New task → Model picker → DeepSeek V4 Flash/Pro should appear
```

### Setting Up Kimi OAuth

```bash
# Install official Kimi CLI if not present
npm install -g @moonshot-ai/kimi-code

# Authenticate with Kimi
kimi login

# Enable OAuth provider in router
./bin/model-router codex providers enable kimi-oauth

# Verify credential detection
./bin/model-router codex providers
# Should show: kimi-oauth [SHOW] ready (OAuth)

# Refresh and restart
./bin/refresh-catalog
# Quit Codex, reopen → K2.7 models appear
```

### Setting Up Grok with Search Tools

```bash
# Install official Grok CLI
npm install -g @xai-official/grok

# OAuth login
grok login --oauth

# Enable in router
./bin/model-router codex providers enable grok-oauth

# Verify
./bin/model-router codex doctor
# Should pass Grok OAuth checks

# Models will include web_search and x_search tools automatically
```

### Curating Groq Models

```bash
# Add Groq API key
./bin/model-router codex provider-key groq set

# Interactive curation
./bin/curate-models groq
# Shows available models from Groq's live catalog
# Select desired models (e.g., llama-3.3-70b-versatile, mixtral-8x7b)

# Test before production use
./bin/test-model 'groq/llama-3.3-70b-versatile' --live --yes

# Refresh catalog
./bin/refresh-catalog
```

### Managing Multiple Providers

```bash
# Enable multiple providers
./bin/model-router codex providers enable deepseek
./bin/model-router codex providers enable anthropic-api
./bin/model-router codex providers enable ollama-cloud

# Set all keys
./bin/model-router codex provider-key deepseek set
./bin/model-router codex provider-key anthropic-api set
./bin/model-router codex provider-key ollama-cloud set

# Check configuration
./bin/model-router codex providers
# All should show [SHOW] ready

# Run doctor
./bin/model-router codex doctor
```

### Separate Cursor Configuration

Cursor uses independent state:

```bash
# Enable provider for Cursor target
./bin/model-router cursor providers enable deepseek

# Set key (separate from Codex)
./bin/model-router cursor provider-key deepseek set

# Check Cursor-specific status
./bin/model-router cursor providers
./bin/model-router cursor doctor
```

## Common Patterns

### Post-Installation Checklist

```bash
# 1. Run doctor
./bin/model-router codex doctor
# Resolve any FAIL lines

# 2. Verify providers
./bin/model-router codex providers
# Ensure intended providers show [SHOW] ready

# 3. Refresh catalog
./bin/refresh-catalog

# 4. Fully quit Codex (Cmd+Q / Alt+F4)

# 5. Reopen Codex, create new task, open model picker
# External models should appear
```

### Rotating API Keys

```bash
# Remove old key
./bin/model-router codex provider-key deepseek remove

# Add new key
./bin/model-router codex provider-key deepseek set

# Restart service
./bin/model-router codex restart
```

### Disabling External Models Temporarily

```bash
# Disable all external providers
./bin/model-router codex providers disable deepseek
./bin/model-router codex providers disable kimi-oauth
./bin/model-router codex providers disable anthropic-api

# Refresh catalog (will only show native GPT models)
./bin/refresh-catalog

# Re-enable later
./bin/model-router codex providers enable deepseek
./bin/refresh-catalog
```

### Checking Quota/Rate Limits

The router automatically parses rate limit headers:

```javascript
// Most providers send x-ratelimit-* headers
// Anthropic sends anthropic-ratelimit-* headers
// Router displays this on quota cards after first request

// No separate API call needed
// No extra configuration required
// Just use a model once and limits appear
```

## Troubleshooting

### Models Not Appearing in Picker

```bash
# 1. Verify catalog path in config
cat ~/.codex/config.toml | grep model_catalog_json
# Should point to merged-models.json in router state dir

# 2. Check merged catalog exists
ls -lh ~/.codex/codex-router/merged-models.json

# 3. Refresh catalog
./bin/refresh-catalog

# 4. Verify providers are ready
./bin/model-router codex providers
# All enabled providers should show [SHOW] ready

# 5. Fully quit Codex
# macOS: Cmd+Q (not just close window)
# Windows: Alt+F4 or quit from system tray

# 6. Reopen Codex, create NEW task
# Model picker loads catalog at startup only
```

### Windows WSL Configuration Mismatch

When Codex Desktop runs on Windows but commands execute in WSL:

```bash
# Point to Windows Codex home from WSL
export CODEX_HOME=/mnt/c/Users/<WindowsUser>/.codex
export CODEX_ROUTER_STATE_DIR="$CODEX_HOME/codex-router"

# Verify config uses WSL-readable path
grep model_catalog_json /mnt/c/Users/<WindowsUser>/.codex/config.toml
# Should be: /mnt/c/Users/.../merged-models.json
# NOT: C:\Users\...\merged-models.json

# Return to authenticated mode
./bin/control auth-mode off
```

### OAuth Session Expired

```bash
# Kimi OAuth
kimi login
./bin/model-router codex doctor  # Should pass kimi-oauth checks

# Grok OAuth
grok login --oauth
./bin/model-router codex doctor  # Should pass grok-oauth checks
```

### Provider Shows "Not Ready"

```bash
# Check provider details
./bin/model-router codex providers

# If API key provider: ensure key is set
./bin/model-router codex provider-key <provider> set

# If OAuth provider: ensure CLI login succeeded
kimi login status  # for Kimi
grok login --status  # for Grok

# Run full diagnostic
./bin/model-router codex doctor
```

### Service Not Running

```bash
# Check status
./bin/model-router codex status

# Restart service
./bin/model-router codex restart

# Check logs
tail -f ~/.codex/codex-router/logs/service.log
```

### Catalog Merge Fails

```bash
# Reset to native GPT models only
./bin/control auth-mode on
./bin/refresh-catalog

# Verify base catalog
cat ~/.codex/codex-router/native-models.json

# Re-enable external providers one by one
./bin/model-router codex providers enable deepseek
./bin/refresh-catalog
# Check for errors

./bin/model-router codex providers enable anthropic-api
./bin/refresh-catalog
```

### Testing Individual Models

```bash
# Live test (makes real API call)
./bin/test-model 'deepseek/deepseek-v4-flash' --live --yes

# Dry run (validates configuration only)
./bin/test-model 'kimi-oauth/k3'
```

### Regional Endpoint Configuration

```bash
# Qwen Singapore region (default)
# No config needed

# Qwen other regions
export QWEN_PLAN_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
./bin/model-router codex restart

# Verify in next request
```

### Removing Router Completely

```bash
# Disable all providers
./bin/model-router codex providers | grep SHOW | while read provider _; do
  ./bin/model-router codex providers disable "$provider"
done

# Remove managed blocks from config.toml
# (Manual edit or use provided uninstall script)

# Stop service
./bin/model-router codex stop

# Remove state directory
rm -rf ~/.codex/codex-router
```

### Migration from Older Versions

The installer auto-detects and migrates recognized older configurations. To rollback:

```bash
# Rollback uses Git history
cd codex-router
git log --oneline  # Find previous commit
git checkout <commit-hash>
./bin/model-router codex restart
```

## Best Practices

1. **Always run doctor after changes**: `./bin/model-router codex doctor`
2. **Fully quit Codex after catalog refresh**: Catalog loads at startup only
3. **Use invisible prompts for keys**: Never paste keys in chat/logs
4. **Test curated models before production**: `./bin/test-model --live --yes`
5. **Keep providers enabled only when needed**: Reduces picker clutter
6. **Use separate credentials per target**: Codex and Cursor state is independent
7. **Check quota cards after first use**: No extra config needed for rate limits
8. **Verify OAuth sessions periodically**: `kimi login status`, `grok login --status`
