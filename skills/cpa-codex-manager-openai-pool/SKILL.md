---
name: cpa-codex-manager-openai-pool
description: Manage OpenAI account pools with automated registration, CLIProxyAPI monitoring, and intelligent auto-replenishment
triggers:
  - how do I set up CPA Codex Manager for OpenAI account pools
  - automate OpenAI account registration with CPA manager
  - configure CLIProxyAPI monitoring and auto-replenishment
  - manage OpenAI account pools with health checks
  - set up batch registration for OpenAI accounts
  - integrate CPA Codex Manager with CLIProxyAPI
  - monitor and maintain OpenAI account quota
  - configure emergency defense for account pool management
---

# CPA-Codex-Manager OpenAI Account Pool Management

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

CPA-Codex-Manager is a high-performance management panel for OpenAI account pools, featuring automated batch registration, real-time CLIProxyAPI platform monitoring, and intelligent maintenance systems.

## What It Does

- **Batch Account Registration**: Parallel (up to 50 threads, 1000 tasks) and pipeline modes with random intervals
- **CLIProxyAPI Auto-Inspection**: Detects 401 auth failures and quota exhaustion, auto-removes invalid accounts
- **Smart Auto-Replenishment**: Monitors pool health, triggers automated replenishment when accounts fall below threshold
- **Real-time Monitoring**: WebSocket-based log streaming and progress visualization
- **Multi-Email Support**: Integrates Outlook, TempMail, CloudMail services
- **Emergency Defense**: Dynamic threshold protection with configurable cooling periods

## Installation

### Standard Installation

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### Environment Configuration

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```bash
# Web UI Configuration
WEBUI_HOST=0.0.0.0
WEBUI_PORT=8000
WEBUI_ACCESS_PASSWORD=your_secure_password

# Database (SQLite default)
APP_DATABASE_URL=data/database.db

# Or PostgreSQL
# APP_DATABASE_URL=postgresql://user:password@host:5432/dbname
```

### Docker Installation

```bash
mkdir -p ~/CPA-Codex-Manager/data ~/CPA-Codex-Manager/logs
cd ~/CPA-Codex-Manager
curl -O https://raw.githubusercontent.com/Maoleio/CPA-Codex-Manager/main/docker-compose.yml
docker compose up -d
```

### Desktop Mode

```bash
pip install pywebview
python desktop.py
```

## Running the Application

### Web Mode

```bash
python webui.py
```

Access at `http://localhost:8000`

### Docker Mode

```bash
docker compose up -d
docker compose logs -f  # View logs
docker compose pull && docker compose up -d  # Update
```

## Core Python API Usage

### Database Models

```python
from app.models import (
    AccountPool,
    RegistrationTask,
    CPAService,
    InspectionHistory
)
from app.database import get_db

# Query account pool
with get_db() as db:
    accounts = db.query(AccountPool).filter(
        AccountPool.status == 'ready'
    ).all()
    
    print(f"Ready accounts: {len(accounts)}")
    for acc in accounts:
        print(f"Email: {acc.email}, Token: {acc.refresh_token}")
```

### Registration Task Creation

```python
from app.services.registration import RegistrationService
from app.schemas import RegistrationTaskCreate

async def create_batch_registration():
    service = RegistrationService()
    
    task_data = RegistrationTaskCreate(
        count=100,
        email_service="outlook",  # outlook, tempmail, cloudmail
        mode="parallel",  # parallel or pipeline
        max_workers=50,
        random_interval_min=5,
        random_interval_max=15
    )
    
    task = await service.create_task(task_data)
    print(f"Task created: {task.id}")
    
    # Start registration
    await service.start_task(task.id)
```

### CPA Service Integration

```python
from app.services.cpa_service import CPAServiceManager

async def configure_cpa():
    manager = CPAServiceManager()
    
    # Add CPA service
    cpa = await manager.add_service(
        name="Production CPA",
        base_url="https://your-cpa-instance.com",
        admin_token="${CPA_ADMIN_TOKEN}",
        enabled=True
    )
    
    # Configure auto-inspection
    await manager.update_inspection_config(
        cpa.id,
        enabled=True,
        interval_minutes=60,
        check_401=True,
        check_quota=True,
        auto_remove=True
    )
```

