---
name: threejs-object-sculptor-codex-plugin
description: Turn attached object images into code-only, animation-ready procedural Three.js models through guided sculpting workflows
triggers:
  - turn this image into a three.js model
  - create a procedural 3d object from this reference
  - build an animation-ready threejs model from this image
  - sculpt a threejs object from this attachment
  - generate a procedural model for this object image
  - convert this reference into a threejs factory
  - make this into a code-only three.js model
  - rebuild this object as procedural threejs geometry
---

# Three.js Object Sculptor Codex Plugin

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

Three.js Object Sculptor is a Codex plugin that reconstructs objects from attached images as code-only procedural Three.js models. It guides Codex through a structured sculpting workflow: validate image suitability, create detailed object specs, decompose geometry and materials, build from blockout to detail with staged passes, wire animation-ready hierarchies, and compare browser renders against original references using AI vision review.

This is **not** photogrammetry or mesh extraction. It's a systematic workflow for generating procedural Three.js factories with quality gates, critical feature validation, and animation readiness baked in.

## Installation

### Plugin Setup

Clone the plugin into your local Codex plugins directory:

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

Restart Codex or start a new thread to load the plugin skill.

### Requirements

- Python 3.10+
- Three.js project for implementation
- Codex with local plugin support
- Image processing tools (PIL/Pillow recommended for PBR extraction)

## Core Workflow

### 1. Image Suitability Check

Before starting, validate whether an image is suitable for procedural reconstruction:

```bash
python3 scripts/probe_reference_image.py ./reference/tower-ship.png
```

**Output:**
- Image resolution and aspect ratio
- Dominant object detection confidence
- Occlusion/ambiguity warnings
- Suitability score (0.0-1.0)

### 2. Pre-Spec Complexity Assessment

Create a complexity assessment before generating the full spec:

```bash
python3 scripts/new_pre_spec_assessment.py "Tower Ship" \
  --image ./reference/tower-ship.png \
  --complexity complex \
  --out assessment.json
```

**Complexity tiers:**
- `simple`: Basic primitives, <10 components, uniform materials
- `moderate`: Compound shapes, 10-30 components, 2-4 material types
- `complex`: Intricate geometry, 30+ components, procedural details, layered materials
- `extreme`: Organic forms, dense hierarchies, procedural systems (foliage, fractals)

### 3. Object Sculpt Spec Creation

Generate the full `ObjectSculptSpec` JSON:

```bash
python3 scripts/new_sculpt_spec.py "Tower Ship" \
  --image ./reference/tower-ship.png \
  --assessment assessment.json \
  --out object-sculpt-spec.json
```

**Spec structure:**
```json
{
  "objectName": "Tower Ship",
  "referenceImagePath": "./reference/tower-ship.png",
  "complexity": "complex",
  "componentHierarchy": [
    {
      "id": "hull_base",
      "type": "structural",
      "geometryPrimitives": ["box", "cylinder"],
      "parentId": null,
      "pivotRole": "root",
      "socketRoles": ["deck_mount", "mast_socket"]
    }
  ],
  "materials": [
    {
      "id": "wood_hull",
      "baseType": "MeshStandardMaterial",
      "pbrParams": {
        "roughness": 0.8,
        "metalness": 0.1
      }
    }
  ],
  "qualityTargets": {
    "silhouetteFidelity": 0.85,
    "criticalFeatures": [
      {
        "id": "tower_structure",
        "threshold": 0.8,
        "failureIsCritical": true
      }
    ]
  },
  "sculptPasses": [
    {
      "passId": "blockout",
      "unlocked": true,
      "completed": false
    }
  ]
}
```

### 4. Spec Validation

Validate the spec before code generation:

```bash
python3 scripts/validate_sculpt_spec.py object-sculpt-spec.json --strict-quality
```

**Validation checks:**
- Component hierarchy integrity (no orphans, valid parent references)
- Material assignments match component IDs
- Pivot/socket references exist
- Quality target thresholds are reasonable (0.0-1.0)
- Critical features are defined for complex objects
- Pass dependencies are acyclic

### 5. Staged Sculpt Passes

Check which pass is currently unlocked:

```bash
python3 scripts/sculpt_pass_orchestrator.py status object-sculpt-spec.json
```

