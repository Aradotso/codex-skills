---
name: threejs-object-sculptor-codex-plugin
description: Convert attached object images into code-only, animation-ready procedural Three.js models through guided sculpting workflow
triggers:
  - turn this image into a Three.js model
  - create a procedural 3D object from this reference
  - sculpt a Three.js object from this attachment
  - generate animation-ready Three.js code for this object
  - build a code-only Three.js model from this image
  - reconstruct this object as procedural Three.js geometry
  - make a browser-ready 3D model from this reference
  - convert this object image to Three.js code
---

# Three.js Object Sculptor Codex Plugin

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Three.js Object Sculptor is a Codex plugin that transforms attached object images into code-only, animation-ready procedural Three.js models. It guides you through a structured sculpting workflow: validate the image, describe the object, decompose into geometry and materials, build from blockout to detail, wire an action-friendly hierarchy, then compare renders against the original reference.

## Core Concept

This plugin does **not** do photogrammetry, mesh extraction, or asset downloading. Instead, it guides Codex through a procedural sculpting workflow with quality gates:

1. **Image validation** - Check if the image is suitable for procedural reconstruction
2. **Pre-spec assessment** - Determine complexity tier and quality targets
3. **Object sculpt spec** - Define component hierarchy, materials, pivots, animation anchors
4. **Staged build pipeline** - Blockout → structural → form → materials → surface → lighting → interaction → optimization
5. **Visual comparison** - Compare rendered output against reference with AI vision scoring
6. **Self-correction** - Block progress when critical features fail threshold

## Installation

### Plugin Installation

Clone into your local Codex plugins directory:

```bash
mkdir -p ~/plugins
git clone <repository-url> ~/plugins/threejs-object-sculptor
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

Restart Codex to load the plugin skill.

### Requirements

- Python 3.10+
- Codex with local plugin support
- Three.js project (for implementing generated factories)

## Quick Start

Attach an object image in Codex and ask:

```
Use Three.js Object Sculptor to turn the object in this attachment into a procedural Three.js model built entirely with code. Make it animation-ready for real-time browser use.
```

The plugin will guide through the full sculpting workflow automatically.

## Core Scripts

All scripts are in the `scripts/` directory and should be run from the plugin root.

### 1. Probe Reference Image

Validate whether an image is suitable for procedural 3D reconstruction:

```bash
python3 scripts/probe_reference_image.py ./reference/spaceship.png
```

Output example:

```json
{
  "suitable": true,
  "object_class": "vehicle_spacecraft",
  "visibility": "clear",
  "complexity_hint": "moderate",
  "warnings": [],
  "recommended_quality_tier": "production_placeholder"
}
```

### 2. Create Pre-Spec Assessment

Define complexity and quality contract before generating the full spec:

```bash
python3 scripts/new_pre_spec_assessment.py "Tower Ship" \
  --image ./reference/tower-ship.png \
  --complexity complex \
  --out assessment.json
```

Complexity tiers: `simple`, `moderate`, `complex`, `very_complex`

### 3. Create Object Sculpt Spec

Generate the full `ObjectSculptSpec` JSON:

```bash
python3 scripts/new_sculpt_spec.py "Tower Ship" \
  --image ./reference/tower-ship.png \
  --assessment assessment.json \
  --out object-sculpt-spec.json
```

Options:
- `--intended-use` - Animation, destruction, transformation, physics
- `--material-classes` - metal, wood, glass, fabric, etc.
- `--target-polycount` - Maximum polygon budget

### 4. Validate Sculpt Spec

Check spec validity and quality gate definitions:

```bash
python3 scripts/validate_sculpt_spec.py object-sculpt-spec.json --strict-quality
```

Flags:
- `--strict-quality` - Enforce all quality gates defined
- `--require-critical-features` - Ensure critical features are specified

### 5. Check Current Sculpt Pass

See which pass is unlocked and ready for generation:

```bash
python3 scripts/sculpt_pass_orchestrator.py status object-sculpt-spec.json
```

Output shows current pass, completion status, and next actions.

### 6. Generate Three.js Factory

Generate TypeScript code for the current unlocked pass:

```bash
python3 scripts/generate_threejs_factory.py object-sculpt-spec.json \
  --out src/createTowerShip.ts \
  --pass blockout
