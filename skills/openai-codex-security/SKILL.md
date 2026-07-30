---
name: openai-codex-security
description: Find, validate, and fix security vulnerabilities using OpenAI's Codex Security CLI and TypeScript SDK
triggers:
  - scan my code for security vulnerabilities
  - use codex security to find issues
  - run a security scan with openai
  - analyze code for security problems
  - fix security vulnerabilities with ai
  - setup codex security scanning
  - integrate openai security tools
  - validate security issues in my codebase
---

# OpenAI Codex Security

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

OpenAI's Codex Security is a CLI and TypeScript SDK that uses AI to find, validate, and fix security vulnerabilities in your codebase. It supports multiple programming languages and integrates into development workflows and CI/CD pipelines.

## Installation

**Requirements:**
- Node.js 22.13.0+ (22.x), 24.x, or 26.x
- Python 3.10 or later
- Access to Codex Security (requires OpenAI account)

```bash
npm install @openai/codex-security
```

For global CLI usage:

```bash
npm install -g @openai/codex-security
```

## Authentication

### Interactive Login (Local Development)

```bash
npx @openai/codex-security login
```

This stores credentials in Codex's credential backend, including system keyring support for managed devices.

### API Key Authentication (CI/CD)

Set one of these environment variables:

```bash
export OPENAI_API_KEY=your-api-key-here
# or
export CODEX_API_KEY=your-api-key-here
```

Environment API keys take precedence and are never stored persistently.

### Choosing Authentication Method

```bash
# Use ChatGPT login
npx @openai/codex-security scan . --auth chatgpt

# Use API key
npx @openai/codex-security scan . --auth api-key
```

To make ChatGPT login the default, unset API keys:

```bash
unset OPENAI_API_KEY CODEX_API_KEY
```

## CLI Commands

### Basic Scan

Scan current directory:

```bash
npx @openai/codex-security scan .
```

Scan specific directory:

```bash
npx @openai/codex-security scan /path/to/project
```

### Advanced Scanning

Use specific model and effort level:

```bash
npx @openai/codex-security scan . --model gpt-5.6-terra --effort high
```

Scan with custom output:

```bash
npx @openai/codex-security scan . --output-format json
npx @openai/codex-security scan . --output-file security-report.json
```

### Login Management

```bash
# Login to Codex Security
npx @openai/codex-security login

# Logout
npx @openai/codex-security logout

# Check authentication status
npx @openai/codex-security whoami
```

## TypeScript SDK

### Basic Usage

```typescript
import { CodexSecurity } from "@openai/codex-security";

async function scanProject() {
  const security = new CodexSecurity();
  
  try {
    const result = await security.run(".");
    console.log("Scan complete!");
    console.log("Report path:", result.reportPath);
    console.log("Vulnerabilities found:", result.vulnerabilities.length);
  } finally {
    await security.close();
  }
}

scanProject();
```

### Custom Configuration

```typescript
import { CodexSecurity } from "@openai/codex-security";

const security = new CodexSecurity({
  model: "gpt-5.6-terra",
  effort: "high",
  apiKey: process.env.OPENAI_API_KEY,
});

const result = await security.run("/path/to/project", {
  exclude: ["node_modules", "dist", "*.test.ts"],
  include: ["src/**/*.ts", "lib/**/*.js"],
});

console.log(`Found ${result.vulnerabilities.length} vulnerabilities`);

for (const vuln of result.vulnerabilities) {
  console.log(`- ${vuln.severity}: ${vuln.title}`);
  console.log(`  File: ${vuln.file}:${vuln.line}`);
  console.log(`  Description: ${vuln.description}`);
}

await security.close();
```

### Processing Scan Results

```typescript
import { CodexSecurity } from "@openai/codex-security";

async function analyzeSecurity() {
  const security = new CodexSecurity();
  const result = await security.run(".");

  // Filter by severity
  const critical = result.vulnerabilities.filter(
    v => v.severity === "critical"
  );
  const high = result.vulnerabilities.filter(
    v => v.severity === "high"
  );

  console.log(`Critical issues: ${critical.length}`);
  console.log(`High severity issues: ${high.length}`);

  // Group by file
  const byFile = result.vulnerabilities.reduce((acc, vuln) => {
    acc[vuln.file] = acc[vuln.file] || [];
    acc[vuln.file].push(vuln);
    return acc;
  }, {} as Record<string, typeof result.vulnerabilities>);

  console.log("\nVulnerabilities by file:");
  for (const [file, vulns] of Object.entries(byFile)) {
    console.log(`${file}: ${vulns.length} issues`);
  }

  await security.close();
}

analyzeSecurity();
```

### Validating Specific Vulnerabilities

```typescript
import { CodexSecurity } from "@openai/codex-security";

async function validateVulnerability(vulnId: string) {
  const security = new CodexSecurity();
  
  const result = await security.run(".");
  const vuln = result.vulnerabilities.find(v => v.id === vulnId);
  
  if (!vuln) {
    console.log("Vulnerability not found");
    await security.close();
    return;
  }

  console.log("Vulnerability Details:");
  console.log(`ID: ${vuln.id}`);
  console.log(`Severity: ${vuln.severity}`);
  console.log(`Title: ${vuln.title}`);
  console.log(`File: ${vuln.file}:${vuln.line}`);
  console.log(`Description: ${vuln.description}`);
  
  if (vuln.recommendation) {
    console.log(`\nRecommendation: ${vuln.recommendation}`);
  }
  
  if (vuln.codeSnippet) {
    console.log(`\nCode:\n${vuln.codeSnippet}`);
  }

  await security.close();
}
```

