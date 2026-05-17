---
name: codex-lb-load-balancer
description: ChatGPT/Codex multi-account load balancer with usage tracking, API key management, and OpenAI-compatible proxy
triggers:
  - set up codex load balancer for multiple accounts
  - configure chatgpt account pooling
  - track openai api usage across accounts
  - manage api keys with rate limits
  - deploy codex-lb with docker
  - balance load across multiple chatgpt accounts
  - set up openai compatible proxy
  - monitor chatgpt usage and costs
---

# codex-lb Load Balancer

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

**codex-lb** is a load balancer and proxy for ChatGPT/Codex accounts that pools multiple OpenAI accounts, tracks usage per account and API key, enforces rate limits, and provides a web dashboard for management. It exposes OpenAI-compatible endpoints (`/v1/*` and `/backend-api/codex/*`) for any client (Codex CLI, OpenCode, OpenClaw, OpenAI SDK).

**Key features:**
- Pool multiple ChatGPT accounts with automatic load balancing
- Per-account usage tracking (tokens, cost, 28-day trends)
- API key management with per-key rate limits (token, cost, time window, model)
- Dashboard with password + optional TOTP authentication
- Auto-sync available models from upstream
- WebSocket support for native Codex streaming

## Installation

### Docker (Recommended)

```bash
docker volume create codex-lb-data
docker run -d --name codex-lb \
  -p 2455:2455 -p 1455:1455 \
  -v codex-lb-data:/var/lib/codex-lb \
  ghcr.io/soju06/codex-lb:latest
```

### uvx (Python)

```bash
uvx codex-lb
```

