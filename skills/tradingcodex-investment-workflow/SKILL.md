---
name: tradingcodex-investment-workflow
description: Install and use TradingCodex to build Codex-native investment research workflows with fixed-role agents, order approval gates, and local Django service plane
triggers:
  - set up TradingCodex for investment research
  - attach TradingCodex to this workspace
  - create a trading workflow with specialist agents
  - configure TradingCodex broker integration
  - review order tickets and portfolio in TradingCodex
  - run TradingCodex decision workflow
  - check TradingCodex safety and approval gates
  - troubleshoot TradingCodex MCP connection
---

# TradingCodex Investment Workflow

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

TradingCodex is a local-first Python/Django investment workflow harness that gives Codex a durable operating system for research, portfolio review, order-ticket checks, approvals, and service-gated execution. It generates a Codex workspace with a `head-manager` agent, nine fixed specialist subagents (fundamental, technical, news, macro, instrument, valuation, portfolio, risk, execution), role prompts, MCP config, and a local web dashboard. Research stays in workspace markdown files; all actions flow through policy, approval, and audit gates.

## Installation

### Attach to Current Workspace (Recommended)

From the **empty** workspace where you want Codex agents to work:

```bash
uvx --refresh --from tradingcodex tcx attach . && ./tcx doctor
```

Then **fully quit and restart Codex**, open the generated workspace, and start a new thread so project MCP config, prompts, skills, and hooks are loaded.

### Install CLI for Repeated Use

```bash
uv tool install tradingcodex
uv tool update-shell
cd /path/to/target-workspace
tcx attach .
./tcx doctor
```

### Install from GitHub Main

```bash
uvx --refresh --from "tradingcodex @ git+https://github.com/monarchjuno/tradingcodex.git@main" tcx attach . && ./tcx doctor
```

### Verify Installation

After attaching and restarting Codex, check that the TradingCodex MCP server auto-starts:

```bash
./tcx doctor
```

Open the local web dashboard:

```
http://127.0.0.1:48267/
```

## Key Concepts

### Fixed Role Roster

TradingCodex uses **nine fixed specialist agents** coordinated by `head-manager`:

| Agent | Owns |
|-------|------|
| `fundamental-analyst` | Business quality, financial statements, filings, economics |
| `technical-analyst` | Price action, trends, momentum, volume, volatility, liquidity |
| `news-analyst` | Verified news, disclosures, event chronology, catalysts |
| `macro-analyst` | Macro, rates, FX, commodities, liquidity, policy |
| `instrument-analyst` | ETF/index, options, crypto market structure, instrument mechanics |
| `valuation-analyst` | Valuation ranges, scenario assumptions, multiples, sensitivity |
| `portfolio-manager` | Portfolio fit, sizing, concentration, liquidity, draft order tickets |
| `risk-manager` | Downside, restricted-list checks, policy readiness, approval receipts |
| `execution-operator` | Approved submission/cancel/status through service boundary only |

### Workflow Model

```text
evidence -> analysis -> valuation -> portfolio fit -> risk review
  -> draft order -> approval receipt -> approved service-gated submission
  -> connection result -> audit/postmortem
```

The `head-manager` dispatches specialist roles, waits for accepted artifacts, preserves conflicts, and synthesizes only what the workflow has earned.

### Safety Boundary

TradingCodex enforces:

- **No direct live broker requests** — paper execution built-in by default
- **Approval gates** — orders require explicit approval receipts
- **Policy checks** — restricted symbols, duplicate requests blocked
- **Audit trail** — all actions logged with requester, payload, result
- **Provider-driven broker integration** — live execution requires installed provider + all gates
- **No raw secrets** — use environment variables only

## CLI Commands

### Workspace Management

```bash
# Attach TradingCodex to target workspace
tcx attach /path/to/workspace

# Check health and configuration
./tcx doctor

# Show version and build info
./tcx version

# Update TradingCodex in current workspace
./tcx update
```

### Django Service Management

```bash
# Start Django development server (auto-started by MCP)
./tcx runserver

# Run Django management commands
./tcx manage migrate
./tcx manage createsuperuser
./tcx manage collectstatic

# Django shell
./tcx manage shell
```

### Testing and Validation

```bash
# Run workspace smoke tests
./tcx test

# Check Django configuration
./tcx manage check
```

## Configuration

### Workspace Structure

After `tcx attach`, your workspace contains:

```
workspace/
├── .codex/
│   ├── agents/           # Role agent definitions
│   ├── prompts/          # Role-specific prompts
│   ├── skills/           # Skill bundles
│   └── project-mcp.json  # MCP configuration
├── trading/
│   ├── decisions/        # Decision packages
│   ├── research/         # Research markdown
│   └── tickets/          # Order tickets
├── tcx                   # Local CLI wrapper
├── .env                  # Configuration (create this)
└── db.sqlite3            # Local Django database
```

