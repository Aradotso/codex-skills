---
name: codex-visio-paper-figure-skill
description: Convert paper figures and AI-generated diagrams into editable Microsoft Visio (.vsdx) files with native shapes, text, and connectors, then export to SVG/PDF/PNG/PPTX
triggers:
  - rebuild this figure as an editable Visio diagram
  - convert this paper diagram to Visio native shapes
  - create editable .vsdx from this reference image
  - turn this architecture diagram into Visio format
  - check if this .vsdx file just embedded the original image
  - export this Visio file to SVG, PDF, and PPTX
  - rebuild this multi-panel scientific figure in Visio
  - fix the layout and colors in this .vsdx to match the reference
---

# Codex Visio Paper Figure Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

The **Codex Visio Paper Figure Skill** transforms reference images (screenshots, AI-generated diagrams, paper figures) into **editable Microsoft Visio `.vsdx` files** composed of native shapes, text boxes, connectors, and groups. It's designed for academic paper workflows where you need to:

- Rebuild model architecture diagrams, flowcharts, and multi-panel scientific figures
- Replace embedded images with true vector graphics
- Maintain consistent styling across paper figures
- Export the same source `.vsdx` to PNG, SVG, PDF, and PPTX

**Core principle**: The final `.vsdx` must use Visio native primitives (rectangles, circles, lines, text), NOT just embed the original reference image as a background.

## Installation

Clone this skill repository into your Codex skills directory:

```powershell
# Windows
git clone https://github.com/pengjunchi0/codex-visio-paper-figure-skill.git "$env:USERPROFILE\.codex\skills\codex-visio-paper-figure-skill"
```

Restart Codex or start a new session to load the skill.

## Requirements

- **Windows** (Visio COM automation requires Windows)
- **Microsoft Visio** (for full drawing automation)
- **PowerShell** (for scripting)
- **Microsoft PowerPoint** (optional, for PPTX export)
- **Codex Desktop** or any Codex environment with local file access

## Key Scripts

### 1. `visio_rebuild_scaffold.ps1`

Main scaffolding script for rebuilding diagrams with native Visio shapes.

**Parameters:**
- `-VsdxPath` - Output `.vsdx` file path
- `-PageW`, `-PageH` - Visio page dimensions (inches)
- `-RefW`, `-RefH` - Reference image pixel dimensions
- `-PreviewPath` - Path to save PNG preview
- `-ExportFormats` - Comma-separated: `png`, `svg`, `pdf`, `pptx`
- `-OutputDir` - Directory for exported files

**Basic usage:**

```powershell
powershell -ExecutionPolicy Bypass -File scripts\visio_rebuild_scaffold.ps1 `
  -VsdxPath "C:\work\model.vsdx" `
  -PageW 16 `
  -PageH 9 `
  -RefW 1600 `
  -RefH 900 `
  -PreviewPath "C:\work\preview.png" `
  -ExportFormats svg,pdf,pptx `
  -OutputDir "C:\work\exports"
```

### 2. `visio_page_tools.ps1`

Utility for exporting existing `.vsdx` files and inspecting package structure.

**Parameters:**
- `-VsdxPath` - Input `.vsdx` file
- `-ExportFormats` - Formats to export
- `-OutputDir` - Export destination
- `-OutputBaseName` - Base name for exported files
- `-InspectPackage` - Check for embedded images (validation)

**Example:**

```powershell
powershell -ExecutionPolicy Bypass -File scripts\visio_page_tools.ps1 `
  -VsdxPath "C:\work\diagram.vsdx" `
  -ExportFormats svg,pdf,pptx `
  -OutputDir "C:\work\exports" `
  -InspectPackage
```

### 3. `visio_export_formats.ps1`

Reusable export functions (PNG, SVG, PDF, PPTX). Sourced by other scripts.

## Core Drawing Functions

The scaffold provides coordinate mapping helpers to prevent panel overlap in complex multi-panel figures:

### Global Coordinate Mapping

