---
name: codex-redteam-mode
description: Opt-in red team mode for AI coding assistants that enables security-focused thinking for penetration testing and red team operations
triggers:
  - enable red team mode for security testing
  - how do I activate codex red team mode
  - switch to red team thinking mode
  - configure AI for penetration testing workflow
  - install red team mode for codex
  - use red team mode for security analysis
  - disable red team mode and return to normal
  - validate red team mode installation
---

# Codex Red Team Mode

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

Codex Red Team Mode is a lightweight, opt-in configuration layer that enables AI coding assistants to think like red team operators during authorized security assessments. Unlike persistent jailbreaks that pollute normal operations, this project provides:

- **Opt-in activation**: Normal mode by default, red team mode only when explicitly enabled
- **Structured routing**: `phase -> router -> pack -> leaf` workflow for security operations
- **Session isolation**: State management via JSON runtime files
- **Lightweight hooks**: Minimal context bloat with targeted prompt overlays

The project supports multiple security phases including web exploitation, Active Directory, post-exploitation, reverse engineering, code auditing, payload development, and evasion techniques.

## Installation

The installer uses managed incremental installation that preserves your existing configuration while injecting only the necessary red team components.

### Python (Cross-platform)

```bash
# Clone the repository
git clone https://github.com/chAng-L19/codex-redteam-mode.git
cd codex-redteam-mode

# Run installer
python scripts/install.py
```

### Windows (PowerShell)

```powershell
# Navigate to project directory
cd codex-redteam-mode

# Run installer with execution policy bypass
powershell -ExecutionPolicy Bypass -File .\scripts\install.ps1
```

### macOS / Linux

```bash
# Ensure Python 3 is available
python3 scripts/install.py
```

The installer will:
- Preserve your original `AGENTS.md` and `hooks.json`
- Inject managed blocks from the repository
- Remove old version runtime remnants
- Write installation manifest
- Automatically run validation

## Validation

After installation, verify the setup:

```bash
# Run validation script
python scripts/validate.py

# Or run full test suite
python -m unittest discover -s tests -p "test_*.py"
```

## Core Commands

### Enable Red Team Mode

```text
# Full command
/redteam on

# Light mode (targeted security analysis)
/redteam light

# Full mode (complete red team workflow)
/redteam full

# Natural language
enable red team mode
Enter Red Team Mode
```

### Disable Red Team Mode

```text
# Command
/redteam off

# Natural language
disable red team mode
Exit Red Team Mode
```

### Check Current Mode

```text
# Query current state
what mode am I in?
show red team status
```

## Modes

| Mode | Default | Use Case |
|------|---------|----------|
| `normal` | ✓ | Regular coding, documentation, general research |
| `redteam-light` | | Targeted security analysis, planning, threat modeling |
| `redteam-full` | | Deep red team workflow with full routing |

## Workflow Structure

The routing mainline follows:

```text
phase -> router -> pack -> leaf
```

### Core Phases

- **web**: Web application testing (XSS, SQLi, CSRF, etc.)
- **ad**: Active Directory exploitation
- **postex**: Post-exploitation activities
- **reverse**: Reverse engineering
- **code-audit**: Source code security analysis
- **payload**: Payload generation and customization
- **evasion**: AV/EDR evasion techniques

### Extended Routers/Packs

- **recon**: Reconnaissance and enumeration
- **api**: API security testing
- **auth**: Authentication/authorization bypass
- **injection**: Various injection attacks
- **file**: File upload/download vulnerabilities
- **cloud**: Cloud infrastructure security
- **container**: Docker/Kubernetes security
- **network**: Network protocol analysis
- **crypto**: Cryptographic vulnerabilities
- **mobile**: Mobile application security

## Usage Patterns

### Web Security Testing

```python
# In red team mode, analyze a web application
"""
/redteam full

I need to assess a web application at https://target.example.com (authorized)
Focus on:
- Authentication mechanisms
- Session management
- Input validation
- API endpoints
"""

# The AI will route through: web -> api -> injection -> leaf
# Providing structured analysis with appropriate techniques
```

### Active Directory Assessment

```python
# Enable red team mode for AD testing
"""
/redteam full

Analyzing Active Directory environment (authorized pentest)
- Domain: corp.example.local
- Current access: low-privilege domain user
- Goal: privilege escalation paths
"""

# Routes through: ad -> enum -> privesc -> pack
```

