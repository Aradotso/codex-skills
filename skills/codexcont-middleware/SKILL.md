---
name: codexcont-middleware
description: Continue-thinking middleware that detects and handles reasoning truncation in Codex/OpenAI Responses-compatible APIs
triggers:
  - set up CodexCont proxy
  - configure continuation middleware
  - handle reasoning truncation
  - proxy OpenAI Codex requests
  - extend thinking limits
  - configure CodexCont authentication
  - debug truncated reasoning
  - fold streaming responses
---

# CodexCont Middleware

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

CodexCont is a Starlette-based proxy middleware that sits between coding agents and OpenAI Responses-compatible APIs. It automatically detects reasoning truncation (when `reasoning_tokens == 518 * n - 2`), silently continues the thinking process, and folds multiple upstream streaming responses into one coherent downstream response.

## Installation

### Prerequisites

- Python >= 3.12
- `uv` package manager recommended

### Setup

```bash
# Clone the repository
git clone https://github.com/neteroster/CodexCont.git
cd CodexCont

# Install dependencies
uv sync

# Copy and configure
cp config.example.toml config.toml

# Run the proxy
uv run python run.py
```

### Alternative: Direct virtual environment usage

```bash
# Windows/Git Bash
.venv/Scripts/python.exe run.py

# Linux/macOS
.venv/bin/python run.py
```

## Configuration

### Basic Configuration Structure

Edit `config.toml`:

```toml
[server]
host = "127.0.0.1"
port = 8787

[upstream]
url = "https://chatgpt.com/backend-api/codex/responses"
mode = "header"  # header | fixed

[auth]
mode = "passthrough"  # passthrough | inject | passthrough_then_inject
access_token = ""
chatgpt_account_id = ""

[continue]
enabled = true
method = "commentary"  # commentary | tool_pair
continue_tool_name = "continue_thinking"
max_rounds = 8
max_reasoning_tokens = 50000
tier_gate_low = 1
tier_gate_high = 100

[repair_followup]
mode = "off"  # off | stateless | stateful
```

### Upstream Mode

**`header` mode (recommended)**: Allows per-request upstream override via `Responses-API-Base` header:

```python
import httpx

response = httpx.post(
    "http://127.0.0.1:8787/v1/responses",
    headers={
        "Responses-API-Base": "https://api.openai.com/v1",
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
    },
    json=payload
)
```

**`fixed` mode**: Always uses the configured `upstream.url`.

### Authentication Modes

**`passthrough`**: Forward client auth headers only:

```toml
[auth]
mode = "passthrough"
```

**`inject`**: Override with configured credentials:

```toml
[auth]
mode = "inject"
access_token = "your-token-here"  # Use env vars in production
chatgpt_account_id = "org-xxxxx"
```

**`passthrough_then_inject`**: Use client auth if present, fallback to config:

```toml
[auth]
mode = "passthrough_then_inject"
access_token = "your-fallback-token"
```

**Security**: The proxy will reject requests with `Responses-API-Base` header when `inject` mode would leak configured credentials to unknown URLs.

### Continuation Methods

**`commentary` (recommended)**: Uses hidden phase commentary to continue thinking:

```toml
[continue]
method = "commentary"
```

**`tool_pair`**: Legacy mode using synthetic tool calls:

```toml
[continue]
method = "tool_pair"
continue_tool_name = "continue_thinking"
```

### Safety Limits

```toml
[continue]
max_rounds = 8                    # Maximum continuation rounds
max_reasoning_tokens = 50000       # Stop after this many reasoning tokens
tier_gate_low = 1                  # Minimum tier n to trigger continuation
tier_gate_high = 100               # Maximum tier n to continue folding
```

## Usage Examples

### Basic Proxy Client

