---
name: codexmonitor-orchestration
description: Expert in CodexMonitor, a Tauri app for orchestrating multiple Codex agents across local workspaces with threads, git integration, and remote daemon support.
triggers:
  - how do I use CodexMonitor
  - set up CodexMonitor workspaces
  - manage Codex agent threads
  - CodexMonitor remote backend
  - build CodexMonitor from source
  - configure CodexMonitor iOS
  - CodexMonitor git integration
  - run CodexMonitor daemon
---

# CodexMonitor Orchestration Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

CodexMonitor is a Tauri-based desktop and mobile app for orchestrating multiple Codex agents across local workspaces. It provides workspace management, thread persistence, git/GitHub integration, file browsing, prompt libraries, and a remote daemon mode for connecting iOS clients or headless setups.

## What CodexMonitor Does

- **Multi-workspace orchestration**: Spawn one `codex app-server` per workspace, resume threads, track unread/running state
- **Thread management**: Pin, rename, archive, copy threads; per-thread drafts; stop/interrupt in-flight turns
- **Worktree agents**: Clone agents for isolated work under app data directory (legacy `.codex-worktrees` supported)
- **Git & GitHub**: Diff stats, staged/unstaged files, commit log, branch management, GitHub Issues/PRs via `gh`
- **Composer**: Image attachments, autocomplete for skills (`$`), prompts (`/prompts:`), reviews (`/review`), file paths (`@`)
- **Remote daemon**: Run Codex on another machine, connect iOS client via TCP (Tailscale support)
- **Prompt library**: Global/workspace prompts with create/edit/delete/move and run in threads
- **File tree**: Search, file-type icons, reveal in Finder/Explorer
- **Terminal dock**: Multiple tabs for background commands (experimental)

## Installation

### Requirements

- Node.js + npm
- Rust toolchain (stable)
- CMake (for native dependencies, dictation/Whisper)
- LLVM/Clang (Windows only, for bindgen)
- Codex CLI installed and in `PATH`
- Git CLI (for worktree operations)
- GitHub CLI `gh` (optional, for GitHub integrations)

### Install Dependencies

```bash
npm install
```

### Check Environment

```bash
npm run doctor
```

### Run in Development

```bash
npm run tauri:dev
```

### Build Production Bundle

```bash
# macOS/Linux
npm run tauri:build

# Windows (opt-in, uses separate config)
npm run tauri:build:win
```

Artifacts: `src-tauri/target/release/bundle/` (platform-specific subfolders)

## Workspace Management

### Adding a Workspace

Workspaces persist to `workspaces.json` in app data directory.

**Via UI**: Sidebar → Add workspace → Select directory

**Data structure** (`src-tauri/src/workspaces/mod.rs`):

```rust
#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Workspace {
    pub id: String,
    pub name: String,
    pub path: String,
    pub codex_home: Option<String>, // Overrides global Codex home
    pub is_remote: bool,
    pub remote_host: Option<String>,
    pub remote_token: Option<String>,
}
```

### Programmatic Workspace Access

Frontend service (`src/services/tauri.ts`):

```typescript
import { invoke } from '@tauri-apps/api/tauri';

// Load all workspaces
const workspaces = await invoke<Workspace[]>('workspace_list');

// Add workspace
const newWorkspace = await invoke<Workspace>('workspace_add', {
  path: '/path/to/project',
  name: 'My Project',
});

// Update workspace
await invoke('workspace_update', {
  id: 'workspace-id',
  updates: { codex_home: '/custom/codex/home' },
});

// Remove workspace
await invoke('workspace_remove', { id: 'workspace-id' });
```

Backend command (`src-tauri/src/lib.rs`):

```rust
#[tauri::command]
async fn workspace_list(
    state: tauri::State<'_, AppState>,
) -> Result<Vec<Workspace>, String> {
    state.workspace_manager.lock().await.list_workspaces()
        .map_err(|e| e.to_string())
}
```

## Thread Management

### Thread Reducer Architecture

