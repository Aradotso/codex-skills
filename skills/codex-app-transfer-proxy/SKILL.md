---
name: codex-app-transfer-proxy
description: Local Rust proxy that translates OpenAI Codex CLI Responses API into Chat Completions for Kimi, DeepSeek, GLM, and other OpenAI-compatible providers
triggers:
  - set up codex app transfer proxy
  - configure codex cli with deepseek
  - use kimi with codex desktop
  - translate responses api to chat completions
  - proxy codex to third party llm
  - configure codex app transfer providers
  - add custom model mapping to codex
  - troubleshoot codex app transfer connection
---

# Codex App Transfer Proxy

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Codex App Transfer is a local desktop gateway written in Rust that proxies OpenAI Codex CLI/Desktop requests. It translates the Responses API protocol (`/responses`) into Chat Completions format, enabling Codex to work with third-party providers like DeepSeek, Kimi, Xiaomi MiMo, Zhipu GLM, Alibaba Bailian, MiniMax, Gemini, Claude, and Grok.

The tool runs as a Tauri 2.x desktop app with a local HTTP server (default `127.0.0.1:18080`) that intercepts Codex requests, performs protocol translation (including multi-turn context, `previous_response_id` history replay, tool calls, and `apply_patch` diffs), and forwards to upstream providers.

## Installation

**From Releases (Recommended)**

