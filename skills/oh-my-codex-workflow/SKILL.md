---
name: oh-my-codex-workflow
description: Expert in Oh My Codex (OMX) - workflow layer for OpenAI Codex CLI with agents, skills, and team coordination
triggers:
  - set up oh my codex for this project
  - start an omx workflow with deep interview
  - create a team execution plan with omx
  - configure omx agents and skills
  - troubleshoot my omx installation
  - run omx ralph for persistent completion
  - use omx team runtime with tmux
  - integrate omx with codex cli
---

# Oh My Codex (OMX) Workflow

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## What OMX Does

Oh My Codex (OMX) is a workflow layer for OpenAI Codex CLI that enhances the base Codex experience with:

- **Canonical workflow**: `$deep-interview` → `$ralplan` → `$ralph` or `$team`
- **Agent teams**: Coordinated parallel execution with tmux-backed worktrees
- **Persistent state**: Plans, logs, memory, and mode tracking in `.omx/`
- **Role keywords**: Reusable specialist roles (executor, architect, reviewer, etc.)
- **Skills system**: Installable workflows like `$deep-interview`, `$ralplan`, `$team`, `$ralph`
- **Project guidance**: Scoped `AGENTS.md` for project-specific context
- **Runtime hooks**: Native Codex lifecycle integration via `.codex/hooks.json`

OMX keeps Codex as the execution engine and adds better task routing, workflow orchestration, and runtime support around it.

## Installation

### Prerequisites

- Node.js 20+
- Codex CLI: `npm install -g @openai/codex`
- Configured Codex auth (check with `codex login status`)
- `tmux` on macOS/Linux for team runtime (optional but recommended)

### Install OMX

```bash
# Install both Codex CLI and OMX globally
npm install -g @openai/codex oh-my-codex

# Run setup to install prompts, skills, hooks, and scaffolding
omx setup

# Verify installation
omx doctor

# Smoke test actual Codex execution
omx exec --skip-git-repo-check -C . "Reply with exactly OMX-EXEC-OK"
```

### Update OMX

```bash
# Check npm, install latest, and refresh setup
omx update

# Or manually:
npm install -g oh-my-codex
omx setup
```

## Core Workflow

### The Recommended Path

```bash
# 1. Launch OMX with recommended settings
omx --madmax --high

# Inside the Codex session:
# 2. Clarify scope (when boundaries are unclear)
$deep-interview "clarify the authentication change"

# 3. Create and approve implementation plan
$ralplan "approve the auth plan and review tradeoffs"

# 4a. Execute with persistent completion loop
$ralph "carry the approved plan to completion"

# OR 4b. Execute with coordinated parallel team
$team 3:executor "execute the approved plan in parallel"

# 5. Convert to durable goals (for multi-session work)
$ultragoal "turn this launch into durable Codex goals"
```

### Launch Modes

```bash
# Default: auto-managed tmux on macOS/Linux interactive terminals
omx --madmax --high

# Direct mode (no OMX tmux/HUD management)
omx --direct --yolo

# Set persistent preference via environment
export OMX_LAUNCH_POLICY=direct  # or tmux, detached-tmux, auto
omx --yolo

# CLI flags override environment (last flag wins)
OMX_LAUNCH_POLICY=direct omx --tmux --yolo  # Uses tmux
```

## Canonical Skills

### $deep-interview

Clarify intent, boundaries, and non-goals when the request is vague.

```text
$deep-interview "clarify requirements for the new API endpoint"
$deep-interview "understand the performance bottleneck before planning fixes"
```

### $ralplan

Turn clarified scope into an approved architecture and implementation plan.

```text
$ralplan "approve the implementation plan and review tradeoffs"
$ralplan "verify the migration strategy is safe"
```

### $ralph

Persistent completion loop - one owner keeps pushing until done.

```text
$ralph "carry the approved plan to completion"
$ralph "implement the auth changes with verification"
```

### $team

Coordinated parallel execution with tmux-backed worktrees.

```text
# Launch team with N agents of role:type
$team 3:executor "execute the approved plan in parallel"
$team 2:architect "design the new service architecture"

# Team management (CLI, not in-session)
omx team status <team-name>
omx team resume <team-name>
omx team shutdown <team-name>
```

### $ultragoal

Convert a launch session into durable Codex goals for multi-session work.

```text
$ultragoal "turn this migration into sequential Codex goals"
```

