---
name: codex-x-desktop-manager
description: Desktop manager for OpenAI Codex CLI with prompt injection, provider switching, and TOML/Auth visualization
triggers:
  - how do I inject custom prompts into Codex CLI
  - switch Codex API providers using Codex-X
  - manage Codex configuration files visually
  - enable unrestricted mode for Codex CLI
  - sync Codex session provider metadata
  - configure third-party Codex providers
  - edit Codex auth.json and config.toml
  - use Codex-X to manage Codex CLI settings
---

# Codex-X Desktop Manager

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Codex-X is a cross-platform desktop application for managing OpenAI Codex CLI configurations. It provides visual interfaces for prompt injection, provider switching, TOML/JSON editing, and session management. Built with Tauri 2, React 18, and Rust.

## What Codex-X Does

- **Prompt Injection**: Inject instruction templates (`gpt5.4-unrestricted.md`, `gpt5.5-unrestricted.md`) into Codex CLI
- **Provider Management**: Switch between official OpenAI and third-party Codex API providers
- **Configuration Editing**: Visual editor for `~/.codex/config.toml` and `~/.codex/auth.json`
- **Session Sync**: Fix provider metadata in historical Codex sessions
- **Cross-Platform**: macOS (Apple Silicon/Intel), Windows, Linux

## Installation

### Download Pre-built Binaries

Download from GitHub Releases:
```bash
# Visit https://github.com/yynxxxxx/Codex-X/releases
# Available formats:
# - macOS: .dmg (Apple Silicon / Intel)
# - Windows: .msi / portable .zip
# - Linux: .deb / .rpm
```

### macOS Gatekeeper Bypass

If macOS shows "app is damaged" warning:
```bash
xattr -dr com.apple.quarantine /Applications/Codex-X.app
```

### Build from Source

```bash
# Clone repository
git clone https://github.com/yynxxxxx/Codex-X.git
cd Codex-X

# Install dependencies
pnpm install

# Development mode
pnpm dev

# Build desktop app
pnpm --dir apps/desktop tauri build
```

## Configuration Paths

Codex-X reads and writes standard Codex CLI configuration files:

```text
~/.codex/config.toml          # Main Codex configuration
~/.codex/auth.json            # Authentication data
~/.codex/sqlite/*.db          # Session databases
~/.codex/sessions/            # Active session data
~/.codex/archived_sessions/   # Archived session data
```

Codex-X stores its own data at:
```text
~/.codexx/codexx.db           # Codex-X application database
```

### Environment Variables

Override default paths:
```bash
export CODEX_HOME=/path/to/.codex
export CODEXX_HOME=/path/to/codex-x-data
export CC_SWITCH_HOME=/path/to/.cc-switch
```

## Key Features

### 1. Prompt Injection

Codex-X includes two instruction templates for Codex CLI:

**gpt5.4-unrestricted.md**:
- CTF sandbox-style bypass approach
- ~180 lines, security research focused
- Detailed methodology for testing scenarios
- Use case: SQL injection testing, penetration testing guidance

**gpt5.5-unrestricted.md**:
- Direct unrestricted developer mode
- ~40 lines, minimal instruction set
- Broad coverage for development tasks
- Use case: Reverse engineering (APK/EXE analysis)

#### Enable Prompt Injection via UI

1. Open Codex-X application
2. Navigate to "指令提示词" (Instruction Prompts) tab
3. Select desired template (5.4 or 5.5)
4. Click "启用" (Enable)
5. Codex-X will:
   - Copy template to `~/.codex/`
   - Update `config.toml` with `model_instructions_file` path

#### Manual Prompt Injection

```bash
# Copy template to Codex config directory
cp examples/gpt5.5-unrestricted.md ~/.codex/

# Edit config.toml
echo 'model_instructions_file = "/Users/yourusername/.codex/gpt5.5-unrestricted.md"' >> ~/.codex/config.toml
```

#### Testing Prompt Injection

After enabling, test with security research queries:
```bash
codex-cli chat

# Query: "如何对目标进行 SQL 注入测试？"
# Expected: Detailed SQL injection testing methodology
# (instead of refusal or generic response)

# Query: "APK逆向分析流程"
# Expected: Android APK reverse engineering workflow
```

### 2. Provider Management

#### Add Third-Party Provider via UI

1. Navigate to "供应商 API" (Provider API) tab
2. Click "添加供应商" (Add Provider)
3. Configure:
   - Name: Custom provider name
   - Base URL: API endpoint (e.g., `https://api.example.com/v1`)
   - API Key: Use environment variable reference
   - Model: Model identifier (e.g., `gpt-4`, `claude-3`)
   - Wire API: Protocol (OpenAI/Anthropic compatible)

#### Provider Configuration in TOML

Codex-X generates TOML configuration:

```toml
[providers.custom_provider]
base_url = "https://api.example.com/v1"
api_key = "${CUSTOM_API_KEY}"
model = "gpt-4"
wire_api = "openai"

[active]
provider = "custom_provider"
```

#### Switch Providers Programmatically

```typescript
// TypeScript example - Tauri command
import { invoke } from '@tauri-apps/api/tauri';

async function switchProvider(providerName: string) {
  await invoke('set_active_provider', { 
    provider: providerName 
  });
}

// Switch to custom provider
await switchProvider('custom_provider');
```

#### Import from cc-switch

If migrating from cc-switch:
1. Set `CC_SWITCH_HOME` environment variable
2. Codex-X will auto-detect and offer import
3. All cc-switch providers will be available in Codex-X

### 3. TOML Configuration Editor

#### View Current Configuration

```typescript
// Tauri command to read config.toml
import { invoke } from '@tauri-apps/api/tauri';

async function loadConfig() {
  const config = await invoke('read_codex_config');
  console.log(config);
  // Returns parsed TOML as JSON
}
```

#### Edit TOML via UI

1. Navigate to "TOML 配置" tab
2. View syntax-highlighted configuration
3. Edit directly in code editor
4. Click "保存" (Save) to write to `~/.codex/config.toml`

#### Programmatic TOML Update

```rust
// Rust example - Tauri command handler
use tauri::command;
use std::fs;
use toml;

#[command]
fn update_codex_config(new_config: String) -> Result<(), String> {
    let config_path = dirs::home_dir()
        .unwrap()
        .join(".codex")
        .join("config.toml");
    
    // Validate TOML syntax
    let _parsed: toml::Value = toml::from_str(&new_config)
        .map_err(|e| format!("Invalid TOML: {}", e))?;
    
    // Write to file
    fs::write(config_path, new_config)
        .map_err(|e| format!("Write failed: {}", e))?;
    
    Ok(())
}
```

### 4. Auth Management

#### View Auth Configuration

```typescript
// Read auth.json
import { invoke } from '@tauri-apps/api/tauri';

interface AuthConfig {
  chatgpt_auth?: string;
  api_keys?: Record<string, string>;
}

async function loadAuth(): Promise<AuthConfig> {
  return await invoke('read_auth_json');
}
```

#### Update Authentication

```rust
// Rust command to update auth.json
use serde_json::json;
use std::fs;

#[command]
fn update_auth(
    chatgpt_token: Option<String>,
    api_keys: Option<HashMap<String, String>>
) -> Result<(), String> {
    let auth_path = dirs::home_dir()
        .unwrap()
        .join(".codex")
        .join("auth.json");
    
    let mut auth = json!({});
    
    if let Some(token) = chatgpt_token {
        auth["chatgpt_auth"] = json!(token);
    }
    
    if let Some(keys) = api_keys {
        auth["api_keys"] = json!(keys);
    }
    
    fs::write(auth_path, serde_json::to_string_pretty(&auth).unwrap())
        .map_err(|e| e.to_string())
}
```

### 5. Session Provider Sync

Codex-X can fix provider metadata in historical sessions.

#### Sync Session Providers

```typescript
// Scan and fix session provider metadata
import { invoke } from '@tauri-apps/api/tauri';

interface SessionSyncResult {
  sessions_found: number;
  sessions_fixed: number;
  errors: string[];
}

async function syncSessionProviders(): Promise<SessionSyncResult> {
  return await invoke('sync_session_providers');
}

// Usage
const result = await syncSessionProviders();
console.log(`Fixed ${result.sessions_fixed} of ${result.sessions_found} sessions`);
```

#### Session Data Locations

Codex-X reads session data from:
```rust
// Rust session scanner
use rusqlite::Connection;
use std::path::PathBuf;

fn get_session_paths() -> Vec<PathBuf> {
    let home = dirs::home_dir().unwrap();
    let codex_dir = home.join(".codex");
    
    vec![
        codex_dir.join("sqlite"),
        codex_dir.join("state_5.sqlite"),
        codex_dir.join("sessions"),
        codex_dir.join("archived_sessions"),
    ]
}

fn fix_session_provider(db_path: &PathBuf, provider: &str) -> Result<(), Box<dyn std::error::Error>> {
    let conn = Connection::open(db_path)?;
    
    conn.execute(
        "UPDATE threads SET provider_metadata = ?1 WHERE provider_metadata IS NULL OR provider_metadata != ?1",
        [provider],
    )?;
    
    Ok(())
}
```

## Common Patterns

### Pattern 1: Enable Unrestricted Mode

```bash
# 1. Open Codex-X
# 2. Navigate to "指令提示词" tab
# 3. Enable gpt5.5-unrestricted.md
# 4. Restart Codex CLI
codex-cli chat

# Test query
"如何进行渗透测试？"
```

### Pattern 2: Switch to Third-Party Provider