Download the latest binary for your platform from [GitHub Releases](https://github.com/Cmochance/codex-app-transfer/releases/latest):

- **Windows**: `Codex-App-Transfer-v<version>-Windows-x64-Setup.exe` (NSIS installer)
- **macOS (Apple Silicon)**: `Codex-App-Transfer-v<version>-macOS-arm64.dmg`
- **macOS (Intel)**: `Codex-App-Transfer-v<version>-macOS-x64.dmg`
- **Linux (Debian/Ubuntu)**: `Codex-App-Transfer-v<version>-Linux-x86_64.deb`
- **Linux (AppImage)**: `Codex-App-Transfer-v<version>-Linux-x86_64.AppImage`

**Build from Source**

```bash
git clone https://github.com/Cmochance/codex-app-transfer.git
cd codex-app-transfer
cargo tauri build --bundles app,dmg  # macOS
cargo tauri build --bundles nsis     # Windows
cargo tauri build --bundles deb,appimage  # Linux
```

**Development Mode**

```bash
cargo tauri dev  # Hot-reload desktop app
cargo test --workspace --lib  # Run unit tests
```

## Configuration

### Adding a Provider

1. Launch Codex App Transfer desktop app
2. Click **+** in the dashboard top-right corner
3. Select a preset (DeepSeek, Kimi, MiMo, etc.) or choose **Custom**
4. Fill in:
   - **API Base URL**: e.g., `https://api.deepseek.com/v1`
   - **API Key**: `$DEEPSEEK_API_KEY` (stored encrypted)
   - **API Format**: `chat_completions` (or `gemini_native`, `anthropic_messages`, etc.)
5. Click **Fetch Models** to populate available models
6. Map OpenAI model slots to real models:
   - `gpt-5.5` → `deepseek-v4-pro`
   - `gpt-5.4` → `deepseek-v4-mini`
   - `gpt-5.3-codex` → `kimi-k2.6`
7. Click **Apply** at the bottom of the page
8. Click **↻ Restart Codex** (top-right) to reload Codex Desktop/CLI

### Provider Configuration Examples

**DeepSeek V4**

```toml
[[providers]]
name = "DeepSeek V4"
api_base = "https://api.deepseek.com/v1"
api_key = "${DEEPSEEK_API_KEY}"
api_format = "chat_completions"
enabled = true
default_model = "deepseek-v4-pro"

[providers.models]
"gpt-5.5" = "deepseek-v4-pro"
"gpt-5.4" = "deepseek-v4-mini"
```

**Kimi For Coding**

```toml
[[providers]]
name = "Kimi Code"
api_base = "https://api.moonshot.cn/v1"
api_key = "${KIMI_API_KEY}"
api_format = "chat_completions"
enabled = true
default_model = "kimi-k2.6"

[providers.models]
"gpt-5.5" = "kimi-k2.6"
"gpt-5.4" = "kimi-k1.5"
```

**Gemini Native (Google AI Studio)**

```toml
[[providers]]
name = "Gemini"
api_base = "https://generativelanguage.googleapis.com"
api_key = "${GOOGLE_AI_STUDIO_KEY}"
api_format = "gemini_native"
enabled = true
default_model = "gemini-3-pro"

[providers.models]
"gpt-5.5" = "gemini-3-pro"
"gpt-5.4" = "gemini-2.0-flash"
```

**Anthropic Messages (Claude)**

```toml
[[providers]]
name = "Claude"
api_base = "https://api.anthropic.com"
api_key = "${ANTHROPIC_API_KEY}"
api_format = "anthropic_messages"
enabled = true
default_model = "claude-3-7-sonnet-20250219"

[providers.models]
"gpt-5.5" = "claude-3-7-sonnet-20250219"
```

### Configuration File Location

- **macOS/Linux**: `~/.codex-app-transfer/config.toml`
- **Windows**: `%USERPROFILE%\.codex-app-transfer\config.toml`

Config is auto-saved when you click **Apply** in the UI. Manual edits require app restart.

### Session Persistence

Multi-turn history is stored in two layers:

- **L1 (Memory)**: LRU cache for active sessions
- **L2 (SQLite)**: `~/.codex-app-transfer/sessions.db` (30-day TTL)

Sessions survive app restarts. To clear:

```bash
rm ~/.codex-app-transfer/sessions.db
```

## Using with Codex CLI/Desktop

### Starting the Proxy

1. Launch Codex App Transfer
2. Enable at least one provider (toggle switch on provider card)
3. Click **Apply**
4. Proxy server starts on `http://127.0.0.1:18080`

Codex App Transfer auto-patches `~/.codex/config.toml` and `~/.codex/auth.json` to route through the local proxy. Original config is snapshotted before modification.

### Verifying Connection

In Codex Desktop, the model picker should show:

```
DeepSeek V4 / deepseek-v4-pro
Kimi Code / kimi-k2.6
```

If you see OpenAI model names only (`gpt-5.5`, `gpt-5.4`), the proxy is not active — click **↻ Restart Codex**.

### Example Codex Interaction

```bash
# In Codex CLI
codex --model gpt-5.5 "Explain this function"
# Routed to deepseek-v4-pro via local proxy
```

Codex Desktop chat will show tool calls (e.g., `read_file`, `apply_patch`) properly round-tripped through the proxy's Responses ↔ Chat Completions adapter.

## Protocol Translation Details

### Responses API → Chat Completions

Codex sends:

```http
POST /responses HTTP/1.1
Content-Type: application/json

{
  "model": "gpt-5.5",
  "messages": [...],
  "stream": true,
  "thinking": {"type": "enabled", "budget": "high"}
}
```

Proxy translates to:

```http
POST https://api.deepseek.com/v1/chat/completions
Content-Type: application/json
Authorization: Bearer ${DEEPSEEK_API_KEY}

{
  "model": "deepseek-v4-pro",
  "messages": [...],
  "stream": true,
  "reasoning_effort": "high"
}
```

Upstream response is translated back to Responses format with:

- `response_id` rewritten from `chatcmpl-...` → `resp_<base64>`
- Tool calls bridged: `function_call` ↔ `custom_tool_call`
- Thinking content injected as `reasoning_content` for Codex UI
- `previous_response_id` maintained across turns for history replay

### Tool Call Handling (`apply_patch`)

Codex's `apply_patch` tool (file edit diff UI) works on chat-completions providers via bidirectional adapter:

**Codex → Upstream (Chat)**

```json
{
  "type": "custom_tool_call",
  "name": "apply_patch",
  "arguments": "{\"file_path\":\"main.rs\",\"patch\":\"...\"}"
}
```

becomes:

```json
{
  "type": "function",
  "function": {
    "name": "apply_patch",
    "arguments": "{\"file_path\":\"main.rs\",\"patch\":\"...\"}"
  }
}
```

**Upstream → Codex (Responses)**

```json
{
  "tool_calls": [{
    "type": "function",
    "function": {"name": "apply_patch", "arguments": "..."}
  }]
}
```

becomes:

```json
{
  "custom_tool_calls": [{
    "type": "custom_tool_call",
    "name": "apply_patch",
    "arguments": "..."
  }]
}
```

Patch format follows V4A standard:

```
*** Begin Patch
@@ main.rs 10-15
- old line 1
- old line 2
+ new line 1
+ new line 2
*** End Patch
```

### Thinking Mode (`reasoning_effort`)

Codex thinking budget (`low` / `medium` / `high` / `xhigh`) maps to provider-specific fields:

| Provider       | `xhigh`/`max`              | Other levels      |
|----------------|----------------------------|-------------------|
| DeepSeek V4    | `reasoning_effort: "max"`  | `"high"`          |
| Kimi/GLM/MiMo  | (omit field)               | (omit field)      |
| Custom Chat    | clamp to `"high"`          | pass through      |

Reasoning content (e.g., DeepSeek's `<think>` blocks) is extracted and injected as Codex `reasoning_content` field.

## Codex Desktop Theme Injection (Optional)

Codex App Transfer can inject custom CSS + background images into Codex Desktop (Electron) via Chrome DevTools Protocol:

1. Navigate to **Theme** tab
2. Enable **Theme Injection** toggle
3. Select a preset (Changli, Azur Lane, Nailin, Zani, Carton) or **Add Custom**
4. For custom: upload JPG/PNG → crop in 1:1 modal → Apply
5. Theme auto-applies on next Codex Desktop launch

**Custom Background Upload**

```rust
// Internal: Theme::Custom stores base64-encoded image + crop rect
#[derive(Serialize, Deserialize)]
pub struct CustomTheme {
    pub image_data: String,  // base64 JPEG/PNG
    pub crop_rect: CropRect, // {x, y, width, height}
}
```

Injected CSS example:

```css
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background: url(data:image/jpeg;base64,...) center/cover no-repeat;
  opacity: 0.3;
  z-index: -1;
}
.chat-panel {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
}
```

Turn off **Theme Injection** toggle to restore native Codex UI.

## Codex Document Management

Sidebar → **Codex** tab provides editors for Codex's AI-readable index files:

### Agents (`AGENTS.md`)

- Reads/writes `AGENTS.md` in any directory (auto-detects nearest `.git/` for project-root vs. subdir classification)
- UI: textarea editor + file picker
- Save triggers Codex reload if running

```markdown
# Agents

## Project Agent
You are a Rust backend engineer working on codex-app-transfer...

## Frontend Agent
You specialize in Tauri + Vue.js...
```

### Memories

- **Main index**: `~/.codex/memories/MEMORY.md`
- **Summary**: `~/.codex/memories/memory_summary.md`
- UI: two-tab editor for both files

```markdown
# Memory

## Coding Preferences
- Always use `anyhow::Result` for error handling
- Prefer `tracing` over `log`

## Project Context
- DeepSeek V4 requires `reasoning_effort: "max"` for xhigh budget
```

### Skills

- Scans `~/.codex/skills/<skill-name>/SKILL.md`
- UI: list of skills with raw markdown editor per skill
- **Open Folder** button launches system file manager for multi-file skills (scripts, examples, templates)

```markdown
---
name: rust-async-patterns
description: Common async/await patterns in Tokio
triggers:
  - write async rust code
  - use tokio runtime
---

# Rust Async Patterns

Use `tokio::spawn` for concurrent tasks:
...
```

### MCP (Model Context Protocol)

- Edits `~/.codex/config.toml` `[mcp_servers.*]` sections (preserves comments via `toml_edit`)
- **Plugins** subtab: lists installed plugins from `~/.codex/plugins/cache/` with enable/disable toggle and uninstall button

```toml
[mcp_servers.filesystem]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
```

All document edits are atomic writes with independent version history (SHA-256 hash-based paths, no cross-file collision).

## API Reference (Internal Rust Modules)

### `src-tauri/src/proxy/protocol_adapter.rs`

**Key Function: `adapt_chat_to_responses`**

```rust
pub async fn adapt_chat_to_responses(
    chat_stream: impl Stream<Item = Result<ChatCompletionChunk>>,
    original_request: &ResponsesRequest,
    provider_config: &ProviderConfig,
) -> Result<impl Stream<Item = Result<ResponsesStreamChunk>>> {
    // Translates chat SSE chunks to Responses format
    // - Rewrites response_id
    // - Bridges tool_calls
    // - Injects reasoning_content from <think> blocks
}
```

**Key Function: `adapt_responses_to_chat`**

```rust
pub fn adapt_responses_to_chat(
    req: &ResponsesRequest,
    provider: &ProviderConfig,
) -> Result<ChatCompletionRequest> {
    // Maps Responses messages to chat messages
    // - Flattens custom_tool_calls → function calls
    // - Injects system prompts for apply_patch rules (language-aware)
    // - Maps thinking.budget → reasoning_effort
}
```

### `src-tauri/src/session/manager.rs`

**Session Lookup**

```rust
pub async fn get_or_create_session(
    &self,
    response_id: Option<&str>,
    request: &ResponsesRequest,
) -> Result<Arc<Session>> {
    // L1: check memory cache
    // L2: query sqlite sessions.db
    // Create new if not found
}
```

**History Replay**

```rust
pub async fn replay_history(
    &self,
    previous_response_id: &str,
) -> Result<Vec<Message>> {
    // Fetches full conversation history for previous_response_id
    // Used in autocompact + multi-turn tool loops
}
```

### `src-tauri/src/config/mod.rs`

**Load/Save Config**

```rust
pub fn load_config() -> Result<AppConfig> {
    let path = get_config_path()?; // ~/.codex-app-transfer/config.toml
    let content = fs::read_to_string(&path)?;
    toml::from_str(&content)
}

pub fn save_config(config: &AppConfig) -> Result<()> {
    let path = get_config_path()?;
    let toml_str = toml::to_string_pretty(config)?;
    fs::write(&path, toml_str)?;
    Ok(())
}
```

**Provider Schema**

```rust
#[derive(Serialize, Deserialize, Clone)]
pub struct ProviderConfig {
    pub name: String,
    pub api_base: String,
    pub api_key: String,
    pub api_format: ApiFormat, // chat_completions | gemini_native | anthropic_messages | responses_passthrough
    pub enabled: bool,
    pub default_model: String,
    pub models: HashMap<String, String>, // "gpt-5.5" -> "deepseek-v4-pro"
    pub request_options: Option<serde_json::Value>, // Provider-specific overrides
}
```

## Common Patterns

### Adding a New Provider Preset

Edit `src-tauri/src/config/presets.rs`:

```rust
pub fn get_preset(name: &str) -> Option<ProviderConfig> {
    match name {
        "deepseek" => Some(ProviderConfig {
            name: "DeepSeek V4".into(),
            api_base: "https://api.deepseek.com/v1".into(),
            api_format: ApiFormat::ChatCompletions,
            models: HashMap::from([
                ("gpt-5.5".into(), "deepseek-v4-pro".into()),
                ("gpt-5.4".into(), "deepseek-v4-mini".into()),
            ]),
            ..Default::default()
        }),
        "my-provider" => Some(ProviderConfig {
            name: "My Provider".into(),
            api_base: "https://api.example.com/v1".into(),
            api_format: ApiFormat::ChatCompletions,
            models: HashMap::from([
                ("gpt-5.5".into(), "my-model-large".into()),
            ]),
            ..Default::default()
        }),
        _ => None,
    }
}
```

Rebuild UI to expose preset in dropdown.

### Injecting Custom System Prompts

Prompts follow UI language setting (`zh-CN` or `en`). Edit `src-tauri/src/proxy/protocol_adapter.rs`:

```rust
fn build_apply_patch_system_prompt(lang: &str) -> String {
    match lang {
        "zh-CN" => "你必须使用 apply_patch 工具...",
        _ => "You must use the apply_patch tool...",
    }
}
```

Prompts are injected only for non-OpenAI providers when `apply_patch` tool is available.

### Custom Tool Repair (Grok Web Example)

Grok Web flattens nested `tool_calls`. Add repair in `src-tauri/src/proxy/grok.rs`:

```rust
fn repair_tool_calls(chunk: &mut ChatCompletionChunk) {
    if let Some(choice) = chunk.choices.first_mut() {
        if let Some(tools) = &choice.delta.tool_calls {
            // Grok sends [{function: {name, arguments}}, ...] at top level
            // Wrap into proper tool_calls structure
            choice.delta.tool_calls = Some(tools.iter().map(|t| ToolCall {
                id: format!("call_{}", uuid::Uuid::new_v4()),
                r#type: "function".into(),
                function: t.function.clone(),
            }).collect());
        }
    }
}
```

Called in `adapt_chat_to_responses` before standard bridging.

## Troubleshooting

### Codex still uses OpenAI models after enabling provider

**Cause**: Codex config not reloaded.

**Fix**: Click **↻ Restart Codex** button in Codex App Transfer UI (top-right corner).

### Provider shows "API key invalid" in logs

**Cause**: API key env var not resolved or incorrect.

**Fix**:

```bash
# Verify env var is set
echo $DEEPSEEK_API_KEY

# Restart Codex App Transfer (env vars loaded on startup)
```

Or paste literal key in UI (not recommended for security).

### `apply_patch` diffs not rendering in Codex

**Cause**: Provider not bridging `function_call` ↔ `custom_tool_call` correctly.

**Fix**: Check logs for `tool_call_repair` warnings. Ensure provider config has `api_format: "chat_completions"` (not `responses_passthrough`).

**Debug**:

```bash
# Enable trace logging
export RUST_LOG=codex_app_transfer=trace
# Check logs tab in UI for tool call JSON
```

### DeepSeek thinking mode not working

**Cause**: `reasoning_effort` not sent or wrong value.

**Fix**: For `xhigh` budget, ensure adapter maps to `"max"`:

```rust
// In protocol_adapter.rs
let reasoning_effort = match thinking_budget {
    "xhigh" => "max",
    _ => "high",
};
```

Verify in logs:

```
[proxy] Sending to DeepSeek: {"reasoning_effort":"max",...}
```

### Session history not persisting

**Cause**: SQLite DB locked or corrupt.

**Fix**:

```bash
# Stop Codex App Transfer
# Remove DB (will recreate on next start)
rm ~/.codex-app-transfer/sessions.db
```

### Codex Desktop theme not applying

**Cause**: CDP connection failed or Codex not running.

**Fix**:

1. Ensure Codex Desktop is running
2. Check **Theme** tab shows "Connected" status
3. Toggle **Theme Injection** off then on
4. Restart Codex Desktop

**Logs**:

```
[theme] CDP connect failed: ConnectionRefused
```

Means Codex Desktop debug port (9222) not accessible — check firewall.

### Multiple instances conflict

**Symptom**: Config changes not saving, "file lock" errors.

**Cause**: Two Codex App Transfer processes running.

**Fix**: Quit both instances (right-click system tray → Exit), relaunch once. App uses single-instance lock (second launch auto-focuses existing window).

### Provider fetch models returns 401

**Cause**: API base URL wrong or key expired.

**Fix**:

```bash
# Test API manually
curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY"

# If 401, regenerate key from provider dashboard
```

Update key in UI, click **Apply**.

---

**For more details**: See [GitHub Issues](https://github.com/Cmochance/codex-app-transfer/issues) or [Changelog](https://github.com/Cmochance/codex-app-transfer/blob/main/CHANGELOG.md).