```powershell
# Convert reference image pixel coordinates to Visio page inches
$x_inch = Ref2Page $x_pixel "x"
$y_inch = Ref2Page $y_pixel "y"
```

### Panel-Local Coordinates (v1.1.1+)

For complex diagrams with multiple panels, define panel boundaries and use relative coordinates:

```powershell
# Define panel A boundaries (in reference pixel coordinates)
$panelA = @{ X0=50; Y0=50; X1=750; Y1=450 }

# Draw rectangle at 10% from panel left, 20% from top, 30% wide, 25% tall
RectRel -Panel $panelA -RelX 0.1 -RelY 0.2 -RelW 0.3 -RelH 0.25 `
  -Fill "rgb(200,220,240)" -Line "rgb(80,100,120)" -LineW 1.5 `
  -Label "Module A"

# Draw text at relative position within panel
TextRel -Panel $panelA -RelX 0.5 -RelY 0.1 `
  -Text "Panel A Title" -FontSize 16 -Bold

# Draw oval
OvalRel -Panel $panelA -RelCX 0.5 -RelCY 0.8 -RelW 0.2 -RelH 0.1 `
  -Fill "rgb(255,200,200)"

# Draw line within panel
LineRel -Panel $panelA -RelX1 0.3 -RelY1 0.5 -RelX2 0.7 -RelY2 0.5 `
  -Arrow "End" -LineW 2
```

### Validation Helpers

```powershell
# Assert a bounding box stays within panel
Assert-RelBox -Panel $panelA -RelX 0.1 -RelY 0.2 -RelW 0.3 -RelH 0.25 `
  -ElementName "Module A"

# Assert a point stays within panel
Assert-RelPoint -Panel $panelA -RelX 0.5 -RelY 0.9 -PointName "Label"
```

These helpers throw errors if elements exceed panel boundaries, preventing overlap and misalignment.

## Real-World Example: Multi-Panel Architecture Diagram

Suppose you have a 1600×900px reference image with three panels:

```powershell
# scripts/rebuild_architecture.ps1
param(
  [string]$VsdxPath = "C:\papers\architecture.vsdx",
  [string]$OutputDir = "C:\papers\exports"
)

# Dimensions
$pageW = 16
$pageH = 9
$refW = 1600
$refH = 900

# Define panels (in reference pixel coordinates)
$panelA = @{ X0=50;   Y0=50;   X1=750;  Y1=450 }  # Input Processing
$panelB = @{ X0=800;  Y0=50;   X1=1550; Y1=450 }  # Model Architecture
$panelC = @{ X0=50;   Y0=500;  X1=1550; Y1=850 }  # Output & Metrics

# Start Visio
$visio = New-Object -ComObject Visio.Application
$visio.Visible = $true
$docs = $visio.Documents
$doc = $docs.Add("")
$page = $doc.Pages.Item(1)
$page.PageSheet.CellsSRC(1,1,0).FormulaU = "$pageW in"
$page.PageSheet.CellsSRC(1,1,1).FormulaU = "$pageH in"

# Helper functions
function Ref2Page($val, $dim) {
  if ($dim -eq "x") { return $val / $refW * $pageW }
  else { return $pageH - ($val / $refH * $pageH) }
}

function RectRel {
  param($Panel, $RelX, $RelY, $RelW, $RelH, $Fill, $Line, $LineW, $Label)
  
  Assert-RelBox -Panel $Panel -RelX $RelX -RelY $RelY -RelW $RelW -RelH $RelH -ElementName $Label
  
  $px0 = $Panel.X0 + $RelX * ($Panel.X1 - $Panel.X0)
  $py0 = $Panel.Y0 + $RelY * ($Panel.Y1 - $Panel.Y0)
  $pw = $RelW * ($Panel.X1 - $Panel.X0)
  $ph = $RelH * ($Panel.Y1 - $Panel.Y0)
  
  $x = Ref2Page $px0 "x"
  $y = Ref2Page $py0 "y"
  $w = $pw / $refW * $pageW
  $h = $ph / $refH * $pageH
  
  $shp = $page.DrawRectangle($x, $y - $h, $x + $w, $y)
  $shp.CellsSRC(1,3,0).FormulaU = """$Fill"""
  $shp.CellsSRC(1,2,0).FormulaU = """$Line"""
  $shp.CellsSRC(1,2,1).FormulaU = "$LineW pt"
  if ($Label) { $shp.Text = $Label }
}

function Assert-RelBox {
  param($Panel, $RelX, $RelY, $RelW, $RelH, $ElementName)
  if ($RelX -lt 0 -or $RelY -lt 0 -or ($RelX + $RelW) -gt 1 -or ($RelY + $RelH) -gt 1) {
    throw "Element '$ElementName' exceeds panel bounds"
  }
}

# Panel A: Input Processing
RectRel -Panel $panelA -RelX 0.1 -RelY 0.1 -RelW 0.35 -RelH 0.2 `
  -Fill "rgb(220,240,255)" -Line "rgb(80,120,160)" -LineW 1.5 `
  -Label "Image Input"

RectRel -Panel $panelA -RelX 0.55 -RelY 0.1 -RelW 0.35 -RelH 0.2 `
  -Fill "rgb(220,255,220)" -Line "rgb(80,160,80)" -LineW 1.5 `
  -Label "Preprocessor"

# Panel B: Model Architecture
RectRel -Panel $panelB -RelX 0.1 -RelY 0.15 -RelW 0.25 -RelH 0.3 `
  -Fill "rgb(255,240,220)" -Line "rgb(200,120,80)" -LineW 1.5 `
  -Label "Encoder"

RectRel -Panel $panelB -RelX 0.4 -RelY 0.15 -RelW 0.25 -RelH 0.3 `
  -Fill "rgb(255,220,240)" -Line "rgb(200,80,120)" -LineW 1.5 `
  -Label "Transformer"

RectRel -Panel $panelB -RelX 0.7 -RelY 0.15 -RelW 0.25 -RelH 0.3 `
  -Fill "rgb(240,220,255)" -Line "rgb(120,80,200)" -LineW 1.5 `
  -Label "Decoder"

# Panel C: Output
RectRel -Panel $panelC -RelX 0.3 -RelY 0.3 -RelW 0.4 -RelH 0.4 `
  -Fill "rgb(255,255,220)" -Line "rgb(160,160,80)" -LineW 1.5 `
  -Label "Output Layer"

# Save
$doc.SaveAs($VsdxPath)
Write-Host "Saved: $VsdxPath"

# Export formats
$formats = @("png", "svg", "pdf", "pptx")
foreach ($fmt in $formats) {
  $outPath = Join-Path $OutputDir "architecture.$fmt"
  # Call export function (from visio_export_formats.ps1)
  # Implementation details in actual script
  Write-Host "Exported: $outPath"
}

$visio.Quit()
```

## Common Patterns

### 1. Rebuild from Reference Image

```powershell
# User provides reference.png at 1920x1080
powershell -ExecutionPolicy Bypass -File scripts\visio_rebuild_scaffold.ps1 `
  -VsdxPath "C:\work\figure1.vsdx" `
  -PageW 16 `
  -PageH 9 `
  -RefW 1920 `
  -RefH 1080 `
  -PreviewPath "C:\work\figure1_preview.png" `
  -ExportFormats svg,pdf `
  -OutputDir "C:\work\exports"
```

Inside the scaffold, customize the drawing logic to match the reference layout.

### 2. Update Existing .vsdx Styling

Open existing file, modify colors/fonts, re-export:

```powershell
$visio = New-Object -ComObject Visio.Application
$doc = $visio.Documents.Open("C:\work\existing.vsdx")
$page = $doc.Pages.Item(1)

# Change all rectangles to new color
foreach ($shp in $page.Shapes) {
  if ($shp.CellExists("FillForegnd", 0)) {
    $shp.CellsSRC(1,3,0).FormulaU = """rgb(200,220,240)"""
  }
}

$doc.Save()
$visio.Quit()
```

