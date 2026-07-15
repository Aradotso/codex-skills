---
name: paper-collage-ad-production
description: Complete paper-cut collage ad production workflow with local IndexTTS-2 voice cloning, animation, audio mixing and MP4 QC
triggers:
  - create a paper collage ad for this product
  - generate a cutout style animated advertisement
  - make a 45 second paper-cut ad with voice cloning
  - produce a collage animation ad with narration
  - build a paper craft style video ad
  - animate a paper cutout commercial with audio
  - create a stop-motion style collage ad
  - generate a textured paper ad video
---

# Paper Collage Ad Production Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

A complete production pipeline for paper-cut / collage style animated advertisements. Handles creative development, scripting, storyboarding, keyframe generation, animation, voice-over (including local IndexTTS-2 voice cloning on Apple Silicon), music, sound effects, composition and MP4 quality control.

## Installation

**Global installation** (available to all Codex projects):

```bash
git clone https://github.com/Jane-xiaoer/paper-collage-ad-codex.git \
  ~/.codex/skills/paper-collage-ad
```

**Project-local installation**:

```bash
mkdir -p .codex/skills
git clone https://github.com/Jane-xiaoer/paper-collage-ad-codex.git \
  .codex/skills/paper-collage-ad
```

After restart or in a new Codex session, you can say:

```text
Use paper-collage-ad to create a fun 45-second cutout ad for this product.
```

## Core Capabilities

- Extract a visual metaphor from product materials
- Generate scripts with dialogue and timestamped storyboards
- Produce style-locked paper-cut keyframes using brand assets
- Animate via Seedance, HyperFrames, layered PNG or FFmpeg
- Synthesize voice-over with standard TTS or local IndexTTS-2 MLX voice cloning
- Add music, paper foley and motion SFX
- Export H.264/AAC MP4 with stream-level validation

## System Dependencies

**macOS**:

```bash
brew install ffmpeg node
bash scripts/check-deps.sh
```

For static keyframes, layered animation and final composition, no API keys are required. Seedance, 即梦, MiniMax and ElevenLabs are optional and require user credentials.

## Project Structure

A typical ad project follows this layout:

```text
my-product-ad/
  assets/
    brand/                # Product images, logos, colors
    voice-reference/      # reference.wav (6-12s clean single speaker)
    voice-model/          # speaker-v2.npz (local generated, not committed)
    voice-final/          # 01.wav, 02.wav... (generated narration)
    music/                # background tracks
    sfx/                  # sound effects
    frames/               # keyframe PNGs
    layers/               # layered PNG scenes for animation
  manifests/
    script.json           # storyboard with timecode
    voice.indextts2.json  # narration manifest
    animation.json        # scene animation config
    audio.json            # music and SFX timeline
  output/
    scenes/               # rendered scene videos
    final.mp4             # final composition
```

## Workflow Steps

### 1. Generate Script and Storyboard

Start with a product brief or description. The skill will:

- Identify a visual metaphor
- Write a 45-second script with dialogue
- Create timestamped storyboard entries

Example assistant interaction:

```text
User: Create a paper collage ad for our organic coffee brand. 
      Emphasize the journey from bean to cup.