**Standard pass sequence:**
1. **blockout**: Silhouette, primary proportions, coarse component layout
2. **structural**: Refined geometry, correct pivots, parent-child hierarchy
3. **form**: Surface curvature, edge flow, secondary shapes
4. **material**: PBR setup, texture coordinates, material layers
5. **surface**: Fine detail, normal variation, procedural noise
6. **lighting**: Environment response, shadow casting, reflection
7. **interaction**: Animation anchors, colliders, destruction seams
8. **optimization**: LOD, instance batching, draw call reduction

Generate code for the current unlocked pass:

```bash
python3 scripts/generate_threejs_factory.py object-sculpt-spec.json \
  --out src/createTowerShip.ts
```

**Generated factory structure:**

```typescript
import * as THREE from 'three';

export interface TowerShipOptions {
  scale?: number;
  animationReady?: boolean;
}

export function createTowerShip(options: TowerShipOptions = {}): THREE.Group {
  const { scale = 1, animationReady = true } = options;
  const root = new THREE.Group();
  root.name = 'TowerShip';

  // Blockout: hull base
  const hullGeometry = new THREE.BoxGeometry(4 * scale, 1 * scale, 2 * scale);
  const hullMaterial = new THREE.MeshStandardMaterial({
    color: 0x8B4513,
    roughness: 0.8,
    metalness: 0.1
  });
  const hull = new THREE.Mesh(hullGeometry, hullMaterial);
  hull.name = 'hull_base';
  hull.userData.pivotRole = 'root';
  hull.userData.sockets = ['deck_mount', 'mast_socket'];
  root.add(hull);

  // Tower structure (critical feature)
  const towerGeometry = new THREE.CylinderGeometry(0.5 * scale, 0.6 * scale, 3 * scale, 8);
  const towerMaterial = new THREE.MeshStandardMaterial({
    color: 0xA0522D,
    roughness: 0.7
  });
  const tower = new THREE.Mesh(towerGeometry, towerMaterial);
  tower.name = 'tower_structure';
  tower.position.set(0, 2 * scale, 0);
  tower.userData.criticalFeature = true;
  hull.add(tower);

  if (animationReady) {
    // Add animation anchors, transform channels
    hull.userData.transformChannels = ['position', 'rotation'];
    tower.userData.transformChannels = ['rotation'];
  }

  return root;
}
```

### 6. Visual Comparison & Review

After rendering the model in browser, create a comparison sheet:

```bash
python3 scripts/make_visual_comparison_sheet.py \
  --reference ./reference/tower-ship.png \
  --render ./screenshots/tower-ship-render.png \
  --out ./screenshots/tower-ship-comparison.png \
  --json
```

This creates a side-by-side comparison image and optional JSON metadata for AI vision review.

Record an AI vision review:

```bash
python3 scripts/append_sculpt_review.py object-sculpt-spec.json \
  --pass-id blockout \
  --fidelity 0.82 \
  --action continue \
  --summary "Blockout proportions acceptable, tower silhouette matches critical threshold." \
  --render-screenshot ./screenshots/tower-ship-render.png \
  --comparison-image ./screenshots/tower-ship-comparison.png \
  --ai-vision-score 0.82 \
  --feature-reviews-json ./reviews/blockout-features.json \
  --ai-vision-notes "Hull shape correct, tower height ratio passes, deck detail deferred to structural pass." \
  --in-place
```

**Feature reviews JSON format:**

```json
{
  "features": [
    {
      "id": "tower_structure",
      "score": 0.85,
      "notes": "Cylindrical form and height proportion match reference"
    },
    {
      "id": "hull_base",
      "score": 0.80,
      "notes": "Silhouette correct, surface detail deferred"
    }
  ]
}
```

**Review actions:**
- `continue`: Pass threshold met, unlock next pass
- `refine`: Acceptable but needs iteration within current pass
- `fail`: Critical feature or overall threshold missed, block progression

### 7. Pass Synchronization

Update pass state based on reviews:

```bash
python3 scripts/sculpt_pass_orchestrator.py sync object-sculpt-spec.json --in-place
```

This marks completed passes and unlocks the next pass in the pipeline when quality gates are met.

## PBR Material Extraction

Extract reference-derived PBR evidence from image pixels:

```bash
python3 scripts/extract_reference_pbr.py ./reference/oak-bark.png \
  --out-dir ./generated/pbr/oak-bark \
  --material-id bark \
  --target-threshold 0.7 \
  --report ./generated/pbr/oak-bark/report.json
```

**Generated outputs:**
- `albedo.png`: Base color map
- `roughness.png`: Surface roughness estimate
- `height.png`: Height/displacement map
- `normal.png`: Normal map (derived from height)
- `ao.png`: Ambient occlusion estimate
- `palette.json`: Dominant color clusters
- `report.json`: Confidence scores and metadata

**Patch spec with PBR evidence:**

```bash
python3 scripts/extract_reference_pbr.py ./reference/oak-bark.png \
  --out-dir ./generated/pbr/oak-bark \
  --material-id bark \
  --target-threshold 0.7 \
  --patch-spec object-sculpt-spec.json \
  --in-place
```

**Spec material entry after patching:**

```json
{
  "id": "bark",
  "baseType": "MeshStandardMaterial",
  "pbrParams": {
    "roughness": 0.75,
    "metalness": 0.05
  },
  "pbrEvidence": {
    "extractedFrom": "./reference/oak-bark.png",
    "albedoPath": "./generated/pbr/oak-bark/albedo.png",
    "roughnessPath": "./generated/pbr/oak-bark/roughness.png",
    "heightPath": "./generated/pbr/oak-bark/height.png",
    "normalPath": "./generated/pbr/oak-bark/normal.png",
    "aoPath": "./generated/pbr/oak-bark/ao.png",
    "confidence": 0.78
  }
}
```

Use `--allow-low-confidence` to patch even when confidence < threshold (not recommended for production).

## Component Hierarchy Patterns

### Animation-Ready Pivots

```json
{
  "id": "door_left",
  "type": "articulated",
  "geometryPrimitives": ["box"],
  "parentId": "chassis",
  "pivotRole": "hinge",
  "pivotOffset": [-0.5, 0, 0],
  "transformChannels": ["rotation.y"],
  "animationAnchors": [
    {
      "id": "door_open_anchor",
      "type": "rotation",
      "axis": "y",
      "range": [0, 1.57]
    }
  ]
}
```

### Destructible Components

```json
{
  "id": "window_panel",
  "type": "detachable",
  "geometryPrimitives": ["plane"],
  "parentId": "building_facade",
  "destructionAnchors": [
    {
      "id": "shatter_origin",
      "type": "fracture",
      "pattern": "radial",
      "fragments": 12
    }
  ],
  "colliderProxy": {
    "type": "box",
    "dimensions": [1, 1.5, 0.1]
  }
}
```

### Socket-Based Assembly

```json
{
  "id": "main_deck",
  "type": "structural",
  "socketRoles": ["mast_socket", "cannon_mount_port", "cannon_mount_starboard"],
  "sockets": [
    {
      "id": "mast_socket",
      "position": [0, 0.5, 0],
      "rotation": [0, 0, 0],
      "acceptsTypes": ["mast", "pole"]
    }
  ]
}
```

## Quality Gate Configuration

### Critical Features

Define features that must pass individual thresholds:

```json
{
  "qualityTargets": {
    "silhouetteFidelity": 0.85,
    "criticalFeatures": [
      {
        "id": "trunk_fork",
        "description": "Primary trunk split into two main branches",
        "threshold": 0.80,
        "failureIsCritical": true,
        "passRestriction": "blockout"
      },
      {
        "id": "canopy_mass",
        "description": "Overall foliage volume and silhouette",
        "threshold": 0.75,
        "failureIsCritical": true,
        "passRestriction": "form"
      },
      {
        "id": "bark_texture",
        "description": "Bark material roughness and color variation",
        "threshold": 0.70,
        "failureIsCritical": false,
        "passRestriction": "material"
      }
    ]
  }
}
```

**Failure behavior:**
- If `failureIsCritical: true` and score < threshold → pass fails even if overall score is high
- If `failureIsCritical: false` → logged as warning, pass can still succeed

### Pass-Specific Quality

Each pass can override global quality targets:

```json
{
  "passId": "blockout",
  "unlocked": true,
  "completed": false,
  "qualityOverride": {
    "silhouetteFidelity": 0.75,
    "allowedDeviations": ["fine_detail", "material_accuracy"]
  }
}
```

