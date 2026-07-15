---
name: codex-orchestration-multi-model
description: Assign different AI models to planning, review, and execution roles within Codex workflows using the Codex Orchestration plugin
triggers:
  - how do I use codex orchestration to assign model roles
  - set up multiple models for planning and execution in codex
  - configure fable 5 as planner in codex orchestration
  - use different models for advisor and executor roles
  - create custom agent roles for codex orchestration
  - troubleshoot codex orchestration model assignment
  - run codex with separate planner advisor and executor
  - bring claude fable into codex workflows
---

# Codex Orchestration Multi-Model Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

Codex Orchestration is a plugin that lets you assign different AI models to specific roles in a Codex workflow:

- **Planner**: Creates and refines the implementation plan (optional, defaults to current Codex model)
- **Advisor**: Reviews plans and identifies gaps before execution (optional)
- **Executor**: Implements the approved plan (required)

The root Codex model remains the orchestrator, coordinating work between roles and delivering final results. This enables using Claude Fable 5 or other models within Codex, potentially reducing premium-model usage by ~40% and speeding up suitable tasks up to 2x through parallel execution.

## Installation

```bash
codex plugin marketplace add Cjbuilds/Codex-Orchestration
codex plugin add codex-orchestration@codex-orchestration
```

**Requirements**: Python 3.11 or newer

After installation, **start a new Codex task** for the plugin to initialize properly.

## Core Commands

### Setup Workflow

```bash
/codex-orchestration setup planner: <model> <effort>, advisor: <model> <effort>, executor: <model> <effort>
```

**Effort levels**: `Low`, `Medium`, `High`, `XHigh`, `Max` (or `Ultra` as alias for Max)

**Examples**:

```bash
# Full three-role setup
/codex-orchestration setup planner: Claude Fable 5 High, advisor: GPT-5.6 Sol High, executor: GPT-5.6 Luna Extra High

# Use current Codex model as planner (omit planner field)
/codex-orchestration setup advisor: Claude Fable 5 High, executor: GPT-5.6 Luna Extra High

# No advisor, just planner and executor
/codex-orchestration setup planner: GPT-5.6 Sol Extra High, executor: GPT-5.6 Luna Extra High

# Minimal: executor only (current model plans, no review)
/codex-orchestration setup executor: GPT-5.6 Luna Extra High
```

**Important rules**:
- Executor is **required**
- Planner and Advisor must use **different model routes** for independent review
- Role labels are literal — models are assigned exactly as specified
- Setup persists across tasks until disabled

### Check Status

```bash
# View current configuration
/codex-orchestration status

# Verify effective routing in active task
/codex-orchestration status --require-effective
```

### Disable Workflow

```bash
/codex-orchestration disable
```

Restores pre-setup routing. Does not delete user-created custom roles.

## Using Claude Fable 5

Claude Fable 5 is bundled and can be used directly without additional provider configuration:

```bash
# As planner
/codex-orchestration setup planner: Claude Fable 5 High, executor: GPT-5.6 Luna Extra High

# As advisor
/codex-orchestration setup advisor: Claude Fable 5 High, executor: GPT-5.6 Luna Extra High
```

Fable 5 uses the official Claude Code CLI with first-party authentication — no API key needed in Codex.

## Creating Custom Agent Roles

For models not already in Codex, create a custom role (requires configured and authenticated provider):

### Project Role (Lives in `.codex/agents/`)

```bash
/codex-orchestration create project role:
name: researcher
model: anthropic/claude-3-5-sonnet-20250219
provider: anthropic-api
effort: high
job: gather evidence and cite sources
```

### Personal Role (Lives in `~/.codex/agents/`, reusable across projects)

```bash
/codex-orchestration create personal role:
name: code-reviewer
model: openai/gpt-4-turbo
provider: openai-api
effort: extra-high
job: review code for security vulnerabilities and best practices
```

**Fields**:
- `name`: Role identifier (kebab-case recommended)
- `model`: Exact model ID from provider
- `provider`: Configured provider ID in Codex
- `effort`: Computational effort level
- `job`: Brief role description

