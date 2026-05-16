---
name: codex-plusplus-tweak-system
description: Expert in developing, installing, and managing tweaks for the Codex++ desktop app extension system
triggers:
  - "help me create a Codex++ tweak"
  - "install codex-plusplus on my machine"
  - "how do I extend Codex with custom features"
  - "write a tweak for the Codex desktop app"
  - "fix my codex-plusplus installation"
  - "add custom keyboard shortcuts to Codex"
  - "manage Codex++ tweaks"
  - "update my Codex app with codex-plusplus installed"
---

# Codex++ Tweak System

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Codex++ is a tweak system for the Codex desktop app that lets you inject custom features, fix UI bugs, and manage extensions without rebuilding the app. It patches the local Codex installation to load a runtime that discovers and executes small ESM modules (tweaks) with full access to the Electron renderer process.

## Installation

### macOS/Linux (Homebrew)

```bash
brew install b-nnett/codex-plusplus/codexplusplus
codexplusplus install
```

### macOS/Linux (Source Bootstrap)

```bash
curl -fsSL https://raw.githubusercontent.com/b-nnett/codex-plusplus/main/install.sh | bash
```

### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/b-nnett/codex-plusplus/main/install.ps1 | iex
```

### Using Bun

```bash
bun install -g github:b-nnett/codex-plusplus
codexplusplus install
```

**What the installer does:**
- Backs up Codex.app to `~/.codex-plusplus/backup/`
- Patches `app.asar` to load the Codex++ runtime
- Re-signs the app with a local signing identity (macOS)
- Installs a watcher that auto-repairs on Codex updates
- Installs default tweaks from GitHub releases

**Installation flags:**
- `--no-default-tweaks` — Skip installing default tweaks
- `--local` — Use stable local signing identity (macOS)

## Key Commands

```bash
# Check installation status
codexplusplus status

# Validate and repair installation
codexplusplus doctor
codexplusplus repair

# Update Codex++ to latest release
codexplusplus update

# Update Codex++ from development branch (advanced)
codexplusplus update --ref main

# Update Codex app itself (macOS - required for patched apps)
codexplusplus update-codex

# Create a new tweak from template
codexplusplus create-tweak my-tweak

# Validate tweak manifest and structure
codexplusplus validate-tweak ~/path/to/tweak

# Enter safe mode (disable all tweaks)
codexplusplus safe-mode
codexplusplus safe-mode --off

# Development mode (watch and reload)
codexplusplus dev

# Uninstall Codex++ completely
codexplusplus uninstall
```

## User Data Directories

| OS | Location |
|---|---|
| macOS | `~/Library/Application Support/codex-plusplus/` |
| Linux | `~/.local/share/codex-plusplus/` |
| Windows | `%APPDATA%/codex-plusplus/` |

**Directory structure:**
```
codex-plusplus/
├── runtime/          # Codex++ runtime code
├── tweaks/           # Installed tweaks
│   ├── my-tweak/
│   │   ├── manifest.json
│   │   └── index.js
├── config.json       # Runtime configuration
└── backup/           # Codex.app backup
```

## Creating a Tweak

### Minimal Tweak Structure

```
my-tweak/
├── manifest.json
└── index.js
```

### manifest.json

```json
{
  "id": "com.example.my-tweak",
  "name": "My Tweak",
  "version": "1.0.0",
  "githubRepo": "username/my-tweak",
  "author": "Your Name",
  "description": "Adds custom functionality to Codex",
  "minRuntime": "0.1.0"
}
```

**Required fields:**
- `id` — Reverse-DNS unique identifier
- `name` — Display name
- `version` — Semver version
- `githubRepo` — `owner/repo` for update checks
- `minRuntime` — Minimum Codex++ runtime version

### Basic Tweak (JavaScript)

```javascript
// index.js
export default {
  start(api) {
    api.log.info('Tweak started');
    
    // Add settings panel
    api.settings.register({
      id: 'my-tweak',
      title: 'My Tweak Settings',
      render: (root) => {
        root.innerHTML = `
          <div>
            <h3>Custom Settings</h3>
            <button id="test-btn">Click me</button>
          </div>
        `;
        
        root.querySelector('#test-btn').addEventListener('click', () => {
          api.log.info('Button clicked!');
        });
      }
    });
  },
  
  stop() {
    // Cleanup resources
  }
};
```

### TypeScript Tweak with Full API

```typescript
// index.ts
import type { Tweak, CodexPlusPlusAPI } from "@codex-plusplus/sdk";

