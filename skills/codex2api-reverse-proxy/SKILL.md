---
name: codex2api-reverse-proxy
description: Codex2API is a production-ready reverse proxy that converts Codex account pools into OpenAI/Anthropic-compatible API gateways with account management, scheduling, and admin dashboard.
triggers:
  - set up codex2api proxy server
  - configure codex account pool gateway
  - deploy openai compatible codex proxy
  - manage codex refresh tokens with api
  - create anthropic compatible codex endpoint
  - configure codex2api with postgresql redis
  - troubleshoot codex2api account scheduler
  - use codex2api admin dashboard
---

# Codex2API Reverse Proxy

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Codex2API is a Go + Gin + React production gateway that transforms a pool of Codex accounts into observable, schedulable OpenAI/Anthropic-compatible API endpoints. It manages Refresh Token/Access Token lifecycles, health scoring, dynamic concurrency, rate-limit recovery, usage tracking, and admin operations through a built-in dashboard.

## What It Does

- **Unified Gateway**: Exposes `/v1/chat/completions`, `/v1/responses`, `/v1/messages`, `/v1/images/generations`, `/v1/images/edits`, and `/v1/models` endpoints
- **Account Pool Management**: Handles Refresh Tokens and Access Tokens with automatic health scoring and cooldown recovery
- **Dynamic Scheduling**: Selects accounts based on health tier, concurrency limits, rate limits, and recent usage
- **Admin Dashboard**: React/Vite UI for account import, API key management, proxy pools, image studio, prompt filtering, usage analytics
- **Flexible Storage**: Production mode (PostgreSQL + Redis) or lightweight mode (SQLite + in-memory cache)

## Installation

### Standard Production Deployment (PostgreSQL + Redis)

```bash
git clone https://github.com/james-6-23/codex2api.git
cd codex2api
cp .env.example .env
# Edit .env with your DATABASE_* and REDIS_* settings
docker compose pull
docker compose up -d
docker compose logs -f codex2api
```

### Lightweight SQLite Deployment

```bash
git clone https://github.com/james-6-23/codex2api.git
cd codex2api
cp .env.sqlite.example .env
# Edit .env if needed
docker compose -f docker-compose.sqlite.yml pull
docker compose -f docker-compose.sqlite.yml up -d
docker compose -f docker-compose.sqlite.yml logs -f codex2api
```

### Local Development

```bash
cp .env.example .env
# Start PostgreSQL and Redis containers or configure local instances
cd frontend && npm ci && npm run build && cd ..
go run .
```

Frontend dev server:

```bash
cd frontend && npm ci && npm run dev
# Frontend runs at http://localhost:5173/admin/
```

## Configuration

### Environment Variables (.env)

**Server:**
```bash
CODEX_PORT=8080
ADMIN_SECRET=your-secure-admin-password
TZ=Asia/Shanghai
```

**PostgreSQL Mode:**
```bash
DATABASE_DRIVER=postgres
DATABASE_HOST=localhost
DATABASE_PORT=5432
DATABASE_USER=codex2api
DATABASE_PASSWORD=secure-db-password
DATABASE_NAME=codex2api
DATABASE_SSLMODE=disable

CACHE_DRIVER=redis
REDIS_ADDR=localhost:6379
REDIS_PASSWORD=secure-redis-password
REDIS_DB=0
```

**SQLite Mode:**
```bash
DATABASE_DRIVER=sqlite
DATABASE_PATH=/data/codex2api.db
CACHE_DRIVER=memory
```

**Redis TLS (Aiven, Upstash, etc.):**
```bash
# Prefer rediss:// URL format
REDIS_ADDR=rediss://default:password@host:port/0

# OR for host:port format
REDIS_ADDR=host:port
REDIS_TLS=true
REDIS_INSECURE_SKIP_VERIFY=false  # Set true only for self-signed certs
REDIS_USERNAME=default
REDIS_PASSWORD=your-password
```

### Runtime Settings (Database)

After first startup, configure via admin dashboard at `/admin/settings`:

- `MaxConcurrency`: Global concurrent request limit
- `GlobalRPM`: Global requests per minute
- `TestModel`: Model for account health checks
- `TestConcurrency`: Test request concurrency
- `ProxyURL`: Global proxy (e.g., `http://proxy:port`)
- `PgMaxConns`: PostgreSQL connection pool size
- `RedisPoolSize`: Redis connection pool size
- Auto-cleanup settings for logs and usage records

## API Usage

### OpenAI Chat Completions

