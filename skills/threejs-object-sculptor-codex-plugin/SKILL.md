```markdown
---
name: threejs-object-sculptor-codex-plugin
description: Turn attached object images into code-only, animation-ready procedural Three.js models using Codex-guided sculpting workflow with quality gates.
triggers:
  - convert this image to a procedural Three.js model
  - turn this object into a Three.js code model
  - create an animation-ready Three.js object from this image
  - build a procedural 3D model from this reference image
  - generate a Three.js factory for this object
  - sculpt a Three.js model from this attached image
  - make a code-only Three.js object from this picture
  - rebuild this object as procedural Three.js geometry
---

# Three.js Object Sculptor

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Three.js Object Sculptor is a Codex plugin that transforms attached object images into quality-gated, animation-ready procedural Three.js models built entirely with code. It guides Codex through a structured sculpting workflow: validate the image, describe the object precisely, decompose it into geometry and material systems, build from blockout to detail, wire an animation-friendly hierarchy, then compare the browser render against the original reference.

**Not photogrammetry.** This plugin does not extract meshes from pixels or download art packs. Instead, it helps Codex infer a procedural model plan and generate TypeScript/Three.js code that approximates the visible object with real pivots, sockets, and transform anchors for animation, physics, and destruction.

## Installation

Clone the plugin into your local Codex plugins directory:

```bash
mkdir -p ~/plugins
git clone https://github.com/vinhhien112/Three.js-Object-Sculptor-Codex-Plugin ~/plugins/threejs-object-sculptor
```

Add to `~/.agents/plugins/marketplace.json`:

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

Restart Codex or start a new thread to load the plugin skill.

## Core Workflow

The plugin enforces a staged build pipeline:

1. **Image validation** — Check if the image is suitable for procedural reconstruction
2. **Pre-spec assessment** — Complexity tier, quality targets, and scope
3. **Object sculpt spec** — Component hierarchy, materials, pivots, sockets, quality gates
4. **Pass-by-pass generation** — Blockout → structural → form → material → surface → lighting → interaction → optimization
5. **Visual comparison** — AI vision review comparing render to reference
6. **Self-correction** — Quality gates block progress if critical features fail

## Key Scripts & Commands

All scripts are run from the plugin root directory.

### 1. Probe Reference Image

Validate whether an image is suitable for procedural 3D reconstruction:

```bash
python3 scripts/probe_reference_image.py ./reference/tower-ship.png
```

**Output:** Suitability report with object class, visibility, complexity estimate, and reconstruction feasibility.

### 2. Create Pre-Spec Assessment

Generate a complexity assessment before code generation:

```bash
python3 scripts/new_pre_spec_assessment.py "Tower Ship" \
  --image ./reference/tower-ship.png \
  --complexity moderate \
  --out assessment.json
```

**Complexity tiers:** `simple`, `moderate`, `complex`, `very-complex`

**Output:** JSON assessment with quality targets, expected component count, material systems, and reconstruction scope.

### 3. Create Object Sculpt Spec

Generate the structured specification that guides all code generation:

```bash
python3 scripts/new_sculpt_spec.py "Tower Ship" \
  --image ./reference/tower-ship.png \
  --assessment assessment.json \
  --out object-sculpt-spec.json
```

**Output:** `ObjectSculptSpec` JSON with:
- Component hierarchy (pivots, sockets, parent-child relationships)
- Material definitions (PBR properties, texture references)
- Lighting setup (key, fill, rim lights)
- Quality gates (overall threshold, critical features)
- Animation anchors (transform channels, detachable parts)
- Destruction anchors (fracture seams, colliders)

### 4. Validate Sculpt Spec

Verify the spec meets structural and quality requirements:

```bash
python3 scripts/validate_sculpt_spec.py object-sculpt-spec.json --strict-quality
```

**Flags:**
- `--strict-quality` — Enforce all quality gate requirements
- `--allow-warnings` — Pass validation with warnings

**Output:** Validation report with errors, warnings, and spec health score.

### 5. Check Current Sculpt Pass

Determine which build pass is currently unlocked:

```bash
python3 scripts/sculpt_pass_orchestrator.py status object-sculpt-spec.json
```

**Pass sequence:**
1. `blockout` — Coarse silhouette and proportions
2. `structural` — Primary component hierarchy
3. `form` — Shape refinement and secondary forms
4. `material` — PBR material application
5. `surface` — Surface detail (normal maps, displacement)
6. `lighting` — Lighting response and shadow behavior
7. `interaction` — Animation/physics readiness
8. `optimization` — Performance and LOD

**Output:** Current pass name, completion status, and blocking issues.

### 6. Generate Three.js Factory

Create the procedural Three.js model code for the current unlocked pass:

```bash
python3 scripts/generate_threejs_factory.py object-sculpt-spec.json \
  --out src/createObjectModel.ts