## Codex Usage Patterns

### Basic Object Reconstruction

**User prompt:**
```
Use Three.js Object Sculptor to turn this tower ship image into a procedural Three.js model.
```

**Agent workflow:**
1. Call `probe_reference_image.py` to validate image
2. Create `new_pre_spec_assessment.py` for complexity planning
3. Generate `new_sculpt_spec.py` with component hierarchy
4. Validate spec with `validate_sculpt_spec.py --strict-quality`
5. Generate blockout pass with `generate_threejs_factory.py`
6. Implement generated TypeScript in Three.js project
7. Capture browser render screenshot
8. Create comparison sheet with `make_visual_comparison_sheet.py`
9. Record AI vision review with `append_sculpt_review.py`
10. If review passes, sync passes with `sculpt_pass_orchestrator.py sync`
11. Repeat for structural, form, material passes

### Animation-Ready Object

**User prompt:**
```
Make this mechanical arm animation-ready with working joints and rotation anchors.
```

**Agent considerations:**
1. Mark all joint components with `pivotRole: "hinge"` or `"ball_joint"`
2. Define `transformChannels` for each articulated component
3. Add `animationAnchors` with axis, range, and constraints
4. Parent hierarchy must support forward kinematics
5. Include `socketRoles` for attachments (gripper, tool mount)
6. Add collider proxies for physics interaction
7. Test rotation ranges don't cause interpenetration

### Destructible Object

**User prompt:**
```
Turn this vase into a destructible object with fracture points and physics-ready fragments.
```

**Agent workflow:**
1. Identify fracture seams in spec (rim, body, base)
2. Add `destructionAnchors` with fracture patterns
3. Mark components as `"detachable"`
4. Define `colliderProxy` for each fragment
5. Plan fragment parent hierarchy (all fragments initially parented to intact root)
6. Add `effectEmitters` for impact particles
7. Include `fragmentMass` and `fragmentCenterOfMass` estimates
8. Generate code that instantiates fragments as separate meshes

## Advanced Patterns

### Procedural Variation

Generate slight variations of the same object:

```typescript
export function createTowerShip(options: TowerShipOptions & { seed?: number } = {}): THREE.Group {
  const { seed = 42 } = options;
  const rng = new SeededRandom(seed);
  
  // Vary tower height by ±10%
  const towerHeight = 3 + rng.range(-0.3, 0.3);
  
  // Randomize plank count
  const plankCount = Math.floor(rng.range(8, 12));
  
  // Procedural wear
  const wearFactor = rng.range(0.2, 0.8);
  hullMaterial.roughness = 0.7 + wearFactor * 0.2;
}
```

### LOD Integration

Add level-of-detail switching:

```typescript
export function createTowerShipLOD(options: TowerShipOptions = {}): THREE.LOD {
  const lod = new THREE.LOD();
  
  const high = createTowerShip({ ...options, detail: 'high' });
  const medium = createTowerShip({ ...options, detail: 'medium' });
  const low = createTowerShip({ ...options, detail: 'low' });
  
  lod.addLevel(high, 0);
  lod.addLevel(medium, 50);
  lod.addLevel(low, 100);
  
  return lod;
}
```

### Instance Batching

For repeated objects (trees, props):

```typescript
export function createForestBatch(treeCount: number): THREE.InstancedMesh {
  const baseTree = createAncientTree({ detail: 'medium' });
  const geometry = mergeGeometries(baseTree); // Merge all meshes
  const material = baseTree.children[0].material;
  
  const instancedMesh = new THREE.InstancedMesh(geometry, material, treeCount);
  
  for (let i = 0; i < treeCount; i++) {
    const matrix = new THREE.Matrix4();
    matrix.setPosition(
      Math.random() * 100 - 50,
      0,
      Math.random() * 100 - 50
    );
    instancedMesh.setMatrixAt(i, matrix);
  }
  
  return instancedMesh;
}
```

## Troubleshooting

### Image Not Suitable

**Error:** `Suitability score 0.42, requires >= 0.6`

**Solutions:**
- Use a clearer reference with single dominant object
- Crop out background clutter
- Increase image resolution (min 512px on shortest side)
- Choose image with clear silhouette and minimal occlusion

