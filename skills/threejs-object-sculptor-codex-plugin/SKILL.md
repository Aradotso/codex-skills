---
name: threejs-object-sculptor-codex-plugin
description: Convert object images into code-only, animation-ready procedural Three.js models through staged sculpting workflow
triggers:
  - turn this image into a Three.js model
  - create a procedural 3D object from this reference
  - sculpt a Three.js object from this attachment
  - build an animation-ready procedural model
  - convert this object image to Three.js code
  - generate a procedural 3D asset from reference
  - make a code-only Three.js model from this image
  - create an action-ready Three.js prop from this photo
---

# Three.js Object Sculptor Codex Plugin

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Three.js Object Sculptor is a Codex plugin that converts object images into code-only procedural Three.js models. It guides you through a structured sculpting workflow: validate the image, describe the object, decompose it into geometry and material systems, build from blockout to detail, and compare the browser render against the original reference.

This is **not** photogrammetry or mesh extraction. It's a procedural code generation workflow with quality gates, staged building, and AI vision feedback.

## Installation

Clone the plugin to your local plugins directory:

```bash
mkdir -p ~/plugins
git clone <repository-url> ~/plugins/threejs-object-sculptor
```

Create or update `~/.agents/plugins/marketplace.json`:

```json
{
  "name": "local",
  "interface": {
    "displayName": "Local Plugins"
  },
  "plugins": [
    {
      "name": "threejs-object-sculptor",
      "source": {
        "source": "local",
        "path": "./plugins/threejs-object-sculptor"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Productivity"
    }
  ]
}
```

Install the plugin:

```bash
codex plugin add threejs-object-sculptor@local
```

Restart your Codex session to load the plugin skill.

## Core Workflow

The plugin enforces a staged sculpting pipeline:

1. **Image validation** — Check if the reference is suitable for procedural reconstruction
2. **Pre-spec assessment** — Complexity tier and quality contract
3. **Sculpt spec creation** — Full component hierarchy, materials, pivots, sockets
4. **Pass-by-pass building** — Blockout → Structural → Form → Material → Surface → Lighting → Interaction → Optimization
5. **Browser rendering** — Screenshot the generated model
6. **AI vision review** — Compare render vs reference, score features
7. **Self-correction** — Unlock next pass or iterate current pass

## Key Scripts

All scripts run from the plugin root directory.

### Probe Reference Image

Validate whether an image is suitable for procedural reconstruction:

```bash
python3 scripts/probe_reference_image.py ./reference/tower-ship.png
```

**Output**: Suitability score, object class, complexity estimate, visibility notes.

### Create Pre-Spec Assessment

Define complexity tier and quality targets before spec creation:

```bash
python3 scripts/new_pre_spec_assessment.py "Tower Ship" \
  --image ./reference/tower-ship.png \
  --complexity moderate \
  --out assessment.json
```

**Complexity tiers**: `simple`, `moderate`, `complex`, `very-complex`

### Create Sculpt Spec

Generate a complete `ObjectSculptSpec` JSON:

```bash
python3 scripts/new_sculpt_spec.py "Tower Ship" \
  --image ./reference/tower-ship.png \
  --assessment assessment.json \
  --out object-sculpt-spec.json
```

**Spec includes**:
- Component hierarchy (root, children, sockets)
- Material definitions (PBR properties, surface features)
- Lighting setup (type, intensity, shadows)
- Pivots and animation anchors
- Destruction anchors and collider proxies
- Quality targets (overall and per-feature thresholds)

### Validate Sculpt Spec

Check spec completeness and quality gates:

```bash
python3 scripts/validate_sculpt_spec.py object-sculpt-spec.json --strict-quality
```

**Flags**:
- `--strict-quality`: Enforce all quality thresholds
- `--check-pivots`: Require pivots for all animatable components
- `--require-materials`: Fail if any component lacks material definition

### Check Sculpt Pass Status

See which pass is currently unlocked:

```bash
python3 scripts/sculpt_pass_orchestrator.py status object-sculpt-spec.json
```

