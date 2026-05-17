---
name: seemseam-ccb-multi-agent-cli
description: Orchestrate multi-agent AI teams (Claude, Codex, Gemini, OpenCode, Droid) with tmux-based supervision, project memory, and inter-agent communication
triggers:
  - set up ccb multi-agent team
  - configure claude codex bridge agents
  - create agent team with ccb
  - add inter-agent communication
  - configure ccb project layout
  - troubleshoot ccb agent teams
  - use ccb ask for agent delegation
  - manage ccb agent worktrees
---

# SeemSeam CCB Multi-Agent CLI

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

CCB (Claude Codex Bridge) is a multi-agent orchestration framework that runs Claude, Codex, Gemini, OpenCode, and Droid agents in supervised tmux panes with shared project memory, inter-agent communication via `/ask`, and isolated worktree support for parallel work.

## What CCB Does

- **Unified CLI entry point**: Start, attach, recover, and supervise multiple AI agent CLIs from one command
- **Inter-agent communication**: Agents can `/ask` each other, broadcast updates, and delegate work
- **Project-level teams**: Define role-based teams with custom pane layouts, provider state, and worktree isolation
- **Shared memory**: All agents access `.ccb/ccb_memory.md` for project-wide context
- **Tmux supervision**: Every agent runs in a named tmux pane with lifecycle management

## Installation

### Unix-like (Linux, macOS, WSL)

```bash
git clone https://github.com/SeemSeam/claude_codex_bridge.git
cd claude_codex_bridge
./install.sh install
```

### Windows

```powershell
git clone https://github.com/SeemSeam/claude_codex_bridge.git
cd claude_codex_bridge
powershell -ExecutionPolicy Bypass -File .\install.ps1 install
```

### Update to Latest Release

```bash
ccb update              # Latest stable
ccb update 6            # Highest v6.x.x
ccb update 6.1          # Highest v6.1.x
ccb update 6.1.21       # Specific version
```

### Requirements

- Python 3.10+
- tmux

## Core Commands

```bash
# Start agents from .ccb/ccb.config
ccb

# Safe start (preserve permission settings)
ccb -s

# Rebuild state (preserve config) then start
ccb -n

# Stop project runtime
ccb kill

# Force cleanup before rebuild
ccb kill -f

# Uninstall
ccb uninstall

# Reinstall
ccb reinstall
```

## Configuration

CCB is configured via `.ccb/ccb.config` (project-local, user-authored). If missing, CCB uses built-in defaults without creating a file.

### Basic Layout Syntax

The first line defines the team and pane layout:

```text
cmd; writer:codex, reviewer:claude; qa:gemini(worktree)
```

**Layout rules:**
- `;` splits panes left-to-right
- `,` stacks panes top-to-bottom
- `cmd` is the shell pane
- `name:provider` defines an agent
- `(worktree)` runs agent in isolated git worktree
- Without `(worktree)`, agent runs `inplace`

### Common Layouts

```text
# Two-agent team
writer:codex, reviewer:claude

# Shell + three agents
cmd; writer:codex, reviewer:claude; qa:gemini(worktree)

# Same provider, different roles
cmd; fast:codex, deep:codex
```

### Per-Agent API Configuration

Add TOML tables after the layout line for agents needing custom API keys, URLs, or models:

```toml
cmd; builder:codex, reviewer:claude; research:gemini(worktree)

[agents.builder]
key = "$OPENAI_API_KEY"
url = "https://api.openai.com/v1"
model = "gpt-4"

[agents.reviewer]
key = "$ANTHROPIC_API_KEY"
url = "https://api.anthropic.com"
model = "claude-3-5-sonnet-20241022"

[agents.research]
key = "$GEMINI_API_KEY"
model = "gemini-2.0-flash-exp"
```

**Notes:**
- Use environment variables for API keys (`$VAR_NAME`)
- `key` and `url` override global provider credentials
- `model` sets agent-specific model
- Do not commit real API keys

### Same Provider, Multiple API Keys

```toml
cmd; fast:codex, deep:codex

[agents.fast]
key = "$OPENAI_FAST_KEY"
model = "gpt-4o-mini"

[agents.deep]
key = "$OPENAI_DEEP_KEY"
url = "https://api.example.com/v1"
model = "gpt-4o"
```

### Advanced Provider Environment

```toml
[agents.builder.provider_profile.env]
OPENAI_API_KEY = "$OPENAI_BUILDER_KEY"
OPENAI_BASE_URL = "https://custom.endpoint.com/v1"
```

Do not mix `key`/`url` shortcuts with `provider_profile.env` on the same agent.

## Inter-Agent Communication

CCB agents can communicate using `/ask` or `$ask` syntax.