```python
import httpx
import os
import json

async def query_with_continuation(prompt: str):
    """Query through CodexCont proxy with automatic continuation."""
    
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": True,
        "reasoning": True  # Enable reasoning to trigger continuation
    }
    
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "http://127.0.0.1:8787/v1/responses",
            headers={
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=300.0
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = line[6:]
                    if data.strip() == "[DONE]":
                        break
                    
                    event = json.loads(data)
                    
                    # Handle reasoning items
                    if event.get("type") == "response.reasoning_item.delta":
                        print(f"Reasoning: {event.get('delta', {}).get('content', '')}")
                    
                    # Handle message content
                    elif event.get("type") == "response.message.delta":
                        print(f"Output: {event.get('delta', {}).get('content', '')}")
                    
                    # Final event with metadata
                    elif event.get("type") == "response.done":
                        metadata = event.get("response", {}).get("metadata", {})
                        rounds = metadata.get("proxy_rounds", [])
                        print(f"\nCompleted in {len(rounds)} round(s)")
                        for i, r in enumerate(rounds):
                            print(f"  Round {i+1}: {r.get('reasoning_tokens')} tokens (tier {r.get('tier')})")
```

### Synchronous Client

```python
import requests
import os

def simple_query(prompt: str):
    """Simple synchronous query through proxy."""
    
    response = requests.post(
        "http://127.0.0.1:8787/v1/responses",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
        },
        json={
            "model": "gpt-4",
            "messages": [{"role": "user", "content": prompt}],
            "stream": True
        },
        stream=True
    )
    
    for line in response.iter_lines():
        if line:
            line_str = line.decode('utf-8')
            if line_str.startswith("data: "):
                data = line_str[6:]
                if data.strip() != "[DONE]":
                    print(data)
```

### Override Upstream URL

```python
import httpx
import os

async def query_different_endpoint(prompt: str):
    """Query a different Responses-compatible endpoint."""
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:8787/v1/responses",
            headers={
                "Responses-API-Base": "https://api.openai.com/v1",
                "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
            },
            json={
                "model": "gpt-4",
                "messages": [{"role": "user", "content": prompt}],
                "stream": True
            }
        )
        return response
```

### Disable Continuation for Specific Request

```python
payload = {
    "model": "gpt-4",
    "messages": [{"role": "user", "content": "Quick question"}],
    "stream": True,
    "reasoning": False  # Disables folding/continuation
}
```

## Understanding Continuation Behavior

### Truncation Detection

The middleware detects truncation when:

1. `usage.output_tokens_details.reasoning_tokens == 518 * n - 2` (for integer n)
2. Reasoning content appears encrypted/truncated
3. Token count is within tier gates (`tier_gate_low` <= n <= `tier_gate_high`)
4. Safety limits not exceeded (`max_rounds`, `max_reasoning_tokens`)

### Response Metadata

The final response includes proxy metadata:

```python
{
    "type": "response.done",
    "response": {
        "metadata": {
            "proxy_rounds": [
                {"reasoning_tokens": 516, "tier": 1},
                {"reasoning_tokens": 1034, "tier": 2}
            ],
            "proxy_billed_usage": {
                "input_tokens": 150,
                "output_tokens": 1550,
                "reasoning_tokens": 1550
            },
            "proxy_stopped_reason": "clean_finish"  # or "max_rounds", "max_tokens", etc.
        },
        "usage": {
            "input_tokens": 150,
            "cached_tokens": 0,
            "output_tokens": 1550,
            "reasoning_tokens": 1550
        }
    }
}
```

### Continuation Flow

```text
User Request
    ↓
CodexCont (round 1)
    ↓
Upstream API → 516 reasoning tokens (truncated)
    ↓
CodexCont detects 518*1-2, buffers output, continues
    ↓
CodexCont (round 2, reasoning replayed + "Continue thinking...")
    ↓
Upstream API → 250 reasoning tokens (complete)
    ↓
CodexCont flushes final output, reconstructs terminal event
    ↓
User receives single coherent stream
```

## Running Tests