**Pass order**:
1. `blockout` — Silhouette and major component placement
2. `structural` — Component connections, pivots, hierarchy
3. `form_refinement` — Proportions, curves, secondary shapes
4. `material` — PBR setup, color, roughness, metalness
5. `surface` — Normal maps, height, AO, detail textures
6. `lighting` — Shadows, environment, light response
7. `interaction` — Animation readiness, transform channels
8. `optimization` — LOD, instancing, draw call reduction

### Generate Three.js Factory

Output TypeScript code for the current unlocked pass:

```bash
python3 scripts/generate_threejs_factory.py object-sculpt-spec.json \
  --out src/createTowerShip.ts
```

**Example generated factory**:

```typescript
import * as THREE from 'three';

export interface TowerShipOptions {
  scale?: number;
  color?: THREE.ColorRepresentation;
}

export function createTowerShip(options: TowerShipOptions = {}): THREE.Group {
  const { scale = 1, color = 0x8b4513 } = options;
  
  const root = new THREE.Group();
  root.name = 'TowerShip';
  
  // Hull (blockout pass)
  const hullGeometry = new THREE.BoxGeometry(4, 1, 8);
  const hullMaterial = new THREE.MeshStandardMaterial({
    color,
    roughness: 0.8,
    metalness: 0.2
  });
  const hull = new THREE.Mesh(hullGeometry, hullMaterial);
  hull.name = 'hull';
  hull.position.set(0, 0, 0);
  root.add(hull);
  
  // Tower (blockout pass)
  const towerGeometry = new THREE.CylinderGeometry(0.8, 1.2, 3, 8);
  const tower = new THREE.Mesh(towerGeometry, hullMaterial.clone());
  tower.name = 'tower';
  tower.position.set(0, 2, -1);
  root.add(tower);
  
  // Sail pivot (structural pass - animation ready)
  const sailPivot = new THREE.Group();
  sailPivot.name = 'sailPivot';
  sailPivot.position.set(0, 3.5, -1);
  tower.add(sailPivot);
  
  root.scale.setScalar(scale);
  return root;
}
```

### Make Visual Comparison Sheet

Create a side-by-side reference/render image for AI vision:

```bash
python3 scripts/make_visual_comparison_sheet.py \
  --reference ./reference/tower-ship.png \
  --render ./screenshots/tower-ship-render.png \
  --out ./screenshots/tower-ship-comparison.png \
  --json
```

**Output**: PNG comparison sheet + JSON metadata for vision scoring.

### Record Sculpt Review

Append an AI vision review to the spec:

```bash
python3 scripts/append_sculpt_review.py object-sculpt-spec.json \
  --pass-id blockout \
  --fidelity 0.85 \
  --action continue \
  --summary "Blockout silhouette matches. Hull and tower proportions acceptable." \
  --render-screenshot ./screenshots/tower-ship-render.png \
  --comparison-image ./screenshots/tower-ship-comparison.png \
  --ai-vision-score 0.85 \
  --feature-reviews-json ./reviews/blockout-features.json \
  --ai-vision-notes "Main forms pass; rigging and sail detail deferred to later passes." \
  --in-place
```

**Feature reviews JSON format**:

```json
{
  "features": [
    {
      "feature_id": "hull_shape",
      "score": 0.88,
      "notes": "Silhouette correct, proportions match"
    },
    {
      "feature_id": "tower_placement",
      "score": 0.82,
      "notes": "Position correct, height slightly low"
    },
    {
      "feature_id": "sail_rigging",
      "score": 0.0,
      "notes": "Not implemented in blockout pass"
    }
  ]
}
```

**Actions**: `continue` (unlock next pass), `iterate` (repeat current pass), `block` (critical failure)

### Sync Pass State

Recalculate unlocked pass after review:

```bash
python3 scripts/sculpt_pass_orchestrator.py sync object-sculpt-spec.json --in-place
```

This updates `spec.passes.current_unlocked_pass` based on review history.

## PBR Material Extraction

Extract procedural PBR evidence from reference images:

```bash
python3 scripts/extract_reference_pbr.py ./reference/oak-bark-closeup.png \
  --out-dir ./generated/pbr/oak-bark \
  --material-id bark \
  --target-threshold 0.7 \
  --report ./generated/pbr/oak-bark/report.json
```

