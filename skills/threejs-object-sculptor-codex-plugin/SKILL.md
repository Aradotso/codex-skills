---
name: threejs-object-sculptor-codex-plugin
description: Codex plugin that converts object images into code-only, animation-ready procedural Three.js models through a staged sculpting workflow with quality gates.
triggers:
  - turn this image into a Three.js model
  - create a procedural 3D object from this reference
  - build an animation-ready Three.js prop from this image
  - reconstruct this object as Three.js geometry code
  - sculpt a Three.js model from this attachment
  - generate a code-only 3D model using Three.js Object Sculptor
  - convert this reference image to a procedural Three.js asset
  - make this object into a browser-rendered Three.js scene
---

# Three.js Object Sculptor Codex Plugin

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

Three.js Object Sculptor is a Codex plugin that transforms object images into code-only procedural Three.js models. Instead of photogrammetry or mesh extraction, it guides Codex through a structured sculpting workflow: validate the image, describe the object, decompose it into geometry and material systems, build from blockout to detail, wire an animation-friendly hierarchy, then compare the browser render against the original reference using AI vision.

**Key characteristics:**

- **Code-only output**: Generates TypeScript/JavaScript Three.js factory functions, not GLB or OBJ files
- **Animation-ready**: Models include pivots, sockets, parent-child hierarchy, and transform anchors
- **Quality-gated**: Uses AI vision to compare renders against reference and fails passes when critical features don't match
- **Staged workflow**: Blockout → structural → form refinement → material → surface → lighting → interaction → optimization
- **Procedural materials**: Extracts PBR evidence (albedo, roughness, normal, AO) from reference images

**Best for:** Real-time browser props, game objects, scene dressing, destructible objects, mechanical parts, botanical objects, stylized reconstructions.

**Not for:** Photogrammetry, exact mesh extraction, scanned assets, production-perfect geometry from a single image.

## Installation

### Clone the Plugin

```bash
mkdir -p ~/plugins
git clone <repository-url> ~/plugins/threejs-object-sculptor
```

### Configure Local Codex Marketplace

Create or edit `~/.agents/plugins/marketplace.json`:

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
        "path": "~/plugins/threejs-object-sculptor"
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

### Install Plugin in Codex

```bash
codex plugin add threejs-object-sculptor@local
```

Restart Codex or start a new thread to load the plugin skill.

## Requirements

- Python 3.10+
- Three.js project for implementation
- Codex with local plugin support
- Browser screenshot capability for visual acceptance testing

## Core Workflow

### 1. Probe Reference Image

Check if an image is suitable for procedural 3D reconstruction:

```bash
python3 scripts/probe_reference_image.py ./reference/spaceship.png
```

**Output:** Suitability assessment (valid/invalid), detected object class, complexity tier, and recommended strategy.

### 2. Create Pre-Spec Assessment

Generate a complexity assessment before code generation:

```bash
python3 scripts/new_pre_spec_assessment.py "Cargo Spaceship" \
  --image ./reference/spaceship.png \
  --complexity moderate \
  --out assessment.json
```

**Complexity tiers:** `simple`, `moderate`, `complex`, `extreme`

**Assessment includes:**
- Estimated geometry primitive count
- Material system complexity
- Animation rig requirements
- Quality contract (fidelity targets)

### 3. Create Object Sculpt Spec

Generate the detailed specification document:

```bash
python3 scripts/new_sculpt_spec.py "Cargo Spaceship" \
  --image ./reference/spaceship.png \
  --assessment assessment.json \
  --out object-sculpt-spec.json
```

**Spec structure:**
- Component hierarchy with parent-child relationships
- Material definitions (albedo, roughness, metalness, emission)
- Lighting response targets
- Pivot points and sockets for animation
- Destruction anchors and detachable components
- Quality thresholds per pass

### 4. Validate Sculpt Spec

Ensure spec integrity before code generation:

```bash
python3 scripts/validate_sculpt_spec.py object-sculpt-spec.json --strict-quality
```

**Validates:**
- Required fields presence
- Component hierarchy consistency
- Material property ranges
- Pass state logic
- Quality threshold sanity

### 5. Check Unlocked Pass

Determine which sculpting pass is currently active:

```bash
python3 scripts/sculpt_pass_orchestrator.py status object-sculpt-spec.json
```

**Pass sequence:**
1. `blockout` – Core silhouette and proportions
2. `structural` – Primary component placement
3. `form-refinement` – Shape accuracy
4. `material-pass` – Material application
5. `surface-pass` – Surface detail and texture response
6. `lighting-pass` – Lighting and shadow behavior
7. `interaction-pass` – Animation readiness, pivots, sockets
8. `optimization` – Performance tuning

### 6. Generate Three.js Factory

Create the procedural model code for the current pass:

```bash
python3 scripts/generate_threejs_factory.py object-sculpt-spec.json \
  --out src/createCargoSpaceship.ts
```

**Generated factory structure:**

```typescript
import * as THREE from 'three';

interface CargoSpaceshipConfig {
  scale?: number;
  material?: THREE.Material;
  enableAnimations?: boolean;
}

export function createCargoSpaceship(
  config: CargoSpaceshipConfig = {}
): THREE.Group {
  const root = new THREE.Group();
  root.name = 'CargoSpaceship';

  // Blockout geometry
  const hullGeometry = new THREE.BoxGeometry(10, 3, 5);
  const hullMaterial = new THREE.MeshStandardMaterial({
    color: 0x8b8b8b,
    metalness: 0.7,
    roughness: 0.3
  });
  const hull = new THREE.Mesh(hullGeometry, hullMaterial);
  hull.name = 'hull';
  root.add(hull);

  // Cabin component (with pivot)
  const cabinGroup = new THREE.Group();
  cabinGroup.name = 'cabin';
  cabinGroup.position.set(0, 1.5, 2);
  
  const cabinGeometry = new THREE.BoxGeometry(3, 2, 2);
  const cabin = new THREE.Mesh(cabinGeometry, hullMaterial);
  cabinGroup.add(cabin);
  root.add(cabinGroup);

  // Engines (detachable components)
  const leftEngine = createEngine();
  leftEngine.name = 'leftEngine';
  leftEngine.position.set(-4, -1, -2);
  leftEngine.userData.detachable = true;
  root.add(leftEngine);

  const rightEngine = createEngine();
  rightEngine.name = 'rightEngine';
  rightEngine.position.set(4, -1, -2);
  rightEngine.userData.detachable = true;
  root.add(rightEngine);

  // Apply config
  if (config.scale) root.scale.setScalar(config.scale);

  return root;
}

function createEngine(): THREE.Group {
  const group = new THREE.Group();
  const geometry = new THREE.CylinderGeometry(0.5, 0.7, 2, 16);
  const material = new THREE.MeshStandardMaterial({
    color: 0x4a4a4a,
    metalness: 0.9,
    roughness: 0.2,
    emissive: 0x0044ff,
    emissiveIntensity: 0.3
  });
  const mesh = new THREE.Mesh(geometry, material);
  mesh.rotation.x = Math.PI / 2;
  group.add(mesh);
  return group;
}
```

### 7. Create Visual Comparison Sheet

After rendering the model, generate a side-by-side comparison:

```bash
python3 scripts/make_visual_comparison_sheet.py \
  --reference ./reference/spaceship.png \
  --render ./screenshots/spaceship-render.png \
  --out ./screenshots/spaceship-comparison.png \
  --json
```

**Output:** Combined image with reference on left, render on right, plus JSON metadata.

### 8. Record AI Vision Review

Submit the comparison for AI vision analysis and record the results:

