---
name: claude-code-codex-delegation
description: Delegate prompts from Claude Code to OpenAI Codex CLI for automated code analysis, refactoring, and editing workflows
triggers:
  - "use codex to analyze this code"
  - "delegate this task to codex"
  - "run codex exec on this repository"
  - "analyze with codex"
  - "refactor using codex"
  - "let codex review this code"
  - "invoke codex for this task"
  - "use codex to improve this"
---

# Claude Code Codex Delegation

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

This skill enables Claude Code to invoke the OpenAI Codex CLI for automated code analysis, refactoring, and editing workflows. It provides a structured way to delegate complex coding tasks to Codex's specialized models while maintaining Claude Code's orchestration capabilities.

## Prerequisites

- Codex CLI installed and available on `PATH`
- Valid Codex credentials configured
- Verify installation: `codex --version`

## Installation

### Via Claude Code Plugin (Recommended)

```bash
/plugin marketplace add skills-directory/skill-codex
/plugin install skill-codex@skill-codex
```

### Standalone Installation

```bash
git clone --depth 1 https://github.com/skills-directory/skill-codex.git /tmp/skills-temp
mkdir -p ~/.claude/skills
cp -r /tmp/skills-temp/plugins/skill-codex/skills/codex ~/.claude/skills/codex
rm -rf /tmp/skills-temp
```

## Core Commands

### Basic Execution

```bash
codex exec [options] "prompt"
```

**Key Options:**
- `-m, --model` - Model selection (`gpt-5.5`, `gpt-5.4`, `gpt-5.4-mini`, `gpt-5.3-codex-spark`, `gpt-5.3-codex`)
- `--config` - Runtime configuration (e.g., `model_reasoning_effort="high"`)
- `--sandbox` - Safety mode (`read-only`, `write`, `full`)
- `--full-auto` - Auto-approve all actions
- `--skip-git-repo-check` - Skip git repository validation

### Session Management

```bash
# Resume previous session
codex resume

# Resume specific session
codex resume <session-id>

# List sessions
codex sessions list
```

## Configuration

### Model Selection

**Available Models:**
- `gpt-5.5` - Latest flagship model
- `gpt-5.4` - Previous generation flagship
- `gpt-5.4-mini` - Faster, cost-effective variant
- `gpt-5.3-codex-spark` - Optimized for code tasks
- `gpt-5.3-codex` - Specialized coding model

### Reasoning Effort Levels

```bash
--config model_reasoning_effort="low"     # Fast, simple tasks
--config model_reasoning_effort="medium"  # Balanced (default)
--config model_reasoning_effort="high"    # Complex analysis
```

### Sandbox Modes

- `read-only` - Analysis only, no file modifications
- `write` - Allow file edits
- `full` - Unrestricted access (use with caution)

## Usage Patterns

### Pattern 1: Code Analysis

```bash
codex exec -m gpt-5.3-codex-spark \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --full-auto \
  --skip-git-repo-check \
  "Analyze this repository for security vulnerabilities and performance bottlenecks" 2>/dev/null
```

### Pattern 2: Refactoring

```bash
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="medium" \
  --sandbox write \
  --full-auto \
  "Refactor the authentication module to use dependency injection" 2>/dev/null
```

### Pattern 3: Test Generation

```bash
codex exec -m gpt-5.3-codex-spark \
  --config model_reasoning_effort="medium" \
  --sandbox write \
  --full-auto \
  "Generate comprehensive unit tests for all exported functions in src/utils.js" 2>/dev/null
```

### Pattern 4: Documentation

```bash
codex exec -m gpt-5.4-mini \
  --config model_reasoning_effort="low" \
  --sandbox write \
  --full-auto \
  "Add JSDoc comments to all public API functions" 2>/dev/null
```

### Pattern 5: Migration

```bash
codex exec -m gpt-5.5 \
  --config model_reasoning_effort="high" \
  --sandbox write \
  "Migrate this Express.js application to Fastify, preserving all functionality" 2>/dev/null
```

## Delegation Workflow

When a user requests Codex delegation, follow this workflow:

1. **Clarify Requirements** (if not specified):
   - Model preference
   - Reasoning effort level
   - Sandbox mode (default: `read-only` for analysis, `write` for modifications)

2. **Construct Command**:
   ```bash
   codex exec -m <model> \
     --config model_reasoning_effort="<level>" \
     --sandbox <mode> \
     --full-auto \
     --skip-git-repo-check \
     "<detailed prompt>" 2>/dev/null
   ```

