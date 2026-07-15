---
name: paper-collage-ad-codex
description: Complete paper-cut collage advertisement production workflow with local IndexTTS-2 voice cloning, animation, audio mixing, and MP4 quality control
triggers:
  - create a paper collage advertisement
  - make a paper-cut style video ad
  - generate animated collage commercial
  - produce stop-motion paper ad with voice cloning
  - build paper collage ad with local TTS
  - create cutout animation advertisement
  - make paper craft style video commercial
  - generate collage ad with IndexTTS voice
---

# Paper Collage Ad for Codex

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

A complete paper-cut/collage advertisement production skill for OpenAI Codex. Handles creative concept, script, storyboard, keyframes, animation, voiceover (including local IndexTTS-2 voice cloning), music, sound effects, compositing, and MP4 quality checking.

## What This Does

This skill guides you through producing 30–60 second paper collage advertisements:

- Extract a visual metaphor from product materials
- Generate script, dialogue, and timecoded storyboard
- Create style-locked paper-cut keyframes using brand assets
- Animate via Seedance, HyperFrames, layered PNG, or FFmpeg
- Generate voiceover using standard TTS or **local IndexTTS-2 MLX** for zero-shot voice cloning (Apple Silicon)
- Add music, paper foley, and action sound effects
- Output H.264/AAC MP4 with stream-level validation

## Installation

### Install the Skill

**Global** (all Codex projects):

```bash
git clone https://github.com/Jane-xiaoer/paper-collage-ad-codex.git \
  ~/.codex/skills/paper-collage-ad
```

**Project-local**:

```bash
mkdir -p .codex/skills
git clone https://github.com/Jane-xiaoer/paper-collage-ad-codex.git \
  .codex/skills/paper-collage-ad
```

Restart Codex or start a new task, then say:

```text
Use paper-collage-ad to create a fun 45-second paper collage ad for this product.
```

### System Dependencies

macOS:

```bash
brew install ffmpeg node
bash ~/.codex/skills/paper-collage-ad/scripts/check-deps.sh
```

FFmpeg and Node.js are required. No API keys needed for static keyframes, layered animation, and final compositing.

## Project Structure

When you start a new ad project, create:

```
<project>/
  assets/
    brand/              # Logo, product images, color palette
    keyframes/          # Generated paper-cut PNG frames
    voice-reference/    # reference.wav (6–12s clean single-speaker audio)
    voice-model/        # speaker-v2.npz (local voice embedding)
    voice-final/        # 01.wav, 02.wav... (scene voiceovers)
    music/              # Background music loops
    sfx/                # Paper rustle, pop, swish sounds
  manifests/
    storyboard.json     # Timecoded scene descriptions
    voice.indextts2.json # Voiceover text + emotion per scene
    audio-mix.json      # Track volumes, fade, timing
  output/
    final.mp4           # Deliverable
```

Copy the privacy-safe `.gitignore`:

```bash
cp ~/.codex/skills/paper-collage-ad/examples/project.gitignore <project>/.gitignore
```

This excludes `voice-reference/`, `voice-model/`, `voice-final/`, and `.env`.

## Workflow

### 1. Script & Storyboard

Provide product info and target audience. The skill will generate:

- **Storyboard JSON** with scene descriptions, visual metaphor, timing
- **Dialogue script** with emotion tags

Example `manifests/storyboard.json`:

```json
{
  "title": "Morning Rush Coffee Ad",
  "duration": 45,
  "scenes": [
    {
      "id": "01",
      "start": 0.0,
      "end": 8.0,
      "visual": "Paper-cut alarm clock explodes into coffee beans",
      "voiceover": "Every morning is a battle.",
      "emotion": "tense"
    },
    {
      "id": "02",
      "start": 8.0,
      "end": 18.0,
      "visual": "Coffee cup rises like a superhero cape",
      "voiceover": "Until Morning Rush Coffee arrives.",
      "emotion": "heroic"
    }
  ]
}
```

### 2. Generate Keyframes

Use brand assets and the storyboard to create paper-cut style PNG keyframes.