```bash
python3 scripts/append_sculpt_review.py object-sculpt-spec.json \
  --pass-id blockout \
  --fidelity 0.85 \
  --action continue \
  --summary "Blockout proportions acceptable. Hull and cabin placement correct." \
  --render-screenshot ./screenshots/spaceship-render.png \
  --comparison-image ./screenshots/spaceship-comparison.png \
  --ai-vision-score 0.85 \
  --feature-reviews-json ./reviews/blockout-features.json \
  --ai-vision-notes "Engine placement needs minor adjustment in structural pass." \
  --in-place
```

**Feature reviews JSON format:**

```json
{
  "features": [
    {
      "name": "hull_shape",
      "score": 0.90,
      "critical": true,
      "notes": "Silhouette matches reference"
    },
    {
      "name": "cabin_placement",
      "score": 0.88,
      "critical": true,
      "notes": "Position and proportions correct"
    },
    {
      "name": "engine_mounts",
      "score": 0.75,
      "critical": true,
      "notes": "Needs slight forward adjustment"
    }
  ]
}
```

**Review actions:**
- `continue` – Pass complete, unlock next pass
- `iterate` – Pass incomplete, iterate on current pass
- `block` – Critical failure, stop workflow
- `reference_needed` – Insufficient reference data

### 9. Sync Pass State

Update the spec with the review results and unlock the next pass if applicable:

```bash
python3 scripts/sculpt_pass_orchestrator.py sync object-sculpt-spec.json --in-place
```

**Pass unlocking logic:**
- Pass must have `action: continue` review
- Overall fidelity score must meet pass threshold
- All critical features must meet their individual thresholds
- Previous pass must be complete

### 10. Iterate Through Remaining Passes

Repeat steps 5-9 for each subsequent pass, progressively refining:

```bash
# Check next pass
python3 scripts/sculpt_pass_orchestrator.py status object-sculpt-spec.json

# Generate updated factory
python3 scripts/generate_threejs_factory.py object-sculpt-spec.json \
  --out src/createCargoSpaceship.ts

# Render, compare, review, sync
# ...repeat workflow
```

## PBR Material Extraction

Extract procedural PBR evidence from reference images:

```bash
python3 scripts/extract_reference_pbr.py ./reference/metal-panel.png \
  --out-dir ./generated/pbr/metal-panel \
  --material-id hull_metal \
  --target-threshold 0.7 \
  --report ./generated/pbr/metal-panel/report.json
```

**Generated maps:**
- `albedo.png` – Base color map
- `roughness.png` – Roughness estimate
- `height.png` – Height/displacement map
- `normal.png` – Normal map (derived from height)
- `ao.png` – Ambient occlusion map
- `palette.json` – Extracted color palette
- `report.json` – Confidence scores and metadata

**Use extracted maps in Three.js:**

```typescript
import * as THREE from 'three';

const textureLoader = new THREE.TextureLoader();

const material = new THREE.MeshStandardMaterial({
  map: textureLoader.load('./generated/pbr/metal-panel/albedo.png'),
  roughnessMap: textureLoader.load('./generated/pbr/metal-panel/roughness.png'),
  normalMap: textureLoader.load('./generated/pbr/metal-panel/normal.png'),
  aoMap: textureLoader.load('./generated/pbr/metal-panel/ao.png'),
  metalness: 0.8,
  roughness: 0.3
});
```

**Low-confidence handling:**

```bash
# Allow low-confidence extraction (< 0.7)
python3 scripts/extract_reference_pbr.py ./reference/unclear-surface.png \
  --out-dir ./generated/pbr/unclear-surface \
  --material-id surface \
  --target-threshold 0.7 \
  --allow-low-confidence
```

## Quality Gates and Critical Features

### Define Critical Features in Spec

Edit the spec to mark identity-defining features:

