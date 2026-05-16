---
name: codex-manager-rust
description: A Codex CLI account manager with local gateway forwarding for managing multiple Codex accounts, usage tracking, and OpenAI-compatible API gateway
triggers:
  - how do I manage multiple Codex accounts
  - set up Codex Manager gateway
  - configure platform keys for Codex
  - import Codex accounts from JSON
  - manage Codex CLI account pool
  - set up local Codex API gateway
  - track Codex usage quotas
  - configure ccswitch with Codex Manager
---

# Codex Manager Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

Codex Manager is a Rust-based account pool manager and local gateway for Codex CLI. It provides:

- **Account Pool Management**: Import, organize, and track multiple Codex accounts with usage quotas
- **Platform Key Management**: Generate and manage API keys bound to specific models and inference levels
- **Local Gateway**: OpenAI-compatible API gateway for Codex CLI, Gemini CLI, Claude Code, and third-party tools
- **Usage Tracking**: Monitor 5-hour + 7-day windows, Code Review, Spark quotas, and reset times
- **Plugin System**: Extensible Rhai-based plugin architecture with built-in and custom markets
- **Aggregation API**: Manage third-party upstream forwarding for Codex/Claude classification

## Installation

### Desktop (Recommended)

Download the latest release for your platform:

- **Windows**: `codexmanager_<version>_x64_en-US.msi`
- **macOS**: `codexmanager_<version>_x64.dmg` or `codexmanager_<version>_aarch64.dmg`
- **Linux**: `codexmanager_<version>_amd64.AppImage` or `.deb`

### Service Mode (Headless)

```bash
# Download service binaries
wget https://github.com/qxcnm/Codex-Manager/releases/latest/download/codexmanager-service
wget https://github.com/qxcnm/Codex-Manager/releases/latest/download/codexmanager-web
wget https://github.com/qxcnm/Codex-Manager/releases/latest/download/codexmanager-start

chmod +x codexmanager-*

# Start service + web
./codexmanager-start
```

### Docker

```bash
docker pull qxcnm/codexmanager:latest

docker run -d \
  -p 3000:3000 \
  -p 8787:8787 \
  -v ./data:/app/data \
  -e CODEX_MANAGER_PORT=3000 \
  -e CODEX_MANAGER_WEB_PORT=8787 \
  qxcnm/codexmanager:latest
```

## Configuration

### Data Directory

Default database locations:

- **Windows**: `%APPDATA%\com.codexmanager.desktop\codexmanager.db`
- **macOS**: `~/Library/Application Support/com.codexmanager.desktop/codexmanager.db`
- **Linux**: `~/.local/share/com.codexmanager.desktop/codexmanager.db`

### Environment Variables

```bash
# Core settings
export CODEX_MANAGER_PORT=3000              # Service port
export CODEX_MANAGER_LISTEN=0.0.0.0         # Listen address
export CODEX_MANAGER_DATABASE_URL=sqlite:///path/to/codexmanager.db

# Proxy configuration
export CODEX_MANAGER_PROXY=http://127.0.0.1:7890

# Timeout settings
export CODEX_MANAGER_REQUEST_TIMEOUT=300    # Total request timeout (seconds)
export CODEX_MANAGER_STREAM_IDLE_TIMEOUT=60 # SSE idle timeout (seconds)
export CODEX_MANAGER_SSE_KEEPALIVE=15       # SSE keepalive interval (seconds)

# Web security
export CODEX_MANAGER_WEB_PASSWORD=your_secure_password
export CODEX_MANAGER_WEB_PORT=8787

# Concurrency
export CODEX_MANAGER_MAX_CONCURRENT_PER_ACCOUNT=3
```

### Configuration File (config.toml)

```toml
[server]
port = 3000
listen = "0.0.0.0"
proxy = "http://127.0.0.1:7890"

[database]
url = "sqlite:///path/to/codexmanager.db"

[timeout]
request = 300
stream_idle = 60
sse_keepalive = 15

[concurrency]
max_per_account = 3

[web]
port = 8787
password = "your_secure_password"
```

## Codex CLI Integration (ccswitch)

### Setup auth.json

Create `~/.codex/auth.json`:

```json
{
  "default_host": "http://127.0.0.1:3000",
  "hosts": {
    "http://127.0.0.1:3000": {
      "access_token": "your-platform-key-from-codexmanager"
    }
  }
}
```

### Setup config.toml

Create `~/.codex/config.toml`:

```toml
[client]
host = "http://127.0.0.1:3000"
```

### Verify Connection

```bash
# Test with ccswitch
ccswitch list

# Or direct curl
curl http://127.0.0.1:3000/v1/models \
  -H "Authorization: Bearer your-platform-key"
```

