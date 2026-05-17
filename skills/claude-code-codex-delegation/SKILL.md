---
name: claude-code-codex-delegation
description: Delegate code analysis, refactoring, and editing tasks from Claude Code to the Codex CLI for autonomous AI workflows
triggers:
  - use codex to analyze this code
  - delegate this to codex
  - run codex on this repository
  - let codex refactor this
  - invoke codex session for this task
  - execute codex with full auto mode
  - resume my codex session
  - have codex review this codebase
---

# Claude Code Codex Delegation Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

This skill enables Claude Code to invoke the **Codex CLI** for automated code analysis, refactoring, and editing workflows. Codex is an autonomous AI coding agent that can perform complex multi-file operations, repository analysis, and sustained editing sessions. By delegating tasks to Codex, you leverage its specialized capabilities for code transformation while maintaining Claude Code's conversational interface.

## Installation

### Prerequisites

Ensure the `codex` CLI is installed and configured:

```bash
# Verify installation
codex --version

# If not installed, follow Codex documentation to install
# Ensure valid credentials are configured
```

The `codex` binary must be available on your `PATH`.

### Installing This Skill

**Option 1: Plugin Installation (Recommended)**

```bash
/plugin marketplace add skills-directory/skill-codex
/plugin install skill-codex@skill-codex
```

**Option 2: Manual Skill Installation**

```bash
git clone --depth 1 https://github.com/skills-directory/skill-codex.git /tmp/skills-temp
mkdir -p ~/.claude/skills
cp -r /tmp/skills-temp/plugins/skill-codex/skills/codex ~/.claude/skills/codex
rm -rf /tmp/skills-temp
```

## Key Commands

### Basic Codex Execution

```bash
# Single-shot analysis (read-only sandbox)
codex exec -m gpt-5.3-codex-spark \
  --sandbox read-only \
  --full-auto \
  --skip-git-repo-check \
  "Analyze this repository for security vulnerabilities" 2>/dev/null

# Code editing with write access
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --sandbox writable \
  --full-auto \
  "Refactor all API handlers to use async/await patterns"

# Resume previous session
codex resume <session-id>
```

### Model Selection

Choose based on task complexity:

- **gpt-5.5**: Most capable, highest cost, best for complex multi-step tasks
- **gpt-5.4**: Balanced performance for general refactoring
- **gpt-5.4-mini**: Fast, cost-effective for simple tasks
- **gpt-5.3-codex-spark**: Optimized for code-specific reasoning
- **gpt-5.3-codex**: Baseline code model

### Reasoning Effort Levels

```bash
# Low effort (faster, cheaper)
--config model_reasoning_effort="low"

# Medium effort (balanced)
--config model_reasoning_effort="medium"

# High effort (thorough, slower)
--config model_reasoning_effort="high"
```

### Sandbox Modes

- `--sandbox read-only`: Analysis tasks, no file modifications
- `--sandbox writable`: Allow Codex to edit files
- `--sandbox full`: Unrestricted access (use with caution)

## Usage Patterns

### Pattern 1: Repository Analysis

```bash
# User asks: "Analyze this codebase for architectural issues"

codex exec -m gpt-5.3-codex-spark \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --full-auto \
  --skip-git-repo-check \
  "Perform comprehensive architectural analysis. Identify:
   1. Code organization issues
   2. Dependency coupling problems
   3. Testing gaps
   4. Performance bottlenecks
   5. Security concerns
   Provide specific file locations and recommendations." 2>/dev/null
```

### Pattern 2: Automated Refactoring

```bash
# User asks: "Refactor this to use TypeScript strict mode"

codex exec -m gpt-5.4 \
  --config model_reasoning_effort="medium" \
  --sandbox writable \
  --full-auto \
  "Enable TypeScript strict mode and fix all resulting type errors:
   1. Update tsconfig.json
   2. Add explicit types to all functions
   3. Fix null/undefined handling
   4. Ensure all tests still pass" 2>/dev/null
```

