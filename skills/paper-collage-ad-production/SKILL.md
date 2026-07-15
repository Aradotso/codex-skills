---
name: paper-collage-ad-production
description: Complete paper-cut collage ad workflow with local IndexTTS-2 voice cloning, animation, audio mixing, and MP4 quality control for Codex
triggers:
  - "create a paper collage ad"
  - "generate a paper-cut style advertisement"
  - "make an animated collage video with voiceover"
  - "produce a 45 second paper collage ad"
  - "set up voice cloning for ad narration"
  - "render and validate MP4 ad output"
  - "build a stop-motion paper ad with TTS"
  - "create layered paper animation with music"
---

# Paper Collage Ad Production

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

A complete skill for producing paper-cut/collage-style advertisements from concept to final MP4. Handles scriptwriting, storyboarding, keyframe generation, animation (Seedance/HyperFrames/layered PNG), local voice cloning with IndexTTS-2 MLX, music, sound effects, composition, and H.264/AAC validation.

## What This Does

- Extract visual metaphors from product materials
- Output script, dialogue, and timecoded storyboards for approval
- Generate brand-locked paper-cut keyframes
- Animate via Seedance, HyperFrames, layered PNG, or FFmpeg
- Clone authorized voices locally with IndexTTS-2 MLX (Apple Silicon)
- Add music, paper foley, and action SFX
- Export stream-validated H.264/AAC MP4

## Installation

**System dependencies (macOS):**

```bash
brew install ffmpeg node
```

**Verify setup:**

```bash
bash scripts/check-deps.sh
```

**Install IndexTTS-2 MLX for local voice cloning:**

```bash
bash scripts/setup-indextts2-mlx.sh
```

Models download to: `~/.local/share/paper-collage-ad/mlx-indextts/models/mlx-indextts2-standard-fp16/`

## Project Structure

```
<project>/
  assets/
    brand/              # Logos, colors, fonts
    keyframes/          # Generated paper-cut frames
    animation/          # Video segments
    voice-reference/    # Authorized reference audio (NOT committed)
    voice-model/        # Local speaker embeddings (NOT committed)
    voice-final/        # Generated narration (NOT committed)
    music/              # Background music
    sfx/                # Sound effects
  manifests/
    storyboard.json     # Scene timing and descriptions
    voice.indextts2.json # Narration script with emotion tags
    animation.json      # Animation segment definitions
    final.json          # Composition timeline
  output/
    final.mp4
```

**Privacy template:**

```bash
cp examples/project.gitignore <project>/.gitignore
```

This excludes `voice-reference/`, `voice-model/`, and generated narration from version control.

## Voice Cloning Workflow

### 1. Prepare Reference Audio

Place a 6–12 second clean mono/stereo WAV of **authorized** voice:

```
<project>/assets/voice-reference/reference.wav
```

### 2. Generate Speaker Embedding

```bash
bash scripts/prepare-indextts2-voice.sh \
  "<project>/assets/voice-reference/reference.wav" \
  "<project>/assets/voice-model/speaker-v2.npz" \
  --i-have-permission
```

### 3. Create Narration Manifest

```bash
cp examples/voice-manifest.indextts2.json \
  "<project>/manifests/voice.indextts2.json"
```

**Example manifest (`voice.indextts2.json`):**

```json
{
  "speaker_path": "assets/voice-model/speaker-v2.npz",
  "output_dir": "assets/voice-final",
  "sample_rate": 48000,
  "segments": [
    {
      "id": "01",
      "text": "Imagine a world where coffee fuels creativity.",
      "emotion": "cheerful",
      "speed": 1.0
    },
    {
      "id": "02",
      "text": "Every cup is a new beginning.",
      "emotion": "calm",
      "speed": 0.95
    }
  ]
}
```

**Supported emotions:** `neutral`, `cheerful`, `sad`, `angry`, `calm`, `excited`

### 4. Generate Narration

```bash
node scripts/narrate-indextts2.mjs \
  --manifest "<project>/manifests/voice.indextts2.json"
```

Outputs: `assets/voice-final/01.wav`, `02.wav`, etc. (48 kHz WAV)

