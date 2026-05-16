---
name: codex-plusplus-ios-simulator-tweak
description: Embed a headless iOS Simulator in Codex++ right panel with mirroring, touch input, and UI element annotations
triggers:
  - add iOS simulator to codex
  - embed simulator in codex panel
  - mirror ios simulator headless
  - annotate simulator UI elements
  - capture ios simulator frame
  - control simulator from codex
  - install codex++ ios simulator tweak
  - send touch events to simulator
---

# Codex++ iOS Simulator Tweak

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

A Codex++ tweak that adds an **iOS Simulator** tab to Codex's right panel. It mirrors a booted iOS simulator without opening `Simulator.app`, forwards touch and keyboard input, and lets you annotate simulator UI elements directly into Codex comments.

## What It Does

- Embeds a live iOS simulator view in Codex's right panel
- Mirrors simulator output through CoreSimulator IOSurface (headless)
- Forwards touch, drag, swipe, keyboard, and hardware button input
- Provides UI element annotations using the accessibility tree
- Device picker to switch between installed simulators
- Auto-boot capability when no simulator is running
- Screenshot and hardware control (Home, Lock, Side Button, Siri)

## Installation

### Prerequisites

1. **macOS** with full **Xcode** installed (not just Command Line Tools)
2. At least one iOS simulator runtime/device downloaded
3. Xcode command-line tools properly configured:

```bash
sudo xcode-select -s /Applications/Xcode.app
```

Verify Xcode path:

```bash
xcode-select -p
# Should output: /Applications/Xcode.app/Contents/Developer
```

### Install Codex++