### Pattern 3: Session Resume

```bash
# User asks: "Continue my previous codex session"

# List recent sessions
codex sessions list --limit 10

# Resume specific session
codex resume abc123def456
```

### Pattern 4: Multi-File Migration

```bash
# User asks: "Migrate all class components to functional components with hooks"

codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --sandbox writable \
  --full-auto \
  "Migrate React class components to functional components:
   1. Convert lifecycle methods to useEffect
   2. Replace this.state with useState
   3. Update event handlers
   4. Preserve all functionality
   5. Update tests accordingly
   
   Process files in src/components directory." 2>/dev/null
```

## Configuration

### Environment Variables

```bash
# Codex API credentials (if required)
export CODEX_API_KEY="your-api-key-from-env"

# Default model preference
export CODEX_DEFAULT_MODEL="gpt-5.3-codex-spark"

# Default reasoning effort
export CODEX_DEFAULT_EFFORT="medium"
```

### Codex Config File

Codex may use `~/.codex/config.yaml` or project-level `.codex.yaml`:

```yaml
default_model: gpt-5.3-codex-spark
reasoning_effort: medium
sandbox_mode: read-only
full_auto: true
skip_git_repo_check: true
```

## Thinking Tokens

**Important**: By default, this skill suppresses Codex's thinking tokens (stderr output) using `2>/dev/null` to prevent context window bloat in Claude Code.

To **enable thinking tokens** for debugging or insight:

```bash
# Remove stderr redirect
codex exec -m gpt-5.3-codex-spark \
  --full-auto \
  "Analyze this code"
# Now you'll see Codex's reasoning process
```

Or explicitly ask Claude: *"Show me the thinking tokens from Codex"*

## Real-World Examples

### Example 1: Security Audit

**User Prompt**: "Use Codex to audit this Express.js API for security issues"

**Executed Command**:
```bash
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --sandbox read-only \
  --full-auto \
  --skip-git-repo-check \
  "Security audit for Express.js API:
   - SQL injection vulnerabilities
   - XSS attack vectors
   - Authentication/authorization flaws
   - Sensitive data exposure
   - Rate limiting gaps
   - CORS misconfigurations
   
   Provide CVE references and fix recommendations." 2>/dev/null
```

### Example 2: Test Generation

**User Prompt**: "Generate comprehensive tests for all untested modules"

**Executed Command**:
```bash
codex exec -m gpt-5.3-codex-spark \
  --config model_reasoning_effort="medium" \
  --sandbox writable \
  --full-auto \
  "Analyze test coverage and generate missing tests:
   1. Identify modules without tests
   2. Create unit tests for pure functions
   3. Create integration tests for API endpoints
   4. Use existing test framework patterns
   5. Aim for 80%+ coverage
   
   Write tests to __tests__/ directory." 2>/dev/null
```

### Example 3: Dependency Upgrade

**User Prompt**: "Upgrade all dependencies and fix breaking changes"

**Executed Command**:
```bash
codex exec -m gpt-5.5 \
  --config model_reasoning_effort="high" \
  --sandbox writable \
  --full-auto \
  "Dependency upgrade workflow:
   1. Update package.json to latest compatible versions
   2. Run npm install
   3. Identify breaking changes in CHANGELOG
   4. Update code to match new APIs
   5. Fix all TypeScript errors
   6. Ensure all tests pass
   
   Create git commits for each major dependency." 2>/dev/null
```

### Example 4: Documentation Generation

**User Prompt**: "Generate API documentation from code"

**Executed Command**:
```bash
codex exec -m gpt-5.3-codex-spark \
  --config model_reasoning_effort="low" \
  --sandbox writable \
  --full-auto \
  "Generate API documentation:
   1. Extract all public API endpoints
   2. Document request/response schemas
   3. Include authentication requirements
   4. Add usage examples
   5. Generate OpenAPI 3.0 spec
   
   Output to docs/api.md and openapi.yaml" 2>/dev/null
```