Dashboard: [http://localhost:2455](http://localhost:2455)  
Proxy endpoints:
- OpenAI v1: `http://localhost:2455/v1`
- Codex backend: `http://localhost:2455/backend-api/codex`

Health check: `http://localhost:1455/health`

## Configuration

### First-Run Setup (Remote Access)

When accessing the dashboard remotely for the first time, you need a bootstrap token to set the password.

**Auto-generated token** (default):

```bash
docker logs codex-lb
# Look for:
# ============================================
#   Dashboard bootstrap token (first-run):
#   <token>
# ============================================
```

Open dashboard → enter token + new password → done.

**Manual bootstrap token:**

```bash
docker run -d --name codex-lb \
  -e CODEX_LB_DASHBOARD_BOOTSTRAP_TOKEN=your-secret-token \
  -p 2455:2455 -p 1455:1455 \
  -v codex-lb-data:/var/lib/codex-lb \
  ghcr.io/soju06/codex-lb:latest
```

**Local access** (localhost) bypasses bootstrap entirely.

### Adding Accounts

1. Open dashboard → **Accounts** → **Add Account**
2. Paste OpenAI session token or login credentials
3. Account syncs available models automatically

### API Key Authentication

API key auth is **disabled by default**. Enable in **Settings → API Key Auth** when:
- Clients connect remotely
- Running in Docker/VM/container with non-local networking

When enabled, clients must pass a Bearer token:

```http
Authorization: Bearer sk-clb-YOUR_KEY_HERE
```

Create API keys in dashboard → **API Keys** → **Create Key**.

Configure rate limits per key:
- Token limit (per window)
- Cost limit (USD, per window)
- Time window (e.g., 1 hour, 1 day)
- Allowed models

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `CODEX_LB_DASHBOARD_BOOTSTRAP_TOKEN` | auto-generated | Bootstrap token for first-run password setup |
| `CODEX_LB_UPSTREAM_STREAM_TRANSPORT` | `auto` | `auto`, `websocket`, or `http` for Codex streaming |
| `CODEX_LB_UPSTREAM_WEBSOCKET_TRUST_ENV` | `false` | Use environment proxies for WebSocket handshakes |
| `CODEX_LB_DATA_DIR` | `/var/lib/codex-lb` | Data directory for SQLite DB and state |

## Client Configuration

### Codex CLI

`~/.codex/config.toml`:

```toml
model = "gpt-5.3-codex"
model_reasoning_effort = "xhigh"
model_provider = "codex-lb"

[model_providers.codex-lb]
name = "OpenAI"
base_url = "http://127.0.0.1:2455/backend-api/codex"
wire_api = "responses"
supports_websockets = true
requires_openai_auth = true
```

**With API key auth:**

```toml
[model_providers.codex-lb]
name = "OpenAI"
base_url = "http://127.0.0.1:2455/backend-api/codex"
wire_api = "responses"
env_key = "CODEX_LB_API_KEY"
supports_websockets = true
requires_openai_auth = true
```

```bash
export CODEX_LB_API_KEY="sk-clb-..."
codex
```

**Enable native WebSocket streaming:**

```bash
export CODEX_LB_UPSTREAM_STREAM_TRANSPORT=websocket
```

**Verify WebSocket transport:**

```bash
RUST_LOG=debug codex exec "Reply with OK only."
```

Healthy signals:
- CLI logs: `connecting to websocket`, `successfully connected to websocket`
- codex-lb logs: `WebSocket /backend-api/codex/responses`
- No fallback `POST /backend-api/codex/responses`

**Migrate existing sessions from OpenAI provider:**

```bash
# JSONL session files
find ~/.codex/sessions -name '*.jsonl' \
  -exec sed -i '' 's/"model_provider":"openai"/"model_provider":"codex-lb"/g' {} +

# SQLite state DB (>= v0.105.0)
sqlite3 ~/.codex/state_5.sqlite \
  "UPDATE threads SET model_provider = 'codex-lb' WHERE model_provider = 'openai';"
```

### OpenCode

**Important:** Use the built-in `openai` provider with `baseURL` override. Custom providers with `@ai-sdk/openai-compatible` drop reasoning content.

Clear existing OpenAI credentials:

```bash
jq 'del(.openai)' ~/.local/share/opencode/auth.json > auth.json.tmp && mv auth.json.tmp ~/.local/share/opencode/auth.json
```

`~/.config/opencode/opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "openai": {
      "options": {
        "baseURL": "http://127.0.0.1:2455/v1",
        "apiKey": "{env:CODEX_LB_API_KEY}"
      },
      "models": {
        "gpt-5.4": {
          "name": "GPT-5.4",
          "reasoning": true,
          "options": { "reasoningEffort": "high", "reasoningSummary": "detailed" },
          "limit": { "context": 1050000, "output": 128000 }
        },
        "gpt-5.3-codex": {
          "name": "GPT-5.3 Codex",
          "reasoning": true,
          "options": { "reasoningEffort": "high", "reasoningSummary": "detailed" },
          "limit": { "context": 272000, "output": 65536 }
        }
      }
    }
  },
  "model": "openai/gpt-5.3-codex"
}
```

```bash
export CODEX_LB_API_KEY="sk-clb-..."
opencode
```

### OpenClaw

`~/.openclaw/openclaw.json`:

```json
{
  "agents": {
    "defaults": {
      "model": { "primary": "codex-lb/gpt-5.4" },
      "models": {
        "codex-lb/gpt-5.4": { "params": { "cacheRetention": "short" } },
        "codex-lb/gpt-5.3-codex": { "params": { "cacheRetention": "short" } }
      }
    }
  },
  "models": {
    "mode": "merge",
    "providers": {
      "codex-lb": {
        "baseUrl": "http://127.0.0.1:2455/v1",
        "apiKey": "${CODEX_LB_API_KEY}",
        "api": "openai-responses",
        "models": [
          {
            "id": "gpt-5.4",
            "name": "gpt-5.4 (codex-lb)",
            "contextWindow": 1050000,
            "contextTokens": 272000,
            "maxTokens": 4096,
            "input": ["text"],
            "reasoning": false
          },
          {
            "id": "gpt-5.3-codex",
            "name": "gpt-5.3-codex (codex-lb)",
            "contextWindow": 400000,
            "contextTokens": 272000,
            "maxTokens": 4096,
            "input": ["text"],
            "reasoning": false
          }
        ]
      }
    }
  }
}
```

```bash
export CODEX_LB_API_KEY="sk-clb-..."
```

### OpenAI Python SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:2455/v1",
    api_key=os.environ["CODEX_LB_API_KEY"],  # or "dummy" if auth disabled
)

