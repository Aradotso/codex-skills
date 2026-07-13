---
name: codex-first-customer-finder-skill
description: Find evidence-backed potential first customers from public signals for startups using Codex AI
triggers:
  - find first customers for my startup
  - research potential early adopters
  - discover design partners from public signals
  - find b2b prospects with timing signals
  - generate customer discovery report
  - identify early customers with evidence
  - search for startup prospects with demand signals
  - create first customer shortlist
---

# Codex First Customer Finder Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

A Codex skill that analyzes startup URLs or product ideas to find qualified potential first customers using recent public pain, demand, and timing signals. It creates evidence-backed prospect shortlists with source links, fit scores, and personalized outreach openers without automatically sending any messages.

## What It Does

- Analyzes startup URLs, repositories, or product descriptions to define ideal customer profiles
- Searches public sources for explicit demand, pain, workaround, switching, and timing signals
- Qualifies prospects with evidence-based scores linking to original public sources
- Drafts respectful, source-based outreach openers (manual sending only)
- Generates responsive standalone HTML reports with prospect rankings
- Avoids private contact enrichment and sensitive personal data collection

## Installation

The skill installs into `~/.codex/skills/first-customer-finder`:

```bash
# Quick installation via npx
npx --yes codex-first-customer-finder-skill@latest
```

After installation, restart your Codex agent to load the skill.

### Manual Installation

```bash
git clone https://github.com/Kappaemme-git/codex-first-customer-finder-skill.git
mkdir -p ~/.codex/skills
cp -R codex-first-customer-finder-skill/first-customer-finder ~/.codex/skills/first-customer-finder
```

## Usage Patterns

### Basic Customer Discovery

Find potential first customers for a startup:

```text
Use $first-customer-finder to find ten evidence-backed potential first customers for https://example.com and create the final HTML report.
```

### Design Partners Mode

Prioritize prospects likely to provide product feedback:

```text
Use $first-customer-finder in design-partners mode for this startup: https://example.com. Prioritize people publicly describing the problem and likely to give product feedback.
```

### B2B Research

Find business prospects with public triggers:

```text
Use $first-customer-finder in b2b mode for https://example.com. Find public business triggers, qualify the relevant companies, and draft one opener per prospect without sending anything.
```

### Community Signal Discovery

Focus on explicit requests and public discussions:

```text
Use $first-customer-finder in community mode for [product description]. Find people actively discussing this problem in public forums and communities.
```

### Quick Research

Generate a shortlist of high-confidence prospects:

```text
Use $first-customer-finder in quick mode for https://example.com to find five strong prospects with the best timing signals.
```

### Deep Analysis

Comprehensive research with pattern analysis:

```text
Use $first-customer-finder in deep mode for https://example.com. Find up to twenty prospects and analyze repeated pain patterns across signals.
```

## Modes

| Mode | Description | Prospect Count |
|------|-------------|----------------|
| `quick` | High-confidence prospects only | Up to 5 |
| `standard` | Balanced research across source types | Up to 10 |
| `deep` | Comprehensive with pattern analysis | Up to 20 |
| `design-partners` | Feedback-oriented early adopters | Up to 10 |
| `b2b` | Companies with business triggers | Up to 10 |
| `community` | Public discussion signals | Up to 10 |

## Report Output

The generated HTML report includes:

1. **Early-customer verdict** - Overall market signal assessment
2. **Primary ICP and disqualifiers** - Ideal customer profile definition
3. **Highest-confidence prospect** - Top-ranked opportunity with evidence
4. **Evidence-backed prospect shortlist** - Complete list with source links
5. **Fit and timing scores** - Quantified prospect qualification
6. **Source links and signal dates** - Original public signal references
7. **Personalized outreach openers** - Draft messages (manual sending)
8. **Repeated pain patterns** - Common themes across signals
9. **Seven-day manual outreach plan** - Suggested sequencing
10. **Research limitations** - Methodology transparency

## Configuration

The skill uses environment variables for API access (if needed for data sources):

```bash
# Example environment configuration (adjust based on actual implementation)
export CODEX_SKILL_DATA_SOURCES="public"
export CODEX_SKILL_MAX_PROSPECTS=10
export CODEX_SKILL_OUTPUT_DIR="./customer-reports"
```

## Invocation Examples

### From Product Description