```

**Output:** TypeScript factory function that constructs the Three.js object hierarchy.

Example generated code structure:

```typescript
import * as THREE from 'three';

export interface ObjectModelOptions {
  pivotMode?: 'local' | 'world';
  lodLevel?: number;
  enablePhysics?: boolean;
}

export function createObjectModel(options: ObjectModelOptions = {}) {
  const root = new THREE.Group();
  root.name = 'TowerShip_Root';
  
  // Component hierarchy with pivots
  const hull = createHull();
  hull.position.set(0, 0, 0);
  root.add(hull);
  
  const cabin = createCabin();
  cabin.position.set(0, 2.5, 0);
  hull.add(cabin);
  
  const sails = createSails();
  sails.position.set(0, 5, 0);
  cabin.add(sails);
  
  // Material application
  applyMaterials(root, options);
  
  // Animation-ready hierarchy
  root.userData.animationAnchors = {
    sails: sails,
    cabin: cabin,
    hull: hull
  };
  
  return root;
}

function createHull(): THREE.Group {
  const hull = new THREE.Group();
  const geometry = new THREE.BoxGeometry(4, 2, 8);
  const mesh = new THREE.Mesh(geometry);
  hull.add(mesh);
  return hull;
}

// ... additional component factories
```

### 7. Create Visual Comparison Sheet

Combine reference and render screenshots for AI vision review:

```bash
python3 scripts/make_visual_comparison_sheet.py \
  --reference ./reference/tower-ship.png \
  --render ./screenshots/tower-ship-render.png \
  --out ./screenshots/tower-ship-comparison.png \
  --json
```

**Output:** 
- Side-by-side comparison PNG
- Optional JSON metadata with image dimensions and alignment

### 8. Extract PBR Evidence

Generate procedural PBR maps from reference image pixels:

```bash
python3 scripts/extract_reference_pbr.py ./reference/oak-bark.png \
  --out-dir ./generated/pbr/oak-bark \
  --material-id bark \
  --target-threshold 0.7 \
  --report ./generated/pbr/oak-bark/report.json
```

**Output:**
- `albedo.png` — Base color map
- `roughness.png` — Roughness estimate
- `height.png` — Height/displacement map
- `normal.png` — Derived normal map
- `ao.png` — Ambient occlusion estimate
- `report.json` — Confidence scores and palette data

**Flags:**
- `--target-threshold` — Minimum confidence (0.0-1.0)
- `--allow-low-confidence` — Override confidence check
- `--material-id` — Material identifier for spec patching

### 9. Record AI Vision Review

Log a visual review with overall and feature-level scores:

```bash
python3 scripts/append_sculpt_review.py object-sculpt-spec.json \
  --pass-id blockout \
  --fidelity 0.82 \
  --action continue \
  --summary "Blockout silhouette acceptable, proportions match reference" \
  --render-screenshot ./screenshots/tower-ship-render.png \
  --comparison-image ./screenshots/tower-ship-comparison.png \
  --ai-vision-score 0.82 \
  --feature-reviews-json ./reviews/blockout-features.json \
  --ai-vision-notes "Hull shape and cabin placement pass; sail detail deferred to surface pass" \
  --in-place
