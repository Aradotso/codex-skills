---
name: codex-storyboard-video-production
description: Create and manage AI video storyboard projects with automated asset generation through Codex Storyboard workspace
triggers:
  - create a video storyboard project
  - generate video assets for storyboard
  - open the storyboard workspace
  - manage storyboard shots and scenes
  - add visual design guidelines to video project
  - process storyboard generation queue
  - create short video script with shots
  - batch generate storyboard media assets
---

# Codex Storyboard Video Production

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

Codex Storyboard is a local-first multi-project storyboard workspace for video production. It enables you to create video projects with detailed shot breakdowns, manage scripts and visual descriptions, and automatically generate image/video assets using Image Generation, HyperFrames, or Remotion. All data is stored locally and accessed through MCP tools.

**Key capabilities:**
- Multi-project video storyboard management
- Shot-by-shot script and visual planning
- Automated asset generation and backfill
- Project-level DESIGN.md for visual consistency
- Multiple aspect ratios (9:16, 16:9, 3:4, 4:3, 1:1)
- Local media upload and preview
- Generation queue management

## Installation

### As Codex Plugin

```bash
codex plugin marketplace add Yuuhann1999/codex-storyboard
codex plugin add codex-storyboard@codex-storyboard
```

After installation, restart Codex or open a new conversation to load MCP tools.

### Standalone Development

```bash
git clone https://github.com/Yuuhann1999/codex-storyboard.git
cd codex-storyboard
npm start
```

Access at `http://127.0.0.1:43218`

## Configuration

### Data Directory

Plugin mode (default):
```
~/.codex-storyboard/
  projects.json
  projects/
    <project-id>/
      project.json
      DESIGN.md
      media/
      generation/
```

Custom data directory via environment variable:
```bash
export CODEX_STORYBOARD_DATA_DIR=/path/to/custom/data
```

Development mode uses `data/` in repository root.

### Port Configuration

Default port is `43218`. The server will auto-increment if occupied.

## Core Workflow

### 1. Open Storyboard Workspace

```text
@codex-storyboard open the Codex storyboard workspace
```

This starts the local server and returns a clickable URL like:
```
http://127.0.0.1:43218
```

### 2. Create a Video Project

**Full project creation with shots:**

```text
@codex-storyboard create a 9:16 vertical video storyboard project about "5 AI coding tips", 
suitable for TikTok, with 5-7 shots, each 3-5 seconds, fast-paced and clean style
```

The MCP tool `create_storyboard_project` supports:
- Project metadata (title, description, aspect ratio)
- Complete shot array (shot type, media type, duration, script, visual description, generation method)
- Optional DESIGN.md content for visual guidelines

**Minimal project creation:**

```text
@codex-storyboard create a new storyboard project called "Product Demo Video" in 16:9 format
```

### 3. Add or Modify Shots

**Add new shots:**

```text
@codex-storyboard add 3 more B-ROLL shots to the current project, 
each showing different code editor features with smooth transitions
```

**Modify existing shot:**

```text
@codex-storyboard update shot 3 to be 8 seconds long, 
change the visual description to "Close-up of keyboard typing with colorful syntax highlighting"
```

**Delete shot:**

```text
@codex-storyboard delete shot 5 from the current project
```

### 4. Add Visual Guidelines (DESIGN.md)

```text
@codex-storyboard add a DESIGN.md to the current project with these guidelines:
- Color palette: Dark mode (#1a1a1a background, #00ff88 accent)
- Typography: SF Pro Display, clean sans-serif
- Style: Minimalist tech aesthetic, high contrast
- Motion: Smooth 60fps, subtle zoom effects
- Composition: Rule of thirds, centered subjects
```

The DESIGN.md is stored at `projects/<project-id>/DESIGN.md` and used as context when generating assets.

### 5. Generate Assets

**Queue shots for generation:**

In the web UI, click "Generate Asset" on individual shots or use "Batch Generate" for multiple shots.

**Process generation queue:**

```text
@codex-storyboard process all pending generation tasks. 
Start with Image Generation for static shots, then HyperFrames for video shots
```

The agent will:
1. Read pending tasks via `get_storyboard_generation_tasks`
2. Generate assets using Image Generation, HyperFrames, or Remotion
3. Backfill completed assets using `complete_storyboard_generation_task`