```text
Use $first-customer-finder for a developer tool that helps teams migrate from MongoDB to PostgreSQL. Focus on recent migration pain signals and active database switchers.
```

### From Repository

```text
Use $first-customer-finder to analyze https://github.com/username/project and find ten potential first customers based on the README and documentation.
```

### With Specific Criteria

```text
Use $first-customer-finder in standard mode for https://example.com. Focus on prospects who have publicly mentioned the problem in the last 30 days and show urgency signals.
```

## Understanding Prospect Scores

- **Fit Score**: How well the prospect matches the ICP (based on role, context, problem description)
- **Timing Score**: Recency and urgency of the public signal
- **Evidence Quality**: Clarity and specificity of the pain point or demand signal

High scores (8-10) indicate strong alignment between the prospect's public signal and your product's value proposition.

## Best Practices

### 1. Start with the Startup Context

Provide as much context as possible:

```text
Use $first-customer-finder for https://example.com (a scheduling tool for freelance consultants). Look for signals around calendar chaos, double-booking, and manual scheduling pain.
```

### 2. Review Evidence Links

Always verify the source links in the report before reaching out. The skill provides hypotheses, not guarantees.

### 3. Customize Outreach Openers

The generated openers are templates. Personalize them further based on:
- Additional profile research
- Specific signal context
- Your brand voice

### 4. Respect Privacy and Intent

- Signals are public, but respect boundaries
- Only reach out if the signal indicates openness to solutions
- Never automate bulk outreach

### 5. Track Follow-up Manually

The skill generates a 7-day plan but doesn't send messages. Use your CRM or manual tracking for:
- Initial outreach status
- Response tracking
- Follow-up scheduling

## Troubleshooting

### Skill Not Found

If Codex doesn't recognize `$first-customer-finder`:

```bash
# Verify installation directory
ls ~/.codex/skills/first-customer-finder

# Reinstall if missing
npx --yes codex-first-customer-finder-skill@latest

# Restart Codex agent
```

### Low-Quality Prospects

If prospects seem irrelevant:

```text
Use $first-customer-finder for https://example.com. Define the ICP more narrowly: exclude hobbyists, focus on B2B SaaS companies with 10-50 employees experiencing [specific pain point].
```

### Insufficient Signal Volume

Try different modes or sources:

```text
Use $first-customer-finder in deep mode for https://example.com. Expand sources to include Reddit, niche forums, and GitHub discussions beyond Twitter/LinkedIn.
```

### Report Not Generating

Ensure the skill completes research before requesting the report:

```text
Use $first-customer-finder for https://example.com in standard mode. After completing prospect research, generate and save the HTML report to ./reports/customers.html
```

## Integration Workflows

### With CRM Export

```text
Use $first-customer-finder for https://example.com. After generating the report, extract prospect data (name, signal, source URL, score) into a CSV for CRM import.
```

### With Content Calendar

```text
Use $first-customer-finder in community mode for https://example.com. Identify the top three pain patterns and suggest five content ideas addressing each pattern for inbound customer acquisition.
```

### With Product Roadmap

```text
Use $first-customer-finder in design-partners mode for https://example.com. Find prospects who mention feature gaps or workarounds that could inform our Q2 roadmap priorities.
```

## Limitations

- **Public signals only**: No private data scraping or contact enrichment
- **Hypotheses, not guarantees**: Prospects are qualified leads, not confirmed buyers
- **Manual outreach required**: Skill never sends messages automatically
- **Source availability**: Results depend on public signal volume and recency
- **Language**: Primary support for English-language signals

## Example Complete Workflow

```text
1. Use $first-customer-finder in standard mode for https://myproduct.com (a Git-based documentation tool for engineering teams)

2. After research completes, review the HTML report focusing on:
   - Top 3 prospects with timing scores above 8
   - Common pain patterns in the "Repeated Patterns" section
   - Source links for signal verification

3. Customize the suggested outreach openers for the top 3 prospects, adding:
   - Reference to their specific project or company
   - One relevant product feature addressing their exact pain point
   - Low-pressure ask (demo vs. feedback vs. conversation)

4. Manually send outreach via LinkedIn/email with 2-day spacing

5. Use the 7-day plan to schedule follow-ups in calendar

6. Track responses and update ICP assumptions based on feedback
```

## License

MIT License - See repository for full details.