## Account Management

### Import Accounts

**Desktop**: Navigate to "Account Management" → "Import Accounts"

**API** (for automation):

```bash
curl -X POST http://127.0.0.1:3000/api/accounts/import \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}" \
  -d '{
    "accounts": [
      {
        "email": "user@example.com",
        "access_token": "sess-...",
        "session_token": "eyJhbGc...",
        "group": "default",
        "tags": ["prod", "high-quota"]
      }
    ]
  }'
```

### Refresh Usage

```bash
# Refresh all accounts
curl -X POST http://127.0.0.1:3000/api/accounts/refresh-all \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}"

# Refresh specific account
curl -X POST http://127.0.0.1:3000/api/accounts/{account_id}/refresh \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}"
```

### Export Accounts

```bash
# Export all accounts
curl http://127.0.0.1:3000/api/accounts/export \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}" \
  -o accounts_export.json

# Export by group
curl "http://127.0.0.1:3000/api/accounts/export?group=production" \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}" \
  -o prod_accounts.json
```

## Platform Key Management

### Create Platform Key

```bash
curl -X POST http://127.0.0.1:3000/api/platform-keys \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}" \
  -d '{
    "name": "production-key",
    "key": "sk-custom-key-or-leave-empty-for-random",
    "models": ["gpt-4", "claude-3-opus-20240229"],
    "inference_level": "high",
    "service_level": "fast",
    "enabled": true
  }'
```

### List Platform Keys

```bash
curl http://127.0.0.1:3000/api/platform-keys \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}"
```

### Bind Models

```bash
curl -X PATCH http://127.0.0.1:3000/api/platform-keys/{key_id} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}" \
  -d '{
    "models": ["gpt-4o", "claude-3-5-sonnet-20241022"],
    "inference_level": "medium"
  }'
```

## Gateway Usage

### OpenAI-Compatible Endpoint

```bash
# Chat completions
curl http://127.0.0.1:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-platform-key" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "stream": true
  }'

# Image generation
curl http://127.0.0.1:3000/v1/images/generations \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-platform-key" \
  -d '{
    "model": "gpt-image-2",
    "prompt": "A futuristic cityscape",
    "n": 1,
    "size": "1024x1024"
  }'
```

### Gemini Forwarding

```bash
# Gemini requests auto-forward to /v1/responses
curl http://127.0.0.1:3000/v1/responses \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-platform-key" \
  -d '{
    "model": "gemini-2.0-flash",
    "messages": [
      {"role": "user", "content": "Explain quantum computing"}
    ]
  }'
```

### With Tools/MCP

```bash
curl http://127.0.0.1:3000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-platform-key" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "user", "content": "Generate an image of a sunset"}
    ],
    "tools": [
      {
        "type": "function",
        "function": {
          "name": "image_generation",
          "description": "Generate images",
          "parameters": {
            "type": "object",
            "properties": {
              "prompt": {"type": "string"}
            }
          }
        }
      }
    ]
  }'
```

## Model Management

### Sync Models

```bash
# Sync from remote
curl -X POST http://127.0.0.1:3000/api/models/sync \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}"

# Export cache (desktop auto-syncs to ~/.codex/models_cache.json)
curl http://127.0.0.1:3000/api/models/export \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}" \
  -o models_cache.json
```

### Add Custom Model

```bash
curl -X POST http://127.0.0.1:3000/api/models \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}" \
  -d '{
    "id": "custom-gpt-4",
    "name": "Custom GPT-4",
    "visibility": "public",
    "supportedInApi": true,
    "maxTokens": 8192
  }'
```

## Aggregation API

### Add Upstream

```bash
curl -X POST http://127.0.0.1:3000/api/aggregation/upstreams \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}" \
  -d '{
    "name": "VisionCoder",
    "base_url": "https://api.visioncoder.cn/v1",
    "api_key": "${VISIONCODER_API_KEY}",
    "provider": "codex",
    "priority": 1,
    "enabled": true
  }'
```

### Test Upstream

```bash
curl -X POST http://127.0.0.1:3000/api/aggregation/upstreams/{id}/test \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}"
```

## Plugin System

### Plugin Directory Structure

```
plugins/
├── manifest.json       # Plugin metadata
├── main.rhai          # Entry point
├── tasks/             # Background tasks
└── ui/                # Optional UI components
```

### Example Plugin (manifest.json)