```

**Feature reviews JSON format:**

```json
[
  {
    "feature_id": "hull_shape",
    "description": "Main hull silhouette and proportions",
    "score": 0.88,
    "pass": true,
    "notes": "Width and length proportions match reference"
  },
  {
    "feature_id": "cabin_blocks",
    "description": "Cabin structure and placement",
    "score": 0.75,
    "pass": true,
    "notes": "Position correct, detail will improve in form pass"
  },
  {
    "feature_id": "sail_rigging",
    "description": "Sail mast and rigging structure",
    "score": 0.45,
    "pass": false,
    "critical": true,
    "notes": "Mast angle incorrect, needs correction before advancing"
  }
]
```

**Actions:** `continue`, `retry`, `revise`, `fail`

**Output:** Updated spec with review appended to pass history.

### 10. Sync Pass State

Update pass completion status based on reviews and quality gates:

```bash
python3 scripts/sculpt_pass_orchestrator.py sync object-sculpt-spec.json --in-place
```

**Output:** Updated spec with pass state transitions, next unlocked pass, and blocking issues.

## ObjectSculptSpec Structure

The spec is a JSON document that drives all code generation:

```json
{
  "meta": {
    "spec_version": "1.0.0",
    "object_name": "Tower Ship",
    "object_class": "vehicle",
    "complexity_tier": "moderate",
    "created_at": "2026-07-12T10:00:00Z",
    "reference_image": "./reference/tower-ship.png"
  },
  "quality_contract": {
    "overall_threshold": 0.75,
    "critical_features": [
      {
        "id": "hull_shape",
        "description": "Main hull silhouette",
        "threshold": 0.8,
        "critical": true
      },
      {
        "id": "sail_rigging",
        "description": "Sail mast and rigging",
        "threshold": 0.7,
        "critical": true
      }
    ]
  },
  "component_hierarchy": {
    "root": {
      "id": "root",
      "name": "TowerShip_Root",
      "type": "group",
      "pivot": [0, 0, 0],
      "children": ["hull", "cabin", "sails"]
    },
    "components": {
      "hull": {
        "id": "hull",
        "name": "Hull",
        "type": "mesh_group",
        "parent": "root",
        "pivot": [0, 0, 0],
        "geometry_type": "composite",
        "transform_channel": "position_y",
        "children": ["cabin"]
      },
      "cabin": {
        "id": "cabin",
        "name": "Cabin",
        "type": "mesh_group",
        "parent": "hull",
        "pivot": [0, 2.5, 0],
        "geometry_type": "box",
        "transform_channel": "rotation_y",
        "children": ["sails"]
      },
      "sails": {
        "id": "sails",
        "name": "Sails",
        "type": "mesh",
        "parent": "cabin",
        "pivot": [0, 5, 0],
        "geometry_type": "custom",
        "transform_channel": "scale_x"
      }
    }
  },
  "material_library": {
    "wood_hull": {
      "id": "wood_hull",
      "type": "pbr",
      "base_color": [0.4, 0.25, 0.15],
      "roughness": 0.8,
      "metalness": 0.0,
      "normal_map": "./generated/pbr/hull/normal.png",
      "ao_map": "./generated/pbr/hull/ao.png"
    },
    "canvas_sail": {
      "id": "canvas_sail",
      "type": "pbr",
      "base_color": [0.95, 0.93, 0.88],
      "roughness": 0.9,
      "metalness": 0.0
    }
  },
  "lighting_setup": {
    "key_light": {
      "type": "directional",
      "position": [5, 10, 7],
      "intensity": 1.0,
      "color": [1.0, 0.98, 0.95]
    },
    "fill_light": {
      "type": "hemisphere",
      "sky_color": [0.6, 0.7, 0.9],
      "ground_color": [0.3, 0.3, 0.4],
      "intensity": 0.4
    }
  },
  "animation_system": {
    "sockets": [
      {
        "id": "mast_top",
        "parent_component": "sails",
        "local_position": [0, 3, 0],
        "purpose": "flag_attachment"
      }
    ],
    "transform_channels": [
      {
        "component_id": "sails",
        "channel": "rotation_z",
        "range": [-0.2, 0.2],
        "purpose": "wind_sway"
      }
    ]
  },
  "destruction_system": {
    "detachable_parts": [
      {
        "component_id": "sails",
        "detach_force_threshold": 50.0,
        "fracture_seams": []
      }
    ],
    "collider_proxies": [
      {
        "component_id": "hull",
        "shape": "box",
        "dimensions": [4, 2, 8]
      }
    ]
  },
  "sculpt_passes": {
    "blockout": {
      "id": "blockout",
      "status": "completed",
      "unlocked": true,
      "reviews": [
        {
          "timestamp": "2026-07-12T11:00:00Z",
          "fidelity": 0.82,
          "action": "continue",
          "ai_vision_score": 0.82,
          "feature_scores": {
            "hull_shape": 0.88,
            "cabin_blocks": 0.75
          }
        }
      ]
    },
    "structural": {
      "id": "structural",
      "status": "in_progress",
      "unlocked": true,
      "reviews": []
    }
  }
}
```

## Common Patterns

### Full Reconstruction Workflow

```python
# 1. Validate reference image
import subprocess
result = subprocess.run([
    'python3', 'scripts/probe_reference_image.py',
    './reference/ancient-tree.png'
], capture_output=True, text=True)