3. **Execute and Parse Output**:
   - Run the command
   - Capture stdout (stderr suppressed by default with `2>/dev/null`)
   - Summarize key findings

4. **Present Results**:
   - Highlight main insights
   - Suggest follow-up actions
   - Offer to resume session for iterative work

## Thinking Tokens

By default, thinking tokens (stderr output) are suppressed with `2>/dev/null` to avoid context window bloat. To view thinking tokens:

**User request:** "Show me the thinking tokens from Codex"

**Command adjustment:**
```bash
codex exec -m gpt-5.3-codex-spark \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --full-auto \
  "Analyze error handling patterns"
# Remove 2>/dev/null to display thinking tokens
```

## Environment Variables

Configure Codex credentials via environment variables:

```bash
export CODEX_API_KEY=your_api_key_here
export CODEX_ORG_ID=your_org_id_here
```

Add to `~/.bashrc`, `~/.zshrc`, or equivalent shell configuration.

## Common Workflows

### Security Audit

```bash
codex exec -m gpt-5.5 \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --full-auto \
  "Perform a comprehensive security audit focusing on: 1) SQL injection risks, 2) XSS vulnerabilities, 3) authentication weaknesses, 4) dependency vulnerabilities" 2>/dev/null
```

### Performance Optimization

```bash
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --full-auto \
  "Profile this codebase and identify: 1) algorithmic inefficiencies, 2) memory leaks, 3) unnecessary re-renders, 4) database query optimization opportunities" 2>/dev/null
```

### Code Quality Review

```bash
codex exec -m gpt-5.3-codex-spark \
  --config model_reasoning_effort="medium" \
  --sandbox read-only \
  --full-auto \
  "Review code quality across: 1) adherence to project style guide, 2) SOLID principles, 3) DRY violations, 4) test coverage gaps" 2>/dev/null
```

### Automated Refactoring

```bash
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --sandbox write \
  "Refactor this monolith into microservices: 1) identify service boundaries, 2) extract services, 3) implement service communication, 4) update tests" 2>/dev/null
```

## Troubleshooting

### Issue: "codex: command not found"

**Solution:**
```bash
# Verify installation
which codex

# If not found, reinstall Codex CLI
# Follow installation instructions at https://docs.openai.com/codex/cli
```

### Issue: Authentication Errors

**Solution:**
```bash
# Verify credentials
codex auth status

# Reconfigure if needed
codex auth login
```

### Issue: Excessive Context Window Usage

**Solution:**
- Always append `2>/dev/null` to suppress thinking tokens unless debugging
- Use more focused prompts
- Consider `gpt-5.4-mini` for simpler tasks

### Issue: Unexpected File Modifications

**Solution:**
- Use `--sandbox read-only` for analysis-only tasks
- Review prompts for clarity
- Remove `--full-auto` flag for manual approval

### Issue: Session Not Resuming

**Solution:**
```bash
# List available sessions
codex sessions list

# Resume with explicit session ID
codex resume <session-id>

# Check session logs
codex sessions logs <session-id>
```

## Best Practices

1. **Model Selection**: Use `gpt-5.3-codex-spark` for most coding tasks; reserve `gpt-5.5` for complex architectural decisions
2. **Reasoning Effort**: Start with `medium`; escalate to `high` only for complex analysis
3. **Sandbox Safety**: Default to `read-only` unless modifications are explicitly required
4. **Prompt Clarity**: Provide detailed, structured prompts with numbered objectives
5. **Session Management**: Use `codex resume` for iterative refinement rather than new executions
6. **Context Preservation**: Suppress thinking tokens by default; enable only when debugging

## Integration Examples

### From Claude Code

```markdown
User: "Use Codex to analyze error handling in this Express app"

Agent Response:
I'll delegate this to Codex with the codex-spark model optimized for code analysis.

[Execute command]:
codex exec -m gpt-5.3-codex-spark \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --full-auto \
  --skip-git-repo-check \
  "Analyze error handling patterns in this Express.js application. Identify: 1) unhandled promise rejections, 2) missing try-catch blocks, 3) inconsistent error response formats, 4) opportunities for centralized error middleware" 2>/dev/null

[Present summarized findings]
```

### Session Continuation

```markdown
User: "Continue the previous Codex session and implement the suggestions"

Agent Response:
I'll resume the previous Codex session and apply the recommended changes.

[Execute command]:
codex resume --sandbox write

[Monitor and summarize applied changes]
```

## Additional Resources

- Official Codex CLI documentation: https://docs.openai.com/codex/cli
- Model comparison guide: https://docs.openai.com/models
- Sandbox security guide: https://docs.openai.com/codex/sandbox
