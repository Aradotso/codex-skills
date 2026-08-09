---
name: codex-desktop-linux-installer
description: Unofficial Linux build and installer for OpenAI Codex Desktop with auto-updates, native packaging, and Computer Use support
triggers:
  - install codex desktop on linux
  - set up openai codex for linux
  - build codex desktop from source
  - enable linux computer use in codex
  - troubleshoot codex desktop linux install
  - update codex desktop linux package
  - configure codex auto-updater
  - create codex appimage for linux
---

# Codex Desktop Linux Installer

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

This skill helps you install, configure, and troubleshoot the unofficial Linux build of OpenAI Codex Desktop. The project converts the macOS-only `Codex.dmg` into a runnable Linux Electron app with native packages (`.deb`, `.rpm`, `.pkg.tar.zst`), AppImage support, and a Nix flake.

## What This Project Does

- **Converts macOS Codex Desktop to Linux**: Extracts and patches the upstream macOS Electron app for Linux
- **Native packaging**: Builds distro-specific packages with bundled Node.js runtime
- **Auto-updater**: Systemd service that detects upstream updates and rebuilds packages locally
- **Linux Computer Use**: Optional Rust MCP backend for desktop automation via AT-SPI, ydotool, and XDG Portal
- **Chrome plugin native host**: Auto-installs Linux native-messaging support for Chrome/Brave/Chromium
- **Single-instance management**: Tray icon and window focus handoff

## Installation

### Quick Install (Native Package)

```bash
# Clone the repository
git clone https://github.com/ilysenko/codex-desktop-linux.git
cd codex-desktop-linux

# Bootstrap: install deps, build app, create package, and install
make bootstrap-native
```

This detects your distro and installs the appropriate package format. For manual control:

```bash
# Just build and install (if deps already present)
make install-native

# Or step-by-step:
make build-app      # Generate codex-app/ from upstream DMG
make package        # Build native package for your distro
make install        # Install the package from dist/
```

### AppImage (No Package Manager)

```bash
make build-app
make appimage
./dist/codex-desktop-*.AppImage
```

AppImages don't include the auto-updater. To update manually:

```bash
git pull --ff-only
make build-app-fresh
make appimage
```

### NixOS / Nix

```bash
# Run directly
nix run github:ilysenko/codex-desktop-linux

# With Computer Use UI enabled
nix run github:ilysenko/codex-desktop-linux#computer-use-ui

# Dev shell with tooling
nix develop github:ilysenko/codex-desktop-linux
```

Enable Cachix binary cache:

```bash
cachix use codex-desktop-linux
```

### Handling noexec /tmp

If `/tmp` is mounted with `noexec`:

```bash
mkdir -p ~/tmp/codex-work ~/tmp/codex-cache
export TMPDIR=~/tmp/codex-work
export XDG_CACHE_HOME=~/tmp/codex-cache

# Run install commands in this shell
make bootstrap-native
```

## Configuration

### Linux Features (Optional Integrations)

Optional features live in `linux-features/`. Enable them before building:

```bash
cp linux-features/features.example.json linux-features/features.json
# Edit features.json to enable desired features
make build-app
```

See `linux-features/README.md` for the feature contract.

### Computer Use UI (Opt-In)

The MCP backend registers by default, but the UI controls are opt-in:

```bash
# One-time build with UI enabled
CODEX_LINUX_ENABLE_COMPUTER_USE_UI=1 make build-app

# Persistent setting (picked up by auto-updater)
mkdir -p ~/.config/codex-desktop
echo '{"codex-linux-computer-use-ui-enabled": true}' > ~/.config/codex-desktop/settings.json
make build-app
```

Or via Nix:

```bash
nix run github:ilysenko/codex-desktop-linux#computer-use-ui
```

Combine with features:

```bash
nix run github:ilysenko/codex-desktop-linux#computer-use-ui-remote-mobile-control
```

### Auto-Updater Configuration

The systemd user service checks for updates every 6 hours:

```bash
# Check service status
systemctl --user status codex-update-manager.service

# View logs
journalctl --user -u codex-update-manager.service -f

# Restart service
systemctl --user restart codex-update-manager.service

# Disable auto-updates
systemctl --user disable --now codex-update-manager.service
```

Update builder location: `/opt/codex-desktop/update-builder`

## Linux Computer Use Setup

Computer Use requires `ydotool` and proper permissions:

```bash
# Debian/Ubuntu
sudo apt install ydotool ydotoold  # ydotoold may be separate package

# Fedora
sudo dnf install ydotool

# Arch
sudo pacman -S ydotool

# openSUSE
sudo zypper install ydotool

# Enable ydotoold service
sudo systemctl enable --now ydotoold  # or ydotool.service on Fedora 44

# Add user to input group (required for /dev/uinput access)
sudo usermod -a -G input "$USER"
# Re-login for group membership to take effect
```

### Verify Computer Use Readiness

