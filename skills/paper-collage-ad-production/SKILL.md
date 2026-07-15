---
name: paper-collage-ad-production
description: Complete paper-cut collage ad production pipeline with local IndexTTS-2 voice cloning, animation, audio mixing, and MP4 quality control for Codex
triggers:
  - "create a paper collage ad for this product"
  - "make a 45 second cutout animation commercial"
  - "generate a paper-cut style advertisement with voice"
  - "produce a collage ad with local voice cloning"
  - "build an animated paper craft ad with IndexTTS"
  - "set up paper collage ad production workflow"
  - "render a stop-motion style ad with narration"
  - "make a papercraft commercial with audio"
---

# Paper Collage Ad Production

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

A complete production pipeline for paper-cut/collage style advertisements. Handles creative ideation, scripting, storyboarding, keyframe generation, animation (via Seedance/HyperFrames/layered PNG/FFmpeg), local voice cloning with IndexTTS-2 MLX, music/SFX integration, and final H.264/AAC MP4 with quality validation.

## Installation

**Global install** (available to all Codex projects):

```bash
git clone https://github.com/Jane-xiaoer/paper-collage-ad-codex.git \
  ~/.codex/skills/paper-collage-ad
```

**Project-local install**:

```bash
mkdir -p .codex/skills
git clone https://github.com/Jane-xiaoer/paper-collage-ad-codex.git \
  .codex/skills/paper-collage-ad
```

Restart Codex or start a new task, then say:

```text
Use paper-collage-ad to create a 45-second paper-cut ad for this product.
```

Codex will read `SKILL.md` and call `references/`, `examples/`, and `scripts/` as needed.

## System Dependencies

**macOS**:

```bash
brew install ffmpeg node
bash scripts/check-deps.sh
```

**Environment variables** (optional services):

```bash
export SEEDANCE_API_KEY="your-key"
export JIMENG_API_KEY="your-key"
export MINIMAX_API_KEY="your-key"
export ELEVENLABS_API_KEY="your-key"
```

For static keyframes and layered animation, **no API keys required**.

## Core Workflow

### 1. Project Structure

```text
<project>/
  assets/
    brand/                 # logos, product images, brand colors
    keyframes/             # generated paper-cut style frames
    voice-reference/       # reference.wav (6-12s, authorized)
    voice-model/           # speaker-v2.npz (local, not in Git)
    voice-final/           # 01.wav, 02.wav... (generated narration)
    music/                 # background music
    sfx/                   # sound effects
  manifests/
    storyboard.json        # scene timing, script, visual descriptions
    voice.indextts2.json   # narration manifest for IndexTTS-2
  output/
    final.mp4              # rendered ad
```

**Privacy template**:

```bash
cp examples/project.gitignore "<project>/.gitignore"
```

### 2. Storyboard & Script

Create or modify storyboard:

```bash
cp examples/storyboard.json "<project>/manifests/storyboard.json"
```

**Example storyboard.json**:

```json
{
  "title": "Product Launch Ad",
  "duration": 45,
  "scenes": [
    {
      "id": "01",
      "duration": 5,
      "timecode": "00:00-00:05",
      "visual": "Paper-cut sun rising over layered hills",
      "narration": "Every morning starts with possibility.",
      "emotion": "warm"
    },
    {
      "id": "02",
      "duration": 8,
      "timecode": "00:05-00:13",
      "visual": "Hand places product center stage, paper petals unfold",
      "narration": "Introducing the new SmartWidget.",
      "emotion": "excited"
    }
  ]
}
```

### 3. Keyframe Generation

Generate paper-cut style keyframes from brand assets and scene descriptions:

```javascript
// scripts/generate-keyframes.mjs
import fs from 'fs';
import path from 'path';

const storyboard = JSON.parse(fs.readFileSync('manifests/storyboard.json', 'utf-8'));
const brandColors = ['#FF6B6B', '#4ECDC4', '#FFE66D'];

for (const scene of storyboard.scenes) {
  console.log(`Scene ${scene.id}: ${scene.visual}`);
  // Generate layered PNG with paper texture, shadows, brand colors
  // Output: assets/keyframes/scene-${scene.id}.png
}
```

Run:

```bash
node scripts/generate-keyframes.mjs --storyboard manifests/storyboard.json
```

### 4. Animation

**Option A: Static layered animation** (no external API):

```bash
node scripts/animate-layers.mjs \
  --keyframes assets/keyframes/ \
  --storyboard manifests/storyboard.json \
  --output output/video-silent.mp4
```

**Option B: Seedance API**:

```javascript
// scripts/animate-seedance.mjs
import axios from 'axios';

const apiKey = process.env.SEEDANCE_API_KEY;

async function animateScene(sceneId, keyframePath, motion) {
  const formData = new FormData();
  formData.append('image', fs.createReadStream(keyframePath));
  formData.append('motion', motion); // 'pan-right', 'zoom-in', 'rotate-ccw'
  formData.append('duration', 5);

  const response = await axios.post('https://api.seedance.ai/v1/animate', formData, {
    headers: { 'Authorization': `Bearer ${apiKey}` }
  });

  return response.data.video_url;
}
```

