---
name: codex-chatgpt-control-bridge
description: Drive visible ChatGPT web sessions from Codex agents for planning, research, and deep reasoning workflows
triggers:
  - consult chatgpt for planning
  - ask chatgpt web for research
  - use chatgpt pro for deep reasoning
  - open a chatgpt thread
  - continue the chatgpt conversation
  - upload files to chatgpt
  - download chatgpt artifacts
  - get a second opinion from chatgpt
version: 1.0.0
---

# codex-chatgpt-control-bridge

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## What This Does

`codex-chatgpt-control` is an unofficial SDK that lets Codex agents control visible ChatGPT web sessions through a browser bridge. It enables structured workflows where Codex handles execution (local files, commands, tests) while delegating planning, research, brainstorming, or deep reasoning to the ChatGPT web product the user can see.

**Key capabilities:**
- Start or continue visible ChatGPT threads
- Submit prompts and capture Markdown responses
- Upload local files through visible browser controls
- Download generated artifacts (files, images)
- Handle clear stop reasons (login required, captcha, permissions)
- Generate privacy-preserving local run reports

**What this is NOT:**
- Not a hidden ChatGPT API wrapper
- Not for account automation or scraping
- Not a generic browser automation framework
- Requires visible browser, signed-in session, and user approval

## Installation

### As Codex Plugin (Recommended)

```bash
codex plugin marketplace add adamallcock/codex-chatgpt-control --ref main
codex plugin add codex-chatgpt-control@codex-chatgpt-control
```

Update to latest:

```bash
codex plugin marketplace upgrade codex-chatgpt-control
codex plugin add codex-chatgpt-control@codex-chatgpt-control
```

### Node Package

```bash
npm install codex-chatgpt-control
```

### Python Package

```bash
pip install codex-chatgpt-control
```

### Runtime Requirements

**For browser control:**
- Signed-in ChatGPT session in Chrome
- Compatible Codex/browser bridge exposing `globalThis.agent`
- User approval for prompts, file uploads, downloads

**For file uploads:**
1. **Chrome extension:** Enable "Allow access to file URLs" in `chrome://extensions` for the Codex bridge extension
2. **Codex settings:** Allow Chrome uploads under Computer Use > Google Chrome > Permissions > Uploads

**For development/testing:**
- Node.js 20+ for Node runtime
- Python 3.10+ for Python client

## Core SDK Usage (Node)

### Basic ChatGPT Consultation

```javascript
import { createChatGPT } from "codex-chatgpt-control";

const chatgpt = createChatGPT({ agent: globalThis.agent });

// Define an agent with instructions
const reviewer = chatgpt.agent({
  name: "reviewer",
  instructions: "Review carefully and return detailed Markdown analysis."
});

// Run a new thread workflow
const result = await chatgpt.runner.run(reviewer, {
  input: "Analyze this project's architecture and suggest improvements.",
  thread: { type: "new" },
  response: { format: "markdown" }
});

console.log(result.output_text);
console.log(result.status); // completed, stopped_by_user, or blocker reason
```

### Continue Existing Thread

```javascript
// User has already opened chatgpt.com/c/<id> in browser
const result = await chatgpt.askInThread({
  thread: { 
    type: "url", 
    url: "https://chatgpt.com/c/abc123" 
  },
  existingTab: true, // Don't replace the user's tab
  prompt: "Continue with the next implementation step.",
  wait: true,
  read: { format: "markdown" }
});

console.log(result.text);
```

### Upload Files to ChatGPT

```javascript
// Paths must be absolute on the backend host machine
const result = await chatgpt.askWithFiles({
  thread: { type: "new" },
  prompt: "Review these design documents and suggest improvements.",
  files: [
    "/home/user/project/docs/architecture.md",
    "/home/user/project/docs/design.pdf"
  ],
  wait: true,
  read: { format: "markdown" }
});
```

**Path requirements:**
- Linux/WSL: `/home/you/file.pdf` or `/mnt/c/work/file.pdf`
- Windows: `C:\\Users\\you\\file.pdf` or `\\\\server\\share\\file.pdf`
- Rejects ambiguous forms like `C:Users\\file.pdf`

### Download Generated Artifacts

```javascript
// Wait for ChatGPT to generate a file
await chatgpt.artifacts.wait({
  kind: "file", // or "image" for image generations
  requireDownload: true,
  timeoutMs: 30000
});

// Download to local directory
const downloaded = await chatgpt.artifacts.downloadLatest({
  destDir: "/absolute/path/to/output/dir"
});

console.log(downloaded.path);
console.log(downloaded.filename);
```

