---
name: paper-collage-ad-production
description: Complete paper-cut collage ad production workflow with local IndexTTS-2 voice cloning, animation pipeline, audio mixing and MP4 quality control
triggers:
  - "create a paper collage ad with voice cloning"
  - "make a paper-cut style advertisement with IndexTTS-2"
  - "generate an animated collage ad with custom voice narration"
  - "produce a stop-motion paper ad with local TTS"
  - "build a collage-style video ad with voice cloning and music"
  - "create animated paper-cut advertisement with narration"
  - "make a 45-second paper collage ad with custom voice"
  - "produce collage ad with IndexTTS-2 voice and animation"
---

# Paper Collage Ad Production Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Production workflow for creating paper-cut collage style advertisements with local voice cloning (IndexTTS-2 MLX), animation pipelines (Seedance, HyperFrames, FFmpeg), audio mixing, and MP4 output with quality validation.

## What This Skill Does

- Extract visual metaphors from product materials for cohesive storytelling
- Generate storyboards with script, dialogue and timecode breakdowns
- Create style-locked paper-cut keyframes using brand assets
- Animate using Seedance, HyperFrames, layered PNGs, or FFmpeg
- Clone voices locally using IndexTTS-2 MLX (Apple Silicon) or use standard TTS
- Add music, paper foley sounds, and action sound effects
- Output H.264/AAC MP4 with stream-level validation

## Installation

### Install the Skill

Global installation (available to all Codex projects):

```bash
git clone https://github.com/Jane-xiaoer/paper-collage-ad-codex.git \
  ~/.codex/skills/paper-collage-ad
```

Project-local installation:

```bash
mkdir -p .codex/skills
git clone https://github.com/Jane-xiaoer/paper-collage-ad-codex.git \
  .codex/skills/paper-collage-ad
```

After restart, invoke with:
```
Use paper-collage-ad to create a fun 45-second paper-cut ad for this product.
```

### System Dependencies

macOS:

```bash
brew install ffmpeg node
bash scripts/check-deps.sh
```

For static keyframes and layered animation only, no API keys required. Optional services (Seedance, 即梦, MiniMax, ElevenLabs) need user-supplied credentials via environment variables.

### IndexTTS-2 MLX Voice Cloning Setup

Install runtime and models (Apple Silicon Mac):

```bash
bash scripts/setup-indextts2-mlx.sh
```

This downloads models to:
```
~/.local/share/paper-collage-ad/mlx-indextts/
  models/mlx-indextts2-standard-fp16/
```

## Project Structure

```
<project>/
  assets/
    brand/              # Product images, logos
    voice-reference/    # reference.wav (6-12s clean single speaker)
    voice-model/        # speaker-v2.npz (generated, never commit)
    voice-final/        # 01.wav, 02.wav... (generated narration)
    keyframes/          # scene_01.png, scene_02.png...
    animated/           # scene_01.mp4, scene_02.mp4...
    music/              # background.mp3
    sfx/                # paper_rustle.wav, swoosh.wav...
  manifests/
    storyboard.json
    voice.indextts2.json
    animation.json
    audio-mix.json
  output/
    final.mp4
```

Privacy template:

```bash
cp examples/project.gitignore "<project>/.gitignore"
```

## Voice Cloning Workflow

### 1. Prepare Voice Reference

Only clone your own voice or voices you have explicit written permission to use.

Place authorized reference audio:
```
<project>/assets/voice-reference/reference.wav
```

Requirements:
- 6-12 seconds
- 48 kHz recommended
- Clean, single speaker
- Clear speech, no background noise

### 2. Generate Speaker Embedding

```bash
bash scripts/prepare-indextts2-voice.sh \
  "<project>/assets/voice-reference/reference.wav" \
  "<project>/assets/voice-model/speaker-v2.npz" \
  --i-have-permission
```

The `--i-have-permission` flag is mandatory and confirms authorization.

### 3. Create Voice Manifest

```bash
cp examples/voice-manifest.indextts2.json \
  "<project>/manifests/voice.indextts2.json"
```

Edit `voice.indextts2.json`:

```json
{
  "speakerPath": "assets/voice-model/speaker-v2.npz",
  "outputDir": "assets/voice-final",
  "sampleRate": 48000,
  "segments": [
    {
      "id": "01",
      "text": "Imagine a world where every cup of coffee tells a story.",
      "emotion": "calm",
      "speed": 1.0
    },
    {
      "id": "02",
      "text": "Our beans travel from mountain to cup in just 72 hours.",
      "emotion": "excited",
      "speed": 1.05
    }
  ]
}
```

Supported emotions: `neutral`, `happy`, `sad`, `angry`, `surprised`, `fearful`, `calm`, `excited`

### 4. Generate Narration

```bash
node scripts/narrate-indextts2.mjs \
  --manifest "<project>/manifests/voice.indextts2.json"
```

Output: `assets/voice-final/01.wav`, `02.wav`, etc.

## Storyboard & Keyframe Generation

### Storyboard Structure

Create `manifests/storyboard.json`:

```json
{
  "title": "Mountain Coffee - Origin Story",
  "duration": 45,
  "visualMetaphor": "Coffee cherries transform into paper birds flying to customers",
  "scenes": [
    {
      "id": "scene_01",
      "timecode": "00:00-00:05",
      "narration": "Imagine a world where every cup tells a story.",
      "visual": "Paper-cut mountains with coffee plants, sunrise gradient background",
      "motion": "Camera slow push into mountain range",
      "sfx": ["birds_chirping", "wind_light"]
    },
    {
      "id": "scene_02",
      "timecode": "00:05-00:12",
      "narration": "Our beans travel from mountain to cup in 72 hours.",
      "visual": "Coffee cherries peel away to reveal origami birds",
      "motion": "Birds unfold and take flight, trailing coffee bean textures",
      "sfx": ["paper_rustle", "whoosh"]
    }
  ]
}
```

### Generate Keyframes

With image generation API (Seedance, 即梦, MiniMax):

```javascript
// scripts/generate-keyframes.mjs
import fs from 'fs';
import { seedanceGenerate } from './lib/seedance.mjs';

const storyboard = JSON.parse(fs.readFileSync('manifests/storyboard.json', 'utf-8'));
const apiKey = process.env.SEEDANCE_API_KEY;

for (const scene of storyboard.scenes) {
  const prompt = `paper-cut collage art style: ${scene.visual}. Layered textured paper, cast shadows, craft aesthetic, ${storyboard.visualMetaphor} theme`;
  
  const imageUrl = await seedanceGenerate(prompt, {
    apiKey,
    width: 1920,
    height: 1080,
    style: 'paper-collage'
  });
  
  // Download to assets/keyframes/
  await downloadImage(imageUrl, `assets/keyframes/${scene.id}.png`);
}
```

Or manually place/create keyframes in `assets/keyframes/`.

## Animation Pipeline

### Option 1: Video Generation API (Seedance, HyperFrames)

Create `manifests/animation.json`:

```json
{
  "scenes": [
    {
      "id": "scene_01",
      "keyframe": "assets/keyframes/scene_01.png",
      "motion": "Camera slow push into mountain range",
      "duration": 5,
      "output": "assets/animated/scene_01.mp4",
      "provider": "seedance"
    }
  ]
}
```

Generate:

```bash
node scripts/animate-scenes.mjs \
  --manifest manifests/animation.json \
  --api-key $SEEDANCE_API_KEY
```

### Option 2: Layered PNG Animation (FFmpeg)

For parallax or simple motion:

```javascript
// scripts/animate-layers.mjs
import { execSync } from 'child_process';

// Separate keyframe into layers: background, midground, foreground
// Use FFmpeg zoompan or overlay filters

const duration = 5;
const fps = 24;

execSync(`ffmpeg -loop 1 -i assets/keyframes/scene_01_bg.png \
  -vf "zoompan=z='min(zoom+0.0015,1.05)':d=${duration * fps}:s=1920x1080:fps=${fps}" \
  -t ${duration} -pix_fmt yuv420p assets/animated/scene_01.mp4`);
```

### Option 3: Frame-by-Frame Stop-Motion

Generate intermediate frames using image APIs with iterative prompts, then stitch:

```bash
ffmpeg -framerate 24 -pattern_type glob -i 'assets/frames/scene_01_*.png' \
  -c:v libx264 -pix_fmt yuv420p assets/animated/scene_01.mp4
```