### 5. Voice Cloning with IndexTTS-2 MLX

**Setup IndexTTS-2** (Apple Silicon Mac):

```bash
bash scripts/setup-indextts2-mlx.sh
```

Installs to `~/.local/share/paper-collage-ad/mlx-indextts/models/mlx-indextts2-standard-fp16/`

**Prepare voice model** (use only authorized voice samples):

```bash
bash scripts/prepare-indextts2-voice.sh \
  "assets/voice-reference/reference.wav" \
  "assets/voice-model/speaker-v2.npz" \
  --i-have-permission
```

**Create voice manifest**:

```bash
cp examples/voice-manifest.indextts2.json manifests/voice.indextts2.json
```

**Example voice manifest**:

```json
{
  "speaker_model": "assets/voice-model/speaker-v2.npz",
  "output_dir": "assets/voice-final",
  "sample_rate": 48000,
  "lines": [
    {
      "id": "01",
      "text": "Every morning starts with possibility.",
      "emotion": "warm",
      "speed": 1.0
    },
    {
      "id": "02",
      "text": "Introducing the new SmartWidget.",
      "emotion": "excited",
      "speed": 1.05
    }
  ]
}
```

**Generate narration**:

```bash
node scripts/narrate-indextts2.mjs \
  --manifest manifests/voice.indextts2.json
```

Output: `assets/voice-final/01.wav`, `02.wav`, etc. (48 kHz WAV)

**IndexTTS-2 emotion tags**: `neutral`, `happy`, `sad`, `angry`, `surprised`, `fearful`, `warm`, `excited`

### 6. Audio Mixing

Combine video, narration, music, and SFX:

```bash
node scripts/mix-audio.mjs \
  --video output/video-silent.mp4 \
  --narration assets/voice-final/ \
  --music assets/music/background.mp3 \
  --sfx assets/sfx/ \
  --storyboard manifests/storyboard.json \
  --output output/final.mp4
```

**Example mix script**:

```javascript
// scripts/mix-audio.mjs
import { execSync } from 'child_process';
import fs from 'fs';

const storyboard = JSON.parse(fs.readFileSync(args.storyboard, 'utf-8'));

// Build FFmpeg filter complex
let filterComplex = '[1:a]volume=0.3[music];'; // Background music at 30%

storyboard.scenes.forEach((scene, i) => {
  const narrationPath = `assets/voice-final/${scene.id}.wav`;
  const delay = scene.timecode.split('-')[0]; // e.g., "00:05"
  filterComplex += `[${i+2}:a]adelay=${timeToMs(delay)}|${timeToMs(delay)}[n${i}];`;
});

filterComplex += `[music]${storyboard.scenes.map((_, i) => `[n${i}]`).join('')}amix=inputs=${storyboard.scenes.length+1}:duration=longest[audio]`;

const cmd = `ffmpeg -i ${args.video} -i ${args.music} ${storyboard.scenes.map(s => `-i assets/voice-final/${s.id}.wav`).join(' ')} -filter_complex "${filterComplex}" -map 0:v -map "[audio]" -c:v copy -c:a aac -b:a 192k ${args.output}`;

execSync(cmd);
```

### 7. Quality Control

Validate final MP4:

```bash
bash scripts/qc-mp4.sh output/final.mp4
```

Checks:
- H.264 codec
- AAC audio
- Resolution ≥ 1080p
- Frame rate consistency
- Audio sync
- File size

**Example QC script**:

```bash
#!/bin/bash
# scripts/qc-mp4.sh

FILE=$1

# Check video codec
VCODEC=$(ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$FILE")
if [ "$VCODEC" != "h264" ]; then
  echo "❌ Video codec must be H.264, found: $VCODEC"
  exit 1
fi

# Check audio codec
ACODEC=$(ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$FILE")
if [ "$ACODEC" != "aac" ]; then
  echo "❌ Audio codec must be AAC, found: $ACODEC"
  exit 1
fi

# Check resolution
HEIGHT=$(ffprobe -v error -select_streams v:0 -show_entries stream=height -of default=noprint_wrappers=1:nokey=1 "$FILE")
if [ "$HEIGHT" -lt 1080 ]; then
  echo "❌ Resolution too low: ${HEIGHT}p (minimum 1080p)"
  exit 1
fi

echo "✅ QC passed: $FILE"
```

## Common Patterns

### Full Pipeline (One Command)

```bash
node scripts/full-pipeline.mjs \
  --product "SmartWidget Pro" \
  --duration 45 \
  --voice-ref assets/voice-reference/reference.wav \
  --brand-assets assets/brand/ \
  --output output/final.mp4
```

### Custom Animation Script