**Outputs**:
- `albedo.png` — Base color map
- `roughness.png` — Roughness estimate
- `height.png` — Height/displacement map
- `normal.png` — Normal map (derived)
- `ao.png` — Ambient occlusion estimate
- `report.json` — Confidence scores per channel

**Confidence threshold**: `--target-threshold 0.7` refuses low-quality extraction unless `--allow-low-confidence` is set.

**Use in spec**:

```json
{
  "materials": {
    "bark": {
      "type": "pbr",
      "albedo": {
        "source": "generated/pbr/oak-bark/albedo.png",
        "confidence": 0.82
      },
      "roughness": {
        "source": "generated/pbr/oak-bark/roughness.png",
        "confidence": 0.75
      },
      "normal": {
        "source": "generated/pbr/oak-bark/normal.png",
        "confidence": 0.68
      }
    }
  }
}
```

## Quality Gates

### Overall Fidelity Score

Global match between reference and render:
- Silhouette: 0–1 score
- Proportions: 0–1 score
- Material read: 0–1 score
- Lighting: 0–1 score
- Camera/view alignment: 0–1 score

**Target**: `spec.quality.target_overall_fidelity` (e.g., 0.75)

### Critical Feature Scores

Per-feature thresholds enforce identity-defining details:

```json
{
  "quality": {
    "critical_features": [
      {
        "feature_id": "hull_shape",
        "description": "Main hull silhouette and proportions",
        "target_score": 0.80
      },
      {
        "feature_id": "sail_rigging",
        "description": "Sail attachment and rigging structure",
        "target_score": 0.70
      }
    ]
  }
}
```

**Pass failure**: If **any** critical feature score is below its threshold, the pass fails even if overall score is acceptable.

## Object Sculpt Spec Structure

Complete spec JSON structure:

```json
{
  "metadata": {
    "spec_version": "1.0",
    "object_name": "Tower Ship",
    "reference_image": "./reference/tower-ship.png",
    "created_at": "2026-07-12T10:00:00Z",
    "complexity_tier": "moderate"
  },
  "components": {
    "root": {
      "component_id": "root",
      "name": "TowerShip",
      "type": "group",
      "children": ["hull", "tower"]
    },
    "hull": {
      "component_id": "hull",
      "name": "hull",
      "type": "mesh",
      "geometry": {
        "primitive": "box",
        "dimensions": [4, 1, 8]
      },
      "material_id": "wood_planks",
      "pivot": [0, 0.5, 0],
      "transform": {
        "position": [0, 0, 0],
        "rotation": [0, 0, 0],
        "scale": [1, 1, 1]
      }
    },
    "tower": {
      "component_id": "tower",
      "name": "tower",
      "type": "mesh",
      "geometry": {
        "primitive": "cylinder",
        "radius_top": 0.8,
        "radius_bottom": 1.2,
        "height": 3,
        "segments": 8
      },
      "material_id": "wood_planks",
      "pivot": [0, 0, 0],
      "transform": {
        "position": [0, 2, -1]
      },
      "sockets": {
        "sail_mount": {
          "socket_id": "sail_mount",
          "position": [0, 1.5, 0],
          "orientation": [0, 0, 0],
          "purpose": "sail_attachment"
        }
      }
    }
  },
  "materials": {
    "wood_planks": {
      "type": "pbr",
      "color": "#8b4513",
      "roughness": 0.8,
      "metalness": 0.1,
      "surface_features": {
        "plank_lines": true,
        "weathering": "moderate"
      }
    }
  },
  "lighting": {
    "primary": {
      "type": "directional",
      "color": "#ffffff",
      "intensity": 1.0,
      "direction": [-0.5, -1, -0.3],
      "cast_shadow": true
    },
    "ambient": {
      "type": "ambient",
      "color": "#404040",
      "intensity": 0.3
    }
  },
  "quality": {
    "target_overall_fidelity": 0.75,
    "critical_features": [
      {
        "feature_id": "hull_shape",
        "description": "Main hull silhouette",
        "target_score": 0.80
      }
    ]
  },
  "passes": {
    "current_unlocked_pass": "blockout",
    "completed_passes": [],
    "pass_order": [
      "blockout",
      "structural",
      "form_refinement",
      "material",
      "surface",
      "lighting",
      "interaction",
      "optimization"
    ]
  },
  "reviews": []
}
```

