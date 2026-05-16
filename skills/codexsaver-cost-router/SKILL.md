---
name: codexsaver-cost-router
description: Route low-risk coding tasks to cheaper LLMs while keeping Codex for high-risk decisions, using MCP tools for cost-aware delegation
triggers:
  - use codexsaver to reduce costs
  - delegate this task to a cheaper model
  - route low-risk work to deepseek
  - create a bounded work packet for this
  - orchestrate specialists for this task
  - set up codexsaver mcp tool
  - configure codexsaver worker provider
  - run codexsaver benchmarks
---

# CodexSaver Cost Router

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

CodexSaver is an MCP tool that makes Codex cost-aware by routing low-risk development work (tests, docs, search, explanation) to cheaper worker LLMs while keeping Codex responsible for architecture, security, and final review. It supports DeepSeek by default with presets for OpenAI, Anthropic, Gemini, Qwen, Ollama, and LM Studio.

## Core Concepts

CodexSaver operates in three modes:

- **Preview Mode**: Shows routing decision without executing
- **V2 Bounded Work Packets**: Single-task delegation with sandboxed patch application and verification
- **V3 Orchestrated Specialists**: Parallel readonly specialists (explainer, perf_reviewer) and mixed graphs for docs/tests/impl

**Key principle**: Codex handles judgment and risk, worker models handle volume and repetition.

## Installation

### Global MCP Tool Setup

```bash
# Clone repository
git clone https://github.com/fendouai/CodexSaver.git
cd CodexSaver

# Install globally
pip install -e .

# Initialize config
codexsaver init

# Add to Codex MCP config (~/.config/codex/mcp.json or workspace .codex/mcp.json)
```

Add to `mcp.json`:

```json
{
  "mcpServers": {
    "codexsaver": {
      "command": "python",
      "args": ["-m", "codexsaver.mcp_server"],
      "env": {}
    }
  }
}
```

### Configuration

Edit `~/.codexsaver/config.json`:

```json
{
  "provider": "deepseek",
  "deepseek": {
    "api_key_env": "DEEPSEEK_API_KEY",
    "model": "deepseek-chat",
    "base_url": "https://api.deepseek.com"
  },
  "openai": {
    "api_key_env": "OPENAI_API_KEY",
    "model": "gpt-4o-mini"
  },
  "worker_compression": {
    "enabled": true,
    "level": "medium"
  },
  "routing": {
    "protected_paths": ["src/auth/", "payment/", ".env"],
    "risk_threshold": "medium"
  }
}
```

Set environment variable:

```bash
export DEEPSEEK_API_KEY="your-key-here"
```

## MCP Tools Reference

### 1. `codexsaver.delegate_task`

Route a task to the worker model with automatic risk assessment.

**Parameters**:
- `task_description` (required): Task to delegate
- `files` (optional): List of file paths for context
- `mode` (optional): `preview` or `execute` (default: `execute`)

**Example call from Codex**:

```python
# Codex calls this internally via MCP
{
  "tool": "codexsaver.delegate_task",
  "arguments": {
    "task_description": "Write docstrings for all public functions",
    "files": ["src/utils.py"],
    "mode": "execute"
  }
}
```

**Response structure**:

```json
{
  "interaction": {
    "tool": "codexsaver.delegate_task",
    "mode": "delegated_execution",
    "headline": "CodexSaver delegated this task to DeepSeek",
    "route_label": "[CodexSaver] route=deepseek task_type=write_docs risk=low",
    "next_step": "Review the worker result and apply if safe"
  },
  "result": "Delegated task output...",
  "cost_savings": "45%",
  "provider": "deepseek"
}
```

### 2. `codexsaver.delegate_work_packet`

V2: Execute bounded work with sandbox verification.

**Parameters**:
- `goal` (required): Clear task goal
- `files` (optional): Context files
- `allowed_files` (required): Globs for writable files
- `forbidden_paths` (optional): Protected paths
- `acceptance_criteria` (required): Success conditions
- `allowed_commands` (required): Verification commands
- `max_iterations` (optional): Default 3
- `max_diff_lines` (optional): Default 500

**Example**:

```python
{
  "tool": "codexsaver.delegate_work_packet",
  "arguments": {
    "goal": "Add type hints to config loader",
    "files": ["codexsaver/config.py"],
    "allowed_files": ["codexsaver/config.py"],
    "forbidden_paths": ["codexsaver/auth/"],
    "acceptance_criteria": "All public functions have type hints",
    "allowed_commands": ["mypy codexsaver/config.py"],
    "max_iterations": 3,
    "max_diff_lines": 200
  }
}
```

### 3. `codexsaver.orchestrate`

V3: Orchestrate specialists for complex tasks.

**Parameters**:
- `task_description` (required): High-level task
- `files` (optional): Context files
- `mode` (optional): `preview` or `execute`

**Example**:

```python
{
  "tool": "codexsaver.orchestrate",
  "arguments": {
    "task_description": "Explain config module and review performance",
    "files": ["codexsaver/config.py"],
    "mode": "execute"
  }
}
```