Thread state is managed by a reducer with slices in `src/features/threads/hooks/threadReducer/`.

**Thread reducer pattern** (`src/features/threads/hooks/threadReducer/index.ts`):

```typescript
export type ThreadAction =
  | { type: 'SET_MESSAGES'; messages: Message[] }
  | { type: 'ADD_MESSAGE'; message: Message }
  | { type: 'UPDATE_MESSAGE'; messageId: string; updates: Partial<Message> }
  | { type: 'SET_RUNNING'; running: boolean }
  | { type: 'SET_UNREAD'; unread: number }
  | { type: 'RESET' };

export function threadReducer(state: ThreadState, action: ThreadAction): ThreadState {
  switch (action.type) {
    case 'SET_MESSAGES':
      return { ...state, messages: action.messages };
    case 'ADD_MESSAGE':
      return { ...state, messages: [...state.messages, action.message] };
    case 'UPDATE_MESSAGE':
      return {
        ...state,
        messages: state.messages.map(m =>
          m.id === action.messageId ? { ...m, ...action.updates } : m
        ),
      };
    case 'SET_RUNNING':
      return { ...state, running: action.running };
    case 'RESET':
      return initialThreadState;
    default:
      return state;
  }
}
```

### Resuming a Thread

Frontend (`src/features/threads/hooks/useThreadResume.ts`):

```typescript
import { invoke } from '@tauri-apps/api/tauri';

async function resumeThread(workspaceId: string, threadId: string) {
  const result = await invoke<{ messages: Message[] }>('thread_resume', {
    workspaceId,
    threadId,
  });
  
  dispatch({ type: 'SET_MESSAGES', messages: result.messages });
  dispatch({ type: 'SET_UNREAD', unread: 0 });
}
```

Backend (`src-tauri/src/codex/mod.rs`):

```rust
#[tauri::command]
async fn thread_resume(
    workspace_id: String,
    thread_id: String,
    state: tauri::State<'_, AppState>,
) -> Result<serde_json::Value, String> {
    let manager = state.workspace_manager.lock().await;
    let workspace = manager.get_workspace(&workspace_id)
        .ok_or("Workspace not found")?;
    
    let server = state.codex_servers.lock().await
        .get(&workspace_id)
        .ok_or("Server not running")?;
    
    server.call("thread/resume", json!({ "thread_id": thread_id })).await
        .map_err(|e| e.to_string())
}
```

### Sending a Message

```typescript
async function sendMessage(
  workspaceId: string,
  threadId: string,
  content: string,
  attachments?: { path: string; mime_type: string }[]
) {
  await invoke('thread_send_message', {
    workspaceId,
    threadId,
    message: {
      role: 'user',
      content,
      attachments,
    },
  });
}
```

### Thread Lifecycle Commands

```typescript
// Stop in-flight turn
await invoke('thread_interrupt', { workspaceId, threadId });

// Pin thread
await invoke('thread_pin', { workspaceId, threadId, pinned: true });

// Rename thread
await invoke('thread_rename', { workspaceId, threadId, name: 'New Name' });

// Archive thread
await invoke('thread_archive', { workspaceId, threadId });

// Copy thread (clone messages)
await invoke('thread_copy', { workspaceId, threadId });
```

## Worktree Agents

Worktree agents create isolated git worktrees under `<app-data>/worktrees/<workspace-id>/`.

### Creating a Worktree

Frontend:

```typescript
const worktree = await invoke<{ path: string; branch: string }>('worktree_create', {
  workspaceId: 'workspace-id',
  branch: 'feature-branch',
});

console.log(`Worktree created at ${worktree.path}`);
```

Backend (`src-tauri/src/shared/workspaces_core/worktree.rs`):