## Animation Workflow

### Static Keyframes

Generate paper-cut frames from brand assets:

```bash
node scripts/generate-keyframes.mjs \
  --storyboard "<project>/manifests/storyboard.json" \
  --brand "<project>/assets/brand" \
  --output "<project>/assets/keyframes"
```

### Layered PNG Animation

For simple parallax/zoom effects:

```bash
node scripts/animate-layers.mjs \
  --manifest "<project>/manifests/animation.json" \
  --output "<project>/assets/animation"
```

**Example `animation.json`:**

```json
{
  "segments": [
    {
      "id": "seg01",
      "duration": 3.0,
      "layers": [
        {
          "image": "assets/keyframes/01_bg.png",
          "motion": {"type": "zoom", "scale_start": 1.0, "scale_end": 1.1}
        },
        {
          "image": "assets/keyframes/01_fg.png",
          "motion": {"type": "pan", "x_start": 0, "x_end": -50}
        }
      ]
    }
  ]
}
```

### FFmpeg Crossfade

```bash
ffmpeg -loop 1 -t 2 -i assets/keyframes/01.png \
       -loop 1 -t 2 -i assets/keyframes/02.png \
       -filter_complex "[0][1]xfade=transition=fade:duration=0.5:offset=1.5" \
       -pix_fmt yuv420p assets/animation/seg01.mp4
```

## Audio Mixing

Combine narration, music, and SFX:

```bash
node scripts/mix-audio.mjs \
  --manifest "<project>/manifests/final.json" \
  --output "<project>/output/audio.wav"
```

**Example `final.json`:**

```json
{
  "audio_tracks": [
    {
      "type": "narration",
      "files": [
        {"path": "assets/voice-final/01.wav", "start": 0.0},
        {"path": "assets/voice-final/02.wav", "start": 3.5}
      ]
    },
    {
      "type": "music",
      "path": "assets/music/background.mp3",
      "volume": 0.3,
      "loop": true
    },
    {
      "type": "sfx",
      "files": [
        {"path": "assets/sfx/paper_rustle.wav", "start": 1.2},
        {"path": "assets/sfx/whoosh.wav", "start": 4.8}
      ]
    }
  ]
}
```

## Final Composition

Render video + audio to MP4:

```bash
node scripts/render-final.mjs \
  --manifest "<project>/manifests/final.json" \
  --output "<project>/output/final.mp4"
```

Internally calls:

```bash
ffmpeg -i video_concat.mp4 -i audio.wav \
  -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -ar 48000 \
  -movflags +faststart \
  output/final.mp4
```

## Quality Control

Validate codec, resolution, duration, audio sync:

```bash
bash scripts/qc-mp4.sh "<project>/output/final.mp4"
```

Checks:
- Video codec: H.264
- Audio codec: AAC
- Sample rate: 48 kHz
- Moov atom position (fast start)
- A/V sync drift < 100ms

## Optional API Services

All require user-provided credentials via environment variables:

**Seedance (video generation):**

```bash
export SEEDANCE_API_KEY="your_key"
node scripts/animate-seedance.mjs --input assets/keyframes/01.png
```

**MiniMax (alternative TTS):**

```bash
export MINIMAX_API_KEY="your_key"
node scripts/narrate-minimax.mjs --manifest manifests/voice.json
```

**ElevenLabs (cloud TTS):**

```bash
export ELEVENLABS_API_KEY="your_key"
node scripts/narrate-elevenlabs.mjs --manifest manifests/voice.json
```

## Common Patterns

### Full Production Pipeline

