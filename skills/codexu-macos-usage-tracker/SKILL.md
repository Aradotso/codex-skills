---
name: codexu-macos-usage-tracker
description: macOS menu bar app for tracking OpenAI Codex and Claude Code quota, token usage, and task management with local-first analytics
triggers:
  - how do I install and configure codexU on macOS
  - show me codexU usage tracking and quota monitoring
  - integrate codexU with Codex or Claude Code on my Mac
  - customize codexU menu bar display and settings
  - build and package codexU from source
  - troubleshoot codexU quota display or token statistics
  - use codexU API to access local Codex usage data
  - configure codexU status bar widgets and shortcuts
---

# codexU macOS Usage Tracker

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

codexU is a native macOS menu bar and desktop application for monitoring OpenAI Codex / ChatGPT Codex and Claude Code usage. It provides real-time quota tracking (5-hour and 7-day windows), token usage analytics, project rankings, skill/tool usage stats, and a today task board. All data is read locally from `~/.codex/` and `~/.claude/` without uploading to third-party services.

## What codexU Does

- **Quota Monitoring**: Displays 5-hour and 7-day quota remaining/used percentages with reset timers in the menu bar
- **Token Analytics**: Tracks uncached input, cached input, and output tokens with API cost equivalency estimates
- **Task Board**: Generates today's task board from local Codex threads and enabled automations
- **Usage Trends**: Shows 6-month daily token heatmap and 7-day trend summaries
- **Project Rankings**: Lists top projects by token usage, estimated value, thread count, and last activity
- **Skill/Tool Stats**: Displays most-used tools and skills from local session events
- **Dual Runtime**: Supports both Codex and Claude Code with global runtime switching
- **Local-First**: All data parsed from local SQLite and JSONL files, no external API calls for usage

## Installation

### From GitHub Release (Recommended)