### Code Security Audit

```python
# Light mode for code review
"""
/redteam light

Review this authentication function for security issues:
```

```python
def authenticate(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = db.execute(query)
    return result.fetchone()
```

"""
```

### Payload Development

```python
# Full mode for payload creation
"""
/redteam full

Need to create a Python reverse shell payload that:
- Connects to ${C2_SERVER}:${C2_PORT} (env vars)
- Evades basic AV signature detection
- Works on Windows 10+
- Maintains persistence
"""

# Routes through: payload -> evasion -> windows -> leaf
```

## Configuration

### Runtime State Files

The mode state is stored in JSON format, typically in:

```
.codex/runtime/redteam_state.json
```

Example state file:

```json
{
  "mode": "redteam-full",
  "phase": "web",
  "router": "injection",
  "pack": "sqli",
  "session_id": "uuid-here",
  "timestamp": "2026-05-19T12:34:56Z"
}
```

### Hooks Configuration

The `hooks.json` file manages prompt overlays:

```json
{
  "redteam": {
    "enabled": false,
    "mode": "normal",
    "phases": ["web", "ad", "postex", "reverse", "code-audit", "payload", "evasion"],
    "routing": "phase-router-pack-leaf"
  }
}
```

### Custom Phase Extension

To add custom phases, edit the routing configuration:

```python
# Example: Adding a custom "wireless" phase
# Edit runtime/routing.json

{
  "phases": {
    "wireless": {
      "routers": ["wifi", "bluetooth", "rfid"],
      "packs": {
        "wifi": ["wpa", "wep", "wps", "evil-twin"],
        "bluetooth": ["ble", "classic", "pairing"]
      }
    }
  }
}
```

## Troubleshooting

### Installation Issues

```bash
# Check if files were properly injected
ls -la .codex/AGENTS.md
cat .codex/hooks.json | grep redteam

# Re-run installer with verbose output
python scripts/install.py --verbose

# Clean install (removes all managed blocks first)
python scripts/install.py --clean
```

### Mode Not Activating

```python
# Verify runtime state
cat .codex/runtime/redteam_state.json

# Check hooks are loaded
python -c "import json; print(json.load(open('.codex/hooks.json'))['redteam'])"

# Force mode switch
/redteam off
/redteam full
```

### Validation Failures

```bash
# Run specific test
python -m unittest tests.test_routing

# Check installer integrity
python scripts/validate.py --check-install

# Verify phase detection
python scripts/validate.py --test-phases
```

### Context Pollution

If normal mode feels influenced by red team prompts:

```text
# Ensure clean mode switch
/redteam off

# Verify state
python -c "import json; print(json.load(open('.codex/runtime/redteam_state.json'))['mode'])"

# Should output: "normal"
```

## Security & Legal Considerations

⚠️ **Authorization Required**: Only use red team mode on systems where you have explicit written authorization.

```python
# Always document scope
"""
AUTHORIZATION:
- Client: Example Corp
- Scope: https://test.example.com
- Date: 2026-05-20 to 2026-05-27
- Contact: security@example.com
"""
```

**Never**:
- Use on production systems without authorization
- Use on third-party systems
- Share credentials or access outside scope
- Ignore legal boundaries

## Integration Examples

### With MCP Tools

```python
# Using with Model Context Protocol tools
"""
/redteam full

Using ${MCP_TOOL_NMAP} scan:
- Target: ${TARGET_NETWORK}
- Ports: 1-65535
- Service detection enabled
- Output: XML format
"""
```

### With CI/CD Security Scanning

```python
# Light mode for automated security review
"""
/redteam light

Analyze this PR for security issues:
- Changes in auth/* files
- New API endpoints
- Database query modifications
"""
```

## Best Practices

1. **Always start in normal mode**: Only activate red team mode when needed
2. **Use light mode for analysis**: Reserve full mode for active testing
3. **Document your scope**: Keep authorization details in session context
4. **Clean state between engagements**: Use `/redteam off` when switching contexts
5. **Validate after updates**: Run tests after any configuration changes
6. **Use environment variables**: Never hardcode credentials or targets

## Contributing

See `CONTRIBUTING.md` in the repository for guidelines on:
- Adding new phases
- Extending router logic
- Creating custom packs
- Submitting bug reports

## License

MIT License - See `LICENSE` file for details.