```javascript
// Animate scene with paper texture and parallax
import { createCanvas, loadImage } from 'canvas';

async function animateScene(keyframePath, duration, fps = 30) {
  const frames = duration * fps;
  const img = await loadImage(keyframePath);
  
  for (let i = 0; i < frames; i++) {
    const canvas = createCanvas(1920, 1080);
    const ctx = canvas.getContext('2d');
    
    // Parallax: move layers at different speeds
    const offset = (i / frames) * 100;
    ctx.drawImage(img, -offset * 0.5, 0); // Background layer
    ctx.drawImage(img, -offset * 1.0, 0); // Foreground layer
    
    // Add paper texture overlay
    ctx.globalAlpha = 0.1;
    ctx.fillStyle = '#FFF8E7';
    ctx.fillRect(0, 0, 1920, 1080);
    
    fs.writeFileSync(`frames/frame-${i.toString().padStart(4, '0')}.png`, canvas.toBuffer());
  }
}
```

### Voice Model Reuse

Once you have `speaker-v2.npz`, reuse across projects:

```bash
# Copy voice model to new project
cp ~/my-voice/speaker-v2.npz new-project/assets/voice-model/

# Update manifest
node scripts/narrate-indextts2.mjs \
  --manifest new-project/manifests/voice.indextts2.json
```

### Batch Scene Rendering

```javascript
// scripts/batch-render.mjs
import { promisify } from 'util';
import { exec } from 'child_process';

const execAsync = promisify(exec);

const scenes = ['01', '02', '03', '04'];

await Promise.all(scenes.map(async (sceneId) => {
  await execAsync(`node scripts/render-scene.mjs --id ${sceneId}`);
  console.log(`✅ Scene ${sceneId} rendered`);
}));
```

## Troubleshooting

### IndexTTS-2 Installation Fails

**Problem**: `mlx` package not found

**Solution**: Ensure Python 3.10+ and Apple Silicon Mac:

```bash
python3 --version  # Must be 3.10+
uname -m           # Must be arm64
pip3 install mlx mlx-lm
```

### Voice Cloning Sounds Robotic

**Problem**: Poor reference audio quality

**Solution**:
- Use 6-12 seconds of clean, single-speaker audio
- Remove background noise with Audacity
- Ensure 48 kHz sample rate: `ffmpeg -i input.wav -ar 48000 output.wav`
- Avoid accents, music, or multiple speakers

### FFmpeg Audio Sync Issues

**Problem**: Narration out of sync with video

**Solution**: Check timecodes in storyboard:

```javascript
// Convert timecode to milliseconds
function timeToMs(timecode) {
  const [min, sec] = timecode.split(':').map(Number);
  return (min * 60 + sec) * 1000;
}

// Verify scene durations sum to total
const totalDuration = storyboard.scenes.reduce((sum, s) => sum + s.duration, 0);
console.log(`Total: ${totalDuration}s, Expected: ${storyboard.duration}s`);
```

### Keyframe Generation Slow

**Problem**: Large brand assets slow down rendering

**Solution**: Pre-resize assets:

```bash
for img in assets/brand/*.png; do
  ffmpeg -i "$img" -vf "scale=1920:-1" "assets/brand/resized/$(basename $img)"
done
```

### Missing Paper Texture

**Problem**: Collage looks too digital

**Solution**: Apply grain and texture overlay:

```javascript
// Add to render pipeline
ctx.globalAlpha = 0.15;
ctx.fillStyle = ctx.createPattern(await loadImage('assets/textures/paper.png'), 'repeat');
ctx.fillRect(0, 0, canvas.width, canvas.height);
```

## Key Scripts Reference

| Script | Purpose |
|--------|---------|
| `check-deps.sh` | Verify system dependencies |
| `setup-indextts2-mlx.sh` | Install IndexTTS-2 runtime |
| `prepare-indextts2-voice.sh` | Generate speaker model from reference |
| `narrate-indextts2.mjs` | Synthesize narration from manifest |
| `generate-keyframes.mjs` | Create paper-cut style frames |
| `animate-layers.mjs` | Static layered animation |
| `animate-seedance.mjs` | Seedance API animation |
| `mix-audio.mjs` | Combine video, narration, music, SFX |
| `qc-mp4.sh` | Validate final MP4 |
| `privacy-check.sh` | Scan for secrets before commit |

## References

- `references/storyboard.md` – Scene structure, timing, pacing
- `references/visual-style.md` – Paper-cut aesthetics, brand integration
- `references/animation.md` – Motion techniques, parallax, transitions
- `references/voice.md` – IndexTTS-2 usage, emotion control
- `references/music.md` – Background music, SFX timing
- `references/qc.md` – MP4 validation checklist

## Privacy & Security

- **Never commit**:
  - Voice reference files (`voice-reference/`)
  - Speaker models (`voice-model/`)
  - Generated narration (`voice-final/`)
  - API keys (use environment variables)
  
- **Before publishing**:

```bash
bash scripts/privacy-check.sh
```

- **Voice cloning ethics**:
  - Only clone your own voice or with explicit written permission
  - Disclose AI-generated narration in deliverables
  - Respect voice actor rights and local regulations

## License

MIT License. Third-party models (IndexTTS-2), APIs, fonts, music, and assets follow their own licenses. No model weights or voice samples included in this repository.