## MCP Tools Reference

### Project Management

**list_storyboard_projects**
```javascript
// List all projects, optionally filter by title
{
  "titleContains": "AI tips" // optional
}
```

**create_storyboard_project**
```javascript
{
  "title": "Product Launch Video",
  "description": "30-second product showcase",
  "aspectRatio": "16:9",
  "shots": [
    {
      "shotType": "A-ROLL",
      "mediaType": "VIDEO",
      "duration": 5,
      "script": "Introducing our new AI-powered tool...",
      "visualDescription": "Product hero shot with dynamic lighting",
      "generationMethod": "hyperframes",
      "notes": "Emphasize sleek UI"
    }
  ],
  "designContent": "# Visual Guidelines\n\n## Brand Colors\n..." // optional
}
```

**get_storyboard_project**
```javascript
{
  "projectId": "proj_abc123"
}
```

**update_storyboard_project**
```javascript
{
  "projectId": "proj_abc123",
  "updates": {
    "title": "New Title",
    "aspectRatio": "9:16"
  }
}
```

**delete_storyboard_project**
```javascript
{
  "projectId": "proj_abc123"
}
```

### Shot Management

**add_storyboard_shot**
```javascript
{
  "projectId": "proj_abc123",
  "shot": {
    "shotType": "B-ROLL",
    "mediaType": "IMAGE",
    "duration": 4,
    "script": "",
    "visualDescription": "Sunset over mountains, golden hour lighting",
    "generationMethod": "image-generation"
  }
}
```

**update_storyboard_shot**
```javascript
{
  "projectId": "proj_abc123",
  "shotId": "shot_xyz789",
  "updates": {
    "duration": 6,
    "visualDescription": "Updated visual description"
  }
}
```

**delete_storyboard_shot**
```javascript
{
  "projectId": "proj_abc123",
  "shotId": "shot_xyz789"
}
```

### DESIGN.md Management

**get_storyboard_design**
```javascript
{
  "projectId": "proj_abc123"
}
```

**update_storyboard_design**
```javascript
{
  "projectId": "proj_abc123",
  "content": "# Visual Style Guide\n\n..."
}
```

**delete_storyboard_design**
```javascript
{
  "projectId": "proj_abc123"
}
```

### Generation Queue

**get_storyboard_generation_tasks**
```javascript
{
  "projectId": "proj_abc123" // optional, returns all if omitted
}
```

Returns tasks with status: `pending`, `claimed`, `completed`, or `failed`

**complete_storyboard_generation_task**
```javascript
{
  "taskId": "task_def456",
  "mediaUrl": "file:///path/to/generated/asset.mp4",
  "metadata": {
    "generatedAt": "2026-07-08T10:30:00Z",
    "method": "hyperframes",
    "prompt": "Actual prompt used..."
  }
}
```

## Common Patterns

### Creating a Complete Short-Form Video Project

```text
@codex-storyboard create a complete 9:16 TikTok-style video storyboard about "3 productivity hacks":

Project title: "3 Productivity Hacks for Developers"
Duration: 25-30 seconds total
Aspect ratio: 9:16

Shot breakdown:
1. A-ROLL: Hook (3s) - "Want to code faster? Here are 3 tricks..." 
   Visual: Face cam with animated text overlay
   Method: hyperframes

2. B-ROLL: Tip 1 (6s) - "First: Use keyboard shortcuts"
   Visual: Screen recording of IDE with shortcuts highlighted
   Method: remotion

3. B-ROLL: Tip 2 (6s) - "Second: Automate repetitive tasks"
   Visual: Terminal showing automation script running
   Method: remotion

4. B-ROLL: Tip 3 (6s) - "Third: Take regular breaks"
   Visual: Person stretching, nature background
   Method: hyperframes

5. A-ROLL: CTA (4s) - "Try these today! Follow for more tips"
   Visual: Face cam with subscribe animation
   Method: hyperframes

Include DESIGN.md with:
- Color scheme: Tech blue (#0066ff) and white
- Font: Montserrat Bold for titles
- Motion: Quick cuts, 0.3s transitions
- Style: High energy, modern, professional
```

### Batch Processing with Error Handling