**Manual** (recommended for brand control):

- Design in Photoshop/Figma, export to `assets/keyframes/01.png`, `02.png`...

**AI-assisted**:

```bash
# Example: use DALL-E or Midjourney to generate, then refine
# Store results in assets/keyframes/
```

Each keyframe should match the scene's visual description.

### 3. Animation

#### Option A: Static Keyframes with Transitions

Simple crossfades via FFmpeg:

```bash
node ~/.codex/skills/paper-collage-ad/scripts/render-keyframe-video.mjs \
  --manifest manifests/storyboard.json \
  --keyframes assets/keyframes \
  --output output/video-base.mp4 \
  --fps 30 \
  --transition crossfade
```

#### Option B: Layered PNG Animation

For parallax or multi-layer movement:

```bash
# Place layered PNGs in assets/keyframes/01/bg.png, 01/mid.png, 01/fg.png
node ~/.codex/skills/paper-collage-ad/scripts/animate-layers.mjs \
  --scene 01 \
  --duration 8.0 \
  --output output/scene-01.mp4
```

#### Option C: Seedance / HyperFrames (API)

If you have API access:

```bash
export SEEDANCE_API_KEY=your_key_here
node ~/.codex/skills/paper-collage-ad/scripts/animate-seedance.mjs \
  --keyframe assets/keyframes/01.png \
  --prompt "paper coffee cup rises and rotates" \
  --duration 8.0 \
  --output output/scene-01.mp4
```

### 4. Voice Clone with IndexTTS-2 MLX (Local)

**Setup** (one-time):

```bash
bash ~/.codex/skills/paper-collage-ad/scripts/setup-indextts2-mlx.sh
```

This downloads models to `~/.local/share/paper-collage-ad/mlx-indextts/models/`.

**Prepare Voice Model** (per speaker):

Place authorized reference audio in `assets/voice-reference/reference.wav` (6–12s, 48kHz mono recommended).

```bash
bash ~/.codex/skills/paper-collage-ad/scripts/prepare-indextts2-voice.sh \
  "assets/voice-reference/reference.wav" \
  "assets/voice-model/speaker-v2.npz" \
  --i-have-permission
```

**Generate Voiceovers**:

Copy and edit the manifest:

```bash
cp ~/.codex/skills/paper-collage-ad/examples/voice-manifest.indextts2.json \
  manifests/voice.indextts2.json
```

Example `manifests/voice.indextts2.json`:

```json
{
  "speaker": "assets/voice-model/speaker-v2.npz",
  "output_dir": "assets/voice-final",
  "sample_rate": 48000,
  "lines": [
    {
      "id": "01",
      "text": "Every morning is a battle.",
      "emotion": "tense",
      "speed": 1.0
    },
    {
      "id": "02",
      "text": "Until Morning Rush Coffee arrives.",
      "emotion": "heroic",
      "speed": 1.05
    }
  ]
}
```

Run synthesis:

```bash
node ~/.codex/skills/paper-collage-ad/scripts/narrate-indextts2.mjs \
  --manifest manifests/voice.indextts2.json
```

Outputs: `assets/voice-final/01.wav`, `02.wav`...

**Privacy**: Only clone your own voice or voices with explicit written permission. Mark deliverables as "AI-generated voiceover."

### 5. Audio Mixing

Prepare background music and SFX in `assets/music/` and `assets/sfx/`.

Create `manifests/audio-mix.json`:

```json
{
  "output": "output/audio-mix.wav",
  "sample_rate": 48000,
  "tracks": [
    {
      "type": "music",
      "file": "assets/music/upbeat-loop.wav",
      "volume": 0.3,
      "loop": true
    },
    {
      "type": "voiceover",
      "file": "assets/voice-final/01.wav",
      "start": 0.5,
      "volume": 1.0
    },
    {
      "type": "voiceover",
      "file": "assets/voice-final/02.wav",
      "start": 8.5,
      "volume": 1.0
    },
    {
      "type": "sfx",
      "file": "assets/sfx/paper-rustle.wav",
      "start": 2.0,
      "volume": 0.6
    }
  ]
}
```