### Explicit `/ask` Delegation

```text
/ask reviewer review the parser changes in src/parser.ts
```

### Explicit `$ask` Delegation

```bash
$ask reviewer review the parser changes in src/parser.ts
```

### Implicit Delegation (Natural Language)

```text
Ask reviewer to check the parser edge cases, then summarize the issues back to me.
```

For implicit delegation to work, add the `ask` skill basics to your system memory or agent prompt.

### Broadcasting to All Agents

Agents can broadcast context updates to all live agents when the whole team needs the same information.

### Agent Discovery

Named agents can discover each other and use named targets for delegation without copy/paste.

## Project Memory

`.ccb/ccb_memory.md` is the shared project memory document. All agents in the team can read and write to this file for persistent context.

```python
# Example: Agent updating shared memory
with open('.ccb/ccb_memory.md', 'a') as f:
    f.write('\n## Feature X Implementation\n')
    f.write('- Completed API endpoint `/api/v1/feature`\n')
    f.write('- Added tests in `tests/test_feature.py`\n')
```

## Worktree Isolation

Agents marked with `(worktree)` run in isolated git worktrees, enabling parallel work without conflicts.

### Example: QA Agent in Worktree

```text
cmd; builder:codex, reviewer:claude; qa:gemini(worktree)
```

The `qa` agent runs in a separate worktree under `.ccb/worktrees/qa/`, allowing it to:
- Test changes without affecting main working tree
- Run parallel test suites
- Isolate experimental work

## Real-World Examples

### Example 1: Full-Stack Development Team

`.ccb/ccb.config`:
```toml
cmd; frontend:codex, backend:claude; test:gemini(worktree)

[agents.frontend]
key = "$OPENAI_API_KEY"
model = "gpt-4o"

[agents.backend]
key = "$ANTHROPIC_API_KEY"
model = "claude-3-5-sonnet-20241022"

[agents.test]
key = "$GEMINI_API_KEY"
model = "gemini-2.0-flash-exp"
```

**Workflow:**
1. Start team: `ccb`
2. Frontend agent builds React component
3. Backend agent implements API endpoint
4. Frontend asks backend: `/ask backend does the /api/users endpoint support pagination?`
5. Test agent runs integration tests in isolated worktree
6. Test agent reports back: `/ask frontend found CORS issue in login flow`

### Example 2: Code Review Pipeline

`.ccb/ccb.config`:
```toml
cmd; writer:codex, reviewer:claude, qa:codex(worktree)

[agents.writer]
key = "$OPENAI_WRITER_KEY"
model = "gpt-4o"

[agents.reviewer]
key = "$ANTHROPIC_API_KEY"
model = "claude-3-5-sonnet-20241022"

[agents.qa]
key = "$OPENAI_QA_KEY"
model = "gpt-4o-mini"
```

**Workflow:**
1. Writer implements feature in `src/feature.py`
2. Writer asks reviewer: `/ask reviewer review src/feature.py for security issues`
3. Reviewer provides feedback in chat
4. Writer applies fixes
5. QA agent runs tests in worktree: `/ask qa run test suite for feature.py`

### Example 3: Research and Documentation

```toml
cmd; research:gemini, writer:codex

[agents.research]
key = "$GEMINI_API_KEY"
model = "gemini-2.0-flash-exp"

[agents.writer]
key = "$OPENAI_API_KEY"
model = "gpt-4o"
```

**Workflow:**
1. Research agent explores API documentation
2. Research broadcasts findings: agent updates `.ccb/ccb_memory.md`
3. Writer reads memory and generates documentation
4. Writer asks research: `/ask research verify these GraphQL schema examples`

## Python Integration Examples

### Programmatically Reading Project Memory

```python
import os

def read_project_memory():
    """Read shared project memory for context."""
    memory_path = os.path.join('.ccb', 'ccb_memory.md')
    if os.path.exists(memory_path):
        with open(memory_path, 'r') as f:
            return f.read()
    return ""

# Use in agent script
context = read_project_memory()
print(f"Current project context:\n{context}")
```

### Writing to Project Memory

```python
import os
from datetime import datetime

def append_to_memory(section, content):
    """Append structured content to project memory."""
    memory_path = os.path.join('.ccb', 'ccb_memory.md')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(memory_path, 'a') as f:
        f.write(f'\n## {section} ({timestamp})\n\n')
        f.write(content)
        f.write('\n')

# Example usage
append_to_memory(
    'API Endpoint Implementation',
    '- Created `/api/v1/users` endpoint\n'
    '- Added authentication middleware\n'
    '- Tests passing in `tests/test_users.py`'
)
```

### Inter-Agent Ask Wrapper

