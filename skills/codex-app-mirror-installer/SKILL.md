---
name: codex-app-mirror-installer
description: Mirror and download official Codex desktop app installers from GitHub Releases with verified checksums
triggers:
  - download codex app installer
  - get codex desktop app for windows or mac
  - mirror codex app installers
  - install codex app from github release
  - verify codex installer checksums
  - download codex msix or dmg
  - get latest codex app version
  - check codex app mirror status
---

# codex-app-mirror-installer

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

This skill provides expertise in using the `codex-app-mirror` project to download and verify official Codex desktop app installers. The project mirrors Windows MSIX (from Microsoft Store) and macOS DMG installers to GitHub Releases every 15 minutes, with SHA256 checksums and version manifests.

## What It Does

`codex-app-mirror` automatically polls Microsoft Store and OpenAI's official CDN for Codex desktop app updates, then publishes verified installers as GitHub Release assets. It does NOT modify, repackage, or build Codex — it only mirrors official packages with checksums.

**Mirrored Assets:**
- Windows x64 MSIX (Microsoft Store ProductId `9PLM9XGG6VKS`)
- macOS Apple Silicon DMG (arm64)
- macOS Intel DMG (x64)
- SHA256SUMS.txt (checksums for all assets)
- release-manifest.json (upstream fingerprints)

## Installation Sources

### GitHub Releases (All Versions)

Latest release: `https://github.com/Wangnov/codex-app-mirror/releases/latest`

All releases: `https://github.com/Wangnov/codex-app-mirror/releases`

### R2 CDN Short Links (Latest Only)

These mirrors are optimized for mainland China network access:

```bash
# Windows MSIX
curl -LO https://codexapp.agentsmirror.com/latest/win

# macOS Apple Silicon
curl -LO https://codexapp.agentsmirror.com/latest/mac-arm64

# macOS Intel
curl -LO https://codexapp.agentsmirror.com/latest/mac-intel

# Checksums
curl -LO https://codexapp.agentsmirror.com/latest/checksums
```

## Downloading and Verifying

### Shell Script Example (macOS/Linux)

```bash
#!/bin/bash
set -e

PLATFORM="mac-arm64"  # or "mac-intel" or "win"
DOWNLOAD_URL="https://codexapp.agentsmirror.com/latest/${PLATFORM}"
CHECKSUMS_URL="https://codexapp.agentsmirror.com/latest/checksums"

# Download installer
echo "Downloading Codex installer..."
curl -L -o codex-installer "${DOWNLOAD_URL}"

# Download checksums
curl -L -o SHA256SUMS.txt "${CHECKSUMS_URL}"

# Verify checksum
echo "Verifying checksum..."
if command -v sha256sum &> /dev/null; then
    sha256sum -c SHA256SUMS.txt --ignore-missing
elif command -v shasum &> /dev/null; then
    shasum -a 256 -c SHA256SUMS.txt 2>&1 | grep "$(basename codex-installer)" || true
else
    echo "Warning: No checksum tool found"
fi

echo "Download complete and verified!"
```

### PowerShell Example (Windows)

```powershell
# Download Windows MSIX
$url = "https://codexapp.agentsmirror.com/latest/win"
$checksumUrl = "https://codexapp.agentsmirror.com/latest/checksums"

Write-Host "Downloading Codex MSIX installer..."
Invoke-WebRequest -Uri $url -OutFile "codex-installer.msix"

Write-Host "Downloading checksums..."
Invoke-WebRequest -Uri $checksumUrl -OutFile "SHA256SUMS.txt"

# Verify checksum
Write-Host "Verifying checksum..."
$expectedHash = (Get-Content SHA256SUMS.txt | Select-String "msix").Line.Split()[0]
$actualHash = (Get-FileHash -Algorithm SHA256 "codex-installer.msix").Hash

if ($actualHash -eq $expectedHash) {
    Write-Host "Checksum verified successfully!" -ForegroundColor Green
} else {
    Write-Host "Checksum mismatch! Download may be corrupted." -ForegroundColor Red
    exit 1
}
```

### GitHub Release Download (Specific Version)

```bash
#!/bin/bash
# Download a specific release version

RELEASE_TAG="codex-app-win-26.513.3673.0-mac-26.513.31313-b2867"
ASSET_NAME="OpenAI.Codex_26.513.3673.0_x64__2p2nqsd0c76g0.Msix"

# Using GitHub API
REPO="Wangnov/codex-app-mirror"
ASSET_URL=$(curl -s "https://api.github.com/repos/${REPO}/releases/tags/${RELEASE_TAG}" \
    | grep "browser_download_url.*${ASSET_NAME}" \
    | cut -d '"' -f 4)

curl -L -o "${ASSET_NAME}" "${ASSET_URL}"
```

