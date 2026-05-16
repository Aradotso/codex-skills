---
name: codex-console-automation
description: AI skill for managing OpenAI account automation using codex-console - registration, payment, token management, and batch operations
triggers:
  - "help me automate OpenAI account registration"
  - "set up codex-console for batch account creation"
  - "configure email services for codex account automation"
  - "manage OpenAI accounts with codex-console"
  - "automate OpenAI subscription and payment binding"
  - "export and upload OpenAI tokens to API gateway"
  - "troubleshoot codex-console registration issues"
  - "configure auto-replenishment for OpenAI accounts"
---

# codex-console Automation Skill

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

codex-console is a comprehensive automation platform for managing OpenAI accounts at scale. It handles registration, login, token extraction, subscription management, payment binding, auto-replenishment, and integration with API gateways like CPA, Sub2API, Team Manager, and New-API.

This is a maintained fork that fixes compatibility issues with OpenAI's evolving authentication flow, including Sentinel POW solving, split registration/login flows, and improved OTP handling.

**Key capabilities:**
- Web UI for task management and monitoring
- Batch account registration with email service integration
- Semi-automated payment card binding with 3DS support
- Automated token refresh and upload to API gateways
- Self-check and repair system
- Auto-replenishment based on inventory levels
- Tag-based account pooling and team management
- SQLite or PostgreSQL backend

## Installation

### Using Python (Recommended for Development)

```bash
# Clone the repository
git clone https://github.com/dou-jiang/codex-console.git
cd codex-console

# Install dependencies with uv (recommended)
uv sync

# Or use pip
pip install -r requirements.txt
```

### Using Docker

```bash
# With docker-compose
docker-compose up -d

# Or with docker run
docker run -d \
  -p 1455:1455 \
  -p 6080:6080 \
  -e WEBUI_HOST=0.0.0.0 \
  -e WEBUI_PORT=1455 \
  -e WEBUI_ACCESS_PASSWORD=your_secure_password \
  -v $(pwd)/data:/app/data \
  --name codex-console \
  ghcr.io/dou-jiang/codex-console:latest
```

### Building Standalone Executable

```bash
# Windows
build.bat

# Linux/macOS
bash build.sh
```

The executable will be in `dist/codex-console-windows-X64.exe` or equivalent.

## Configuration

### Environment Variables

Create `.env` from template:

```bash
cp .env.example .env
```

Key variables:

```bash
# Server
APP_HOST=0.0.0.0
APP_PORT=8000
APP_ACCESS_PASSWORD=admin123

# Database (SQLite by default)
APP_DATABASE_URL=data/database.db

# Or PostgreSQL
APP_DATABASE_URL=postgresql://user:password@host:5432/dbname

# Logging
LOG_LEVEL=info

# Debug mode
DEBUG=false
```

**Priority:** CLI args > `.env` > database settings > defaults

### First-Time Setup

1. Start the web UI:
```bash
python webui.py --access-password mypassword
```

2. Access at `http://127.0.0.1:8000`

3. Configure in Settings page:
   - Email service credentials
   - Proxy settings
   - Upload targets (CPA/Sub2API/New-API)
   - Payment automation options

## Core Usage Patterns

### Starting the Web UI

```python
# webui.py - main entry point
import uvicorn
from src.web.app import app
from src.utils.settings import get_settings

if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
        log_level=settings.log_level.lower()
    )
```

CLI options:

```bash
# Default
python webui.py

# Custom host/port
python webui.py --host 0.0.0.0 --port 8080

# Set password
python webui.py --access-password mypassword

# Debug mode (hot reload)
python webui.py --debug
```

### Email Service Integration

codex-console supports multiple email providers:

```python
# src/services/email_service.py
from src.services.email_service import EmailServiceFactory

# Configure in database or code
email_config = {
    "service_type": "cloudmail",  # or luckmail, yydsmail, outlook
    "api_key": None,  # from env: CLOUDMAIL_API_KEY
    "config": {
        "base_url": "https://api.cloudmail.com",
        "timeout": 30
    }
}

# Factory creates appropriate service
service = EmailServiceFactory.create(email_config)

# Fetch verification code
otp = await service.get_verification_code(
    email="test@example.com",
    timeout=60
)
```

