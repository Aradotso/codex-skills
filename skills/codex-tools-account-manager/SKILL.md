---
name: codex-tools-account-manager
description: Desktop tool for managing multiple Codex accounts, monitoring usage, and providing local API proxy with public access
triggers:
  - "manage my Codex accounts"
  - "switch between Codex accounts"
  - "set up Codex API proxy"
  - "monitor Codex usage limits"
  - "create local Codex API endpoint"
  - "expose Codex API to public network"
  - "import Codex account tokens"
  - "configure Cursor with Codex proxy"
---

# Codex Tools Account Manager

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

**codex-tools** is a React + Tauri desktop application for managing multiple Codex accounts, monitoring usage quotas (5h/1week windows), and providing a local OpenAI-compatible API proxy. It supports account switching, automatic usage tracking, and public network exposure via cloudflared.

**Primary use cases:**
- Manage multiple Codex accounts and switch between them
- Monitor usage limits and intelligently select accounts with remaining quota
- Run a local `/v1` API proxy that routes requests through Codex accounts
- Expose the proxy to the internet for tools like Cursor that block private IPs
- Automatically restart editors and sync OpenAI tokens after account switching

## Installation

### macOS

Download the latest `.dmg` from [releases](https://github.com/170-carry/codex-tools/releases):

```bash
# If you get "app is damaged" error:
sudo spctl --master-disable
sudo xattr -r -d com.apple.quarantine /Applications/Codex\ Tools.app
```

### Windows

Download the `.msi` or `.exe` installer from releases.

### From Source

Requirements: Node.js 20+, Rust stable

```bash
git clone https://github.com/170-carry/codex-tools.git
cd codex-tools
npm install
npm run tauri dev
```

Build production:

```bash
npm run tauri build
```

## Account Management

### Import Accounts

**Method 1: OAuth Login**
- Click the OAuth login button in the UI
- Follow the authentication flow
- Account token is automatically imported

**Method 2: Upload JSON Files**

Import single or multiple `.json` token files:

```json
{
  "access_token": "your_access_token_here",
  "refresh_token": "your_refresh_token_here",
  "expires_at": 1234567890
}
```

**Method 3: Import from Directory**

Point the app to a folder containing multiple `.json` token files. All valid tokens will be imported in batch.

**Method 4: Restore Backup**

Import a previously exported `accounts.json` backup file.

> **Note:** After import, the app restores your current logged-in account to avoid disrupting your active session.

### Export Accounts

Export all accounts as `accounts.json` for backup:

```json
{
  "accounts": [
    {
      "id": "account_id_1",
      "access_token": "token1",
      "refresh_token": "refresh1",
      "plan_type": "Pro",
      "usage_5h": 450,
      "usage_1week": 2000
    }
  ]
}
```

### View Usage

The UI displays:
- **5h window**: Requests used in the last 5 hours
- **1week window**: Requests used in the last 7 days
- **Plan type**: Free/Pro/Business
- **Last refresh**: Timestamp of last usage check

Click "Refresh" to manually update, or wait for automatic refresh (default: every 5 minutes).

### Switch Accounts

1. Select an account from the list
2. Click "Switch & Launch Codex"
3. The app will:
   - Write the new token to the local Codex config
   - Launch the Codex desktop app (or fallback to `codex app` CLI)
   - Optionally sync the OpenAI token to Opencode
   - Optionally restart your selected editor (VS Code, Cursor, etc.)

**Smart Switch:**
Click "Smart Switch" to automatically select the account with the most remaining quota in the current window.

## API Proxy

The proxy provides an OpenAI-compatible `/v1` endpoint backed by Codex accounts.

### Start the Proxy

**UI:**
- Navigate to "API Proxy" tab
- Click "Start Proxy"
- The proxy starts on `http://127.0.0.1:8787/v1` (default)

**Auto-start:**
Enable "Start proxy on app launch" in settings.

### Configuration

**Port:**
- Default: `8787`
- Custom: Set in the settings panel

**API Key:**
- Fixed key: Set a static key in settings
- Manual refresh: Click "Refresh API Key" to generate a new random key
- The key is used for Bearer token authentication

**Account Selection:**
The proxy automatically selects the account with the most remaining quota when handling requests.

### Usage Example

```bash
# Test the proxy
curl http://127.0.0.1:8787/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -d '{
    "model": "gpt-5.4",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

```python
import openai

openai.api_base = "http://127.0.0.1:8787/v1"
openai.api_key = "YOUR_API_KEY"

response = openai.ChatCompletion.create(
    model="gpt-5.4",
    messages=[{"role": "user", "content": "Write a hello world in Rust"}]
)
print(response.choices[0].message.content)
```

```javascript
import OpenAI from "openai";

const client = new OpenAI({
  baseURL: "http://127.0.0.1:8787/v1",
  apiKey: process.env.CODEX_PROXY_KEY,
});

const completion = await client.chat.completions.create({
  model: "gpt-5.4",
  messages: [{ role: "user", content: "Explain async/await in JS" }],
});

console.log(completion.choices[0].message.content);
```

### Supported Models

- `gpt-5.4` (recommended)
- `gpt-5-4` (alias)

Add custom models in Cursor: Settings → Models → Add or search model

## Cursor Integration

Cursor blocks private IP addresses (`127.0.0.1`, `localhost`, `192.168.x.x`, `10.x.x.x`) when used as OpenAI base URLs.

### Solution: Use Public URL

**Option 1: Cloudflared (Built-in)**

1. Navigate to "Public Access" tab
2. Click "Start Cloudflared"
3. Copy the generated public URL (e.g., `https://abc123.trycloudflare.com`)
4. In Cursor:
   - Settings → Models
   - Enable "OpenAI API Key", paste your proxy API key
   - Enable "Override OpenAI Base URL", paste `https://abc123.trycloudflare.com/v1`
   - Add custom model `gpt-5.4`

**Option 2: Named Tunnel**

Configure a named cloudflared tunnel for a persistent URL:

```yaml
# cloudflared config.yml
tunnel: your-tunnel-id
credentials-file: /path/to/credentials.json

ingress:
  - hostname: codex.yourdomain.com
    service: http://127.0.0.1:8787
  - service: http_status:404
```

**Option 3: Remote Reverse Proxy**

Deploy a reverse proxy on a public server:

```nginx
# nginx.conf
server {
    listen 443 ssl;
    server_name codex.yourdomain.com;

    location /v1 {
        proxy_pass http://your-local-ip:8787/v1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Cursor Configuration

1. Open Cursor → Settings → Models
2. Enable "OpenAI API Key", enter your proxy API key
3. Enable "Override OpenAI Base URL", enter your public URL with `/v1`
4. In "Add or search model", type `gpt-5.4` and click "Add Custom Model"
5. Test by asking a question in Cursor chat

## Cloudflared Public Access

### Quick Tunnel

No configuration required. Generates a random `.trycloudflare.com` URL:

1. Click "Start Quick Tunnel"
2. URL appears in the UI (e.g., `https://random-words-123.trycloudflare.com`)
3. Share this URL or use in Cursor

### Named Tunnel

Requires a Cloudflare account and tunnel setup:

1. Create a tunnel at [Cloudflare Zero Trust](https://one.dash.cloudflare.com/)
2. Download credentials JSON
3. In codex-tools: Settings → Cloudflared → Named Tunnel
4. Upload credentials and configure hostname
5. Click "Start Named Tunnel"

### HTTP/2 Support

Enable HTTP/2 in settings for better performance with streaming responses.

## Editor Integration

### Restart Editor After Switch

Enable in Settings → Editor:
- VS Code
- Cursor
- Other (specify process name)

When you switch accounts, the app will:
1. Kill the editor process
2. Wait 2 seconds
3. Restart the editor

### Sync OpenAI Token to Opencode

Enable in Settings → Integrations:
- Automatically sync the Codex OpenAI token to Opencode config
- Useful if you use both tools in parallel

## CC Switch Integration

codex-tools can act as a custom provider for [CC Switch](https://github.com/codex-cpp/cc-switch):

```json
{
  "providers": [
    {
      "name": "codex-local",
      "type": "custom",
      "base_url": "http://127.0.0.1:8787/v1",
      "api_key": "${CODEX_PROXY_KEY}",
      "protocol": "responses"
    }
  ]
}
```

The proxy follows the `responses` protocol for account selection and load balancing.

## Troubleshooting

### "App is Damaged" on macOS

```bash
sudo spctl --master-disable
sudo xattr -r -d com.apple.quarantine /Applications/Codex\ Tools.app
```

### Cursor Shows `ssrf_blocked` Error

This means Cursor is blocking private IPs. Use a public URL via cloudflared or a reverse proxy (see "Cursor Integration").

### Proxy Not Starting

- Check if port `8787` is already in use: `lsof -i :8787`
- Try a different port in settings
- Ensure you have at least one valid account imported

### Account Import Fails

- Verify JSON structure matches the expected format
- Check token expiry: `expires_at` should be in the future
- Re-authenticate via OAuth if refresh token is expired

### Usage Not Updating

- Click "Refresh" manually
- Check network connectivity
- Verify account tokens are still valid (re-login if needed)

### Cloudflared Tunnel Fails

- Ensure `cloudflared` binary is installed and accessible
- For named tunnels, verify credentials file path
- Check Cloudflare dashboard for tunnel status

### Editor Not Restarting

- Verify the editor process name in settings matches the actual process
- On macOS, grant codex-tools accessibility permissions if needed
- Try manually killing and restarting the editor

## Configuration Files

### Account Storage

Accounts are stored in the Tauri app data directory:

- macOS: `~/Library/Application Support/com.codex-tools.app/`
- Windows: `%APPDATA%/com.codex-tools.app/`
- Linux: `~/.local/share/com.codex-tools.app/`

### Settings

Settings are persisted in the same directory as `settings.json`:

```json
{
  "proxy_port": 8787,
  "api_key": "your-static-key",
  "auto_start_proxy": true,
  "editor": "cursor",
  "restart_editor_on_switch": true,
  "sync_opencode": false,
  "cloudflared_http2": true,
  "language": "en"
}
```

## Development

### Project Structure

```
codex-tools/
├── src/               # React frontend
│   ├── components/    # UI components
│   ├── hooks/         # React hooks
│   └── lib/           # Utilities
├── src-tauri/         # Rust backend
│   ├── src/
│   │   ├── main.rs    # Entry point
│   │   ├── proxy.rs   # API proxy logic
│   │   ├── accounts.rs # Account management
│   │   └── cloudflared.rs # Cloudflared integration
│   └── Cargo.toml
└── package.json
```

### Adding a New Feature

1. Define Tauri command in `src-tauri/src/main.rs`:

```rust
#[tauri::command]
async fn my_new_feature(param: String) -> Result<String, String> {
    // Implementation
    Ok(format!("Processed: {}", param))
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![my_new_feature])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
```

2. Call from React frontend:

```typescript
import { invoke } from "@tauri-apps/api/tauri";

const result = await invoke<string>("my_new_feature", { param: "test" });
console.log(result);
```

### Running Tests

```bash
# Rust tests
cd src-tauri
cargo test

# Frontend tests (if configured)
npm test
```

## Release Process

Releases are automated via GitHub Actions. To trigger a release:

```bash
git tag v0.2.0
git push origin v0.2.0
```

Builds for macOS (Intel + ARM) and Windows will be created automatically.

## License

MIT License. See [LICENSE](https://github.com/170-carry/codex-tools/blob/main/LICENSE).