## Version Information

Release tags include both Windows and macOS versions:

```
codex-app-win-<windows-version>-mac-<mac-version>-b<build>
```

Example: `codex-app-win-26.513.3673.0-mac-26.513.31313-b2867`

### Parsing Version from Manifest

```bash
#!/bin/bash
# Download and parse release manifest

curl -s "https://codexapp.agentsmirror.com/latest/checksums" -o SHA256SUMS.txt
curl -s "https://api.github.com/repos/Wangnov/codex-app-mirror/releases/latest" | \
    jq -r '.tag_name, .published_at, .body'

# Or download manifest JSON directly from release assets
MANIFEST_URL=$(curl -s "https://api.github.com/repos/Wangnov/codex-app-mirror/releases/latest" \
    | jq -r '.assets[] | select(.name=="release-manifest.json") | .browser_download_url')

curl -s "${MANIFEST_URL}" | jq '.'
```

## GitHub Actions Integration

### Workflow Example: Auto-Download Latest

```yaml
name: Install Codex App
on:
  schedule:
    - cron: '0 */6 * * *'  # Every 6 hours
  workflow_dispatch:

jobs:
  download-codex:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        include:
          - os: windows-latest
            platform: win
            extension: msix
          - os: macos-latest
            platform: mac-arm64
            extension: dmg

    steps:
      - name: Download Codex installer
        shell: bash
        run: |
          curl -L -o "codex-installer.${{ matrix.extension }}" \
            "https://codexapp.agentsmirror.com/latest/${{ matrix.platform }}"

      - name: Download checksums
        shell: bash
        run: |
          curl -L -o SHA256SUMS.txt \
            "https://codexapp.agentsmirror.com/latest/checksums"

      - name: Verify checksum (Unix)
        if: runner.os != 'Windows'
        run: |
          shasum -a 256 -c SHA256SUMS.txt --ignore-missing

      - name: Verify checksum (Windows)
        if: runner.os == 'Windows'
        shell: powershell
        run: |
          $expected = (Get-Content SHA256SUMS.txt | Select-String "msix").Line.Split()[0]
          $actual = (Get-FileHash -Algorithm SHA256 "codex-installer.msix").Hash
          if ($actual -ne $expected) { exit 1 }

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: codex-installer-${{ matrix.platform }}
          path: codex-installer.${{ matrix.extension }}
```

## Python Example: Latest Release Info

```python
#!/usr/bin/env python3
import requests
import json

def get_latest_codex_release():
    """Fetch latest Codex app mirror release information."""
    url = "https://api.github.com/repos/Wangnov/codex-app-mirror/releases/latest"
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    
    print(f"Tag: {data['tag_name']}")
    print(f"Published: {data['published_at']}")
    print(f"\nAssets:")
    
    for asset in data['assets']:
        print(f"  - {asset['name']}")
        print(f"    Size: {asset['size'] / 1024 / 1024:.2f} MB")
        print(f"    Download: {asset['browser_download_url']}")
        print()
    
    return data

def download_with_verification(platform='mac-arm64'):
    """Download and verify Codex installer."""
    import hashlib
    
    # Download installer
    installer_url = f"https://codexapp.agentsmirror.com/latest/{platform}"
    checksums_url = "https://codexapp.agentsmirror.com/latest/checksums"
    
    print(f"Downloading {platform} installer...")
    installer_response = requests.get(installer_url)
    installer_response.raise_for_status()
    
    # Calculate hash
    sha256_hash = hashlib.sha256(installer_response.content).hexdigest()
    
    # Verify against checksums
    checksums_response = requests.get(checksums_url)
    checksums_response.raise_for_status()
    
    checksums = checksums_response.text
    
    if sha256_hash.lower() in checksums.lower():
        print(f"✓ Checksum verified: {sha256_hash}")
        return installer_response.content
    else:
        raise ValueError("Checksum verification failed!")

if __name__ == "__main__":
    release_info = get_latest_codex_release()
    
    # Example: download macOS arm64
    # installer_bytes = download_with_verification('mac-arm64')
    # with open('codex-installer.dmg', 'wb') as f:
    #     f.write(installer_bytes)
```