# 2. Create pre-spec assessment
subprocess.run([
    'python3', 'scripts/new_pre_spec_assessment.py',
    'Ancient Autumn Tree',
    '--image', './reference/ancient-tree.png',
    '--complexity', 'complex',
    '--out', './specs/tree-assessment.json'
])

# 3. Create sculpt spec
subprocess.run([
    'python3', 'scripts/new_sculpt_spec.py',
    'Ancient Autumn Tree',
    '--image', './reference/ancient-tree.png',
    '--assessment', './specs/tree-assessment.json',
    '--out', './specs/tree-sculpt-spec.json'
])

# 4. Validate spec
subprocess.run([
    'python3', 'scripts/validate_sculpt_spec.py',
    './specs/tree-sculpt-spec.json',
    '--strict-quality'
])

# 5. Generate blockout pass
subprocess.run([
    'python3', 'scripts/generate_threejs_factory.py',
    './specs/tree-sculpt-spec.json',
    '--out', './src/createAncientTree.ts'
])
```

### Iterative Pass Refinement

```python
import subprocess
import json

spec_path = './specs/tower-ship-spec.json'

while True:
    # Check current pass
    result = subprocess.run([
        'python3', 'scripts/sculpt_pass_orchestrator.py',
        'status', spec_path
    ], capture_output=True, text=True)
    
    status = json.loads(result.stdout)
    current_pass = status['current_pass']
    
    if current_pass is None:
        print("All passes complete!")
        break
    
    print(f"Working on: {current_pass}")
    
    # Generate code for current pass
    subprocess.run([
        'python3', 'scripts/generate_threejs_factory.py',
        spec_path,
        '--out', f'./src/createModel_{current_pass}.ts'
    ])
    
    # (Render in browser, capture screenshot, run AI vision review)
    # ...
    
    # Record review (example: auto-continue if score > 0.75)
    ai_score = 0.82  # From AI vision
    action = 'continue' if ai_score >= 0.75 else 'retry'
    
    subprocess.run([
        'python3', 'scripts/append_sculpt_review.py',
        spec_path,
        '--pass-id', current_pass,
        '--fidelity', str(ai_score),
        '--action', action,
        '--summary', f'Pass {current_pass} score: {ai_score}',
        '--ai-vision-score', str(ai_score),
        '--in-place'
    ])
    
    # Sync pass state
    subprocess.run([
        'python3', 'scripts/sculpt_pass_orchestrator.py',
        'sync', spec_path,
        '--in-place'
    ])
    
    if action == 'retry':
        print(f"Pass {current_pass} failed quality gate, retrying...")
        continue
```

### PBR Material Extraction

```python
import subprocess

# Extract PBR maps from bark reference
subprocess.run([
    'python3', 'scripts/extract_reference_pbr.py',
    './reference/oak-bark-closeup.png',
    '--out-dir', './generated/pbr/oak-bark',
    '--material-id', 'bark_ancient',
    '--target-threshold', '0.7',
    '--report', './generated/pbr/oak-bark/report.json'
])

# Patch spec with extracted material data
with open('./generated/pbr/oak-bark/report.json') as f:
    pbr_report = json.load(f)

with open('./specs/tree-sculpt-spec.json') as f:
    spec = json.load(f)

# Update material library
spec['material_library']['bark_ancient']['normal_map'] = './generated/pbr/oak-bark/normal.png'
spec['material_library']['bark_ancient']['ao_map'] = './generated/pbr/oak-bark/ao.png'
spec['material_library']['bark_ancient']['roughness'] = pbr_report['roughness_estimate']

with open('./specs/tree-sculpt-spec.json', 'w') as f:
    json.dump(spec, f, indent=2)