```

Generated factory example structure:

```typescript
import * as THREE from 'three';

export interface TowerShipComponents {
  hull: THREE.Group;
  cabin: THREE.Group;
  sails: THREE.Group[];
  masts: THREE.Group[];
}

export function createTowerShip(): THREE.Group & { components: TowerShipComponents } {
  const root = new THREE.Group();
  root.name = 'TowerShip';
  
  // Blockout geometry
  const hull = new THREE.Group();
  const hullMesh = new THREE.Mesh(
    new THREE.BoxGeometry(8, 2, 3),
    new THREE.MeshStandardMaterial({ color: 0x8B4513 })
  );
  hull.add(hullMesh);
  hull.position.y = 0;
  root.add(hull);
  
  // Cabin
  const cabin = new THREE.Group();
  const cabinMesh = new THREE.Mesh(
    new THREE.BoxGeometry(4, 3, 2.5),
    new THREE.MeshStandardMaterial({ color: 0xD2691E })
  );
  cabin.add(cabinMesh);
  cabin.position.set(0, 2.5, 0);
  root.add(cabin);
  
  // Masts and sails
  const masts: THREE.Group[] = [];
  const sails: THREE.Group[] = [];
  
  for (let i = 0; i < 3; i++) {
    const mast = new THREE.Group();
    const mastPole = new THREE.Mesh(
      new THREE.CylinderGeometry(0.2, 0.2, 8),
      new THREE.MeshStandardMaterial({ color: 0x654321 })
    );
    mast.add(mastPole);
    mast.position.set(i * 2 - 2, 5, 0);
    root.add(mast);
    masts.push(mast);
    
    const sail = new THREE.Mesh(
      new THREE.PlaneGeometry(2, 3),
      new THREE.MeshStandardMaterial({ 
        color: 0xFFF8DC,
        side: THREE.DoubleSide 
      })
    );
    sail.position.set(0, 0, 0.5);
    mast.add(sail);
    sails.push(mast);
  }
  
  const components: TowerShipComponents = {
    hull,
    cabin,
    sails,
    masts
  };
  
  return Object.assign(root, { components });
}
```

### 7. Visual Comparison Sheet

Create a side-by-side comparison image for AI vision review:

```bash
python3 scripts/make_visual_comparison_sheet.py \
  --reference ./reference/tower-ship.png \
  --render ./screenshots/tower-ship-render.png \
  --out ./screenshots/comparison.png \
  --json
```

Outputs both PNG comparison sheet and JSON metadata.

### 8. Record AI Vision Review

Append a sculpt pass review with vision scores:

```bash
python3 scripts/append_sculpt_review.py object-sculpt-spec.json \
  --pass-id blockout \
  --fidelity 0.85 \
  --action continue \
  --summary "Blockout silhouette matches reference. Hull proportions correct." \
  --render-screenshot ./screenshots/tower-ship-render.png \
  --comparison-image ./screenshots/comparison.png \
  --ai-vision-score 0.85 \
  --feature-reviews-json ./reviews/blockout-features.json \
  --ai-vision-notes "Mast spacing acceptable. Sail geometry deferred to form pass." \
  --in-place
```

Feature reviews JSON format:

```json
[
  {
    "feature_id": "hull_shape",
    "name": "Hull Shape",
    "score": 0.9,
    "threshold": 0.75,
    "passed": true,
    "notes": "Silhouette matches reference"
  },
  {
    "feature_id": "mast_positions",
    "name": "Mast Positions",
    "score": 0.8,
    "threshold": 0.7,
    "passed": true,
    "notes": "Spacing acceptable"
  }
]
```

### 9. Sync Pass State

Update pass completion and unlock next pass:

```bash
python3 scripts/sculpt_pass_orchestrator.py sync object-sculpt-spec.json --in-place
```

Pass progression:
1. `blockout` - Basic shapes and proportions
2. `structural` - Core components and hierarchy
3. `form_refinement` - Detailed geometry
4. `material_pass` - Material definitions
5. `surface_pass` - Surface details and textures
6. `lighting_pass` - Lighting response
7. `interaction_pass` - Animation anchors and physics
8. `optimization` - Performance tuning

## PBR Material Extraction

Extract procedural PBR evidence from reference images:

```bash
python3 scripts/extract_reference_pbr.py ./reference/oak-bark.png \
  --out-dir ./generated/pbr/oak-bark \
  --material-id bark \
  --target-threshold 0.7 \
  --report ./generated/pbr/oak-bark/report.json
