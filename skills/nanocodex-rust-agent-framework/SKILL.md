---
name: nanocodex-rust-agent-framework
description: Build and orchestrate frontier OpenAI agents in Rust with Nanocodex's modular components for API clients, tools, and agent lifecycle management.
triggers:
  - build an AI agent with nanocodex
  - create a rust openai agent
  - use nanocodex agent framework
  - implement nanocodex tools
  - set up nanocodex agent session
  - integrate openai codex in rust
  - nanocodex agent examples
  - configure nanocodex workspace
---

# Nanocodex Rust Agent Framework

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Nanocodex is a Rust framework for building frontier OpenAI agents with modular, composable components. It provides building blocks for agent lifecycle management, OpenAI API integration, tool execution, and observability. The framework emphasizes small, excellent components with sharp boundaries: an OpenAI client works without an agent loop, tools work without a CLI, and the agent orchestrates these pieces cleanly.

## Installation

### CLI Installation

Install the Nanocodex CLI on macOS or Linux:

```sh
curl -fsSL https://nanocodex.paradigm.xyz | bash
```

Switch between versions:

```sh
nanocodex update                 # latest stable
nanocodex update 0.2.0           # specific version
nanocodex update --nightly       # nightly build
nanocodex update --pr 50         # PR artifact (requires gh CLI)
nanocodex update --path ./nanocodex  # local binary
```

### Rust Library

Add to your `Cargo.toml`:

```toml
[dependencies]
nanocodex = "0.2"

# Or with observability support
nanocodex = { version = "0.2", features = ["observability"] }

# Or use individual components
nanocodex-agent = "0.2"
nanocodex-oai-api = "0.2"
nanocodex-tools = "0.2"
```

## Core Components

Nanocodex is organized into distinct layers:

- **`nanocodex`** - Facade with common imports and prelude
- **`nanocodex-agent`** - Agent lifecycle, prompt ordering, tool loop, cancellation
- **`nanocodex-oai-api`** - OpenAI WebSocket client, authentication, session management
- **`nanocodex-tools`** - Tool runtime, workspace tools, MCP support
- **`nanocodex-observability`** - OpenTelemetry tracing and metrics

## Basic Agent Setup

### Minimal Agent Example

```rust
use nanocodex::{Nanocodex, OpenAi};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let openai = OpenAi::new(std::env::var("OPENAI_API_KEY")?)?;
    
    let (agent, mut events) = Nanocodex::builder(openai)
        .instructions(
            "You are a Rust coding agent. Make focused changes, \
             preserve unrelated work, and run relevant tests before finishing."
        )
        .workspace(std::env::current_dir()?)
        .build()?;

    // Spawn event listener
    let event_task = tokio::spawn(async move {
        while let Some(event) = events.recv().await {
            eprintln!("event {}: {:?}", event.seq, event.kind);
            if event.kind.is_terminal() {
                break;
            }
        }
    });

    // Send prompt and await result
    let result = agent
        .prompt("Find and fix the failing parser test.")
        .await?
        .await?;

    event_task.await?;
    println!("{}", result.final_message());
    
    Ok(())
}
```

### Streaming Agent Response

Stream deltas as they arrive:

```rust
use nanocodex::{Nanocodex, OpenAi};
use nanocodex::agent::events::{AgentEventData, AssistantEvent};
use futures_util::StreamExt;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let openai = OpenAi::new(std::env::var("OPENAI_API_KEY")?)?;
    let (agent, _events) = Nanocodex::builder(openai)
        .instructions("You are a helpful assistant.")
        .build()?;

    let mut turn = agent.prompt("Explain async/await in Rust").await?;
    
    while let Some(event) = turn.next().await {
        if let AgentEventData::Assistant(AssistantEvent::Delta(delta)) = event.data()? {
            print!("{}", delta.text);
        }
    }
    
    let result = turn.await?;
    println!("\n\nFinal: {}", result.final_message());
    
    Ok(())
}
```

## Agent Builder Configuration

### Workspace and Instructions

```rust
use nanocodex::{Nanocodex, OpenAi};
use std::path::PathBuf;

let openai = OpenAi::new(std::env::var("OPENAI_API_KEY")?)?;

let (agent, events) = Nanocodex::builder(openai)
    .instructions("You are a Rust expert focused on performance and correctness.")
    .workspace(PathBuf::from("/path/to/project"))
    .build()?;
```

### Custom Tools

Register custom tools with the agent:

```rust
use nanocodex::{Nanocodex, OpenAi};
use nanocodex::tools::{Tool, Tools};
use serde::{Deserialize, Serialize};
use async_trait::async_trait;

#[derive(Debug, Deserialize)]
struct FetchUrlParams {
    url: String,
}

#[derive(Debug, Serialize)]
struct FetchUrlResult {
    content: String,
    status: u16,
}

struct FetchUrlTool;

#[async_trait]
impl Tool for FetchUrlTool {
    fn name(&self) -> &str {
        "fetch_url"
    }

    fn description(&self) -> &str {
        "Fetch content from a URL"
    }

    fn parameters_schema(&self) -> serde_json::Value {
        serde_json::json!({
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The URL to fetch"
                }
            },
            "required": ["url"]
        })
    }

    async fn execute(
        &self,
        params: serde_json::Value,
    ) -> Result<serde_json::Value, Box<dyn std::error::Error + Send + Sync>> {
        let params: FetchUrlParams = serde_json::from_value(params)?;
        let response = reqwest::get(&params.url).await?;
        let status = response.status().as_u16();
        let content = response.text().await?;
        
        let result = FetchUrlResult { content, status };
        Ok(serde_json::to_value(result)?)
    }
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let openai = OpenAi::new(std::env::var("OPENAI_API_KEY")?)?;
    
    let mut tools = Tools::new();
    tools.register(FetchUrlTool);
    
    let (agent, _events) = Nanocodex::builder(openai)
        .instructions("You can fetch URLs to help users.")
        .tools(tools)
        .build()?;
    
    let result = agent
        .prompt("Fetch https://example.com and summarize it")
        .await?
        .await?;
    
    println!("{}", result.final_message());
    Ok(())
}
```

### Using the Tool Macro

Simplify tool creation with the `#[tool]` macro:

```rust
use nanocodex::tools::tool;
use serde::{Deserialize, Serialize};

#[derive(Deserialize)]
struct CalculateParams {
    expression: String,
}

#[derive(Serialize)]
struct CalculateResult {
    result: f64,
}

#[tool(
    name = "calculate",
    description = "Evaluate a mathematical expression"
)]
async fn calculate(params: CalculateParams) -> Result<CalculateResult, String> {
    // Simple example - real implementation would parse expression
    Ok(CalculateResult { result: 42.0 })
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let openai = nanocodex::OpenAi::new(std::env::var("OPENAI_API_KEY")?)?;
    
    let mut tools = nanocodex::tools::Tools::new();
    tools.register(calculate);
    
    let (agent, _events) = nanocodex::Nanocodex::builder(openai)
        .tools(tools)
        .build()?;
    
    Ok(())
}
```

## OpenAI API Client (Standalone)

Use the OpenAI client without the full agent:

```rust
use nanocodex::oai::{OpenAi, Message, MessageContent, Role};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let client = OpenAi::new(std::env::var("OPENAI_API_KEY")?)?;
    
    let session = client.session().await?;
    
    let messages = vec![
        Message {
            role: Role::User,
            content: MessageContent::Text("Hello, how are you?".to_string()),
        }
    ];
    
    let mut turn = session.chat(messages).await?;
    
    while let Some(response) = turn.next().await {
        let response = response?;
        if let Some(text) = response.text() {
            print!("{}", text);
        }
    }
    
    Ok(())
}
```

## Session Management

### Multi-Turn Conversations

The agent automatically maintains conversation history:

```rust
use nanocodex::{Nanocodex, OpenAi};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let openai = OpenAi::new(std::env::var("OPENAI_API_KEY")?)?;
    let (agent, _events) = Nanocodex::builder(openai)
        .instructions("You are a helpful assistant.")
        .build()?;

    // First turn
    let result1 = agent
        .prompt("My name is Alice")
        .await?
        .await?;
    println!("Turn 1: {}", result1.final_message());

    // Second turn - agent remembers context
    let result2 = agent
        .prompt("What's my name?")
        .await?
        .await?;
    println!("Turn 2: {}", result2.final_message());
    
    Ok(())
}
```

### Cloning Agent Handles

Create cheap clones for concurrent access:

```rust
let agent_clone = agent.clone();

tokio::spawn(async move {
    let result = agent_clone
        .prompt("Background task")
        .await?
        .await?;
    Ok::<_, Box<dyn std::error::Error>>(())
});
```

### Forking Sessions

Create branching conversations:

```rust
// Fork from current state
let forked_agent = agent.fork().await?;

// Fork from specific snapshot
let snapshot_id = result.snapshot_id();
let branched_agent = agent.fork_from(snapshot_id).await?;

// Spawn new independent session
let spawned_agent = agent.spawn().await?;
```

## CLI Usage

### Interactive TUI Mode

```sh
nanocodex
```

### One-Shot Commands

```sh
nanocodex run "implement a binary search function in src/search.rs"
```

### VM-Backed Tools

Run tools in an isolated VM:

```sh
# Build VM guest runtime
just build-vm-guest

# Run with VM backing
nanocodex \
  --vm .nanocodex/vm/session-rootfs.ext4 \
  --vm-guest-runtime target/aarch64-unknown-linux-musl/debug/nanocodex-vm-guest \
  --vm-workspace /app

# One-shot with VM
nanocodex run "inspect the repository" \
  --vm .nanocodex/vm/session-rootfs.ext4 \
  --vm-guest-runtime target/aarch64-unknown-linux-musl/debug/nanocodex-vm-guest \
  --vm-workspace /app
```