### Auto-Replenishment Configuration

```python
from app.services.replenishment import ReplenishmentService

async def setup_auto_replenish():
    service = ReplenishmentService()
    
    # Configure replenishment rules
    await service.configure(
        cpa_service_id=1,
        enabled=True,
        threshold=50,  # Trigger when ready accounts < 50
        replenish_count=100,
        mode="parallel",
        email_service="outlook"
    )
```

### Manual Account Inspection

```python
from app.services.inspection import InspectionService

async def run_inspection():
    service = InspectionService()
    
    result = await service.inspect_cpa_accounts(
        cpa_service_id=1,
        check_401=True,
        check_quota=True,
        auto_remove=True
    )
    
    print(f"Inspection complete:")
    print(f"  Total checked: {result['total_checked']}")
    print(f"  Valid: {result['valid_count']}")
    print(f"  Invalid (401): {result['invalid_401']}")
    print(f"  Quota exhausted: {result['quota_exhausted']}")
    print(f"  Removed: {result['removed_count']}")
```

### Emergency Defense Configuration

```python
from app.services.emergency import EmergencyDefenseService

async def configure_emergency_defense():
    service = EmergencyDefenseService()
    
    await service.configure(
        enabled=True,
        threshold_percentage=50,  # Trigger if ready% < 50%
        cleanup_percentage=50,    # Remove 50% of accounts
        cooldown_minutes=5        # Wait 5min before retry
    )
```

## WebSocket Integration for Real-time Logs

```python
from fastapi import WebSocket
import asyncio

# Server-side WebSocket handler
async def websocket_log_stream(websocket: WebSocket, task_id: int):
    await websocket.accept()
    
    # Stream registration logs
    async for log_line in get_task_logs(task_id):
        await websocket.send_json({
            "type": "log",
            "task_id": task_id,
            "message": log_line,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    await websocket.close()
```

## Common Patterns

### Full Registration Workflow

```python
from app.services.registration import RegistrationService
from app.services.cpa_service import CPAServiceManager

async def full_registration_workflow():
    # Create and start registration task
    reg_service = RegistrationService()
    task = await reg_service.create_task(
        count=200,
        email_service="outlook",
        mode="parallel",
        max_workers=50
    )
    
    # Monitor progress
    await reg_service.start_task(task.id)
    
    while True:
        status = await reg_service.get_task_status(task.id)
        print(f"Progress: {status['success']}/{status['total']} "
              f"({status['progress_percentage']:.1f}%)")
        
        if status['status'] in ['completed', 'failed']:
            break
        
        await asyncio.sleep(5)
    
    # Upload successful accounts to CPA
    cpa_manager = CPAServiceManager()
    uploaded = await cpa_manager.upload_accounts(
        cpa_service_id=1,
        task_id=task.id
    )
    
    print(f"Uploaded {uploaded} accounts to CPA")
```

### Scheduled Inspection with Auto-Replenish

```python
import asyncio
from app.services.inspection import InspectionService
from app.services.replenishment import ReplenishmentService

async def scheduled_maintenance():
    inspection = InspectionService()
    replenish = ReplenishmentService()
    
    while True:
        # Run inspection
        result = await inspection.inspect_cpa_accounts(
            cpa_service_id=1,
            check_401=True,
            check_quota=True,
            auto_remove=True
        )
        
        # Check if replenishment needed
        ready_count = result['valid_count']
        if ready_count < 50:
            print(f"Low account count ({ready_count}), triggering replenishment")
            await replenish.trigger_replenish(
                cpa_service_id=1,
                count=100
            )
        
        # Wait 1 hour
        await asyncio.sleep(3600)
```

### Query Account Pool Statistics

```python
from app.database import get_db
from app.models import AccountPool
from sqlalchemy import func

def get_pool_statistics():
    with get_db() as db:
        stats = db.query(
            AccountPool.status,
            func.count(AccountPool.id).label('count')
        ).group_by(AccountPool.status).all()
        
        return {status: count for status, count in stats}

# Example output: {'ready': 150, 'invalid': 10, 'quota_exhausted': 5}
```