```javascript
// scripts/full-pipeline.mjs
import { execSync } from 'child_process';

const PROJECT = process.argv[2];

// 1. Generate storyboard (manual or LLM-assisted)
// 2. Create keyframes
execSync(`node scripts/generate-keyframes.mjs --storyboard ${PROJECT}/manifests/storyboard.json --output ${PROJECT}/assets/keyframes`);

// 3. Animate segments
execSync(`node scripts/animate-layers.mjs --manifest ${PROJECT}/manifests/animation.json --output ${PROJECT}/assets/animation`);

// 4. Generate narration
execSync(`node scripts/narrate-indextts2.mjs --manifest ${PROJECT}/manifests/voice.indextts2.json`);

// 5. Mix audio
execSync(`node scripts/mix-audio.mjs --manifest ${PROJECT}/manifests/final.json --output ${PROJECT}/output/audio.wav`);

// 6. Render final MP4
execSync(`node scripts/render-final.mjs --manifest ${PROJECT}/manifests/final.json --output ${PROJECT}/output/final.mp4`);

// 7. QC
execSync(`bash scripts/qc-mp4.sh ${PROJECT}/output/final.mp4`);
```

### Custom Emotion Interpolation

```javascript
// In narrate-indextts2.mjs
const emotions = {
  'cheerful': { pitch: 1.1, energy: 1.2 },
  'calm': { pitch: 0.95, energy: 0.8 }
};

for (const seg of manifest.segments) {
  const params = emotions[seg.emotion] || emotions.neutral;
  // Pass params to IndexTTS-2 inference
}
```

### Brand Color Extraction

```javascript
import Vibrant from 'node-vibrant';

const palette = await Vibrant.from('assets/brand/logo.png').getPalette();
const primary = palette.Vibrant.hex;
const secondary = palette.LightVibrant.hex;

// Use in keyframe generation prompts
const prompt = `paper collage, ${productName}, dominant color ${primary}, accent ${secondary}, flat cutout style`;
```

## Troubleshooting

**IndexTTS-2 model not found:**

```bash
ls ~/.local/share/paper-collage-ad/mlx-indextts/models/
# If empty, re-run setup:
bash scripts/setup-indextts2-mlx.sh
```

**Voice cloning sounds robotic:**

- Use longer reference audio (10–12s)
- Ensure reference is clean mono/stereo, 16–48 kHz
- Try `speed: 0.95` to reduce artifacts

**Animation segments out of sync:**

```bash
# Check segment durations
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 assets/animation/seg01.mp4

# Adjust in animation.json, then re-render
node scripts/render-final.mjs --manifest manifests/final.json --output output/final.mp4
```

**MP4 fails QC:**

```bash
# Check codec details
ffprobe -v error -show_streams output/final.mp4

# Re-encode with correct settings
ffmpeg -i output/final.mp4 -c:v libx264 -crf 23 -pix_fmt yuv420p -c:a aac -b:a 192k -ar 48000 -movflags +faststart output/final_fixed.mp4
```

**Permission errors on voice cloning:**

Always verify you have explicit authorization to clone a voice. The `--i-have-permission` flag is a manual safeguard — do not bypass this for public or commercial projects.

## Key Scripts Reference

| Script | Purpose |
|--------|---------|
| `check-deps.sh` | Verify ffmpeg, node, python |
| `setup-indextts2-mlx.sh` | Install IndexTTS-2 runtime + models |
| `prepare-indextts2-voice.sh` | Generate speaker embedding from reference |
| `narrate-indextts2.mjs` | Synthesize narration with local voice |
| `generate-keyframes.mjs` | Create paper-cut frames |
| `animate-layers.mjs` | Parallax/zoom animation from layers |
| `animate-seedance.mjs` | Optional: video gen via Seedance API |
| `mix-audio.mjs` | Combine narration, music, SFX |
| `render-final.mjs` | Compose video + audio to MP4 |
| `qc-mp4.sh` | Validate codec, sync, faststart |
| `privacy-check.sh` | Scan for leaked keys/voices |

## Environment Variables

```bash
# Optional cloud services
SEEDANCE_API_KEY=
MINIMAX_API_KEY=
ELEVENLABS_API_KEY=

# Local paths (auto-detected)
INDEXTTS2_MODEL_PATH=~/.local/share/paper-collage-ad/mlx-indextts/models/mlx-indextts2-standard-fp16
```

## License & Attribution

- Skill code: MIT
- IndexTTS-2 models: Separate license (downloaded via setup script)
- Always disclose AI-generated narration in final deliverables
- Only clone voices you own or have explicit written authorization for
