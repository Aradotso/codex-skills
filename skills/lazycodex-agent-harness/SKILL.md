---
name: lazycodex-agent-harness
description: AI agent orchestration for complex codebases with planning, execution, and verified completion through OmO framework
triggers:
  - set up lazycodex in my project
  - create an agent plan with lazycodex
  - run autonomous coding loop
  - execute a work plan with verified completion
  - initialize deep project memory for agents
  - orchestrate multi-agent coding tasks
  - use lazycodex for complex codebase work
  - start ultrawork loop for my task
---

# LazyCodex Agent Harness

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

LazyCodex is an agent orchestration harness for complex codebases, packaging [oh-my-openagent (OmO)](https://github.com/code-yeongyu/oh-my-openagent) for AI coding environments like Codex, Claude Code, and Cursor. It provides project memory, strategic planning, durable execution, verified completion, and specialized skills for autonomous coding workflows.

Think of it as LazyVim for Codex — a curated distribution that makes agent orchestration usable without configuration overhead.

## Installation

LazyCodex installs via `npx` without global packages:

```bash
# Standard installation with TUI
npx lazycodex-ai install

# Fully autonomous setup without terminal UI
npx lazycodex-ai install --no-tui --codex-autonomous
```

This is shorthand for:
```bash
npx --yes --package oh-my-openagent omo install --platform=codex
```

The installer configures OmO commands that become available in your Codex environment with the `$command` syntax.

## Core Commands

### `$ulw-loop` — Verified Autonomous Loop

Self-referential execution loop that continues until Oracle-verified completion. Caps at 500 iterations in ultrawork mode, 100 in normal mode.

```bash
# Basic autonomous loop
$ulw-loop "refactor authentication module to use JWT"

# With explicit completion promise
$ulw-loop "add TypeScript strict mode to entire codebase" \
  --completion-promise="All .ts files pass tsc --strict with zero errors"

# Strategy options
$ulw-loop "optimize database queries" --strategy=reset
$ulw-loop "fix all linting errors" --strategy=continue
```

**When to use**: Tasks requiring iterative refinement with evidence-based completion (test passage, lint clean, build success).

### `$ulw-plan` — Strategic Planning

Prometheus strategic planner that writes decision-complete plans without touching product code.

```bash
# Generate a plan
$ulw-plan "add real-time collaboration features"

# Creates: plans/<slug>.md
# Example: plans/add-real-time-collaboration-features.md
```

**Plan structure:**
- Strategic decisions made upfront
- Checkbox-based task breakdown
- No implementation code (planning phase only)
- Ready for `$start-work` execution

**When to use**: Complex features requiring architectural decisions before implementation.

### `$start-work` — Durable Plan Execution

Executes a plan file until every checkbox is complete. Uses Boulder progress tracking.

```bash
# Execute most recent plan
$start-work

# Execute specific plan
$start-work add-real-time-collaboration-features

# Use custom worktree
$start-work api-refactor --worktree ./feature-branch
```

Prints `**ORCHESTRATION COMPLETE**` when all checkboxes are done.

**When to use**: After `$ulw-plan` generates a plan, or when resuming interrupted work.

## Project Memory: `/init-deep`

Generates hierarchical `AGENTS.md` context files for large repositories. Scores directory complexity and writes local guidance near code that needs it.

```bash
/init-deep
```

**What it creates:**
```
project-root/
├── AGENTS.md                    # Top-level context
├── src/
│   ├── AGENTS.md               # Module-level guidance
│   ├── components/
│   │   └── AGENTS.md           # Component patterns
│   └── utils/
│       └── AGENTS.md           # Utility conventions
```

**When to run:**
- Initial setup for repositories too large to explain from memory
- After major structural refactoring
- When onboarding new AI agents to the codebase

**Example AGENTS.md content:**
```markdown
# Project: E-commerce Platform

## Architecture
- Next.js 15 app router
- Prisma ORM with PostgreSQL
- tRPC for type-safe API

## Key Landmarks
- `/src/server/api/routers/` - tRPC route definitions
- `/src/components/ui/` - Radix UI + Tailwind components
- `/prisma/schema.prisma` - Database schema source of truth

## Agent Guidance
- Always run `pnpm db:push` after schema changes
- UI components use `cn()` utility for Tailwind merging
- API routes require auth middleware from `@/server/auth`
```

## Specialized Skills

LazyCodex includes skills for domain-specific work:

| Skill | Purpose | Trigger |
|-------|---------|---------|
| `review-work` | Multi-angle post-implementation review | After major feature completion |
| `remove-ai-slops` | Clean up AI-generated code patterns | Before PR submission |
| `frontend-ui-ux` | Polish user-facing interfaces | UI component work |
| `programming` | Strict TypeScript/Rust/Python/Go discipline | Language-specific implementation |
| `LSP` | Diagnostics, definitions, references, symbols | Code navigation and refactoring |
| `AST-grep` | Structural search and rewrite | Large-scale code transformations |
| `rules` | Project instructions from AGENTS/rules files | Context-aware execution |
| `comment-checker` | Post-edit feedback | After edit operations |

Skills are invoked automatically based on task context or explicitly via agent commands.

## Common Workflows

### Workflow 1: Feature Planning → Execution

```bash
# Step 1: Strategic planning
$ulw-plan "add WebSocket support for real-time notifications"

# Creates: plans/add-websocket-support-for-real-time-notifications.md
# Review the plan, adjust if needed

# Step 2: Execute the plan
$start-work add-websocket-support-for-real-time-notifications

# Agent orchestrates:
# - Sisyphus: Coordination
# - Hephaestus: Implementation
# - Oracle: Verification
# - Librarian: Documentation

# Outputs: **ORCHESTRATION COMPLETE**
```

### Workflow 2: Autonomous Bug Fix

```bash
# Self-healing loop with evidence-based completion
$ulw-loop "fix failing integration tests in payment module" \
  --completion-promise="npm test -- payment.test.ts exits 0"

# Agent loop:
# 1. Run tests, capture failures
# 2. Analyze root cause
# 3. Implement fix
# 4. Verify with Oracle
# 5. Repeat until promise satisfied
```

### Workflow 3: Large Refactor with Memory

```bash
# Step 1: Initialize project memory
/init-deep

# Step 2: Plan the refactor with context
$ulw-plan "migrate from REST to tRPC across all API routes"

# Step 3: Execute with checkpoints
$start-work migrate-from-rest-to-trpc

# Boulder progress tracking allows resumption if interrupted
```

## TypeScript API Examples

LazyCodex itself is built with TypeScript. Here's how to interact programmatically with OmO internals:

### Custom Skill Definition

```typescript
// skills/custom-skill.ts
import { defineSkill } from 'oh-my-openagent';

export default defineSkill({
  name: 'api-testing',
  description: 'Generate and run API integration tests',
  
  triggers: [
    'test the API endpoints',
    'add integration tests',
    'verify API contracts'
  ],
  
  async execute(context) {
    const { projectPath, taskDescription } = context;
    
    // Analyze API routes
    const routes = await this.analyzeRoutes(projectPath);
    
    // Generate test files
    for (const route of routes) {
      await this.generateTest(route);
    }
    
    // Run tests with Oracle verification
    const result = await this.runTests();
    return result;
  }
});
```

### Hook Integration

```typescript
// hooks/pre-commit-check.ts
import { defineHook } from 'oh-my-openagent';

export default defineHook({
  lifecycle: 'pre-commit',
  
  async run(context) {
    const { files } = context;
    
    // Run linter on changed files
    const lintResult = await exec('eslint', files);
    
    if (lintResult.exitCode !== 0) {
      throw new Error('Linting failed. Fix errors before committing.');
    }
    
    // Type check
    const tscResult = await exec('tsc', ['--noEmit']);
    
    if (tscResult.exitCode !== 0) {
      throw new Error('Type errors detected.');
    }
    
    return { success: true };
  }
});
```

### Model Routing Configuration

```typescript
// config/model-routing.ts
import { defineModelRouting } from 'oh-my-openagent';

export default defineModelRouting({
  categories: {
    'quick-edit': {
      model: 'gpt-5.4-mini',
      reasoning: 'low'
    },
    'ultrabrain': {
      model: 'gpt-5.2',
      reasoning: 'xhigh'
    },
    'agentic-coding': {
      model: 'gpt-5.3-codex',
      reasoning: 'high'
    }
  },
  
  fallbackChain: [
    'gpt-5.3-codex',
    'gpt-5.2',
    'gpt-5.4-mini'
  ]
});
```

## Configuration

LazyCodex uses zero-config defaults but supports customization via `.lazycodex/config.json`:

```json
{
  "agents": {
    "sisyphus": {
      "maxIterations": 500,
      "strategy": "continue"
    },
    "oracle": {
      "verificationStrict": true
    }
  },
  "skills": {
    "enabled": [
      "review-work",
      "programming",
      "LSP",
      "frontend-ui-ux"
    ],
    "disabled": ["remove-ai-slops"]
  },
  "models": {
    "defaultProvider": "openai",
    "routing": {
      "preferCodingModels": true
    }
  },
  "hooks": {
    "preCommit": true,
    "postPlan": false
  }
}
```

### Environment Variables

```bash
# OpenAI API configuration
export OPENAI_API_KEY=your_openai_api_key_here
export OPENAI_API_BASE=https://api.openai.com/v1  # Optional custom endpoint

# Model preferences
export OMO_DEFAULT_MODEL=gpt-5.3-codex
export OMO_REASONING_LEVEL=high  # low, medium, high, xhigh

# Agent behavior
export OMO_MAX_ITERATIONS=500
export OMO_STRATEGY=continue  # continue or reset

# Debugging
export OMO_DEBUG=true
export OMO_LOG_LEVEL=verbose
```

## Multi-Model Routing Explained

LazyCodex uses intelligent model selection based on task categories:

| Task Type | Model | Reasoning | Use Case |
|-----------|-------|-----------|----------|
| Quick edits | `gpt-5.4-mini` | Low | Simple refactors, formatting |
| Standard coding | `gpt-5.3-codex` | High | Feature implementation |
| Complex logic | `gpt-5.2` | X-High | Architecture decisions |
| Code review | `gpt-5.2` | High | Bug analysis, security review |

This is quota-efficient: expensive reasoning models run only when needed.

**Verify routing:**
```bash
# Check which model handled each subtask
cat .lazycodex/logs/execution.log | grep "model="
```

## Troubleshooting

### Agent Loop Not Terminating

**Symptom:** `$ulw-loop` exceeds iteration cap without completion.

**Solutions:**
```bash
# Make completion promise more specific
$ulw-loop "fix tests" \
  --completion-promise="npm test exits with code 0 AND coverage > 80%"

# Use reset strategy to clear context
$ulw-loop "refactor auth" --strategy=reset

# Check Oracle logs
cat .lazycodex/logs/oracle.log
```

### Plan Not Executing

**Symptom:** `$start-work` fails to find or execute plan.

**Solutions:**
```bash
# List available plans
ls plans/

# Specify plan explicitly with correct slug
$start-work add-websocket-support  # Not add-websocket-support.md

# Check plan file has valid checkbox syntax
# ✓ - [ ] Task description (not [x] or other formats)
```

### Model Selection Issues

**Symptom:** Unexpected model appears in logs or quota usage spikes.

**Solutions:**
```bash
# Force specific model for testing
export OMO_DEFAULT_MODEL=gpt-5.4-mini

# Disable auto-routing temporarily
export OMO_DISABLE_ROUTING=true

# Check model requirements
cat src/packages/model-core/src/model-requirements.ts
```

### AGENTS.md Not Generated

**Symptom:** `/init-deep` completes but no context files appear.

**Solutions:**
```bash
# Ensure sufficient directory depth
# /init-deep only creates AGENTS.md for complex directories

# Check scoring threshold
export OMO_COMPLEXITY_THRESHOLD=3  # Lower = more AGENTS.md files

# Run with verbose logging
export OMO_DEBUG=true
/init-deep
```

### Skill Not Triggering

**Symptom:** Expected skill doesn't activate during execution.

**Solutions:**
```bash
# Check skill is enabled
cat .lazycodex/config.json | grep -A 5 "skills"

# Explicit skill invocation
$ulw-loop "optimize queries" --skills=programming,LSP

# Verify skill triggers match your phrasing
cat skills/<skill-name>.md | grep "triggers:"
```

## Advanced Patterns

### Parallel Agent Execution

```typescript
// Launch multiple agents for independent subtasks
import { orchestrate } from 'oh-my-openagent';

await orchestrate({
  parallel: true,
  tasks: [
    { agent: 'hephaestus', work: 'implement API routes' },
    { agent: 'hephaestus', work: 'create UI components' },
    { agent: 'librarian', work: 'update documentation' }
  ]
});
```

### Custom Verification Logic

```typescript
// Define Oracle completion criteria
import { defineVerification } from 'oh-my-openagent';

export default defineVerification({
  name: 'test-coverage-threshold',
  
  async verify(context) {
    const coverage = await getCoverage();
    
    return {
      passed: coverage.total > 80,
      evidence: `Total coverage: ${coverage.total}%`,
      nextSteps: coverage.total <= 80 
        ? ['Add tests for uncovered branches']
        : []
    };
  }
});
```

### Progressive Enhancement Workflow

```bash
# Start with basic implementation
$ulw-plan "add dark mode toggle"
$start-work add-dark-mode-toggle

# Enhance with polish skill
$ulw-loop "polish dark mode UX" --skills=frontend-ui-ux

# Final cleanup
$ulw-loop "remove any AI code patterns" --skills=remove-ai-slops
```

## Resources

- **Homepage**: [lazycodex.ai](https://lazycodex.ai)
- **OmO Repository**: [github.com/code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)
- **Documentation**: [lazycodex.ai/docs](https://lazycodex.ai/docs)
- **Model Docs**: [OpenAI Platform](https://platform.openai.com/docs/models)

LazyCodex is maintained by Jobdori (AI assistant) and distributed under MIT license.