### Environment Variables

Create `.env` in workspace root:

```bash
# Django settings
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True

# Database (optional, defaults to SQLite)
# DATABASE_URL=postgresql://user:pass@localhost/tradingcodex

# Broker provider secrets (example for live execution)
# ALPACA_API_KEY=your-alpaca-key
# ALPACA_API_SECRET=your-alpaca-secret
# ALPACA_BASE_URL=https://paper-api.alpaca.markets

# Data source API keys
# ALPHA_VANTAGE_API_KEY=your-key
# FINNHUB_API_KEY=your-key
```

### MCP Configuration

TradingCodex auto-generates `.codex/project-mcp.json`:

```json
{
  "mcpServers": {
    "tradingcodex": {
      "command": "uvx",
      "args": ["--from", "tradingcodex", "tcx", "mcp"],
      "env": {
        "DJANGO_SETTINGS_MODULE": "tradingcodex.settings",
        "TRADINGCODEX_WORKSPACE": "${workspaceFolder}"
      }
    }
  }
}
```

## Using TradingCodex in Code

### Python Service Layer Examples

```python
from tradingcodex.services.order import OrderService
from tradingcodex.services.approval import ApprovalService
from tradingcodex.services.portfolio import PortfolioService
from tradingcodex.models import OrderTicket, ExecutionMode

# Draft an order ticket
order_service = OrderService()
ticket = order_service.create_ticket(
    symbol="AAPL",
    action="BUY",
    quantity=10,
    order_type="MARKET",
    requester_agent="portfolio-manager",
    execution_mode=ExecutionMode.PAPER,
    notes="Adding tech exposure per macro thesis"
)

# Request approval
approval_service = ApprovalService()
approval = approval_service.request_approval(
    ticket=ticket,
    requester_agent="risk-manager",
    approval_type="ORDER_EXECUTION"
)

# Submit order (requires approval)
if approval.status == "APPROVED":
    result = order_service.submit_ticket(
        ticket=ticket,
        approval_receipt=approval.receipt_id
    )
    print(f"Order submitted: {result.external_id}")
```

### Query Portfolio State

```python
from tradingcodex.services.portfolio import PortfolioService

portfolio_service = PortfolioService()

# Get current positions
positions = portfolio_service.get_positions()
for position in positions:
    print(f"{position.symbol}: {position.quantity} @ ${position.avg_cost}")

# Get portfolio summary
summary = portfolio_service.get_summary()
print(f"Total equity: ${summary.total_equity}")
print(f"Cash: ${summary.cash}")
print(f"Buying power: ${summary.buying_power}")
```

### Research Index Management

```python
from tradingcodex.services.research import ResearchService

research_service = ResearchService()

# Index research markdown
research_service.index_file(
    path="trading/research/aapl-q4-earnings.md",
    analyst_agent="fundamental-analyst",
    symbols=["AAPL"],
    readiness="accepted",
    source_type="EARNINGS_CALL"
)

# Query research by symbol
aapl_research = research_service.find_by_symbol("AAPL")
for doc in aapl_research:
    print(f"{doc.created_at}: {doc.title} ({doc.readiness})")
```

### Policy Checks

```python
from tradingcodex.services.policy import PolicyService

policy_service = PolicyService()

# Check if symbol is restricted
is_allowed = policy_service.check_symbol_allowed("AAPL")

# Check order against policy
policy_result = policy_service.check_order(
    symbol="AAPL",
    action="BUY",
    quantity=1000,
    estimated_value=175000.00,
    account_equity=500000.00
)

if not policy_result.allowed:
    print(f"Policy violation: {policy_result.reason}")
```

## Common Workflows

### 1. Decision Workflow (Alpha)

Generate a Decision Package for an investment idea:

```python
from tradingcodex.workflows.decision import DecisionWorkflow

workflow = DecisionWorkflow()

# Start decision workflow
decision = workflow.start_decision(
    idea="Increase tech exposure via AAPL position",
    requester="head-manager",
    target_symbols=["AAPL"]
)

# Workflow dispatches specialist agents to fill Decision Package:
# - Fundamental analysis
# - Technical analysis  
# - News/catalyst review
# - Macro context
# - Valuation range
# - Portfolio fit
# - Risk assessment
# - Draft order ticket

# Check decision status
status = workflow.get_decision_status(decision.id)
print(f"Decision {decision.id}: {status.stage} ({status.completion_pct}%)")
```

### 2. Broker Integration Setup