```json
{
  "quality_targets": {
    "passes": {
      "blockout": {
        "fidelity_threshold": 0.75,
        "critical_features": [
          {
            "name": "hull_shape",
            "threshold": 0.80,
            "description": "Primary fuselage silhouette and proportions"
          },
          {
            "name": "cabin_placement",
            "threshold": 0.75,
            "description": "Cabin position relative to hull centerline"
          },
          {
            "name": "engine_mounts",
            "threshold": 0.70,
            "description": "Engine attachment points and symmetry"
          }
        ]
      },
      "structural": {
        "fidelity_threshold": 0.80,
        "critical_features": [
          {
            "name": "wing_attachment",
            "threshold": 0.85,
            "description": "Wing root connection and dihedral angle"
          }
        ]
      }
    }
  }
}
```

### Pass/Fail Logic

A pass **fails** if:
- Overall fidelity score < pass threshold, OR
- Any critical feature score < its individual threshold

**Example:** Pass has overall score 0.82 (above 0.75 threshold) but `hull_shape` scores 0.72 (below 0.80 threshold) → **FAIL**

### Review with Feature Scores

```bash
# Review with critical feature failure
python3 scripts/append_sculpt_review.py object-sculpt-spec.json \
  --pass-id blockout \
  --fidelity 0.82 \
  --action iterate \
  --summary "Overall score acceptable but hull_shape below threshold." \
  --render-screenshot ./screenshots/render.png \
  --comparison-image ./screenshots/comparison.png \
  --ai-vision-score 0.82 \
  --feature-reviews-json ./reviews/features.json \
  --ai-vision-notes "Hull width-to-height ratio incorrect. Iterate on blockout." \
  --in-place
```

## Animation-Ready Hierarchy

### Pivot and Socket Definitions

In the sculpt spec, define transform anchors:

```json
{
  "components": [
    {
      "id": "turret",
      "name": "Turret",
      "parent": "hull",
      "geometry_type": "composite",
      "pivot": {
        "position": [0, 2.5, 0],
        "purpose": "rotation_anchor",
        "channels": ["rotation_y"]
      },
      "sockets": [
        {
          "id": "barrel_mount",
          "position": [0, 0.5, 1.2],
          "accepts": ["barrel"]
        }
      ]
    },
    {
      "id": "barrel",
      "name": "Barrel",
      "parent": "turret",
      "geometry_type": "cylinder",
      "pivot": {
        "position": [0, 0.5, 1.2],
        "purpose": "rotation_anchor",
        "channels": ["rotation_x"]
      }
    }
  ]
}
```

### Generated Animation-Ready Code

The factory generator creates proper hierarchy:

```typescript
export function createTurretTank(): THREE.Group {
  const root = new THREE.Group();
  root.name = 'TurretTank';

  // Hull (root component)
  const hull = new THREE.Mesh(
    new THREE.BoxGeometry(4, 1.5, 6),
    new THREE.MeshStandardMaterial({ color: 0x556b2f })
  );
  hull.name = 'hull';
  root.add(hull);

  // Turret (child of hull, pivot at [0, 2.5, 0])
  const turretGroup = new THREE.Group();
  turretGroup.name = 'turret';
  turretGroup.position.set(0, 2.5, 0);
  turretGroup.userData.pivot = { channels: ['rotation_y'] };
  
  const turretMesh = new THREE.Mesh(
    new THREE.CylinderGeometry(1, 1, 1, 16),
    new THREE.MeshStandardMaterial({ color: 0x556b2f })
  );
  turretGroup.add(turretMesh);
  root.add(turretGroup);

  // Barrel (child of turret, pivot at [0, 0.5, 1.2])
  const barrelGroup = new THREE.Group();
  barrelGroup.name = 'barrel';
  barrelGroup.position.set(0, 0.5, 1.2);
  barrelGroup.userData.pivot = { channels: ['rotation_x'] };
  
  const barrelMesh = new THREE.Mesh(
    new THREE.CylinderGeometry(0.2, 0.2, 3, 16),
    new THREE.MeshStandardMaterial({ color: 0x2f4f4f })
  );
  barrelMesh.rotation.x = Math.PI / 2;
  barrelGroup.add(barrelMesh);
  turretGroup.add(barrelGroup);

  return root;
}
```