### 3. Check for Embedded Images

```powershell
powershell -ExecutionPolicy Bypass -File scripts\visio_page_tools.ps1 `
  -VsdxPath "C:\work\diagram.vsdx" `
  -InspectPackage
```

Looks for large PNG/JPG files in `/visio/media/` inside the `.vsdx` ZIP. Warns if the diagram is just an embedded image.

## Acceptance Criteria

A correctly rebuilt `.vsdx` should:

- ✅ Match the reference layout
- ✅ Use native Visio shapes (rectangles, circles, lines, text)
- ✅ Have editable text and shapes
- ✅ NOT embed the entire reference image as the final content
- ✅ Use consistent colors, fonts, and line weights
- ✅ For multi-panel figures: no panel overlap, no elements crossing boundaries
- ✅ Export cleanly to SVG, PDF, PNG, PPTX from the same source `.vsdx`

## Troubleshooting

### "Visio COM object not found"

Install Microsoft Visio. The COM automation API requires a licensed Visio installation on Windows.

### Exported files are empty

Check that the `.vsdx` saved successfully before export. Verify the page has visible shapes:

```powershell
$page.Shapes.Count  # Should be > 0
```

### Panels overlap in multi-panel figures

Use panel-local coordinates with `Assert-RelBox` and `Assert-RelPoint`:

```powershell
Assert-RelBox -Panel $panelA -RelX 0.1 -RelY 0.2 -RelW 0.8 -RelH 0.6 `
  -ElementName "BigModule"
```

This throws an error if the box exceeds panel boundaries.

### Text is cut off

Increase relative width/height, or use multi-line text:

```powershell
$shp.Text = "Line 1`nLine 2`nLine 3"
```

### Colors don't match reference

Use a color picker on the reference image and convert to RGB:

```powershell
$shp.CellsSRC(1,3,0).FormulaU = """rgb(123,210,98)"""
```

## Export Format Details

| Format | Method | Notes |
|--------|--------|-------|
| **PNG** | `$page.Export($path)` | Raster, good for previews |
| **SVG** | `FixedFormat = 4` | Vector, editable in Illustrator/Inkscape |
| **PDF** | `FixedFormat = 2` | Vector, for paper submission |
| **PPTX** | PowerPoint COM | Creates slide with embedded SVG |

PPTX export example:

```powershell
$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = $true
$pres = $ppt.Presentations.Add()
$slide = $pres.Slides.Add(1, 12)  # 12 = ppLayoutBlank

# Export Visio page to SVG first
$svgPath = "C:\temp\diagram.svg"
$page.Export($svgPath)

# Insert SVG into slide
$slide.Shapes.AddPicture($svgPath, $false, $true, 0, 0, 720, 405)
$pres.SaveAs("C:\work\diagram.pptx")
$ppt.Quit()
```

## Version History

- **v1.1.1** - Panel calibration, local coordinates, anti-overlap validation
- **v1.1** - Multi-format export (PNG, SVG, PDF, PPTX)
- **v1.0** - Initial release with Visio COM scaffolding

## References

- `SKILL.md` - Main workflow and rules
- `references/rebuild-guidelines.md` - Detailed drawing strategies for complex scientific figures
- `scripts/visio_export_formats.ps1` - Export function library
- `scripts/visio_page_tools.ps1` - Inspection and export utilities
- `scripts/visio_rebuild_scaffold.ps1` - Drawing scaffolding with coordinate helpers

---

**When to use this skill:**

- User wants to convert a paper diagram to editable Visio
- User needs SVG/PDF/PPTX exports from a single source
- User wants to verify a `.vsdx` isn't just an embedded image
- User needs consistent styling across multiple paper figures

**When NOT to use this skill:**

- User just wants to embed an image in a slide deck (use PowerPoint directly)
- User needs pure raster image editing (use Photoshop/GIMP)
- User doesn't need Visio-native editability
