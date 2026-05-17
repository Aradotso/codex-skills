---
name: codex-cli-delegation
description: Delegate coding tasks to OpenAI Codex CLI for automated analysis, refactoring, and multi-file editing workflows
triggers:
  - "use codex to analyze this code"
  - "delegate this task to codex"
  - "run codex on this repository"
  - "let codex refactor this"
  - "invoke codex for code analysis"
  - "start a codex session"
  - "ask codex to improve this"
  - "run codex exec on this project"
---

# Codex CLI Delegation

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

The Codex CLI is OpenAI's command-line tool for automated code analysis, refactoring, and editing. It provides both one-shot execution (`codex exec`) and interactive session modes for complex multi-file workflows. This skill enables AI agents to delegate sophisticated coding tasks to Codex, leveraging its specialized models for code understanding and transformation.

**Key capabilities:**
- Automated codebase analysis and suggestions
- Multi-file refactoring with git integration
- Context-aware code editing
- Repository-wide pattern detection
- Session-based iterative workflows

## Installation

### Prerequisites

The Codex CLI must be installed and configured before using this skill:

```bash
# Verify installation
codex --version

# If not installed, follow OpenAI's installation guide
# Typically: pip install openai-codex-cli
# or: npm install -g @openai/codex-cli

# Configure credentials
codex auth login
# or set environment variable
export OPENAI_API_KEY=your_key_here
```

Confirm the installation works:

```bash
codex exec "Hello from Codex"
```

## Core Commands

### One-Shot Execution

```bash
codex exec [options] "prompt"
```

**Essential options:**
- `-m, --model`: Model selection (`gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.3-codex-spark`, `gpt-5.3-codex`)
- `--config model_reasoning_effort=LEVEL`: Reasoning depth (`low`, `medium`, `high`)
- `--sandbox MODE`: Safety mode (`read-only`, `full`, `none`)
- `--full-auto`: Automatic execution without confirmation
- `--skip-git-repo-check`: Bypass git repository validation
- `--stream`: Stream output in real-time
- `--session ID`: Resume or create named session

### Session Management

```bash
# Start interactive session
codex session start

# Resume existing session
codex session resume <session-id>

# List sessions
codex session list

# Export session history
codex session export <session-id>
```

## Model Selection Guide

| Model | Use Case | Speed | Cost |
|-------|----------|-------|------|
| `gpt-5.5` | Complex refactoring, architecture | Slowest | Highest |
| `gpt-5.4` | Standard analysis, multi-file edits | Medium | Medium |
| `gpt-5.4-mini` | Quick fixes, simple tasks | Fast | Low |
| `gpt-5.3-codex-spark` | Rapid prototyping | Fastest | Lowest |
| `gpt-5.3-codex` | Legacy compatibility | Medium | Medium |

**Default recommendation:** `gpt-5.3-codex-spark` for most tasks, `gpt-5.4` for complex workflows.

## Reasoning Effort Levels

- **`low`**: Fast, surface-level analysis (15-30s)
- **`medium`**: Balanced depth and speed (30-90s) — **recommended default**
- **`high`**: Deep reasoning, comprehensive analysis (90s-5min)

## Sandbox Modes

- **`read-only`**: Analysis only, no file modifications — **safe default**
- **`full`**: Can read and write files (use with caution)
- **`none`**: No filesystem access (prompt-only mode)

## Common Patterns

### Repository Analysis

```bash
# Comprehensive codebase review
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="medium" \
  --sandbox read-only \
  --full-auto \
  --skip-git-repo-check \
  "Analyze this repository for code quality issues, architecture patterns, and suggest improvements" \
  2>/dev/null
```

### Refactoring Workflow

```bash
# Extract common patterns into reusable functions
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --sandbox full \
  --session refactor-session-1 \
  "Identify duplicated code in src/ and refactor into shared utilities. Preserve all functionality and add tests."
```

### Bug Investigation

```bash
# Debug specific issue with context
codex exec -m gpt-5.5 \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --stream \
  "Investigate the null pointer exception in user_service.py line 47. Trace the call chain and suggest fixes."
```

### Documentation Generation

```bash
# Generate comprehensive docs
codex exec -m gpt-5.4-mini \
  --config model_reasoning_effort="low" \
  --sandbox full \
  --full-auto \
  "Generate API documentation for all public functions in lib/. Use JSDoc format and include examples."
```

### Session-Based Iterative Work

```bash
# Start session for multi-step migration
codex session start --id migration-to-typescript

# Step 1
codex exec --session migration-to-typescript \
  "Convert src/utils/helpers.js to TypeScript with proper type definitions"

# Step 2 (continues context)
codex exec --session migration-to-typescript \
  "Update all imports of helpers.js to use the new TypeScript module"

# Review session history
codex session export migration-to-typescript
```

## Configuration

### Global Config File

Location: `~/.codex/config.yaml`