**Response for readonly_swarm**:

```json
{
  "status": "success",
  "graph_type": "readonly_swarm",
  "findings": 10,
  "quality_score": 0.75,
  "latency_seconds": 6.45,
  "cost_savings": "52%",
  "results": {
    "explainer": "Config module loads from ~/.codexsaver/config.json...",
    "perf_reviewer": "No blocking I/O, caching recommended..."
  }
}
```

## CLI Commands

### Initialize Configuration

```bash
codexsaver init
```

Creates `~/.codexsaver/config.json` with DeepSeek defaults.

### Preview Routing Decision

```bash
codexsaver preview "Write unit tests for auth module" --files src/auth.py
```

Shows routing decision without executing.

### Execute Work Packet

```bash
codexsaver work-packet \
  "Add docstrings to public functions" \
  --files src/utils.py \
  --allowed-file src/utils.py \
  --acceptance "All functions have docstrings" \
  --allowed-command "python -m pydoc src.utils" \
  --workspace .
```

### Orchestrate Specialists

```bash
# Readonly specialists (fastest, most reliable)
codexsaver orchestrate "Explain installer flow and review performance" \
  --files codexsaver/install.py

# Mixed graph (docs + explain)
codexsaver orchestrate "Document API and explain usage patterns" \
  --files codexsaver/api.py

# Dry run
codexsaver orchestrate "Implement login and add tests" \
  --files src/auth.py \
  --dry-run
```

### Run Single Specialist

```bash
# Explainer
codexsaver specialist explainer "Explain this module" \
  --files codexsaver/router.py

# Performance Reviewer
codexsaver specialist perf_reviewer "Review performance" \
  --files codexsaver/delegate.py
```

### Install Project Guidance

```bash
# Basic: AGENTS.md guidance only
codexsaver superpower install --profile basic --workspace .

# Full: AGENTS.md + hooks + local config
codexsaver superpower install --profile full --workspace .
```

## Python API

### Direct Delegation

```python
from codexsaver.delegate import delegate_task

result = delegate_task(
    task_description="Write docstrings for utils module",
    files=["src/utils.py"],
    mode="execute"
)

print(result["interaction"]["route_label"])
print(result["result"])
```

### Work Packet Execution

```python
from codexsaver.work_packet import execute_work_packet

result = execute_work_packet(
    goal="Add type hints to config loader",
    files=["codexsaver/config.py"],
    allowed_files=["codexsaver/config.py"],
    acceptance_criteria="All functions have type hints",
    allowed_commands=["mypy codexsaver/config.py"],
    workspace_root="."
)

if result["status"] == "success":
    print(f"Patch applied: {result['changed_files']}")
elif result["preflight_satisfied"]:
    print("Task already satisfied, no work needed")
```

### Specialist Orchestration

```python
from codexsaver.orchestrate import orchestrate_task

result = orchestrate_task(
    task_description="Explain config module and review performance",
    files=["codexsaver/config.py"],
    mode="execute"
)

if result["status"] == "success":
    print(f"Graph type: {result['graph_type']}")
    print(f"Findings: {result['findings']}")
    print(f"Quality score: {result['quality_score']}")
    for specialist, output in result["results"].items():
        print(f"\n{specialist}:\n{output}")
```

### Router Configuration

```python
from codexsaver.router import Router

router = Router()

# Check if task is safe to delegate
decision = router.should_delegate(
    task_description="Write unit tests",
    files=["src/utils.py"]
)

print(f"Route: {decision['route']}")  # 'deepseek' or 'codex'
print(f"Risk: {decision['risk_level']}")  # 'low', 'medium', 'high'
print(f"Task type: {decision['task_type']}")  # 'write_tests', 'explain', etc.
```

## Common Patterns

### Pattern 1: Low-Risk Documentation Work

**When to use**: Adding or updating docs, docstrings, README sections

```python
# Via MCP tool
{
  "tool": "codexsaver.delegate_task",
  "arguments": {
    "task_description": "Add docstrings to all public functions in utils",
    "files": ["src/utils.py"],
    "mode": "execute"
  }
}
```

**Expected route**: `deepseek` (low risk, high volume)

### Pattern 2: Bounded Test Generation

**When to use**: Creating tests for well-defined modules

```bash
codexsaver work-packet \
  "Write pytest tests for config loader" \
  --files codexsaver/config.py \
  --allowed-file tests/test_config.py \
  --acceptance "tests/test_config.py exists and pytest passes" \
  --allowed-command "pytest tests/test_config.py -v" \
  --workspace .
```

**Expected route**: `deepseek` with sandbox verification

### Pattern 3: Readonly Analysis

**When to use**: Code explanation, performance hints, security scan (no patches)

```bash
codexsaver orchestrate "Explain auth flow and review performance" \
  --files src/auth.py
```

**Expected route**: `readonly_swarm` (parallel explainer + perf_reviewer)

### Pattern 4: Codex Takeover for High-Risk Work

