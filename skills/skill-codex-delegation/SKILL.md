---
name: skill-codex-delegation
description: Delegate coding tasks from Claude Code to OpenAI Codex CLI for autonomous code analysis, refactoring, and multi-file editing workflows
triggers:
  - "use codex to analyze this codebase"
  - "delegate this refactoring to codex"
  - "run codex exec on this project"
  - "have codex review and improve this code"
  - "use codex with reasoning effort to solve this"
  - "start a codex session for this task"
  - "invoke codex cli for automated editing"
  - "run codex in sandbox mode"
---

# Codex Delegation Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

**skill-codex** enables Claude Code (or other AI coding agents) to delegate complex coding tasks to the OpenAI Codex CLI. This is useful when you need autonomous multi-file editing, deep code analysis, or refactoring workflows that benefit from Codex's specialized reasoning models.

The Codex CLI supports:
- Multiple GPT models (gpt-5.5, gpt-5.4, gpt-5.3-codex-spark, etc.)
- Adjustable reasoning effort levels (low, medium, high)
- Sandbox modes (read-only, docker, off) for safe execution
- Session resumption for iterative workflows
- Full automation mode for autonomous task completion

## Installation

### Prerequisites

1. **Install Codex CLI:**
   ```bash
   # Installation method depends on your OS
   # Verify installation:
   codex --version
   ```

2. **Configure Codex credentials:**
   ```bash
   # Set up API keys (use environment variables)
   export OPENAI_API_KEY=your_api_key_here
   
   # Or configure via codex config
   codex config set api_key $OPENAI_API_KEY
   ```

3. **Verify installation:**
   ```bash
   codex --version
   # Should output version info without errors
   ```

### Install as Claude Code Plugin (Recommended)

```bash
/plugin marketplace add skills-directory/skill-codex
/plugin install skill-codex@skill-codex
```

### Install as Standalone Skill

```bash
git clone --depth 1 https://github.com/skills-directory/skill-codex.git /tmp/skills-temp && \
mkdir -p ~/.claude/skills && \
cp -r /tmp/skills-temp/plugins/skill-codex/skills/codex ~/.claude/skills/codex && \
rm -rf /tmp/skills-temp
```

## Key Commands

### Basic Execution

```bash
# Simple execution with default model
codex exec "analyze this codebase and suggest improvements"

# Specify model
codex exec -m gpt-5.3-codex-spark "refactor this module for better performance"

# With reasoning effort
codex exec -m gpt-5.4 --config model_reasoning_effort="high" "complex architectural review"
```

### Sandbox Modes

```bash
# Read-only (safe for analysis)
codex exec --sandbox read-only "analyze code quality"

# Docker sandbox (isolated execution)
codex exec --sandbox docker "run tests and fix failing ones"

# No sandbox (full file system access)
codex exec --sandbox off "update configuration files"
```

### Full Automation Mode

```bash
# Autonomous execution without prompts
codex exec --full-auto --skip-git-repo-check \
  "implement user authentication feature"
```

### Session Management

```bash
# Resume last session
codex resume

# Resume specific session
codex resume --session abc123

# List sessions
codex sessions list
```

## Configuration

### Model Selection

Available models (as of documentation):
- `gpt-5.5` - Latest flagship model
- `gpt-5.4` - Previous generation flagship
- `gpt-5.4-mini` - Faster, cost-effective option
- `gpt-5.3-codex-spark` - Specialized for code with enhanced reasoning
- `gpt-5.3-codex` - Code-specialized model

### Reasoning Effort Levels

- `low` - Fast responses, basic reasoning
- `medium` - Balanced reasoning and speed (default)
- `high` - Deep analysis, slower but more thorough

### Common Configurations

```bash
# Set default model
codex config set default_model gpt-5.3-codex-spark

# Set default reasoning effort
codex config set model_reasoning_effort medium

# Set default sandbox mode
codex config set sandbox_mode read-only
```

## Usage Patterns

### Pattern 1: Code Analysis

When user asks: *"analyze this codebase for security issues"*

```bash
codex exec -m gpt-5.3-codex-spark \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --full-auto \
  --skip-git-repo-check \
  "Perform comprehensive security audit of this codebase. Identify: 1) SQL injection risks, 2) XSS vulnerabilities, 3) insecure dependencies, 4) authentication weaknesses. Provide specific file locations and remediation steps." 2>/dev/null
```

**Note:** `2>/dev/null` suppresses thinking tokens (stderr). Omit to see Codex's reasoning process.

### Pattern 2: Refactoring Workflow

When user asks: *"refactor this module to use dependency injection"*

```bash
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="medium" \
  --sandbox docker \
  --full-auto \
  "Refactor src/services/user-service.js to use dependency injection pattern. Update all imports, add constructor injection, create service container. Maintain backward compatibility." 2>/dev/null
```

### Pattern 3: Feature Implementation

When user asks: *"add rate limiting to the API"*

```bash
codex exec -m gpt-5.5 \
  --config model_reasoning_effort="high" \
  --sandbox off \
  --full-auto \
  "Implement rate limiting middleware for Express API. Requirements: 1) Redis-based storage, 2) configurable limits per endpoint, 3) proper error responses, 4) unit tests. Update routes and add documentation." 2>/dev/null
```

### Pattern 4: Session Resume for Iterative Work

```bash
# Initial task
codex exec -m gpt-5.3-codex-spark "create REST API for user management"

# Review output, then resume to iterate
codex resume
# User provides feedback in the resumed session
```

### Pattern 5: Multi-File Editing

When user asks: *"update all components to use the new theme system"*

