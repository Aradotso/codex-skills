---
name: codex-cli-best-practice
description: Guide to mastering Codex CLI through subagents, skills, workflows, MCP servers, and agentic engineering patterns
triggers:
  - "set up codex cli best practices"
  - "create a codex subagent"
  - "write a codex skill"
  - "configure codex mcp server"
  - "implement agentic workflow with codex"
  - "use codex orchestration pattern"
  - "add codex plugin marketplace"
  - "optimize codex configuration"
---

# codex-cli-best-practice

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

A comprehensive guide and reference implementation for Codex CLI best practices, covering the journey from vibe coding to agentic engineering. This skill teaches you how to leverage Codex CLI's advanced features: subagents, skills, MCP servers, workflows, and configuration patterns.

## What This Project Provides

**codex-cli-best-practice** is a reference repository that demonstrates:

- **Subagents**: Custom TOML-configured agents for parallel orchestration
- **Skills**: Reusable instruction packages with progressive disclosure
- **MCP Integration**: Model Context Protocol servers for external tool access
- **Workflows**: End-to-end patterns (Agent → Skill → Output)
- **Configuration**: Layered TOML config system with profiles and approval policies
- **Hooks**: Shell scripts that inject into the agentic loop
- **Memories**: Cross-session memory pipeline for context retention

## Installation

### Prerequisites

1. **Install Codex CLI** (requires Codex Pro subscription):
   ```bash
   # macOS
   brew install --cask codex-cli
   
   # Or download from https://developers.openai.com/codex/cli
   ```

2. **Clone this repository**:
   ```bash
   git clone https://github.com/shanraisshan/codex-cli-best-practice.git
   cd codex-cli-best-practice
   ```

3. **Initialize Codex in your project**:
   ```bash
   codex init
   ```

## Key Concepts & Configuration

### 1. Subagents (`.codex/agents/<name>.toml`)

Subagents are custom agents with dedicated role configs. Example weather agent:

```toml
# .codex/agents/weather-agent.toml
[agents.weather-agent]
model = "gpt-5.4"
instructions = """
You are a weather data specialist. When asked:
1. Extract location and units from user request
2. Fetch current weather from Open-Meteo API
3. Return structured data for downstream skills
"""
temperature = 0.7
max_tokens = 2000
```

Invoke with:
```bash
codex
> @weather-agent Get Dubai weather in Celsius
```

Global agent settings in `.codex/config.toml`:
```toml
[agents]
max_threads = 4
max_depth = 3
job_max_runtime_seconds = 300
```

### 2. Skills (`.agents/skills/<name>/SKILL.md`)

Skills are reusable instruction packages. Required structure:

```
.agents/skills/weather-svg-creator/
├── SKILL.md              # Core instructions with YAML frontmatter
├── scripts/              # Helper scripts
│   └── create_svg.py
├── references/           # Documentation
│   └── svg-spec.md
└── assets/              # Templates, images
    └── template.svg
```

**Example SKILL.md**:
```markdown
---
name: weather-svg-creator
description: Creates SVG weather cards from structured weather data
---

# Weather SVG Creator

You create beautiful SVG weather cards. When invoked:

1. Accept weather data (location, temp, condition, humidity)
2. Use scripts/create_svg.py to generate SVG
3. Output to specified path

## Usage Pattern

```python
# scripts/create_svg.py will be called with:
python scripts/create_svg.py \
  --location "Dubai" \
  --temp "32" \
  --condition "Sunny" \
  --output "weather.svg"
```
```

Invoke skills:
```bash
# Explicit
codex
> Use $weather-svg-creator to make a card for Dubai, 32°C, Sunny

# Implicit (by description match)
> Create an SVG weather card
```

### 3. MCP Servers (`.codex/config.toml`)

Connect external tools via Model Context Protocol:

```toml
# .codex/config.toml
[mcp_servers.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/Users/shan/projects"]
supports_parallel_tool_calls = true

[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
env = { GITHUB_PERSONAL_ACCESS_TOKEN = "${GITHUB_TOKEN}" }

[mcp_servers.weather]
command = "python"
args = ["-m", "mcp_server_weather"]
working_directory = ".codex/mcp-servers/weather"
```

Manage MCP servers:
```bash
# List available servers
codex mcp list

# Add new server
codex mcp add weather

# Test server
codex mcp get weather

# OAuth login (for supported servers)
codex mcp login github
```

### 4. Orchestration Workflow (Agent → Skill)

The canonical pattern from this repo:

```bash
codex
> Fetch the current weather for Dubai in Celsius and create the SVG weather card output using the repo.
```

