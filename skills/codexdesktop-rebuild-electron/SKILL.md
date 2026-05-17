---
name: codexdesktop-rebuild-electron
description: Cross-platform Electron desktop app for OpenAI Codex with build and development workflows
triggers:
  - build codex desktop app
  - develop with codex desktop
  - electron forge codex configuration
  - package codex for multiple platforms
  - run codex desktop in development
  - create codex desktop release
  - configure electron app for codex
  - troubleshoot codex desktop build
---

# Codex Desktop Rebuild Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

CodexDesktop-Rebuild is a cross-platform Electron application that rebuilds the OpenAI Codex Desktop App for macOS, Windows, and Linux. It uses Electron Forge for building and packaging across multiple architectures (x64, arm64).

## Installation

```bash
# Clone the repository
git clone https://github.com/Haleclipse/CodexDesktop-Rebuild.git
cd CodexDesktop-Rebuild

# Install dependencies
npm install
```

## Development

### Running in Development Mode

```bash
npm run dev
```

This starts the Electron app with hot-reloading enabled via Vite.

### Project Structure

```
├── src/
│   ├── .vite/build/     # Main process (Electron backend)
│   └── webview/         # Renderer process (Frontend UI)
├── resources/
│   ├── electron.icns    # macOS app icon
│   └── notification.wav # Notification sound
├── scripts/
│   └── patch-copyright.js
├── forge.config.js      # Electron Forge configuration
└── package.json
```

## Building

### Build for Current Platform

```bash
npm run build
```

### Build for Specific Platforms

```bash
# macOS
npm run build:mac-x64
npm run build:mac-arm64

# Windows
npm run build:win-x64

# Linux
npm run build:linux-x64
npm run build:linux-arm64
```

### Build All Platforms

```bash
npm run build:all
```

This creates distributables in the `out/` directory.

## Configuration

### Electron Forge Configuration

The `forge.config.js` file controls build settings:

```javascript
module.exports = {
  packagerConfig: {
    name: 'Codex Desktop',
    icon: './resources/electron',
    asar: true,
    executableName: 'codex-desktop',
    appBundleId: 'com.cometix.codex',
  },
  makers: [
    {
      name: '@electron-forge/maker-zip',
      platforms: ['darwin', 'linux', 'win32']
    },
    {
      name: '@electron-forge/maker-dmg',
      config: {
        name: 'Codex Desktop',
        icon: './resources/electron.icns'
      }
    },
    {
      name: '@electron-forge/maker-deb',
      config: {
        options: {
          maintainer: 'Cometix Space',
          homepage: 'https://github.com/Haleclipse/CodexDesktop-Rebuild'
        }
      }
    }
  ],
  plugins: [
    {
      name: '@electron-forge/plugin-vite',
      config: {
        build: [
          {
            entry: 'src/.vite/build/main.js',
            config: 'vite.main.config.js'
          }
        ],
        renderer: [
          {
            name: 'main_window',
            config: 'vite.renderer.config.js'
          }
        ]
      }
    }
  ]
};
```

### Package.json Scripts

```javascript
{
  "scripts": {
    "dev": "electron-forge start",
    "build": "electron-forge make",
    "build:mac-x64": "electron-forge make --platform=darwin --arch=x64",
    "build:mac-arm64": "electron-forge make --platform=darwin --arch=arm64",
    "build:win-x64": "electron-forge make --platform=win32 --arch=x64",
    "build:linux-x64": "electron-forge make --platform=linux --arch=x64",
    "build:linux-arm64": "electron-forge make --platform=linux --arch=arm64",
    "build:all": "npm run build:mac-x64 && npm run build:mac-arm64 && npm run build:win-x64 && npm run build:linux-x64 && npm run build:linux-arm64"
  }
}
```

## Main Process Development

### Basic Electron Main Process Structure

```javascript
// src/.vite/build/main.js
const { app, BrowserWindow } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    icon: path.join(__dirname, '../../resources/electron.icns')
  });

  // Load the renderer
  if (process.env.VITE_DEV_SERVER_URL) {
    mainWindow.loadURL(process.env.VITE_DEV_SERVER_URL);
  } else {
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'));
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createWindow();
  }
});
```

### IPC Communication