Codex previews the role file before creation.

## Workflow Execution Flow

```text
User Task
    ↓
Codex Orchestrates
    ↓
Planner Creates Plan
    ↓
Advisor Reviews Plan
    ↓
[Needs Work?] → Yes → Planner Improves → Back to Advisor
    ↓ No
Plan Approved
    ↓
Executors Implement (potentially parallel)
    ↓
Codex Tests & Delivers
```

**Limits**:
- Maximum 5 review cycles
- If approval not reached, execution stops and unresolved issues are shown
- Advisor approval gates implementation, doesn't guarantee success

## Working with Codex Goals

Orchestration works with Codex Goals:

1. Create Goal normally: `/goal create "implement user authentication"`
2. Tell Codex to use saved orchestration workflow
3. Codex applies role routing while managing Goal state, permissions, and verification

The plugin only guides model assignment; Codex owns Goal orchestration.

## Configuration Patterns

### Maximum Planning Rigor

```bash
/codex-orchestration setup planner: Claude Fable 5 Max, advisor: GPT-5.6 Sol Extra High, executor: GPT-5.6 Luna High
```

Use case: Complex architecture requiring thorough review before implementation.

### Speed-Optimized Execution

```bash
/codex-orchestration setup planner: GPT-5.6 Sol Medium, executor: GPT-5.6 Luna Extra High
```

Use case: Well-understood tasks where fast implementation matters more than review.

### Cost-Efficient Research

```bash
/codex-orchestration setup planner: Claude Fable 5 Low, advisor: GPT-5.6 Sol Medium, executor: GPT-5.6 Luna Medium
```

Use case: Exploratory work where multiple iterations are expected.

### External Model Integration

```bash
# First, create custom role
/codex-orchestration create project role:
name: deepseek-coder
model: deepseek/deepseek-coder-33b
provider: deepseek-api
effort: high
job: implement code with performance optimization focus

# Then assign to executor
/codex-orchestration setup planner: Claude Fable 5 High, executor: deepseek-coder High
```

## Python Integration Example

The plugin itself is Python-based. Custom role definitions are YAML but processed by Python tooling.

### Example: Programmatic Role Creation Helper

```python
import subprocess
import json

def create_orchestration_role(name: str, model: str, provider: str, 
                             effort: str, job: str, scope: str = "project"):
    """Helper to create orchestration roles programmatically."""
    
    role_spec = f"""
/codex-orchestration create {scope} role:
name: {name}
model: {model}
provider: {provider}
effort: {effort}
job: {job}
"""
    
    # In actual Codex environment, this would be handled by Codex
    # This is illustrative of the structure
    print(f"Would create {scope} role: {name}")
    print(role_spec)
    
    return role_spec

# Example usage
create_orchestration_role(
    name="security-auditor",
    model="anthropic/claude-3-opus-20240229",
    provider="anthropic-api",
    effort="max",
    job="audit code for security vulnerabilities with detailed reports",
    scope="personal"
)
```

### Example: Status Check Integration

```python
import subprocess
import json
import os

def get_orchestration_status():
    """Check current orchestration configuration."""
    
    # This would typically be called within a Codex skill context
    result = subprocess.run(
        ["codex", "plugin", "list", "--json"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        plugins = json.loads(result.stdout)
        orchestration = next(
            (p for p in plugins if "codex-orchestration" in p.get("name", "")),
            None
        )
        
        if orchestration:
            version = orchestration.get("version", "unknown")
            print(f"Codex Orchestration version: {version}")
            
            # Check for minimum required version
            if version >= "0.5.1":
                return True
            else:
                print("Warning: Update required for reliable Planner assignment")
                return False
    
    return False

# Example usage
if get_orchestration_status():
    print("Orchestration ready")
else:
    print("Orchestration needs attention")
```

## Troubleshooting

### Version Issues

**Problem**: Old version persists after update