### Image Generation Workflow

```javascript
// Images are artifacts, not text messages
await chatgpt.ask({
  thread: { type: "new" },
  prompt: "Generate a system architecture diagram.",
  wait: true
});

// Check if response is an image (messages.readLatest may return not_found)
await chatgpt.artifacts.wait({
  kind: "image",
  requireDownload: true
});

const image = await chatgpt.artifacts.downloadLatest({
  destDir: "/path/to/images"
});
```

## Core SDK Usage (Python)

### Basic Workflow

```python
from codex_chatgpt_control import (
    Agent, BackendClient, Runner, StdioBackendTransport
)

# Connect to Node backend
backend = BackendClient(StdioBackendTransport(
    command=["npx", "--yes", "--package", "codex-chatgpt-control", 
             "codex-chatgpt-control-backend"]
))
runner = Runner(backend)

try:
    # Run consultation workflow
    result = runner.run_sync(
        Agent(
            name="planner",
            instructions="Create detailed implementation plans."
        ),
        {
            "input": "Plan the next feature implementation.",
            "thread": {"type": "new"},
            "response": {"format": "markdown"},
        },
    )
    
    print(f"Status: {result.status}")
    print(f"Response: {result.output_text}")
finally:
    backend.close()
```

### File Upload (Python)

```python
result = runner.run_sync(
    Agent(name="reviewer", instructions="Review uploaded files."),
    {
        "input": "Review these specifications.",
        "thread": {"type": "new"},
        "response": {"format": "markdown"},
        "files": [
            "/home/user/project/specs.md",
            "/home/user/project/requirements.pdf"
        ]
    }
)
```

## Common Patterns

### Planning Consultation

```javascript
const planner = chatgpt.agent({
  name: "strategic-planner",
  instructions: "Create detailed, actionable implementation plans with clear milestones."
});

const plan = await chatgpt.runner.run(planner, {
  input: `Review our current codebase structure and plan the migration to microservices.
  
Context:
- Monolithic Express.js app, ~50k LOC
- PostgreSQL database
- Need to maintain backward compatibility
- 6-month timeline`,
  thread: { type: "new" },
  response: { format: "markdown" }
});

// Save plan locally
await fs.writeFile("migration-plan.md", plan.output_text);
```

### Research Synthesis

```javascript
const researcher = chatgpt.agent({
  name: "research-synthesizer",
  instructions: "Gather information, compare approaches, and synthesize findings into actionable recommendations."
});

const research = await chatgpt.runner.run(researcher, {
  input: "Research current best practices for WebAssembly in Node.js applications. Compare available runtimes and toolchains.",
  thread: { type: "new" },
  response: { format: "markdown" }
});
```

### Deep Code Review

```javascript
// Upload multiple files for holistic review
const review = await chatgpt.askWithFiles({
  thread: { type: "new" },
  prompt: `Perform a comprehensive security and architecture review.
  
Focus on:
1. Authentication/authorization flows
2. Data validation and sanitization
3. API design consistency
4. Error handling patterns
5. Performance considerations`,
  files: [
    "/project/src/auth/middleware.js",
    "/project/src/api/routes.js",
    "/project/src/db/queries.js"
  ],
  wait: true,
  read: { format: "markdown" }
});
```

### Multi-Step Conversation

```javascript
// Start thread
const initial = await chatgpt.ask({
  thread: { type: "new" },
  prompt: "Let's design a caching strategy for this API.",
  wait: true,
  read: { format: "markdown" }
});

const threadUrl = initial.thread_url;

// Continue thread with follow-up
const followup = await chatgpt.askInThread({
  thread: { type: "url", url: threadUrl },
  existingTab: false,
  prompt: "Now consider Redis vs Memcached for this use case.",
  wait: true,
  read: { format: "markdown" }
});

// Another iteration
const final = await chatgpt.askInThread({
  thread: { type: "url", url: threadUrl },
  existingTab: false,
  prompt: "Generate configuration examples for the recommended approach.",
  wait: true,
  read: { format: "markdown" }
});
```

## Handling Stop Reasons

The SDK returns structured stop reasons when workflows cannot proceed:

