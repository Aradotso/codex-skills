---
name: heige-codex-skin-studio
description: One-click theme & skin switcher for OpenAI Codex Desktop using CDP injection — custom images, 12 built-in themes, persistent across restarts
triggers:
  - how do I theme Codex Desktop
  - customize Codex Desktop appearance
  - apply custom skin to Codex
  - change Codex Desktop theme
  - use HeiGe Codex Skin Studio
  - create custom Codex theme from image
  - enable persistent theming in Codex
  - troubleshoot Codex skin not loading
---

# HeiGe Codex Skin Studio

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

**HeiGe Codex Skin Studio** is a theme and skin switcher for OpenAI Codex Desktop (macOS/Windows) that injects custom CSS and backgrounds through Chrome DevTools Protocol (CDP) on loopback `127.0.0.1:9341`. It does **not** modify `app.asar`, binaries, or signature resources. One image becomes a theme; a top menu (`🎨`) switches themes instantly and controls persistence across restarts.

## What It Does

- **12 built-in themes**: Hatsune Miku, Genshin Impact (2), Wuthering Waves (2), Naruto (2), Love and Deepspace (2), Dragon Ball (2), easter egg
- **Custom image themes**: Upload any PNG/JPG/WebP, auto-extracts color palette and generates dark/light variants
- **Persistent skin**: Optional launch agent (macOS LaunchAgent / Windows scheduled task) reapplies theme on every Codex restart
- **Reading enhancement**: 90% transparent adaptive background for replies, toggled in theme center
- **AI-assisted theme creation**: `.skill` file enables Codex to generate images and apply them as themes end-to-end

## Installation

### macOS

```bash
cd /path/to/heige-codex-skin-studio
open scripts/install.command
```

This installs the launcher and applies the default Miku theme. The `🎨` menu appears in Codex Desktop's top bar.

### Windows

```cmd
cd \path\to\heige-codex-skin-studio
scripts\windows\install.bat
```

For daily use, run `scripts\windows\apply.ps1` or the compatibility alias `scripts\windows\enable-skin.bat` to restore the current session. To enable persistence (launch on login), use the `🎨` menu's "Persistent Skin" toggle.

**Uninstall** (Windows):

```cmd
scripts\windows\uninstall.bat
```

Removes scheduled tasks, Start Menu shortcuts, AppData state, and stable installation directory.

## Key Commands & Scripts

| Script | Purpose |
|--------|---------|
| `scripts/install.command` (macOS) | Initial install, sets up launcher |
| `scripts/windows/install.bat` | Initial install (Windows) |
| `scripts/apply.command` (macOS) | Restore skin for current session, `--restart` flag to force quit & relaunch |
| `scripts/windows/apply.ps1` | Restore skin (Windows) |
| `scripts/pause.command` / `scripts/pause.ps1` | Temporarily disable skin (current session) |
| `scripts/resume.command` / `scripts/resume.ps1` | Re-enable skin (current session) |
| `scripts/restore.command` / `scripts/restore.ps1` | Remove skin, restore native UI |
| `scripts/windows/close-codex.bat` | Safely quit Codex/GPT Desktop, preserve persistence settings |
| `scripts/windows/uninstall.bat` | Complete uninstall (Windows) |
| `customize.command` | Generate theme from local image file |

**Command-line options** (for `apply.command` / `apply.ps1`):

```bash
# macOS
./scripts/apply.command --restart        # Force quit Codex & relaunch with skin
./scripts/apply.command --theme miku     # Apply specific built-in theme
./scripts/apply.command --custom /path/to/image.png  # Apply custom image theme

# Windows (PowerShell)
.\scripts\windows\apply.ps1 -Restart
.\scripts\windows\apply.ps1 -Theme "genshin-night"
.\scripts\windows\apply.ps1 -CustomImage "C:\path\to\image.jpg"
```

## Creating Custom Themes

### Method 1: Top Menu Upload

1. Click `🎨` in Codex Desktop
2. Select `＋ Custom Image`
3. Upload PNG/JPG/JPEG/WebP
4. Auto-extracts palette, generates light/dark variants
5. Theme is saved to user library and persists if "Persistent Skin" is enabled

### Method 2: Command-Line Generator

```bash
# macOS
./customize.command

# Prompts for image path, generates theme in output/custom-theme/
```

### Method 3: AI-Assisted (Codex Skill)

Install `output/heige-codex-skin-studio.skill` in Codex Desktop, then prompt:

> "Generate a cyberpunk neon cityscape, then create a Codex theme from it"

Codex will generate the image, extract colors, and apply the theme automatically.

## Theme JSON Format

Themes are stored in `themes/<theme-name>/theme.json`:

```json
{
  "name": "Miku 488137",
  "author": "HeiGe AI",
  "version": "2.0.0",
  "description": "High-fidelity Hatsune Miku theme",
  "background": {
    "light": "miku-light.webp",
    "dark": "miku-dark.webp"
  },
  "colors": {
    "light": {
      "primary": "#39C5BB",
      "secondary": "#5DCECD",
      "accent": "#7FD9D8",
      "background": "#E8F8F8",
      "surface": "#FFFFFF",
      "text": "#1A1A1A",
      "textSecondary": "#666666",
      "border": "#D0E8E8"
    },
    "dark": {
      "primary": "#39C5BB",
      "secondary": "#2DB5B0",
      "accent": "#5DCECD",
      "background": "#0A1A1A",
      "surface": "#162828",
      "text": "#E8F8F8",
      "textSecondary": "#A0B8B8",
      "border": "#2D4848"
    }
  },
  "codexAppearance": {
    "light": "light",
    "dark": "dark"
  }
}
```

**Key fields**:
- `background.light` / `background.dark`: relative paths to background images
- `colors.light` / `colors.dark`: 8-color palette (primary, secondary, accent, background, surface, text, textSecondary, border)
- `codexAppearance`: maps theme mode to Codex's native light/dark setting

## Configuration & Persistence

**Persistent skin** is controlled via the `🎨` menu toggle:

- **macOS**: Creates `~/Library/LaunchAgents/com.heigeai.codex-skin-controller.plist`
- **Windows**: Creates scheduled task `HeiGeAI_CodexSkinController` for current user login

**User theme library**: Custom uploaded themes are stored in:
- macOS: `~/Library/Application Support/HeiGeCodexSkin/user-themes/`
- Windows: `%APPDATA%\HeiGeCodexSkin\user-themes\`

**State file** (tracks current theme, persistence status):
- macOS: `~/Library/Application Support/HeiGeCodexSkin/skin-state.json`
- Windows: `%APPDATA%\HeiGeCodexSkin\skin-state.json`

```json
{
  "currentTheme": "miku",
  "persistenceEnabled": true,
  "readingEnhancement": true,
  "lastApplied": "2026-07-29T12:34:56.789Z"
}
```

## Common Patterns

### Apply a Built-in Theme Programmatically

```javascript
// In src/injector/theme-manager.js (or your own script)
const ThemeManager = require('./src/injector/theme-manager.js');
const tm = new ThemeManager();

await tm.applyTheme('genshin-night'); // Built-in theme ID
```

### Generate & Apply Custom Theme from Image

```javascript
const { generateThemeFromImage } = require('./src/utils/theme-generator.js');
const ThemeManager = require('./src/injector/theme-manager.js');

const imagePath = '/path/to/wallpaper.jpg';
const outputDir = './output/my-custom-theme';

// Extract colors, generate theme.json + CSS
await generateThemeFromImage(imagePath, outputDir, {
  themeName: 'My Custom Theme',
  author: 'Your Name'
});

// Apply it
const tm = new ThemeManager();
await tm.applyTheme(outputDir); // Pass directory path for custom themes
```

### Inject CSS Directly via CDP

```javascript
const CDP = require('chrome-remote-interface');

const client = await CDP({ port: 9341 });
const { Page, Runtime } = client;

await Page.enable();
await Runtime.enable();

const css = `
  body {
    background-image: url('file:///path/to/bg.png');
    background-size: cover;
  }
  .chat-message {
    background-color: rgba(57, 197, 187, 0.9) !important;
  }
`;

await Runtime.evaluate({
  expression: `
    (function() {
      const style = document.createElement('style');
      style.id = 'heige-custom-skin';
      style.textContent = ${JSON.stringify(css)};
      document.head.appendChild(style);
    })();
  `
});

await client.close();
```

### Read Current Theme State

```javascript
const fs = require('fs');
const path = require('path');
const os = require('os');

const stateDir = process.platform === 'win32'
  ? path.join(process.env.APPDATA, 'HeiGeCodexSkin')
  : path.join(os.homedir(), 'Library', 'Application Support', 'HeiGeCodexSkin');

const statePath = path.join(stateDir, 'skin-state.json');
const state = JSON.parse(fs.readFileSync(statePath, 'utf-8'));

console.log('Current theme:', state.currentTheme);
console.log('Persistence enabled:', state.persistenceEnabled);
```

### Toggle Reading Enhancement

```javascript
// In injected context (via CDP Runtime.evaluate)
window.heigeReadingEnhancement = !window.heigeReadingEnhancement;

