---
name: codex-hygiene-skill
description: Audit and tune Codex Desktop context surfaces, tool availability, and token usage through telemetry measurement
triggers:
  - "measure my Codex context usage"
  - "check Codex tool availability"
  - "audit token usage in this thread"
  - "show me Codex telemetry stats"
  - "analyze Codex Desktop performance"
  - "review MCP server status"
  - "optimize Codex context size"
  - "check why Codex is slow"
---

# Codex Hygiene Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

This skill provides expertise in using **codex-hygiene**, a tool for auditing and tuning Codex Desktop context and tool surfaces. It measures recent telemetry, reviews MCP/app/skill availability, and helps keep long-running goal workflows scoped to current work.

## What Codex Hygiene Does

Codex Hygiene is a diagnostic skill that:

- **Measures token usage**: Queries Codex Desktop SQLite telemetry databases to show recent token consumption per thread and window
- **Audits tool availability**: Distinguishes actual tool calls from tool availability, enabled state from cached inventory
- **Identifies bottlenecks**: Helps correlate elevated usage with app surface size, MCP/plugin state, snapshot reuse, stale project stanzas, long-thread replay, or background fan-out
- **Suggests reversible hygiene**: Recommends cleanup steps without deleting logs, caches, or projects
- **Maintains quality**: Keeps long-running goal work quality-aware by narrowing replay and tool scope

## Installation

Install codex-hygiene into your Codex skills directory:

```bash
# Create skills directory if needed
mkdir -p "$HOME/.agents/skills"

# Clone the repository
git clone https://github.com/sunflower-of-parchman/codex-hygiene.git \
  "$HOME/.agents/skills/codex-hygiene"
```

After installation, invoke the skill with `$codex-hygiene`. Codex normally detects newly installed skills automatically. Restart Codex Desktop if the skill doesn't appear.

## Key Commands

### Measure Context Usage

The primary command is `measure_codex_context.sh`, which queries Codex telemetry:

```bash
# Basic measurement (recent activity)
"$HOME/.agents/skills/codex-hygiene/scripts/measure_codex_context.sh"

# Measure specific window (last 5 interactions)
"$HOME/.agents/skills/codex-hygiene/scripts/measure_codex_context.sh" 5

# Measure specific window with more history
"$HOME/.agents/skills/codex-hygiene/scripts/measure_codex_context.sh" 30

# Measure specific thread in window
"$HOME/.agents/skills/codex-hygiene/scripts/measure_codex_context.sh" 5 <thread_id>
```

### Script Parameters

- **First argument**: Number of recent entries to examine (default: recent activity)
- **Second argument**: Specific thread ID to analyze (optional)

### Environment Variables

```bash
# Custom Codex data location
export CODEX_HOME="$HOME/.codex-custom"

# Skill installation directory (if not default)
export SKILL_DIR="$HOME/my-custom-path/codex-hygiene"
```

## Understanding Output

The measurement script provides compact counts covering:

### Token Telemetry
- Input tokens by thread
- Output tokens by thread
- Total tokens per interaction
- Window-level aggregates

### Tool Availability
- Number of tools reported as available
- Tools actually called
- MCP servers enabled vs. cached
- App integrations active

### Context Sources
- Snapshot reuse frequency
- Project stanza count
- Thread replay depth
- Background task count

**Safety note**: The script does NOT dump full logs, configs, tool schemas, secrets, or environment values.

## Configuration

### Codex Configuration File

Codex Hygiene reads but does not modify `~/.codex/config.toml`. Always back up before manual edits:

```bash
# Backup your config
cp ~/.codex/config.toml ~/.codex/config.toml.backup

# View current MCP servers
cat ~/.codex/config.toml | grep -A 10 "\[mcp\]"
```

### Custom Data Locations

If your Codex data lives elsewhere:

```bash
export CODEX_HOME="/path/to/codex/data"
"$SKILL_DIR/scripts/measure_codex_context.sh"
```

## Common Patterns

### Diagnose High Token Usage

```bash
# Measure recent threads
SKILL_DIR="$HOME/.agents/skills/codex-hygiene"
"$SKILL_DIR/scripts/measure_codex_context.sh" 10

# Check if usage correlates with:
# - Many MCP servers enabled
# - Large tool availability surface
# - Deep thread replay
# - Stale project contexts
```

### Audit MCP Server State

```bash
# List MCP servers (requires jq and codex CLI)
codex mcp list

# Check server status in config
cat ~/.codex/config.toml | grep -A 5 "\\[mcp.servers"

# Compare enabled vs. actually-called tools in telemetry
"$SKILL_DIR/scripts/measure_codex_context.sh" 5
```

### Optimize Long-Running Threads

For threads with elevated token usage:

```bash
# Measure specific thread
"$SKILL_DIR/scripts/measure_codex_context.sh" 20 thread_abc123

# Review recommendations in references/long-thread-replay.md
cat "$SKILL_DIR/references/long-thread-replay.md"

# Consider:
# - Starting fresh thread for new subtask
# - Disabling unused MCP servers temporarily
# - Removing stale project paths from config
```

### Pre-Deploy Hygiene Check

Before starting a large goal or project:

```bash
# 1. Measure baseline
"$SKILL_DIR/scripts/measure_codex_context.sh" 5

# 2. Review MCP servers - disable unused
codex mcp list
# Edit config to comment out unused servers

# 3. Clean stale project contexts
# Review ~/.codex/config.toml [projects] section

# 4. Restart Codex Desktop to apply changes
```

## Real Code Examples

### Shell Integration

