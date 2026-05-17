---
name: academic-research-skills-codex
description: AI-assisted academic research workflows for literature review, paper writing, peer review, and research pipelines
triggers:
  - help me write an academic paper
  - conduct a literature review
  - review this research manuscript
  - plan a systematic review
  - generate research paper outline
  - format academic citations
  - run academic research pipeline
  - peer review simulation
---

# Academic Research Skills for Codex

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

This skill provides a comprehensive suite of AI-assisted academic research workflows including deep research, paper writing, peer review, and end-to-end research pipelines. Originally designed for Claude Code, this Codex-native package routes requests to specialized research agents based on user intent.

## What It Does

Academic Research Skills (ARS) for Codex provides five core workflows:

1. **Deep Research** - Literature reviews, systematic reviews, research question refinement, fact-checking
2. **Academic Paper** - Outlining, drafting, citation formatting, revision, AI disclosure
3. **Academic Paper Reviewer** - Manuscript review, simulated peer review, editorial decisions
4. **Academic Pipeline** - End-to-end research-to-publication workflow with integrity gates
5. **Experiment Agent** - Code experiment planning, study protocols, reproducibility validation

## Installation

Install using the Codex skill installer with git method:

```bash
python "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo Imbad0202/academic-research-skills-codex \
  --ref main \
  --path skills/academic-research-suite \
  --method git
```

### Update Existing Installation

```bash
rm -rf "$HOME/.codex/skills/academic-research-suite"
python "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo Imbad0202/academic-research-skills-codex \
  --ref main \
  --path skills/academic-research-suite \
  --method git
```

After installation, open a new Codex conversation to activate the skill.

### Verify Installation

```text
/skills
```

You should see one entry: `academic-research-suite`. You should NOT see separate entries for `academic-paper`, `deep-research`, etc.

## Core Usage Patterns

### Basic Invocation

Use `$academic-research-suite` followed by your research task:

```text
Use $academic-research-suite to help me plan a systematic literature review on
AI adoption in higher education quality assurance.
```

The Codex adapter automatically routes to the appropriate workflow based on your request.

### Workflow Selection

| Workflow | When to Use | Example Trigger |
|----------|-------------|-----------------|
| `deep-research` | Need research question refinement, literature review, fact-checking | "conduct a systematic review on..." |
| `academic-paper` | Need paper outline, drafting, citations, revision | "write a research paper about..." |
| `academic-paper-reviewer` | Need manuscript review, peer review simulation | "review this research manuscript..." |
| `academic-pipeline` | Need full research-to-publication workflow | "run end-to-end pipeline from topic to paper" |
| `experiment-agent` | Need code experiment design, study protocols | "plan a reproducible code experiment..." |

### Structured Request Pattern

For best results, provide goal, current state, and constraints:

```text
Use $academic-research-suite.

Goal: write a journal article on AI in higher education QA
Current materials: literature matrix and rough findings, no outline yet
Output needed: paper architecture and evidence checklist
Constraints: English, APA 7, policy audience
```

## Command Aliases

Codex emulates Claude Code `/ars-*` commands as aliases:

| Alias | Workflow | Purpose |
|-------|----------|---------|
| `ars-plan` | academic-paper | Create paper plan/structure |
| `ars-outline` | academic-paper | Generate outline only |
| `ars-abstract` | academic-paper | Draft abstract |
| `ars-lit-review` | academic-paper | Build literature review |
| `ars-citation-check` | academic-paper | Verify citations |
| `ars-disclosure` | academic-paper | Generate AI disclosure statement |
| `ars-format-convert` | academic-paper | Convert between formats |
| `ars-revision-coach` | academic-paper | Get revision guidance |
| `ars-revision` | academic-paper | Execute revisions |
| `ars-full` | academic-pipeline | Run full pipeline |

### Using Aliases

Either prefix style works:

```text
Use $academic-research-suite: ars-plan my paper on AI governance
```

Or if your client supports it:

```text
/ars-plan my paper on AI governance
```

## Workflow Examples

### Deep Research: Socratic Question Refinement

When you have a broad topic but no clear research question:

```text
Use $academic-research-suite.

I want to write about AI adoption in higher education quality assurance.
I don't have a clear research question yet.
Use Socratic dialogue to help me narrow the question first.
```