## Observability

### Enable Tracing

```rust
use nanocodex::observability::{init_tracing, TracingConfig};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    init_tracing(TracingConfig::default())?;
    
    let openai = nanocodex::OpenAi::new(std::env::var("OPENAI_API_KEY")?)?;
    let (agent, _events) = nanocodex::Nanocodex::builder(openai).build()?;
    
    // Agent operations will now emit structured traces
    let result = agent.prompt("test").await?.await?;
    
    Ok(())
}
```

### OpenTelemetry Integration

```rust
use nanocodex::observability::{init_tracing, TracingConfig};
use opentelemetry::global;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let config = TracingConfig {
        endpoint: Some("http://localhost:4317".to_string()),
        service_name: "my-agent".to_string(),
        ..Default::default()
    };
    
    init_tracing(config)?;
    
    // Your agent code here
    
    global::shutdown_tracer_provider();
    Ok(())
}
```

## Common Patterns

### Error Handling

```rust
use nanocodex::{Nanocodex, OpenAi};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let openai = match OpenAi::new(std::env::var("OPENAI_API_KEY")?) {
        Ok(client) => client,
        Err(e) => {
            eprintln!("Failed to create OpenAI client: {}", e);
            return Err(e.into());
        }
    };
    
    let (agent, _events) = Nanocodex::builder(openai).build()?;
    
    match agent.prompt("test").await {
        Ok(turn) => {
            match turn.await {
                Ok(result) => println!("{}", result.final_message()),
                Err(e) => eprintln!("Turn failed: {}", e),
            }
        }
        Err(e) => eprintln!("Failed to send prompt: {}", e),
    }
    
    Ok(())
}
```

### Timeout Handling

```rust
use tokio::time::{timeout, Duration};

let result = timeout(
    Duration::from_secs(60),
    agent.prompt("complex task").await?.await,
).await??;
```

### Cost Tracking

```rust
let result = agent.prompt("analyze this code").await?.await?;

if let Some(usage) = result.usage() {
    println!("Tokens used: {} input, {} output", 
             usage.input_tokens, 
             usage.output_tokens);
    if let Some(cost) = usage.estimated_cost_usd() {
        println!("Estimated cost: ${:.4}", cost);
    }
}
```

## Troubleshooting

### Authentication Issues

Ensure `OPENAI_API_KEY` is set:

```sh
export OPENAI_API_KEY=sk-...
```

For ChatGPT authentication instead of API keys, use:

```rust
let openai = OpenAi::from_chatgpt_auth()?;
```

### WebSocket Connection Failures

The client automatically handles reconnection and replay. If persistent issues occur:

1. Check network connectivity
2. Verify API key permissions
3. Ensure no firewall blocking WebSocket connections
4. Review rate limits on your OpenAI account

### Tool Execution Errors

Debug tool calls with event monitoring:

```rust
let event_task = tokio::spawn(async move {
    while let Some(event) = events.recv().await {
        match &event.kind {
            nanocodex::agent::EventKind::ToolCall { name, args } => {
                eprintln!("Tool called: {} with {:?}", name, args);
            }
            nanocodex::agent::EventKind::ToolResult { result } => {
                eprintln!("Tool result: {:?}", result);
            }
            _ => {}
        }
    }
});
```

### Memory and Context Management

The agent handles compaction automatically. To monitor context size:

```rust
if let Some(usage) = result.usage() {
    if usage.input_tokens > 100_000 {
        eprintln!("Warning: Large context ({} tokens)", usage.input_tokens);
    }
}
```

### VM Issues

When using VM-backed tools:

1. Ensure VM guest runtime is built for correct architecture
2. Check VM image has `nanocodex-vm-guest` in `/usr/local/bin`
3. Verify workspace path exists in VM
4. On macOS, ensure proper code signing for VM binaries

## Configuration Files

### AGENTS.md Discovery

Place `AGENTS.md` in your workspace root for agent context:

```markdown
# Project Context

This is a Rust library for parsing configuration files.

## Key Files
- `src/parser.rs` - Main parsing logic
- `src/config.rs` - Configuration structures

## Testing
Run tests with: `cargo test`
```

The agent automatically discovers and uses this context.

## Best Practices

1. **Use typed results**: Leverage `TurnResult` for structured access to messages, usage, and snapshots
2. **Monitor events**: Subscribe to the event stream for debugging and telemetry
3. **Clone efficiently**: Use `agent.clone()` for concurrent access to the same session
4. **Handle errors gracefully**: The double-await pattern allows separate error handling for prompt submission and completion
5. **Provide clear instructions**: Set detailed system instructions via the builder
6. **Organize tools**: Group related tools and use clear naming conventions
7. **Track costs**: Monitor token usage and estimated costs in production
