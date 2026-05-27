---
name: codexguide-reference
description: CodexGuide - Comprehensive practical guide for OpenAI Codex across CLI, desktop app, cloud, and IDE integrations for beginners to teams
triggers:
  - how do I get started with OpenAI Codex
  - show me CodexGuide documentation
  - help me set up Codex CLI
  - what's the difference between Codex app and CLI
  - how to configure AGENTS.md for my project
  - guide me through Codex sandbox and approvals
  - Codex best practices for teams
  - troubleshoot Codex installation issues
---

# CodexGuide Reference

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

CodexGuide is a comprehensive practical guide for OpenAI Codex that helps beginners, creators, developers, and teams learn how to effectively use Codex across different interfaces (CLI, desktop app, cloud, IDE extensions) and integrate it into real-world workflows.

## What CodexGuide Covers

CodexGuide addresses three core questions:

1. **How to start**: Which entry point, task, and settings should beginners use
2. **How to deliver**: How to communicate requirements so Codex can read projects, modify files, run commands, and produce verifiable results
3. **How to accumulate**: How to turn successful tasks into reusable templates, rules, cases, and safety boundaries for teams

The guide is organized into:

- **Entry paths**: Desktop app, CLI, Cloud/Web, IDE extensions, ChatGPT mobile
- **Configuration topics**: CLI options, `config.toml`, MCP, Skills, Subagents, security approvals
- **Workflow methods**: Task design, verification approaches, non-development workflows, team playbooks
- **Practical cases**: PPT, Draw.io, browser automation, Obsidian, Feishu, Figma, Notion, CI fixes
- **Official references**: OpenAI documentation index and authoritative sources

## Accessing CodexGuide

### Online Documentation

Visit the comprehensive documentation site:

```bash
# Online reading
https://codexguide.ai/

# Direct paths
https://codexguide.ai/guide/00-overview.html  # Learning roadmap
https://codexguide.ai/platform/               # Platform comparison
https://codexguide.ai/configuration/          # Configuration topics
https://codexguide.ai/practice/               # Practice methods
https://codexguide.ai/recipes/                # Real-world cases
```

### Local Development

Clone and run the documentation locally:

```bash
# Clone the repository
git clone https://github.com/freestylefly/CodexGuide.git
cd CodexGuide

# Install dependencies (requires Node.js 18+)
pnpm install

# Start development server
pnpm dev

# Build static site
pnpm build
```

## Key Learning Paths

### For First-Time Users