**What happens**:
1. `@weather-agent` fetches data from Open-Meteo
2. Returns structured JSON: `{"location": "Dubai", "temp": 32, "condition": "Clear"}`
3. Codex matches `$weather-svg-creator` skill by description
4. Skill runs `scripts/create_svg.py` with data
5. SVG output saved and displayed

### 5. Configuration Layers

```toml
# .codex/config.toml
[features]
memories = true           # Cross-session memory
codex_hooks = true       # Enable hooks
fast_mode = false        # 1.5x speed mode

[approval_policy]
edits_outside_cwd = "prompt"
deletions = "prompt"
shell_commands = "auto_approve_safe"

[sandbox]
enabled = true
include_patterns = ["src/**", "tests/**"]
exclude_patterns = ["*.pyc", "__pycache__/**"]

[model]
default = "gpt-5.4"
review_model = "gpt-5.4-large-context"
temperature = 0.7

[memories]
max_tokens = 10000
collection_interval_seconds = 300

# Developer instructions (always included)
developer_instructions = """
Follow repo conventions:
- Use type hints in Python
- Run pytest before committing
- Update AGENTS.md for architectural changes
"""
```

### 6. Hooks (`.codex/hooks.json`)

Inject shell scripts into the agentic loop:

```json
{
  "hooks": {
    "before_edit": {
      "script": ".codex/hooks/lint-check.sh",
      "description": "Run linter before edits"
    },
    "after_shell": {
      "script": ".codex/hooks/log-command.sh",
      "description": "Log all shell commands"
    },
    "before_commit": {
      "script": ".codex/hooks/run-tests.sh",
      "description": "Run test suite"
    }
  }
}
```

Hook script example:
```bash
#!/bin/bash
# .codex/hooks/lint-check.sh

# Codex provides context via env vars:
# CODEX_HOOK_FILES, CODEX_HOOK_CONTEXT

for file in $CODEX_HOOK_FILES; do
  if [[ $file == *.py ]]; then
    ruff check "$file" || exit 1
  fi
done

exit 0
```

### 7. Plugins & Marketplace

Install plugin marketplaces:

```bash
# Add GitHub marketplace
codex plugin marketplace add github:openai/codex-plugins

# Add local marketplace
codex plugin marketplace add ~/my-plugins

# Browse installed plugins
codex
> /plugins

# Install specific plugin
codex plugin install security-scanner
```

Create a plugin (`.codex-plugin/plugin.json`):
```json
{
  "name": "my-workflow-plugin",
  "version": "1.0.0",
  "description": "Custom workflow automation",
  "skills": ["skills/planner", "skills/executor"],
  "mcp_servers": {
    "custom-api": {
      "command": "node",
      "args": ["mcp-server.js"]
    }
  }
}
```

### 8. Memories (Cross-Session Context)

Enable in config:
```toml
[features]
memories = true

[memories]
max_tokens = 10000
collection_interval_seconds = 300
```

Control via TUI:
```bash
codex
> /memories use      # Enable for this session
> /memories reset    # Clear all memories
```

Memories are user-scoped, not project-scoped.

## Common Workflows

### Create a New Subagent

```bash
codex
> Create a subagent called @api-designer that specializes in REST API design. 
  It should use gpt-5.4-large-context and follow OpenAPI 3.0 standards.
  Save to .codex/agents/api-designer.toml
```

### Create a New Skill

```bash
codex
> Use the $skill-creator to make a new skill called database-migrator.
  It should help write Alembic migrations for SQLAlchemy models.
  Include example migration scripts.
```

### Set Up MCP Server for Custom Tool

```python
# .codex/mcp-servers/weather/server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("weather-mcp")

@app.tool()
async def get_weather(location: str, units: str = "celsius"):
    """Fetch current weather for a location."""
    # Integration with Open-Meteo API
    import httpx
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": ...,
                "longitude": ...,
                "current_weather": "true",
                "temperature_unit": units
            }
        )
        return response.json()

if __name__ == "__main__":
    stdio_server(app)
```

Add to config:
```toml
[mcp_servers.weather]
command = "python"
args = [".codex/mcp-servers/weather/server.py"]
```

### Implement Agent → Skill Workflow

1. **Create the agent**:
```toml
# .codex/agents/data-fetcher.toml
[agents.data-fetcher]
model = "gpt-5.4"
instructions = "Fetch data from APIs and return structured JSON"
```

2. **Create the skill**:
```markdown
# .agents/skills/data-visualizer/SKILL.md
---
name: data-visualizer
description: Creates charts from JSON data
---

Accept JSON data and create matplotlib/plotly visualizations.
```