### Animate the Hierarchy

```typescript
import { createTurretTank } from './createTurretTank';

const tank = createTurretTank();
scene.add(tank);

// Find animation anchors
const turret = tank.getObjectByName('turret') as THREE.Group;
const barrel = tank.getObjectByName('barrel') as THREE.Group;

// Animate turret rotation (Y-axis)
function animateTurret(time: number) {
  if (turret) {
    turret.rotation.y = Math.sin(time * 0.5) * Math.PI / 4;
  }
}

// Animate barrel elevation (X-axis)
function animateBarrel(time: number) {
  if (barrel) {
    barrel.rotation.x = Math.sin(time * 0.3) * Math.PI / 8;
  }
}

// Animation loop
function animate() {
  const time = performance.now() * 0.001;
  animateTurret(time);
  animateBarrel(time);
  renderer.render(scene, camera);
  requestAnimationFrame(animate);
}
animate();
```

## Destructible Objects

### Define Destruction Anchors

In the spec:

```json
{
  "components": [
    {
      "id": "window_glass",
      "name": "Window Glass",
      "parent": "cabin",
      "geometry_type": "plane",
      "destruction_anchor": {
        "detachable": true,
        "fracture_pattern": "radial_shatter",
        "debris_count": 8,
        "physics_enabled": true
      }
    }
  ]
}
```

### Generated Destructible Code

```typescript
export function createCabin(): THREE.Group {
  const cabin = new THREE.Group();
  cabin.name = 'cabin';

  // ... cabin geometry ...

  // Window glass (detachable)
  const windowGlass = new THREE.Mesh(
    new THREE.PlaneGeometry(2, 1.5),
    new THREE.MeshPhysicalMaterial({
      color: 0xaaccff,
      transparent: true,
      opacity: 0.3,
      transmission: 0.9
    })
  );
  windowGlass.name = 'window_glass';
  windowGlass.position.set(0, 1, 1.01);
  windowGlass.userData.destructionAnchor = {
    detachable: true,
    fracturePattern: 'radial_shatter',
    debrisCount: 8,
    physicsEnabled: true
  };
  cabin.add(windowGlass);

  return cabin;
}
```

### Implement Destruction

```typescript
function shatterWindow(windowMesh: THREE.Mesh) {
  const anchor = windowMesh.userData.destructionAnchor;
  if (!anchor || !anchor.detachable) return;

  // Remove original mesh
  const parent = windowMesh.parent;
  parent?.remove(windowMesh);

  // Create debris
  for (let i = 0; i < anchor.debrisCount; i++) {
    const debris = new THREE.Mesh(
      new THREE.PlaneGeometry(0.3, 0.3),
      windowMesh.material
    );
    debris.position.copy(windowMesh.position);
    debris.rotation.copy(windowMesh.rotation);
    
    // Add physics velocity
    const velocity = new THREE.Vector3(
      (Math.random() - 0.5) * 5,
      Math.random() * 3,
      (Math.random() - 0.5) * 5
    );
    debris.userData.velocity = velocity;
    debris.userData.angularVelocity = new THREE.Vector3(
      Math.random() * 10,
      Math.random() * 10,
      Math.random() * 10
    );
    
    parent?.add(debris);
    debrisObjects.push(debris);
  }
}
```

## Configuration

### Spec Configuration Options

Key spec sections to customize:

```json
{
  "object_name": "Cargo Spaceship",
  "reference_image": "./reference/spaceship.png",
  "complexity_tier": "moderate",
  "target_primitive_count": 150,
  "quality_targets": {
    "global_fidelity_threshold": 0.80,
    "require_lighting_response": true,
    "require_animation_readiness": true,
    "passes": {
      "blockout": {
        "fidelity_threshold": 0.75,
        "critical_features": [...]
      }
    }
  },
  "components": [...],
  "materials": [...],
  "lighting_response": {
    "primary_light_direction": [0.5, 1, 0.5],
    "ambient_intensity": 0.3,
    "shadow_behavior": "hard"
  }
}
```