## Animation-Ready Features

The plugin designs objects for action readiness:

### Pivots

Transform origins for rotation and scale:

```json
{
  "pivot": [0, 0.5, 0]
}
```

### Sockets

Attachment points for child objects or effects:

```json
{
  "sockets": {
    "cannon_mount_left": {
      "position": [-1.5, 1, 2],
      "orientation": [0, -1.57, 0],
      "purpose": "weapon_attachment"
    }
  }
}
```

### Transform Channels

Animatable properties:

```json
{
  "animation_channels": {
    "sail_rotation": {
      "property": "rotation.y",
      "range": [-0.5, 0.5]
    },
    "wheel_spin": {
      "property": "rotation.z",
      "range": [0, 6.28]
    }
  }
}
```

### Destruction Anchors

Breakable or detachable parts:

```json
{
  "destruction_anchors": {
    "mast_break": {
      "component_id": "main_mast",
      "break_point": [0, 2.5, 0],
      "fracture_type": "clean_break"
    }
  }
}
```

## Codex Usage Pattern

### Basic Object Generation

In Codex, attach an object image and say:

```
Use Three.js Object Sculptor to turn the object in this attachment into a procedural Three.js model built entirely with code.
```

### With Quality Requirements

```
Create a procedural Three.js model from this tower ship reference. Target overall fidelity 0.80. Make sure hull shape, tower placement, and sail rigging pass their critical feature thresholds.
```

### With Animation Intent

```
Build an animation-ready procedural ship from this image. I need pivots for the wheel, sockets for cannons, and the masts should be detachable for destruction effects.
```

### With Material Detail

```
Create a procedural tree from this ancient oak reference. Extract bark PBR from the trunk closeup region. Target roughness confidence 0.75 minimum.
```

## Troubleshooting

### Image Rejected as Unsuitable

**Symptom**: `probe_reference_image.py` returns low suitability score.

**Solutions**:
- Use images with clear object visibility
- Avoid heavily occluded or abstract compositions
- Provide side/front views rather than extreme angles
- Check lighting — extreme shadows or blown highlights reduce suitability

### Pass Won't Unlock After Review

**Symptom**: `current_unlocked_pass` stays on same pass after `continue` review.

**Solutions**:
- Check critical feature scores — any below threshold blocks progress
- Verify `--action continue` in review command
- Run `sculpt_pass_orchestrator.py sync` to recalculate
- Inspect `spec.reviews` array for blocking reviews

### Generated Code Missing Animation Pivots

**Symptom**: Factory output has objects but no pivot points or sockets.

**Solutions**:
- Ensure `structural` pass is completed before generating
- Add explicit `pivots` and `sockets` to component definitions in spec
- Validate spec with `--check-pivots` flag
- Iterate on structural pass with pivot requirements in review notes

### Low PBR Confidence Scores

**Symptom**: `extract_reference_pbr.py` refuses to output maps.

**Solutions**:
- Use higher resolution reference closeups
- Ensure uniform lighting in material reference region
- Lower `--target-threshold` or add `--allow-low-confidence`
- Manually paint or supplement albedo/roughness maps

### AI Vision Score Doesn't Match Visual Quality

**Symptom**: Comparison looks good but vision score is low.

**Solutions**:
- Verify comparison sheet shows both images clearly
- Check camera angle and zoom match reference
- Use same lighting conditions in render as reference
- Review feature-level scores — global score may hide critical failures

### Spec Validation Fails

**Symptom**: `validate_sculpt_spec.py` reports missing required fields.

**Solutions**:
- Run with `--strict-quality` to see all failures
- Check `components` tree has valid parent-child links
- Ensure all `material_id` references exist in `materials`
- Add `quality.critical_features` if complexity tier is `complex` or higher

## Best Practices

1. **Start with probe**: Always validate reference image suitability before creating spec
2. **Use pre-spec assessment**: Define complexity and quality contract before detailed spec work
3. **Build pass-by-pass**: Don't skip passes — blockout → structural → refinement
4. **Set critical features early**: Define identity features in spec before first pass
5. **Compare at same angle**: Render screenshots should match reference camera position
6. **Extract PBR from closeups**: Use cropped material regions, not full object shots
7. **Review features, not just global score**: Critical features block progress when threshold fails
8. **Plan for animation**: Add pivots and sockets in structural pass, not optimization
9. **Use JSON feature reviews**: Structured per-feature scoring beats text-only summaries
10. **Sync after every review**: Run `sculpt_pass_orchestrator.py sync` to update unlocked pass

