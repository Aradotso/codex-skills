---
name: codex-cli-delegation
description: Delegate complex code analysis, refactoring, and editing tasks to OpenAI Codex CLI from within Claude Code
triggers:
  - "use codex to analyze this code"
  - "delegate this to codex"
  - "run codex on this repository"
  - "ask codex to refactor this"
  - "start a codex session"
  - "execute this with codex"
  - "use codex for code review"
  - "invoke codex cli"
---

# Codex CLI Delegation

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

The Codex CLI (`codex`) is a command-line tool that enables automated code analysis, refactoring, editing, and agentic workflows using OpenAI's GPT models with specialized code-understanding capabilities. This skill enables AI coding agents to delegate tasks to Codex for multi-file operations, complex refactoring, and autonomous code editing.

**Key capabilities:**
- Execute one-off prompts with `codex exec`
- Resume interactive sessions with context persistence
- Multi-file code analysis and editing
- Automated git integration and safety checks
- Configurable sandbox modes (read-only, edit, full)
- Model selection and reasoning effort tuning

## Prerequisites

Verify Codex is installed and configured:

```bash
codex --version
```

If not installed, follow [Codex installation instructions](https://github.com/openai/codex-cli) and configure credentials:

```bash
# Set OpenAI API key
export OPENAI_API_KEY="${OPENAI_API_KEY}"

# Verify configuration
codex config show
```

## Installation

This skill is typically installed via Claude Code's plugin system:

```bash
/plugin marketplace add skills-directory/skill-codex
/plugin install skill-codex@skill-codex
```

Or as a standalone skill:

```bash
git clone --depth 1 git@github.com:skills-directory/skill-codex.git /tmp/skills-temp && \
mkdir -p ~/.claude/skills && \
cp -r /tmp/skills-temp/plugins/skill-codex/skills/codex ~/.claude/skills/codex && \
rm -rf /tmp/skills-temp
```

## Core Commands

### `codex exec`

Execute a one-off prompt with full configuration control:

```bash
# Basic execution
codex exec "Analyze error handling patterns in this codebase"

# With model selection
codex exec -m gpt-5.3-codex-spark "Refactor authentication module"

# With reasoning effort
codex exec --config model_reasoning_effort="high" "Find performance bottlenecks"

# With sandbox mode
codex exec --sandbox read-only "Review code quality"
codex exec --sandbox edit "Add type hints to Python files"
codex exec --sandbox full "Refactor and run tests"

# Full automation mode
codex exec --full-auto --skip-git-repo-check "Analyze this repository"

# Suppress thinking tokens (recommended for Claude Code context)
codex exec "Your prompt" 2>/dev/null
```

### Session Resume

Continue previous Codex sessions with context:

```bash
# List available sessions
codex sessions list

# Resume a specific session
codex resume <session-id>

# Resume with additional prompt
codex resume <session-id> "Continue with the refactoring we discussed"
```

## Model Selection

Choose the appropriate model for your task:

| Model | Best For | Reasoning |
|-------|----------|-----------|
| `gpt-5.5` | Most complex tasks, architectural decisions | Highest |
| `gpt-5.4` | Advanced refactoring, multi-file analysis | High |
| `gpt-5.4-mini` | Faster analysis, simpler edits | Medium |
| `gpt-5.3-codex-spark` | Quick code review, rapid prototyping | Low-Medium |
| `gpt-5.3-codex` | Standard code operations | Low |

Example:

```bash
# For complex architectural analysis
codex exec -m gpt-5.5 --config model_reasoning_effort="high" \
  "Design a plugin system for this application"

# For quick code review
codex exec -m gpt-5.3-codex-spark --config model_reasoning_effort="low" \
  "Check for security issues in authentication"
```

## Reasoning Effort Levels

Control computational depth:

- **`low`**: Fast, surface-level analysis
- **`medium`**: Balanced speed and depth
- **`high`**: Deep reasoning, comprehensive analysis

```bash
codex exec --config model_reasoning_effort="high" \
  "Analyze concurrency patterns and race conditions"
```

## Sandbox Modes

Control Codex's file system access:

- **`read-only`**: Analysis only, no modifications
- **`edit`**: Can modify files but limited execution
- **`full`**: Full file system and execution access

```bash
# Safe analysis
codex exec --sandbox read-only "Audit this codebase"

# Controlled editing
codex exec --sandbox edit "Add error handling to all API calls"

# Full automation (use with caution)
codex exec --sandbox full --full-auto "Implement feature X with tests"
```

## Common Workflows

### Code Analysis

```bash
# Comprehensive repository analysis
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --full-auto \
  "Analyze this repository comprehensively: architecture, patterns, code quality, potential improvements" \
  2>/dev/null

# Security audit
codex exec -m gpt-5.5 \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  "Perform security audit focusing on authentication, authorization, and data validation" \
  2>/dev/null
```

### Refactoring

```bash
# Extract reusable components
codex exec -m gpt-5.4 \
  --sandbox edit \
  "Identify duplicated code and extract into reusable functions" \
  2>/dev/null

# Type safety improvements
codex exec -m gpt-5.3-codex-spark \
  --sandbox edit \
  "Add TypeScript type annotations to all exported functions" \
  2>/dev/null
```

### Feature Implementation

```bash
# Implement with tests
codex exec -m gpt-5.5 \
  --config model_reasoning_effort="high" \
  --sandbox full \
  --full-auto \
  "Implement user authentication with JWT tokens, including unit tests and integration tests" \
  2>/dev/null
```

### Documentation

```bash
# Generate comprehensive docs
codex exec -m gpt-5.4 \
  --sandbox edit \
  "Add JSDoc comments to all public APIs and update README with usage examples" \
  2>/dev/null
```

## Configuration

### Environment Variables

```bash
# OpenAI API key (required)
export OPENAI_API_KEY="${OPENAI_API_KEY}"

# Codex configuration directory (optional)
export CODEX_CONFIG_DIR="${HOME}/.config/codex"
```

### Global Config File

Located at `~/.config/codex/config.yaml`:

```yaml
default_model: gpt-5.4
default_reasoning_effort: medium
default_sandbox: edit
auto_git_check: true
thinking_tokens: false
```

### Per-Execution Config

```bash
# Override config for single execution
codex exec \
  --config model_reasoning_effort="high" \
  --config auto_git_check="false" \
  "Your prompt here"
```

## Thinking Tokens

By default, this skill suppresses Codex's reasoning output (stderr) to avoid bloating context:

```bash
# Suppressed (default for Claude Code)
codex exec "Analyze code" 2>/dev/null

# Show thinking tokens for debugging
codex exec "Analyze code"
```

**When to show thinking tokens:**
- Debugging Codex behavior
- Understanding complex analysis decisions
- Learning from Codex's reasoning process

## Safety and Git Integration

Codex includes built-in safety checks:

```bash
# Requires clean git state (recommended)
codex exec --sandbox edit "Refactor module"

# Skip git check (use with caution)
codex exec --sandbox edit --skip-git-repo-check "Quick fix"

# Full automation without prompts
codex exec --full-auto --skip-git-repo-check "Automated task"
```

**Best practices:**
1. Always work in a git repository with committed changes
2. Use `read-only` sandbox for analysis
3. Review changes before committing
4. Use `--full-auto` only for well-defined, low-risk tasks

## Error Handling

### Common Issues

**API Key Not Set:**
```bash
Error: OPENAI_API_KEY not found
```
Solution:
```bash
export OPENAI_API_KEY="${OPENAI_API_KEY}"
```

**Codex Not Found:**
```bash
codex: command not found
```
Solution: Install Codex CLI and ensure it's in PATH

**Git Repository Required:**
```bash
Error: Not a git repository
```
Solution: Initialize git or use `--skip-git-repo-check`

**Rate Limiting:**
```bash
Error: Rate limit exceeded
```
Solution: Reduce reasoning effort or switch to a faster model

## Integration with Claude Code

When delegating to Codex from Claude Code:

1. **Ask for clarification** on model and reasoning effort if not specified
2. **Default to `read-only` sandbox** for analysis tasks
3. **Suppress thinking tokens** unless explicitly requested: `2>/dev/null`
4. **Summarize Codex output** rather than showing raw responses
5. **Offer follow-up actions** based on Codex results

Example integration pattern:

```python
# In Claude Code skill activation
def invoke_codex(prompt, model=None, reasoning=None, sandbox="read-only"):
    # Confirm model selection
    if model is None:
        # Ask user: "Which model? gpt-5.5, gpt-5.4, gpt-5.4-mini, gpt-5.3-codex-spark, gpt-5.3-codex"
        model = get_user_choice()
    
    # Confirm reasoning effort
    if reasoning is None:
        # Ask user: "Reasoning effort? low, medium, high"
        reasoning = get_user_choice()
    
    # Build command
    cmd = f'codex exec -m {model} --config model_reasoning_effort="{reasoning}" --sandbox {sandbox} --full-auto --skip-git-repo-check "{prompt}" 2>/dev/null'
    
    # Execute and return results
    return execute_command(cmd)
```

## Advanced Patterns

### Iterative Refinement

```bash
# Initial analysis
codex exec -m gpt-5.4 "Analyze authentication module" > analysis.txt

# Resume with refinements
SESSION_ID=$(codex sessions list | head -1 | awk '{print $1}')
codex resume $SESSION_ID "Focus on OAuth2 implementation details"
```

### Multi-Stage Workflows

```bash
# Stage 1: Analysis (read-only)
codex exec --sandbox read-only \
  "Identify components that need refactoring" > refactor-plan.txt

# Stage 2: Refactoring (edit)
codex exec --sandbox edit \
  "Refactor components listed in refactor-plan.txt"

# Stage 3: Testing (full)
codex exec --sandbox full \
  "Run test suite and fix any failures"
```

### Combining with Shell Scripts

```bash
#!/bin/bash
# automated-review.sh

echo "Starting Codex code review..."

# Security audit
codex exec -m gpt-5.5 \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  "Security audit focusing on OWASP Top 10" \
  2>/dev/null > security-report.md

# Code quality
codex exec -m gpt-5.4 \
  --sandbox read-only \
  "Code quality analysis: complexity, maintainability, test coverage" \
  2>/dev/null > quality-report.md

echo "Reports generated: security-report.md, quality-report.md"
```

## Troubleshooting

### Performance Issues

If Codex is slow:
- Use lower reasoning effort: `--config model_reasoning_effort="low"`
- Switch to faster model: `-m gpt-5.3-codex-spark`
- Narrow the scope of your prompt

### Context Window Limits

If hitting context limits:
- Break large tasks into smaller prompts
- Use `--sandbox read-only` to limit file scanning
- Exclude large dependencies or build artifacts

### Inconsistent Results

If results vary significantly:
- Increase reasoning effort for more consistent analysis
- Use `gpt-5.5` or `gpt-5.4` for complex tasks
- Provide more specific, detailed prompts

## Resources

- [Codex CLI Documentation](https://github.com/openai/codex-cli)
- [Model Comparison Guide](https://platform.openai.com/docs/models)
- [Agentic Workflows with ralph-meets-rex](https://github.com/klaudworks/ralph-meets-rex)