```javascript
const result = await chatgpt.runner.run(agent, config);

switch (result.status) {
  case "completed":
    // Success - use result.output_text
    console.log(result.output_text);
    break;
    
  case "stopped_by_user":
    // User interrupted - respect the stop
    console.log("User stopped the workflow");
    break;
    
  case "browser_bridge_unavailable":
    // No bridge access - report to user, don't retry
    console.log("Browser bridge not available. Check Codex bridge status.");
    break;
    
  case "login_required":
    // ChatGPT session expired
    console.log("ChatGPT login required. User needs to sign in.");
    break;
    
  case "captcha_or_verification":
    // Human verification needed
    console.log("ChatGPT requires verification. User must complete captcha.");
    break;
    
  default:
    // Other blocker
    console.log(`Workflow stopped: ${result.status}`);
}
```

**Important:** Do not retry blindly on blockers. These are user-actionable states.

## Run Reports

Generate privacy-preserving local reports:

```javascript
const report = chatgpt.createReport({
  title: "Feature Planning Session",
  description: "Consulted ChatGPT for microservices architecture plan",
  includeContent: false, // Default: omit prompts and responses
  metadata: {
    task: "architecture-planning",
    project: "api-migration"
  }
});

// Add run entry
report.addRun({
  agent: "strategic-planner",
  status: "completed",
  thread_url: "https://chatgpt.com/c/abc123",
  input: "Plan migration...", // Only if includeContent: true
  output_text: "..." // Only if includeContent: true
});

// Save report
await chatgpt.reports.save(report, "/path/to/reports/dir");
```

## Discovery and Help

```javascript
// List all available commands
const commands = chatgpt.commands();
console.log(commands);

// Get command-specific help
const help = chatgpt.describe("askWithFiles");
console.log(help);

// General help
chatgpt.help();
```

## Configuration

### Browser Bridge Check

```javascript
// Check if bridge is available before starting workflows
const session = chatgpt.session;
const status = await session.check();

if (status.bridge_available) {
  // Proceed with browser workflows
} else {
  console.log("Bridge unavailable. Switch to API-only workflows.");
}
```

### Response Format

```javascript
// Markdown (default, recommended)
const md = await chatgpt.ask({
  thread: { type: "new" },
  prompt: "Explain async/await",
  wait: true,
  read: { format: "markdown" }
});

// Plain text (strips formatting)
const txt = await chatgpt.ask({
  thread: { type: "new" },
  prompt: "Explain async/await",
  wait: true,
  read: { format: "text" }
});
```

## Troubleshooting

### "browser_bridge_unavailable"

**Cause:** No `globalThis.agent` available or bridge not initialized.

**Fix:**
- Ensure running in Codex environment with browser bridge enabled
- Check Codex settings: Computer Use > Google Chrome > Enable
- Verify Chrome extension is active

### File Upload Fails

**Cause:** Missing file URL permissions or upload gate.

**Fix:**
1. Chrome extension: Enable "Allow access to file URLs" in `chrome://extensions`
2. Codex app: Allow uploads in Computer Use > Google Chrome > Permissions > Uploads
3. Verify paths are absolute on backend host machine
4. Check file exists and is readable

### "login_required" or "captcha_or_verification"

**Cause:** ChatGPT session expired or requires human verification.

**Fix:**
- User must manually sign in to chatgpt.com in Chrome
- Complete any captcha/verification prompts
- Do not attempt to automate this - respect the stop reason

### Artifact Download Returns "not_found"

**Cause:** Artifact may not be ready or ChatGPT returned text instead.

**Fix:**
- Use `artifacts.wait()` with appropriate timeout
- Check if response is text (use `messages.readLatest()`) or artifact
- For images, always check artifacts even if messages.readLatest returns not_found

### Rate Limiting or Overuse

**Cause:** Excessive ChatGPT requests may hit rate limits.

**Fix:**
- Batch questions into single prompts when possible
- Use multi-step threads instead of separate new threads
- Respect stop reasons and don't retry blindly
- Consider using ChatGPT for planning/research, not execution

## When to Use This Skill

**Good use cases:**
- Deep planning requiring long context or reasoning
- Research synthesis and information gathering
- Second-opinion code reviews
- Brainstorming and ideation
- Design critique and positioning
- Naming and branding decisions

**Bad use cases:**
- Rapid iteration (use Codex directly)
- Automated testing (use local tools)
- Bulk data processing (use scripts)
- Real-time execution (use Codex execution environment)
- Anything requiring hidden/automated access

## Project Resources

- **Repo:** https://github.com/adamallcock/codex-chatgpt-control
- **npm:** https://www.npmjs.com/package/codex-chatgpt-control
- **PyPI:** https://pypi.org/project/codex-chatgpt-control/
- **License:** MIT
- **Architecture docs:** `docs/architecture.md`
- **Browser bridge docs:** `docs/browser-bridge.md`
- **Safety model:** `docs/safety.md`