```bash
# Check current version
codex plugin list --json | grep -A5 "codex-orchestration"

# If version is old or sourceType is "local", remove and reinstall
/codex-orchestration disable  # If workflow is active
codex plugin remove codex-orchestration@codex-orchestration
codex plugin marketplace remove codex-orchestration
codex plugin marketplace add Cjbuilds/Codex-Orchestration
codex plugin add codex-orchestration@codex-orchestration
```

**Required version**: 0.5.1 or newer for reliable Planner assignment

### Planner/Advisor Not Working

**Problem**: Models not assigned to correct roles

**Solutions**:
1. Verify you started a **new task** after setup
2. Check role assignment: `/codex-orchestration status`
3. Ensure Planner and Advisor use **different model routes**
4. Confirm version >= 0.5.1 (addresses Advisor-only cache issue)

### Fable 5 Authentication

**Problem**: Claude Fable 5 not accessible

**Solutions**:
1. Verify Claude Code CLI is installed and authenticated
2. Test authentication outside Codex first
3. Fable 5 uses first-party Claude login, not Anthropic API key
4. Check `claude --version` and re-authenticate if needed

### Workflow Not Applying

**Problem**: Setup command runs but workflow doesn't activate

**Solutions**:
1. Run `/codex-orchestration status --require-effective` in active task
2. Ensure Python 3.11+ is available
3. Check for permission issues with `.codex/agents/` directory
4. Restart Codex session after setup

### Model Not Available

**Problem**: Custom model not recognized

**Solutions**:
1. Verify provider is configured: `codex providers list`
2. Confirm provider authentication is valid
3. Check exact model ID matches provider's naming
4. Test model access outside orchestration first
5. Ensure role file was created: check `.codex/agents/` or `~/.codex/agents/`

### Parallel Execution Not Happening

**Note**: Codex decides when parallel work is beneficial based on task structure. Orchestration enables it but doesn't force it.

- Independent implementation steps may run in parallel
- Speed improvements (up to 2x) depend on task suitability
- Use `/codex-orchestration status` to verify Executor is configured

### Plan Review Loops

**Problem**: Advisor and Planner stuck in revision cycles

**Solutions**:
1. Review loop is limited to 5 cycles maximum
2. If approval not reached, Codex shows latest plan and issues
3. Consider adjusting Advisor effort level (lower may be less strict)
4. Check that Advisor and Planner are truly different model routes

## Important Limitations

- **Codex remains root orchestrator** — plugin only routes work
- **No direct role communication** — Planner/Advisor report only to Codex
- **Instruction-enforced boundaries** — Fable tools reserved for root model
- **Existing authentication required** — plugin doesn't create credentials
- **Provider compatibility** — custom models need compatible provider setup
- **No subagent override** — if user says "no subagents", Codex must comply

## Updating

```bash
codex plugin marketplace upgrade codex-orchestration
codex plugin add codex-orchestration@codex-orchestration
```

Verify update: `codex plugin list --json`

**Before downgrading**: Run `/codex-orchestration disable` with current version first.

## Uninstalling

```bash
# 1. Disable workflow first
/codex-orchestration disable

# 2. Remove plugin
codex plugin remove codex-orchestration@codex-orchestration
codex plugin marketplace remove codex-orchestration
```

**Note**: Custom roles in `.codex/agents/` or `~/.codex/agents/` are preserved and must be removed separately if desired.

## Best Practices

1. **Start new tasks** after setup/update for changes to take effect
2. **Use different models** for Planner and Advisor to ensure independent review
3. **Match effort to task** — Max isn't always better for iteration speed
4. **Test custom roles** outside orchestration before assigning
5. **Keep plugin updated** (>= 0.5.1) for reliable behavior
6. **Use project roles** for project-specific models, **personal roles** for cross-project tools
7. **Monitor with status** command to verify effective routing

## Reference

- **Repository**: Cjbuilds/Codex-Orchestration
- **License**: MIT
- **Language**: Python
- **Requires**: Python 3.11+, Codex
- **Docs**: [Production Readiness Audit](docs/production-readiness-audit.md), [Security Policy](SECURITY.md)
