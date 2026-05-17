---
name: opencode-openai-codex-auth
description: OAuth authentication plugin for OpenCode that enables GPT-5.x and Codex model access via ChatGPT Plus/Pro subscriptions
triggers:
  - "set up OpenCode with ChatGPT authentication"
  - "configure OpenCode to use GPT-5 models"
  - "install opencode-openai-codex-auth plugin"
  - "authenticate OpenCode with my ChatGPT account"
  - "use GPT-5.2 Codex models in OpenCode"
  - "configure OpenCode model variants"
  - "troubleshoot OpenCode OAuth authentication"
  - "switch between OpenCode GPT-5 models"
---

# opencode-openai-codex-auth

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

`opencode-openai-codex-auth` is a TypeScript-based OAuth authentication plugin that connects OpenCode to OpenAI's GPT-5.x and Codex models using your existing ChatGPT Plus/Pro subscription. It provides 22 pre-configured model presets with variant support, eliminating complex API setup while maintaining full model access.

**Key Features:**
- Official ChatGPT OAuth flow (no API keys required)
- 22 model presets across GPT-5.2, GPT-5.2-Codex, and GPT-5.1 families
- Variant system (none/low/medium/high/xhigh) for fine-grained control
- Automatic token refresh and usage-aware error handling
- Multimodal input support (text, images, files)
- Legacy OpenCode (v1.0.209-) and modern (v1.0.210+) compatibility

## Installation

### Quick Install (Recommended)

```bash
# Modern OpenCode (v1.0.210+)
npx -y opencode-openai-codex-auth@latest

# Legacy OpenCode (v1.0.209 and below)
npx -y opencode-openai-codex-auth@latest --legacy
```

### Manual Installation

```bash
# Clone or download the config
git clone https://github.com/numman-ali/opencode-openai-codex-auth.git
cd opencode-openai-codex-auth

# Copy config to OpenCode directory
# Modern:
cp config/opencode-modern.json ~/.opencode/config.json

# Legacy:
cp config/opencode-legacy.json ~/.opencode/config.json
```

### Uninstallation

```bash
# Remove plugin only
npx -y opencode-openai-codex-auth@latest --uninstall

# Remove plugin and all configs
npx -y opencode-openai-codex-auth@latest --uninstall --all
```

## Authentication

### Initial Login

```bash
# Authenticate with ChatGPT account
opencode auth login
```

This opens your browser to complete OAuth flow. Follow the prompts to authorize OpenCode access.

### Verify Authentication

```bash
# Check current auth status
opencode auth status

# Refresh token if needed
opencode auth refresh
```

### Logout

```bash
opencode auth logout
```

## Available Models

### GPT-5.2 Family

**gpt-5.2** (General purpose, latest flagship)
- Variants: `none`, `low`, `medium`, `high`, `xhigh`
- Use case: General coding, documentation, architecture

**gpt-5.2-codex** (Code-specialized)
- Variants: `low`, `medium`, `high`, `xhigh`
- Use case: Code generation, refactoring, debugging

### GPT-5.1 Family

**gpt-5.1-codex-max** (Maximum code performance)
- Variants: `low`, `medium`, `high`, `xhigh`
- Use case: Complex algorithms, large refactors

**gpt-5.1-codex** (Balanced code model)
- Variants: `low`, `medium`, `high`
- Use case: Standard coding tasks

**gpt-5.1-codex-mini** (Faster, lighter)
- Variants: `medium`, `high`
- Use case: Quick fixes, snippets

**gpt-5.1** (General purpose)
- Variants: `none`, `low`, `medium`, `high`
- Use case: Mixed coding and documentation

## Usage Examples

### Modern OpenCode (v1.0.210+)

