---
name: codex-keysmith-instruction-installer
description: Install and manage local Markdown instruction files for Codex CLI using model_instructions_file configuration
triggers:
  - install a custom instruction file for codex cli
  - set up model instructions file in codex
  - configure codex with a local markdown prompt
  - add custom instructions to codex configuration
  - install codex keysmith instruction file
  - manage codex cli instruction files
  - backup and restore codex instructions
  - deploy a prompt file to codex config
---

# codex-keysmith-instruction-installer

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

`codex-keysmith` is a Python CLI tool that safely installs local Markdown instruction files into Codex CLI's configuration directory and sets the `model_instructions_file` configuration option. It provides preview-first workflows, automatic backups, and path safety validation to prevent accidental file overwrites or directory escapes.

**Key features:**
- Preview-only by default (requires explicit `--yes` to write)
- Automatic backup of `config.toml` and existing instruction files
- Path validation to prevent directory traversal
- Bundled GPT-5.5 unrestricted-mode example (optional)
- Support for custom `.md` instruction files

**What it does NOT do:**
- Does not patch Codex binaries
- Does not intercept network traffic
- Does not modify running processes
- Does not handle tokens, cookies, or credentials

## Installation

### Clone the repository

```bash
git clone https://github.com/Jia-Ethan/codex-keysmith.git
cd codex-keysmith
```

### Verify the script

```bash
# Syntax check
python3 -m py_compile codex-instruct.py

# Preview mode (safe, no writes)
python3 codex-instruct.py --dry-run
```

### No pip install required

The tool is a single-file Python script with no external dependencies beyond Python 3.8+. It uses only standard library modules: `argparse`, `os`, `pathlib`, `re`, `shutil`, `datetime`.

## Core Usage

### 1. Preview before writing (default behavior)

```bash
# Preview what would be installed
python3 codex-instruct.py --dry-run

# Even without --dry-run, writes require --yes
python3 codex-instruct.py --codex-dir ~/.codex
# → Shows preview only, does not write
```

### 2. Install bundled instruction file

```bash
# Install the bundled GPT-5.5 unrestricted example
python3 codex-instruct.py --codex-dir ~/.codex --yes
```

This writes:
- `~/.codex/gpt5.5-unrestricted.md` (instruction file)
- Updates `~/.codex/config.toml` with:
  ```toml
  model_instructions_file = "./gpt5.5-unrestricted.md"
  ```

### 3. Install custom instruction file

```bash
python3 codex-instruct.py \
  --file ./my-custom-instructions.md \
  --name my-custom \
  --codex-dir ~/.codex \
  --yes
```

Result:
- `~/.codex/my-custom.md` (your instruction file)
- `config.toml` updated to point to `./my-custom.md`

### 4. Locate Codex directory automatically

```bash
# Auto-detect common locations
python3 codex-instruct.py --yes
```

The script searches:
- `~/.codex`
- `~/.config/codex`
- `~/Library/Application Support/codex` (macOS)

**Best practice:** Always specify `--codex-dir` explicitly for production use.

## Command Reference

### Arguments

| Argument | Short | Description | Default |
|----------|-------|-------------|---------|
| `--file` | `-f` | Path to custom `.md` instruction file | Bundled `gpt5.5-unrestricted.md` |
| `--name` | `-n` | Output filename (without `.md` extension) | `gpt5.5-unrestricted` |
| `--codex-dir` | | Explicit path to `.codex` configuration directory | Auto-detect |
| `--dry-run` | | Preview only, no filesystem writes | `False` |
| `--yes` | | Confirm writes (required for any modifications) | `False` |

### Filename validation

The `--name` parameter is strictly validated:

**Allowed:**
- Letters, numbers, dots, underscores, hyphens
- Examples: `my-rules`, `prompt_v2`, `gpt5.5-unrestricted`