```yaml
# Default model
default_model: gpt-5.3-codex-spark

# Default reasoning effort
default_reasoning_effort: medium

# Default sandbox mode
default_sandbox: read-only

# Suppress thinking tokens (stderr) by default
suppress_thinking: true

# Auto-approve low-risk operations
auto_approve:
  - read-only
  - documentation

# Git integration
git:
  auto_commit: false
  commit_message_template: "Codex: {summary}"
```

### Environment Variables

```bash
# API credentials
export OPENAI_API_KEY=sk-...

# Override default model
export CODEX_DEFAULT_MODEL=gpt-5.4

# Set reasoning effort
export CODEX_REASONING_EFFORT=high

# Session storage directory
export CODEX_SESSION_DIR=~/.codex/sessions
```

## Working with Thinking Tokens

By default, this skill suppresses thinking tokens (Codex's internal reasoning on stderr) using `2>/dev/null` to avoid context pollution. 

**To view thinking tokens:**

```bash
# Remove stderr redirection
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  "Analyze this function"
# (stderr will show reasoning process)
```

**When to show thinking tokens:**
- Debugging unexpected Codex behavior
- Understanding complex analysis decisions
- Learning Codex's reasoning patterns
- Troubleshooting edge cases

## Real-World Examples

### Example 1: Migrate API Endpoints

```bash
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --sandbox full \
  --session api-migration \
  --skip-git-repo-check \
  "Migrate all REST endpoints in src/routes/ from Express to Fastify. Preserve middleware, error handling, and add Fastify schema validation." \
  2>/dev/null
```

### Example 2: Security Audit

```bash
codex exec -m gpt-5.5 \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --stream \
  "Perform a security audit of authentication logic. Check for: SQL injection, XSS, CSRF, insecure session handling, and hardcoded secrets." \
  2>/dev/null
```

### Example 3: Test Coverage Analysis

```bash
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="medium" \
  --sandbox read-only \
  --full-auto \
  "Analyze test coverage in tests/. Identify untested edge cases and suggest new test cases for critical paths." \
  2>/dev/null
```

### Example 4: Performance Optimization

```bash
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --sandbox full \
  --session perf-opt \
  "Profile the data processing pipeline in src/pipeline/. Identify bottlenecks and optimize for 10x throughput improvement. Add benchmarks." \
  2>/dev/null
```

## Troubleshooting

### Command Not Found

```bash
# Check PATH
which codex

# Reinstall if missing
pip install --upgrade openai-codex-cli
# or
npm install -g @openai/codex-cli
```

### Authentication Errors

```bash
# Re-authenticate
codex auth logout
codex auth login

# Or set API key directly
export OPENAI_API_KEY=sk-...
```

### Git Repository Errors

If Codex complains about missing git repository:

```bash
# Initialize git if needed
git init

# Or skip the check
codex exec --skip-git-repo-check "your prompt"
```

### Rate Limiting

```bash
# Check quota
codex quota

# Use cheaper model
codex exec -m gpt-5.4-mini --config model_reasoning_effort="low" "prompt"
```

### Session Corruption

```bash
# List sessions
codex session list

# Delete corrupted session
codex session delete <session-id>

# Clear all sessions
rm -rf ~/.codex/sessions/*
```

### Excessive Thinking Tokens

If context window fills with thinking tokens:

```bash
# Always suppress stderr for normal operation
codex exec "prompt" 2>/dev/null

# Use lower reasoning effort
codex exec --config model_reasoning_effort="low" "prompt"
```

## Best Practices

1. **Start with read-only**: Always use `--sandbox read-only` for analysis unless modifications are explicitly needed
2. **Choose appropriate models**: Use `gpt-5.4-mini` for simple tasks, `gpt-5.4` or `gpt-5.5` for complex work
3. **Use sessions for multi-step work**: Maintain context across related operations
4. **Suppress thinking tokens by default**: Add `2>/dev/null` unless debugging
5. **Be specific in prompts**: Include file paths, expected outcomes, and constraints
6. **Review before auto-approval**: Avoid `--full-auto` with `--sandbox full` for critical code
7. **Version control integration**: Commit before running Codex edits for easy rollback
8. **Monitor costs**: Check `codex quota` regularly when using premium models

## Integration Tips for AI Agents

When delegating to Codex:

1. **Ask for model preference**: If user doesn't specify, ask which model to use
2. **Ask for reasoning effort**: If user doesn't specify, ask for low/medium/high
3. **Default to safe modes**: Use `read-only` sandbox unless user requests edits
4. **Summarize outputs**: Codex can be verbose — extract key insights for the user
5. **Handle sessions intelligently**: Suggest session IDs for related multi-step tasks
6. **Expose thinking tokens on request**: If user asks "why did Codex decide X?", rerun without `2>/dev/null`
7. **Validate prerequisites**: Check `codex --version` before first use