interface MyTweakConfig {
  enabled: boolean;
  customColor: string;
}

export default {
  start(api: CodexPlusPlusAPI) {
    // Access configuration
    const config = api.config.get<MyTweakConfig>('my-tweak', {
      enabled: true,
      customColor: '#ff0000'
    });
    
    // Logging
    api.log.info('Starting tweak with config:', config);
    api.log.warn('This is a warning');
    api.log.error('This is an error');
    
    // DOM manipulation
    const observer = new MutationObserver(() => {
      const chatInput = document.querySelector('[contenteditable="true"]');
      if (chatInput && config.enabled) {
        chatInput.style.borderColor = config.customColor;
      }
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
    
    // Settings panel with persistence
    api.settings.register({
      id: 'my-tweak',
      title: 'My Tweak',
      render: (root) => {
        root.innerHTML = `
          <div class="tweak-settings">
            <label>
              <input type="checkbox" id="enabled" ${config.enabled ? 'checked' : ''}>
              Enable custom styling
            </label>
            <label>
              Custom color:
              <input type="color" id="color" value="${config.customColor}">
            </label>
            <button id="save">Save</button>
          </div>
        `;
        
        root.querySelector('#save')?.addEventListener('click', () => {
          const enabled = (root.querySelector('#enabled') as HTMLInputElement).checked;
          const customColor = (root.querySelector('#color') as HTMLInputElement).value;
          
          api.config.set('my-tweak', { enabled, customColor });
          api.log.info('Settings saved');
          
          // Reload to apply changes
          location.reload();
        });
      }
    });
    
    // Store observer for cleanup
    (api as any)._observer = observer;
  },
  
  stop() {
    const observer = (this as any)._observer;
    if (observer) {
      observer.disconnect();
    }
  }
} satisfies Tweak;
```

### Advanced: Injecting Custom UI

```typescript
export default {
  start(api) {
    // Wait for Codex UI to be ready
    const injectCustomButton = () => {
      const toolbar = document.querySelector('.chat-toolbar');
      if (!toolbar) return;
      
      const btn = document.createElement('button');
      btn.textContent = '✨ Custom Action';
      btn.className = 'toolbar-button';
      btn.onclick = () => {
        api.log.info('Custom action triggered');
        // Your custom logic
      };
      
      toolbar.appendChild(btn);
    };
    
    // Observe for toolbar appearance
    const observer = new MutationObserver(() => {
      injectCustomButton();
    });
    
    observer.observe(document.body, {
      childList: true,
      subtree: true
    });
    
    injectCustomButton(); // Try immediately
  },
  
  stop() {}
};
```

### Keyboard Shortcuts Tweak

```typescript
export default {
  start(api) {
    const handleKeydown = (e: KeyboardEvent) => {
      // Cmd/Ctrl + Shift + K
      if ((e.metaKey || e.ctrlKey) && e.shiftKey && e.key === 'k') {
        e.preventDefault();
        api.log.info('Custom shortcut triggered');
        // Your action here
      }
    };
    
    document.addEventListener('keydown', handleKeydown);
    
    // Store for cleanup
    (api as any)._keyHandler = handleKeydown;
  },
  
  stop() {
    const handler = (this as any)._keyHandler;
    if (handler) {
      document.removeEventListener('keydown', handler);
    }
  }
};
```

## Configuration

### Runtime Config

Located at `<user-data-dir>/config.json`:

```json
{
  "enabledTweaks": [
    "com.example.my-tweak",
    "co.bennett.custom-keyboard-shortcuts"
  ],
  "autoUpdate": true,
  "safeMode": false,
  "logLevel": "info"
}
```

### Per-Tweak Config

Tweaks can store configuration using the API:

```typescript
// Get config with defaults
const config = api.config.get('my-tweak', { theme: 'dark' });

// Update config
api.config.set('my-tweak', { theme: 'light' });

// Config is persisted automatically
```

## Tweak Distribution & Updates

### Publishing a Tweak

1. Create a GitHub repository for your tweak
2. Add tweak files (manifest.json, index.js/ts)
3. Create a GitHub Release with a semver tag (e.g., `v1.0.0`)
4. Attach a `.zip` of the tweak folder to the release

**Release structure:**
```
my-tweak-v1.0.0.zip
└── my-tweak/
    ├── manifest.json
    └── index.js
```

### Installing Tweaks

Users copy tweak folders to `<user-data-dir>/tweaks/` and enable them in **Settings → Tweaks**.

### Update Checking

Codex++ checks `githubRepo` in manifest.json for newer releases once per day. Users review release notes and manually update.

## Common Patterns

### Persistent State

```typescript
let myState = api.config.get('my-tweak', { count: 0 });

function incrementCounter() {
  myState.count++;
  api.config.set('my-tweak', myState);
}
```

### React to Codex Events

```typescript
// Watch for new messages
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    mutation.addedNodes.forEach((node) => {
      if (node instanceof HTMLElement && node.matches('.message')) {
        api.log.info('New message detected');
      }
    });
  });
});

