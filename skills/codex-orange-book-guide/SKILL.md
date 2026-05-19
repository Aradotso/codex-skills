---
name: codex-orange-book-guide
description: Expert guide for using OpenAI Codex across all five forms (CLI, Desktop, Cloud, IDE, Chrome) based on the complete Orange Book tutorial
triggers:
  - "how do I use OpenAI Codex effectively"
  - "show me Codex CLI commands and workflow"
  - "what are the differences between Codex forms"
  - "help me set up Codex for my project"
  - "explain Codex auto-review and sandbox mode"
  - "how to use Codex Desktop App with Computer Use"
  - "what are Codex Skills and MCP servers"
  - "compare Codex vs Claude Code for my project"
---

# OpenAI Codex Orange Book Guide

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Expert knowledge from "OpenAI Codex: The Complete Guide" (橙皮书) by HuaShu — covering all five forms of Codex (CLI, Desktop App, Cloud, IDE Extension, Chrome Extension) plus mobile companion. This skill teaches practical workflows, commands, and patterns for shipping products with AI coding agents.

## Overview

The Codex Orange Book is a comprehensive guide covering:

- **Five Forms**: CLI (Terminal), Desktop App, Cloud, IDE Extensions, Chrome Extension
- **Mobile Companion**: Remote control for Desktop App (shipped May 14, 2026)
- **GPT-5.5**: Default model with 82.6% SWE-bench Verified, 82.7% Terminal-Bench 2.0
- **Three Pro Tiers**: $20 Pro, $100 Pro (recommended for indie devs), $200 Pro
- **Key Features**: Auto-review, persistent `/goal`, Computer Use, Automations, Memory

## Installation & Setup

### CLI Installation (Primary Interface)

```bash
# Install via npm (requires Node.js 18+)
npm install -g @openai/codex-cli

# Or via Homebrew (macOS)
brew install openai-codex

# Verify installation
codex --version

# Login (opens browser for OAuth)
codex auth login

# Initialize in project directory
cd your-project
codex init
```

### Desktop App Installation