response = client.chat.completions.create(
    model="gpt-5.3-codex",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

### Any OpenAI-Compatible Client

Point the base URL to:
- Chat Completions API: `http://127.0.0.1:2455/v1`
- Codex Backend API: `http://127.0.0.1:2455/backend-api/codex`

Pass API key as `Authorization: Bearer sk-clb-...` header if auth is enabled.

## Usage Patterns

### Multi-Account Load Balancing

codex-lb automatically distributes requests across healthy accounts based on:
- Account availability
- Usage limits
- Model availability per account

Add accounts in dashboard → **Accounts** → **Add Account**. Disable individual accounts temporarily without removing them.

### Rate Limiting

Configure per-API-key limits in dashboard → **API Keys** → **Edit Key**:

**Token limit:**
```
Max tokens: 100000
Window: 1 hour
```

**Cost limit:**
```
Max cost: 5.00 USD
Window: 1 day
```

**Model restrictions:**
```
Allowed models: gpt-5.3-codex, gpt-5.4-mini
```

### Usage Tracking

Dashboard → **Accounts** shows per-account:
- Total tokens used
- Total cost (USD)
- 28-day usage trends
- Model availability

Dashboard → **API Keys** shows per-key:
- Requests made
- Tokens consumed
- Cost incurred
- Rate limit status

### WebSocket Streaming (Codex)

codex-lb supports native WebSocket streaming for Codex CLI:

**Auto mode (default):**
```bash
# Uses WebSocket for native Codex headers or preferred models
# Falls back to HTTP for others
```

**Force WebSocket:**
```bash
export CODEX_LB_UPSTREAM_STREAM_TRANSPORT=websocket
```

**Force HTTP:**
```bash
export CODEX_LB_UPSTREAM_STREAM_TRANSPORT=http
```

**Reverse proxy setup** — ensure your reverse proxy forwards WebSocket upgrades:

**nginx:**
```nginx
location / {
    proxy_pass http://codex-lb:2455;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
}
```

**Caddy:**
```
reverse_proxy localhost:2455
```

(Caddy handles WebSockets automatically)

## Troubleshooting

### Bootstrap token not working

- **Local access:** No token needed for localhost. Access dashboard directly.
- **Remote access:** Check logs for auto-generated token:
  ```bash
  docker logs codex-lb | grep "bootstrap token"
  ```
- **Token used:** Bootstrap token is one-time. If password is already set, log in with password.

### API key rejected

- **Auth disabled:** Set `Authorization: Bearer dummy` or any non-empty string. If remote request is rejected, enable API key auth in dashboard.
- **Auth enabled:** Create API key in dashboard → **API Keys**. Pass as `Authorization: Bearer sk-clb-...`.
- **Rate limit:** Check dashboard → **API Keys** for limit status. Increase limits or wait for window reset.

### WebSocket connection fails (Codex)

- **Verify transport:** Run `RUST_LOG=debug codex exec "test"` and check logs for `connecting to websocket`.
- **Reverse proxy:** Ensure proxy forwards WebSocket upgrades (see nginx/Caddy examples above).
- **Direct connection:** Set `CODEX_LB_UPSTREAM_WEBSOCKET_TRUST_ENV=false` to bypass environment proxies.
- **Fallback to HTTP:** codex-lb automatically falls back. Check logs for `POST /backend-api/codex/responses` instead of `WebSocket`.

### Account sync fails

- **Invalid credentials:** Re-add account with fresh session token.
- **OpenAI API changes:** Update codex-lb to latest version:
  ```bash
  docker pull ghcr.io/soju06/codex-lb:latest
  docker restart codex-lb
  ```
- **Model availability:** Some models may not be available on all accounts. Check dashboard → **Accounts** → **Models**.

### Usage not tracking

- **Check logs:** Look for errors in request processing.
- **Database corruption:** Backup and recreate volume:
  ```bash
  docker stop codex-lb
  docker volume create codex-lb-data-backup
  docker run --rm -v codex-lb-data:/from -v codex-lb-data-backup:/to alpine sh -c "cp -av /from/. /to"
  docker volume rm codex-lb-data
  docker volume create codex-lb-data
  docker start codex-lb
  ```

### Codex sessions not appearing after migration

Run migration commands to update `model_provider` in session files and SQLite DB:

```bash
# JSONL sessions
find ~/.codex/sessions -name '*.jsonl' \
  -exec sed -i '' 's/"model_provider":"openai"/"model_provider":"codex-lb"/g' {} +

# SQLite state DB
sqlite3 ~/.codex/state_5.sqlite \
  "UPDATE threads SET model_provider = 'codex-lb' WHERE model_provider = 'openai';"
```

### Dashboard won't load

- **Port conflict:** Check if port 2455 is in use:
  ```bash
  lsof -i :2455
  docker ps
  ```
- **Change port:**
  ```bash
  docker run -d --name codex-lb -p 3000:2455 -p 1455:1455 \
    -v codex-lb-data:/var/lib/codex-lb ghcr.io/soju06/codex-lb:latest
  ```
  Access at `http://localhost:3000`.

### High latency or timeout

- **Add more accounts:** Distribute load across more ChatGPT accounts.
- **Check account health:** Dashboard → **Accounts** → disable slow or failing accounts.
- **Increase timeout:** Configure client timeout (e.g., OpenAI SDK `timeout=120`).

## Advanced Configuration

### Multi-Replica Setup

For high availability, run multiple codex-lb replicas sharing the same encryption key:

```bash
# Generate shared key
SHARED_KEY=$(openssl rand -hex 32)

# Replica 1
docker run -d --name codex-lb-1 \
  -e CODEX_LB_ENCRYPTION_KEY=$SHARED_KEY \
  -p 2455:2455 -p 1455:1455 \
  -v codex-lb-data:/var/lib/codex-lb \
  ghcr.io/soju06/codex-lb:latest

# Replica 2
docker run -d --name codex-lb-2 \
  -e CODEX_LB_ENCRYPTION_KEY=$SHARED_KEY \
  -p 2456:2455 -p 1456:1455 \
  -v codex-lb-data:/var/lib/codex-lb \
  ghcr.io/soju06/codex-lb:latest
```

Put replicas behind a load balancer (nginx, HAProxy, etc.).

### Custom Data Directory

```bash
docker run -d --name codex-lb \
  -e CODEX_LB_DATA_DIR=/custom/path \
  -v /host/custom/path:/custom/path \
  -p 2455:2455 -p 1455:1455 \
  ghcr.io/soju06/codex-lb:latest
```

### Kubernetes/Helm

See project repository for Helm chart. Key points:
- Share encryption key across pods via Secret
- Use PersistentVolumeClaim for SQLite database
- Configure Ingress for WebSocket support

## Common Patterns

### Development Team Usage

Each developer gets an API key with daily cost limit:

```python
# Team member A
client = OpenAI(
    base_url="https://codex-lb.company.com/v1",
    api_key=os.environ["DEV_A_API_KEY"],  # $10/day limit
)

# Team member B
client = OpenAI(
    base_url="https://codex-lb.company.com/v1",
    api_key=os.environ["DEV_B_API_KEY"],  # $5/day limit
)
```

Monitor usage in dashboard → **API Keys**.

### CI/CD Integration

Separate API key for CI with token limit:

```yaml
# .github/workflows/test.yml
- name: Run AI tests
  env:
    CODEX_LB_API_KEY: ${{ secrets.CI_CODEX_KEY }}  # 50k tokens/hour
  run: |
    pytest tests/ai/
```

### Model-Specific Routing

Restrict expensive models to specific keys:

**Production key:** `gpt-5.4`, `gpt-5.3-codex` allowed, $50/day  
**Development key:** `gpt-5.4-mini`, `gpt-5.1-codex-mini` allowed, $10/day

Configure in dashboard → **API Keys** → **Allowed Models**.

---

This skill enables AI coding agents to help developers deploy, configure, and troubleshoot codex-lb for managing multiple ChatGPT/Codex accounts with load balancing, usage tracking, and rate limiting.