### Factory Generation Options

```bash
# Generate with custom template
python3 scripts/generate_threejs_factory.py object-sculpt-spec.json \
  --out src/createModel.ts \
  --template ./templates/custom-factory.ts.j2

# Generate with optimization flags
python3 scripts/generate_threejs_factory.py object-sculpt-spec.json \
  --out src/createModel.ts \
  --optimize-geometry \
  --merge-materials

# Generate for specific pass
python3 scripts/generate_threejs_factory.py object-sculpt-spec.json \
  --out src/createModel.ts \
  --force-pass structural
```

## Common Patterns

### Pattern 1: Botanical Object (Tree)

```bash
# Probe tree reference
python3 scripts/probe_reference_image.py ./reference/oak-tree.png

# Create pre-spec for complex botanical object
python3 scripts/new_pre_spec_assessment.py "Ancient Oak Tree" \
  --image ./reference/oak-tree.png \
  --complexity complex \
  --out assessment.json

# Create spec with botanical components
python3 scripts/new_sculpt_spec.py "Ancient Oak Tree" \
  --image ./reference/oak-tree.png \
  --assessment assessment.json \
  --out tree-spec.json

# Define critical features: trunk fork, canopy mass, root flare, bark texture
# Edit tree-spec.json manually or via Codex

# Validate
python3 scripts/validate_sculpt_spec.py tree-spec.json --strict-quality

# Generate blockout
python3 scripts/generate_threejs_factory.py tree-spec.json \
  --out src/createOakTree.ts
```

**Botanical spec patterns:**
- Trunk as primary structural component with fork pivots
- Branches as recursive child components with socket hierarchy
- Canopy as instanced geometry or particle system
- Bark as procedural roughness + normal map material
- Roots as radial anchor components

### Pattern 2: Mechanical Object (Vehicle)

```bash
# Vehicle with wheels, chassis, detachable parts
python3 scripts/new_pre_spec_assessment.py "Combat Rover" \
  --image ./reference/rover.png \
  --complexity moderate \
  --out assessment.json

python3 scripts/new_sculpt_spec.py "Combat Rover" \
  --image ./reference/rover.png \
  --assessment assessment.json \
  --out rover-spec.json
```

**Mechanical spec patterns:**
- Chassis as root with wheel sockets at precise positions
- Wheels as detachable components with rotation pivots
- Turret/barrel with multi-axis rotation anchors
- Armor panels as breakable components with destruction anchors
- Engine glow as emissive material with animation channels

### Pattern 3: Architectural Object (Building)

```bash
# Building with modular components
python3 scripts/new_pre_spec_assessment.py "Medieval Tower" \
  --image ./reference/tower.png \
  --complexity moderate \
  --out assessment.json

python3 scripts/new_sculpt_spec.py "Medieval Tower" \
  --image ./reference/tower.png \
  --assessment assessment.json \
  --out tower-spec.json
```

**Architectural spec patterns:**
- Foundation as root component
- Floors as stacked child components with vertical sockets
- Windows as detachable components with glass shatter anchors
- Roof as separate component with tiling texture
- Stairs/ladders as interaction sockets

### Pattern 4: PBR Material Pipeline

```bash
# Extract PBR from multiple reference angles
python3 scripts/extract_reference_pbr.py ./reference/metal-hull-front.png \
  --out-dir ./pbr/metal-hull \
  --material-id hull_metal_front

python3 scripts/extract_reference_pbr.py ./reference/metal-hull-side.png \
  --out-dir ./pbr/metal-hull \
  --material-id hull_metal_side

# Composite maps in Three.js
# Use front albedo, side normal, blended roughness
```

**Multi-view PBR pattern:**
- Extract albedo from best-lit view
- Extract normal from highest detail view
- Extract roughness from most representative surface
- Blend or composite in Three.js material setup