```go
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/sashabaranov/go-openai"
)

func main() {
	config := openai.DefaultConfig(os.Getenv("CODEX2API_KEY"))
	config.BaseURL = "http://localhost:8080/v1"
	client := openai.NewClientWithConfig(config)

	resp, err := client.CreateChatCompletion(
		context.Background(),
		openai.ChatCompletionRequest{
			Model: "claude-code",
			Messages: []openai.ChatCompletionMessage{
				{
					Role:    openai.ChatMessageRoleUser,
					Content: "Explain how Codex2API account scheduling works",
				},
			},
		},
	)
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	fmt.Println(resp.Choices[0].Message.Content)
}
```

### Anthropic Messages (Compatible Endpoint)

```python
import os
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ.get("CODEX2API_KEY"),
    base_url="http://localhost:8080/v1"
)

message = client.messages.create(
    model="claude-code",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain dynamic concurrency in Codex2API"}
    ]
)

print(message.content[0].text)
```

### Native Codex Responses

```bash
curl -X POST http://localhost:8080/v1/responses \
  -H "Authorization: Bearer $CODEX2API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-code",
    "messages": [
      {
        "role": "user",
        "content": "Write a hello world in Go"
      }
    ],
    "stream": false
  }'
```

### Image Generation

```bash
curl -X POST http://localhost:8080/v1/images/generations \
  -H "Authorization: Bearer $CODEX2API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "A serene mountain landscape at sunset",
    "model": "gemini-2.0-flash-exp-image",
    "n": 1,
    "size": "1024x1024"
  }'
```

### Image Editing

```bash
curl -X POST http://localhost:8080/v1/images/edits \
  -H "Authorization: Bearer $CODEX2API_KEY" \
  -F "image=@original.png" \
  -F "prompt=Add a rainbow in the sky" \
  -F "model=gemini-2.0-flash-exp-image" \
  -F "n=1"
```

### List Models

```bash
curl http://localhost:8080/v1/models \
  -H "Authorization: Bearer $CODEX2API_KEY"
```

## Account Management API

### Upload Refresh Tokens

```bash
curl -X POST http://localhost:8080/api/admin/accounts/upload \
  -H "X-Admin-Key: $ADMIN_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "tokens": [
      "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
      "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
    ]
  }'
```

### Upload Access Tokens

```bash
curl -X POST http://localhost:8080/api/admin/accounts/upload \
  -H "X-Admin-Key: $ADMIN_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "tokens": [
      "sess-abc123...",
      "sess-def456..."
    ],
    "type": "access_token"
  }'
```

### Test Account Health

```bash
# Test all accounts
curl -X POST http://localhost:8080/api/admin/accounts/test \
  -H "X-Admin-Key: $ADMIN_SECRET"

# Test specific account
curl -X POST http://localhost:8080/api/admin/accounts/test \
  -H "X-Admin-Key: $ADMIN_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"account_id": "550e8400-e29b-41d4-a716-446655440000"}'
```

### List Accounts

```bash
curl http://localhost:8080/api/admin/accounts \
  -H "X-Admin-Key: $ADMIN_SECRET"
```

### Delete Account

```bash
curl -X DELETE http://localhost:8080/api/admin/accounts/550e8400-e29b-41d4-a716-446655440000 \
  -H "X-Admin-Key: $ADMIN_SECRET"
```

## API Key Management

### Create API Key

```bash
curl -X POST http://localhost:8080/api/admin/apikeys \
  -H "X-Admin-Key: $ADMIN_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Production Client",
    "key": "sk-custom-key-123",
    "max_rpm": 100,
    "max_tpm": 50000
  }'
```

Response:
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Production Client",
  "key": "sk-custom-key-123",
  "max_rpm": 100,
  "max_tpm": 50000,
  "enabled": true,
  "created_at": "2026-05-16T10:30:00Z"
}
```

### List API Keys

```bash
curl http://localhost:8080/api/admin/apikeys \
  -H "X-Admin-Key: $ADMIN_SECRET"
```

### Disable/Enable API Key

```bash
curl -X PATCH http://localhost:8080/api/admin/apikeys/550e8400-e29b-41d4-a716-446655440000 \
  -H "X-Admin-Key: $ADMIN_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'
```

## Common Patterns

### Account Scheduler Logic

The scheduler selects accounts based on:

1. **Health Tier**: `Active` (healthy) > `Cooldown` (recovering) > `Inactive` (failed)
2. **Concurrency**: Current concurrent requests < account's max concurrency
3. **Rate Limits**: RPM (requests per minute) and TPM (tokens per minute) not exceeded
4. **Score**: Weighted by success rate, recent failures, and last success time
5. **Cooldown Recovery**: Accounts in cooldown automatically transition to Active after configured interval

```go
// Scheduler picks account with highest score among eligible candidates
// Example internal scoring (simplified):
score := (successRate * 0.5) + 
         (1.0 - recentFailureRate * 0.3) + 
         (timeSinceLastSuccess * 0.2)
