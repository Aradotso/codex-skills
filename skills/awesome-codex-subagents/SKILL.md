---
name: awesome-codex-subagents
description: A curated collection of 136+ specialized Codex subagents for development tasks across 10 categories
triggers:
  - "install codex subagents for my project"
  - "set up specialized AI agents for development"
  - "add backend developer subagent to codex"
  - "how do I use codex subagents"
  - "configure project-specific agents"
  - "what subagents are available for security testing"
  - "install the python-pro subagent"
  - "add react specialist agent to my workspace"
---

# awesome-codex-subagents

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

A definitive collection of 136+ specialized Codex subagents covering development, infrastructure, quality assurance, and domain-specific tasks. Each subagent is a `.toml` configuration file that extends Codex with focused expertise for specific development scenarios.

## What This Project Does

This repository provides pre-configured Codex subagents that you can install to delegate specialized tasks to AI assistants with domain expertise. Instead of asking a general-purpose agent to handle everything, you can explicitly invoke subagents optimized for:

- **Core Development**: API design, frontend/backend development, fullstack work
- **Language Specialists**: Python, TypeScript, Go, Rust, Java, and 20+ more languages
- **Infrastructure**: DevOps, Kubernetes, Terraform, cloud architecture
- **Quality & Security**: Testing, security audits, accessibility, code review
- **Data & Analytics**: Data engineering, ML pipelines, analytics
- **Content & Documentation**: Technical writing, API docs, localization
- **Domain-Specific**: Fintech, healthcare, gaming, embedded systems
- **Emerging Tech**: Blockchain, AI/ML infrastructure, quantum computing
- **Research & Tools**: Web search, academic research, benchmarking

## Installation

### Global Installation (Available in All Projects)

```bash
# Clone the repository
git clone https://github.com/VoltAgent/awesome-codex-subagents.git
cd awesome-codex-subagents

# Create global agents directory
mkdir -p ~/.codex/agents

# Install specific subagents (examples)
cp categories/01-core-development/backend-developer.toml ~/.codex/agents/
cp categories/02-language-specialists/python-pro.toml ~/.codex/agents/
cp categories/03-infrastructure/kubernetes-specialist.toml ~/.codex/agents/
```

### Project-Specific Installation (Higher Precedence)

```bash
# In your project root
mkdir -p .codex/agents

# Install project-specific agents
cp path/to/awesome-codex-subagents/categories/04-quality-security/reviewer.toml .codex/agents/
cp path/to/awesome-codex-subagents/categories/02-language-specialists/typescript-pro.toml .codex/agents/
```

### Install All Subagents in a Category

```bash
# Install all language specialists globally
mkdir -p ~/.codex/agents
cp categories/02-language-specialists/*.toml ~/.codex/agents/

# Install all infrastructure agents for current project
mkdir -p .codex/agents
cp categories/03-infrastructure/*.toml .codex/agents/
```

## Subagent Structure

Each subagent is a `.toml` file with this structure:

```toml
name = "python-pro"
description = "Python ecosystem master for development, testing, and packaging"
model = "gpt-5.3-codex-spark"
model_reasoning_effort = "medium"
sandbox_mode = "workspace-write"

[instructions]
text = """
You are a Python development expert specializing in modern Python 3.10+...

Core Responsibilities:
- Write idiomatic, type-hinted Python code
- Use virtual environments and modern packaging tools
- Implement comprehensive testing with pytest
...
"""
```

### Key Configuration Fields

- **name**: Unique identifier for the subagent
- **description**: When to invoke this subagent (used by Codex for routing)
- **model**: Which GPT model to use (`gpt-5.4` for deep reasoning, `gpt-5.3-codex-spark` for fast tasks)
- **sandbox_mode**: Filesystem access (`read-only`, `workspace-write`, or `full`)
- **instructions.text**: The system prompt defining the subagent's expertise and behavior

## Using Subagents

### Explicit Delegation in Prompts

Codex does **not** auto-spawn custom subagents. You must explicitly delegate:

```bash
# Invoke the backend developer subagent
"@backend-developer create a REST API for user management with FastAPI"

# Use the security auditor to review code
"@security-auditor review the authentication module for vulnerabilities"

# Get the Python specialist to refactor code
"@python-pro refactor this script to use type hints and dataclasses"
```

### Multiple Subagents in Sequence

```bash
# Design API first, then implement
"@api-designer design a RESTful API for a blog system"
# After reviewing the design:
"@backend-developer implement the blog API using the design from api-designer"
```

### Project-Specific Overrides

If both global and project-specific agents exist with the same name, the project-specific one takes precedence:

```bash
# Global agent at ~/.codex/agents/reviewer.toml
# Project agent at .codex/agents/reviewer.toml
# The project version will be used when you invoke @reviewer
```

## Common Patterns

### Backend Development Workflow