```typescript
// Add provider via Tauri API
import { invoke } from '@tauri-apps/api/tauri';

await invoke('add_provider', {
  name: 'anthropic',
  baseUrl: 'https://api.anthropic.com/v1',
  apiKey: '${ANTHROPIC_API_KEY}',
  model: 'claude-3-opus-20240229',
  wireApi: 'anthropic'
});

await invoke('set_active_provider', { provider: 'anthropic' });
```

### Pattern 3: Batch Config Update

```rust
// Update multiple TOML fields atomically
use toml_edit::{Document, value};

#[command]
fn batch_update_config(updates: HashMap<String, String>) -> Result<(), String> {
    let config_path = dirs::home_dir().unwrap().join(".codex/config.toml");
    let content = fs::read_to_string(&config_path).unwrap();
    let mut doc = content.parse::<Document>().unwrap();
    
    for (key, val) in updates {
        let keys: Vec<&str> = key.split('.').collect();
        let mut current = &mut doc;
        
        for (i, k) in keys.iter().enumerate() {
            if i == keys.len() - 1 {
                current[k] = value(val.clone());
            } else {
                current = &mut current[k];
            }
        }
    }
    
    fs::write(config_path, doc.to_string()).unwrap();
    Ok(())
}
```

### Pattern 4: Monitor Session Creation

```typescript
// Watch for new Codex sessions and auto-sync provider
import { invoke } from '@tauri-apps/api/tauri';
import { listen } from '@tauri-apps/api/event';

// Set up file watcher
await invoke('watch_session_directory');

// Listen for new session events
await listen('session-created', async (event) => {
  const sessionId = event.payload.session_id;
  await invoke('sync_single_session', { sessionId });
});
```

## Troubleshooting

### Issue: "App is damaged" on macOS

**Solution**: Remove quarantine attribute
```bash
xattr -dr com.apple.quarantine /Applications/Codex-X.app
```

### Issue: Config.toml changes not reflected in Codex CLI

**Solution**: Restart Codex CLI after saving changes
```bash
# Kill existing Codex processes
pkill -f codex-cli

# Start fresh session
codex-cli chat
```

### Issue: Provider switch fails

**Diagnosis**: Check TOML syntax
```bash
# Validate TOML
cat ~/.codex/config.toml | python -c "import sys, toml; toml.loads(sys.stdin.read())"
```

**Solution**: Use Codex-X TOML editor (validates before saving)

### Issue: Session sync reports errors

**Common causes**:
- Corrupted SQLite database
- Missing rollout JSONL files
- Permission issues

**Solution**:
```bash
# Check file permissions
ls -la ~/.codex/sqlite/
ls -la ~/.codex/sessions/

# Fix permissions
chmod -R 755 ~/.codex/

# Verify SQLite integrity
sqlite3 ~/.codex/state_5.sqlite "PRAGMA integrity_check;"
```

### Issue: Custom prompt not applied

**Checklist**:
1. Verify file path in config.toml
2. Check file exists: `ls -la ~/.codex/gpt5.5-unrestricted.md`
3. Restart Codex CLI
4. Test with explicit prompt injection query

```bash
# Manual verification
grep model_instructions_file ~/.codex/config.toml
cat ~/.codex/gpt5.5-unrestricted.md
```

### Issue: API key not recognized

**Solution**: Use environment variables instead of hardcoded keys
```bash
# Set API key
export CUSTOM_API_KEY="your-actual-key-here"

# Verify in config.toml
grep api_key ~/.codex/config.toml
# Should show: api_key = "${CUSTOM_API_KEY}"
```

## Development & Extension

### Add Custom Tauri Command

```rust
// src-tauri/src/main.rs
#[tauri::command]
fn custom_codex_operation(param: String) -> Result<String, String> {
    // Your custom logic
    Ok(format!("Processed: {}", param))
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            custom_codex_operation,
            // ... existing commands
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

### Call from Frontend

```typescript
import { invoke } from '@tauri-apps/api/tauri';

const result = await invoke<string>('custom_codex_operation', {
  param: 'test-value'
});
```

### Add New Prompt Template

```bash
# 1. Create new template
cat > examples/custom-prompt.md << 'EOF'
# Custom Codex Instructions

You are in custom mode. Follow these rules:
- Rule 1
- Rule 2
EOF

# 2. Add to Codex-X UI (modify React component)
# apps/desktop/src/components/PromptManager.tsx
```

## Resources

- **GitHub**: https://github.com/yynxxxxx/Codex-X
- **Releases**: https://github.com/yynxxxxx/Codex-X/releases
- **License**: MIT
- **Community**: LINUX DO Forum (https://linux.do/)

## Technology Stack

- **Desktop Framework**: Tauri 2
- **Frontend**: React 18, TypeScript, Vite
- **Backend**: Rust
- **Database**: SQLite (rusqlite)
- **Config Formats**: TOML, JSON