```

### Health Check Workflow

```bash
# Accounts are tested with TestModel (configured in settings)
# Default: claude-code
# Test sends minimal completion request and validates response

# Health states:
# - Active: Last test succeeded, ready for requests
# - Cooldown: Recent failure, waiting for recovery
# - Inactive: Multiple consecutive failures, excluded from scheduling
```

### Proxy Configuration

Set per-account proxy:

```bash
curl -X PATCH http://localhost:8080/api/admin/accounts/550e8400-e29b-41d4-a716-446655440000 \
  -H "X-Admin-Key: $ADMIN_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"proxy_url": "http://proxy.example.com:8080"}'
```

Global proxy via settings page or environment:
```bash
# .env
PROXY_URL=http://global-proxy:8080
```

### Streaming Responses

```python
import os
import anthropic

client = anthropic.Anthropic(
    api_key=os.environ.get("CODEX2API_KEY"),
    base_url="http://localhost:8080/v1"
)

with client.messages.stream(
    model="claude-code",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Count to 10"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Prompt Filter (Block/Warn/Modify)

Configure in admin dashboard under "Prompt Filter":

```json
{
  "enabled": true,
  "rules": [
    {
      "pattern": "(?i)nuclear",
      "action": "block",
      "message": "Content violates policy"
    },
    {
      "pattern": "(?i)medical advice",
      "action": "warn",
      "message": "Consider consulting a professional"
    }
  ]
}
```

## Docker Commands

### Standard Mode

```bash
# Start
docker compose up -d

# View logs
docker compose logs -f codex2api

# Restart
docker compose restart codex2api

# Stop
docker compose down

# Update to latest
docker compose pull && docker compose up -d
```

### SQLite Mode

```bash
# Start
docker compose -f docker-compose.sqlite.yml up -d

# Logs
docker compose -f docker-compose.sqlite.yml logs -f codex2api

# Update
docker compose -f docker-compose.sqlite.yml pull
docker compose -f docker-compose.sqlite.yml up -d
```

### Backup and Restore

**PostgreSQL:**
```bash
# Backup
docker exec codex2api-postgres pg_dump -U codex2api codex2api > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore
docker exec -i codex2api-postgres psql -U codex2api codex2api < backup_20260516_103000.sql
```

**SQLite:**
```bash
# Backup (requires running container)
docker exec codex2api sqlite3 /data/codex2api.db ".backup /data/backup_$(date +%Y%m%d_%H%M%S).db"

# Or copy from host (if /data is mounted)
cp /path/to/data/codex2api.db /path/to/backup/codex2api_$(date +%Y%m%d_%H%M%S).db
```

## Troubleshooting

### No Healthy Accounts Available

**Symptom:** API returns 503 or "No available account"

**Solutions:**
1. Check account health in admin dashboard
2. Run account tests: `POST /api/admin/accounts/test`
3. Verify Refresh Tokens are valid (not expired)
4. Check cooldown settings and wait for recovery
5. Review logs for authentication failures

```bash
# Check account status
curl http://localhost:8080/api/admin/accounts \
  -H "X-Admin-Key: $ADMIN_SECRET" | jq '.[] | {id, email, status, health_tier}'

# Force test all accounts
curl -X POST http://localhost:8080/api/admin/accounts/test \
  -H "X-Admin-Key: $ADMIN_SECRET"
```

### Database Connection Failed

**PostgreSQL:**
```bash
# Test connection
docker exec codex2api-postgres pg_isready -U codex2api

# Check logs
docker logs codex2api-postgres

# Verify .env settings match docker-compose.yml
grep DATABASE_ .env
```

**SQLite:**
```bash
# Check file permissions
docker exec codex2api ls -la /data/codex2api.db

# Verify mount point
docker inspect codex2api | jq '.[0].Mounts'
```

### Redis Connection Failed

```bash
# Test Redis
docker exec codex2api-redis redis-cli ping

# Check authentication
docker exec codex2api-redis redis-cli -a "$REDIS_PASSWORD" ping

# For TLS issues with cloud Redis
# Ensure REDIS_ADDR uses rediss:// or REDIS_TLS=true
# Check REDIS_INSECURE_SKIP_VERIFY if using self-signed certs
```

### Rate Limit Exceeded

**Symptom:** 429 Too Many Requests

**Solutions:**
1. Check API key limits in admin dashboard
2. Increase `max_rpm` or `max_tpm` for the key
3. Review global `GlobalRPM` setting
4. Add more accounts to the pool
5. Verify account-level rate limits

```bash
# Update API key limits
curl -X PATCH http://localhost:8080/api/admin/apikeys/YOUR_KEY_ID \
  -H "X-Admin-Key: $ADMIN_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"max_rpm": 200, "max_tpm": 100000}'
```

### High Concurrency Blocking

**Symptom:** Requests queue or timeout during high load

**Solutions:**
1. Increase `MaxConcurrency` in settings
2. Add more healthy accounts
3. Adjust per-account concurrency limits
4. Scale horizontally (multiple Codex2API instances with shared PostgreSQL/Redis)

```bash
# Check current concurrency
curl http://localhost:8080/api/admin/stats \
  -H "X-Admin-Key: $ADMIN_SECRET" | jq '.current_concurrency'
```

### Image Generation Fails

**Common issues:**
1. Model doesn't support images (only `gemini-*-image` models work)
2. Image file format not supported (use PNG/JPEG)
3. File size exceeds limits
4. No accounts with image capability

```bash
# Verify image-capable models
curl http://localhost:8080/v1/models \
  -H "Authorization: Bearer $CODEX2API_KEY" | jq '.data[] | select(.id | contains("image"))'
```

### Admin Dashboard 401 Unauthorized

**Symptom:** Login fails or /api/admin/* returns 401

**Solutions:**
1. Verify `ADMIN_SECRET` in .env matches login password
2. Check `X-Admin-Key` header in requests
3. Restart after changing `ADMIN_SECRET`

```bash
# Check current admin secret source
docker exec codex2api env | grep ADMIN_SECRET

# Restart to apply .env changes
docker compose restart codex2api
```

### Memory or CPU Usage High

**PostgreSQL mode:**
```bash
# Reduce connection pool size in settings
# Default PgMaxConns: 25, RedisPoolSize: 10

# Monitor resource usage
docker stats codex2api codex2api-postgres codex2api-redis
```

**SQLite mode:**
```bash
# SQLite is single-threaded; for high concurrency use PostgreSQL
# Check database file size
docker exec codex2api du -h /data/codex2api.db

# Run VACUUM to reclaim space
docker exec codex2api sqlite3 /data/codex2api.db "VACUUM;"
```

## Advanced Configuration

### Custom Test Model

```bash
# Update via settings API
curl -X PATCH http://localhost:8080/api/admin/settings \
  -H "X-Admin-Key: $ADMIN_SECRET" \
  -H "Content-Type: application/json" \
  -d '{"test_model": "claude-sonnet-4"}'
```

### Auto-Cleanup Policies

Configure in admin settings:

- `AutoCleanupEnabled`: Enable automatic cleanup
- `LogRetentionDays`: Keep request logs for N days (default 30)
- `UsageRetentionDays`: Keep usage records for N days (default 90)

### Horizontal Scaling

Multiple Codex2API instances can share PostgreSQL + Redis:

```yaml
# docker-compose.yml
services:
  codex2api-1:
    image: ghcr.io/james-6-23/codex2api:latest
    environment:
      - DATABASE_HOST=postgres
      - REDIS_ADDR=redis:6379
  codex2api-2:
    image: ghcr.io/james-6-23/codex2api:latest
    environment:
      - DATABASE_HOST=postgres
      - REDIS_ADDR=redis:6379
```

Use a load balancer (nginx, Caddy, Traefik) to distribute requests.

### Health Check Endpoint

```bash
curl http://localhost:8080/health
```

Response:
```json
{
  "status": "healthy",
  "database": "ok",
  "cache": "ok",
  "timestamp": "2026-05-16T10:30:00Z"
}
```

Use in Kubernetes liveness/readiness probes or Docker healthchecks.

## Resources

- **Documentation**: [docs/](https://github.com/james-6-23/codex2api/tree/main/docs)
  - [API.md](https://github.com/james-6-23/codex2api/blob/main/docs/API.md): Full API reference
  - [DEPLOYMENT.md](https://github.com/james-6-23/codex2api/blob/main/docs/DEPLOYMENT.md): Deployment modes and upgrade guide
  - [CONFIGURATION.md](https://github.com/james-6-23/codex2api/blob/main/docs/CONFIGURATION.md): Environment variables and settings
  - [ARCHITECTURE.md](https://github.com/james-6-23/codex2api/blob/main/docs/ARCHITECTURE.md): System architecture and scheduler design
  - [TROUBLESHOOTING.md](https://github.com/james-6-23/codex2api/blob/main/docs/TROUBLESHOOTING.md): Common issues and fixes
- **Live Demo**: [https://codex2api-latest-vu8j.onrender.com](https://codex2api-latest-vu8j.onrender.com) (password: `codex2api`)
- **Repository**: [https://github.com/james-6-23/codex2api](https://github.com/james-6-23/codex2api)