```bash
# 1. Design the API
mkdir -p .codex/agents
cp categories/01-core-development/api-designer.toml .codex/agents/

# 2. Install language-specific agent
cp categories/02-language-specialists/python-pro.toml .codex/agents/

# 3. Add security review
cp categories/04-quality-security/security-auditor.toml .codex/agents/

# Usage:
"@api-designer design a REST API for inventory management"
"@python-pro implement the inventory API with FastAPI and SQLAlchemy"
"@security-auditor review the authentication and authorization logic"
```

### Infrastructure Setup

```bash
# Install infrastructure agents
mkdir -p ~/.codex/agents
cp categories/03-infrastructure/terraform-engineer.toml ~/.codex/agents/
cp categories/03-infrastructure/kubernetes-specialist.toml ~/.codex/agents/
cp categories/03-infrastructure/cloud-architect.toml ~/.codex/agents/

# Usage:
"@cloud-architect design AWS infrastructure for a multi-region web app"
"@terraform-engineer write Terraform modules for the AWS design"
"@kubernetes-specialist create Kubernetes manifests for the application"
```

### Full-Stack Feature Development

```bash
# Install full-stack agents
cp categories/02-language-specialists/react-specialist.toml .codex/agents/
cp categories/02-language-specialists/nodejs-expert.toml .codex/agents/
cp categories/04-quality-security/e2e-tester.toml .codex/agents/

# Usage:
"@react-specialist build a product listing page with filtering and pagination"
"@nodejs-expert create Express API endpoints for product data"
"@e2e-tester write Playwright tests for the product listing flow"
```

### Code Quality Pipeline

```bash
# Install quality agents
cp categories/04-quality-security/reviewer.toml .codex/agents/
cp categories/04-quality-security/test-engineer.toml .codex/agents/
cp categories/04-quality-security/accessibility-tester.toml .codex/agents/

# Usage:
"@reviewer analyze the new payment module for design issues"
"@test-engineer add unit and integration tests for the payment module"
"@accessibility-tester audit the checkout page for WCAG 2.1 AA compliance"
```

## Configuration

### Custom Subagent Configuration

Create `.codex/config.toml` in your project:

```toml
[agents]
# Override default models for specific agents
python-pro.model = "gpt-5.4"  # Use more powerful model
reviewer.sandbox_mode = "read-only"  # Restrict to read-only

# Set default reasoning effort
*.model_reasoning_effort = "high"
```

### Creating Custom Subagents

Create a new `.toml` file in `.codex/agents/`:

```toml
name = "my-custom-agent"
description = "Specialized agent for my team's specific needs"
model = "gpt-5.3-codex-spark"
sandbox_mode = "workspace-write"

[instructions]
text = """
You are a custom development agent for [YOUR TEAM/PROJECT].

Your primary responsibilities:
1. Follow our team's coding standards (link to internal docs)
2. Use our specific tech stack: [list technologies]
3. Implement features according to our architecture patterns

Code Style:
- Use [specific linter/formatter]
- Follow [naming conventions]
- Include [specific testing patterns]

Always:
- Check our internal documentation at [URL]
- Reference our API patterns in [repo location]
- Use our shared component library [package name]
"""
```

## Category Overview

### Core Development (12 agents)
- `api-designer` - REST and GraphQL API design
- `backend-developer` - Server-side development
- `frontend-developer` - UI/UX implementation
- `fullstack-developer` - End-to-end features
- `mobile-developer` - Cross-platform mobile apps

### Language Specialists (28 agents)
- `python-pro` - Python ecosystem expert
- `typescript-pro` - TypeScript development
- `rust-engineer` - Systems programming
- `golang-pro` - Go concurrency and services
- `react-specialist` - React 18+ patterns
- `nextjs-developer` - Next.js 14+ full-stack
- `vue-expert` - Vue 3 Composition API
- `angular-architect` - Angular 15+ enterprise

### Infrastructure (16 agents)
- `devops-engineer` - CI/CD pipelines
- `kubernetes-specialist` - K8s orchestration
- `terraform-engineer` - Infrastructure as Code
- `cloud-architect` - AWS/GCP/Azure design
- `sre-engineer` - Site reliability
- `docker-expert` - Container optimization

### Quality & Security (16 agents)
- `security-auditor` - Vulnerability assessment
- `test-engineer` - Testing strategy
- `reviewer` - Code review specialist
- `accessibility-tester` - WCAG compliance
- `performance-optimizer` - Performance tuning

## Troubleshooting

### Subagent Not Found

```bash
# Check if subagent is installed
ls -la ~/.codex/agents/
ls -la .codex/agents/

# Verify the name matches the file
cat .codex/agents/python-pro.toml | grep "^name"

# Restart Codex session
# (Implementation-specific, usually closing and reopening)
```

### Wrong Subagent Responding

```bash
# Check for name conflicts
find ~/.codex/agents .codex/agents -name "*.toml" -exec grep "^name" {} \; -print

# Project-specific agents override global ones
# Remove the duplicate or rename one:
mv .codex/agents/python-pro.toml .codex/agents/python-pro-custom.toml
```