```text
@codex-storyboard process all pending generation tasks for project "3 Productivity Hacks".

For each task:
1. Check the shot's generationMethod and DESIGN.md guidelines
2. Generate asset using appropriate service (Image Generation/HyperFrames/Remotion)
3. Save asset to project's media folder
4. Backfill using complete_storyboard_generation_task
5. If generation fails, mark as failed and continue to next task

Report progress and any errors encountered.
```

### Iterating on Visual Style

```text
@codex-storyboard I want to adjust the visual style for project "Product Demo".

Current DESIGN.md focuses on dark mode, but let's shift to:
- Light mode with white background (#ffffff)
- Pastel accent colors (#ff6b9d pink, #4ecdc4 teal)
- Softer, more playful aesthetic
- Rounded corners on UI elements
- Bouncy animation timing

Update the DESIGN.md and regenerate shots 2, 4, and 6 with the new style.
```

### Multi-Project Management

```text
@codex-storyboard show me all storyboard projects that contain "tutorial" in the title.
For each project, show:
- Total number of shots
- How many shots have completed assets
- How many are still pending generation
- Project aspect ratio
```

## Local API Endpoints

The storyboard workspace exposes a REST API on `127.0.0.1:43218`:

### Projects

```javascript
// List all projects
GET /api/projects

// Create project
POST /api/projects
{
  "title": "My Video",
  "description": "Video description",
  "aspectRatio": "16:9",
  "shots": [...], // optional
  "designContent": "..." // optional
}

// Get project
GET /api/projects/:projectId

// Update project
PATCH /api/projects/:projectId
{
  "title": "Updated Title",
  "aspectRatio": "9:16"
}

// Delete project
DELETE /api/projects/:projectId
```

### Shots

```javascript
// Add shot
POST /api/projects/:projectId/shots
{
  "shotType": "A-ROLL",
  "mediaType": "VIDEO",
  "duration": 5,
  ...
}

// Update shot
PATCH /api/projects/:projectId/shots/:shotId
{
  "duration": 8,
  "visualDescription": "New description"
}

// Delete shot
DELETE /api/projects/:projectId/shots/:shotId

// Upload media
POST /api/projects/:projectId/shots/:shotId/media
Content-Type: multipart/form-data
file: <binary>
```

### DESIGN.md

```javascript
// Get design guidelines
GET /api/projects/:projectId/design

// Update design guidelines
POST /api/projects/:projectId/design
{
  "content": "# Design Guidelines\n..."
}

// Delete design guidelines
DELETE /api/projects/:projectId/design
```

### Generation Queue

```javascript
// Get pending tasks
GET /api/generation/tasks?projectId=<id>

// Create task
POST /api/generation/tasks
{
  "projectId": "proj_123",
  "shotId": "shot_456",
  "generationMethod": "hyperframes"
}

// Claim task
POST /api/generation/tasks/:taskId/claim

// Complete task
POST /api/generation/tasks/:taskId/complete
{
  "mediaUrl": "file:///path/to/asset.mp4",
  "metadata": {...}
}

// Mark failed
POST /api/generation/tasks/:taskId/fail
{
  "error": "Generation timeout"
}
```

## Media Asset Guidelines

### Supported Formats

**Images:** PNG, JPEG, WebP, GIF  
**Videos:** MP4, WebM, MOV  
**Max file size:** 100MB per file

### Asset Storage

```
projects/<project-id>/
  media/
    shot_<shot-id>_<timestamp>.<ext>
  generation/
    <method>/
      <generation-artifacts>
```

### Manual Upload

In the web UI, click on empty shot media boxes or use "Local Upload" button. Files are copied to the project's `media/` folder and referenced in `project.json`.

## Troubleshooting

### MCP Tools Not Available

**Symptom:** Codex doesn't recognize `@codex-storyboard` or storyboard MCP tools

**Solution:**
```bash
# Reinstall plugin
codex plugin remove codex-storyboard
codex plugin marketplace add Yuuhann1999/codex-storyboard
codex plugin add codex-storyboard@codex-storyboard

# Restart Codex or open new conversation
```

### Server Won't Start

**Symptom:** "Address already in use" or connection refused