## Project Structure

OMX creates and manages these directories:

```
.omx/
├── plans/           # Approved implementation plans from $ralplan
├── logs/            # Execution logs from $ralph and $team
├── memory/          # Persistent agent memory
├── ultragoal/       # Durable multi-goal artifacts
└── teams/           # Team runtime state and worktrees

.codex/
├── config.toml      # Codex configuration (OMX seeds defaults)
├── hooks.json       # Native Codex hooks (OMX-managed wrappers)
└── prompts/         # OMX-installed role and skill prompts

AGENTS.md            # Project-specific agent guidance (optional)
```

## Configuration

### Model and Environment Routing

Edit `.omx-config.json` for model/env routing (only use keys supported by your OMX version):

```json
{
  "model": "gpt-5.5",
  "provider": "openai",
  "baseURL": "https://api.openai.com/v1",
  "env": {
    "OPENAI_API_KEY": "${OPENAI_API_KEY}"
  }
}
```

See [model/env routing reference](https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/reference/omx-config-schema-routing.md) for details.

### Codex Config Seeding

OMX seeds `.codex/config.toml` with recommended defaults for `gpt-5.5`:

```toml
[gpt-5.5]
model_name = "gpt-5.5"
model_context_window = 250000
model_auto_compact_token_limit = 200000
```

### AGENTS.md Merge

Preserve existing project guidance while adding OMX sections:

```bash
# Merge mode: inserts between <!-- OMX:AGENTS:START --> / END -->
omx setup --merge-agents

# Default: skips existing AGENTS.md in non-interactive mode
omx setup
```

## Common Patterns

### Standard Workflow

```typescript
// TypeScript example: typical OMX workflow pattern
async function standardWorkflow() {
  // 1. Clarify scope
  // Run: $deep-interview "understand the feature requirements"
  
  // 2. Create plan
  // Run: $ralplan "approve the implementation approach"
  
  // 3. Execute
  // Option A - single persistent owner:
  // Run: $ralph "implement with verification"
  
  // Option B - parallel team:
  // Run: $team 3:executor "execute in parallel"
  
  // 4. Convert to goals for multi-session work
  // Run: $ultragoal "create durable goals for remaining work"
}
```

### Team Execution

```bash
# Launch team from CLI
omx team 3:executor "migrate database schema with verification"

# Check team status
omx team status migration-team

# Resume paused team
omx team resume migration-team

# Clean shutdown
omx team shutdown migration-team
```

### Direct Codex Exec

```typescript
// Use omx exec for one-off Codex calls outside a session
import { execSync } from 'child_process';

const result = execSync(
  'omx exec --skip-git-repo-check -C . "List all TypeScript files in src/"',
  { encoding: 'utf-8' }
);

console.log(result);
```

### Custom Skill Creation

```bash
# Skills are stored in .codex/prompts/skills/
# Create a new skill file:
# .codex/prompts/skills/my-custom-skill.md

# Content structure:
# ---
# name: my-custom-skill
# triggers:
#   - do custom thing
# ---
# # Skill instructions
# When invoked, this skill should...
```

## CLI Commands

### Setup and Verification

```bash
omx setup                    # Install prompts, skills, hooks, scaffolding
omx setup --merge-agents     # Preserve existing AGENTS.md while adding OMX sections
omx setup --force            # Force overwrite existing files
omx doctor                   # Verify installation integrity
omx update                   # Check npm, install latest, refresh setup
omx uninstall                # Remove OMX-managed hooks (keep user hooks)
```

### Launch

```bash
omx --madmax --high          # Recommended default
omx --yolo                   # Quick launch, less safety
omx --direct --yolo          # No OMX tmux management
omx --tmux                   # Force tmux mode
```

### Execution

```bash
omx exec [options] "prompt"                    # Direct Codex execution
omx exec --skip-git-repo-check -C . "prompt"   # Skip git repo requirement
```

### Team Runtime

```bash
omx team N:role "task"       # Launch N agents of role:type
omx team status <name>       # Check team status
omx team resume <name>       # Resume paused team
omx team shutdown <name>     # Clean shutdown
omx team list                # List active teams
```

### Monitoring

```bash
omx hud --watch              # Launch monitoring HUD (operator surface)
```

## Environment Variables