```rust
pub async fn create_worktree(
    workspace_path: &str,
    workspace_id: &str,
    branch: &str,
    app_data_dir: &Path,
) -> Result<Worktree, WorktreeError> {
    let worktree_dir = app_data_dir.join("worktrees").join(workspace_id);
    std::fs::create_dir_all(&worktree_dir)?;
    
    let worktree_path = worktree_dir.join(branch);
    
    let output = Command::new("git")
        .args(&["worktree", "add", worktree_path.to_str().unwrap(), branch])
        .current_dir(workspace_path)
        .output()?;
    
    if !output.status.success() {
        return Err(WorktreeError::GitError(
            String::from_utf8_lossy(&output.stderr).to_string()
        ));
    }
    
    Ok(Worktree {
        path: worktree_path.to_string_lossy().to_string(),
        branch: branch.to_string(),
    })
}
```

### Listing Worktrees

```typescript
const worktrees = await invoke<Worktree[]>('worktree_list', {
  workspaceId: 'workspace-id',
});
```

### Removing a Worktree

```typescript
await invoke('worktree_remove', {
  workspaceId: 'workspace-id',
  path: '/path/to/worktree',
});
```

## Git Integration

### Git Diff Stats

Frontend:

```typescript
const stats = await invoke<{
  staged: { path: string; status: string }[];
  unstaged: { path: string; status: string }[];
}>('git_diff_stats', { workspaceId: 'workspace-id' });
```

Backend (`src-tauri/src/shared/git_ui_core/diff.rs`):

```rust
pub fn get_diff_stats(repo_path: &str) -> Result<DiffStats, GitError> {
    let repo = Repository::open(repo_path)?;
    let mut index = repo.index()?;
    
    let head_tree = repo.head()?.peel_to_tree()?;
    let diff_index_tree = repo.diff_tree_to_index(Some(&head_tree), Some(&index), None)?;
    let diff_index_workdir = repo.diff_index_to_workdir(Some(&index), None)?;
    
    let staged = collect_diff_entries(&diff_index_tree)?;
    let unstaged = collect_diff_entries(&diff_index_workdir)?;
    
    Ok(DiffStats { staged, unstaged })
}
```

### Branch Management

```typescript
// List branches
const branches = await invoke<{ name: string; current: boolean; ahead: number; behind: number }[]>(
  'git_list_branches',
  { workspaceId: 'workspace-id' }
);

// Checkout branch
await invoke('git_checkout_branch', {
  workspaceId: 'workspace-id',
  branch: 'main',
});

// Create branch
await invoke('git_create_branch', {
  workspaceId: 'workspace-id',
  branch: 'feature-new',
  fromBranch: 'main',
});
```

### GitHub Integration

Requires `gh` CLI:

```typescript
// List issues
const issues = await invoke<GitHubIssue[]>('github_list_issues', {
  workspaceId: 'workspace-id',
});

// List PRs
const prs = await invoke<GitHubPR[]>('github_list_prs', {
  workspaceId: 'workspace-id',
});

// Get PR diff
const diff = await invoke<string>('github_pr_diff', {
  workspaceId: 'workspace-id',
  prNumber: 42,
});

// Ask PR (send PR context to new thread)
await invoke('github_ask_pr', {
  workspaceId: 'workspace-id',
  prNumber: 42,
  question: 'What does this PR change?',
});
```

Backend (`src-tauri/src/shared/git_ui_core/github.rs`):

```rust
pub async fn list_prs(repo_path: &str) -> Result<Vec<GitHubPR>, GitHubError> {
    let output = Command::new("gh")
        .args(&["pr", "list", "--json", "number,title,author,state"])
        .current_dir(repo_path)
        .output()
        .await?;
    
    if !output.status.success() {
        return Err(GitHubError::CliError(
            String::from_utf8_lossy(&output.stderr).to_string()
        ));
    }
    
    Ok(serde_json::from_slice(&output.stdout)?)
}
```

## Remote Daemon Mode

Remote daemon mode allows running Codex on a separate machine (e.g., desktop) and connecting from iOS or other clients.

### Desktop Daemon Setup

**Via UI**:
1. Settings → Server
2. Set `Remote backend token` (shared secret)
3. Click `Start daemon` in `Mobile access daemon`

