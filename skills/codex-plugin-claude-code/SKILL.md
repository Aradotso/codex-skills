---
name: codex-plugin-claude-code
description: Use OpenAI Codex from inside Claude Code for code reviews, adversarial reviews, and delegating tasks to Codex as a subagent.
triggers:
  - review my code with codex
  - run a codex adversarial review
  - delegate this task to codex
  - check codex job status
  - cancel the running codex task
  - set up codex plugin for claude code
  - rescue this with codex
  - run codex review in background
---

# Codex Plugin for Claude Code

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

The `codex-plugin-cc` enables Claude Code users to leverage OpenAI Codex directly from their workflow. You can request code reviews (standard or adversarial), delegate tasks to Codex as a background subagent, and manage long-running Codex jobs—all without leaving Claude Code.

**Key capabilities:**
- `/codex:review` — standard read-only Codex code review
- `/codex:adversarial-review` — steerable review that challenges design decisions
- `/codex:rescue` — delegate investigation/fix tasks to Codex subagent
- `/codex:status`, `/codex:result`, `/codex:cancel` — manage background jobs

## Requirements

- **Node.js 18.18+**
- **ChatGPT subscription (including Free tier) or OpenAI API key**
- **Codex CLI** (the plugin can help install it via `/codex:setup`)

Usage contributes to your Codex usage limits.

## Installation

### 1. Add the marketplace and install the plugin

```bash
/plugin marketplace add openai/codex-plugin-cc
/plugin install codex@openai-codex
/reload-plugins
```

### 2. Run setup

```bash
/codex:setup
```

This checks if Codex is installed and authenticated. If missing and npm is available, it can offer to install Codex for you.

### 3. Install Codex CLI (if needed)

If you prefer manual installation:

```bash
npm install -g @openai/codex
```

### 4. Authenticate Codex

If Codex is installed but not logged in:

```bash
!codex login
```

Follow the prompts to sign in with ChatGPT or API key.

### 5. Verify

After setup, you should see:
- Slash commands: `/codex:review`, `/codex:adversarial-review`, `/codex:rescue`, `/codex:status`, `/codex:result`, `/codex:cancel`, `/codex:setup`
- Subagent: `codex:codex-rescue` in `/agents`

Test it:

```bash
/codex:review --background
/codex:status
/codex:result
```

## Commands

### `/codex:review`

Runs a standard Codex code review on uncommitted changes or branch diff.

**Flags:**
- `--base <ref>` — compare against a base branch (e.g., `main`)
- `--wait` — wait synchronously for result
- `--background` — run asynchronously (recommended for multi-file changes)

**Examples:**

```bash
# Review uncommitted changes
/codex:review

# Review current branch vs main
/codex:review --base main

# Run in background
/codex:review --background
```

**Notes:**
- Read-only, no modifications
- Use `/codex:status` and `/codex:result` for background jobs

---

### `/codex:adversarial-review`

Runs a **steerable** review that challenges implementation and design choices. Useful for pressure-testing assumptions, tradeoffs, and alternative approaches.

**Flags:**
- Same as `/codex:review`: `--base`, `--wait`, `--background`
- Accepts **focus text** after flags to steer the review

**Examples:**

```bash
# General adversarial review
/codex:adversarial-review

# Challenge caching and retry design
/codex:adversarial-review --base main challenge whether this was the right caching and retry design

# Focus on race conditions
/codex:adversarial-review --background look for race conditions and question the chosen approach
```

**Use cases:**
- Pre-ship review challenging direction, not just code details
- Testing design choices, hidden assumptions, alternative approaches
- Pressure-testing auth, data loss, rollback, race conditions, reliability

---

### `/codex:rescue`

Delegates a task to Codex through the `codex:codex-rescue` subagent. Codex will investigate, fix, or continue work.

**Flags:**
- `--background` — run asynchronously (recommended for long tasks)
- `--wait` — wait synchronously
- `--resume` — continue latest rescue thread for this repo
- `--fresh` — start a new rescue thread
- `--model <model>` — specify model (e.g., `gpt-5.4-mini`, `spark`)
- `--effort <level>` — reasoning effort: `low`, `medium`, `high`

**Examples:**

```bash
# Investigate test failure
/codex:rescue investigate why the tests started failing

# Fix with smallest safe patch
/codex:rescue fix the failing test with the smallest safe patch

# Resume latest rescue
/codex:rescue --resume apply the top fix from the last run

# Use specific model and effort
/codex:rescue --model gpt-5.4-mini --effort medium investigate the flaky integration test

# Quick fix with spark
/codex:rescue --model spark fix the issue quickly

# Background investigation
/codex:rescue --background investigate the regression
```