```bash
# Run test suite
uv run python tests/test_middleware.py

# Or with activated venv
.venv/Scripts/python.exe tests/test_middleware.py
```

Tests cover:
- Truncation detection math
- SSE parsing/rewriting
- Commentary and tool-pair continuation
- Auth safety guards
- Header transparency
- Upstream URL resolution

## Troubleshooting

### Proxy not detecting truncation

**Check request format:**
```python
# Ensure these are set:
payload = {
    "stream": True,      # Must be true
    "reasoning": True,   # Or omit (defaults to true)
    # ...
}
```

**Verify configuration:**
```toml
[continue]
enabled = true
tier_gate_low = 1     # Must be <= detected tier
tier_gate_high = 100  # Must be >= detected tier
```

### Authentication errors

**With `Responses-API-Base` override:**
```toml
# Use passthrough mode
[auth]
mode = "passthrough"
```

**Inject mode rejecting requests:**
- The proxy blocks requests with `Responses-API-Base` when using `inject` mode to prevent credential leaks
- Solution: Use `passthrough` mode and send auth in request headers

### High first-token latency for final output

This is expected behavior. Final answer text is buffered until the terminal round proves it's not truncated. Reasoning tokens stream live, but final message content waits for confirmation.

### Upstream connection errors

**Check upstream URL:**
```toml
[upstream]
url = "https://chatgpt.com/backend-api/codex/responses"
mode = "fixed"
```

**Enable debug logging:**
```python
# In run.py or your client
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Non-streaming requests not folded

Currently expected: non-streaming requests pass through unchanged. Use `"stream": true` to enable continuation folding.

### Tool name conflicts

When using `method = "tool_pair"`:
```toml
[continue]
continue_tool_name = "continue_thinking"  # Must not conflict with real tools
```

If your request declares a real tool with this name, folding is disabled for safety.

## Advanced Configuration

### Multiple proxy instances

For load balancing, run multiple instances on different ports:

```bash
# Instance 1
PORT=8787 uv run python run.py

# Instance 2  
PORT=8788 uv run python run.py
```

Update config for port override:
```python
import os
from middleware.config import load_config

config = load_config()
config.server.port = int(os.getenv("PORT", 8787))
```

### Stateful repair mode

```toml
[repair_followup]
mode = "stateful"  # Tracks conversation state in-memory
```

**Warning**: State is process-local and not shared across instances. Not recommended for production load-balanced deployments.

### Custom continuation messages

Edit `middleware/codex.py`:

```python
# For commentary method
CONTINUE_MARKER = "Continue your reasoning from where you left off..."

# For tool_pair method  
def _build_tool_pair_continuation(...):
    # Customize tool description/arguments
    pass
```

## Integration Examples

### With LangChain

```python
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(
    openai_api_base="http://127.0.0.1:8787/v1",
    model="gpt-4",
    streaming=True
)

response = llm.invoke("Complex reasoning task...")
```

### With OpenAI Python SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:8787/v1",
    api_key=os.getenv("OPENAI_API_KEY")
)

stream = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Think deeply about..."}],
    stream=True
)

for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

### With Cursor/Claude Code

Configure in editor settings:

```json
{
  "openai.api.baseUrl": "http://127.0.0.1:8787/v1",
  "openai.api.key": "${OPENAI_API_KEY}"
}
```

## Best Practices

1. **Use environment variables for secrets**: Never hardcode API keys in `config.toml`
2. **Start with `passthrough` auth mode**: Simplest and most secure for development
3. **Monitor `proxy_rounds` metadata**: Understand how many continuation rounds are triggered
4. **Set reasonable safety limits**: Prevent runaway token costs with `max_rounds` and `max_reasoning_tokens`
5. **Use `commentary` method**: More reliable than legacy `tool_pair` approach
6. **Test without proxy first**: Ensure upstream connectivity before adding middleware layer
7. **Enable streaming**: Non-streaming requests bypass continuation logic