### Subagent Not Following Instructions

```bash
# Review the instruction text
cat .codex/agents/your-agent.toml

# Ensure description clearly states when to invoke
# Update the instructions section to be more specific:
nano .codex/agents/your-agent.toml

# Be explicit in your delegation:
"@your-agent [very specific task description]"
```

### Performance Issues

```bash
# Check model configuration
cat .codex/agents/slow-agent.toml | grep "^model"

# Switch to faster model for simple tasks:
# Change model = "gpt-5.4" to model = "gpt-5.3-codex-spark"

# Reduce reasoning effort in config:
[agents]
slow-agent.model_reasoning_effort = "low"
```

### Sandbox Restrictions

```bash
# If agent can't modify files:
# Check sandbox_mode in the .toml file
cat .codex/agents/your-agent.toml | grep "sandbox_mode"

# Update to allow writes:
sandbox_mode = "workspace-write"

# Or for full system access (use cautiously):
sandbox_mode = "full"
```

## Real-World Examples

### Example 1: Building a REST API with Python

```bash
# Install agents
cp categories/02-language-specialists/python-pro.toml .codex/agents/
cp categories/01-core-development/api-designer.toml .codex/agents/

# Step 1: Design
"@api-designer design a REST API for a task management system with users, projects, and tasks"

# Step 2: Implement
"@python-pro implement the task management API using FastAPI with:
- JWT authentication
- SQLAlchemy models
- Pydantic schemas
- CRUD endpoints for users, projects, and tasks
- PostgreSQL database"

# Step 3: Test
"@python-pro add pytest tests for all endpoints with fixtures and mocks"
```

### Example 2: Infrastructure with Terraform

```bash
# Install agents
cp categories/03-infrastructure/terraform-engineer.toml .codex/agents/
cp categories/03-infrastructure/cloud-architect.toml .codex/agents/

# Design infrastructure
"@cloud-architect design AWS infrastructure for a containerized web application with:
- ECS Fargate for compute
- RDS PostgreSQL for database
- ElastiCache Redis for sessions
- ALB for load balancing
- S3 for static assets
- CloudFront for CDN"

# Implement with Terraform
"@terraform-engineer create Terraform modules for the AWS infrastructure design:
- Use remote state in S3
- Separate modules for VPC, ECS, RDS, Redis, ALB
- Variables for environment-specific config
- Outputs for endpoints and connection strings"
```

### Example 3: Frontend Development with React

```bash
# Install agents
cp categories/02-language-specialists/react-specialist.toml .codex/agents/
cp categories/02-language-specialists/typescript-pro.toml .codex/agents/

# Build UI component
"@react-specialist create a DataTable component with:
- TypeScript types
- Column sorting
- Pagination
- Row selection
- Filtering
- Virtualized scrolling for large datasets
- Tailwind CSS styling"

# Add tests
"@react-specialist write React Testing Library tests for DataTable covering:
- Rendering with mock data
- Sorting functionality
- Pagination controls
- Filter interactions"
```

### Example 4: Security Review Pipeline

```bash
# Install security agents
cp categories/04-quality-security/security-auditor.toml .codex/agents/
cp categories/04-quality-security/dependency-auditor.toml .codex/agents/

# Audit authentication code
"@security-auditor review the authentication system in src/auth/ for:
- SQL injection vulnerabilities
- XSS risks
- CSRF protection
- Session management
- Password hashing
- Rate limiting"

# Check dependencies
"@dependency-auditor scan package.json and identify:
- Known CVEs in dependencies
- Outdated packages with security patches
- License compliance issues
- Recommended updates"
```

## Environment Variables

Subagents should reference environment variables for sensitive data:

```python
# ✅ Correct - use environment variables
import os
DATABASE_URL = os.getenv("DATABASE_URL")
API_KEY = os.getenv("API_KEY")

# ❌ Incorrect - never hardcode secrets
DATABASE_URL = "postgresql://user:pass@localhost/db"
API_KEY = "sk-1234567890abcdef"
```

When instructing subagents:

```bash
"@python-pro create a database connection using the DATABASE_URL environment variable from .env"

"@nodejs-expert set up AWS SDK to use credentials from AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables"
```

## Additional Resources

- [Official Codex Documentation](https://developers.openai.com/codex/subagents)
- [GitHub Repository](https://github.com/VoltAgent/awesome-codex-subagents)
- [Discord Community](https://s.voltagent.dev/discord)
- [Related Collections](https://github.com/VoltAgent) - Agent skills, Claude subagents, OpenClaw skills

## Contributing

To add custom subagents to your local collection:

1. Create a new `.toml` file following the structure above
2. Place it in `.codex/agents/` (project) or `~/.codex/agents/` (global)
3. Reference the official documentation for advanced configuration options

To contribute to the upstream repository, submit a pull request with your subagent in the appropriate category folder.