**Supported services:**
- CloudMail (API-based)
- LuckMail (API-based)
- YYDS Mail (API-based)
- Outlook (self-hosted accounts)

### Registration Flow

```python
# src/core/register.py
from src.core.register import RegisterService
from src.models.task import RegisterTask

async def register_account(email: str, password: str, proxy: str):
    """Register a new OpenAI account"""
    
    task = RegisterTask(
        email=email,
        password=password,
        proxy=proxy,
        status="pending"
    )
    
    service = RegisterService(task)
    result = await service.execute()
    
    return result
    # Returns: {"success": True, "account_id": 123, "token": "..."}
```

**Key steps handled:**
1. Sentinel POW solving
2. Email verification (auto-fetch from email service)
3. Split registration/login flow
4. Token extraction
5. Workspace caching

### Batch Registration

```python
# src/core/auto_register.py
from src.core.auto_register import AutoRegisterService

async def batch_register(count: int):
    """Register multiple accounts"""
    
    service = AutoRegisterService()
    
    # Configure
    await service.configure({
        "target_count": count,
        "email_service": "cloudmail",
        "proxy_pool": "residential",
        "auto_upload": True,
        "upload_target": "newapi"
    })
    
    # Start registration
    await service.start()
    
    # Monitor progress
    status = await service.get_status()
    # Returns: {"completed": 50, "failed": 2, "running": True}
```

### Payment Binding

```python
# src/core/payment.py
from src.core.payment import PaymentService
from src.models.task import BindCardTask

async def bind_payment_card(account_id: int, card_info: dict):
    """Bind payment card to account (semi-automated)"""
    
    task = BindCardTask(
        account_id=account_id,
        card_number=card_info["number"],  # Store encrypted
        expiry=card_info["expiry"],
        cvv=card_info["cvv"],
        billing_address={
            "street": "auto-generated",  # Random US address
            "city": "New York",
            "state": "NY",
            "zip": "10001",
            "country": "US"
        },
        status="pending"
    )
    
    service = PaymentService(task)
    result = await service.execute()
    
    # Note: 3DS verification requires manual intervention
    # Browser window will open for 3DS flow
    
    return result
```

### Token Management

```python
# src/core/account_manager.py
from src.core.account_manager import AccountManager
from src.models.account import Account

async def refresh_account_token(account_id: int):
    """Refresh access token for an account"""
    
    manager = AccountManager()
    account = await manager.get_account(account_id)
    
    # Refresh using refresh_token
    new_token = await manager.refresh_token(account)
    
    # Auto-upload to configured targets
    await manager.upload_to_targets(account)
    
    return new_token
```

### Auto-Upload to API Gateways

```python
# src/services/upload_service.py
from src.services.upload_service import UploadService

async def upload_account(account_id: int, target: str):
    """Upload account to API gateway"""
    
    service = UploadService()
    
    # Supported targets: cpa, sub2api, team_manager, newapi
    result = await service.upload(
        account_id=account_id,
        target=target
    )
    
    return result
    # Returns: {"success": True, "external_id": "...", "quota": 20}
```

**New-API configuration example:**

```python
# In settings or database
newapi_config = {
    "base_url": "https://api.example.com",
    "api_key": None,  # from env: NEWAPI_API_KEY
    "auto_upload": True,
    "upload_on_register": True,
    "quota_per_account": 20
}
```

### Task Management

```python
# src/services/task_service.py
from src.services.task_service import TaskService

async def manage_tasks():
    """Unified task management"""
    
    service = TaskService()
    
    # Create registration task
    task_id = await service.create_task(
        task_type="register",
        count=10,
        config={"email_service": "cloudmail"}
    )
    
    # Pause task
    await service.pause_task(task_id)
    
    # Resume task
    await service.resume_task(task_id)
    
    # Cancel task
    await service.cancel_task(task_id)
    
    # Retry failed items
    await service.retry_task(task_id)
    
    # Get status
    status = await service.get_task_status(task_id)
```

### Auto-Replenishment