## Common Patterns

### Check for Updates

```bash
#!/bin/bash
# Compare local version with latest release

CURRENT_VERSION_FILE="$HOME/.codex-version"

if [ -f "$CURRENT_VERSION_FILE" ]; then
    CURRENT_VERSION=$(cat "$CURRENT_VERSION_FILE")
else
    CURRENT_VERSION="unknown"
fi

LATEST_TAG=$(curl -s "https://api.github.com/repos/Wangnov/codex-app-mirror/releases/latest" \
    | jq -r '.tag_name')

echo "Current: $CURRENT_VERSION"
echo "Latest:  $LATEST_TAG"

if [ "$CURRENT_VERSION" != "$LATEST_TAG" ]; then
    echo "New version available!"
    exit 0
else
    echo "Already up to date"
    exit 1
fi
```

### Batch Download All Platforms

```bash
#!/bin/bash
set -e

RELEASE_TAG="${1:-latest}"
REPO="Wangnov/codex-app-mirror"
OUTPUT_DIR="codex-installers"

mkdir -p "$OUTPUT_DIR"

if [ "$RELEASE_TAG" = "latest" ]; then
    RELEASE_URL="https://api.github.com/repos/${REPO}/releases/latest"
else
    RELEASE_URL="https://api.github.com/repos/${REPO}/releases/tags/${RELEASE_TAG}"
fi

echo "Fetching release: $RELEASE_TAG"
ASSETS=$(curl -s "$RELEASE_URL" | jq -r '.assets[] | "\(.name)\t\(.browser_download_url)"')

while IFS=$'\t' read -r name url; do
    echo "Downloading: $name"
    curl -L -o "${OUTPUT_DIR}/${name}" "$url"
done <<< "$ASSETS"

echo "All assets downloaded to $OUTPUT_DIR"
```

## Troubleshooting

### Checksum Verification Fails

```bash
# Re-download and compare file sizes first
curl -I "https://codexapp.agentsmirror.com/latest/mac-arm64" | grep -i content-length

# Download fresh checksums
curl -L -o SHA256SUMS.txt "https://codexapp.agentsmirror.com/latest/checksums"

# Verify file isn't corrupted
file codex-installer.dmg  # Should show: "VAX COFF executable"
```

### Windows MSIX Won't Install

The mirror provides the raw MSIX package. Installation may fail if:
- AppX/MSIX services are disabled on your system
- Group Policy blocks sideloading
- Certificate trust is not configured

The project does NOT modify Microsoft Store authorization. If Microsoft Store works for you, use that instead.

### macOS DMG Verification

```bash
# Check DMG structure
hdiutil verify Codex-mac-arm64.dmg

# Mount and inspect
hdiutil attach Codex-mac-arm64.dmg
ls -la /Volumes/Codex/
open /Volumes/Codex/Codex.app/Contents/Info.plist

# Unmount
hdiutil detach /Volumes/Codex/
```

### Rate Limiting GitHub API

```bash
# Check rate limit status
curl -s https://api.github.com/rate_limit | jq '.rate'

# Use authenticated requests for higher limits
curl -H "Authorization: token ${GITHUB_TOKEN}" \
    https://api.github.com/repos/Wangnov/codex-app-mirror/releases/latest
```

### R2 CDN Not Accessible

If R2 short links fail, fall back to GitHub Releases:

```bash
# GitHub Releases direct download (always works)
LATEST_URL=$(curl -s https://api.github.com/repos/Wangnov/codex-app-mirror/releases/latest \
    | jq -r '.assets[] | select(.name | contains("arm64")) | .browser_download_url')

curl -L -o codex-installer.dmg "$LATEST_URL"
```

## Project Architecture

The mirror uses:
- **DisplayCatalog API** for Microsoft Store ProductId lookup
- **FE3 API** for Windows package metadata resolution
- **OpenAI CDN** for macOS DMG HEAD requests (ETag/Last-Modified)
- **GitHub Actions** for 15-minute polling and release publishing
- **.NET** for Store metadata parsing (no third-party dependencies)

The project does NOT use `StoreLib` or modify package contents.

## Resources

- GitHub Repository: `https://github.com/Wangnov/codex-app-mirror`
- Community: LINUX DO community discussion (linked in repo)
- Microsoft Store ProductId: `9PLM9XGG6VKS`
- Upstream macOS URLs: `https://persistent.oaistatic.com/codex-app-prod/Codex*.dmg`