```javascript
// Main process
const { ipcMain } = require('electron');

ipcMain.handle('execute-codex-command', async (event, command) => {
  // Execute codex CLI command
  const result = await executeCommand(command);
  return result;
});

// Renderer process
const { ipcRenderer } = require('electron');

async function runCodex(command) {
  const result = await ipcRenderer.invoke('execute-codex-command', command);
  return result;
}
```

## Renderer Development

### Vite Configuration for Renderer

```javascript
// vite.renderer.config.js
import { defineConfig } from 'vite';
import path from 'path';

export default defineConfig({
  root: path.join(__dirname, 'src/webview'),
  build: {
    outDir: path.join(__dirname, '.vite/renderer'),
    emptyOutDir: true
  }
});
```

### Frontend Integration

```javascript
// src/webview/main.js
import './style.css';

// Initialize the app
document.addEventListener('DOMContentLoaded', () => {
  const app = document.getElementById('app');
  
  app.innerHTML = `
    <div class="codex-interface">
      <h1>Codex Desktop</h1>
      <textarea id="prompt" placeholder="Enter your prompt..."></textarea>
      <button id="execute">Execute</button>
      <pre id="output"></pre>
    </div>
  `;

  document.getElementById('execute').addEventListener('click', async () => {
    const prompt = document.getElementById('prompt').value;
    const output = await window.codex.execute(prompt);
    document.getElementById('output').textContent = output;
  });
});
```

## CI/CD with GitHub Actions

The project automatically builds on push to `master` or tag creation:

```yaml
# .github/workflows/build.yml
name: Build
on:
  push:
    branches: [master]
    tags: ['v*']

jobs:
  build:
    strategy:
      matrix:
        os: [macos-latest, windows-latest, ubuntu-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm install
      - run: npm run build
      - uses: actions/upload-artifact@v3
        with:
          name: dist-${{ matrix.os }}
          path: out/
```

## Troubleshooting

### Build Fails on Native Dependencies

```bash
# Rebuild native modules for Electron
npm install --save-dev @electron/rebuild
npx electron-rebuild
```

### Icon Not Showing

Ensure icon files exist:
- macOS: `resources/electron.icns`
- Windows: `resources/electron.ico`
- Linux: `resources/electron.png`

### Code Signing Issues on macOS

```javascript
// forge.config.js
module.exports = {
  packagerConfig: {
    osxSign: {
      identity: process.env.APPLE_IDENTITY,
      'hardened-runtime': true,
      entitlements: 'entitlements.plist',
      'entitlements-inherit': 'entitlements.plist',
      'signature-flags': 'library'
    },
    osxNotarize: {
      appleId: process.env.APPLE_ID,
      appleIdPassword: process.env.APPLE_PASSWORD,
      teamId: process.env.APPLE_TEAM_ID
    }
  }
};
```

### Development Server Not Starting

```bash
# Clear Vite cache
rm -rf .vite

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### Cross-Platform Build Issues

Use Docker for consistent builds:

```bash
docker run --rm -v $(pwd):/project electronuserland/builder:wine \
  /bin/bash -c "cd /project && npm install && npm run build:win-x64"
```

## Common Patterns

### Adding Custom Menu

```javascript
const { Menu } = require('electron');

const template = [
  {
    label: 'File',
    submenu: [
      { role: 'quit' }
    ]
  },
  {
    label: 'Edit',
    submenu: [
      { role: 'undo' },
      { role: 'redo' },
      { type: 'separator' },
      { role: 'cut' },
      { role: 'copy' },
      { role: 'paste' }
    ]
  }
];

const menu = Menu.buildFromTemplate(template);
Menu.setApplicationMenu(menu);
```

### Auto-Update Configuration

```javascript
const { autoUpdater } = require('electron-updater');

autoUpdater.checkForUpdatesAndNotify();

autoUpdater.on('update-available', () => {
  // Notify user
});

autoUpdater.on('update-downloaded', () => {
  // Prompt to restart
  autoUpdater.quitAndInstall();
});
```

### Environment-Specific Configuration

```javascript
// Check environment
const isDev = process.env.NODE_ENV === 'development';

if (isDev) {
  // Enable DevTools
  mainWindow.webContents.openDevTools();
}
```