## Troubleshooting

### Codex Command Not Found

```bash
# Verify installation
which codex

# Check PATH
echo $PATH

# If missing, reinstall Codex CLI per official docs
```

### Authentication Errors

```bash
# Verify credentials
codex auth status

# Re-authenticate if needed
codex auth login

# Check environment variables
env | grep CODEX
```

### Sandbox Permission Errors

If Codex reports permission issues:

```bash
# Ensure correct sandbox mode
--sandbox writable  # for file edits

# Check file permissions
ls -la <affected-files>

# For git repositories, ensure .git directory is accessible
```

### Context Window Overflow

If Claude Code runs out of context:

1. **Suppress thinking tokens**: Ensure `2>/dev/null` is present
2. **Use targeted prompts**: Be specific about which files/modules to analyze
3. **Chain operations**: Break complex tasks into smaller Codex invocations
4. **Use session resume**: For multi-turn workflows, use `codex resume`

### Model Timeout or Rate Limits

```bash
# Switch to faster model
-m gpt-5.4-mini

# Reduce reasoning effort
--config model_reasoning_effort="low"

# Check Codex status
codex status
```

### Session Not Found

```bash
# List available sessions
codex sessions list

# Sessions may expire after 24 hours
# Start new session instead of resuming
```

## Best Practices

1. **Start with read-only**: Use `--sandbox read-only` for analysis tasks to prevent unintended modifications
2. **Match model to task**: Use `gpt-5.4-mini` for simple tasks, `gpt-5.5` for complex refactoring
3. **Be specific**: Detailed prompts yield better results from Codex
4. **Review outputs**: Always review Codex-generated code before committing
5. **Use version control**: Ensure clean git state before allowing write operations
6. **Chain thoughtfully**: For multi-step workflows, guide Codex through each phase explicitly
7. **Monitor costs**: Higher-tier models and reasoning efforts consume more tokens

## Integration with Claude Code Workflows

### Workflow 1: Analysis → Discussion → Action

```
1. User: "Analyze this codebase with Codex"
2. Claude: [Runs Codex in read-only mode]
3. Claude: [Summarizes findings in conversation]
4. User: "Fix the issues Codex found"
5. Claude: [Runs Codex in writable mode with specific fixes]
```

### Workflow 2: Iterative Refactoring

```
1. User: "Refactor authentication module"
2. Claude: [Codex session 1 - analyze structure]
3. User: "Good, now apply those changes"
4. Claude: [Codex resume - implement changes]
5. User: "Add tests for the new structure"
6. Claude: [Codex resume - generate tests]
```

### Workflow 3: Validation Pipeline

```
1. Claude: [Makes code changes directly]
2. User: "Have Codex validate these changes"
3. Claude: [Runs Codex analysis on recent changes]
4. Claude: [Reports validation results]
```

## Advanced Features

### Custom Reasoning Configuration

```bash
codex exec -m gpt-5.4 \
  --config model_reasoning_effort="high" \
  --config temperature=0.3 \
  --config max_tokens=8000 \
  "Your task here"
```

### Targeting Specific Files

```bash
codex exec -m gpt-5.3-codex-spark \
  --files "src/auth/*.ts" \
  --sandbox read-only \
  --full-auto \
  "Analyze authentication implementation in these files"
```

### Combining with Git Operations

```bash
# Before refactoring
git checkout -b codex-refactor

# Run Codex
codex exec -m gpt-5.4 --sandbox writable --full-auto "Refactor task"

# After Codex completes
git add .
git commit -m "Codex: automated refactoring"
git diff main
```

---

**Note**: This skill is part of the Codex Skills collection at [ara.so](https://ara.so). For the most autonomous setup combining Claude Code and Codex, see [klaudworks/ralph-meets-rex](https://github.com/klaudworks/ralph-meets-rex).