```

## Quality Gates & Critical Features

Quality gates prevent passes from advancing when visual fidelity is insufficient.

**Two-level acceptance:**

1. **Overall match** (silhouette, proportions, material read, lighting)
2. **Critical feature match** (identity-defining features with individual thresholds)

**Example: Tower Ship critical features**

```json
{
  "quality_contract": {
    "overall_threshold": 0.75,
    "critical_features": [
      {
        "id": "hull_shape",
        "description": "Hull silhouette and proportions",
        "threshold": 0.80,
        "critical": true
      },
      {
        "id": "cabin_blocks",
        "description": "Cabin structure placement",
        "threshold": 0.70,
        "critical": true
      },
      {
        "id": "sail_rigging",
        "description": "Mast and sail geometry",
        "threshold": 0.75,
        "critical": true
      },
      {
        "id": "rails",
        "description": "Deck rails and trim",
        "threshold": 0.60,
        "critical": false
      }
    ]
  }
}
```

**Blocking logic:**
- If any **critical** feature fails its threshold, the pass fails
- Overall score must pass its threshold
- Non-critical features log warnings but don't block

## Animation-Ready Hierarchy

The plugin designs objects with animation in mind from the start.

**Key elements:**

1. **Pivots** — Local transform centers for rotation/scale
2. **Sockets** — Attachment points for child objects or effects
3. **Transform channels** — Pre-identified animation properties
4. **Parent-child hierarchy** — Logical component relationships
5. **Detachable parts** — Components that can break off or transform independently

**Example: Ancient Tree animation setup**

```json
{
  "animation_system": {
    "sockets": [
      {
        "id": "branch_01_tip",
        "parent_component": "branch_01",
        "local_position": [2.5, 0, 0],
        "purpose": "leaf_cluster_attachment"
      },
      {
        "id": "trunk_fork",
        "parent_component": "trunk_main",
        "local_position": [0, 5, 0],
        "purpose": "branch_spawn_point"
      }
    ],
    "transform_channels": [
      {
        "component_id": "branch_01",
        "channel": "rotation_z",
        "range": [-0.1, 0.1],
        "purpose": "wind_sway"
      },
      {
        "component_id": "canopy",
        "channel": "scale",
        "range": [0.95, 1.05],
        "purpose": "breathing_idle"
      }
    ],
    "detachable_parts": [
      {
        "component_id": "branch_02",
        "detach_force_threshold": 30.0,
        "fracture_seams": ["trunk_fork"]
      }
    ]
  }
}
```

**Generated TypeScript integration:**

```typescript
export function createAncientTree() {
  const root = new THREE.Group();
  
  const trunk = createTrunk();
  trunk.position.set(0, 0, 0);
  root.add(trunk);
  
  const branch01 = createBranch();
  branch01.position.set(0, 5, 0); // trunk_fork socket
  branch01.rotation.set(0, 0, Math.PI / 6);
  trunk.add(branch01);
  
  // Animation anchors
  root.userData.animationAnchors = {
    trunk,
    branch01,
    sockets: {
      branch_01_tip: new THREE.Vector3(2.5, 0, 0),
      trunk_fork: new THREE.Vector3(0, 5, 0)
    }
  };
  
  // Transform channels for animation
  root.userData.transformChannels = {
    branch01_sway: {
      target: branch01,
      property: 'rotation.z',
      range: [-0.1, 0.1]
    }
  };
  
  return root;
}
```

## Troubleshooting

### Image validation fails

**Problem:** `probe_reference_image.py` reports image is unsuitable.

**Solutions:**
- Ensure object is clearly visible and not occluded
- Use images with clean background or high object-to-background contrast
- Avoid extreme camera angles or heavy perspective distortion
- Provide higher resolution image (minimum 512x512 recommended)

### Spec validation errors

**Problem:** `validate_sculpt_spec.py` reports structural errors.

**Common issues:**
- Missing required component hierarchy fields (`id`, `name`, `type`, `pivot`)
- Orphaned components (parent not in hierarchy)
- Circular parent-child relationships
- Invalid material references
- Quality contract missing critical feature thresholds

**Solution:** Review spec structure against schema, ensure all components have valid parents (except root).

### Pass won't unlock

**Problem:** `sculpt_pass_orchestrator.py status` shows pass is blocked.

**Causes:**
- Previous pass has not passed quality gates
- Critical feature failed in last review
- Review action was `fail` or `revise` instead of `continue`

**Solution:**
```bash
# Check last review for the blocking pass
python3 scripts/sculpt_pass_orchestrator.py status object-sculpt-spec.json