## Troubleshooting

### Issue: Spec Validation Fails

**Error:** `Missing required field: quality_targets.passes.blockout.fidelity_threshold`

**Solution:**

```bash
# Use template to generate complete spec
python3 scripts/new_sculpt_spec.py "Object Name" \
  --image ./reference/object.png \
  --assessment assessment.json \
  --out spec.json

# Validate with detailed output
python3 scripts/validate_sculpt_spec.py spec.json --strict-quality --verbose
```

### Issue: Pass Won't Unlock

**Problem:** Pass review has `action: continue` but next pass remains locked.

**Diagnosis:**

```bash
# Check pass state
python3 scripts/sculpt_pass_orchestrator.py status spec.json

# Review last recorded review
python3 scripts/sculpt_pass_orchestrator.py reviews spec.json
```

**Common causes:**
- Critical feature score below threshold (check `--feature-reviews-json`)
- Overall fidelity below pass threshold
- Previous pass not marked complete
- Review action is `iterate` not `continue`

**Solution:**

```bash
# Ensure all critical features pass
# Re-review with corrected scores
python3 scripts/append_sculpt_review.py spec.json \
  --pass-id blockout \
  --fidelity 0.85 \
  --action continue \
  --feature-reviews-json ./reviews/corrected-features.json \
  --in-place

# Force sync
python3 scripts/sculpt_pass_orchestor.py sync spec.json --in-place
```

### Issue: Generated Factory Doesn't Match Spec

**Problem:** Factory code missing components or incorrect hierarchy.

**Diagnosis:**

```bash
# Check which pass is unlocked
python3 scripts/sculpt_pass_orchestrator.py status spec.json

# Verify spec component definitions
python3 scripts/validate_sculpt_spec.py spec.json --verbose
```

**Solution:**

```bash
# Regenerate factory for correct pass
python3 scripts/generate_threejs_factory.py spec.json \
  --out src/createModel.ts \
  --force-pass structural

# If spec is wrong, edit and regenerate
# Edit spec.json -> validate -> generate
```

### Issue: Low PBR Extraction Confidence

**Error:** `Confidence 0.52 below target threshold 0.70. Extraction aborted.`

**Cause:** Reference image has poor lighting, blur, or ambiguous surface properties.

**Solutions:**

```bash
# Option 1: Allow low confidence (not recommended for critical materials)
python3 scripts/extract_reference_pbr.py ./reference/unclear.png \
  --out-dir ./pbr/unclear \
  --material-id surface \
  --allow-low-confidence

# Option 2: Lower threshold (use with caution)
python3 scripts/extract_reference_pbr.py ./reference/unclear.png \
  --out-dir ./pbr/unclear \
  --material-id surface \
  --target-threshold 0.50

# Option 3: Provide better reference image
# Use well-lit, high-resolution, focused image
```

### Issue: AI Vision Review Scores Too Low

**Problem:** Comparison consistently scores below 0.70 even when model looks correct.

**Diagnosis:**
- Check comparison sheet alignment
- Verify reference and render are same camera angle
- Check lighting consistency

**Solutions:**

```bash
# Regenerate comparison with alignment hints
python3 scripts/make_visual_comparison_sheet.py \
  --reference ./reference/object.png \
  --render ./screenshots/render.png \
  --out ./screenshots/comparison.png \
  --match-brightness \
  --match-contrast

# Provide multiple camera angles for review
python3 scripts/make_visual_comparison_sheet.py \
  --reference ./reference/object-front.png \
  --render ./screenshots/render-front.png \
  --out ./screenshots/comparison-front.png
```

### Issue: Too Many Primitives (Performance)

**Problem:** Generated model exceeds target primitive count, poor browser performance.

**Solution:**

```bash
# Adjust target in pre-spec assessment
# Edit assessment.json: "target_primitive_count": 100

# Regenerate