observer.observe(document.querySelector('#chat-container'), {
  childList: true,
  subtree: true
});
```

### CSS Injection

```typescript
const style = document.createElement('style');
style.textContent = `
  .custom-theme {
    --primary-color: #00ff00;
  }
  
  .chat-message {
    border-left: 3px solid var(--primary-color);
  }
`;
document.head.appendChild(style);

// Store for cleanup
(api as any)._styleElement = style;
```

## Troubleshooting

### Codex won't launch after install

```bash
# Check status
codexplusplus status

# Repair installation
codexplusplus repair

# If repair fails, uninstall and reinstall
codexplusplus uninstall
codexplusplus install
```

### Tweak not loading

```bash
# Validate tweak structure
codexplusplus validate-tweak ~/Library/Application\ Support/codex-plusplus/tweaks/my-tweak

# Check runtime logs (look for errors)
tail -f ~/Library/Logs/codex-plusplus/runtime.log
```

### Safe mode (disable all tweaks)

```bash
codexplusplus safe-mode
# Launch Codex, fix issues, then:
codexplusplus safe-mode --off
```

### macOS Gatekeeper issues

After first launch of re-signed Codex:
1. System Preferences → Privacy & Security
2. Click "Open Anyway" for Codex.app
3. Or: `xattr -cr /Applications/Codex.app`

### Codex update breaks Codex++

```bash
# macOS: Use official updater
codexplusplus update-codex

# After Codex updates, watcher auto-repairs
# Or manually:
codexplusplus repair
```

### Windows: Wrong app launches

Launch **Codex++** from Start Menu/Desktop, not the Microsoft Store **Codex** shortcut. The Store version is unpatched.

### Development workflow

```bash
# Watch for changes and auto-reload
codexplusplus dev

# Edit tweak files in:
# macOS: ~/Library/Application Support/codex-plusplus/tweaks/my-tweak/
# Reload Codex (Cmd+R / Ctrl+R) to see changes
```

### Clear all config

```bash
# Remove config but keep tweaks
rm ~/Library/Application\ Support/codex-plusplus/config.json

# Full reset
rm -rf ~/Library/Application\ Support/codex-plusplus/
codexplusplus install
```

## Security Notes

- Tweaks run with full Electron renderer privileges
- Only install tweaks from trusted sources
- Review tweak code before installing
- `githubRepo` in manifest enables update notifications but doesn't auto-update
- Codex++ never executes code without user consent

## Example: Complete UI Tweak

```typescript
// Dark mode toggle tweak
import type { Tweak } from "@codex-plusplus/sdk";

export default {
  start(api) {
    const config = api.config.get('dark-mode', { enabled: false });
    
    const applyTheme = (dark: boolean) => {
      document.body.classList.toggle('dark-theme', dark);
    };
    
    applyTheme(config.enabled);
    
    api.settings.register({
      id: 'dark-mode',
      title: 'Dark Mode',
      render: (root) => {
        root.innerHTML = `
          <label>
            <input type="checkbox" id="toggle" ${config.enabled ? 'checked' : ''}>
            Enable dark mode
          </label>
        `;
        
        root.querySelector('#toggle')?.addEventListener('change', (e) => {
          const enabled = (e.target as HTMLInputElement).checked;
          api.config.set('dark-mode', { enabled });
          applyTheme(enabled);
        });
      }
    });
    
    // Inject CSS
    const style = document.createElement('style');
    style.textContent = `
      .dark-theme {
        background: #1a1a1a;
        color: #ffffff;
      }
    `;
    document.head.appendChild(style);
    (api as any)._style = style;
  },
  
  stop() {
    document.body.classList.remove('dark-theme');
    const style = (this as any)._style;
    if (style) style.remove();
  }
} satisfies Tweak;
```