```

Generates:
- `albedo.png` - Base color map
- `roughness.png` - Roughness estimate
- `height.png` - Height/displacement map
- `normal.png` - Normal map (computed from height)
- `ao.png` - Ambient occlusion estimate
- `palette.json` - Dominant color palette
- `report.json` - Confidence scores and metadata

Options:
- `--allow-low-confidence` - Accept results below threshold
- `--patch-spec` - Auto-update sculpt spec with PBR data

## Object Sculpt Spec Structure

The `ObjectSculptSpec` is a JSON document that defines the complete procedural model plan:

```json
{
  "meta": {
    "name": "Tower Ship",
    "version": "0.1.0",
    "reference_image": "./reference/tower-ship.png",
    "complexity": "complex",
    "intended_use": ["animation", "real_time_rendering"]
  },
  "quality": {
    "target_fidelity": 0.8,
    "critical_features": [
      {
        "id": "hull_shape",
        "name": "Hull Shape",
        "threshold": 0.75,
        "weight": 1.0
      },
      {
        "id": "sail_rigging",
        "name": "Sail Rigging",
        "threshold": 0.7,
        "weight": 0.8
      }
    ],
    "overall_threshold": 0.75,
    "block_on_critical_fail": true
  },
  "components": [
    {
      "id": "hull",
      "name": "Hull",
      "type": "primary",
      "geometry_type": "custom",
      "parent_id": null,
      "pivot": [0, 0, 0],
      "transform_channels": ["position", "rotation"],
      "materials": ["wood_planks"],
      "detail_level": "high"
    },
    {
      "id": "main_mast",
      "name": "Main Mast",
      "type": "articulated",
      "geometry_type": "cylinder",
      "parent_id": "hull",
      "pivot": [0, 2, 0],
      "transform_channels": ["rotation_z"],
      "materials": ["wood_smooth"],
      "sockets": ["sail_attachment_top", "sail_attachment_mid"]
    }
  ],
  "materials": [
    {
      "id": "wood_planks",
      "class": "wood",
      "color": "#8B4513",
      "roughness": 0.7,
      "metalness": 0.0,
      "pbr_evidence": {
        "albedo_map": "./generated/pbr/wood/albedo.png",
        "roughness_map": "./generated/pbr/wood/roughness.png",
        "normal_map": "./generated/pbr/wood/normal.png"
      }
    }
  ],
  "lighting": {
    "ambient_color": "#404040",
    "directional_lights": [
      {
        "color": "#FFFFFF",
        "intensity": 1.0,
        "direction": [-1, -1, -1]
      }
    ]
  },
  "passes": [
    {
      "id": "blockout",
      "name": "Blockout",
      "order": 0,
      "unlocked": true,
      "completed": true,
      "quality_gate": 0.7
    },
    {
      "id": "structural",
      "name": "Structural",
      "order": 1,
      "unlocked": true,
      "completed": false,
      "quality_gate": 0.75
    }
  ],
  "reviews": [
    {
      "pass_id": "blockout",
      "timestamp": "2026-07-12T10:30:00Z",
      "overall_score": 0.85,
      "action": "continue",
      "feature_scores": [
        {"feature_id": "hull_shape", "score": 0.9}
      ]
    }
  ]
}
```

## Workflow Patterns

### Pattern 1: Single Image to Complete Model

```bash
# 1. Probe image
python3 scripts/probe_reference_image.py ./ref/object.png

# 2. Create assessment
python3 scripts/new_pre_spec_assessment.py "Object Name" \
  --image ./ref/object.png \
  --complexity moderate \
  --out assessment.json

# 3. Create spec
python3 scripts/new_sculpt_spec.py "Object Name" \
  --image ./ref/object.png \
  --assessment assessment.json \
  --out spec.json

# 4. Validate
python3 scripts/validate_sculpt_spec.py spec.json --strict-quality