**Standalone Daemon CLI**:

```bash
# Build daemon binaries
cd src-tauri
cargo build --bin codex_monitor_daemon --bin codex_monitor_daemonctl

# Start daemon (reads settings.json from app data dir)
./target/debug/codex_monitor_daemonctl start

# Status
./target/debug/codex_monitor_daemonctl status

# Stop
./target/debug/codex_monitor_daemonctl stop

# Override settings
./target/debug/codex_monitor_daemonctl start \
  --listen 0.0.0.0:4732 \
  --token $REMOTE_TOKEN \
  --data-dir /path/to/app/data
```

### Daemon RPC Architecture

Daemon entrypoint (`src-tauri/src/bin/codex_monitor_daemon.rs`):

```rust
#[tokio::main]
async fn main() -> Result<()> {
    let listener = TcpListener::bind(&args.listen).await?;
    let shared_state = Arc::new(DaemonState::new(app_data_dir, codex_path)?);
    
    loop {
        let (socket, _) = listener.accept().await?;
        let state = shared_state.clone();
        tokio::spawn(handle_connection(socket, state));
    }
}

async fn handle_connection(socket: TcpStream, state: Arc<DaemonState>) {
    let (reader, writer) = socket.into_split();
    let reader = BufReader::new(reader);
    let mut writer = BufWriter::new(writer);
    
    let mut lines = reader.lines();
    while let Some(line) = lines.next_line().await? {
        let request: JsonRpcRequest = serde_json::from_str(&line)?;
        let response = handle_rpc_request(request, &state).await;
        writer.write_all(serde_json::to_string(&response)?.as_bytes()).await?;
        writer.write_all(b"\n").await?;
        writer.flush().await?;
    }
}
```

RPC routing (`src-tauri/src/bin/codex_monitor_daemon/rpc.rs`):

```rust
pub async fn handle_rpc_request(
    request: JsonRpcRequest,
    state: &DaemonState,
) -> JsonRpcResponse {
    match request.method.as_str() {
        "workspace/list" => workspace_list(state).await,
        "workspace/add" => workspace_add(request.params, state).await,
        "thread/list" => thread_list(request.params, state).await,
        "thread/resume" => thread_resume(request.params, state).await,
        "thread/send" => thread_send(request.params, state).await,
        "git/diff_stats" => git_diff_stats(request.params, state).await,
        _ => JsonRpcResponse::error(-32601, "Method not found"),
    }
}
```

### iOS Client Connection (Tailscale)

**Desktop (Tailscale helper)**:
1. Settings → Server → Tailscale helper
2. Click `Detect Tailscale` → note suggested host (e.g., `your-mac.your-tailnet.ts.net:4732`)

**iOS**:
1. Settings → Server
2. Enter desktop Tailscale host and matching token
3. Tap `Connect & test`

Frontend client (`src/services/remoteDaemon.ts`):