```bash
# Launch policy preference
export OMX_LAUNCH_POLICY=direct    # direct, tmux, detached-tmux, auto

# Codex home (affects plugin cache location)
export CODEX_HOME=~/.codex

# API keys (referenced in .omx-config.json)
export OPENAI_API_KEY=your_key_here
export ANTHROPIC_API_KEY=your_key_here
```

## Troubleshooting

### Installation Issues

```bash
# Verify setup
omx doctor

# Check Codex auth
codex login status

# Smoke test actual execution
omx exec --skip-git-repo-check -C . "Reply with exactly OMX-EXEC-OK"

# Refresh setup after version bump
omx setup

# Or use update to check npm first
omx update
```

### Team Runtime Issues

```bash
# Verify tmux is installed
which tmux

# Check team status
omx team status <team-name>

# Review team logs
cat .omx/teams/<team-name>/logs/*

# Clean shutdown if stuck
omx team shutdown <team-name>
```

### Hook Issues

```bash
# Verify hooks are registered
cat .codex/hooks.json

# Refresh OMX-managed hooks (preserves user hooks)
omx setup

# Check hook execution logs
cat .omx/logs/hooks/*
```

### Model/Provider Issues

```bash
# Verify .omx-config.json routing
cat .omx-config.json

# Check Codex config
cat .codex/config.toml

# Test with direct exec
omx exec --skip-git-repo-check -C . "test prompt"

# Verify env vars are set
echo $OPENAI_API_KEY
```

### Common Errors

**Error: Codex not found**
```bash
npm install -g @openai/codex
```

**Error: Auth failed**
```bash
codex login
codex login status
```

**Error: tmux not found (team runtime)**
```bash
# macOS
brew install tmux

# Linux
sudo apt-get install tmux  # or yum, dnf, etc.
```

**Error: Setup refresh skips AGENTS.md**
```bash
# Use merge mode to preserve existing content
omx setup --merge-agents

# Or force overwrite
omx setup --force
```

## Advanced Usage

### Plugin Mode vs Setup Mode

OMX ships both as npm package (setup mode) and Codex plugin (plugin mode):

**Setup mode** (recommended):
```bash
npm install -g oh-my-codex
omx setup
```
- Installs native agents and prompts
- Manages `.codex/hooks.json` wrappers
- Full runtime integration

**Plugin mode**:
- Install via Codex plugin marketplace
- Bundles skills in plugin manifest
- Optional MCP compatibility (disabled by default)
- Removes legacy OMX-managed prompts to avoid shadowing
- Native/runtime hooks still setup-owned
- Not a replacement for full OMX setup

### Custom Agent Roles

Create custom roles in `.codex/prompts/agents/`:

```markdown
---
name: security-reviewer
role: Security Review Specialist
---

# Security Reviewer Agent

You are a security review specialist. When assigned a task:

1. Review code for security vulnerabilities
2. Check for OWASP top 10 issues
3. Validate input sanitization
4. Review authentication/authorization
5. Document findings with severity levels
```

### Integration with Other Tools

```bash
# Use OMX in CI/CD
omx exec --skip-git-repo-check -C . "Run security audit on changed files"

# Integrate with git hooks
# .git/hooks/pre-commit
#!/bin/bash
omx exec -C . "Review staged changes for issues"
```

## Best Practices

1. **Start with clarification**: Use `$deep-interview` when scope is unclear
2. **Approve plans explicitly**: Always run `$ralplan` before execution
3. **Choose the right execution mode**: `$ralph` for persistent loops, `$team` for parallel work
4. **Use durable goals**: Run `$ultragoal` for multi-session work
5. **Review `.omx/` artifacts**: Check plans and logs for context
6. **Keep AGENTS.md updated**: Maintain project-specific guidance
7. **Verify with `omx doctor`**: Run after setup or when issues arise
8. **Test with `omx exec`**: Smoke test auth and execution before workflows

## Resources

- **Website**: https://oh-my-codex.dev
- **GitHub**: https://github.com/Yeachan-Heo/oh-my-codex
- **Discord**: https://discord.gg/PUwSMR9XNk
- **Documentation**: 
  - [Getting Started](https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/getting-started.html)
  - [Agents](https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/agents.html)
  - [Skills](https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/skills.html)
  - [Model/Env Routing](https://github.com/Yeachan-Heo/oh-my-codex/blob/main/docs/reference/omx-config-schema-routing.md)