**Natural delegation:**

You can also ask naturally:

```text
Ask Codex to redesign the database connection to be more resilient.
```

**Notes:**
- If `--model` or `--effort` omitted, Codex uses its own defaults
- `spark` maps to `gpt-5.3-codex-spark`
- Follow-up rescues can continue the latest task

---

### `/codex:status`

Shows running and recent Codex jobs for the current repository.

**Examples:**

```bash
# Show all jobs
/codex:status

# Show specific job
/codex:status task-abc123
```

**Use cases:**
- Check background work progress
- See latest completed job
- Confirm if task still running

---

### `/codex:result`

Shows final output for a finished job. Includes Codex session ID for resuming in Codex CLI.

**Examples:**

```bash
# Show latest result
/codex:result

# Show specific result
/codex:result task-abc123
```

**Resume in Codex CLI:**

```bash
codex resume <session-id>
```

---

### `/codex:cancel`

Cancels an active background Codex job.

**Examples:**

```bash
# Cancel latest job
/codex:cancel

# Cancel specific job
/codex:cancel task-abc123
```

---

### `/codex:setup`

Checks if Codex is installed and authenticated. Can install Codex if npm is available. Also manages optional review gate.

**Examples:**

```bash
# Check setup
/codex:setup

# Enable review gate (advanced)
/codex:setup --enable-review-gate

# Disable review gate
/codex:setup --disable-review-gate
```

**Review gate:**
- Uses a `Stop` hook to run targeted Codex review based on Claude's response
- Blocks stop if issues found, so Claude can address them
- **Warning:** Can create long Claude/Codex loops and drain usage limits quickly

---

## Configuration

The plugin uses your local Codex CLI configuration. Config is picked up from:

- **User-level:** `~/.codex/config.toml`
- **Project-level:** `.codex/config.toml` (must be trusted)

### Common Configurations

**Set default model and reasoning effort:**

Create `.codex/config.toml` at the root of your project:

```toml
model = "gpt-5.4-mini"
model_reasoning_effort = "high"
```

**Custom OpenAI base URL:**

In your Codex config:

```toml
openai_base_url = "https://your-custom-endpoint.example.com"
```

**Use environment variables for API keys:**

Codex respects `OPENAI_API_KEY` if you're using API key authentication:

```bash
export OPENAI_API_KEY=your-api-key-here
codex login
```