Mix:

```bash
node ~/.codex/skills/paper-collage-ad/scripts/mix-audio.mjs \
  --manifest manifests/audio-mix.json
```

### 6. Final Composite & QC

Merge video and audio:

```bash
ffmpeg -i output/video-base.mp4 -i output/audio-mix.wav \
  -c:v libx264 -preset slow -crf 20 -c:a aac -b:a 192k \
  -movflags +faststart output/final.mp4
```

Validate:

```bash
bash ~/.codex/skills/paper-collage-ad/scripts/qc-mp4.sh output/final.mp4
```

Checks:

- H.264 video codec
- AAC audio codec, 48kHz
- Duration matches storyboard
- No stream errors
- Fast-start moov atom for web playback

## Configuration

### Environment Variables

Optional API services (only if you use them):

```bash
# .env (never commit this)
SEEDANCE_API_KEY=sk-...
ELEVENLAB_API_KEY=...
MINIMAX_API_KEY=...
```

Load in Node.js scripts:

```javascript
import dotenv from 'dotenv';
dotenv.config();
const apiKey = process.env.SEEDANCE_API_KEY;
```

### Voice Emotion Tags

IndexTTS-2 supports emotion control. Common tags:

- `neutral`
- `happy`, `excited`
- `sad`, `tense`
- `angry`, `calm`
- `heroic`, `mysterious`

Adjust `emotion` in `voice.indextts2.json` per line.

### Animation Parameters

Layered animation script accepts:

```javascript
// scripts/animate-layers.mjs usage
{
  scene: "01",
  duration: 8.0,
  layers: [
    { file: "bg.png", motion: "static" },
    { file: "mid.png", motion: "pan", speed: 20 },
    { file: "fg.png", motion: "zoom", speed: 1.1 }
  ]
}
```

## Code Examples

### Programmatic Storyboard Generation

```javascript
// generate-storyboard.mjs
import fs from 'fs';

const product = {
  name: "Morning Rush Coffee",
  tagline: "Wake up ready",
  audience: "busy professionals"
};

const storyboard = {
  title: `${product.name} Ad`,
  duration: 45,
  scenes: [
    {
      id: "01",
      start: 0.0,
      end: 8.0,
      visual: "Alarm clock explodes into coffee beans",
      voiceover: "Every morning is a battle.",
      emotion: "tense"
    },
    {
      id: "02",
      start: 8.0,
      end: 18.0,
      visual: "Coffee cup superhero cape",
      voiceover: `Until ${product.name} arrives.`,
      emotion: "heroic"
    },
    {
      id: "03",
      start: 18.0,
      end: 28.0,
      visual: "Paper commuter runs on coffee steam train",
      voiceover: "Now you're unstoppable.",
      emotion: "excited"
    },
    {
      id: "04",
      start: 28.0,
      end: 45.0,
      visual: "Product pack with logo, sunburst",
      voiceover: `${product.name}. ${product.tagline}.`,
      emotion: "confident"
    }
  ]
};

fs.writeFileSync('manifests/storyboard.json', JSON.stringify(storyboard, null, 2));
console.log('✓ Storyboard written');
```

### Custom FFmpeg Transition

```javascript
// scripts/render-keyframe-video.mjs (simplified)
import { execSync } from 'child_process';
import fs from 'fs';

const manifest = JSON.parse(fs.readFileSync('manifests/storyboard.json', 'utf-8'));
const keyframesDir = 'assets/keyframes';
const output = 'output/video-base.mp4';
const fps = 30;

let filterComplex = '';
let inputs = '';

manifest.scenes.forEach((scene, i) => {
  const duration = scene.end - scene.start;
  const kf = `${keyframesDir}/${scene.id}.png`;
  inputs += `-loop 1 -t ${duration} -i ${kf} `;
  
  if (i === 0) {
    filterComplex += `[0:v]fade=t=in:st=0:d=0.5,fade=t=out:st=${duration - 0.5}:d=0.5[v0]; `;
  } else {
    filterComplex += `[${i}:v]fade=t=in:st=0:d=0.5,fade=t=out:st=${duration - 0.5}:d=0.5[v${i}]; `;
  }
});

// Concatenate
const concatInputs = manifest.scenes.map((_, i) => `[v${i}]`).join('');
filterComplex += `${concatInputs}concat=n=${manifest.scenes.length}:v=1:a=0[outv]`;

const cmd = `ffmpeg ${inputs} -filter_complex "${filterComplex}" -map "[outv]" -r ${fps} -c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p ${output}`;

execSync(cmd, { stdio: 'inherit' });
console.log(`✓ Video rendered: ${output}`);
```