**Solution:**
```bash
# Check if port 43218 is occupied
lsof -i :43218

# Kill process or let server auto-increment port
# Server will try 43218, 43219, 43220, etc.
```

### Assets Not Generating

**Symptom:** Generation tasks stay in "pending" state

**Checklist:**
1. Verify Image Generation/HyperFrames/Remotion capabilities are available in Codex
2. Check DESIGN.md doesn't have conflicting requirements
3. Ensure shot's `visualDescription` is clear and detailed
4. Try claiming and processing tasks manually:

```text
@codex-storyboard get pending tasks for current project and try processing them one by one with detailed error logging
```

### Media Files Missing

**Symptom:** UI shows broken image/video icons

**Solution:**
```bash
# Check media directory exists and has correct permissions
ls -la ~/.codex-storyboard/projects/<project-id>/media/

# Verify mediaUrl in project.json points to existing file
cat ~/.codex-storyboard/projects/<project-id>/project.json | grep mediaUrl

# Re-upload or regenerate missing assets
```

### DESIGN.md Not Applied

**Symptom:** Generated assets don't match visual guidelines

**Best practices:**
- Be specific with color codes, fonts, and measurements
- Include examples or reference images in guidelines
- Specify motion timing and easing functions
- Separate technical constraints from creative direction
- Test with one shot before batch generating

**Example effective DESIGN.md:**
```markdown
# Visual Style Guide

## Color Palette
- Primary: #0066ff (Bright Blue)
- Secondary: #00ff88 (Neon Green)
- Background: #0a0a0a (Near Black)
- Text: #ffffff (White)

## Typography
- Headlines: Montserrat ExtraBold, 48-72pt
- Body: Inter Regular, 16-24pt
- Code: JetBrains Mono, 14pt

## Composition
- 16:9 safe zones: 10% padding on all sides
- Text overlays: bottom third, left-aligned
- Logo placement: top-right corner, 5% margin

## Motion Language
- Transitions: 0.3s ease-out
- Text animation: Fade in + slide up, 0.5s
- Timing: 60fps target, smooth interpolation

## Technical Constraints
- Max video bitrate: 10 Mbps
- Audio: 192 kbps AAC
- Codec: H.264, Profile High

## Reference Style
Modern tech aesthetic, inspired by Apple product videos and Vercel marketing.
```

## Best Practices

### 1. Start with Clear Project Scope

Define total duration, platform (TikTok/YouTube/Instagram), and target audience before creating shots.

### 2. Use A-ROLL for Scripted Content

A-ROLL shots should have detailed `script` field with exact dialogue. B-ROLL can have empty script.

### 3. Balance Shot Durations

- Hook: 2-4s
- Mid-content shots: 4-8s  
- CTA: 3-5s
- Total TikTok/Reels: 15-60s
- Total YouTube Shorts: 15-60s

### 4. Write Detailed Visual Descriptions

**Bad:**
```
"Person talking"
```

**Good:**
```
"Medium shot of developer sitting at desk, facing camera at 45° angle, 
soft natural lighting from left window, modern minimalist office background 
with plants, wearing casual blue shirt, gesturing enthusiastically"
```

### 5. Leverage DESIGN.md for Consistency

Create DESIGN.md before generating assets. Update it as you refine the style. Regenerate shots after major DESIGN.md changes.

### 6. Process Generation in Stages

1. Generate all Image Generation assets first (fastest)
2. Generate HyperFrames videos (medium)
3. Generate complex Remotion renders (slowest)

This allows earlier review and reduces wasted compute on style mismatches.

### 7. Version Control for Projects

```bash
# Back up important projects
cp -r ~/.codex-storyboard/projects/proj_abc123 ~/backups/

# Or use git
cd ~/.codex-storyboard
git init
git add projects/
git commit -m "Snapshot of video projects"
```

---

**Environment Variables:**
- `CODEX_STORYBOARD_DATA_DIR` - Custom data directory
- `PORT` - Custom server port (default: 43218)

**File Structure:**
```
~/.codex-storyboard/
├── projects.json              # Project index
└── projects/
    └── <project-id>/
        ├── project.json       # Project metadata + shots
        ├── DESIGN.md          # Visual guidelines
        ├── media/             # Uploaded/generated assets
        └── generation/        # Build artifacts
```