```python
from tradingcodex.services.broker import BrokerService
from tradingcodex.integrations.alpaca import AlpacaProvider

broker_service = BrokerService()

# Register broker provider (requires installed provider package)
provider = AlpacaProvider(
    api_key=os.getenv("ALPACA_API_KEY"),
    api_secret=os.getenv("ALPACA_API_SECRET"),
    base_url=os.getenv("ALPACA_BASE_URL")
)

broker_profile = broker_service.register_provider(
    provider_name="alpaca",
    provider=provider,
    account_type="PAPER"
)

# Sync account state
sync_result = broker_service.sync_account(broker_profile.id)
print(f"Synced {sync_result.positions_count} positions, {sync_result.orders_count} orders")

# Review capability profile
capabilities = broker_service.get_capabilities(broker_profile.id)
print(f"Supports market orders: {capabilities.supports_market_orders}")
print(f"Supports extended hours: {capabilities.supports_extended_hours}")
```

### 3. Order Ticket Lifecycle

```python
from tradingcodex.services.order import OrderService
from tradingcodex.models import OrderTicket

order_service = OrderService()

# 1. Draft
ticket = order_service.create_ticket(
    symbol="MSFT",
    action="BUY",
    quantity=5,
    order_type="LIMIT",
    limit_price=350.00,
    time_in_force="DAY",
    requester_agent="portfolio-manager",
    execution_mode="PAPER"
)

# 2. Check (policy, duplicate detection)
check_result = order_service.check_ticket(ticket.id)
if not check_result.passed:
    print(f"Ticket check failed: {check_result.issues}")

# 3. Approve (via risk-manager or approval service)
approval = approval_service.request_approval(
    ticket=ticket,
    requester_agent="risk-manager",
    approval_type="ORDER_EXECUTION"
)

# 4. Submit (requires approval receipt)
if approval.status == "APPROVED":
    result = order_service.submit_ticket(
        ticket=ticket,
        approval_receipt=approval.receipt_id
    )
    
# 5. Monitor
status = order_service.get_ticket_status(ticket.id)
print(f"Order {ticket.id}: {status.state} - {status.fill_pct}% filled")

# 6. Cancel if needed
if status.state == "OPEN":
    cancel_result = order_service.cancel_ticket(ticket.id)
```

### 4. Research Artifact Workflow

Create research markdown that specialist agents consume:

```python
from tradingcodex.services.research import ResearchService
from pathlib import Path

research_service = ResearchService()

# Create research file
research_path = Path("trading/research/tsla-q4-2024-earnings.md")
research_path.parent.mkdir(parents=True, exist_ok=True)

research_content = """# TSLA Q4 2024 Earnings Analysis

## Metadata
- **Symbol**: TSLA
- **Analyst**: fundamental-analyst
- **Date**: 2024-01-25
- **Readiness**: accepted
- **Sources**: 10-K filing, earnings call transcript

## Key Findings

### Revenue Growth
- Q4 revenue: $25.2B (+3% YoY)
- Automotive revenue: $21.5B
- Energy generation: $1.4B

### Margin Pressure
- Gross margin: 17.6% (down from 23.8% YoY)
- Price cuts impacting profitability
- Cost reduction initiatives underway

### Production/Delivery
- Q4 deliveries: 484,507 vehicles
- Cybertruck production ramping
- Berlin/Texas capacity expansion

## Valuation Considerations
- Current P/E: 65x (premium to sector avg 12x)
- Growth dependent on autonomous/energy
- Competition intensifying (BYD, others)

## Risk Factors
- Margin compression risk
- Regulatory/Musk execution risk
- Demand uncertainty in key markets
"""

research_path.write_text(research_content)

# Index for other agents to discover
doc = research_service.index_file(
    path=str(research_path),
    analyst_agent="fundamental-analyst",
    symbols=["TSLA"],
    readiness="accepted",
    source_type="EARNINGS_CALL"
)

print(f"Research indexed: {doc.id}")
```

## MCP Tools

TradingCodex exposes MCP tools for Codex agents:

### Order Management Tools

```
tradingcodex_create_order_ticket
tradingcodex_check_order_ticket
tradingcodex_submit_order_ticket
tradingcodex_cancel_order_ticket
tradingcodex_get_order_status
tradingcodex_list_order_tickets
```

### Portfolio Tools

```
tradingcodex_get_portfolio_positions
tradingcodex_get_portfolio_summary
tradingcodex_sync_portfolio
```

### Research Tools

```
tradingcodex_index_research
tradingcodex_find_research
tradingcodex_get_research_by_symbol
```

### Approval Tools

```
tradingcodex_request_approval
tradingcodex_check_approval_status
```

### Broker Tools

```
tradingcodex_list_broker_providers
tradingcodex_get_broker_capabilities
tradingcodex_sync_broker_account
```