Expected: ARS asks narrowing questions before producing an outline.

### Academic Paper: From Notes to Draft

```text
Use $academic-research-suite.

Task: Turn these research notes into an IMRaD paper.
Materials: [attach notes.md, data_summary.csv]
Target: 6000-8000 words, APA 7, submit to Higher Education Research
Output: Full outline with section word counts, then draft intro
```

### Paper Review: Simulated Peer Review

```text
Use $academic-research-suite to review this manuscript.

Mode: full review
Focus: methodology, contribution, citation integrity, desk-reject risks
Output: reviewer reports + editorial decision letter

[attach manuscript.pdf or manuscript.md]
```

### Academic Pipeline: Staged Execution

For checkpoint-based workflow:

```text
Use $academic-research-suite to start an academic-pipeline run.

Begin with Stage 0 intake and stop after producing the pipeline dashboard.
Wait for my approval before Stage 1.
```

### Experiment Agent: Reproducible Study Design

```text
Use $academic-research-suite experiment-agent.

Plan a code experiment comparing three ML models on education dataset.
Requirements: reproducible, statistical rigor, version control, artifact storage
Output: experiment protocol + reproducibility checklist
```

## Configuration

### Environment Variables

For cross-model verification (optional):

```bash
export ARS_CROSS_MODEL=claude-opus-4.7
export ANTHROPIC_API_KEY=your_api_key_here
```

Without these, ARS runs entirely within Codex/OpenAI. Cross-model review uses Anthropic API when explicitly requested.

### Material Passport

ARS tracks research artifacts through "Material Passports" - metadata files that follow:

```json
{
  "artifact_id": "paper_v1_outline",
  "created": "2026-05-17T10:30:00Z",
  "workflow": "academic-paper",
  "stage": "outline",
  "integrity_checks": ["citation_format", "structure"],
  "sources": ["source1.pdf", "source2.pdf"],
  "status": "approved"
}
```

Reset Material Passport by starting a new Codex conversation.

## Working with Citations

### Citation Check

```text
Use $academic-research-suite: ars-citation-check

[paste paper text with citations]

Verify all citations are formatted correctly in APA 7.
Flag any unverifiable sources.
```

Expected output:
- Citation format compliance report
- Unverifiable citations flagged
- Suggested corrections

### Literature Review Mode

```text
Use $academic-research-suite: ars-lit-review

Topic: AI ethics in higher education
Scope: 2020-2026, peer-reviewed only
Output: thematic synthesis with citation matrix
```

## Paper Formatting and Conversion

### Format Conversion

```text
Use $academic-research-suite: ars-format-convert

Input: [attach paper.md]
From: Markdown
To: LaTeX (IEEE conference template)
Preserve: citations, figures, tables
```

### AI Disclosure Statement

```text
Use $academic-research-suite: ars-disclosure

Paper stage: final draft before submission
AI tools used: Codex for literature search, outline generation, citation formatting
Human contribution: research design, analysis, interpretation, revision
Output: journal-ready disclosure statement
```

## Revision Workflow

### Revision Coach

For guidance without executing changes:

```text
Use $academic-research-suite: ars-revision-coach

[attach draft.md and reviewer_comments.txt]

Analyze reviewer feedback and suggest revision strategy.
Prioritize major vs minor revisions.
Do not rewrite yet - provide plan only.
```

### Execute Revisions

```text
Use $academic-research-suite: ars-revision

[attach draft.md and reviewer_comments.txt]

Execute revisions based on Reviewer 2 methodology concerns.
Track changes: show original -> revised for each section.
Update Material Passport with revision metadata.
```

## Troubleshooting

### Skill Not Found

If `/skills` doesn't show `academic-research-suite`:

1. Verify installation path: `ls -la "$HOME/.codex/skills/academic-research-suite"`
2. Reinstall using update command above
3. Open a **new** Codex conversation (old sessions cache skills)

### Multiple ARS Skills Showing

If you see `academic-paper`, `deep-research`, etc. as separate skills:

```bash
# Remove all ARS skills
rm -rf "$HOME/.codex/skills/academic-"*
rm -rf "$HOME/.codex/skills/deep-research"
rm -rf "$HOME/.codex/skills/experiment-agent"

# Reinstall single suite
python "$HOME/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo Imbad0202/academic-research-skills-codex \
  --ref main \
  --path skills/academic-research-suite \
  --method git
```