## Audio Mixing

Create `manifests/audio-mix.json`:

```json
{
  "timeline": [
    {
      "type": "music",
      "file": "assets/music/background.mp3",
      "volume": 0.3,
      "fadeIn": 1.0,
      "fadeOut": 2.0
    },
    {
      "type": "narration",
      "file": "assets/voice-final/01.wav",
      "start": 0.5,
      "volume": 1.0
    },
    {
      "type": "sfx",
      "file": "assets/sfx/paper_rustle.wav",
      "start": 5.2,
      "volume": 0.6
    },
    {
      "type": "narration",
      "file": "assets/voice-final/02.wav",
      "start": 5.8,
      "volume": 1.0
    }
  ],
  "output": "output/audio-mix.wav",
  "sampleRate": 48000
}
```

Mix:

```bash
node scripts/mix-audio.mjs \
  --manifest manifests/audio-mix.json
```

Internal implementation uses FFmpeg `-filter_complex`:

```javascript
// Simplified example
const filters = [];
filters.push(`[0:a]volume=${musicVolume},afade=t=in:st=0:d=${fadeIn},afade=t=out:st=${duration - fadeOut}:d=${fadeOut}[music]`);
filters.push(`[1:a]volume=${narrationVolume},adelay=${narrationStart * 1000}|${narrationStart * 1000}[narration]`);
filters.push(`[music][narration]amix=inputs=2:duration=longest[out]`);

execSync(`ffmpeg -i music.mp3 -i narration.wav \
  -filter_complex "${filters.join(';')}" \
  -map "[out]" output.wav`);
```

## Final Composition

Concatenate video scenes and add audio:

```bash
node scripts/compose-final.mjs \
  --video-list manifests/video-order.txt \
  --audio output/audio-mix.wav \
  --output output/final.mp4
```

`manifests/video-order.txt`:

```
file 'assets/animated/scene_01.mp4'
file 'assets/animated/scene_02.mp4'
file 'assets/animated/scene_03.mp4'
```

Compose script:

```javascript
// scripts/compose-final.mjs
import { execSync } from 'child_process';

// Concatenate video
execSync(`ffmpeg -f concat -safe 0 -i manifests/video-order.txt \
  -c copy output/video-concat.mp4`);

// Add audio
execSync(`ffmpeg -i output/video-concat.mp4 -i output/audio-mix.wav \
  -c:v copy -c:a aac -b:a 192k -shortest output/final.mp4`);
```

## Quality Control

Validate output:

```bash
bash scripts/qc-video.sh output/final.mp4
```

Checks:
- Video codec: H.264
- Audio codec: AAC
- Resolution: 1920×1080 (or project target)
- Frame rate consistency
- No silent segments
- Audio levels within broadcast safe range (-23 LUFS target)

Example QC script:

```bash
#!/bin/bash
VIDEO=$1

# Check codecs
ffprobe -v error -select_streams v:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$VIDEO"
# Expected: h264

ffprobe -v error -select_streams a:0 -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "$VIDEO"
# Expected: aac

# Check resolution
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of csv=s=x:p=0 "$VIDEO"
# Expected: 1920x1080

# Check LUFS
ffmpeg -i "$VIDEO" -af loudnorm=print_format=json -f null - 2>&1 | grep input_i
# Target: -23.0 LUFS ±2
```

## Environment Variables

Optional service integrations read from environment:

```bash
# .env (never commit)
SEEDANCE_API_KEY=sk-...
MINIMAX_API_KEY=...
ELEVENLABS_API_KEY=...
JIMENG_API_KEY=...
```

Load in scripts:

```javascript
import 'dotenv/config';

const apiKey = process.env.SEEDANCE_API_KEY;
if (!apiKey) {
  console.error('SEEDANCE_API_KEY not set');
  process.exit(1);
}
```

## Common Patterns

### Full Production Pipeline