## CI/CD Integration

### GitHub Actions

```yaml
name: Security Scan

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: '22'
      
      - name: Install Codex Security
        run: npm install -g @openai/codex-security
      
      - name: Run Security Scan
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
        run: codex-security scan . --auth api-key --output-format json --output-file security-report.json
      
      - name: Upload Results
        uses: actions/upload-artifact@v3
        with:
          name: security-report
          path: security-report.json
```

### GitLab CI

```yaml
security_scan:
  image: node:22
  script:
    - npm install -g @openai/codex-security
    - codex-security scan . --auth api-key --output-format json --output-file security-report.json
  variables:
    OPENAI_API_KEY: $OPENAI_API_KEY
  artifacts:
    reports:
      security: security-report.json
```

### Jenkins Pipeline

```groovy
pipeline {
  agent any
  
  environment {
    OPENAI_API_KEY = credentials('openai-api-key')
  }
  
  stages {
    stage('Security Scan') {
      steps {
        sh 'npm install -g @openai/codex-security'
        sh 'codex-security scan . --auth api-key --output-format json --output-file security-report.json'
        archiveArtifacts artifacts: 'security-report.json'
      }
    }
  }
}
```

## Configuration

### Environment Variables

- `OPENAI_API_KEY` or `CODEX_API_KEY`: API key for authentication
- `CODEX_SECURITY_STATE_DIR`: Custom state directory for scan history (useful when repository directory is read-only)

### Scan Configuration

Common options:

- `--model <model>`: AI model to use (e.g., `gpt-5.6-terra`)
- `--effort <level>`: Scan effort level (`low`, `medium`, `high`)
- `--auth <method>`: Authentication method (`chatgpt`, `api-key`)
- `--output-format <format>`: Output format (`text`, `json`, `sarif`)
- `--output-file <path>`: Save report to specific file
- `--exclude <patterns>`: Exclude files/directories from scan
- `--include <patterns>`: Include only specific files/directories

## Common Patterns

### Pre-commit Hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

npx @openai/codex-security scan . --effort low --auth api-key

if [ $? -ne 0 ]; then
  echo "Security scan failed. Commit aborted."
  exit 1
fi
```

### Automated Fix Application

```typescript
import { CodexSecurity } from "@openai/codex-security";
import { writeFile } from "fs/promises";

async function autoFix() {
  const security = new CodexSecurity();
  const result = await security.run(".");

  for (const vuln of result.vulnerabilities) {
    if (vuln.autoFix && vuln.severity === "critical") {
      console.log(`Auto-fixing: ${vuln.title} in ${vuln.file}`);
      // Apply fix (implementation depends on vuln.autoFix structure)
    }
  }

  await security.close();
}
```

### Progressive Scanning

```typescript
import { CodexSecurity } from "@openai/codex-security";

async function progressiveScan() {
  const security = new CodexSecurity();

  // Quick scan first
  console.log("Running quick scan...");
  let result = await security.run(".", { effort: "low" });
  
  if (result.vulnerabilities.some(v => v.severity === "critical")) {
    console.log("Critical issues found, running deep scan...");
    result = await security.run(".", { effort: "high" });
  }

  await security.close();
  return result;
}
```

## Troubleshooting

### Authentication Issues

**Problem:** "Authentication failed" or "Invalid API key"

**Solutions:**
- Verify API key is set correctly: `echo $OPENAI_API_KEY`
- Try explicit authentication: `npx @openai/codex-security login`
- Check API key permissions in OpenAI dashboard
- Ensure you have access to Codex Security

### Node.js Version Errors

**Problem:** "Unsupported Node.js version"

**Solutions:**
- Check version: `node --version`
- Install compatible version (22.13.0+, 24.x, or 26.x)
- Use nvm: `nvm install 22 && nvm use 22`

### Scan History Not Saving

**Problem:** Cannot write scan history

**Solution:** Set custom state directory:

```bash
export CODEX_SECURITY_STATE_DIR=/tmp/codex-security-state
npx @openai/codex-security scan .
```

### Memory Issues on Large Codebases

**Problem:** Out of memory errors

**Solutions:**
- Exclude large directories: `--exclude node_modules,dist,build`
- Scan incrementally by directory
- Use lower effort level: `--effort low`
- Increase Node.js memory: `NODE_OPTIONS=--max-old-space-size=4096`

### False Positives

**Problem:** Too many false positive vulnerabilities

**Solutions:**
- Use higher confidence threshold in SDK options
- Review and filter results by severity
- Exclude test files and generated code
- Report false positives to improve model accuracy

### CI/CD Failures

**Problem:** Scans fail in CI/CD pipeline

**Solutions:**
- Ensure Python 3.10+ is installed in CI environment
- Verify API key is properly set as secret
- Use `--auth api-key` explicitly in CI
- Check CI runner has sufficient memory and CPU
- Add timeout handling for long scans
