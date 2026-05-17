---
name: codex-auto-register
description: Automate ChatGPT/Codex account registration and OAuth token generation using DuckMail temporary email service
triggers:
  - how do I auto-register Codex accounts
  - register ChatGPT accounts automatically
  - generate Codex OAuth tokens programmatically
  - use DuckMail API for ChatGPT registration
  - bulk create Codex accounts with tokens
  - automate Codex account creation
  - set up CLIProxyAPI token files
  - configure codex auto register tool
---

# Codex Auto Register

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

`codex_auto_register` is a Python tool for automated ChatGPT/Codex account registration and OAuth token generation using the DuckMail temporary email API. It supports two workflows:

1. **Root script** (`chatgpt_register.py`): Register ChatGPT accounts with optional OAuth
2. **Codex protocol script** (`codex/protocol_keygen.py`): Full Codex OAuth flow with CLIProxyAPI v6 compatible token output

## Installation

### Dependencies

For root registration script:

```bash
pip install curl_cffi
```

For Codex protocol script:

```bash
pip install requests urllib3
```

### Configuration Setup

1. Copy example configs to active configs:

```bash
cp config.example.json config.json
cp codex/config.example.json codex/config.json
```

2. Edit `config.json` and `codex/config.json` with your credentials (see Configuration section)

## Root Script: ChatGPT Registration

### Configuration (`config.json`)

```json
{
  "total_accounts": 5,
  "duckmail_api_base": "https://duckmail.example.com",
  "duckmail_bearer": "${DUCKMAIL_TOKEN}",
  "proxy": "http://username:password@proxy.example.com:8080",
  "output_file": "registered_accounts.txt",
  "enable_oauth": true,
  "oauth_required": false,
  "upload_api_url": "https://cpa.example.com/api/accounts",
  "upload_api_token": "${CPA_API_TOKEN}"
}
```

**Key Fields:**
- `total_accounts`: Number of accounts to register
- `duckmail_api_base`: DuckMail API endpoint
- `duckmail_bearer`: DuckMail authentication token (use env var)
- `proxy`: HTTP/HTTPS proxy (required for registration)
- `enable_oauth`: Whether to perform OAuth flow
- `oauth_required`: Fail if OAuth fails
- `upload_api_url`/`upload_api_token`: Optional CPA upload

### Usage

```bash
python chatgpt_register.py
```

The script will:
1. Create temporary email via DuckMail
2. Register ChatGPT account
3. Optionally perform OAuth
4. Save results to `registered_accounts.txt`
5. Optionally upload to CPA

### Output Format

`registered_accounts.txt` contains:
```
email@example.com:password123:access_token:refresh_token
email2@example.com:password456:access_token2:refresh_token2
```

## Codex Protocol Script

### Configuration (`codex/config.json`)

```json
{
  "total_accounts": 10,
  "duckmail_api_base": "https://duckmail.example.com",
  "duckmail_bearer": "${DUCKMAIL_TOKEN}",
  "proxy": "http://user:pass@proxy.example.com:8080",
  "output_dir": "codex_tokens",
  "accounts_file": "accounts.txt",
  "csv_file": "registered_accounts.csv",
  "upload_api_url": "https://cpa.example.com/api/codex",
  "upload_api_token": "${CPA_API_TOKEN}",
  "save_access_token": true,
  "save_refresh_token": true,
  "ak_file": "ak.txt",
  "rk_file": "rk.txt"
}

```

### Usage

```bash
python codex/protocol_keygen.py
```

The script performs:
1. DuckMail temporary email creation
2. ChatGPT account registration
3. Codex OAuth login flow
4. Token extraction and storage
5. CLIProxyAPI v6 compatible file generation

### Output Files

**Token JSON files** (CLIProxyAPI v6 format):
```
codex_tokens/
├── fk-xxxxxx.json
├── fk-yyyyyy.json
└── ...
```

Each JSON contains:
```json
{
  "access_token": "ey...",
  "refresh_token": "ey...",
  "expires_at": 1234567890
}
```

**Account files:**
- `accounts.txt`: email:password:access_token:refresh_token
- `ak.txt`: Access tokens (one per line)
- `rk.txt`: Refresh tokens (one per line)
- `registered_accounts.csv`: CSV format with all fields

## Common Patterns

### Environment Variables for Secrets

Never hardcode credentials. Use environment variables:

```bash
export DUCKMAIL_TOKEN="your_duckmail_token"
export CPA_API_TOKEN="your_cpa_token"
```

Reference in config:
```json
{
  "duckmail_bearer": "${DUCKMAIL_TOKEN}",
  "upload_api_token": "${CPA_API_TOKEN}"
}
```

### Proxy Configuration

Both scripts require proxies to bypass rate limits:

```json
{
  "proxy": "http://username:password@proxy-host:port"
}
```

For SOCKS5:
```json
{
  "proxy": "socks5://username:password@proxy-host:port"
}
```

### Batch Registration

Register multiple accounts in sequence:

```python
# In your automation script
import subprocess
import json

config = {
    "total_accounts": 50,
    "duckmail_api_base": "...",
    # ... other config
}

with open("codex/config.json", "w") as f:
    json.dump(config, f)

subprocess.run(["python", "codex/protocol_keygen.py"])
```

### Token File Naming Convention

Codex tokens follow CLIProxyAPI v6 naming:
- Format: `fk-{unique_id}.json`
- Compatible with CLIProxyAPI token directory structure
- Can be directly placed in CPA token folders

## DuckMail API Integration

The project uses DuckMail for temporary email:

**Create email:**
```
POST {duckmail_api_base}/api/email/create
Authorization: Bearer {duckmail_bearer}
```

**Check inbox:**
```
GET {duckmail_api_base}/api/email/{email_id}/messages
Authorization: Bearer {duckmail_bearer}
```

See `duckmaildoc.md` for full API reference.

## Troubleshooting

### Registration Fails

**Problem:** ChatGPT registration returns errors

**Solutions:**
1. Verify proxy is working and not banned
2. Check DuckMail API is accessible
3. Ensure `duckmail_bearer` token is valid
4. Try different proxy IP range

### OAuth Token Not Generated

**Problem:** `enable_oauth: true` but no tokens

**Solutions:**
1. Set `oauth_required: false` to continue without OAuth
2. Verify proxy supports OAuth endpoints
3. Check account was successfully verified
4. Inspect network logs for OAuth failures

### DuckMail Email Not Received

**Problem:** Verification email not arriving

**Solutions:**
1. Wait 30-60 seconds (DuckMail polling interval)
2. Check DuckMail API rate limits
3. Verify email was successfully created
4. Try different email domain if available

### CPA Upload Fails

**Problem:** `upload_api_url` returns errors

**Solutions:**
1. Verify `upload_api_token` is correct
2. Check CPA endpoint is accessible through proxy
3. Ensure token format matches CPA expectations
4. Review CPA API documentation for required fields

### Token Files Not Compatible

**Problem:** CLIProxyAPI doesn't recognize tokens

**Solutions:**
1. Verify filename format: `fk-*.json`
2. Check JSON structure matches expected schema
3. Ensure `expires_at` is Unix timestamp
4. Validate tokens are not expired

### Proxy Authentication Errors

**Problem:** 407 Proxy Authentication Required

**Solutions:**
1. Verify proxy username/password are correct
2. Use URL-encoded credentials in proxy string
3. Test proxy with curl: `curl -x proxy http://api.openai.com`
4. Check proxy supports CONNECT method for HTTPS

## File Structure

Generated files (all in `.gitignore`):

```
project_root/
├── config.json                    # Root script config
├── registered_accounts.txt        # Root script output
└── codex/
    ├── config.json               # Codex script config
    ├── accounts.txt              # email:password:tokens
    ├── ak.txt                    # Access tokens only
    ├── rk.txt                    # Refresh tokens only
    ├── registered_accounts.csv   # CSV format
    └── codex_tokens/             # CLIProxyAPI compatible
        ├── fk-xxxxx.json
        └── fk-yyyyy.json
```

## Security Notes

- Never commit `config.json` files (use `.example.json` templates)
- Store tokens securely (files are gitignored by default)
- Use environment variables for all secrets
- Rotate DuckMail tokens regularly
- Keep proxy credentials separate from code
- Review `registered_accounts.txt` for sensitive data before sharing logs

## Integration with CLIProxyAPI

Place generated token files directly in CPA token directory:

```bash
cp codex/codex_tokens/*.json /path/to/CLIProxyAPI/tokens/codex/
```

CPA will automatically detect and use tokens with `fk-*.json` naming pattern.