### Wrong Workflow Selected

If ARS routes to the wrong workflow, be more explicit:

```text
Use $academic-research-suite deep-research workflow in socratic mode.

[your request]
```

Or use specific alias:

```text
Use $academic-research-suite: ars-outline

[your request]
```

### Citation Verification Fails

When citations cannot be verified:

- ARS should mark them as **unverified** rather than inventing support
- If verification is critical, provide DOIs or URLs for sources
- Use `ars-citation-check` mode with source files attached

### Codex Warnings

These warnings are non-blocking:

- `[features].codex_hooks is deprecated` - update Codex config when convenient
- `hooks need review before they can run` - ARS Codex doesn't require hooks for normal use

## Advanced Patterns

### Staged Pipeline with Checkpoints

```text
Use $academic-research-suite academic-pipeline workflow.

Stage 0: Intake and dashboard
STOP and show dashboard for approval

[After approval]

Stage 1: Research question refinement via Socratic dialogue
STOP and show refined question

[Continue stage by stage]
```

### Parallel Literature Search

```text
Use $academic-research-suite deep-research workflow.

Search strategy: parallel tracks
Track 1: Scopus, Web of Science - quantitative studies
Track 2: Google Scholar - grey literature, policy docs
Track 3: Specialized databases - ERIC, ProQuest Education

Synthesize results into single literature matrix.
```

### Multi-Pass Review

```text
Use $academic-research-suite academic-paper-reviewer workflow.

Pass 1: Structure and contribution (desk-reject check)
[Wait for my review]

Pass 2: Methodology rigor
[Wait for my review]

Pass 3: Citation integrity and ethics
[Final decision]
```

## Integration with Research Tools

### With Reference Managers

```text
Use $academic-research-suite: ars-citation-check

Citation library: Zotero export attached (bibtex format)
Paper: [attach draft.md]

Cross-check all in-text citations against Zotero library.
Flag missing entries and formatting errors.
```

### With Data Analysis Code

```text
Use $academic-research-suite experiment-agent workflow.

Existing analysis: [attach analysis.py, results.csv]
Task: Create reproducible experiment protocol around this analysis
Output: protocol.md, requirements.txt, reproduction checklist
```

### With Institutional Templates

```text
Use $academic-research-suite: ars-format-convert

Input: [attach paper.md]
Template: University PhD thesis LaTeX template [attach template.tex]
Preserve: custom environments for theorems, university citation style
```

## CLI Smoke Test

Test routing without full execution:

```bash
codex exec --ephemeral --sandbox read-only \
  -C /path/to/academic-research-skills-codex \
  'Use $academic-research-suite. Router smoke test only. Classify workflow and mode for: I want to write a paper on AI adoption but do not have a research question yet.'
```

Expected: Route to `deep-research` `socratic` mode.

## Key Differences from Claude Code Version

This Codex package differs from the original Claude Code ARS:

| Feature | Claude Code | Codex Package |
|---------|-------------|---------------|
| Installation | Plugin marketplace | Git-based skill installer |
| Commands | Native `/ars-*` slash commands | Emulated aliases via router |
| Agent teams | Automatic background agents | Inline unless explicitly delegated |
| Hooks | SessionStart, SubagentStop | Vendored for traceability only |
| Cross-model review | GPT/Gemini secondary dispatch | Anthropic Claude API (explicit config) |
| Updates | Marketplace auto-update | Manual reinstall |

## Version Information

- **Codex Package Version**: v0.1.6
- **Vendored ARS Commit**: `1d0c8625207c9cd8fc46132b1ef930f2cc012236`
- **License**: CC BY-NC 4.0 (non-commercial use)
- **Original Repository**: https://github.com/Imbad0202/academic-research-skills

## Additional Resources

- **Codex Setup Guide**: `skills/academic-research-suite/ars/docs/SETUP.md`
- **Architecture Details**: `skills/academic-research-suite/ars/docs/ARCHITECTURE.md`
- **Claude Code Version**: https://github.com/Imbad0202/academic-research-skills

For issues specific to the Codex packaging, open an issue at the Codex package repository. For ARS workflow issues, consult the original Claude Code repository.