```bash
# Basic usage with model and variant
opencode run "write hello world to test.txt" \
  --model=openai/gpt-5.2 \
  --variant=medium

# Use Codex-specialized model
opencode run "refactor this function for performance" \
  --model=openai/gpt-5.2-codex \
  --variant=high

# File operations with multimodal input
opencode run "analyze this image and extract data" \
  --model=openai/gpt-5.2 \
  --variant=medium \
  --input=screenshot.png

# Maximum quality for complex tasks
opencode run "implement OAuth2 flow with PKCE" \
  --model=openai/gpt-5.1-codex-max \
  --variant=xhigh
```

### Legacy OpenCode (v1.0.209 and below)

```bash
# Model name includes variant suffix
opencode run "write hello world to test.txt" \
  --model=openai/gpt-5.2-medium

# High-quality code generation
opencode run "create REST API with Express" \
  --model=openai/gpt-5.2-codex-high

# Fast iterations
opencode run "fix syntax error in app.ts" \
  --model=openai/gpt-5.1-codex-mini-medium
```

### Interactive Mode

```bash
# Start interactive session
opencode chat --model=openai/gpt-5.2-codex --variant=medium

# In chat:
> create a TypeScript interface for a User model
> add validation methods
> generate unit tests
```

## Configuration

### Modern Config Structure (v1.0.210+)

```json
{
  "models": {
    "openai/gpt-5.2": {
      "provider": "openai",
      "model": "gpt-5.2-base",
      "apiKeyEnv": "OPENAI_SESSION_TOKEN",
      "endpoint": "https://chat.openai.com/backend-api/conversation",
      "variants": {
        "none": {"temperature": 0.3},
        "low": {"temperature": 0.5},
        "medium": {"temperature": 0.7},
        "high": {"temperature": 0.85},
        "xhigh": {"temperature": 0.95}
      },
      "capabilities": ["code", "multimodal"],
      "maxTokens": 8192
    }
  }
}
```

### Legacy Config Structure (v1.0.209-)

```json
{
  "models": {
    "openai/gpt-5.2-medium": {
      "provider": "openai",
      "model": "gpt-5.2-base",
      "apiKeyEnv": "OPENAI_SESSION_TOKEN",
      "endpoint": "https://chat.openai.com/backend-api/conversation",
      "temperature": 0.7,
      "capabilities": ["code", "multimodal"],
      "maxTokens": 8192
    }
  }
}
```

### Environment Variables

The plugin stores the OAuth session token automatically. No manual environment configuration needed.

**Token storage location:**
```
~/.opencode/auth/session.json
```

### Custom Configuration

Create or modify `~/.opencode/config.json`:

```typescript
// Add custom model preset
{
  "models": {
    "openai/my-custom-preset": {
      "provider": "openai",
      "model": "gpt-5.2-codex",
      "temperature": 0.6,
      "maxTokens": 4096,
      "topP": 0.9,
      "capabilities": ["code"]
    }
  }
}
```

## Common Patterns

### Selecting the Right Model

```bash
# Quick tasks, fast iteration → codex-mini or low variant
opencode run "add comments to this function" \
  --model=openai/gpt-5.1-codex-mini --variant=medium

# Standard development → gpt-5.2-codex medium
opencode run "implement user authentication" \
  --model=openai/gpt-5.2-codex --variant=medium

# Complex architecture → codex-max high/xhigh
opencode run "design microservices architecture" \
  --model=openai/gpt-5.1-codex-max --variant=xhigh

# Documentation/mixed → gpt-5.2 or gpt-5.1
opencode run "write API documentation" \
  --model=openai/gpt-5.2 --variant=medium
```

### Batch Operations

```bash
# Process multiple files
for file in src/*.ts; do
  opencode run "add TypeScript strict type checks to $file" \
    --model=openai/gpt-5.2-codex \
    --variant=medium
done
```

### Project Scaffolding

```bash
# Generate project structure
opencode run "create Next.js 14 project with TypeScript, Tailwind, and shadcn/ui" \
  --model=openai/gpt-5.2-codex \
  --variant=high \
  --output=./new-project
```

### Code Review

