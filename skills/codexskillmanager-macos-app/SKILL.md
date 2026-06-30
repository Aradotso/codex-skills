---
name: codexskillmanager-macos-app
description: Build and use CodexSkillManager, a macOS SwiftUI app for managing local and remote Codex/Claude skills
triggers:
  - how do I build CodexSkillManager
  - manage my Codex skills with CodexSkillManager
  - browse Clawdhub skills locally
  - import skills into Codex or Claude Code
  - render SKILL.md files in macOS
  - delete or organize my local Codex skills
  - download remote skills from Clawdhub
  - build a SwiftUI app with SwiftPM only
---

# Codex Skill Manager

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

CodexSkillManager is a native macOS SwiftUI application for managing local Codex and Claude Code skills. It browses `~/.codex/skills`, `~/.codex/skills/public`, and `~/.claude/skills`, renders `SKILL.md` files with Markdown, and lets you discover and download remote skills from Clawdhub.

## What It Does

- **Browse local skills**: Scans Codex and Claude skill directories
- **Render Markdown**: Displays `SKILL.md` with inline reference previews
- **Import skills**: Add skills from folders or zip archives
- **Delete skills**: Remove unwanted skills from the sidebar
- **Clawdhub integration**: Search and download remote skills
- **Visual tags**: Shows installation status (Codex/Claude) and version info
- **Author info**: Displays Clawdhub author details in skill views

## Requirements

- macOS 26+
- Swift 6.2+
- Xcode (for toolchain) or Swift toolchain installed

## Building the App

### Quick Build & Run

```bash
# Clone the repository
git clone https://github.com/Dimillian/CodexSkillManager.git
cd CodexSkillManager

# Build with Swift Package Manager
swift build

# Run directly
swift run CodexSkillManager
```

### Package as macOS App

```bash
# Use the provided script
./Scripts/compile_and_run.sh
```

This script compiles the app bundle and launches it. The resulting `.app` will be in the build directory.

### Manual Build for Release

```bash
# Build in release mode
swift build -c release

# The binary will be in .build/release/CodexSkillManager
.build/release/CodexSkillManager
```

## Project Structure

This project uses **SwiftPM only** (no Xcode project file):

```
CodexSkillManager/
├── Package.swift          # Swift package manifest
├── Sources/
│   └── CodexSkillManager/
│       ├── App.swift      # Main app entry point
│       ├── Views/         # SwiftUI views
│       ├── Models/        # Data models
│       └── Services/      # Skill loading, Clawdhub API
├── Scripts/
│   └── compile_and_run.sh
└── README.md
```

## Key Components

### Skill Directories

CodexSkillManager scans these default paths:

```swift
// Local skill directories
let codexSkillsPaths = [
    "~/.codex/skills",
    "~/.codex/skills/public",
    "~/.claude/skills"
]
```

### Skill Model Structure

Each skill is a directory containing a `SKILL.md` file:

```
my-skill/
├── SKILL.md              # Main skill definition
└── (optional files)      # Supporting code, examples
```

### SKILL.md Format

```yaml
---
name: example-skill
description: Brief description
triggers:
  - example trigger phrase
---

# Skill Content

Markdown content here...
```

## Common Usage Patterns

### Browsing Local Skills

1. Launch CodexSkillManager
2. Sidebar shows skills from all configured directories
3. Click a skill to view rendered `SKILL.md`
4. Tags show installation status: **Codex**, **Claude**, or both

### Importing a Skill

```swift
// Import from folder
SkillImporter.importFromFolder(at: folderURL, to: .codex)

// Import from zip
SkillImporter.importFromZip(at: zipURL, to: .claude)
```

**UI Flow:**
1. Click "Import Skill" button
2. Choose folder or zip file
3. Select destination: Codex or Claude Code
4. Skill appears in sidebar immediately

### Deleting a Skill

```swift
// Programmatic deletion
SkillManager.shared.delete(skill: skill, from: .codex)
```

**UI Flow:**
1. Right-click skill in sidebar
2. Select "Delete Skill"
3. Confirm deletion dialog
4. Skill removed from disk and sidebar

### Browsing Clawdhub Skills

```swift
// Fetch latest skills
ClawdhubService.shared.fetchLatestSkills { skills in
    // Update UI with remote skills
}

// Search skills
ClawdhubService.shared.search(query: "python") { results in
    // Display search results
}
```

**UI Flow:**
1. Switch to "Clawdhub" tab
2. Browse latest skills or search
3. Click skill to view details + author info
4. Download button installs to Codex/Claude

### Downloading Remote Skills

```swift
// Download to Codex
ClawdhubService.shared.download(skill: remoteSkill, to: .codex) { result in
    switch result {
    case .success(let localPath):
        print("Installed to \(localPath)")
    case .failure(let error):
        print("Download failed: \(error)")
    }
}
```

## SwiftUI Views

### Main App Structure

```swift
import SwiftUI

@main
struct CodexSkillManagerApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .frame(minWidth: 800, minHeight: 600)
        }
        .windowStyle(.hiddenTitleBar)
        .windowToolbarStyle(.unified)
    }
}
```

### Sidebar + Detail Pattern

```swift
struct ContentView: View {
    @State private var selectedSkill: Skill?
    @StateObject private var skillManager = SkillManager.shared
    
    var body: some View {
        NavigationSplitView {
            // Sidebar: skill list
            List(skillManager.skills, selection: $selectedSkill) { skill in
                SkillRow(skill: skill)
            }
        } detail: {
            // Detail: rendered SKILL.md
            if let skill = selectedSkill {
                SkillDetailView(skill: skill)
            } else {
                Text("Select a skill")
            }
        }
    }
}
```

### Markdown Rendering