```typescript
class RemoteDaemonClient {
  private socket: WebSocket | null = null;
  private requestId = 0;
  
  async connect(host: string, token: string): Promise<void> {
    this.socket = new WebSocket(`ws://${host}`);
    
    await new Promise((resolve, reject) => {
      this.socket!.onopen = () => {
        this.send('auth', { token }).then(resolve).catch(reject);
      };
      this.socket!.onerror = reject;
    });
  }
  
  async send(method: string, params: any): Promise<any> {
    const id = ++this.requestId;
    const request = { jsonrpc: '2.0', id, method, params };
    
    return new Promise((resolve, reject) => {
      const handler = (event: MessageEvent) => {
        const response = JSON.parse(event.data);
        if (response.id === id) {
          this.socket!.removeEventListener('message', handler);
          if (response.error) {
            reject(new Error(response.error.message));
          } else {
            resolve(response.result);
          }
        }
      };
      
      this.socket!.addEventListener('message', handler);
      this.socket!.send(JSON.stringify(request));
    });
  }
}
```

## Composer & Autocomplete

### Autocomplete Triggers

- `$` — skills
- `/prompts:` — prompts
- `/review` — code review
- `@` — file paths

Frontend autocomplete hook (`src/features/composer/hooks/useAutocomplete.ts`):

```typescript
export function useAutocomplete(value: string, cursorPosition: number) {
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  
  useEffect(() => {
    const prefix = value.slice(0, cursorPosition);
    
    if (prefix.endsWith('$')) {
      // Fetch skills
      invoke<string[]>('autocomplete_skills', { prefix }).then(setSuggestions);
    } else if (prefix.includes('/prompts:')) {
      // Fetch prompts
      invoke<Prompt[]>('autocomplete_prompts', { prefix }).then(setSuggestions);
    } else if (prefix.endsWith('@')) {
      // Fetch file paths
      invoke<string[]>('autocomplete_files', {
        workspaceId,
        prefix,
      }).then(setSuggestions);
    } else {
      setSuggestions([]);
    }
  }, [value, cursorPosition]);
  
  return suggestions;
}
```

### Follow-up Behavior

Settings → Composer → Follow-up default:
- `Queue` — queue messages if agent is running
- `Steer` — interrupt current turn and steer

Override for single message:
- macOS: `Shift+Cmd+Enter`
- Windows/Linux: `Shift+Ctrl+Enter`

## Prompt Library

Prompts load from `$CODEX_HOME/prompts` (or `~/.codex/prompts`).

### Prompt File Format

```markdown
---
description: Generate unit tests for a function
args:
  - name: function_name
    description: Name of the function to test
---

Generate comprehensive unit tests for the function `{{function_name}}`, covering edge cases and error handling.
```

### Managing Prompts

```typescript
// List prompts
const prompts = await invoke<Prompt[]>('prompt_list', { workspaceId });

// Create prompt
await invoke('prompt_create', {
  workspaceId,
  name: 'generate-tests',
  content: '...',
  isGlobal: false, // workspace-specific
});

// Run prompt in current thread
await invoke('prompt_run', {
  workspaceId,
  threadId,
  promptId: 'generate-tests',
  args: { function_name: 'calculateTotal' },
});

// Run prompt in new thread
await invoke('prompt_run_new_thread', {
  workspaceId,
  promptId: 'generate-tests',
  args: { function_name: 'calculateTotal' },
});
```

## Configuration

### App Settings

Persisted to `settings.json` in app data directory.

```typescript
interface AppSettings {
  theme: 'light' | 'dark' | 'system';
  backend_mode: 'local' | 'remote';
  remote_provider?: 'tcp' | 'ws';
  remote_tcp_host?: string;
  remote_tcp_token?: string;
  codex_path?: string; // Custom Codex binary path
  default_access_mode?: 'default' | 'direct' | 'tool_only';
  ui_scale?: number;
  follow_up_behavior?: 'queue' | 'steer';
  reduced_transparency?: boolean;
}

// Get settings
const settings = await invoke<AppSettings>('get_app_settings');

// Update settings
await invoke('update_app_settings', {
  updates: { theme: 'dark', ui_scale: 1.2 },
});
```

### Codex Config

Feature settings sync to `$CODEX_HOME/config.toml`:

```toml
[features]
collaboration_modes = true
unified_exec = true  # Background terminal
apps = false  # Experimental

[personality]
tone = "professional"
```

Load/save via:

```typescript
const config = await invoke<CodexConfig>('get_codex_config_path');

await invoke('codex_doctor'); // Validate Codex setup
```

## iOS Development

### Build for Simulator

```bash
./scripts/build_run_ios.sh
# Options: --simulator "<name>", --target aarch64-sim|x86_64-sim, --skip-build, --no-clean
```

### Build for USB Device

```bash
# List devices
./scripts/build_run_ios_device.sh --list-devices