First install [Codex++](https://github.com/b-nnett/codex-plusplus), the Codex extension framework.

### Install the Tweak

Clone or download this tweak into the Codex++ tweaks directory:

```bash
mkdir -p ~/Library/Application\ Support/codex-plusplus/tweaks/
cd ~/Library/Application\ Support/codex-plusplus/tweaks/
git clone https://github.com/b-nnett/codex-plusplus-ios-simulator.git ios-simulator
```

Or manually place the folder:

```text
~/Library/Application Support/codex-plusplus/tweaks/ios-simulator/
```

The tweak runs a preflight check on first launch and shows fix hints if dependencies are missing.

## Usage

### Opening the Simulator Panel

**Via UI:**
- Click the `+` menu in Codex's right panel
- Select **iOS Simulator** (appears below the divider)

**Via Keyboard:**
- Press `Cmd+Y`

### Controls

Once the panel is open:

- **Tap/Click**: Click anywhere on the simulator screen
- **Drag/Swipe**: Click and drag
- **Keyboard**: Type directly (focus is captured)
- **Hardware Buttons**:
  - Home button
  - Lock button
  - Side button
  - Siri button
- **Screenshot**: Capture current simulator state
- **Device Picker**: Dropdown to switch simulators
- **Auto-boot**: Toggle to automatically boot simulator when none is running

### Annotations

Annotation mode allows you to reference specific UI elements in Codex comments:

1. Click the **annotation button** in the simulator panel
2. Click on a UI element in the simulator
3. Write your comment in Codex's native comment UI

The tweak automatically includes:
- Element label and accessibility role
- Simulator device ID
- Element frame coordinates
- Marker point
- Viewport size

**Example annotation payload:**

```javascript
{
  "element": {
    "label": "Sign In",
    "role": "Button",
    "frame": { "x": 120, "y": 450, "width": 175, "height": 44 }
  },
  "simulator": "iPhone 15 Pro",
  "marker": { "x": 207.5, "y": 472 },
  "viewport": { "width": 393, "height": 852 }
}
```

Use cases:
- "Fix this button layout" → points to specific button
- "Why is this label truncated?" → includes label frame and text
- "Adjust spacing here" → marks exact coordinates

## File Structure

```text
ios-simulator/
├── index.js                    # Main Codex++ tweak entry point
├── helpers/
│   ├── sim-capture.swift       # Headless frame capture helper
│   └── sim-input.m             # Touch, keyboard, hardware button helper
├── manifest.json               # Tweak metadata
└── README.md
```

## Key Code Patterns

### Tweak Entry Point (index.js)

The main tweak file exports a Codex++ tweak object:

```javascript
module.exports = {
  name: 'iOS Simulator',
  icon: 'phone.fill',
  
  // Called when panel is opened
  onActivate(panel) {
    panel.setTitle('iOS Simulator');
    initializeSimulator(panel);
  },
  
  // Called when panel is closed
  onDeactivate() {
    stopHelpers();
    cleanupResources();
  },
  
  // Panel UI setup
  renderPanel(container) {
    const canvas = document.createElement('canvas');
    const controls = createControlBar();
    container.append(canvas, controls);
    return { canvas, controls };
  }
};
```

### Capturing Simulator Frames (sim-capture.swift)

The Swift helper uses CoreSimulator to capture IOSurface frames:

```swift
import Foundation
import CoreSimulator
import IOSurface

// Connect to simulator framebuffer
let device = SimDevice(udid: deviceUDID)
let surface = device.surface // IOSurface

// Capture loop
while isRunning {
    let surfaceRef = device.io.surface
    let baseAddress = IOSurfaceGetBaseAddress(surfaceRef)
    let width = IOSurfaceGetWidth(surfaceRef)
    let height = IOSurfaceGetHeight(surfaceRef)
    
    // Write raw frame to stdout
    fwrite(baseAddress, 1, width * height * 4, stdout)
    fflush(stdout)
    
    usleep(16667) // ~60fps
}
```

### Sending Input Events (sim-input.m)

The Objective-C helper sends touch and keyboard events:

```objc
#import <Foundation/Foundation.h>
#import <SimulatorKit/SimulatorKit.h>

// Send touch event
- (void)sendTouchAtX:(CGFloat)x y:(CGFloat)y phase:(NSString*)phase {
    SimDevice *device = [self deviceWithUDID:deviceUDID];
    SimDeviceIOClient *io = device.io;
    
    SimDeviceIOTouchEvent *event = [SimDeviceIOTouchEvent new];
    event.x = x;
    event.y = y;
    event.phase = [self phaseFromString:phase]; // began, moved, ended
    
    [io sendTouchEvent:event];
}

// Send keyboard input
- (void)sendKeyPress:(NSString*)key {
    SimDevice *device = [self deviceWithUDID:deviceUDID];
    [device.io sendKeyboardEvent:key];
}

// Hardware buttons
- (void)pressHomeButton {
    SimDevice *device = [self deviceWithUDID:deviceUDID];
    [device.io pressButton:SimDeviceIOButtonHome];
}
```

### Device Management

List available simulators:

```javascript
const { execSync } = require('child_process');

function getAvailableSimulators() {
  const output = execSync('xcrun simctl list devices --json', { encoding: 'utf8' });
  const data = JSON.parse(output);
  
  const devices = [];
  for (const runtime in data.devices) {
    for (const device of data.devices[runtime]) {
      if (device.isAvailable) {
        devices.push({
          udid: device.udid,
          name: device.name,
          state: device.state,
          runtime: runtime
        });
      }
    }
  }
  return devices;
}
```

Boot a simulator:

```javascript
function bootSimulator(udid) {
  execSync(`xcrun simctl boot ${udid}`, { encoding: 'utf8' });
}
```

Shutdown:

```javascript
function shutdownSimulator(udid) {
  execSync(`xcrun simctl shutdown ${udid}`, { encoding: 'utf8' });
}
```

## Configuration

The tweak compiles helper binaries on first use and caches them:

```text
~/Library/Caches/co.bennett.ios-simulator/
├── sim-capture          # Compiled Swift helper
└── sim-input            # Compiled Objective-C helper
```

No network requests are made. All compilation happens locally.

### manifest.json

```json
{
  "name": "iOS Simulator",
  "version": "1.0.0",
  "description": "Headless iOS Simulator for Codex++",
  "entry": "index.js",
  "permissions": [
    "process",
    "filesystem"
  ],
  "shortcuts": [
    {
      "key": "cmd+y",
      "action": "toggleSimulator"
    }
  ]
}
```

## Troubleshooting

### Preflight Check Failed

**Error:** "Xcode not found"

```bash
# Ensure Xcode is installed
xcode-select -p

# If pointing to Command Line Tools, fix with:
sudo xcode-select -s /Applications/Xcode.app
```

**Error:** "No simulators available"

```bash
# List available simulators
xcrun simctl list devices

# Download iOS runtimes in Xcode:
# Xcode → Settings → Platforms → [Download iOS runtime]
```

### Helper Compilation Fails

**Error:** "Swift compiler not found"

```bash
# Verify swiftc is available
which swiftc

# Should be under Xcode.app/Contents/Developer/
# If not, run: sudo xcode-select -s /Applications/Xcode.app
```

**Error:** "Framework not found: SimulatorKit"

```bash
# SimulatorKit is a private framework included with Xcode
# Ensure full Xcode is installed, not just Command Line Tools

# Check framework exists:
ls /Applications/Xcode.app/Contents/Developer/Library/PrivateFrameworks/SimulatorKit.framework
```

### Simulator Won't Boot

**Error:** "Unable to boot device in current state: Booted"

The simulator is already running. Use the device picker to select it, or shut it down first:

```bash
xcrun simctl shutdown <UDID>
```

**Error:** "Failed to boot device"

Check simulator logs:

```bash
xcrun simctl spawn booted log stream --predicate 'subsystem == "com.apple.CoreSimulator"'
```

### No Frame Output

**Symptom:** Black screen in Codex panel

1. Verify simulator is booted:
   ```bash
   xcrun simctl list devices | grep Booted
   ```

2. Check helper process is running:
   ```bash
   ps aux | grep sim-capture
   ```

3. Restart the panel (close and reopen with `Cmd+Y`)

### Touch Input Not Working

1. Ensure simulator window is not open in `Simulator.app` (conflicting input)
2. Check `sim-input` helper is running:
   ```bash
   ps aux | grep sim-input
   ```
3. Verify device UDID matches between capture and input helpers

### Annotations Return Empty Labels

**Cause:** App under test has poor accessibility labeling

**Solution:** Add accessibility labels to your UI elements:

```swift
// SwiftUI
Text("Sign In")
    .accessibilityLabel("Sign In Button")
    .accessibilityIdentifier("signInButton")

// UIKit
button.accessibilityLabel = "Sign In Button"
button.accessibilityIdentifier = "signInButton"
```

## Common Workflows

### Testing a SwiftUI App

1. Open simulator panel (`Cmd+Y`)
2. Select device from picker (e.g., "iPhone 15 Pro")
3. Launch your app from Xcode or command line:
   ```bash
   xcrun simctl launch <UDID> com.yourcompany.yourapp
   ```
4. Interact with UI in Codex panel
5. Annotate elements to document issues

### Debugging Layout Issues

1. Enable annotation mode
2. Click on the element with incorrect layout
3. Write comment: "This button is clipped on iPhone SE"
4. The annotation includes frame and viewport size for the agent to analyze

### Recording Interaction Sequences

```javascript
// Custom extension to record touch sequences
const touches = [];

panel.on('touch', (x, y, phase) => {
  touches.push({ x, y, phase, timestamp: Date.now() });
});

panel.on('annotate', () => {
  // Include touch sequence in annotation
  return { touches, viewport, element };
});
```

## Privacy & Security

- **No Screen Recording permission required** (uses CoreSimulator IOSurface directly)
- **No network requests** (all helpers compiled locally)
- **Helper processes stopped** when tweak deactivates
- **Cached binaries** stored in user cache directory only

## License

MIT