```json
{
  "id": "account-auto-refresh",
  "name": "Auto Refresh Accounts",
  "version": "1.0.0",
  "author": "Your Name",
  "description": "Automatically refresh account usage every hour",
  "entry": "main.rhai",
  "permissions": ["accounts.read", "accounts.refresh"],
  "tasks": [
    {
      "name": "refresh-task",
      "schedule": "0 */1 * * *",
      "script": "tasks/refresh.rhai"
    }
  ]
}
```

### Example Plugin (main.rhai)

```rust
// Access system API via Rhai built-ins
fn on_install() {
    log_info("Plugin installed");
    
    // Get all accounts
    let accounts = system_call("accounts.list", #{});
    log_info(`Found ${accounts.len()} accounts`);
}

fn on_enable() {
    log_info("Plugin enabled");
}

fn on_task_run(task_name) {
    if task_name == "refresh-task" {
        let accounts = system_call("accounts.list", #{});
        
        for account in accounts {
            if account.enabled {
                system_call("accounts.refresh", #{
                    id: account.id
                });
                log_info(`Refreshed account: ${account.email}`);
            }
        }
    }
}
```

### Install Plugin

```bash
# Via API
curl -X POST http://127.0.0.1:3000/api/plugins/install \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}" \
  -d '{
    "source": "file:///path/to/plugin",
    "market": "custom"
  }'
```

## Common Patterns

### Account Rotation Strategy

```rust
// Rust service-side logic (for reference)
use codexmanager::{AccountPool, SelectionStrategy};

let pool = AccountPool::new(db).await?;

// Select by lowest usage
let account = pool.select_account(SelectionStrategy::LowestUsage {
    model: "gpt-4o",
    inference_level: "high",
}).await?;

// Select by round-robin
let account = pool.select_account(SelectionStrategy::RoundRobin {
    group: "production",
}).await?;
```

### Rate Limiting

```bash
# Set per-account concurrency
curl -X PATCH http://127.0.0.1:3000/api/settings \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}" \
  -d '{
    "max_concurrent_per_account": 2,
    "enable_conservative_backoff": true
  }'
```

### Health Check

```bash
# Check service health
curl http://127.0.0.1:3000/health

# Check account pool status
curl http://127.0.0.1:3000/api/accounts/stats \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}"
```

## Troubleshooting

### Service Won't Start

```bash
# Check port availability
netstat -an | grep 3000

# Check logs (desktop)
# Windows: %APPDATA%\com.codexmanager.desktop\logs
# macOS: ~/Library/Logs/com.codexmanager.desktop
# Linux: ~/.local/share/com.codexmanager.desktop/logs

# Check logs (service)
./codexmanager-service --log-level debug
```

### Accounts Not Matching

```bash
# Check account hit rules
curl http://127.0.0.1:3000/api/accounts/debug-match \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}" \
  -d '{
    "model": "gpt-4o",
    "inference_level": "high"
  }'
```

### Challenge Interception

If accounts are flagged with challenge/captcha:

1. Check proxy configuration: `CODEX_MANAGER_PROXY`
2. Reduce concurrency: `max_concurrent_per_account`
3. Enable conservative backoff in settings
4. Manually re-authorize affected accounts via browser

### Model Cache Not Syncing

```bash
# Force sync to ~/.codex/models_cache.json
curl -X POST http://127.0.0.1:3000/api/models/sync-local \
  -H "Authorization: Bearer ${CODEX_MANAGER_API_KEY}"

# Verify cache location
cat ~/.codex/models_cache.json
```

### macOS Gatekeeper Block

```bash
# Allow unsigned app
xattr -dr com.apple.quarantine /Applications/codexmanager.app

# Or use System Preferences → Security & Privacy → Allow
```

### Database Locked

```bash
# Stop all instances
pkill codexmanager

# Remove lock file (if exists)
rm ~/.local/share/com.codexmanager.desktop/codexmanager.db-wal
rm ~/.local/share/com.codexmanager.desktop/codexmanager.db-shm

# Restart service
./codexmanager-start
```

## Additional Resources

- [Full Documentation](https://github.com/qxcnm/Codex-Manager/tree/main/docs/zh-CN)
- [Deployment Guide](https://github.com/qxcnm/Codex-Manager/blob/main/docs/zh-CN/report/运行与部署指南.md)
- [Environment Variables Reference](https://github.com/qxcnm/Codex-Manager/blob/main/docs/zh-CN/report/环境变量与运行配置说明.md)
- [Plugin Development](https://github.com/qxcnm/Codex-Manager/blob/main/docs/zh-CN/report/插件中心对接与接口清单.md)
- [Internal API Reference](https://github.com/qxcnm/Codex-Manager/blob/main/docs/zh-CN/report/系统内部接口总表.md)