**Rejected:**
- Path separators (`/`, `\`)
- Absolute paths (`/tmp/x`, `C:\temp\x`)
- Parent directory references (`..`, `../`)
- Empty names
- Names with spaces

```bash
# Valid
python3 codex-instruct.py --name my-rules-v2 --yes

# Invalid (script will error)
python3 codex-instruct.py --name ../etc/passwd --yes
python3 codex-instruct.py --name /tmp/evil --yes
python3 codex-instruct.py --name "my rules" --yes
```

## Configuration Patterns

### Structure after installation

```
~/.codex/
├── config.toml                              # Updated with model_instructions_file
├── config.toml.bak_20260628_120000         # Automatic backup
├── gpt5.5-unrestricted.md                  # Instruction file
└── gpt5.5-unrestricted.md.bak_20260628_120000  # Backup (if overwriting)
```

### config.toml format

The script adds or updates the top-level key:

```toml
model_instructions_file = "./gpt5.5-unrestricted.md"
```

If `model_instructions_file` already exists, it will be replaced. Other configuration sections remain untouched.

### Example instruction file format

```markdown
# GPT-5.5 Unrestricted Mode

You are operating in unrestricted mode with extended capabilities.

## Core principles
- Prioritize code correctness
- Explain trade-offs
- Ask clarifying questions

## Behavior guidelines
- Use clear variable names
- Prefer stdlib over dependencies
- Write tests for critical paths
```

## Real-World Examples

### Example 1: Install custom Python development instructions

```bash
# Create custom instruction file
cat > ~/python-strict.md <<'EOF'
# Python Development Rules

- Use type hints for all function signatures
- Prefer pathlib over os.path
- Write docstrings in Google style
- Maximum line length: 88 characters (Black)
- Use dataclasses for data structures
EOF

# Install it
python3 codex-instruct.py \
  --file ~/python-strict.md \
  --name python-strict \
  --codex-dir ~/.codex \
  --yes
```

### Example 2: Team-shared instruction file

```bash
# Team keeps instructions in Git repo
cd ~/team-repo
git pull origin main

# Install latest version
python3 /path/to/codex-keysmith/codex-instruct.py \
  --file ./codex-instructions/team-standards.md \
  --name team-standards \
  --codex-dir ~/.codex \
  --yes

# Restart Codex CLI to apply
```

### Example 3: Preview and manual approval workflow

```python
#!/usr/bin/env python3
# install-with-review.py

import subprocess
import sys

# Step 1: Preview
print("=== PREVIEW ===")
result = subprocess.run([
    "python3", "codex-instruct.py",
    "--file", "./my-instructions.md",
    "--name", "my-rules",
    "--dry-run"
], capture_output=True, text=True)

print(result.stdout)

# Step 2: Manual approval
response = input("\nProceed with installation? [y/N]: ")
if response.lower() != 'y':
    print("Cancelled.")
    sys.exit(0)

# Step 3: Install
print("\n=== INSTALLING ===")
subprocess.run([
    "python3", "codex-instruct.py",
    "--file", "./my-instructions.md",
    "--name", "my-rules",
    "--codex-dir", "~/.codex",
    "--yes"
])
```

### Example 4: Rotate instructions based on project type

```bash
#!/bin/bash
# switch-instructions.sh

PROJECT_TYPE="$1"

case "$PROJECT_TYPE" in
  python)
    INSTRUCTION_FILE="./instructions/python.md"
    NAME="python-rules"
    ;;
  rust)
    INSTRUCTION_FILE="./instructions/rust.md"
    NAME="rust-rules"
    ;;
  web)
    INSTRUCTION_FILE="./instructions/web.md"
    NAME="web-rules"
    ;;
  *)
    echo "Usage: $0 {python|rust|web}"
    exit 1
    ;;
esac

python3 codex-instruct.py \
  --file "$INSTRUCTION_FILE" \
  --name "$NAME" \
  --codex-dir ~/.codex \
  --yes