## Integration with Three.js Projects

### Import Generated Factory

```typescript
import { createTowerShip } from './createTowerShip';
import * as THREE from 'three';

const scene = new THREE.Scene();
const ship = createTowerShip({ scale: 2, color: 0x654321 });
scene.add(ship);
```

### Animate Using Pivots

```typescript
const ship = createTowerShip();
const wheel = ship.getObjectByName('wheel');
if (wheel) {
  // Pivot was set in structural pass
  wheel.rotation.z += 0.01;
}
```

### Attach to Sockets

```typescript
const cannon = createCannonModel();
const leftMount = ship.getObjectByName('cannon_mount_left');
if (leftMount) {
  leftMount.add(cannon);
}
```

### Destruction Example

```typescript
const mast = ship.getObjectByName('main_mast');
if (mast && shouldBreak) {
  // Destruction anchor defined in spec
  ship.remove(mast);
  const brokenMast = mast.clone();
  scene.add(brokenMast);
  // Apply physics or animation
}
```

## Environment Variables

The plugin scripts do not require API keys or secrets by default. If you extend the workflow to use external vision APIs or cloud rendering:

```bash
export VISION_API_KEY=your_api_key_here
export RENDER_SERVICE_URL=https://your-render-service.com
```

Reference in custom scripts:

```python
import os
api_key = os.environ.get('VISION_API_KEY')
```

## Common Patterns

### Procedural Vegetation

```json
{
  "metadata": {
    "object_name": "Ancient Oak",
    "complexity_tier": "complex"
  },
  "components": {
    "trunk": {
      "geometry": { "primitive": "cylinder" },
      "sockets": {
        "branch_socket_1": { "position": [0, 3, 0] },
        "branch_socket_2": { "position": [0, 5, 1] }
      }
    },
    "branch_1": {
      "geometry": { "primitive": "curve" },
      "pivot": [0, 0, 0]
    }
  },
  "materials": {
    "bark": {
      "type": "pbr",
      "albedo": { "source": "generated/pbr/oak-bark/albedo.png" },
      "roughness": { "source": "generated/pbr/oak-bark/roughness.png" },
      "normal": { "source": "generated/pbr/oak-bark/normal.png" }
    },
    "leaves": {
      "type": "pbr",
      "color": "#8b6914",
      "alpha_test": 0.5,
      "double_sided": true
    }
  }
}
```

### Mechanical Props

```json
{
  "metadata": {
    "object_name": "Vintage Camera",
    "complexity_tier": "moderate"
  },
  "components": {
    "body": {
      "geometry": { "primitive": "box" },
      "material_id": "metal_body"
    },
    "lens": {
      "geometry": { "primitive": "cylinder" },
      "pivot": [0, 0, 0],
      "animation_channels": {
        "focus_ring": { "property": "rotation.z", "range": [0, 3.14] }
      }
    }
  },
  "materials": {
    "metal_body": {
      "type": "pbr",
      "color": "#2a2a2a",
      "roughness": 0.3,
      "metalness": 0.9
    }
  }
}
```

### Destructible Objects

```json
{
  "components": {
    "crate": {
      "component_id": "crate",
      "children": ["panel_top", "panel_front", "panel_left"]
    }
  },
  "destruction_anchors": {
    "panel_top_break": {
      "component_id": "panel_top",
      "break_point": [0, 0.5, 0],
      "fracture_type": "hinge"
    },
    "panel_front_shatter": {
      "component_id": "panel_front",
      "break_point": [0, 0, 0.5],
      "fracture_type": "shatter",
      "fragment_count": 8
    }
  }
}
```

## Summary

Three.js Object Sculptor turns object images into procedural Three.js code through a structured workflow with quality gates, staged building, AI vision feedback, and animation-ready output. Use it when you need code-native Three.js assets with meaningful hierarchy, transform readiness, and visual fidelity validation.