Download from [codex.openai.com](https://codex.openai.com) or install via CLI:

```bash
codex install desktop
```

### Chrome Extension

Install from Chrome Web Store or via CLI:

```bash
codex install chrome
```

## Core CLI Commands

### Project Management

```bash
# Initialize Codex in current directory
codex init

# Start a new chat session
codex chat

# Start with a specific goal
codex chat "Build a REST API with Express"

# Clear context but keep /goal
codex /clear

# Full reset including /goal
codex /reset
```

### Essential Commands (In-Session)

```bash
# Set persistent goal across sessions
/goal Build a real-time chat app with WebSockets

# View current goal
/goal

# Clear goal
/goal clear

# Run shell commands
/sh npm install express
/sh git status

# Edit files with vim
/vim src/index.js

# Read file contents
/read package.json

# Write/create files
/write src/config.js
# (opens editor, save and exit to apply)

# Approve all pending changes
/approve

# Reject pending changes
/reject

# Enable full auto-review (caution: review settings first)
/auto-review all

# Disable auto-review
/auto-review off

# Check current mode
/mode
```

### Sandbox & Safety

```bash
# Run in sandbox mode (isolated environment)
codex --sandbox

# Enable file watching (auto-sync changes)
codex --watch

# Limit operations to specific directories
codex --restrict src/,tests/

# Dry run (show what would happen)
codex --dry-run "refactor auth module"
```

## Auto-Review System

Codex v2.0 introduced auto-review that approves ~99% of low-risk actions automatically:

```bash
# Configure auto-review levels
/auto-review interactive  # Default: prompt for high-risk only
/auto-review all          # Auto-approve everything (DANGEROUS)
/auto-review off          # Prompt for all changes

# Check what's pending approval
/status

# Review individual changes
/diff src/index.js
```

**Safety Note**: Never use `/auto-review all` with Full Access mode on Windows — documented cases of 370GB+ file deletions.

## Desktop App Features

### Computer Use

The Desktop App can control your computer beyond the terminal:

```python
# Example: Codex opening browser and filling forms
# (Natural language in Desktop App chat)
"""
Open Chrome, navigate to github.com/new, 
create a repository named 'my-project',
initialize with README, and copy the clone URL
"""
```

### Multi-Day Automations

```bash
# Set up recurring automation
/automation create "Daily backup"
  schedule: "0 2 * * *"  # 2 AM daily
  tasks:
    - /sh npm run backup
    - /sh git add .
    - /sh git commit -m "Auto backup"
    - /sh git push

# List automations
/automation list

# Pause automation
/automation pause "Daily backup"
```

### Mobile Companion

```bash
# Connect mobile app (ChatGPT iOS/Android) to Desktop
codex remote-control enable

# Get QR code for pairing
codex remote-control qr

# Send commands from mobile
# (Use ChatGPT app, say: "Tell my desktop Codex to run tests")

# Disable remote control
codex remote-control disable
```

## AGENTS.md Configuration

Create `AGENTS.md` in your project root to guide Codex behavior:

```markdown
# Project: MyApp
# Stack: Next.js 14, TypeScript, Tailwind, Supabase

## Architecture
- `/app` - Next.js App Router pages
- `/components` - React components (use 'use client' for interactive)
- `/lib` - Utilities and API clients
- `/supabase` - Database schema and migrations

## Coding Standards
- Use TypeScript strict mode
- Follow Airbnb style guide
- Prefer functional components with hooks
- Use Zod for validation
- Write tests with Vitest

## Never
- Don't commit .env files
- Don't use `any` type
- Don't install packages without asking
- Don't modify database/schema.sql directly (use migrations)

## Dependencies
- Authentication: Supabase Auth
- Styling: Tailwind + shadcn/ui
- State: Zustand for global, useState for local
- Forms: React Hook Form + Zod

## Testing
Run tests before committing:
```bash
npm test
npm run typecheck
npm run lint
```

## Deployment
Deploy via Vercel:
```bash
npm run build
vercel deploy --prod
```
```

## Skills & MCP Servers

### Installing Skills

```bash
# Install skill from file
codex skill install ./path/to/SKILL.md

# Install from URL
codex skill install https://example.com/skills/nextjs-expert.md

# List installed skills
codex skill list

# Enable/disable skills
codex skill enable nextjs-expert
codex skill disable nextjs-expert

# Remove skill
codex skill remove nextjs-expert
```

### Using MCP (Model Context Protocol) Servers

```bash
# Configure MCP server in ~/.config/codex/mcp.json
cat > ~/.config/codex/mcp.json << 'EOF'
{
  "servers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    },
    "postgres": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp/postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      }
    }
  }
}
EOF

# Use MCP tools in chat
codex chat "Use github MCP to create an issue"

# List available MCP tools
/mcp list
```

## IDE Extensions

### VS Code Extension

```bash
# Install extension
code --install-extension openai.codex

# Or via CLI
codex install vscode

# Use in VS Code
# Cmd/Ctrl + Shift + P → "Codex: Start Chat"
# Select code → Right click → "Ask Codex"
```

### Cursor Integration

Codex can work alongside Cursor:

```bash
# Use Codex for file operations, Cursor for inline edits
codex chat "Set up the project structure"
# Then switch to Cursor for fine-grained code changes
```

## Cloud & Chrome Extension

### Cloud Sessions

```bash
# Start cloud session (no local install needed)
# Visit cloud.codex.openai.com

# Connect local CLI to cloud session
codex cloud connect

# Sync local project to cloud
codex cloud sync

# Run long-running tasks in cloud
codex cloud run "npm run build && deploy to staging"
```

### Chrome Extension Usage

```python
# Example: Scraping and automation
"""
Codex Chrome Extension can:
1. Extract structured data from current page
2. Fill forms automatically
3. Navigate multi-step workflows
4. Capture screenshots with annotations
"""

# In chat with Chrome extension active:
# "Extract all product prices from this page into a CSV"
# "Fill out this form with test data from our fixtures"
# "Click through the checkout flow and screenshot each step"
```

## Real-World Examples

### Example 1: Building an Express API

```bash
# Start with goal
codex chat

# In chat:
/goal Build a REST API with Express, TypeScript, and Prisma. Include auth with JWT.

# Codex will:
# 1. Initialize package.json
# 2. Install dependencies
# 3. Set up TypeScript config
# 4. Create folder structure
# 5. Implement routes, middleware, auth
# 6. Set up Prisma schema
# 7. Write tests

# Review changes
/status

# Approve all
/approve

# Run the server
/sh npm run dev
```

### Example 2: Adding a Feature with Computer Use (Desktop App)

```markdown
In Desktop App chat:

"I need to add OAuth login to my Next.js app. 
Open the Supabase dashboard in my browser,
create a new OAuth app for Google,
copy the client ID and secret,
update my .env.local file,
and implement the login button component."

(Desktop App will control browser, copy credentials, edit files)
```

### Example 3: Multi-Day Project with Automations

```bash
# Set up project automation
/automation create "Nightly build and test"
  schedule: "0 0 * * *"
  tasks:
    - /sh git pull origin main
    - /sh npm install
    - /sh npm run build
    - /sh npm test
    - /sh npm run e2e
    - notify: "Build status: ${STATUS}"

# Set persistent goal for tomorrow
/goal Complete the payment integration module with Stripe. 
Include webhook handling, subscription management, and invoice generation.

# Close session - goal persists across days
/exit
```

### Example 4: Using Skills with AGENTS.md

```bash
# Install Next.js skill
codex skill install https://skills.ara.so/nextjs-14-app-router.md

# Create AGENTS.md
cat > AGENTS.md << 'EOF'
# Use Next.js 14 App Router conventions
# Reference the nextjs-14-app-router skill for patterns
# Deploy to Vercel
EOF

# Codex now has both skill + project context
codex chat "Add a new blog post page with MDX support"
```

## Pricing Tiers (As of May 2026)

| Tier | Price | Best For | Limits |
|------|-------|----------|--------|
| **Free** | $0 | Testing | 25 messages/day, GPT-4o |
| **Pro** | $20/mo | Casual users | 500 msgs/day, GPT-5.5 |
| **Pro Plus** | $100/mo | **Indie devs** | 5K msgs/day, priority, Cloud |
| **Pro Max** | $200/mo | Teams | Unlimited, MultiAgentV2, Automations |

**Recommendation**: $100 Pro Plus is the sweet spot for indie developers shipping products.

## Persistent `/goal` System

Key feature in v2.0 — goals survive across sessions:

```bash
# Set a long-term goal
/goal Build a SaaS product for invoice management. 
Include multi-tenant architecture, PDF generation, 
email reminders, and Stripe integration.

# Work on it across multiple sessions
# Day 1:
codex chat "Start with database schema and auth"
/exit

# Day 2:
codex chat "Continue from where we left off"
# (Codex remembers the /goal)

# Day 3:
codex chat "Add PDF generation with Puppeteer"

# Goal survives /clear (context reset)
/clear
codex chat "What's my current goal?"
# → Returns the invoice SaaS goal

# Remove goal when done
/goal clear
```

## Troubleshooting

### Common Issues

```bash
# Issue: "Context limit exceeded"
# Solution: Clear context, keep goal
/clear
codex chat "Continue with the same goal"

# Issue: Codex suggesting wrong patterns
# Solution: Update AGENTS.md with constraints
echo "## Never use class components, only functional" >> AGENTS.md

# Issue: Auto-review approving too much
# Solution: Switch to interactive mode
/auto-review interactive

# Issue: Desktop App not connecting to mobile
# Solution: Regenerate QR code
codex remote-control disable
codex remote-control enable
codex remote-control qr

# Issue: MCP server not working
# Solution: Check env vars and permissions
echo $GITHUB_TOKEN  # Should output token
codex mcp debug github

# Issue: Slow responses
# Solution: Check model (should be GPT-5.5)
/model
# If not on GPT-5.5, upgrade plan or switch:
/model gpt-5.5
```

### Windows Full Access Warning

**CRITICAL**: Do NOT enable Full Access mode on Windows. Documented cases:
- User lost 370GB of files
- User lost 700GB of files  
- User lost 240GB of system files

Use `--restrict` flag instead:

```bash
codex --restrict C:\Users\YourName\Projects\
```

### Debugging Failed Automations

```bash
# Check automation logs
codex automation logs "Daily backup"

# Test automation manually
codex automation run "Daily backup" --dry-run

# Fix and retry
codex automation edit "Daily backup"
```

## When to Use Codex vs. Claude Code

From §10 of the Orange Book:

**Use Codex when**:
- Building new projects from scratch (better project setup)
- Need Computer Use (browser automation, UI testing)
- Running long multi-day workflows (persistent /goal)
- Need cloud execution (no local resources)
- Want mobile remote control

**Use Claude Code when**:
- Refactoring existing complex code (Opus 4.7: 64.3% SWE-bench)
- Need highest reasoning quality (Opus 4.7 > GPT-5.5)
- Working in mature codebases (better at understanding existing patterns)
- Prefer Cursor-like inline editing

**Dual-tool workflow**:
```bash
# Use Codex for scaffolding
codex chat "Set up a React Native app with Expo, TypeScript, and navigation"

# Switch to Claude Code for complex logic
# Open in Cursor/Claude Code:
# "Refactor the authentication flow to handle edge cases"
```

## Advanced Patterns

### Hooks for Custom Workflows

Create `.codex/hooks/pre-approve.sh`:

```bash
#!/bin/bash
# Run linter before approving changes

echo "Running linter..."
npm run lint

if [ $? -ne 0 ]; then
  echo "❌ Lint errors found. Fix before approving."
  exit 1
fi

echo "✅ Lint passed"
exit 0
```

Make executable:

```bash
chmod +x .codex/hooks/pre-approve.sh
```

### Multi-Agent Workflows (Pro Max)

```bash
# Enable MultiAgentV2 (requires $200/mo Pro Max)
/multi-agent enable

# Assign specialized agents
/agent create frontend --skills nextjs-14,tailwind
/agent create backend --skills express,prisma
/agent create testing --skills vitest,playwright

# Coordinate work
codex chat "Frontend agent: build the UI. 
Backend agent: create the API. 
Testing agent: write e2e tests. 
Work in parallel."
```

### Version Control Integration

```bash
# Auto-commit approved changes
cat > .codex/hooks/post-approve.sh << 'EOF'
#!/bin/bash
git add .
git commit -m "Codex: $(codex last-message --summary)"
EOF

chmod +x .codex/hooks/post-approve.sh
```

## Resources

- **Official Docs**: [codex.openai.com/docs](https://codex.openai.com/docs)
- **Orange Book PDF**: Download from [github.com/alchaincyf/codex-orange-book](https://github.com/alchaincyf/codex-orange-book)
- **Skills Repository**: [ara.so/skills](https://ara.so/skills)
- **HuaShu's Site**: [huasheng.ai](https://www.huasheng.ai/)
- **Community**: X/Twitter [@AlchainHust](https://x.com/AlchainHust)

## Environment Variables

```bash
# Required
export OPENAI_API_KEY=your_key_here  # Or use `codex auth login`

# Optional
export CODEX_MODEL=gpt-5.5           # Default model
export CODEX_AUTO_REVIEW=interactive # Auto-review level
export CODEX_RESTRICT=src/,tests/    # Restrict file access
export GITHUB_TOKEN=ghp_xxxxx        # For GitHub MCP
export DATABASE_URL=postgresql://... # For Prisma/Postgres MCP
```

## Tips from the Orange Book

1. **Start with `/goal`**: Set persistent goals for multi-session projects
2. **Use `AGENTS.md`**: Guide Codex with project-specific rules upfront
3. **Install skills**: Don't reinvent patterns, use community skills
4. **Desktop for automation**: Computer Use + Automations = powerful workflows
5. **Mobile for monitoring**: Remote control lets you check progress anywhere
6. **Sandbox for experiments**: Use `--sandbox` when trying risky changes
7. **Hook into your toolchain**: Pre/post approve hooks integrate with CI/CD
8. **$100 tier is sweet spot**: Pro Plus gives Cloud + enough capacity for indie shipping
9. **Dual-tool when needed**: Codex for scaffolding, Claude Code for complex refactors
10. **Read the Orange Book**: 200+ pages of real-world patterns and gotchas

---

*This skill is based on "OpenAI Codex: The Complete Guide" v2.0.1 by HuaShu (花叔), part of the Orange Book Series. Licensed CC BY-NC-SA 4.0.*