## Web Dashboard

Access at `http://127.0.0.1:48267/` to review:

- **Agents**: Role roster, skills, strategy skills
- **Research**: Markdown index, readiness labels, source metadata
- **Broker Center**: Provider profiles, capabilities, connection status
- **Data Sources**: Available sources, role access scopes
- **Order Tickets**: Draft/approved/submitted orders, lifecycle state
- **Portfolio**: Positions, cash, equity, allocation
- **Activity**: Recent actions, audit trail

## Troubleshooting

### MCP Server Not Starting

```bash
# Check MCP server manually
uvx --from tradingcodex tcx mcp

# Verify project-mcp.json exists
cat .codex/project-mcp.json

# Check MCP logs in Codex
# Codex → Settings → MCP → View Logs
```

### Database Errors

```bash
# Reset and migrate database
./tcx manage migrate --run-syncdb

# Check database connectivity
./tcx manage dbshell
```

### Missing Environment Variables

```bash
# Verify .env file exists
cat .env

# Check that secrets are not in workspace files
grep -r "API_KEY" trading/ research/ .codex/  # Should return no matches
```

### Order Submission Fails

```python
# Check policy violations
from tradingcodex.services.policy import PolicyService
policy_service = PolicyService()

result = policy_service.check_order(
    symbol="AAPL",
    action="BUY", 
    quantity=100,
    estimated_value=17500.00,
    account_equity=100000.00
)

if not result.allowed:
    print(f"Policy block: {result.reason}")

# Verify approval receipt exists
from tradingcodex.models import Approval
approval = Approval.objects.filter(
    ticket_id=ticket.id,
    status="APPROVED"
).first()

if not approval:
    print("No approval found - order requires approval gate")
```

### Provider Not Found

```bash
# List installed providers
./tcx manage shell
>>> from tradingcodex.services.broker import BrokerService
>>> broker_service = BrokerService()
>>> providers = broker_service.list_providers()
>>> for p in providers:
...     print(f"{p.name}: {p.account_type}")

# Install provider package if missing
uv pip install tradingcodex-alpaca
```

### Research Not Indexed

```python
# Manually index research directory
from tradingcodex.services.research import ResearchService
from pathlib import Path

research_service = ResearchService()

for md_file in Path("trading/research").glob("*.md"):
    try:
        doc = research_service.index_file(
            path=str(md_file),
            analyst_agent="fundamental-analyst",
            symbols=[],  # Extract from frontmatter
            readiness="draft"
        )
        print(f"Indexed: {md_file.name}")
    except Exception as e:
        print(f"Failed to index {md_file.name}: {e}")
```

### Live Execution Blocked

Live execution requires **all safety gates**:

1. Installed provider package
2. Provider registered in Broker Center
3. Environment variables set: `PROVIDER_LIVE_EXECUTION_ENABLED=true`
4. Workspace config: `execution_mode: LIVE` in policy
5. Approval receipt with matching payload
6. No duplicate submission (idempotency check)
7. Connection gate passed
8. Audit logged

```python
# Check execution mode
from tradingcodex.models import OrderTicket

ticket = OrderTicket.objects.get(id=ticket_id)
print(f"Execution mode: {ticket.execution_mode}")

# Verify live gate environment variable
import os
print(f"Live execution enabled: {os.getenv('PROVIDER_LIVE_EXECUTION_ENABLED')}")
```

## Best Practices

1. **Always use `head-manager` for workflow coordination** — do not bypass role handoffs
2. **Keep research in markdown files** — avoid storing analysis only in chat transcripts
3. **Use approval gates for all orders** — never self-issue approvals
4. **Start with paper execution** — only enable live after thorough testing
5. **Review policy violations** — understand why orders are blocked
6. **Index research artifacts** — make analysis discoverable to other agents
7. **Check audit trail** — review activity log for unexpected actions
8. **Use environment variables for secrets** — never commit API keys
9. **Run `./tcx doctor` after updates** — verify configuration health
10. **Read generated role prompts** — understand what each specialist agent owns

## Additional Resources

- **Documentation**: [docs/README.md](https://github.com/monarchjuno/tradingcodex/tree/main/docs)
- **Safety Policy**: [docs/safety-policy-and-execution.md](https://github.com/monarchjuno/tradingcodex/blob/main/docs/safety-policy-and-execution.md)
- **Architecture**: [docs/system-architecture.md](https://github.com/monarchjuno/tradingcodex/blob/main/docs/system-architecture.md)
- **Contributing**: [CONTRIBUTING.md](https://github.com/monarchjuno/tradingcodex/blob/main/CONTRIBUTING.md)
- **Discord**: https://discord.gg/Wr25KZnabh
- **License**: Apache-2.0