1. **Start with desktop app** ([guide/01-app-installation.md](https://codexguide.ai/guide/01-app-installation.html))
   - Download and install Codex desktop app
   - Subscribe to Plus/Pro
   - Understand the interface
   - Complete first low-risk task

2. **Mobile coordination** ([guide/04-mobile-control-desktop.md](https://codexguide.ai/guide/04-mobile-control-desktop.html))
   - Use ChatGPT mobile app to track desktop tasks
   - Coordinate between devices

### For Developers Integrating Codex

1. **CLI setup** ([guide/11-cli-installation.md](https://codexguide.ai/guide/11-cli-installation.html)):

```bash
# Install Codex CLI
npm install -g @openai/codex-cli

# Login
codex login

# Initialize in your project
cd your-project
codex init

# Run your first task
codex "add unit tests for the authentication module"
```

2. **Project configuration with AGENTS.md** ([guide/14-agents-md.md](https://codexguide.ai/guide/14-agents-md.html)):

```markdown
# AGENTS.md example structure

## Project Overview
Brief description of the project, tech stack, and purpose.

## Development Rules
- Code style guidelines
- Testing requirements
- File organization patterns

## Task Boundaries
- What Codex should do
- What requires human approval
- Security constraints

## Common Tasks
### Adding a feature
1. Create feature branch
2. Write tests first
3. Implement feature
4. Update documentation

### Fixing a bug
1. Reproduce the issue
2. Add regression test
3. Fix and verify
4. Update changelog
```

3. **Sandbox and approvals** ([guide/15-sandbox-approvals.md](https://codexguide.ai/guide/15-sandbox-approvals.html)):

```toml
# config.toml example
[sandbox]
enabled = true
allowed_commands = ["npm", "git", "pytest"]
allowed_paths = ["src/", "tests/", "docs/"]

[approvals]
require_approval_for_commands = ["rm", "docker", "kubectl"]
require_approval_for_paths = [".env", "secrets/"]
require_approval_for_network = true
```

### For Teams and Tool Builders

1. **Team playbook structure** ([practice/team-playbook.md](https://codexguide.ai/practice/team-playbook.html)):

```markdown
## Team Codex Playbook

### Entry Point Selection
- CLI for local development
- Cloud for code review and collaboration
- IDE extensions for inline assistance

### Shared AGENTS.md
- Team coding standards
- Approval workflows
- Security boundaries
- Communication patterns

### Task Templates
#### Feature Development
- Requirements gathering
- Test-driven approach
- Documentation updates
- Code review process

#### Bug Fixes
- Reproduction steps
- Root cause analysis
- Fix verification
- Regression prevention

### Review and Iteration
- Weekly retrospectives
- Template updates
- Security audit
- Knowledge sharing
```

2. **Security configuration** ([configuration/security-admin.md](https://codexguide.ai/configuration/security-admin.html)):

```toml
# Security-focused config.toml
[security]
# Prevent access to sensitive files
blocked_paths = [
  ".env",
  ".env.*",
  "secrets/",
  "credentials/",
  "*.pem",
  "*.key"
]

# Require approval for destructive operations
dangerous_commands = [
  "rm -rf",
  "drop table",
  "delete from",
  "docker system prune",
  "kubectl delete"
]

# Network restrictions
allow_network_access = false
allowed_domains = ["api.example.com", "docs.example.com"]

# Credential management
never_log_credentials = true
use_env_vars = true
```

## Platform Comparison

### CLI vs Desktop App vs Cloud vs IDE

**Use CLI when:**
- Working in existing projects with Git
- Need deep project context and multi-file edits
- Want to run commands and verify results locally
- Integrating with CI/CD pipelines

**Use Desktop App when:**
- First-time user learning Codex
- Need visual interface and file tree
- Want to preview changes before applying
- Working on personal projects with lower risk

**Use Cloud/Web when:**
- Collaborating with team on code review
- Sharing Codex sessions with others
- Need access from any browser
- Working on documentation or analysis

**Use IDE Extensions when:**
- Want inline code suggestions
- Need context-aware completions
- Prefer staying in your editor (VS Code, Cursor, etc.)
- Working on focused, file-level tasks

## Configuration Topics

### CLI Options

```bash
# Basic usage
codex "task description"

# Specify files
codex "refactor this file" --files src/app.js

# Approve all changes automatically (use with caution)
codex "add logging" --auto-approve

# Use specific model
codex "optimize performance" --model gpt-4

# Dry run (show plan without executing)
codex "migrate database" --dry-run

# Include specific context
codex "fix bug" --context tests/,docs/

# Set working directory
codex "update configs" --cwd ./backend
```

### MCP (Model Context Protocol) Integration

```json
{
  "mcp": {
    "enabled": true,
    "providers": [
      {
        "name": "github",
        "type": "repository",
        "config": {
          "owner": "your-org",
          "repo": "your-repo"
        }
      },
      {
        "name": "slack",
        "type": "communication",
        "config": {
          "workspace_id": "${SLACK_WORKSPACE_ID}"
        }
      }
    ]
  }
}
```

### Skills and Subagents

```yaml
# skill.yaml example
name: python-testing-expert
description: Expert in Python testing with pytest
triggers:
  - write tests for this Python module
  - add pytest fixtures
  - mock external dependencies

capabilities:
  - pytest
  - unittest
  - mocking
  - fixtures
  - parametrization

instructions: |
  When writing Python tests:
  1. Use pytest as the default framework
  2. Organize tests in test_*.py files
  3. Use fixtures for setup/teardown
  4. Mock external API calls
  5. Include docstrings explaining test purpose
  6. Aim for >80% coverage
```

## Common Workflow Patterns

### Development Task Flow

```bash
# 1. Start with clear task description
codex "implement user authentication with JWT tokens"

# 2. Review proposed changes
# Codex will show files to be modified and plan

# 3. Approve or iterate
# Type 'y' to approve, 'n' to reject, or provide feedback

# 4. Verify results
npm test
npm run lint

# 5. Commit changes
git add .
git commit -m "feat: add JWT authentication"
```

### Non-Development Workflows

**Content Creation:**
```bash
# Generate documentation
codex "create API documentation from source code"

# Create presentations
codex "generate PowerPoint outline for quarterly review"

# Organize knowledge base
codex "convert meeting notes to Obsidian markdown with tags"
```

**Browser Automation:**
```bash
# Web scraping
codex "scrape product data from this e-commerce site"

# Form filling
codex "automate form submission for these entries"
```

**Data Processing:**
```bash
# CSV manipulation
codex "merge these three CSV files and remove duplicates"

# Data analysis
codex "analyze sales data and generate summary report"
```

## Troubleshooting

### Common Issues

**Authentication errors:**
```bash
# Re-login
codex logout
codex login

# Check authentication status
codex whoami
```

**Permission errors:**
```bash
# Check sandbox configuration
cat ~/.config/codex/config.toml

# Temporarily disable sandbox for debugging (use carefully)
codex "task" --no-sandbox
```

**Context not loaded:**
```bash
# Explicitly specify context files
codex "task" --context src/,tests/,README.md

# Re-initialize project
rm -rf .codex
codex init
```

**Changes not applied:**
```bash
# Check git status
git status

# Review Codex session logs
codex logs

# Use verbose mode
codex "task" --verbose
```

## Real-World Examples

### Example 1: Adding Tests to Existing Code

```bash
# Task: Add comprehensive tests for a Python module
codex "add pytest tests for src/auth/jwt.py with at least 90% coverage"

# Codex will:
# 1. Analyze existing code
# 2. Create tests/auth/test_jwt.py
# 3. Add fixtures in tests/conftest.py
# 4. Mock external dependencies
# 5. Add parametrized tests for edge cases
```

Generated test file:
```python
import pytest
from unittest.mock import patch, MagicMock
from src.auth.jwt import create_token, verify_token, TokenExpiredError

@pytest.fixture
def mock_user():
    return {
        "id": 123,
        "email": "user@example.com",
        "role": "admin"
    }

def test_create_token_success(mock_user):
    token = create_token(mock_user)
    assert isinstance(token, str)
    assert len(token) > 0

def test_verify_token_valid(mock_user):
    token = create_token(mock_user)
    payload = verify_token(token)
    assert payload["id"] == mock_user["id"]
    assert payload["email"] == mock_user["email"]

@pytest.mark.parametrize("invalid_token", [
    "",
    "invalid.token.string",
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.invalid",
])
def test_verify_token_invalid(invalid_token):
    with pytest.raises(ValueError):
        verify_token(invalid_token)

@patch('src.auth.jwt.datetime')
def test_token_expiration(mock_datetime, mock_user):
    # Mock time to test expiration
    mock_datetime.utcnow.return_value = datetime(2026, 1, 1)
    token = create_token(mock_user, expires_in=3600)
    
    # Move time forward past expiration
    mock_datetime.utcnow.return_value = datetime(2026, 1, 2)
    
    with pytest.raises(TokenExpiredError):
        verify_token(token)
```

### Example 2: Creating AGENTS.md for a React Project

```bash
codex "create an AGENTS.md file with rules for our React TypeScript project"
```

Generated AGENTS.md:
```markdown
# AGENTS.md

## Project Overview
React TypeScript application with Material-UI components and Redux Toolkit for state management.

## Tech Stack
- React 18.2
- TypeScript 5.0
- Material-UI 5.x
- Redux Toolkit
- React Router 6
- Vite

## Development Rules

### Code Style
- Use functional components with hooks
- Prefer named exports over default exports
- Use TypeScript strict mode
- Follow ESLint and Prettier configurations
- Maximum component file size: 300 lines

### Component Structure
```typescript
// src/components/ExampleComponent.tsx
import React from 'react';
import { Box, Typography } from '@mui/material';

interface ExampleComponentProps {
  title: string;
  onAction: () => void;
}

export const ExampleComponent: React.FC<ExampleComponentProps> = ({
  title,
  onAction
}) => {
  return (
    <Box>
      <Typography variant="h5">{title}</Typography>
    </Box>
  );
};
```

### State Management
- Use Redux Toolkit for global state
- Use local state for component-specific data
- Create slices in `src/store/slices/`
- Use typed hooks from `src/store/hooks.ts`

### Testing Requirements
- Unit tests for utility functions
- Component tests with React Testing Library
- Minimum 70% coverage
- Mock API calls in tests

### File Organization
```
src/
├── components/     # Reusable UI components
├── pages/         # Route-level components
├── store/         # Redux store and slices
├── hooks/         # Custom React hooks
├── utils/         # Utility functions
├── types/         # TypeScript type definitions
└── api/           # API client code
```

## Task Boundaries

### Codex Should
- Create new components following established patterns
- Add unit and component tests
- Update type definitions
- Refactor code while maintaining functionality
- Add inline documentation

### Requires Human Approval
- Changing Redux store structure
- Modifying authentication logic
- Updating dependencies
- Deleting files or components
- API endpoint changes

### Never Do
- Commit API keys or secrets
- Disable TypeScript checks
- Remove error handling
- Deploy to production
```

### Example 3: CI/CD Fix Workflow

```bash
# Diagnose CI failure
codex "analyze GitHub Actions failure in latest commit and fix the failing test"

# Codex will:
# 1. Read .github/workflows/ci.yml
# 2. Check recent commit diff
# 3. Identify failing test from logs
# 4. Fix the root cause
# 5. Update test if needed
# 6. Verify locally before committing
```

## Best Practices

### Task Design
1. **Be specific**: "Add error handling to the login function" is better than "improve code"
2. **Provide context**: Reference specific files, functions, or requirements
3. **Set boundaries**: Specify what should and shouldn't change
4. **Include verification**: Describe how to test the changes

### Security
1. **Never commit secrets**: Use environment variables
2. **Review before approval**: Don't auto-approve without understanding changes
3. **Use sandbox mode**: Restrict file and command access
4. **Audit regularly**: Review what Codex has access to

### Team Adoption
1. **Start small**: Begin with low-risk tasks
2. **Create templates**: Build a library of successful task patterns
3. **Share learnings**: Document what works and what doesn't
4. **Iterate rules**: Update AGENTS.md based on experience
5. **Regular retrospectives**: Discuss Codex usage in team meetings

## Resources

- **Official Documentation**: https://codexguide.ai
- **GitHub Repository**: https://github.com/freestylefly/CodexGuide
- **OpenAI Codex Official**: https://openai.com/codex/
- **CLI Getting Started**: https://help.openai.com/en/articles/11096431-openai-codex-cli-getting-started
- **Codex Cloud Docs**: https://platform.openai.com/docs/codex

## Contributing to CodexGuide

CodexGuide welcomes contributions:

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/CodexGuide.git
cd CodexGuide

# Create feature branch
git checkout -b feature/your-contribution

# Install and test
pnpm install
pnpm dev

# Make changes to docs/ directory
# Follow existing structure and style

# Submit pull request
git add .
git commit -m "docs: add section on X"
git push origin feature/your-contribution
```

Contribution areas:
- Beginner-friendly tutorial improvements
- Real-world case studies
- Common errors and solutions
- Team practices and workflows
- Official documentation updates

See [CONTRIBUTING.md](https://github.com/freestylefly/CodexGuide/blob/main/CONTRIBUTING.md) for detailed guidelines.