```bash
# Analyze code quality
opencode run "review this PR for security issues and best practices" \
  --model=openai/gpt-5.2-codex \
  --variant=high \
  --input=git-diff.txt
```

## TypeScript Integration

If you're building tools on top of this plugin:

```typescript
import { OpenCodeAuth } from 'opencode-openai-codex-auth';

// Initialize auth client
const auth = new OpenCodeAuth({
  configPath: '~/.opencode/config.json'
});

// Authenticate
await auth.login();

// Get session token
const token = await auth.getSessionToken();

// Make authenticated request
const response = await auth.request({
  model: 'gpt-5.2-codex',
  variant: 'medium',
  messages: [
    { role: 'user', content: 'Write a TypeScript function' }
  ]
});

// Refresh token if expired
if (auth.isTokenExpired()) {
  await auth.refresh();
}

// Logout
await auth.logout();
```

## Troubleshooting

### Authentication Issues

**Problem:** `opencode auth login` fails or times out

```bash
# Clear auth cache
rm -rf ~/.opencode/auth/

# Re-authenticate
opencode auth login

# Check for browser issues
opencode auth login --debug
```

**Problem:** "Invalid session token" error

```bash
# Refresh token
opencode auth refresh

# If refresh fails, re-login
opencode auth logout
opencode auth login
```

### Model Access Issues

**Problem:** "Model not available" error

- Verify ChatGPT Plus/Pro subscription is active
- Check model name matches exactly (case-sensitive)
- Ensure using correct variant syntax for your OpenCode version

```bash
# Modern (v1.0.210+)
--model=openai/gpt-5.2 --variant=medium

# Legacy (v1.0.209-)
--model=openai/gpt-5.2-medium
```

**Problem:** Rate limiting or quota errors

- ChatGPT subscriptions have usage limits
- Wait 1-2 hours and retry
- Use lower variants (`low`, `medium`) for less resource-intensive tasks
- Switch to `codex-mini` for quick iterations

### Configuration Issues

**Problem:** Config not loading

```bash
# Verify config exists
cat ~/.opencode/config.json

# Reinstall with correct version flag
npx -y opencode-openai-codex-auth@latest  # modern
npx -y opencode-openai-codex-auth@latest --legacy  # legacy

# Check OpenCode version
opencode --version
```

**Problem:** Wrong config format

```bash
# Check OpenCode version
opencode --version

# If v1.0.210+ but using legacy config:
npx -y opencode-openai-codex-auth@latest

# If v1.0.209- but using modern config:
npx -y opencode-openai-codex-auth@latest --legacy
```

### Performance Issues

**Problem:** Slow responses

- Use lower variants (`low`, `medium`) instead of `xhigh`
- Switch to `codex-mini` for simpler tasks
- Check network connection
- Verify ChatGPT service status

**Problem:** Timeouts

```bash
# Increase timeout in config
{
  "timeout": 120000,  // 2 minutes
  "retries": 3
}
```

### Debug Mode

```bash
# Enable verbose logging
export OPENCODE_DEBUG=1
opencode run "test command" --model=openai/gpt-5.2 --variant=medium

# Check logs
tail -f ~/.opencode/logs/debug.log
```

## Best Practices

1. **Use appropriate variants:** Start with `medium`, scale up only when needed
2. **Model selection:** Use `codex` variants for pure code tasks, general models for mixed content
3. **Token management:** Auth tokens auto-refresh, but monitor session expiry
4. **Rate limiting:** Respect ChatGPT usage limits; avoid rapid-fire requests
5. **Version compatibility:** Match plugin config to your OpenCode version
6. **Security:** Never commit `~/.opencode/auth/` directory; tokens are sensitive

## Additional Resources

- Official Docs: https://numman-ali.github.io/opencode-openai-codex-auth/
- Configuration Guide: `docs/configuration.md`
- Architecture: `docs/development/ARCHITECTURE.md`
- Troubleshooting: `docs/troubleshooting.md`
- GitHub Issues: https://github.com/numman-ali/opencode-openai-codex-auth/issues