```bash
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="medium" \
  --sandbox docker \
  --full-auto \
  --skip-git-repo-check \
  "Update all React components in src/components/ to use the new theme system from src/styles/theme.js. Replace hardcoded colors with theme tokens. Update imports. Preserve all functionality." 2>/dev/null
```

## Real-World Examples

### Example 1: Repository Analysis

```bash
# User prompt: "Use codex to analyze this repo and suggest improvements"
# Agent execution:

codex exec -m gpt-5.3-codex-spark \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --full-auto \
  --skip-git-repo-check \
  "Analyze this repository comprehensively:
  
1. Code Quality: Identify code smells, duplication, complexity issues
2. Architecture: Assess structure, separation of concerns, modularity
3. Performance: Find bottlenecks, inefficient algorithms, optimization opportunities
4. Testing: Evaluate test coverage, quality, missing test cases
5. Documentation: Review README, inline comments, API docs completeness
6. Security: Check for common vulnerabilities, insecure patterns
7. Dependencies: Review package.json for outdated or risky dependencies

Provide actionable recommendations prioritized by impact." 2>/dev/null
```

### Example 2: TypeScript Migration

```bash
# User prompt: "migrate this JavaScript project to TypeScript"

codex exec -m gpt-5.5 \
  --config model_reasoning_effort="high" \
  --sandbox docker \
  --full-auto \
  "Migrate this JavaScript project to TypeScript:

1. Add tsconfig.json with appropriate settings
2. Rename .js files to .ts/.tsx
3. Add type annotations to all functions and variables
4. Create interface definitions for data structures
5. Fix all type errors
6. Update package.json scripts for TypeScript compilation
7. Ensure all tests pass after migration

Prioritize type safety while maintaining code clarity." 2>/dev/null
```

### Example 3: Performance Optimization

```bash
# User prompt: "optimize database queries in this service"

codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --full-auto \
  "Analyze and optimize database queries in src/services/:

1. Identify N+1 query problems
2. Find missing indexes
3. Detect inefficient joins or subqueries
4. Suggest query refactoring for better performance
5. Recommend caching strategies
6. Provide benchmarking approach

Focus on src/services/order-service.js and src/services/product-service.js" 2>/dev/null
```

## Delegation Workflow

When delegating to Codex from Claude Code:

1. **Assess Task Complexity**: Determine if Codex delegation is appropriate
2. **Select Model**: Choose based on task complexity and speed requirements
3. **Set Reasoning Effort**: 
   - `low` for simple tasks
   - `medium` for standard refactoring
   - `high` for architectural changes or complex analysis
4. **Choose Sandbox Mode**:
   - `read-only` for analysis tasks
   - `docker` for code changes (safe isolation)
   - `off` for config file updates or when docker isn't available
5. **Execute with Full Auto**: Use `--full-auto --skip-git-repo-check` for autonomous completion
6. **Suppress/Show Thinking**: Use `2>/dev/null` to hide reasoning, omit to show

## Troubleshooting

### Codex Command Not Found

```bash
# Verify installation
which codex

# Add to PATH if needed
export PATH=$PATH:/path/to/codex/bin

# Verify again
codex --version
```

### Authentication Errors

```bash
# Check API key is set
echo $OPENAI_API_KEY

# If empty, set it
export OPENAI_API_KEY=your_key_here

# Or configure via codex
codex config set api_key $OPENAI_API_KEY
```

### Session Resume Fails

```bash
# List available sessions
codex sessions list

# Resume specific session by ID
codex resume --session <session_id>

# Start fresh if session is corrupted
codex exec "continue previous task: [describe task]"
```

### Thinking Tokens Overflow Context

Always use `2>/dev/null` to suppress stderr (thinking tokens) unless debugging:

```bash
# Good - suppresses thinking
codex exec "task" 2>/dev/null

# Only for debugging - shows thinking
codex exec "task"
```

### Docker Sandbox Issues

```bash
# Verify Docker is running
docker ps

# Use read-only sandbox if Docker unavailable
codex exec --sandbox read-only "task"

# Or disable sandbox (use cautiously)
codex exec --sandbox off "task"
```

### Model Not Available

```bash
# List available models
codex models list

# Use fallback model if preferred isn't available
codex exec -m gpt-5.4-mini "task"
```

## Best Practices

1. **Always verify Codex installation** before delegating tasks
2. **Use read-only sandbox** for analysis tasks to prevent accidental changes
3. **Suppress thinking tokens** (`2>/dev/null`) to avoid context overflow
4. **Choose appropriate reasoning effort** - high for complex tasks, low for simple ones
5. **Resume sessions** for iterative refinement rather than starting fresh
6. **Provide detailed prompts** - Codex performs better with clear, structured instructions
7. **Use full-auto mode** for autonomous completion without interruptions
8. **Review Codex output** before applying changes to critical code

## Environment Variables

```bash
# Required
export OPENAI_API_KEY=sk-...

# Optional
export CODEX_DEFAULT_MODEL=gpt-5.3-codex-spark
export CODEX_DEFAULT_SANDBOX=read-only
export CODEX_DEFAULT_REASONING=medium
```

## Integration with Claude Code

When Claude Code activates this skill:

1. Detect trigger phrases in user prompt
2. Ask for model selection if not specified
3. Ask for reasoning effort if not specified
4. Determine appropriate sandbox mode based on task
5. Construct and execute codex command
6. Parse and summarize output for user
7. Offer to resume session for follow-up

This enables seamless delegation of complex coding tasks while Claude Code maintains conversational context and user interaction.