```python
# src/core/auto_replenishment.py
from src.core.auto_replenishment import AutoReplenishmentService

async def configure_auto_replenish():
    """Configure automatic account replenishment"""
    
    service = AutoReplenishmentService()
    
    await service.configure({
        "enabled": True,
        "min_threshold": 10,  # Start when inventory < 10
        "target_count": 50,   # Replenish to 50 accounts
        "check_interval": 3600,  # Check every hour
        "max_daily_registers": 100
    })
    
    # Start monitoring
    await service.start()
```

### Self-Check and Repair

```python
# src/services/selfcheck.py
from src.services.selfcheck import SelfCheckService

async def run_system_selfcheck():
    """Run comprehensive system self-check"""
    
    service = SelfCheckService()
    
    # Run checks
    results = await service.run_all_checks()
    
    # Results include:
    # - Database connectivity
    # - Email service status
    # - Proxy availability
    # - Account token validity
    # - Upload target connectivity
    
    # Auto-repair if enabled
    if results["has_issues"]:
        await service.auto_repair(results)
    
    return results
```

### Account Pooling and Tags

```python
# src/models/account.py
from src.core.account_manager import AccountManager

async def manage_account_pools():
    """Organize accounts with tags and pools"""
    
    manager = AccountManager()
    
    # Add account to team pool
    await manager.update_account(
        account_id=123,
        updates={
            "role_tag": "team_member",
            "biz_tag": "project_alpha",
            "pool_state": "team_pool",
            "priority": 5
        }
    )
    
    # Query by pool
    team_accounts = await manager.get_accounts_by_pool("team_pool")
    
    # Query by tag
    project_accounts = await manager.get_accounts_by_tag("project_alpha")
```

## Database Models

### Account Model

```python
# src/models/account.py
from sqlalchemy import Column, Integer, String, DateTime, JSON
from src.database import Base

class Account(Base):
    __tablename__ = "accounts"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    
    # Auth tokens
    access_token = Column(String)
    refresh_token = Column(String)
    session_token = Column(String)
    
    # Status
    status = Column(String, default="active")  # active, suspended, expired
    subscription_status = Column(String)  # none, trial, plus, team
    
    # Pooling and tags
    role_tag = Column(String)  # team_member, candidate, etc.
    biz_tag = Column(String)   # project/client identifier
    pool_state = Column(String)  # team_pool, candidate_pool, blocked_pool
    priority = Column(Integer, default=0)
    
    # Metadata
    quota = Column(Integer, default=0)
    workspace_id = Column(String)
    last_used_at = Column(DateTime)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    
    # Upload tracking
    upload_status = Column(JSON)  # {"cpa": true, "newapi": true}
```

### Task Model

```python
# src/models/task.py
from sqlalchemy import Column, Integer, String, DateTime, JSON
from src.database import Base

class RegisterTask(Base):
    __tablename__ = "register_tasks"
    
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    proxy = Column(String)
    
    # Task state
    status = Column(String, default="pending")  # pending, running, completed, failed, paused
    progress = Column(Integer, default=0)
    error_message = Column(String)
    
    # Result
    account_id = Column(Integer)  # Reference to created account
    access_token = Column(String)
    
    # Metadata
    created_at = Column(DateTime)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)
    retry_count = Column(Integer, default=0)
```

## API Routes

### Account Management

```python
# GET /api/accounts
# List all accounts with filters
GET /api/accounts?status=active&pool=team_pool&limit=50

# GET /api/accounts/{id}
# Get account details
GET /api/accounts/123

# POST /api/accounts/{id}/refresh
# Refresh account token
POST /api/accounts/123/refresh

# POST /api/accounts/{id}/upload
# Upload to API gateway
POST /api/accounts/123/upload
{
    "target": "newapi"
}

# DELETE /api/accounts/{id}
# Delete account
DELETE /api/accounts/123
```

### Task Management

```python
# POST /api/tasks/register
# Create registration task
POST /api/tasks/register
{
    "count": 10,
    "email_service": "cloudmail",
    "auto_upload": true,
    "upload_target": "newapi"
}

# POST /api/tasks/{id}/pause
# Pause task
POST /api/tasks/123/pause

# POST /api/tasks/{id}/resume
# Resume task
POST /api/tasks/123/resume

# POST /api/tasks/{id}/cancel
# Cancel task
POST /api/tasks/123/cancel

# POST /api/tasks/{id}/retry
# Retry failed items
POST /api/tasks/123/retry
```