### Component Hierarchy Validation Failed

**Error:** `Component 'wheel_rear_right' references non-existent parent 'chassis_rear'`

**Solutions:**
- Check all `parentId` references exist as component `id`
- Ensure no circular parent chains
- Verify root component has `parentId: null`

### Critical Feature Failed

**Error:** `Critical feature 'tower_structure' scored 0.65, threshold 0.80, pass FAILED`

**Solutions:**
- Review comparison sheet to identify visual mismatch
- Refine geometry in current pass before progressing
- Lower threshold if feature is inherently ambiguous in reference
- Add more geometry primitives to component definition
- Check if material or lighting is causing false negative

### Pass Won't Unlock

**Error:** `Cannot unlock 'form' pass, dependency 'structural' not completed`

**Solutions:**
- Run `sculpt_pass_orchestrator.py status` to see pass chain
- Ensure previous pass has AI vision review with `action: continue`
- Run `sync` to update pass states
- Check `sculptPasses[].completed` in spec JSON

### Low PBR Extraction Confidence

**Warning:** `PBR extraction confidence 0.58 below threshold 0.70`

**Solutions:**
- Use higher resolution reference crop
- Choose region with clear material variation (not flat color)
- Adjust `--target-threshold` if acceptable
- Use `--allow-low-confidence` flag (inspect outputs first)
- Manually provide PBR maps instead of extraction

### Generated Code Doesn't Match Reference

**Issue:** Silhouette is wrong even after blockout review

**Solutions:**
- Review component hierarchy: are all major parts defined?
- Check geometry primitives: too coarse or wrong types?
- Verify scale factors in `createObject()` match proportions
- Add more components to hierarchy before code generation
- Use AI vision review to identify which feature is mismatched

## Configuration

### Default Quality Thresholds

Edit in spec or pass to CLI:

```bash
python3 scripts/new_sculpt_spec.py "Object Name" \
  --image ./reference.png \
  --silhouette-fidelity 0.80 \
  --overall-match 0.75 \
  --out spec.json
```

### Custom Pass Sequence

Override default passes:

```json
{
  "sculptPasses": [
    { "passId": "rough_blockout", "unlocked": true },
    { "passId": "refined_blockout", "unlocked": false },
    { "passId": "material_blockout", "unlocked": false },
    { "passId": "final_detail", "unlocked": false }
  ]
}
```

### Environment Variables

For PBR extraction and comparison tools:

```bash
export THREEJS_SCULPTOR_DEFAULT_THRESHOLD=0.75
export THREEJS_SCULPTOR_STRICT_VALIDATION=true
export THREEJS_SCULPTOR_COMPARISON_DPI=150
```

## Integration with Three.js Projects

### Vite + TypeScript Setup

```typescript
// src/main.ts
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls';
import { createTowerShip } from './createTowerShip';

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({ antialias: true });

renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);

const towerShip = createTowerShip({ scale: 1, animationReady: true });
scene.add(towerShip);

const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
directionalLight.position.set(5, 10, 5);
scene.add(ambientLight, directionalLight);

camera.position.set(10, 10, 10);
controls.update();

function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}
animate();
```

### Capture Render Screenshot

Use browser DevTools or:

```typescript
function captureScreenshot(renderer: THREE.WebGLRenderer, filename: string) {
  renderer.domElement.toBlob((blob) => {
    const url = URL.createObjectURL(blob!);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.click();
  });
}

// After render
captureScreenshot(renderer, 'tower-ship-render.png');
```

## Common Codex Prompts

**Iterative refinement:**
```
The tower height is too short compared to reference. Increase it by 30% and regenerate the structural pass.
```

**Add animation:**
```
Add rotation animation to the tower component, pivoting from the base, 360 degrees over 10 seconds.
```

**Material enhancement:**
```
Extract PBR evidence from the hull reference crop and apply it to the wood_hull material.
```

**Quality review:**
```
Create a comparison sheet and run AI vision review. If overall score > 0.8 and all critical features pass, unlock the next pass.
```

**Destructible setup:**
```
Mark the tower as a detachable component with radial fracture pattern and 8 fragments.
```

This skill enables Codex to systematically reconstruct objects from images as procedural Three.js code with animation readiness, quality validation, and iterative refinement workflows.