### IndexTTS-2 Synthesis Script

```javascript
// scripts/narrate-indextts2.mjs (simplified)
import { execSync } from 'child_process';
import fs from 'fs';
import path from 'path';

const manifestPath = process.argv[2] || 'manifests/voice.indextts2.json';
const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));

const mlxIndexTTSPath = path.join(
  process.env.HOME,
  '.local/share/paper-collage-ad/mlx-indextts'
);

manifest.lines.forEach(line => {
  const outFile = path.join(manifest.output_dir, `${line.id}.wav`);
  const cmd = [
    `cd ${mlxIndexTTSPath}`,
    `source venv/bin/activate`,
    `python -m mlx_indextts.synthesize`,
    `--model models/mlx-indextts2-standard-fp16`,
    `--speaker ${manifest.speaker}`,
    `--text "${line.text}"`,
    `--emotion ${line.emotion}`,
    `--speed ${line.speed || 1.0}`,
    `--output ${outFile}`,
    `--sample-rate ${manifest.sample_rate}`
  ].join(' && ');
  
  console.log(`Synthesizing ${line.id}...`);
  execSync(cmd, { stdio: 'inherit', shell: '/bin/bash' });
});

console.log('✓ All voiceovers generated');
```

### Audio Mixing with FFmpeg

```javascript
// scripts/mix-audio.mjs (simplified)
import { execSync } from 'child_process';
import fs from 'fs';

const manifest = JSON.parse(fs.readFileSync('manifests/audio-mix.json', 'utf-8'));
let filterComplex = '';
let inputs = '';

manifest.tracks.forEach((track, i) => {
  inputs += `-i ${track.file} `;
  const vol = track.volume || 1.0;
  const delay = (track.start || 0) * 1000; // ms
  
  filterComplex += `[${i}:a]volume=${vol},adelay=${delay}|${delay}[a${i}]; `;
});

const mixInputs = manifest.tracks.map((_, i) => `[a${i}]`).join('');
filterComplex += `${mixInputs}amix=inputs=${manifest.tracks.length}:duration=longest[outa]`;

const cmd = `ffmpeg ${inputs} -filter_complex "${filterComplex}" -map "[outa]" -ar ${manifest.sample_rate} ${manifest.output}`;

execSync(cmd, { stdio: 'inherit' });
console.log(`✓ Audio mixed: ${manifest.output}`);
```

## Common Patterns

### Pattern: Multi-Scene Video from Keyframes

```bash
# 1. Generate storyboard
node generate-storyboard.mjs

# 2. Create keyframes (manual or AI)
# Save to assets/keyframes/01.png, 02.png...

# 3. Render video
node ~/.codex/skills/paper-collage-ad/scripts/render-keyframe-video.mjs \
  --manifest manifests/storyboard.json \
  --keyframes assets/keyframes \
  --output output/video-base.mp4

# 4. Generate voiceovers
node ~/.codex/skills/paper-collage-ad/scripts/narrate-indextts2.mjs \
  --manifest manifests/voice.indextts2.json

# 5. Mix audio
node ~/.codex/skills/paper-collage-ad/scripts/mix-audio.mjs \
  --manifest manifests/audio-mix.json

# 6. Composite
ffmpeg -i output/video-base.mp4 -i output/audio-mix.wav \
  -c:v libx264 -crf 20 -c:a aac -b:a 192k \
  -movflags +faststart output/final.mp4

# 7. QC
bash ~/.codex/skills/paper-collage-ad/scripts/qc-mp4.sh output/final.mp4
```