```bash
# 1. Setup voice
bash scripts/prepare-indextts2-voice.sh \
  assets/voice-reference/reference.wav \
  assets/voice-model/speaker-v2.npz \
  --i-have-permission

# 2. Generate narration
node scripts/narrate-indextts2.mjs \
  --manifest manifests/voice.indextts2.json

# 3. Generate keyframes (manual or API)
node scripts/generate-keyframes.mjs

# 4. Animate scenes
node scripts/animate-scenes.mjs \
  --manifest manifests/animation.json

# 5. Mix audio
node scripts/mix-audio.mjs \
  --manifest manifests/audio-mix.json

# 6. Compose final video
node scripts/compose-final.mjs \
  --video-list manifests/video-order.txt \
  --audio output/audio-mix.wav \
  --output output/final.mp4

# 7. QC
bash scripts/qc-video.sh output/final.mp4
```

### Voice-Only Update

Already have video, just update narration:

```bash
# Edit voice manifest
vim manifests/voice.indextts2.json

# Regenerate voice
node scripts/narrate-indextts2.mjs \
  --manifest manifests/voice.indextts2.json

# Re-mix audio
node scripts/mix-audio.mjs \
  --manifest manifests/audio-mix.json

# Re-compose
node scripts/compose-final.mjs \
  --video-list manifests/video-order.txt \
  --audio output/audio-mix.wav \
  --output output/final.mp4
```

### Quick Storyboard Iteration

```javascript
// scripts/quick-iterate.mjs
// Re-generate keyframes and preview without full animation

import { generateKeyframe } from './lib/image-gen.mjs';
import { createPreviewGrid } from './lib/preview.mjs';

const storyboard = JSON.parse(fs.readFileSync('manifests/storyboard.json', 'utf-8'));

for (const scene of storyboard.scenes) {
  await generateKeyframe(scene, `assets/keyframes/${scene.id}.png`);
}

// Create HTML preview grid
await createPreviewGrid('assets/keyframes', 'output/preview.html');
```

## Troubleshooting

### IndexTTS-2 MLX Issues

**Error: Model not found**

```bash
# Re-run setup
bash scripts/setup-indextts2-mlx.sh

# Verify installation
ls -la ~/.local/share/paper-collage-ad/mlx-indextts/models/
```

**Poor voice quality**

- Use cleaner reference audio (6-12s, no background noise)
- Ensure 48 kHz sample rate
- Try `emotion: "neutral"` first, then adjust
- Keep `speed` between 0.9-1.1

**Out of memory on Apple Silicon**

- Close other apps
- Reduce concurrent segment generation
- Use standard TTS fallback for longer scripts

### FFmpeg Encoding Issues

**Audio out of sync**

```bash
# Force constant frame rate
ffmpeg -i input.mp4 -vsync cfr -r 24 -c:v libx264 -crf 18 output.mp4
```

**File too large**

```bash
# Adjust CRF (18=high quality, 23=default, 28=smaller)
ffmpeg -i input.mp4 -c:v libx264 -crf 23 -c:a aac -b:a 128k output.mp4
```

**Pixelation in gradients**

```bash
# Use higher bitrate or lower CRF
ffmpeg -i input.mp4 -c:v libx264 -crf 18 -preset slow output.mp4
```

### API Rate Limits

```javascript
// Add delay between requests
async function generateWithRetry(prompt, options) {
  for (let i = 0; i < 3; i++) {
    try {
      return await seedanceGenerate(prompt, options);
    } catch (err) {
      if (err.status === 429) {
        await new Promise(resolve => setTimeout(resolve, 5000 * (i + 1)));
        continue;
      }
      throw err;
    }
  }
}
```

## Privacy & Security

- **Never commit** `voice-reference/`, `voice-model/`, or personal narration
- **Never commit** API keys or `.env` files
- Use project `.gitignore` template: `cp examples/project.gitignore .gitignore`
- Run privacy check before publishing: `bash scripts/privacy-check.sh`
- Always disclose AI-generated voice in deliverables
- Only clone voices with explicit written authorization

## References

See `references/` directory for detailed specs:

- `storyboard.md` - Scene structure and timing
- `visual-style.md` - Paper-cut collage aesthetics
- `animation.md` - Motion techniques and providers
- `voice.md` - IndexTTS-2 emotion control and fallback options
- `audio-mix.md` - Music, SFX and normalization
- `qc.md` - Final validation checklist

## License

MIT License. Third-party models, runtimes, fonts, music, assets and APIs are subject to their own licenses. IndexTTS-2 model weights are not included in this repository.
