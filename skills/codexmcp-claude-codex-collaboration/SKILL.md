---
name: codexmcp-claude-codex-collaboration
description: Enable seamless collaboration between Claude Code and Codex using MCP protocol for multi-agent AI coding workflows
triggers:
  - how do I connect Claude Code with Codex
  - set up CodexMCP for multi-agent collaboration
  - use Claude Code and Codex together
  - configure MCP bridge between AI coding assistants
  - enable parallel AI coding agents
  - manage sessions between Claude and Codex
  - troubleshoot CodexMCP connection
  - implement multi-round dialogue with Codex
---

# CodexMCP: Claude Code & Codex Collaboration

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

CodexMCP is an MCP (Model Context Protocol) server that enables seamless collaboration between Claude Code and Codex. It bridges these two AI coding assistants, allowing Claude Code to handle architecture and planning while Codex handles implementation and debugging, with features like session persistence, parallel execution, and reasoning trace tracking.

## What It Does

CodexMCP provides:
- **Multi-round dialogue** between Claude Code and Codex with session management
- **Parallel task execution** with isolated session IDs
- **Reasoning trace tracking** for detailed debugging insights
- **Enhanced error handling** and workspace safety controls
- **Session persistence** across multiple interactions

## Installation

### Prerequisites

Ensure you have:
- Claude Code v2.0.56+ installed and configured
- Codex CLI v0.61.0+ installed and configured
- `uv` tool installed ([installation guide](https://docs.astral.sh/uv/getting-started/installation/))

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Install CodexMCP

**1. Remove official Codex MCP (if installed):**
```bash
claude mcp remove codex
```

**2. Install CodexMCP:**
```bash
claude mcp add codex -s user --transport stdio -- uvx --from git+https://github.com/GuDaStudio/codexmcp.git codexmcp
```

**3. Verify installation:**
```bash
claude mcp list
```

Expected output:
```
codex: uvx --from git+https://github.com/GuDaStudio/codexmcp.git codexmcp - ✓ Connected
```

**4. (Optional) Auto-approve MCP interactions:**

Edit `~/.claude/settings.json` and add `mcp__codex__codex` to the allow list.

## Configuration

### Recommended Claude Code System Prompt

Add to `~/.claude/CLAUDE.md` for optimal collaboration:

```markdown
## Core Instruction for CodeX MCP

At any time, you must consider how to collaborate with Codex and leverage the MCP tools it provides.

**Mandatory steps:**
1. After forming initial analysis of user requirements, inform Codex of the requirements and initial thoughts, and ask it to refine the analysis and implementation plan.
2. Before implementing specific coding tasks, **must request a code implementation prototype from Codex** (require Codex to only provide unified diff patch, strictly prohibit any real code modifications). After obtaining the prototype, you **must use it only as a logical reference, rewrite the code modification** to form enterprise-grade, highly readable, highly maintainable code before implementing the actual programming changes.
3. Whenever concrete coding behavior is completed, **must immediately use Codex to review code changes and corresponding requirement completion**.
4. Codex only provides reference; you **must have your own thinking and even question Codex's answers**. You and Codex must continuously debate to find the only path to truth.

## Codex Tool Invocation Specification

### Tool Parameters

**Required:**
- `PROMPT` (string): Task instruction for Codex
- `cd` (Path): Working directory root path

**Optional:**
- `sandbox` (string): "read-only" (default), "workspace-write", "danger-full-access"
- `SESSION_ID` (UUID | null): Continue previous session (default: None for new session)
- `skip_git_repo_check` (boolean): Allow running outside Git repo (default: False)
- `return_all_messages` (boolean): Return all messages including reasoning (default: False)
- `image` (List[Path] | null): Attach image files to initial prompt
- `model` (string | null): Specify model (default: user config)
- `yolo` (boolean | null): Run all commands without approval (default: False)
- `profile` (string | null): Config profile from ~/.codex/config.toml

### Best Practices

- **Always save SESSION_ID** for multi-round dialogue
- Use `sandbox="read-only"` for safe prototyping
- Set `return_all_messages=True` for detailed debugging
- Ensure `cd` points to an existing directory
```

## API Reference

### The `codex` Tool

CodexMCP provides a single MCP tool called `codex` that executes AI-assisted coding tasks.

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `PROMPT` | `str` | ✅ | - | Task instruction for Codex |
| `cd` | `Path` | ✅ | - | Working directory root path |
| `sandbox` | `Literal["read-only", "workspace-write", "danger-full-access"]` | ❌ | `"read-only"` | Sandbox policy |
| `SESSION_ID` | `UUID \| None` | ❌ | `None` | Session ID for continuation |
| `skip_git_repo_check` | `bool` | ❌ | `False` | Allow non-Git repos |
| `return_all_messages` | `bool` | ❌ | `False` | Return full reasoning trace |
| `image` | `List[Path] \| None` | ❌ | `None` | Attach images to prompt |
| `model` | `str \| None` | ❌ | `None` | Specify model |
| `yolo` | `bool \| None` | ❌ | `False` | Skip all approvals |
| `profile` | `str \| None` | ❌ | `None` | Config profile name |

#### Return Value

**Success:**
```json
{
  "success": true,
  "SESSION_ID": "550e8400-e29b-41d4-a716-446655440000",
  "agent_messages": "Codex response text...",
  "all_messages": []  // Only when return_all_messages=True
}
```

**Failure:**
```json
{
  "success": false,
  "error": "Error message"
}
```

## Usage Patterns

### Pattern 1: Single-shot Code Review

```python
# In Claude Code, invoke Codex for code review
# (This is conceptual - actual invocation happens through MCP)

tool_params = {
    "PROMPT": "Review the authentication logic in src/auth.py for security issues",
    "cd": "/path/to/project",
    "sandbox": "read-only",
    "return_all_messages": True
}

# MCP tool call returns:
{
    "success": True,
    "SESSION_ID": "abc-123",
    "agent_messages": "Found potential SQL injection in line 45..."
}
```

### Pattern 2: Multi-round Dialogue Session

```python
# First request: Get implementation plan
params_1 = {
    "PROMPT": "Analyze requirements for user authentication feature",
    "cd": "/path/to/project",
    "sandbox": "read-only"
}
# Returns: SESSION_ID = "session-xyz"

# Second request: Continue the session
params_2 = {
    "PROMPT": "Now generate a unified diff patch for the authentication module",
    "cd": "/path/to/project",
    "SESSION_ID": "session-xyz",  # Continue previous conversation
    "sandbox": "read-only"
}

# Third request: Ask follow-up questions
params_3 = {
    "PROMPT": "What about edge cases for token expiration?",
    "cd": "/path/to/project",
    "SESSION_ID": "session-xyz",
    "sandbox": "read-only"
}
```

### Pattern 3: Parallel Task Execution

```python
# Task A: Bug investigation (isolated session)
task_a = {
    "PROMPT": "Debug memory leak in data processor",
    "cd": "/path/to/project",
    "sandbox": "read-only"
}
# Returns: SESSION_ID_A = "task-a-123"

# Task B: Feature prototyping (separate isolated session)
task_b = {
    "PROMPT": "Create prototype for caching layer",
    "cd": "/path/to/project",
    "sandbox": "read-only"
}
# Returns: SESSION_ID_B = "task-b-456"

# Both tasks run independently without context interference
```

### Pattern 4: Detailed Reasoning Trace

```python
# Enable full message history for debugging
params = {
    "PROMPT": "Optimize database query performance in reports module",
    "cd": "/path/to/project",
    "sandbox": "read-only",
    "return_all_messages": True  # Get full reasoning chain
}

# Returns:
{
    "success": True,
    "SESSION_ID": "debug-session",
    "agent_messages": "Optimized query reduces execution time...",
    "all_messages": [
        {"role": "reasoning", "content": "Analyzing query structure..."},
        {"role": "tool_call", "content": "read_file reports/queries.py"},
        {"role": "tool_result", "content": "...file contents..."},
        {"role": "reasoning", "content": "Identified N+1 query pattern..."},
        # ... full trace
    ]
}
```

### Pattern 5: Image-based Context

```python
# Attach architecture diagram for context
params = {
    "PROMPT": "Review this architecture and suggest improvements",
    "cd": "/path/to/project",
    "image": ["/path/to/architecture.png", "/path/to/flowchart.svg"],
    "sandbox": "read-only"
}
```

## Common Workflows

### Workflow 1: Claude Architecting + Codex Implementing

1. **Claude analyzes requirements** and creates high-level plan
2. **Claude invokes Codex** with architectural decisions:
   ```python
   {
       "PROMPT": "Based on this architecture, create implementation prototype for auth service",
       "cd": "/path/to/project",
       "sandbox": "read-only"
   }
   ```
3. **Codex returns unified diff patch** (no actual changes)
4. **Claude reviews and refines** the code
5. **Claude implements** the final version
6. **Claude asks Codex to review** the implementation:
   ```python
   {
       "PROMPT": "Review the auth service implementation for security and best practices",
       "cd": "/path/to/project",
       "SESSION_ID": "previous-session-id",
       "sandbox": "read-only"
   }
   ```

### Workflow 2: Bug Investigation

1. **Claude identifies bug symptoms**
2. **Claude delegates to Codex** for detailed investigation:
   ```python
   {
       "PROMPT": "Investigate null pointer exception in payment processor at line 234",
       "cd": "/path/to/project",
       "sandbox": "read-only",
       "return_all_messages": True  # Get detailed trace
   }
   ```
3. **Codex traces execution flow** and identifies root cause
4. **Claude formulates fix** based on Codex insights
5. **Claude asks Codex to validate** the fix

### Workflow 3: Code Refactoring

1. **Claude plans refactoring strategy**
2. **Claude requests Codex analysis**:
   ```python
   {
       "PROMPT": "Analyze technical debt in legacy payment module",
       "cd": "/path/to/project",
       "sandbox": "read-only"
   }
   ```
3. **Codex identifies patterns** and suggests improvements
4. **Claude implements refactoring** in stages
5. **Codex reviews each stage** for consistency

## Troubleshooting

### Connection Issues

**Problem:** `codex: ... - ✗ Not Connected`

**Solutions:**
```bash
# Check MCP configuration
claude mcp list

# Reinstall CodexMCP
claude mcp remove codex
claude mcp add codex -s user --transport stdio -- uvx --from git+https://github.com/GuDaStudio/codexmcp.git codexmcp

# Restart Claude Code
# (Close and reopen the application)
```

### Session Not Persisting

**Problem:** Session context is lost between calls

**Solutions:**
- Ensure `SESSION_ID` from previous response is passed to next call
- Verify the returned `SESSION_ID` is a valid UUID
- Check that the same `cd` path is used across session calls

```python
# ✅ Correct: Save and reuse SESSION_ID
response_1 = codex_tool(PROMPT="First task", cd="/project")
session_id = response_1["SESSION_ID"]

response_2 = codex_tool(
    PROMPT="Continue task",
    cd="/project",
    SESSION_ID=session_id  # Reuse here
)

# ❌ Wrong: Not passing SESSION_ID
response_2 = codex_tool(PROMPT="Continue task", cd="/project")  # New session!
```

### Working Directory Errors

**Problem:** Tool fails silently or returns "directory not found"

**Solutions:**
```python
# ✅ Use absolute paths
params = {
    "cd": "/home/user/projects/myapp",
    "PROMPT": "..."
}

# ✅ Or resolve relative paths first
import os
params = {
    "cd": os.path.abspath("./myapp"),
    "PROMPT": "..."
}

# ❌ Don't use relative paths directly
params = {
    "cd": "./myapp",  # May not resolve correctly
    "PROMPT": "..."
}
```

### Git Repository Check Failing

**Problem:** Codex refuses to run outside Git repository

**Solutions:**
```python
# Option 1: Initialize Git repo
# $ cd /path/to/project
# $ git init

# Option 2: Skip the check (not recommended for production)
params = {
    "PROMPT": "...",
    "cd": "/path/to/project",
    "skip_git_repo_check": True  # Bypass Git requirement
}
```

### Sandbox Permission Errors

**Problem:** Codex cannot write files when needed

**Solutions:**
```python
# For read-only analysis (safest, default)
params = {"sandbox": "read-only"}

# For workspace modifications
params = {"sandbox": "workspace-write"}

# For full access (use with caution)
params = {"sandbox": "danger-full-access"}

# Or skip sandbox entirely (not recommended)
params = {"yolo": True}
```

### Model Configuration Issues

**Problem:** Using wrong model or hitting rate limits

**Solutions:**
```python
# Use specific model
params = {
    "PROMPT": "...",
    "cd": "/project",
    "model": "claude-3-opus"  # Specify model
}

# Use custom profile from ~/.codex/config.toml
params = {
    "PROMPT": "...",
    "cd": "/project",
    "profile": "production"  # Load specific config
}
```

### Debugging Reasoning Failures

**Problem:** Codex gives unexpected results

**Solutions:**
```python
# Enable full message trace
params = {
    "PROMPT": "...",
    "cd": "/project",
    "return_all_messages": True  # See full reasoning chain
}

# Inspect the response
response = codex_tool(**params)
for msg in response.get("all_messages", []):
    print(f"{msg['role']}: {msg['content']}")
```

## Advanced Configuration

### Custom Codex Config Profile

Edit `~/.codex/config.toml`:

```toml
[profiles.production]
model = "claude-3-opus"
max_tokens = 8192
temperature = 0.3

[profiles.experimental]
model = "claude-3-sonnet"
max_tokens = 16384
temperature = 0.7
```

Use in CodexMCP:
```python
params = {
    "PROMPT": "...",
    "cd": "/project",
    "profile": "production"  # Load this profile
}
```

### Environment Variables

CodexMCP respects standard Codex CLI environment variables:

```bash
# Set default model
export CODEX_MODEL="claude-3-opus"

# Set API key (if needed)
export ANTHROPIC_API_KEY="sk-ant-..."

# Custom config location
export CODEX_CONFIG_PATH="~/.config/codex/custom.toml"
```

## Integration Examples

### Example: Full Development Cycle

```python
# Step 1: Claude analyzes requirements
# (Manual interaction with user)

# Step 2: Claude asks Codex for implementation plan
plan_response = codex_tool(
    PROMPT="Create implementation plan for user authentication with JWT tokens",
    cd="/path/to/project",
    sandbox="read-only"
)
session_id = plan_response["SESSION_ID"]

# Step 3: Claude asks for code prototype
prototype_response = codex_tool(
    PROMPT="Generate unified diff patch for JWT auth implementation",
    cd="/path/to/project",
    SESSION_ID=session_id,
    sandbox="read-only"
)

# Step 4: Claude refines and implements
# (Claude writes actual code based on prototype)

# Step 5: Claude asks Codex to review
review_response = codex_tool(
    PROMPT="Review the implemented JWT authentication for security issues",
    cd="/path/to/project",
    SESSION_ID=session_id,
    sandbox="read-only",
    return_all_messages=True
)

# Step 6: Claude addresses feedback and iterates
```

## Best Practices

1. **Always use `sandbox="read-only"`** for Codex prototyping to prevent accidental changes
2. **Track SESSION_ID** for multi-round conversations
3. **Use absolute paths** for the `cd` parameter
4. **Enable `return_all_messages`** when debugging or tracing reasoning
5. **Set up Git repositories** before running Codex (or use `skip_git_repo_check` sparingly)
6. **Use descriptive PROMPTs** that clearly state the task and context
7. **Leverage parallel sessions** for independent tasks (different SESSION_IDs)
8. **Review Codex outputs** critically — treat them as suggestions, not final solutions

## Resources

- [GitHub Repository](https://github.com/GuDaStudio/codexmcp)
- [Official Homepage](https://code.guda.studio)
- [Codex CLI Documentation](https://developers.openai.com/codex/quickstart)
- [Claude Code Documentation](https://docs.claude.com/docs/claude-code)
- [MCP Protocol Specification](https://modelcontextprotocol.io)