# If critical feature failed, regenerate code and re-review
python3 scripts/generate_threejs_factory.py object-sculpt-spec.json --out src/model.ts

# After fixing and re-rendering, record new review with passing scores
python3 scripts/append_sculpt_review.py object-sculpt-spec.json \
  --pass-id blockout \
  --fidelity 0.85 \
  --action continue \
  --ai-vision-score 0.85 \
  --in-place

# Sync state
python3 scripts/sculpt_pass_orchestrator.py sync object-sculpt-spec.json --in-place
```

### PBR extraction low confidence

**Problem:** `extract_reference_pbr.py` refuses to patch spec due to low confidence.

**Solutions:**
- Use close-up reference image with clear surface detail
- Ensure adequate lighting without blown highlights or deep shadows
- Increase image resolution
- Lower `--target-threshold` if procedural approximation is acceptable
- Use `--allow-low-confidence` flag to force extraction (not recommended for critical materials)

### Generated code doesn't match reference

**Problem:** Visual comparison shows poor match even after multiple passes.

**Diagnosis:**
- Check which critical features are failing
- Review AI vision notes for specific geometry or material issues
- Verify spec component hierarchy matches object structure

**Solutions:**
- Revise spec component decomposition (more/fewer components)
- Adjust quality thresholds if targets are unrealistic for one-image reconstruction
- Add reference views from other angles if hidden sides are critical
- Use PBR extraction for better material approximation
- Consider lowering complexity tier if object is over-scoped

### Three.js factory runtime errors

**Problem:** Generated TypeScript code throws errors when imported.

**Common issues:**
- Missing Three.js imports
- Invalid geometry parameters
- Material texture paths don't exist
- Component hierarchy depth too deep

**Solution:**
```typescript
// Ensure Three.js is installed
// npm install three @types/three

import * as THREE from 'three';

// Verify texture paths are correct
const textureLoader = new THREE.TextureLoader();
const normalMap = textureLoader.load('./generated/pbr/hull/normal.png', 
  undefined, 
  undefined, 
  (err) => console.error('Failed to load texture:', err)
);

// Add null checks for complex hierarchy
if (root.userData.animationAnchors?.branch01) {
  // Safe to use
}
```

## Best Practices

1. **Start with complexity assessment** — Don't skip the pre-spec step; it sets realistic quality targets.

2. **Use quality gates strictly** — Critical features prevent "looks okay" objects that lose identity-defining details.

3. **Extract PBR from close-ups** — General object image for geometry, close-up surface shots for materials.

4. **Design for animation early** — Even static objects benefit from proper pivots and hierarchy for later camera work or interaction.

5. **Review every pass** — Don't let Codex auto-advance; each pass review catches compounding errors early.

6. **Provide multiple reference angles** — Single-image reconstruction makes assumptions; additional views improve accuracy.

7. **Use feature-level scoring** — Overall match can hide failed critical features; always score identity-defining elements separately.

8. **Keep specs under version control** — Commit the JSON spec after each successful pass for rollback capability.

## Environment Variables

No API keys or secrets are required. All processing is local.

Optional environment variables:

```bash
# Override default plugin directory
export CODEX_PLUGIN_DIR=~/custom-plugins

# Default Three.js project output path
export THREEJS_OUTPUT_DIR=./src/models

# PBR extraction quality
export PBR_EXTRACTION_QUALITY=high  # low|medium|high
```

## Integration with Three.js Projects

Example integration into a Vite + Three.js project:

```typescript
// src/main.ts
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { createTowerShip } from './models/createTowerShip';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
camera.position.set(10, 10, 10);

// Add generated model
const towerShip = createTowerShip({
  pivotMode: 'local',
  lodLevel: 1,
  enablePhysics: false
});

scene.add(towerShip);

// Lighting (matches spec lighting_setup)
const keyLight = new THREE.DirectionalLight(0xFFF9F2, 1.0);
keyLight.position.set(5, 10, 7);
scene.add(keyLight);

const hemiLight = new THREE.HemisphereLight(0x99B3E6, 0x4D4D66, 0.4);
scene.add(hemiLight);

// Animation using generated anchors
function animate() {
  requestAnimationFrame(animate);
  
  // Use transform channels from spec
  if (towerShip.userData.transformChannels?.sail_