### Export and Import

```python
# GET /api/export/accounts
# Export accounts in various formats
GET /api/export/accounts?format=codex&pool=team_pool

# Supported formats: codex, json, csv, newapi, cpa

# POST /api/import/accounts
# Import accounts from file
POST /api/import/accounts
Content-Type: multipart/form-data
file: accounts.json
```

## Common Workflows

### Complete Registration Pipeline

```python
import asyncio
from src.core.register import RegisterService
from src.services.upload_service import UploadService
from src.models.task import RegisterTask

async def full_registration_workflow():
    """End-to-end: register account, verify, bind card, upload"""
    
    # Step 1: Register
    task = RegisterTask(
        email="auto-generated@cloudmail.com",
        password="SecurePass123!",
        proxy="http://proxy.example.com:8080"
    )
    
    reg_service = RegisterService(task)
    result = await reg_service.execute()
    
    if not result["success"]:
        raise Exception(f"Registration failed: {result['error']}")
    
    account_id = result["account_id"]
    
    # Step 2: Bind payment (semi-automated)
    # Note: This opens browser for 3DS - requires monitoring
    from src.core.payment import PaymentService
    from src.models.task import BindCardTask
    
    bind_task = BindCardTask(
        account_id=account_id,
        card_number="encrypted_card_data",
        expiry="12/25",
        cvv="123",
        billing_address={"auto": True}  # Auto-generate random US address
    )
    
    payment_service = PaymentService(bind_task)
    payment_result = await payment_service.execute()
    
    # Step 3: Upload to API gateway
    upload_service = UploadService()
    upload_result = await upload_service.upload(
        account_id=account_id,
        target="newapi"
    )
    
    return {
        "account_id": account_id,
        "email": task.email,
        "uploaded": upload_result["success"]
    }

# Run
asyncio.run(full_registration_workflow())
```

### Batch Account Refresh

```python
from src.core.account_manager import AccountManager
import asyncio

async def batch_refresh_tokens():
    """Refresh tokens for all active accounts"""
    
    manager = AccountManager()
    
    # Get all active accounts
    accounts = await manager.get_accounts(status="active")
    
    results = []
    for account in accounts:
        try:
            new_token = await manager.refresh_token(account)
            
            # Auto-upload if configured
            if manager.settings.auto_upload_on_refresh:
                await manager.upload_to_targets(account)
            
            results.append({
                "account_id": account.id,
                "success": True,
                "token": new_token
            })
        except Exception as e:
            results.append({
                "account_id": account.id,
                "success": False,
                "error": str(e)
            })
    
    return results

# Run
asyncio.run(batch_refresh_tokens())
```

### Scheduled Auto-Replenishment

```python
# src/schedulers/auto_replenish_scheduler.py
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.core.auto_replenishment import AutoReplenishmentService

scheduler = AsyncIOScheduler()

async def check_and_replenish():
    """Check inventory and trigger replenishment if needed"""
    
    service = AutoReplenishmentService()
    status = await service.check_inventory()
    
    if status["current_count"] < status["min_threshold"]:
        needed = status["target_count"] - status["current_count"]
        await service.start_replenishment(count=needed)

# Schedule every hour
scheduler.add_job(
    check_and_replenish,
    'interval',
    hours=1,
    id='auto_replenish'
)

scheduler.start()
```

## Troubleshooting

### Sentinel POW Solving Fails

**Issue:** Registration fails with "Sentinel POW required" error.

**Solution:** Ensure you're using latest version (v1.1.2+) which includes POW solving:

```python
# src/core/register.py automatically handles this
# If issues persist, check proxy quality:
from src.utils.proxy import test_proxy

result = await test_proxy("http://proxy.example.com:8080")
if not result["sentinel_pass"]:
    print("Proxy blocked by Sentinel - use residential proxy")
```

### Email OTP Not Received

**Issue:** Registration hangs waiting for verification code.

**Solution:**

1. Check email service status in Settings
2. Verify API key is set correctly
3. Test email service manually:

```python
from src.services.email_service import EmailServiceFactory

service = EmailServiceFactory.create({
    "service_type": "cloudmail",
    "api_key": "test_key"
})

# Test connection
status = await service.test_connection()
print(status)  # Should return {"success": True}
```

### Token Refresh Fails

**Issue:** `refresh_token` returns 401 Unauthorized.

**Solution:**

1. Check if refresh token is expired (30 days typically)
2. Force re-login instead:

```python
from src.core.account_manager import AccountManager

manager = AccountManager()
account = await manager.get_account(account_id)

# Re-login to get fresh tokens
await manager.re_login(account)
```

### Payment Binding Stuck on 3DS

**Issue:** Browser opens for 3DS but verification never completes.

**Solution:**

3DS cannot be automated. Monitor the browser window and:
1. Complete 3DS challenge manually
2. Wait for callback
3. codex-console will detect completion and continue

### Database Migration Issues

**Issue:** Alembic migration fails after update.

**Solution:**

```bash
# Reset to latest migration
alembic stamp head

# Or manually migrate
alembic upgrade head

# If corrupted, backup and recreate:
cp data/database.db data/database.db.backup
rm data/database.db
python webui.py  # Auto-creates with latest schema
```

### Auto-Upload Not Working

**Issue:** Accounts registered but not uploaded to New-API/CPA.

**Solution:**

1. Verify upload target is configured in Settings
2. Test connection:

```python
from src.services.upload_service import UploadService

service = UploadService()
test_result = await service.test_target("newapi")
print(test_result)  # Check connectivity
```

3. Enable auto-upload in task config:

```python
{
    "auto_upload": true,
    "upload_target": "newapi",
    "upload_on_register": true
}
```

### High Registration Failure Rate

**Issue:** Most registration attempts fail.

**Solution:**

1. **Use residential proxies** - datacenter IPs are often blocked
2. **Slow down** - add delays between attempts
3. **Check email service quota** - may be rate-limited
4. **Review logs** - look for specific error patterns

```bash
# Enable debug logging
export LOG_LEVEL=debug
python webui.py

# Check logs in data/logs/
tail -f data/logs/register.log
```

### Port Already in Use

**Issue:** `Address already in use` error on startup.

**Solution:**

codex-console auto-switches ports if 8000 is taken. To force a specific port:

```bash
python webui.py --port 8080
```

Or kill the process using port 8000:

```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

## Advanced Configuration

### Custom Email Service

Implement custom email provider:

```python
# src/services/custom_email.py
from src.services.email_service import BaseEmailService

class CustomEmailService(BaseEmailService):
    async def get_verification_code(self, email: str, timeout: int = 60) -> str:
        """Fetch OTP from custom provider"""
        # Your implementation
        pass
    
    async def test_connection(self) -> dict:
        """Test API connectivity"""
        # Your implementation
        pass

# Register in factory
# src/services/email_service.py
EMAIL_SERVICES["custom"] = CustomEmailService
```

### Custom Upload Target

Add new API gateway integration:

```python
# src/services/custom_upload.py
from src.services.upload_service import BaseUploadTarget

class CustomUploadTarget(BaseUploadTarget):
    async def upload_account(self, account: Account) -> dict:
        """Upload account to custom gateway"""
        # Your implementation
        pass

# Register
# src/services/upload_service.py
UPLOAD_TARGETS["custom"] = CustomUploadTarget
```

## Security Best Practices

1. **Never commit secrets** - use environment variables:
```bash
export CLOUDMAIL_API_KEY=your_key_here
export NEWAPI_API_KEY=your_key_here
```

2. **Change default password** immediately:
```bash
python webui.py --access-password strong_password_here
```

3. **Use PostgreSQL for production** - SQLite is development-only:
```bash
export APP_DATABASE_URL=postgresql://user:pass@host:5432/db
```

4. **Encrypt sensitive fields** - card data, passwords are encrypted at rest

5. **Enable audit logging** - track all operations:
```python
from src.models.audit import OperationAuditLog

# Auto-logged for sensitive operations
```

## Resources

- **Official Repo:** https://github.com/dou-jiang/codex-console
- **Blog/Docs:** https://blog.cysq8.cn/
- **QQ Group:** 291638849
- **Telegram:** https://t.me/codex_console
- **License:** MIT