## Configuration Best Practices

### Inspection Configuration

```python
# config.py or .env
INSPECTION_CONFIG = {
    "interval_minutes": 60,  # Check every hour
    "check_401": True,       # Enable auth failure detection
    "check_quota": True,     # Enable quota exhaustion detection
    "auto_remove": True,     # Auto-remove invalid accounts
    "emergency_threshold": 50,  # Trigger emergency if ready% < 50%
}
```

### Replenishment Configuration

```python
REPLENISHMENT_CONFIG = {
    "enabled": True,
    "threshold": 50,          # Trigger when ready accounts < 50
    "replenish_count": 100,   # Add 100 accounts per trigger
    "mode": "parallel",       # Use parallel mode for speed
    "email_service": "outlook",
    "max_workers": 50
}
```

### Registration Modes

**Parallel Mode** (fast, high volume):
```python
parallel_config = {
    "mode": "parallel",
    "max_workers": 50,
    "count": 1000
}
```

**Pipeline Mode** (stealth, bypass rate limits):
```python
pipeline_config = {
    "mode": "pipeline",
    "random_interval_min": 10,
    "random_interval_max": 30,
    "count": 100
}
```

## Troubleshooting

### Registration Failures

```python
# Check failed registrations
from app.models import RegistrationTask

with get_db() as db:
    failed_tasks = db.query(RegistrationTask).filter(
        RegistrationTask.status == 'failed'
    ).all()
    
    for task in failed_tasks:
        print(f"Task {task.id}: {task.error_message}")
```

### CPA Connection Issues

```python
from app.services.cpa_service import CPAServiceManager

async def test_cpa_connection():
    manager = CPAServiceManager()
    
    try:
        health = await manager.check_health(cpa_service_id=1)
        print(f"CPA Status: {health['status']}")
    except Exception as e:
        print(f"Connection failed: {e}")
        # Check base_url and admin_token in database
```

### Account Pool Health Check

```python
from app.services.inspection import InspectionService

async def health_check():
    service = InspectionService()
    
    result = await service.inspect_cpa_accounts(
        cpa_service_id=1,
        check_401=True,
        check_quota=True,
        auto_remove=False  # Don't remove, just check
    )
    
    total = result['total_checked']
    valid = result['valid_count']
    health_percentage = (valid / total * 100) if total > 0 else 0
    
    print(f"Pool health: {health_percentage:.1f}%")
    
    if health_percentage < 50:
        print("⚠️  Pool health critical, consider manual intervention")
```

### Database Migration

```python
# If using PostgreSQL, migrate from SQLite
from app.database import init_db
from app.models import Base

# Initialize new database schema
init_db()

# Manual data migration (example)
import sqlite3
from app.database import get_db

sqlite_conn = sqlite3.connect('data/database.db')
sqlite_cursor = sqlite_conn.cursor()

accounts = sqlite_cursor.execute(
    "SELECT email, password, refresh_token, status FROM account_pool"
).fetchall()

with get_db() as db:
    for email, password, token, status in accounts:
        account = AccountPool(
            email=email,
            password=password,
            refresh_token=token,
            status=status
        )
        db.add(account)
    db.commit()
```

## Desktop Packaging

### macOS

```bash
chmod +x scripts/build_macos_dmg.sh
./scripts/build_macos_dmg.sh
# Output: dist/CPA-Codex-Manager.dmg
```

### Windows

```bat
scripts\build_windows.bat
REM Output: dist\CPA-Codex-Manager\CPA-Codex-Manager.exe
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `WEBUI_HOST` | `127.0.0.1` | Web UI bind address |
| `WEBUI_PORT` | `8000` | Web UI port |
| `WEBUI_ACCESS_PASSWORD` | - | Admin password (required) |
| `APP_DATABASE_URL` | `data/database.db` | Database connection string |

All secrets should be stored in environment variables or `.env` file, never hardcoded.