```bash
# Run diagnostics
./codex-app/resources/plugins/openai-bundled/plugins/computer-use/bin/codex-computer-use-linux doctor

# Enable GNOME accessibility
./codex-app/resources/plugins/openai-bundled/plugins/computer-use/bin/codex-computer-use-linux setup

# Test components
./codex-app/resources/plugins/openai-bundled/plugins/computer-use/bin/codex-computer-use-linux apps
./codex-app/resources/plugins/openai-bundled/plugins/computer-use/bin/codex-computer-use-linux windows
./codex-app/resources/plugins/openai-bundled/plugins/computer-use/bin/codex-computer-use-linux screenshot
```

Or ask Codex in-app:

> Check whether Linux Computer Use is ready

### Desktop Environment Requirements

- **GNOME**: Works out of the box (uses GNOME Shell DBus for screenshots)
- **KDE Plasma**: Needs `xdg-desktop-portal-kde`
- **Sway/Hyprland**: Needs `xdg-desktop-portal-wlr`
- **i3**: Needs your distro's XDG Portal backend

Window management is supported on GNOME, KWin/Plasma, Hyprland, and i3.

## Key Commands

### Build Commands

```bash
make bootstrap-native      # Full bootstrap: deps + build + package + install
make install-native        # Build + package + install (deps assumed present)
make build-app             # Generate codex-app/ from upstream DMG
make build-app-fresh       # Force fresh download of upstream DMG
make package               # Build native package for detected distro
make install               # Install package from dist/
make appimage              # Build AppImage (requires build-app first)
make run-app               # Run the built app without installing
```

### Development Commands

```bash
make build-dev-app         # Build side-by-side dev variant (different app ID)
make run-dev-app           # Run dev variant
make clean                 # Remove build artifacts
make clean-app             # Remove codex-app/ only
```

Override dev identity:

```bash
DEV_APP_ID=com.example.codex.dev \
DEV_APP_NAME="Codex Desktop Dev" \
CODEX_WEBVIEW_PORT=8081 \
make build-dev-app
```

### Package-Specific Install

```bash
make install-deb           # Force .deb install
make install-rpm           # Force .rpm install
make install-pacman        # Force .pkg.tar.zst install
```

## Code Examples

### Rust: Custom Linux Feature

Create a new feature in `linux-features/my-feature/`:

```rust
// linux-features/my-feature/src/main.rs
use std::env;
use std::fs;
use std::path::PathBuf;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let codex_app = PathBuf::from(env::var("CODEX_APP_DIR")?);
    let resources = codex_app.join("resources");
    
    // Patch main.js
    let main_js = resources.join("app.asar.unpacked/dist/main.js");
    let content = fs::read_to_string(&main_js)?;
    let patched = content.replace(
        "// FEATURE_HOOK",
        "require('./my-feature-init.js');"
    );
    fs::write(&main_js, patched)?;
    
    // Copy integration script
    fs::copy(
        "linux-features/my-feature/my-feature-init.js",
        resources.join("app.asar.unpacked/dist/my-feature-init.js")
    )?;
    
    Ok(())
}
```

Enable in `linux-features/features.json`:

```json
{
  "enabled": ["my-feature"]
}
```

### Rust: Computer Use Plugin Extension

Extend the Computer Use backend:

```rust
// Custom accessibility query
use atspi::AccessibilityConnection;
use atspi::accessible::AccessibleProxy;

async fn find_widget_by_name(conn: &AccessibilityConnection, name: &str) -> Option<AccessibleProxy> {
    let desktop = conn.get_desktop(0).await.ok()?;
    let children = desktop.get_children().await.ok()?;
    
    for child in children {
        if let Ok(child_name) = child.get_name().await {
            if child_name.contains(name) {
                return Some(child);
            }
        }
    }
    None
}
```

### Shell: Custom Update Hook

Add a post-update script that runs after auto-updater installs:

```bash
#!/bin/bash
# ~/.config/codex-desktop/post-update.sh

# Reapply custom patches
cd ~/codex-desktop-linux
git pull --ff-only

# Enable custom features
cp linux-features/features.json.backup linux-features/features.json

# Rebuild if needed
if [ -n "$CODEX_VERSION_CHANGED" ]; then
    make build-app
fi
```

Make executable and reference in systemd override:

```bash
chmod +x ~/.config/codex-desktop/post-update.sh

mkdir -p ~/.config/systemd/user/codex-update-manager.service.d
cat > ~/.config/systemd/user/codex-update-manager.service.d/override.conf <<EOF
[Service]
ExecStartPost=/home/USER/.config/codex-desktop/post-update.sh
EOF

systemctl --user daemon-reload
systemctl --user restart codex-update-manager.service
```

## Troubleshooting

### App Won't Launch

```bash
# Check desktop entry
cat ~/.local/share/applications/codex-desktop.desktop

# Run manually to see errors
/opt/codex-desktop/codex-desktop --enable-logging --v=1

# Check Electron sandbox permissions
ls -la /opt/codex-desktop/chrome-sandbox

# Try disabling GPU acceleration
/opt/codex-desktop/codex-desktop --disable-gpu
```