CodexSkillManager uses [swift-markdown-ui](https://github.com/gonzalezreal/swift-markdown-ui):

```swift
import MarkdownUI

struct SkillDetailView: View {
    let skill: Skill
    
    var body: some View {
        ScrollView {
            Markdown(skill.content)
                .markdownTheme(.gitHub)
                .padding()
        }
    }
}
```

## Configuration

### Custom Skill Paths

Edit or extend the skill directory paths:

```swift
// In SkillManager.swift
class SkillManager: ObservableObject {
    let skillPaths = [
        FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent(".codex/skills"),
        FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent(".codex/skills/public"),
        FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent(".claude/skills"),
        // Add custom paths here
    ]
}
```

### Clawdhub API Endpoint

```swift
// In ClawdhubService.swift
let apiBaseURL = "https://clawdhub.com/api"

// Fetch latest skills
func fetchLatestSkills(completion: @escaping ([RemoteSkill]) -> Void) {
    let url = URL(string: "\(apiBaseURL)/skills/latest")!
    // URLSession request...
}
```

## Packaging & Distribution

### Create Standalone App Bundle

```bash
# Build release binary
swift build -c release

# Create app bundle structure
mkdir -p CodexSkillManager.app/Contents/MacOS
mkdir -p CodexSkillManager.app/Contents/Resources

# Copy binary
cp .build/release/CodexSkillManager \
   CodexSkillManager.app/Contents/MacOS/

# Create Info.plist
cat > CodexSkillManager.app/Contents/Info.plist <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>CodexSkillManager</string>
    <key>CFBundleIdentifier</key>
    <string>com.dimillian.CodexSkillManager</string>
    <key>CFBundleName</key>
    <string>CodexSkillManager</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>26.0</string>
</dict>
</plist>
EOF

# Launch
open CodexSkillManager.app
```

## Troubleshooting

### "Command not found: swift"

Ensure Swift toolchain is installed:

```bash
# Check Swift version
swift --version

# Install via Xcode or download from swift.org
xcode-select --install
```

### Skills Not Appearing

Check directory permissions:

```bash
# Verify skill directories exist
ls -la ~/.codex/skills
ls -la ~/.claude/skills

# Create if missing
mkdir -p ~/.codex/skills ~/.claude/skills
```

### Markdown Not Rendering

Ensure `SKILL.md` exists and is valid:

```bash
# Check skill directory
cd ~/.codex/skills/my-skill
cat SKILL.md

# Validate YAML frontmatter
head -n 10 SKILL.md
```

### Build Errors on macOS < 26

CodexSkillManager requires **macOS 26+**. For older macOS:

1. Fork the repository
2. Lower `platforms` in `Package.swift`:

```swift
platforms: [
    .macOS(.v14)  // Change from v26
]
```

3. Remove API calls unavailable in older macOS versions

### Clawdhub Connection Failed

Check network connectivity:

```bash
# Test API endpoint
curl https://clawdhub.com/api/skills/latest

# Check for firewall/proxy issues
```

If behind a corporate proxy, configure URLSession with proxy settings.

## Extending CodexSkillManager

### Add Custom Skill Source

```swift
// Create new skill provider
class CustomSkillProvider: SkillProvider {
    func fetchSkills() -> [Skill] {
        // Load from custom source
        return parseSkillsFromAPI()
    }
}

// Register in SkillManager
skillManager.addProvider(CustomSkillProvider())
```

### Custom Markdown Theme

```swift
import MarkdownUI

extension Theme {
    static let custom = Theme()
        .text {
            ForegroundColor(.primary)
            FontSize(14)
        }
        .code {
            FontFamilyVariant(.monospaced)
            BackgroundColor(.secondary.opacity(0.1))
        }
}

// Use in view
Markdown(content)
    .markdownTheme(.custom)
```

## Code Examples

### Programmatic Skill Installation

```swift
import Foundation

func installSkill(from url: URL, to destination: SkillDestination) throws {
    let skillName = url.lastPathComponent
    let targetPath = destination.basePath
        .appendingPathComponent(skillName)
    
    let fileManager = FileManager.default
    
    // Copy skill directory
    try fileManager.copyItem(at: url, to: targetPath)
    
    // Verify SKILL.md exists
    let skillMD = targetPath.appendingPathComponent("SKILL.md")
    guard fileManager.fileExists(atPath: skillMD.path) else {
        throw SkillError.invalidSkill
    }
    
    print("✅ Installed \(skillName) to \(destination)")
}

// Usage
let skillURL = URL(fileURLWithPath: "/path/to/my-skill")
try installSkill(from: skillURL, to: .codex)
```

### Parse Skill Metadata

```swift
import Foundation
import Yams

struct SkillMetadata: Codable {
    let name: String
    let description: String
    let triggers: [String]
}

func parseSkillMetadata(from markdownPath: URL) throws -> SkillMetadata {
    let content = try String(contentsOf: markdownPath)
    
    // Extract YAML frontmatter
    let pattern = #"^---\n(.*?)\n---"#
    let regex = try NSRegularExpression(pattern: pattern, options: .dotMatchesLineSeparators)
    
    guard let match = regex.firstMatch(in: content, range: NSRange(content.startIndex..., in: content)),
          let yamlRange = Range(match.range(at: 1), in: content) else {
        throw SkillError.noFrontmatter
    }
    
    let yamlString = String(content[yamlRange])
    let metadata = try YAMLDecoder().decode(SkillMetadata.self, from: yamlString)
    
    return metadata
}
```

## License

MIT License - see repository for full text.

## Resources

- **Repository**: https://github.com/Dimillian/CodexSkillManager
- **Clawdhub**: https://clawdhub.com
- **swift-markdown-ui**: https://github.com/gonzalezreal/swift-markdown-ui
- **Swift Package Manager**: https://swift.org/package-manager