See [Codex config reference](https://developers.openai.com/codex/config-reference) for full options.

---

## Workflow Patterns

### Review Before Shipping

```bash
/codex:review
```

Wait for output, address feedback, commit.

---

### Adversarial Pre-Ship Review

```bash
/codex:adversarial-review --base main challenge the retry and timeout strategy
```

Use this to pressure-test critical design decisions.

---

### Delegate Bug Investigation

```bash
/codex:rescue --background investigate why the build is failing in CI
```

Check in later:

```bash
/codex:status
/codex:result
```

---

### Quick Fix with Spark Model

```bash
/codex:rescue --model spark fix the linter error quickly
```

---

### Resume Previous Rescue

```bash
/codex:rescue --resume apply the suggested fix from the last run
```

---

### Long-Running Background Task

```bash
/codex:adversarial-review --background
/codex:rescue --background investigate the flaky test
```

Monitor:

```bash
/codex:status
```

Retrieve:

```bash
/codex:result
```

Cancel if needed:

```bash
/codex:cancel
```

---

### Continue Work in Codex CLI

After `/codex:result`, copy the session ID and resume directly in Codex:

```bash
codex resume abc123-session-id
```

This lets you review Codex's work or continue it there.

---

## Code Examples

### JavaScript: Triggering Codex Review from a Script

While the plugin is used via Claude Code slash commands, you can programmatically trigger Codex CLI tasks in Node.js:

```javascript
const { execSync } = require('child_process');

function runCodexReview(baseBranch = null) {
  let cmd = 'codex review';
  if (baseBranch) {
    cmd += ` --base ${baseBranch}`;
  }
  try {
    const output = execSync(cmd, { encoding: 'utf-8' });
    console.log(output);
  } catch (error) {
    console.error('Codex review failed:', error.message);
  }
}

runCodexReview('main');
```

### JavaScript: Checking Codex Job Status

```javascript
const { execSync } = require('child_process');

function getCodexStatus(taskId = null) {
  let cmd = 'codex status';
  if (taskId) {
    cmd += ` ${taskId}`;
  }
  try {
    const output = execSync(cmd, { encoding: 'utf-8' });
    return JSON.parse(output); // Adjust based on actual Codex CLI output format
  } catch (error) {
    console.error('Failed to get Codex status:', error.message);
    return null;
  }
}

const status = getCodexStatus();
console.log(status);
```

### JavaScript: Delegating Task with Environment Config

```javascript
const { execSync } = require('child_process');

function delegateToCodex(task, model = 'gpt-5.4-mini', effort = 'medium') {
  // Ensure Codex uses the right config
  process.env.CODEX_MODEL = model;
  process.env.CODEX_REASONING_EFFORT = effort;

  const cmd = `codex rescue "${task}"`;
  try {
    const output = execSync(cmd, { encoding: 'utf-8' });
    console.log('Codex rescue output:', output);
  } catch (error) {
    console.error('Codex rescue failed:', error.message);
  }
}

delegateToCodex('investigate the failing integration test');
```

---

## Troubleshooting

### Codex Not Found

**Symptom:** `/codex:setup` reports Codex is not installed.

**Solution:**

```bash
npm install -g @openai/codex
```

Then re-run:

```bash
/codex:setup
```

---

### Authentication Failed

**Symptom:** Codex commands fail with authentication error.

**Solution:**

```bash
!codex login
```

Follow the prompts to sign in with ChatGPT or API key.

---

### Background Job Stuck

**Symptom:** `/codex:status` shows job running for too long.

**Solution:**

```bash
/codex:cancel
```

Then retry or investigate Codex logs.

---

### Review Gate Draining Usage

**Symptom:** Review gate creates long Claude/Codex loops.

**Solution:**

Disable the review gate:

```bash
/codex:setup --disable-review-gate
```

Only enable when actively monitoring.

---

### Custom Base URL Not Picked Up

**Symptom:** Codex ignores `openai_base_url` config.

**Solution:**

Ensure `.codex/config.toml` is in the project root and the project is **trusted**. See [Codex config docs](https://developers.openai.com/codex/config-advanced#project-config-files-codexconfigtoml).

---

### Node.js Version Too Old

**Symptom:** Plugin fails to load or Codex CLI errors.

**Solution:**

Upgrade to Node.js 18.18+:

```bash
nvm install 18
nvm use 18
```

Or use your system's package manager.

---

## Advanced Usage

### Combining with Claude Code Native Commands

You can alternate between Claude Code's native review and Codex's review:

```bash
# Claude review
/review

# Codex adversarial review
/codex:adversarial-review --base main challenge the error handling strategy
```

### Using Codex Config Profiles

Define multiple configs and switch via environment:

**`.codex/config.toml` (default):**

```toml
model = "gpt-5.4-mini"
model_reasoning_effort = "medium"
```

**`.codex/config-high.toml`:**

```toml
model = "gpt-5.4"
model_reasoning_effort = "high"
```

Switch in shell before running commands:

```bash
export CODEX_CONFIG=.codex/config-high.toml
/codex:rescue investigate the race condition thoroughly
```

(Exact mechanism depends on Codex CLI support; adjust as needed.)

---

### Resuming Codex Sessions

After a rescue or review, grab the session ID from `/codex:result` and resume in Codex CLI for deeper investigation:

```bash
/codex:result
# Copy session ID: abc123-xyz

# In terminal
codex resume abc123-xyz
```

---

## Summary

The Codex plugin for Claude Code bridges two powerful AI coding tools:

- **Standard reviews:** `/codex:review`
- **Adversarial reviews:** `/codex:adversarial-review`
- **Task delegation:** `/codex:rescue`
- **Job management:** `/codex:status`, `/codex:result`, `/codex:cancel`

Install, authenticate, and leverage Codex's deep code understanding alongside Claude Code's agent workflow. Use background jobs for long tasks, adversarial reviews for design challenges, and rescue for delegating investigations and fixes.

**Configuration:** Uses your local Codex CLI config (`~/.codex/config.toml` or `.codex/config.toml`).

**Authentication:** Same as Codex CLI (`codex login`).

**Workflow:** Delegate to Codex, check status, retrieve results, or resume in Codex CLI for deeper work.

---

**Resources:**

- [Codex CLI Reference](https://developers.openai.com/codex/cli/reference/)
- [Codex Config Reference](https://developers.openai.com/codex/config-reference)
- [Codex Pricing](https://developers.openai.com/codex/pricing/)
- [Plugin Repository](https://github.com/openai/codex-plugin-cc)