```python
import subprocess

def ask_agent(agent_name, query):
    """Send query to another agent via CCB ask."""
    result = subprocess.run(
        ['ask', agent_name, query],
        capture_output=True,
        text=True
    )
    return result.stdout

# Example usage
response = ask_agent('reviewer', 'review src/auth.py for security issues')
print(f"Reviewer feedback:\n{response}")
```

## Tmux Integration

CCB runs all agents in tmux panes. Useful tmux commands:

```bash
# List CCB sessions
tmux ls

# Attach to CCB session
tmux attach -t <session-name>

# Navigate panes (within tmux)
Ctrl+b <arrow-key>

# Copy mode
# Drag left mouse button to select, Ctrl+Shift+V to paste
```

## Troubleshooting

### Issue: `ccb` command not found

**Solution:**
```bash
# Verify installation
which ccb

# Reinstall
cd claude_codex_bridge
./install.sh install

# Check PATH includes CCB bin directory
echo $PATH | grep ccb
```

### Issue: Agents not starting

**Solution:**
```bash
# Check .ccb/ccb.config syntax
cat .ccb/ccb.config

# Rebuild state
ccb kill -f
ccb -n

# Check agent provider availability
which claude
which codex
```

### Issue: `/ask` not working

**Causes:**
- Agent doesn't have `ask` skill in system memory
- Agent is using built-in multi-agent behavior instead

**Solution:**
Add to agent system prompt or `.ccb/ccb_memory.md`:
```markdown
## Inter-Agent Communication

Use `/ask <agent_name> <query>` to delegate tasks to other agents.
Use `$ask <agent_name> <query>` as alternative syntax.

Available agents: [list agent names from layout]
```

### Issue: API key errors

**Solution:**
```bash
# Verify environment variables
echo $OPENAI_API_KEY
echo $ANTHROPIC_API_KEY

# Check .ccb/ccb.config uses env vars
cat .ccb/ccb.config

# Never commit real keys
git diff .ccb/ccb.config
```

### Issue: Worktree conflicts

**Solution:**
```bash
# List worktrees
git worktree list

# Remove stale worktree
git worktree remove .ccb/worktrees/<agent-name>

# Restart CCB
ccb kill -f
ccb
```

### Issue: Stale processes after kill

**Solution:**
```bash
# Force cleanup
ccb kill -f

# If still stuck, find CCB processes
ps aux | grep ccb

# Kill manually
kill -9 <pid>

# Restart
ccb
```

## Best Practices

1. **Use environment variables for API keys**: Never commit real keys to `.ccb/ccb.config`
2. **Name agents by role**: `writer`, `reviewer`, `tester` are clearer than `agent1`, `agent2`
3. **Use worktrees for isolation**: Mark test/experimental agents with `(worktree)`
4. **Update shared memory**: Keep `.ccb/ccb_memory.md` current for team context
5. **Explicit delegation first**: Use `/ask` when you know the target; let agents decide only when workflow is clear
6. **Start safe**: Use `ccb -s` to preserve manual permission settings during development
7. **Clean restarts**: Use `ccb -n` when changing layouts or providers

## Configuration Examples

### Minimal Two-Agent Setup

`.ccb/ccb.config`:
```text
writer:codex, reviewer:claude
```

### Complex Multi-Provider Team

`.ccb/ccb.config`:
```toml
cmd; builder:codex, reviewer:claude; qa:gemini(worktree), researcher:gemini

[agents.builder]
key = "$OPENAI_BUILDER_KEY"
model = "gpt-4o"

[agents.reviewer]
key = "$ANTHROPIC_REVIEWER_KEY"
model = "claude-3-5-sonnet-20241022"

[agents.qa]
key = "$GEMINI_QA_KEY"
model = "gemini-2.0-flash-exp"

[agents.researcher]
key = "$GEMINI_RESEARCH_KEY"
model = "gemini-1.5-pro"
```

### Same Provider, Different Endpoints

`.ccb/ccb.config`:
```toml
cmd; prod:codex, staging:codex

[agents.prod]
key = "$OPENAI_PROD_KEY"
url = "https://api.openai.com/v1"
model = "gpt-4o"

[agents.staging]
key = "$OPENAI_STAGING_KEY"
url = "https://staging.example.com/v1"
model = "gpt-4o-mini"
```

## Additional Resources

- **Project homepage**: https://github.com/SeemSeam/claude_codex_bridge
- **Community**: Linux.do forum (testing and feedback)
- **Contact**: bfly123@126.com, WeChat: seemseam-com
- **Provider CLIs**: Ensure Claude, Codex, Gemini, OpenCode, or Droid CLIs are installed separately

CCB is agent-orchestration infrastructure. It does not bundle agent CLIs—install them separately and configure their API keys via environment variables.