**When to use**: Auth, payment, destructive migrations, ambiguous architecture

```python
{
  "tool": "codexsaver.delegate_task",
  "arguments": {
    "task_description": "Refactor authentication middleware",
    "files": ["src/auth/middleware.py"],
    "mode": "execute"
  }
}
```

**Expected route**: `codex` (protected path detected)

Response includes:

```json
{
  "interaction": {
    "mode": "codex_takeover",
    "headline": "CodexSaver kept this task with Codex",
    "route_label": "[CodexSaver] route=codex reason=protected_path"
  }
}
```

### Pattern 5: Mixed Graph Orchestration

**When to use**: Docs + explanation + small impl changes

```bash
codexsaver orchestrate "Document API, explain usage, and add examples" \
  --files codexsaver/api.py
```

**Expected graph**: `docs + explain` (mixed readonly + bounded patch)

## Risk Assessment Rules

CodexSaver routes tasks based on:

### Automatic Codex Takeover

- Files match `protected_paths` (auth, payment, .env)
- Task mentions security, permissions, migration
- Ambiguous requirements
- Multi-file behavioral changes without verification

### Safe Delegation to Worker

- Task type: `write_tests`, `write_docs`, `explain`, `search`
- Files outside protected paths
- Clear acceptance criteria
- Bounded scope with verification commands

### Configuration Override

```json
{
  "routing": {
    "protected_paths": ["src/auth/", "billing/", "*.key"],
    "risk_threshold": "medium",
    "force_codex_patterns": ["payment", "security", "migrate"]
  }
}
```

## Worker Output Compression

Reduce delegated output length for faster Codex review:

```json
{
  "worker_compression": {
    "enabled": true,
    "level": "medium"
  }
}
```

Levels:
- `low`: Minor trimming
- `medium`: Remove verbose explanations, keep facts
- `high`: Maximum compression, essential info only

Response includes compression notice:

```json
{
  "interaction": {
    "compression": {
      "active": true,
      "level": "medium",
      "notice": "Worker output compressed to medium level"
    }
  }
}
```

## Troubleshooting

### MCP Tool Not Found

**Symptom**: Codex doesn't recognize `codexsaver.*` tools

**Fix**:

```bash
# Verify MCP server config
cat ~/.config/codex/mcp.json

# Test MCP server manually
python -m codexsaver.mcp_server

# Restart Codex after config changes
```

### Worker Provider Authentication Failed

**Symptom**: `Authentication error: DEEPSEEK_API_KEY not found`

**Fix**:

```bash
# Set environment variable
export DEEPSEEK_API_KEY="sk-..."

# Verify config
cat ~/.codexsaver/config.json

# Test provider directly
codexsaver preview "test task" --files README.md
```

### Sandbox Verification Failed

**Symptom**: Work packet returns `verification_failed`

**Fix**:

```bash
# Check allowed commands are valid
codexsaver work-packet \
  "test task" \
  --allowed-command "python -c 'import sys; sys.exit(0)'" \
  --acceptance "passes basic check" \
  --workspace . \
  --verbose

# Increase max iterations
codexsaver work-packet \
  "complex task" \
  --max-iterations 5 \
  --workspace .
```

### All Tasks Route to Codex

**Symptom**: No cost savings, everything stays with Codex

**Fix**:

```json
{
  "routing": {
    "risk_threshold": "low",
    "protected_paths": []
  }
}
```

Or use explicit work packets for guaranteed delegation.

### V3 Orchestration Returns `needs_codex`

**Symptom**: Complex graphs fall back conservatively

**Expected behavior**: V3 patch orchestration is still maturing. Use for:
- ✅ Readonly specialist swarms (established)
- ✅ Single bounded patches (v2 mature)
- ⚠️ Multi-patch graphs (promising but conservative)

**Workaround**: Break complex tasks into separate work packets.

## Best Practices

1. **Start with preview mode** to understand routing decisions
2. **Use work packets for implementation** to get sandbox verification
3. **Use orchestration for analysis** (readonly swarms are fastest)
4. **Keep Codex for ambiguity** - don't force delegation on unclear tasks
5. **Monitor cost savings** - review interaction blocks in responses
6. **Set realistic acceptance criteria** - make verification commands specific
7. **Protect sensitive paths** - add to `protected_paths` config
8. **Enable compression** for faster Codex review of delegated output

## Environment Variables

```bash
# Required for DeepSeek (default provider)
export DEEPSEEK_API_KEY="sk-..."

# Optional alternative providers
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."
export GEMINI_API_KEY="..."
export QWEN_API_KEY="..."

# Optional: override config path
export CODEXSAVER_CONFIG_PATH="/custom/path/config.json"
```

## Provider Presets

Switch providers in `~/.codexsaver/config.json`:

```json
{
  "provider": "openai",
  "openai": {
    "api_key_env": "OPENAI_API_KEY",
    "model": "gpt-4o-mini"
  }
}
```

Supported: `deepseek`, `openai`, `anthropic`, `gemini`, `qwen`, `ollama`, `lmstudio`