# 5. Loop through passes
for pass in blockout structural form_refinement material_pass; do
  # Generate code
  python3 scripts/generate_threejs_factory.py spec.json \
    --out src/createObject.ts --pass $pass
  
  # (User implements and renders in browser)
  
  # Compare
  python3 scripts/make_visual_comparison_sheet.py \
    --reference ./ref/object.png \
    --render ./screenshots/${pass}.png \
    --out ./screenshots/compare-${pass}.png
  
  # Review
  python3 scripts/append_sculpt_review.py spec.json \
    --pass-id $pass \
    --fidelity 0.8 \
    --action continue \
    --render-screenshot ./screenshots/${pass}.png \
    --comparison-image ./screenshots/compare-${pass}.png \
    --in-place
  
  # Sync
  python3 scripts/sculpt_pass_orchestrator.py sync spec.json --in-place
done
```

### Pattern 2: Material-First Workflow

When the object has distinctive materials, extract PBR evidence first:

```bash
# Extract materials from close-up reference
python3 scripts/extract_reference_pbr.py ./ref/bark-closeup.png \
  --out-dir ./pbr/bark \
  --material-id trunk_bark \
  --target-threshold 0.7

python3 scripts/extract_reference_pbr.py ./ref/leaf-closeup.png \
  --out-dir ./pbr/leaves \
  --material-id foliage \
  --target-threshold 0.65

# Create spec with material evidence
python3 scripts/new_sculpt_spec.py "Ancient Tree" \
  --image ./ref/tree-full.png \
  --assessment assessment.json \
  --out spec.json

# Manually patch spec.json materials section with PBR paths
# Then proceed with normal workflow
```

### Pattern 3: Critical Feature Monitoring

Define strict critical features for identity-sensitive objects:

```json
{
  "quality": {
    "critical_features": [
      {
        "id": "logo_placement",
        "name": "Logo Placement",
        "threshold": 0.9,
        "weight": 1.0,
        "block_on_fail": true
      },
      {
        "id": "wheel_count",
        "name": "Wheel Count",
        "threshold": 1.0,
        "weight": 1.0,
        "block_on_fail": true
      }
    ],
    "block_on_critical_fail": true
  }
}
```

Record reviews with feature-specific scores:

```bash
python3 scripts/append_sculpt_review.py spec.json \
  --pass-id structural \
  --fidelity 0.75 \
  --action retry \
  --summary "Logo position incorrect - blocks progress" \
  --feature-reviews-json reviews.json \
  --in-place
```

## Implementing Generated Factories

### Basic Scene Setup

```typescript
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { createTowerShip } from './createTowerShip';

// Scene setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87CEEB);

const camera = new THREE.PerspectiveCamera(
  75,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.set(15, 10, 15);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);

// Lighting (match spec lighting section)
const ambientLight = new THREE.AmbientLight(0x404040);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xFFFFFF, 1.0);
directionalLight.position.set(-1, -1, -1).normalize();
scene.add(directionalLight);

// Create object
const ship = createTowerShip();
scene.add(ship);

// Animation loop
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();

// Screenshot for review
function captureScreenshot() {
  renderer.render(scene, camera);
  return renderer.domElement.toDataURL('image/png');
}
```

### Animation-Ready Usage

```typescript
const ship = createTowerShip();

// Access components for animation
ship.components.sails.forEach((sail, index) => {
  // Animate sail rotation
  gsap.to(sail.rotation, {
    z: Math.sin(Date.now() * 0.001 + index) * 0.2,
    duration: 2,
    repeat: -1,
    yoyo: true
  });
});

// Animate mast sway
ship.components.masts.forEach(mast => {
  gsap.to(mast.rotation, {
    x: Math.sin(Date.now() * 0.0005) * 0.05,
    duration: 3,
    repeat: -1,
    yoyo: true
  });
});

// Hull bob animation
gsap.to(ship.components.hull.position, {
  y: '+=0.5',
  duration: 2,
  repeat: -1,
  yoyo: true,
  ease: 'sine.inOut'
});
```

## Troubleshooting

### "Image not suitable for procedural reconstruction"

**Cause**: Image is too blurry, ambiguous, or lacks clear object boundaries.

**Solution**: Use a clearer reference image with:
- Single dominant object
- Clear silhouette
- Good contrast
- Minimal occlusion
- Neutral or simple background

### "Critical feature failed threshold"

**Cause**: A identity-defining feature scored below its threshold.

**Solution**: 
1. Review feature-specific scores in the review JSON
2. Identify which component is incorrect
3. Adjust geometry generation in that pass
4. Re-render and re-review
5. Lower threshold only if feature is truly less critical than initially assessed

### "Pass locked - previous pass incomplete"

**Cause**: Previous pass didn't complete successfully or sync didn't run.

**Solution**:
```bash
# Check status
python3 scripts/sculpt_pass_orchestrator.py status spec.json