1. Download the correct DMG for your Mac architecture from [GitHub Releases](https://github.com/shanggqm/codexU/releases/latest):
   - Apple Silicon: `codexU-<version>-mac-arm64.dmg`
   - Intel: `codexU-<version>-mac-x86_64.dmg`

2. Open the DMG and drag `codexU.app` to `/Applications`

3. First launch requires manual security approval:
   ```bash
   # Open the app once (will be blocked)
   open /Applications/codexU.app
   
   # Then go to System Settings > Privacy & Security > Security
   # Click "Open Anyway" next to codexU.app
   # Confirm with Touch ID or password
   ```

4. Grant file access when prompted:
   - codexU needs read access to `~/.codex/` for Codex data
   - If using Claude Code tracking, also needs `~/.claude/` access

### From Source

**Requirements:**
- macOS 14+
- Xcode Command Line Tools
- Codex installed and logged in

```bash
# Clone the repository
git clone https://github.com/shanggqm/codexU.git
cd codexU

# Build the app
make build

# Run directly
make run

# Install to /Applications
make install

# Check local data sources
make probe
```

## Key Commands and Usage

### Menu Bar Interactions

```swift
// Click menu bar icon → Opens Runtime menu with quick stats
// Shows Codex or Claude Code card with:
// - 5-hour and 7-day remaining quota
// - Today's token usage
// - Total token usage
// Click card → Opens main window switched to that runtime
```

### Keyboard Shortcuts

- **`Command + U`**: Toggle main window visibility (customizable in Settings)
- **Esc** (during shortcut recording): Cancel
- **Backspace** (during shortcut recording): Clear

### Main Window Views

1. **Today Tasks**: In-progress, pending, scheduled, and completed tasks from local threads
2. **Usage Trends**: Daily token heatmap (6 months) + 7-day trend summary
3. **Project Rankings**: Top projects by token, value, threads, last active
4. **Skill Usage**: Top tool calls and skill usage from local sessions

### Settings Window

Access via menu bar Runtime menu → "Open Settings" or `codexU` app menu:

- **General**: Language (中文/English), appearance (auto/light/dark)
- **Status Bar**: Display mode (minimal/classic/rich), quota metric (used/remaining), visible indicators (5h/7d/today tokens/reset countdown)
- **Window**: Keep main window on top, close behavior (hide/quit)
- **System**: Auto-update check, check for beta versions, view status, manual update check

## Configuration and Data Sources

### Data Sources

codexU reads from local files only:

**Codex:**
```
~/.codex/state_5.sqlite          # Account, quotas, token totals
~/.codex/sessions/**/rollout-*.jsonl  # Fine-grained token events
~/.codex/archived_sessions/*.jsonl    # Archived session events
~/.codex/automations/**/automation.toml  # Enabled automations
```

**Claude Code:**
```
~/.claude/projects/**/*.jsonl    # Transcript usage data
~/.claude/tasks/**/*.json        # Task definitions
~/Library/Caches/codexU/claude-code/statusline-snapshot.json  # Optional quota cache
```

### Status Bar Customization

The status bar supports three display modes with adaptive single/dual ring layouts:

**Minimal Mode:**
- Bold quota ring only
- Adapts to single ring when only one quota window active

**Classic Mode:**
- Quota progress rings with percentage inside
- Separate ring per active quota window

**Rich Mode:**
- Full labels, progress bars, reset timers
- 5h/7d progress colors match main window blue/purple rings

**Quota Metrics:**
- Used: Clockwise/left-to-right progress
- Remaining: Counter-clockwise/right-to-left progress

### API Cost Equivalency ("羊毛进度")

codexU estimates API-equivalent value for monthly Codex usage:

```
API Equivalent Value =
  (uncached_input_tokens / 1,000,000) * uncached_input_price
+ (cached_input_tokens / 1,000,000) * cached_input_price
+ (output_tokens / 1,000,000) * output_price
```

Progress bar shows position relative to Plus, Pro 100, Pro 200, and max monthly value (~$46,500 based on 200M tokens/day * 30 days).

## Code Examples

### Building and Packaging

```bash
# Build for current architecture
make build

# Build release DMG for current arch
make release

# Build for specific architecture
make release-arm64   # Apple Silicon
make release-intel   # Intel
make release-all     # Both architectures

# Output in dist/ folder:
# dist/codexU-1.0.5-mac-arm64.dmg
# dist/codexU-1.0.5-mac-arm64.dmg.sha256
# dist/codexU-1.0.5-mac-x86_64.dmg
# dist/codexU-1.0.5-mac-x86_64.dmg.sha256
```

### Accessing Local Usage Data (Swift)

codexU uses SwiftUI and Swift concurrency to parse local Codex data:

```swift
import Foundation
import SQLite3

// Example: Read quota from state_5.sqlite
func readCodexQuota() throws -> (fiveHour: Double, sevenDay: Double) {
    let dbPath = FileManager.default.homeDirectoryForCurrentUser
        .appendingPathComponent(".codex/state_5.sqlite")
        .path
    
    var db: OpaquePointer?
    guard sqlite3_open(dbPath, &db) == SQLITE_OK else {
        throw NSError(domain: "codexU", code: 1)
    }
    defer { sqlite3_close(db) }
    
    // Query rate limits table (structure varies by Codex version)
    var stmt: OpaquePointer?
    let query = """
        SELECT window_duration_seconds, remaining_count, total_count
        FROM rate_limits
        WHERE window_duration_seconds IN (18000, 604800)
    """
    
    var quotas: [Int: (Double, Double)] = [:]
    if sqlite3_prepare_v2(db, query, -1, &stmt, nil) == SQLITE_OK {
        while sqlite3_step(stmt) == SQLITE_ROW {
            let window = Int(sqlite3_column_int(stmt, 0))
            let remaining = Double(sqlite3_column_int64(stmt, 1))
            let total = Double(sqlite3_column_int64(stmt, 2))
            quotas[window] = (remaining, total)
        }
    }
    sqlite3_finalize(stmt)
    
    let fiveHour = quotas[18000].map { $0.0 / $0.1 } ?? 0.0
    let sevenDay = quotas[604800].map { $0.0 / $0.1 } ?? 0.0
    return (fiveHour, sevenDay)
}
```

### Reading Session Token Events

```swift
import Foundation

struct TokenEvent: Codable {
    let type: String
    let timestamp: Date
    let tokenCount: TokenCount
    
    struct TokenCount: Codable {
        let inputTokens: Int
        let outputTokens: Int
        let cacheReadInputTokens: Int?
        let cacheCreationInputTokens: Int?
    }
}

// Parse rollout JSONL for token usage
func parseSessionTokens(sessionPath: String) throws -> [TokenEvent] {
    let rolloutPath = sessionPath + "/rollout-0.jsonl"
    let content = try String(contentsOfFile: rolloutPath)
    
    return content.split(separator: "\n")
        .compactMap { line in
            guard let data = line.data(using: .utf8),
                  let event = try? JSONDecoder().decode(TokenEvent.self, from: data),
                  event.type == "token_count" else {
                return nil
            }
            return event
        }
}

// Calculate API equivalent cost
func calculateAPICost(tokens: TokenEvent.TokenCount, model: String = "claude-sonnet-3-5-20241022") -> Double {
    let uncachedInput = tokens.inputTokens - (tokens.cacheReadInputTokens ?? 0)
    let cachedInput = tokens.cacheReadInputTokens ?? 0
    let output = tokens.outputTokens
    
    // OpenAI API pricing per 1M tokens (example rates)
    let uncachedInputPrice = 3.0  // $3/1M
    let cachedInputPrice = 0.3    // $0.3/1M (cached discount)
    let outputPrice = 15.0        // $15/1M
    
    return (Double(uncachedInput) / 1_000_000 * uncachedInputPrice) +
           (Double(cachedInput) / 1_000_000 * cachedInputPrice) +
           (Double(output) / 1_000_000 * outputPrice)
}
```

### Custom Shortcut Registration

```swift
import Carbon
import SwiftUI

class ShortcutManager: ObservableObject {
    @Published var currentShortcut: (modifiers: UInt32, keyCode: UInt16)?
    private var eventHandler: EventHandlerRef?
    
    func register(modifiers: UInt32, keyCode: UInt16, handler: @escaping () -> Void) {
        // Minimum: 2 modifiers including Command or Control
        guard modifiers.nonzeroBitCount >= 2,
              (modifiers & UInt32(cmdKey)) != 0 || (modifiers & UInt32(controlKey)) != 0 else {
            return
        }
        
        let hotKeyID = EventHotKeyID(signature: FourCharCode("codU"), id: 1)
        var hotKeyRef: EventHotKeyRef?
        
        RegisterEventHotKey(
            keyCode,
            modifiers,
            hotKeyID,
            GetApplicationEventTarget(),
            0,
            &hotKeyRef
        )
        
        currentShortcut = (modifiers, keyCode)
    }
}
```

## Common Patterns

### Setting Up First-Time Use

```swift
// Check if Codex is installed and logged in
func checkCodexSetup() -> Bool {
    let stateDB = FileManager.default.homeDirectoryForCurrentUser
        .appendingPathComponent(".codex/state_5.sqlite")
    
    guard FileManager.default.fileExists(atPath: stateDB.path) else {
        print("Codex not installed or not used yet")
        return false
    }
    
    // Verify at least one session exists
    let sessionsDir = FileManager.default.homeDirectoryForCurrentUser
        .appendingPathComponent(".codex/sessions")
    
    let hasSession = (try? FileManager.default.contentsOfDirectory(atPath: sessionsDir.path))?.isEmpty == false
    return hasSession
}
```

### Switching Between Codex and Claude Code

```swift
enum Runtime: String, CaseIterable {
    case codex = "Codex"
    case claude = "Claude Code"
}

@Published var selectedRuntime: Runtime = .codex {
    didSet {
        // Refresh all views with new runtime data
        Task {
            await refreshQuota()
            await refreshTokenStats()
            await refreshTaskBoard()
        }
    }
}

// Toggle runtime from menu bar or main window
func toggleRuntime() {
    selectedRuntime = selectedRuntime == .codex ? .claude : .codex
}
```

### Adaptive Single/Dual Ring Layout

```swift
struct QuotaDisplay: View {
    let fiveHourQuota: Double?
    let sevenDayQuota: Double?
    
    var body: some View {
        HStack(spacing: 8) {
            if let fiveHour = fiveHourQuota {
                QuotaRing(percentage: fiveHour, label: "5h", color: .blue)
            }
            
            if let sevenDay = sevenDayQuota {
                QuotaRing(percentage: sevenDay, label: "7d", color: .purple)
            }
        }
        .animation(.easeInOut, value: fiveHourQuota != nil)
        .animation(.easeInOut, value: sevenDayQuota != nil)
    }
}
```

### Particle Effects with Performance Optimization

```swift
struct ParticleView: View {
    @Environment(\.scenePhase) private var scenePhase
    @State private var isWindowFocused = false
    let powerSavingMode: Bool
    
    var shouldRenderParticles: Bool {
        // Only render when window is visible, focused, and not in power saving
        scenePhase == .active && isWindowFocused && !powerSavingMode
    }
    
    var body: some View {
        ZStack {
            if shouldRenderParticles {
                ParticleEmitter()
                    .transition(.opacity)
            }
        }
        .onReceive(NotificationCenter.default.publisher(for: NSWindow.didBecomeKeyNotification)) { _ in
            isWindowFocused = true
        }
        .onReceive(NotificationCenter.default.publisher(for: NSWindow.didResignKeyNotification)) { _ in
            isWindowFocused = false
        }
    }
}
```

## Troubleshooting

### Quota Shows `--` or Empty

**Problem**: Status bar or main window shows `--` for quotas instead of percentages.

**Solutions:**
1. Verify Codex is logged in: `codex auth login`
2. Check SQLite file exists: `ls -la ~/.codex/state_5.sqlite`
3. Use at least once to generate state: Create a new Codex thread
4. For Claude Code: Ensure statusline snapshot cache exists (optional feature)
5. Check file permissions: `chmod 600 ~/.codex/state_5.sqlite`

### Token Statistics Not Updating

**Problem**: Today's tokens or trend charts show zero or stale data.

**Solutions:**
1. Verify session files exist: `ls ~/.codex/sessions/`
2. Check rollout JSONL files: `find ~/.codex/sessions -name "rollout-*.jsonl"`
3. For Claude Code: Check transcript JSONL: `find ~/.claude/projects -name "*.jsonl"`
4. Click refresh button in main window
5. Check Console.app for codexU parsing errors

### App Won't Open After Install

**Problem**: macOS blocks app launch with security warning.

**Solutions:**
```bash
# Method 1: Right-click → Open in Finder
# Method 2: Command line override
xattr -dr com.apple.quarantine /Applications/codexU.app

# Then open System Settings > Privacy & Security
# Click "Open Anyway" next to codexU.app
```

### Shortcut Key Not Working

**Problem**: Custom shortcut doesn't trigger main window.

**Solutions:**
1. Ensure at least 2 modifiers including Command or Control
2. Check for conflicts: System Settings > Keyboard > Keyboard Shortcuts
3. Reset to default in codexU Settings
4. Common conflicts: Avoid `Command + Shift + U` (Character Viewer)
5. Try alternative: `Command + Control + U`, `Command + Option + U`

### High CPU Usage

**Problem**: codexU uses excessive CPU in background.

**Solutions:**
1. Update to v1.0.5+ (optimized polling and particle rendering)
2. Enable power saving mode in Settings (only renders particles on hover)
3. Particle effects auto-disable when:
   - Window is minimized or hidden
   - Battery is low
   - Thermal state is critical
   - "Reduce motion" accessibility setting is on
4. Close main window (hides Dock icon, keeps menu bar)

### Build Errors from Source

**Problem**: `make build` fails with Swift compilation errors.

**Solutions:**
```bash
# Ensure Xcode Command Line Tools installed
xcode-select --install

# Check macOS version (requires 14+)
sw_vers

# Clean build artifacts
make clean
rm -rf build/

# Verify Swift version
swift --version  # Should be Swift 5.9+

# Try explicit architecture
make build ARCH=arm64  # or x86_64
```

### DMG Packaging Fails

**Problem**: `make release` fails or produces corrupt DMG.

**Solutions:**
```bash
# Install required tools
brew install create-dmg

# Check disk space
df -h

# Clean dist folder
rm -rf dist/
mkdir -p dist/

# Build without signing first
make build

# Manual DMG creation
create-dmg \
  --volname "codexU" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --app-drop-link 450 200 \
  dist/codexU-test.dmg \
  build/Release/codexU.app
```

### Claude Code Quota Missing

**Problem**: Claude Code 5h/7d quotas show `--` even with active subscription.

**Cause**: codexU needs optional statusline snapshot cache file.

**Solutions:**
1. This is expected behavior (cache file is optional)
2. Token statistics and trends still work from transcript JSONL
3. Manual cache population not currently supported
4. Only affects quota display, not usage analytics

### Update Check Fails

**Problem**: "Check for Updates" in Settings shows connection error.

**Solutions:**
```bash
# Test GitHub API access
curl -I https://api.github.com/repos/shanggqm/codexU/releases/latest

# Check network proxy settings
# System Settings > Network > Advanced > Proxies

# Disable auto-check if behind firewall:
# codexU Settings > System > Uncheck "Automatically check for updates"
```

### File Access Denied Errors

**Problem**: codexU logs show permission denied for `~/.codex/` or `~/.claude/`.

**Solutions:**
1. Grant Full Disk Access: System Settings > Privacy & Security > Full Disk Access → Add codexU
2. Or manually fix permissions:
```bash
chmod -R 755 ~/.codex
chmod -R 755 ~/.claude
```
3. If using symlinks, ensure target directories are readable
4. Check Console.app for specific file paths being denied

## Reference Links

- **Homepage**: https://shanggqm.github.io/codexU-site/
- **Repository**: https://github.com/shanggqm/codexU
- **Releases**: https://github.com/shanggqm/codexU/releases
- **Issues**: https://github.com/shanggqm/codexU/issues
- **Distribution Guide**: [DISTRIBUTION.md](https://github.com/shanggqm/codexU/blob/main/DISTRIBUTION.md)
- **License**: MIT