// Reload theme to apply
const themeId = document.documentElement.dataset.heigeTheme;
window.heigeApplyTheme(themeId);
```

## Environment Variables

- `HEIGE_CODEX_CDP_PORT` — Override CDP port (default: `9341`)
- `HEIGE_CODEX_THEME_DIR` — Custom theme directory (default: `./themes`)
- `HEIGE_LOG_LEVEL` — `debug` | `info` | `warn` | `error` (default: `info`)

Example:

```bash
export HEIGE_CODEX_CDP_PORT=9342
export HEIGE_LOG_LEVEL=debug
./scripts/apply.command
```

## Troubleshooting

### Skin not appearing after restart

1. Check persistence is enabled: `🎨` menu → "Persistent Skin" should be green
2. Verify launch agent exists:
   - macOS: `ls ~/Library/LaunchAgents/com.heigeai.codex-skin-controller.plist`
   - Windows: `schtasks /Query /TN HeiGeAI_CodexSkinController`
3. Re-run install script

### Codex window becomes sluggish (low FPS, input lag)

```bash
# macOS
./scripts/apply.command --restart

# Windows
.\scripts\windows\apply.ps1 -Restart
```

Force-quit and relaunch Codex with fresh CDP session.

### Custom image theme not saving

- Ensure image is PNG/JPG/JPEG/WebP, <10MB
- Check user theme directory exists and is writable:
  - macOS: `~/Library/Application Support/HeiGeCodexSkin/user-themes/`
  - Windows: `%APPDATA%\HeiGeCodexSkin\user-themes\`
- Review logs: `tail -f ~/.heige-codex-skin.log` (macOS) or `%TEMP%\heige-codex-skin.log` (Windows)

### CDP connection refused

- Codex must be launched with `--remote-debugging-port=9341`
- Check Codex is running: `ps aux | grep Codex` (macOS) or `tasklist | findstr Codex` (Windows)
- Firewall/antivirus may block loopback port — whitelist `127.0.0.1:9341`

### "Persistent Skin" toggle stuck on "Waiting..."

- macOS: Check LaunchAgent plist syntax: `plutil -lint ~/Library/LaunchAgents/com.heigeai.codex-skin-controller.plist`
- Windows: Run `schtasks /Query /TN HeiGeAI_CodexSkinController /V /FO LIST` to verify task exists and is enabled
- Re-run install script to repair

### Theme colors not matching preview

- Verify `theme.json` color keys are correct (primary, secondary, accent, background, surface, text, textSecondary, border)
- Check Codex's native appearance setting — theme applies `codexAppearance.light` or `codexAppearance.dark` to the app
- Some UI elements may use Codex's built-in styles — skin only overrides injected CSS

### Uninstall doesn't remove all files

```bash
# macOS
rm -rf ~/Library/Application\ Support/HeiGeCodexSkin
rm ~/Library/LaunchAgents/com.heigeai.codex-skin-controller.plist
launchctl remove com.heigeai.codex-skin-controller

# Windows
schtasks /Delete /TN HeiGeAI_CodexSkinController /F
rd /s /q "%APPDATA%\HeiGeCodexSkin"
rd /s /q "%LOCALAPPDATA%\Programs\HeiGeCodexSkin"
```

## Security Notes

- CDP on loopback (`127.0.0.1:9341`) has **no authentication** — any local process with same user privileges can connect
- Injection only occurs during local debugging session; native Codex signature is **not modified**
- Full security policy: `SECURITY.md` in project root
- Asset provenance (themes, images): `ASSET_PROVENANCE.md`

## Real-World Example: AI-Driven Theme Pipeline

```javascript
// Install the .skill file in Codex Desktop first:
// output/heige-codex-skin-studio.skill

// Then in Codex chat, prompt:
// "Generate a pastel sakura landscape, 1920x1080, then create a Codex theme"

// Codex will execute (simplified):
const { generateImage } = require('./src/ai/image-generator.js');
const { generateThemeFromImage } = require('./src/utils/theme-generator.js');
const ThemeManager = require('./src/injector/theme-manager.js');

async function aiThemePipeline(prompt) {
  // 1. Generate image via Codex's internal DALL-E
  const imagePath = await generateImage(prompt, {
    size: '1920x1080',
    outputPath: './output/ai-generated.png'
  });

  // 2. Extract palette and generate theme
  const themeDir = './output/sakura-theme';
  await generateThemeFromImage(imagePath, themeDir, {
    themeName: 'AI Sakura',
    author: 'Codex AI'
  });

  // 3. Apply theme
  const tm = new ThemeManager();
  await tm.applyTheme(themeDir);

  console.log('✅ AI-generated theme applied!');
}

aiThemePipeline('pastel sakura landscape with cherry blossoms at sunset');
```

## License & Attribution

- **Code**: MIT License
- **Assets**: See `ASSET_PROVENANCE.md` for per-file sources and licensing
- **Trademarks**: Character/franchise assets (Miku, Genshin, etc.) are property of their respective owners; this project does not claim rights or grant licenses for redistribution

---

**Tip**: After installing, use the `🎨` menu in Codex Desktop for all theme operations. For programmatic control, import `src/injector/theme-manager.js` and call `applyTheme(themeId)`.