3. **Invoke**:
```bash
codex
> @data-fetcher get GitHub stars for shanraisshan/codex-cli-best-practice, 
  then $data-visualizer create a trend chart
```

### Enable Fast Mode

```bash
codex
> /fast on         # Enable 1.5x speed (2x credits)
> /fast status     # Check current mode
> /fast off        # Disable
```

Or in config:
```toml
[model]
service_tier = "fast"  # Always use fast mode
```

### Code Review Workflow

```bash
# Review uncommitted changes
codex
> /review

# Review specific branch
> /review main..feature-branch

# Review with custom instructions
> /review --instructions "Focus on security and performance"
```

Configure review model:
```toml
[model]
review_model = "gpt-5.4-large-context"
```

## Slash Commands Reference

| Command | Description |
|---------|-------------|
| `/plan` | Create execution plan before acting |
| `/fast on\|off\|status` | Toggle fast mode (1.5x speed) |
| `/fork` | Create parallel session branch |
| `/review [ref]` | Code review for changes/branch |
| `/status` | Show session info and token usage |
| `/mcp` | Manage MCP servers |
| `/agent <name>` | Switch to specific subagent |
| `/apps` | Manage connected applications |
| `/model` | Change model for session |
| `/permissions` | Manage approval policies |
| `/skills` | Browse and invoke skills |
| `/plugins` | Browse plugin marketplace |
| `/memories use\|reset` | Control memory system |

## Environment Variables

```bash
# Required
export OPENAI_API_KEY="sk-..."  # Codex Pro API key

# Optional
export CODEX_HOME="$HOME/.codex"  # Config directory
export GITHUB_TOKEN="ghp_..."     # For GitHub MCP server
export ANTHROPIC_API_KEY="sk-..." # For Claude models (if configured)
```

## Troubleshooting

### Subagent Not Found

**Issue**: `@my-agent not recognized`

**Solution**:
```bash
# Check agent config exists
ls .codex/agents/my-agent.toml

# Verify TOML syntax
codex config validate

# Restart codex session
codex
> /exit
codex
```

### Skill Not Triggering

**Issue**: Skill not invoked implicitly

**Solution**:
- Use explicit invoke: `$skill-name`
- Check skill description is specific enough
- Verify SKILL.md has valid YAML frontmatter
- Check `.agents/skills/` directory structure

### MCP Server Connection Failed

**Issue**: `MCP server 'xyz' not responding`

**Solution**:
```bash
# Test server directly
codex mcp get xyz

# Check server logs
cat ~/.codex/logs/mcp-xyz.log

# Verify command and args in config.toml
# Ensure env vars are set (use ${VAR} syntax)

# Restart server
codex mcp remove xyz
codex mcp add xyz
```

### Hooks Not Running

**Issue**: Hooks defined but not executing

**Solution**:
```toml
# Enable in config
[features]
codex_hooks = true
```

```bash
# Make scripts executable
chmod +x .codex/hooks/*.sh

# Test hook directly
.codex/hooks/my-hook.sh
```

### Memory Not Persisting

**Issue**: Context lost between sessions

**Solution**:
```bash
codex
> /memories use  # Enable for this thread

# Check feature flag
# In .codex/config.toml:
[features]
memories = true
```

### Approval Policy Too Restrictive

**Issue**: Every action requires approval

**Solution**:
```toml
[approval_policy]
shell_commands = "auto_approve_safe"  # Auto-approve safe commands
edits_outside_cwd = "auto_approve"    # Less restrictive
network_access = "auto_approve"       # For MCP servers

# Or use profiles
[profiles.dev]
approval_policy.shell_commands = "auto_approve_safe"
```

## Best Practices

1. **Start with `/plan`**: Let Codex create execution plans for complex tasks
2. **Use AGENTS.md**: Document project structure and conventions
3. **Namespace subagents**: Use descriptive names like `@api-designer` not `@api`
4. **Scope skills narrowly**: One skill = one clear responsibility
5. **Test MCP servers**: Use `codex mcp get` to verify before adding to workflow
6. **Layer configs**: Use profiles for different environments (dev, prod)
7. **Enable hooks selectively**: Start with `after_shell` for logging
8. **Review approval policy**: Balance security and automation
9. **Use memories sparingly**: Enable only for long-running projects
10. **Document workflows**: Create `.md` files showing Agent → Skill patterns

## Resources

- **Official Docs**: https://developers.openai.com/codex/overview
- **This Repo**: https://github.com/shanraisshan/codex-cli-best-practice
- **MCP Spec**: https://modelcontextprotocol.io
- **Community Skills**: https://github.com/topics/codex-cli-skills
- **Plugin Marketplace**: Built into Codex CLI (`/plugins`)