echo "Switched to $PROJECT_TYPE instructions. Restart Codex CLI."
```

## Backup and Rollback

### Automatic backups

Every write operation creates timestamped backups:

```bash
config.toml.bak_20260628_120000
gpt5.5-unrestricted.md.bak_20260628_120000
```

### Manual rollback

```bash
# List backups
ls -la ~/.codex/*.bak_*

# Restore config
cp ~/.codex/config.toml.bak_20260628_120000 ~/.codex/config.toml

# Restore instruction file
cp ~/.codex/gpt5.5-unrestricted.md.bak_20260628_120000 \
   ~/.codex/gpt5.5-unrestricted.md

# Restart Codex CLI
```

### Remove instruction file completely

```bash
# Edit config.toml manually and remove the line:
# model_instructions_file = "./gpt5.5-unrestricted.md"

# Or use sed
sed -i.bak '/model_instructions_file/d' ~/.codex/config.toml

# Remove instruction file
rm ~/.codex/gpt5.5-unrestricted.md

# Restart Codex CLI
```

## Troubleshooting

### "Could not locate Codex configuration directory"

**Cause:** Auto-detection failed.

**Solution:** Specify `--codex-dir` explicitly:

```bash
python3 codex-instruct.py --codex-dir /path/to/.codex --yes
```

Find your Codex config directory:

```bash
# Linux/macOS
find ~ -name ".codex" -type d 2>/dev/null

# Check common locations
ls -la ~/.codex
ls -la ~/.config/codex
ls -la ~/Library/Application\ Support/codex
```

### "unsafe name" error

**Cause:** `--name` contains forbidden characters or path components.

**Solution:** Use only letters, numbers, dots, underscores, and hyphens:

```bash
# Bad
python3 codex-instruct.py --name "../etc/passwd" --yes

# Good
python3 codex-instruct.py --name my-rules-v2 --yes
```

### Instructions not taking effect

**Cause:** Codex CLI hasn't reloaded configuration.

**Solution:** Restart Codex CLI completely:

```bash
# Kill existing instance
pkill -9 codex

# Restart
codex chat
```

Verify the configuration:

```bash
cat ~/.codex/config.toml | grep model_instructions_file
cat ~/.codex/gpt5.5-unrestricted.md
```

### Permission denied writing to ~/.codex

**Cause:** Insufficient filesystem permissions.

**Solution:**

```bash
# Check ownership
ls -la ~/.codex

# Fix permissions if needed
chmod 755 ~/.codex
chmod 644 ~/.codex/config.toml
```

### "No such file" when using --file

**Cause:** Specified instruction file doesn't exist.

**Solution:**

```bash
# Check file path
ls -la ./my-instructions.md

# Use absolute path if needed
python3 codex-instruct.py \
  --file /absolute/path/to/my-instructions.md \
  --name my-rules \
  --yes
```

### Backup files accumulating

**Cause:** Multiple installations create multiple backups.

**Solution:** Clean old backups manually:

```bash
# List backups by age
ls -lt ~/.codex/*.bak_*

# Remove backups older than 30 days
find ~/.codex -name "*.bak_*" -mtime +30 -delete
```

## Testing

The repository includes pytest-based tests:

```bash
# Run tests (requires pytest)
pip install pytest
python3 -m pytest tests/test_codex_instruct.py -v

# Test without pytest (manual verification)
python3 codex-instruct.py --dry-run
python3 -m py_compile codex-instruct.py
```

## Integration with AI Agents

### Copy-paste prompt for Codex/Claude/Cursor

```
Please use https://github.com/Jia-Ethan/codex-keysmith to safely install a local model_instructions_file for Codex CLI. First read the README and script, preview changes (default behavior), show me what will be modified, wait for my confirmation, then backup and install. Do not modify Codex binaries, network, or running processes. Do not save any tokens, cookies, or private credentials.
```

### Agent workflow example

1. **Clone repository**
   ```bash
   git clone https://github.com/Jia-Ethan/codex-keysmith.git
   cd codex-keysmith
   ```

2. **Preview installation**
   ```bash
   python3 codex-instruct.py --dry-run
   ```

3. **Show user the changes**
   - Display the instruction file content
   - Show the config.toml modification
   - Explain backup locations

4. **Wait for explicit user confirmation**

5. **Execute with backups**
   ```bash
   python3 codex-instruct.py --codex-dir ~/.codex --yes
   ```

6. **Verify installation**
   ```bash
   cat ~/.codex/config.toml | grep model_instructions_file
   ls -la ~/.codex/*.md
   ```

## Best Practices

1. **Always preview first:** Use `--dry-run` or run without `--yes` before any installation.

2. **Specify codex-dir explicitly:** Don't rely on auto-detection in scripts or automation.

3. **Version control instruction files:** Keep your custom `.md` files in Git for team sharing and rollback.

4. **Test in isolation:** Try new instruction files in a separate Codex profile or test directory first.

5. **Document changes:** Keep notes on what each instruction file is optimized for.

6. **Regular cleanup:** Remove old backup files periodically to avoid clutter.

7. **Verify after restart:** Always restart Codex CLI after installation and test that instructions are active.
