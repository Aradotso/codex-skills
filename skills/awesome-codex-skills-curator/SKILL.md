---
name: awesome-codex-skills-curator
description: Curate, install, and manage Codex skills from the awesome-codex-skills collection for AI coding agents.
triggers:
  - "install a Codex skill from the awesome list"
  - "browse available Codex skills"
  - "add a skill to my Codex setup"
  - "what skills are available for Codex"
  - "install the meeting notes skill"
  - "show me Codex skills for productivity"
  - "set up a new Codex skill from awesome-codex-skills"
  - "manage my Codex skills collection"
---

# Awesome Codex Skills Curator

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

This skill helps you browse, install, and manage skills from the [awesome-codex-skills](https://github.com/ComposioHQ/awesome-codex-skills) collection — a curated library of practical Codex skills for automating workflows across 1000+ apps.

## What is Awesome Codex Skills?

Awesome Codex Skills is a community-driven collection of modular instruction bundles (skills) that extend Codex's capabilities. Each skill is a folder containing a `SKILL.md` with:
- **Metadata** (name, description, triggers) — helps Codex decide when to fire the skill
- **Step-by-step instructions** — guides Codex through task execution
- **Code examples and patterns** — real implementations in the project's language

Skills cover development tools, productivity, communication, data analysis, and meta utilities.

## Installation

### Quick Start: Install the Skill Installer

```bash
# Clone the repository
git clone https://github.com/ComposioHQ/awesome-codex-skills.git
cd awesome-codex-skills

# The skill installer is at skill-installer/scripts/install-skill-from-github.py
# It installs skills to $CODEX_HOME/skills (defaults to ~/.codex/skills)
```

### Install a Specific Skill

```bash
# Install a skill from the main repository
python skill-installer/scripts/install-skill-from-github.py \
  --repo ComposioHQ/awesome-codex-skills \
  --path meeting-notes-and-actions

# Install a skill from an external repository
python skill-installer/scripts/install-skill-from-github.py \
  --repo yujiachen-y/codebase-recon-skill \
  --path skills/codebase-recon \
  --name codebase-recon

# Install from a different branch
python skill-installer/scripts/install-skill-from-github.py \
  --repo ComposioHQ/awesome-codex-skills \
  --path codebase-migrate \
  --branch dev
```

### Manual Installation

```bash
# Copy a skill folder directly to your Codex skills directory
cp -r ./spreadsheet-formula-helper ~/.codex/skills/

# Restart Codex to load the new skill
# The skill will be available based on its triggers
```

## Key Commands

### Skill Installer Script

```bash
python skill-installer/scripts/install-skill-from-github.py [OPTIONS]
```

**Options:**
- `--repo OWNER/NAME` — GitHub repository (required)
- `--path PATH` — Path to skill folder in repo (required)
- `--name NAME` — Custom skill name (optional, defaults to folder name)
- `--branch BRANCH` — Git branch (optional, defaults to main)
- `--skills-dir DIR` — Custom skills directory (optional, defaults to $CODEX_HOME/skills)

### Environment Variables

```bash
# Set custom Codex home directory
export CODEX_HOME=~/my-codex-config

# Skills will be installed to $CODEX_HOME/skills
```

## Browsing Available Skills

### By Category

**Development & Code Tools:**
- `brooks-lint` — AI code reviews with book citations
- `codebase-migrate` — Large codebase migrations in batches
- `codebase-recon` — Git history analysis for hotspots
- `gh-fix-ci` — Fix failing GitHub Actions
- `sentry-triage` — Diagnose Sentry issues locally

**Productivity & Collaboration:**
- `meeting-notes-and-actions` — Turn transcripts into action items
- `notion-knowledge-capture` — Chat to structured Notion pages
- `issue-triage` — Triage Linear/Jira backlogs
- `support-ticket-triage` — Categorize and draft responses

**Communication & Writing:**
- `email-draft-polish` — Draft and refine emails
- `content-research-writer` — Research and draft with citations
- `changelog-generator` — Create changelogs from commits

**Data & Analysis:**
- `spreadsheet-formula-helper` — Write complex formulas
- `datadog-logs` — Query Datadog from CLI
- `lead-research-assistant` — Enrich lead records

## Real Usage Examples

### Example 1: Install Meeting Notes Skill

```python
import subprocess
import os

def install_meeting_notes_skill():
    """Install the meeting-notes-and-actions skill."""
    repo = "ComposioHQ/awesome-codex-skills"
    path = "meeting-notes-and-actions"
    
    cmd = [
        "python",
        "skill-installer/scripts/install-skill-from-github.py",
        "--repo", repo,
        "--path", path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✓ Skill installed to {os.environ.get('CODEX_HOME', '~/.codex')}/skills/{path}")
        print("Restart Codex to load the skill.")
    else:
        print(f"✗ Installation failed: {result.stderr}")
    
    return result.returncode == 0

# Usage
install_meeting_notes_skill()
```

### Example 2: Batch Install Multiple Skills

```python
import subprocess
from typing import List, Tuple

def batch_install_skills(skills: List[Tuple[str, str]]):
    """
    Install multiple skills from the awesome-codex-skills collection.
    
    Args:
        skills: List of (repo, path) tuples
    """
    results = []
    
    for repo, path in skills:
        print(f"Installing {path} from {repo}...")
        
        cmd = [
            "python",
            "skill-installer/scripts/install-skill-from-github.py",
            "--repo", repo,
            "--path", path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        success = result.returncode == 0
        
        results.append({
            "skill": path,
            "success": success,
            "output": result.stdout if success else result.stderr
        })
        
        status = "✓" if success else "✗"
        print(f"{status} {path}")
    
    return results

# Install a productivity suite
productivity_skills = [
    ("ComposioHQ/awesome-codex-skills", "meeting-notes-and-actions"),
    ("ComposioHQ/awesome-codex-skills", "issue-triage"),
    ("ComposioHQ/awesome-codex-skills", "email-draft-polish"),
]

results = batch_install_skills(productivity_skills)
print(f"\nInstalled {sum(r['success'] for r in results)}/{len(results)} skills")
```

### Example 3: Install External Repository Skill

```bash
# Install brooks-lint from external repo
python skill-installer/scripts/install-skill-from-github.py \
  --repo hyhmrright/brooks-lint \
  --path skills/brooks-lint \
  --name brooks-lint

# Install codebase-recon
python skill-installer/scripts/install-skill-from-github.py \
  --repo yujiachen-y/codebase-recon-skill \
  --path skills/codebase-recon \
  --name codebase-recon

# Install unslop (removes AI writing patterns)
python skill-installer/scripts/install-skill-from-github.py \
  --repo MohamedAbdallah-14/unslop \
  --path skills/unslop \
  --name unslop
```

### Example 4: Check Installed Skills

```python
import os
from pathlib import Path

def list_installed_skills():
    """List all installed Codex skills with their metadata."""
    codex_home = os.environ.get("CODEX_HOME", os.path.expanduser("~/.codex"))
    skills_dir = Path(codex_home) / "skills"
    
    if not skills_dir.exists():
        print(f"Skills directory not found: {skills_dir}")
        return []
    
    skills = []
    for skill_path in skills_dir.iterdir():
        if not skill_path.is_dir() or skill_path.name.startswith("."):
            continue
        
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            continue
        
        # Parse frontmatter for name and description
        with open(skill_md, "r") as f:
            content = f.read()
            if content.startswith("---"):
                frontmatter = content.split("---")[1]
                name = None
                description = None
                
                for line in frontmatter.split("\n"):
                    if line.startswith("name:"):
                        name = line.split(":", 1)[1].strip()
                    elif line.startswith("description:"):
                        description = line.split(":", 1)[1].strip()
                
                skills.append({
                    "path": skill_path.name,
                    "name": name,
                    "description": description
                })
    
    return skills

# Usage
skills = list_installed_skills()
for skill in skills:
    print(f"• {skill['name']}: {skill['description']}")
```

## Common Patterns

### Pattern 1: Category-Based Installation

```python
def install_category(category: str):
    """Install all skills from a specific category."""
    
    categories = {
        "dev-tools": [
            "codebase-migrate",
            "gh-fix-ci",
            "sentry-triage",
            "webapp-testing"
        ],
        "productivity": [
            "meeting-notes-and-actions",
            "issue-triage",
            "notion-knowledge-capture",
            "support-ticket-triage"
        ],
        "writing": [
            "email-draft-polish",
            "changelog-generator",
            "content-research-writer"
        ]
    }
    
    if category not in categories:
        print(f"Unknown category: {category}")
        return
    
    skills = [(f"ComposioHQ/awesome-codex-skills", path) 
              for path in categories[category]]
    
    return batch_install_skills(skills)

# Install all productivity skills
install_category("productivity")
```

### Pattern 2: Skill with Composio Integration

```bash
# Install connect skill for app integrations
python skill-installer/scripts/install-skill-from-github.py \
  --repo ComposioHQ/awesome-codex-skills \
  --path connect

# Connect to apps (requires Composio CLI)
composio login
composio add slack
composio add github
composio add notion

# Now use skills that leverage these connections
# e.g., "send a Slack message summarizing the PR review"
```

### Pattern 3: Custom Skills Directory

```bash
# Use a custom skills directory
export CODEX_HOME=/opt/codex-config

python skill-installer/scripts/install-skill-from-github.py \
  --repo ComposioHQ/awesome-codex-skills \
  --path meeting-notes-and-actions \
  --skills-dir /opt/codex-config/skills

# Or specify directly in command
python skill-installer/scripts/install-skill-from-github.py \
  --repo ComposioHQ/awesome-codex-skills \
  --path issue-triage \
  --skills-dir ~/my-project/.codex/skills
```

## Skill Structure

Each skill follows this structure:

```
skill-name/
├── SKILL.md          # Main skill definition
├── examples/         # Optional: example files
├── templates/        # Optional: templates
└── README.md         # Optional: additional docs
```

**SKILL.md Format:**
```markdown
---
name: skill-name
description: One-line description of what the skill does
triggers:
  - "phrase users might say"
  - "another natural trigger"
  - "install X"
---

# Skill Name

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

[Detailed instructions, examples, patterns]
```

## Troubleshooting

### Skill Not Loading

```bash
# Check if skill is in the right location
ls -la ~/.codex/skills/

# Verify SKILL.md exists and has frontmatter
cat ~/.codex/skills/meeting-notes-and-actions/SKILL.md | head -n 10

# Restart Codex completely
# (Method varies by Codex implementation)
```

### Installation Fails

```python
# Check Python and git are available
import subprocess

def check_dependencies():
    """Verify installation dependencies."""
    checks = {
        "python": ["python", "--version"],
        "git": ["git", "--version"]
    }
    
    for name, cmd in checks.items():
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✓ {name}: {result.stdout.strip()}")
            else:
                print(f"✗ {name}: not working")
        except FileNotFoundError:
            print(f"✗ {name}: not found")

check_dependencies()
```

### Skill Conflicts

```bash
# List all skills and check for duplicate names
find ~/.codex/skills -name "SKILL.md" -exec grep -H "^name:" {} \;

# Remove conflicting skill
rm -rf ~/.codex/skills/duplicate-skill-name

# Reinstall with custom name
python skill-installer/scripts/install-skill-from-github.py \
  --repo ComposioHQ/awesome-codex-skills \
  --path meeting-notes-and-actions \
  --name meeting-notes-v2
```

### Network Issues

```bash
# Install from a local clone
git clone https://github.com/ComposioHQ/awesome-codex-skills.git /tmp/skills
cp -r /tmp/skills/meeting-notes-and-actions ~/.codex/skills/

# Or use a specific branch for stability
python skill-installer/scripts/install-skill-from-github.py \
  --repo ComposioHQ/awesome-codex-skills \
  --path meeting-notes-and-actions \
  --branch stable
```

## Creating Your Own Skills

To contribute a skill to the collection:

1. **Fork the repository**
2. **Create a new skill folder** with a descriptive name
3. **Write SKILL.md** with YAML frontmatter and instructions
4. **Test locally** by copying to `~/.codex/skills/`
5. **Submit a PR** to ComposioHQ/awesome-codex-skills

**Minimal SKILL.md template:**

```markdown
---
name: my-awesome-skill
description: Does something specific and useful
triggers:
  - "do the thing"
  - "help me with X"
---

# My Awesome Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

[Your skill documentation here]
```

## Best Practices

1. **Start small** — Install 2-3 skills for your immediate needs
2. **Test triggers** — Say the trigger phrases to verify skill activation
3. **Combine skills** — Use multiple skills in one workflow (e.g., gh-fix-ci + pr-review-ci-fix)
4. **Keep updated** — Pull the latest awesome-codex-skills regularly
5. **Share learnings** — Contribute improvements back to the collection

## Resources

- **Repository**: https://github.com/ComposioHQ/awesome-codex-skills
- **Composio CLI**: For app integrations (Slack, GitHub, Notion, etc.)
- **Discord**: https://discord.com/invite/composio
- **Documentation**: See individual skill README files

## Integration with Other Tools

### Bernstein Multi-Agent Orchestrator

```bash
# awesome-codex-skills works with Bernstein for parallel agents
git clone https://github.com/chernistry/bernstein
cd bernstein

# Skills are available to all agents in isolated worktrees
```

### Cursor, Claude Code, VS Code

```bash
# Skills work across AI coding agents
# Install to shared location or symlink
ln -s ~/.codex/skills ~/cursor/skills
ln -s ~/.codex/skills ~/claude/skills
```