### Pattern: Voice Clone for Multiple Projects

Keep a single authorized voice model in a shared location:

```bash
# One-time voice model prep
bash ~/.codex/skills/paper-collage-ad/scripts/prepare-indextts2-voice.sh \
  ~/my-voice/reference.wav \
  ~/my-voice/speaker-v2.npz \
  --i-have-permission

# In each project manifest, reference:
{
  "speaker": "~/my-voice/speaker-v2.npz",
  ...
}
```

### Pattern: Batch QC Multiple Ads

```bash
for mp4 in output/*.mp4; do
  echo "Checking $mp4..."
  bash ~/.codex/skills/paper-collage-ad/scripts/qc-mp4.sh "$mp4"
done
```

## Troubleshooting

### IndexTTS-2 Voice Sounds Robotic

- **Check reference audio**: Must be clean, 6–12s, single speaker, no background noise
- **Increase sample rate**: Use 48000 Hz in manifest
- **Adjust speed**: Try `"speed": 0.95` for more natural pacing
- **Emotion mismatch**: Ensure emotion tag matches spoken content

### FFmpeg "Invalid duration" Error

- **Check timecodes**: Ensure `end > start` in storyboard
- **Keyframe missing**: Verify `assets/keyframes/XX.png` exists for each scene
- **Use absolute paths**: If relative paths fail, try absolute

### Video/Audio Out of Sync

- **Sample rate mismatch**: Ensure all audio is 48kHz before mixing
- **Incorrect start times**: Verify `start` in `audio-mix.json` matches storyboard
- **Re-encode audio**: `ffmpeg -i in.wav -ar 48000 out.wav`

### QC Script Reports "moov atom not at start"

- **Add faststart flag**:

```bash
ffmpeg -i input.mp4 -c copy -movflags +faststart output.mp4
```

### Voice Clone Fails with "Permission Denied"

- **Activate venv**: Ensure script runs `source venv/bin/activate`
- **Check paths**: Verify `~/.local/share/paper-collage-ad/mlx-indextts/` exists
- **Re-run setup**:

```bash
bash ~/.codex/skills/paper-collage-ad/scripts/setup-indextts2-mlx.sh
```

### Animation Looks Choppy

- **Increase FPS**: Use `--fps 60` in render script
- **Check keyframe resolution**: Ensure all PNGs are same size (e.g., 1920×1080)
- **Use better codec**: Add `-preset slow` for higher quality

## References

- **SKILL.md**: Main workflow orchestration
- **references/**: Detailed guides for storyboard, visuals, animation, voice, music, QC
- **examples/**: Copyable JSON manifests and HTML templates
- **scripts/**: All executable Node.js and Bash utilities

## Privacy & Security

- No API keys, voice samples, or brand assets included
- `.gitignore` excludes `voice-reference/`, `voice-model/`, `voice-final/`, `.env`
- Before public release, run:

```bash
bash ~/.codex/skills/paper-collage-ad/scripts/privacy-check.sh
```

**Voice Cloning Ethics**: Only clone voices you own or have written permission to clone. Disclose AI generation in all deliverables.

## License

MIT License. Third-party models, fonts, music, and APIs are subject to their own licenses. IndexTTS-2 model weights are not bundled.

---

**Quick Start Summary**:

1. Install skill globally or locally
2. Run `bash scripts/check-deps.sh`
3. Create project structure with `assets/`, `manifests/`, `output/`
4. Generate storyboard → keyframes → video → voice → audio → composite → QC
5. Use local IndexTTS-2 for voice cloning (Apple Silicon) or fallback to standard TTS
6. Deliver privacy-compliant, stream-validated MP4

For full Chinese workflow, see [WORKFLOW.zh-CN.md](https://github.com/Jane-xiaoer/paper-collage-ad-codex/blob/main/WORKFLOW.zh-CN.md).