```bash
#!/bin/bash
# Add to your .bashrc or .zshrc for quick hygiene checks

codex_measure() {
    local skill_dir="$HOME/.agents/skills/codex-hygiene"
    if [ -d "$skill_dir" ]; then
        "$skill_dir/scripts/measure_codex_context.sh" "${1:-10}"
    else
        echo "codex-hygiene not installed"
    fi
}

# Usage: codex_measure 5
```

### Pre-Commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-push
# Check Codex hygiene before pushing code

SKILL_DIR="$HOME/.agents/skills/codex-hygiene"
if [ -f "$SKILL_DIR/scripts/measure_codex_context.sh" ]; then
    echo "Running Codex hygiene check..."
    "$SKILL_DIR/scripts/measure_codex_context.sh" 3
fi
```

### Periodic Monitoring Script

```bash
#!/bin/bash
# monitor_codex_hygiene.sh
# Run daily to track token usage trends

SKILL_DIR="$HOME/.agents/skills/codex-hygiene"
LOG_FILE="$HOME/.codex-hygiene-history.log"

timestamp=$(date +"%Y-%m-%d %H:%M:%S")
echo "=== $timestamp ===" >> "$LOG_FILE"
"$SKILL_DIR/scripts/measure_codex_context.sh" 5 >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"

# Review trends
tail -50 "$LOG_FILE"
```

## Troubleshooting

### Script Not Found

**Problem**: `command not found: measure_codex_context.sh`

**Solution**:
```bash
# Verify installation
ls "$HOME/.agents/skills/codex-hygiene/scripts/"

# Use full path
SKILL_DIR="$HOME/.agents/skills/codex-hygiene"
"$SKILL_DIR/scripts/measure_codex_context.sh"

# Or add to PATH
export PATH="$HOME/.agents/skills/codex-hygiene/scripts:$PATH"
```

### SQLite Database Locked

**Problem**: `database is locked`

**Solution**:
```bash
# Close Codex Desktop
# Wait 5 seconds
# Run measurement again
"$SKILL_DIR/scripts/measure_codex_context.sh" 5

# The script uses -readonly flag, but active writes can block
```

### No Telemetry Data

**Problem**: Script shows no data or zero counts

**Solution**:
```bash
# Check if Codex telemetry database exists
ls -lh ~/.codex/telemetry.db

# Check if CODEX_HOME is set incorrectly
echo $CODEX_HOME

# Verify Codex Desktop has been used recently
# (telemetry is only written during active use)
```

### jq or codex CLI Not Found

**Problem**: Optional tools missing

**Solution**:
```bash
# Install jq (macOS)
brew install jq

# Install jq (Linux)
sudo apt-get install jq  # Debian/Ubuntu
sudo yum install jq      # RedHat/CentOS

# Verify codex CLI
which codex

# These are optional - core measurement works without them
```

### Permission Denied

**Problem**: Cannot read telemetry database

**Solution**:
```bash
# Check permissions
ls -l ~/.codex/telemetry.db

# Fix if needed (database should be user-readable)
chmod 644 ~/.codex/telemetry.db

# Verify ownership
ls -l ~/.codex/
```

## Advanced Usage

### Custom Telemetry Queries

The measurement script uses read-only SQLite queries. You can run custom queries:

```bash
# Interactive SQLite session
sqlite3 -readonly ~/.codex/telemetry.db

# Example: List all tables
.tables

# Example: Show schema
.schema

# Example: Count total interactions
SELECT COUNT(*) FROM interactions;

# Exit
.quit
```

### Combining with Other Tools

```bash
# Export measurement to JSON for analysis
"$SKILL_DIR/scripts/measure_codex_context.sh" 20 | \
  awk '/tokens/{print}' | \
  tee codex-usage.txt

# Watch telemetry in real-time
watch -n 5 "$SKILL_DIR/scripts/measure_codex_context.sh" 3

# Compare before/after MCP changes
"$SKILL_DIR/scripts/measure_codex_context.sh" 5 > before.txt
# Make MCP config changes and restart Codex
"$SKILL_DIR/scripts/measure_codex_context.sh" 5 > after.txt
diff before.txt after.txt
```

## References

The skill includes detailed references:

- **references/remediation.md**: Step-by-step cleanup recommendations
- **references/long-thread-replay.md**: Managing token usage in long conversations

```bash
# View remediation guide
cat "$HOME/.agents/skills/codex-hygiene/references/remediation.md"

# View long-thread guide
cat "$HOME/.agents/skills/codex-hygiene/references/long-thread-replay.md"
```

## Safety & Best Practices

1. **Read-only by default**: Scripts use `sqlite3 -readonly` flag
2. **No secrets dumped**: Output excludes configs, schemas, env vars, API keys
3. **Backup configs**: Always backup `~/.codex/config.toml` before editing
4. **Reversible actions**: Recommendations focus on disable/restart, not delete
5. **Version awareness**: Telemetry schemas may change across Codex versions

## Testing

Run the included test suite:

```bash
cd "$HOME/.agents/skills/codex-hygiene"
bash tests/measure_codex_context_test.sh
```

## Compatibility

- **OS**: macOS, Linux, Unix-like systems
- **Requirements**: Bash, `sqlite3`, Perl, `awk`, `sort`
- **Optional**: `jq`, `codex` CLI for enhanced app-cache and plugin summaries
- **Codex**: Designed for Codex Desktop with local telemetry databases

## When to Use This Skill

Use codex-hygiene when:

- Codex Desktop feels slow or unresponsive
- Token usage seems unexpectedly high
- You want to audit which tools are actually being called
- Long-running threads are accumulating context
- You're debugging MCP server configuration
- You need to optimize before a large coding session
- You want visibility into Codex's internal state

---

**Project**: [sunflower-of-parchman/codex-hygiene](https://github.com/sunflower-of-parchman/codex-hygiene)  
**License**: MIT