### Computer Use Permission Denied

```bash
# Verify ydotool socket access
ls -la "$XDG_RUNTIME_DIR/.ydotool_socket"

# Check group membership (must show 'input')
groups

# If 'input' missing, add and re-login
sudo usermod -a -G input "$USER"

# Verify ydotoold is running
systemctl status ydotoold.service  # or ydotool.service

# Test direct ydotool command
ydotool type "test"
```

### Auto-Updater Not Running

```bash
# Check service status
systemctl --user status codex-update-manager.service

# View detailed logs
journalctl --user -u codex-update-manager.service --no-pager

# Manually trigger update check
systemctl --user restart codex-update-manager.service

# Check polkit policy
cat /usr/share/polkit-1/actions/com.codex.desktop.update.policy
```

### Package Build Fails

```bash
# Clean and retry
make clean
make bootstrap-native

# Check disk space
df -h /tmp

# Try with custom tmp directory
export TMPDIR=~/tmp/codex-work
mkdir -p "$TMPDIR"
make build-app

# Verify dependencies
make check-deps  # If available, or manually check rust, node, etc.
```

### DMG Extraction Fails

```bash
# Force fresh download
rm -rf ~/.cache/codex-desktop-linux/Codex.dmg
make build-app-fresh

# Check network/proxy
curl -I https://codex-desktop-builds.openai.com/latest/Codex.dmg

# Verify 7z is installed
7z --help
```

### Wayland Issues

```bash
# Force Wayland platform
/opt/codex-desktop/codex-desktop --ozone-platform=wayland

# Force X11 through XWayland
/opt/codex-desktop/codex-desktop --ozone-platform=x11

# Check current session type
echo $XDG_SESSION_TYPE
```

### CLI Preflight Debugging

```bash
# Enable verbose CLI checks at launch
CODEX_SYNC_CLI_PREFLIGHT=1 /opt/codex-desktop/codex-desktop

# Manually verify CLI install
npx @openai/codex --version

# Use bundled npm
/opt/codex-desktop/resources/node/bin/npm list -g @openai/codex
```

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `CODEX_LINUX_ENABLE_COMPUTER_USE_UI` | Enable Computer Use UI for one build |
| `CODEX_SYNC_CLI_PREFLIGHT` | Verbose CLI checks at launch |
| `TMPDIR` | Override temp directory for builds |
| `XDG_CACHE_HOME` | Override cache directory |
| `DEV_APP_ID` | Custom app ID for dev builds |
| `DEV_APP_NAME` | Custom app name for dev builds |
| `CODEX_WEBVIEW_PORT` | Override webview port (dev builds) |

## Common Patterns

### Building for Multiple Distros

```bash
# Build in Docker for consistent environment
docker run -v $(pwd):/work -w /work ubuntu:22.04 bash -c "
  apt update && apt install -y build-essential curl
  make bootstrap-native
"

# Or use Nix for reproducible builds
nix build github:ilysenko/codex-desktop-linux
```

### Custom Feature Development Workflow

```bash
# 1. Create feature directory
mkdir -p linux-features/my-feature/src

# 2. Implement feature (see Rust example above)
# 3. Add to features.json
echo '{"enabled": ["my-feature"]}' > linux-features/features.json

# 4. Build and test
make build-dev-app
make run-dev-app

# 5. Package for production
make build-app
make package
```

### Automated Testing Setup

```bash
#!/bin/bash
# ci-test.sh

set -e

# Build app
make build-app

# Run Computer Use diagnostics
./codex-app/resources/plugins/openai-bundled/plugins/computer-use/bin/codex-computer-use-linux doctor

# Verify package builds
make package

# Check package contents
dpkg-deb -c dist/codex-desktop_*.deb  # For Debian/Ubuntu
# or
rpm -qlp dist/codex-desktop-*.rpm     # For Fedora/SUSE
# or
tar -tf dist/codex-desktop-*.pkg.tar.zst  # For Arch
```

## Platform Support Matrix

| Distro Family | Package Format | Auto-Updater | Notes |
|---------------|----------------|--------------|-------|
| Debian/Ubuntu | `.deb` | ✅ | Bundled Node.js runtime |
| Fedora | `.rpm` | ✅ | dnf5 for Fedora 41+ |
| openSUSE | `.rpm` | ✅ | Uses `zypper --no-gpg-checks` |
| Arch/Manjaro | `.pkg.tar.zst` | ✅ | pacman |
| AppImage | `.AppImage` | ❌ | Manual rebuild required |
| NixOS | flake | N/A | Reproducible, cached |

## Resources

- **Repository**: https://github.com/ilysenko/codex-desktop-linux
- **Contributing**: Read `CONTRIBUTING.md` before opening PRs
- **Linux Features**: See `linux-features/README.md` for feature contract
- **Computer Use Author**: [@avifenesh](https://github.com/avifenesh)
- **Upstream**: [OpenAI Codex Desktop](https://openai.com/codex/)