# Force unlock next pass (use carefully)
python3 scripts/sculpt_pass_orchestrator.py unlock spec.json \
  --pass structural --in-place
```

### "Low PBR extraction confidence"

**Cause**: Reference image doesn't provide clear material evidence.

**Solution**:
```bash
# Allow low confidence (will note in spec)
python3 scripts/extract_reference_pbr.py image.png \
  --material-id mat \
  --allow-low-confidence \
  --out-dir ./pbr/mat

# Or use procedural materials instead of image-derived
```

### Generated code doesn't compile

**Cause**: Three.js version mismatch or missing imports.

**Solution**: Ensure Three.js version compatibility:
```bash
npm install three@^0.150.0
```

Add missing imports:
```typescript
import * as THREE from 'three';
import { mergeGeometries } from 'three/examples/jsm/utils/BufferGeometryUtils';
```

## Quality Gate Best Practices

1. **Set realistic thresholds** - Simple objects: 0.75+, Complex: 0.65-0.75
2. **Define 3-5 critical features max** - Too many makes progress impossible
3. **Weight features appropriately** - Identity features: 1.0, Details: 0.5-0.8
4. **Use block_on_critical_fail** - Only for must-have features
5. **Review with consistent camera angle** - Match reference viewpoint
6. **Capture clean screenshots** - No UI, grid, or debug overlays

## Advanced Patterns

### Multi-View Reference

For complex objects, use multiple reference views:

```bash
# Create base spec from primary view
python3 scripts/new_sculpt_spec.py "Vehicle" \
  --image ./ref/front.png \
  --out spec.json

# Add additional views to reviews
python3 scripts/append_sculpt_review.py spec.json \
  --pass-id structural \
  --fidelity 0.8 \
  --comparison-image ./screenshots/compare-front.png \
  --ai-vision-notes "Front view matches. Side view next." \
  --in-place

# Review side view separately
python3 scripts/make_visual_comparison_sheet.py \
  --reference ./ref/side.png \
  --render ./screenshots/side-render.png \
  --out ./screenshots/compare-side.png
```

### Procedural Variations

Generate spec once, create variations programmatically:

```typescript
export function createTowerShip(config: {
  sailCount?: number;
  hullScale?: number;
  sailColor?: THREE.ColorRepresentation;
} = {}) {
  const { sailCount = 3, hullScale = 1.0, sailColor = 0xFFF8DC } = config;
  
  // Use config to vary generated geometry
  // Maintains same component structure
}

// Generate fleet
const flagship = createTowerShip({ hullScale: 1.5, sailCount: 4 });
const escort1 = createTowerShip({ hullScale: 0.8, sailColor: 0xFFE4B5 });
const escort2 = createTowerShip({ hullScale: 0.8, sailColor: 0xFFE4B5 });
```

### Export to GLB

Add export capability to generated factory:

```typescript
import { GLTFExporter } from 'three/examples/jsm/exporters/GLTFExporter';

export async function exportTowerShipGLB(): Promise<ArrayBuffer> {
  const ship = createTowerShip();
  const exporter = new GLTFExporter();
  
  return new Promise((resolve, reject) => {
    exporter.parse(
      ship,
      (gltf) => resolve(gltf as ArrayBuffer),
      { binary: true },
      (error) => reject(error)
    );
  });
}
```

## Environment Variables

No API keys required. Optional environment variables for tooling:

- `THREEJS_SCULPTOR_TEMP_DIR` - Temporary file storage (default: `/tmp`)
- `THREEJS_SCULPTOR_LOG_LEVEL` - `DEBUG`, `INFO`, `WARN`, `ERROR` (default: `INFO`)

## Resources

- **Live Demos**: 
  - Tower Ship: https://3dship.harrysoftware.com
  - Ancient Tree: https://tree.harrysoftware.com
- **Three.js Documentation**: https://threejs.org/docs/
- **Plugin Repository**: Check README for latest examples and updates