# Build and run
./scripts/build_run_ios_device.sh --device "<device name>" --team <TEAM_ID>
# Options: --target aarch64, --skip-build, --bundle-id <id>
```

### Signing Configuration

Preferred: `src-tauri/tauri.ios.local.conf.json` (gitignored):

```json
{
  "bundle": {
    "iOS": {
      "developmentTeam": "YOUR_TEAM_ID"
    }
  },
  "identifier": "com.yourcompany.codexmonitor"
}
```

### TestFlight Release

```bash
# Copy .testflight.local.env.example to .testflight.local.env and fill values
./scripts/release_testflight_ios.sh
```

Required env vars in `.testflight.local.env`:

```bash
IOS_TEAM_ID=YOUR_TEAM_ID
BUNDLE_ID=com.yourcompany.codexmonitor
TESTFLIGHT_BETA_GROUP="Beta Testers"
APPLE_ID=your-apple-id@example.com
APP_STORE_CONNECT_TEAM_ID=YOUR_ASC_TEAM_ID
```

## Terminal Dock

Experimental feature for background commands.

```typescript
// Execute command in terminal tab
await invoke('terminal_exec', {
  workspaceId,
  tabId: 'tab-1',
  command: 'npm test',
});

// Create new terminal tab
await invoke('terminal_create_tab', { workspaceId, name: 'Tests' });

// Close terminal tab
await invoke('terminal_close_tab', { workspaceId, tabId: 'tab-1' });
```

## Troubleshooting

### Native Build Errors

```bash
npm run doctor
```

Common issues:
- **CMake not found**: Install CMake
- **bindgen errors (Windows)**: Install LLVM/Clang
- **Rust targets missing (iOS)**: `rustup target add aarch64-apple-ios aarch64-apple-ios-sim`

### Codex Not Found

Set custom Codex path in Settings → General → Codex binary path, or ensure `codex` is in `PATH`.

### Remote Daemon Connection Fails

1. Confirm daemon is running: `./target/debug/codex_monitor_daemonctl status`
2. Check token matches between desktop and client
3. Verify host/port reachable (Tailscale: both devices online in same tailnet)
4. Check firewall rules for listening port (default 4732)

### Thread Resume Shows Stale Messages

Threads are restored from disk via `thread/resume`. If messages are stale:
1. Ensure workspace `cwd` matches thread working directory
2. Restart workspace server: Remove and re-add workspace

### Worktree Creation Fails

Ensure workspace is a git repository:

```bash
cd /path/to/workspace
git status
```

Legacy worktrees under `.codex-worktrees/` are supported but new ones use `<app-data>/worktrees/<workspace-id>/`.

### iOS Signing Issues

First-time device setup:
1. iPhone unlocked and trusted with Mac
2. Developer Mode enabled on iPhone (Settings → Privacy & Security → Developer Mode)
3. Open Xcode via `./scripts/build_run_ios_device.sh --open-xcode` and approve signing

## File Structure Reference

```
src/
  features/app/bootstrap/         App bootstrap orchestration
  features/app/orchestration/     Layout/thread/workspace orchestration
  features/threads/hooks/threadReducer/  Thread reducer slices
  features/composer/              Composer UI and autocomplete
  features/git/                   Git UI components
  features/prompts/               Prompt library UI
  services/tauri.ts               Tauri IPC wrapper
  types.ts                        Shared TypeScript types

src-tauri/
  src/lib.rs                      Tauri command registry
  src/bin/codex_monitor_daemon.rs Remote daemon entrypoint
  src/bin/codex_monitor_daemon/rpc/ Daemon RPC handlers
  src/shared/git_ui_core/         Git/GitHub core
  src/shared/workspaces_core/     Workspace/worktree core
  src/workspaces/                 Workspace adapters
  src/codex/                      Codex app-server adapters
  src/files/                      File adapters
```

## Resources

- **Homepage**: https://www.codexmonitor.app
- **Repository**: https://github.com/Dimillian/CodexMonitor
- **License**: MIT
- **Codebase Map**: `docs/codebase-map.md` (task-oriented file lookup)
- **iOS Tailscale Blueprint**: `docs/mobile-ios-tailscale-blueprint.md`
