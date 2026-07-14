---
name: chatgpt-plus-subscription-guide
description: Guide for subscribing to ChatGPT Plus/Pro and Codex services from China, including payment methods, proxy setup, and troubleshooting
triggers:
  - how do I subscribe to ChatGPT Plus from China
  - what are the methods to pay for ChatGPT Pro
  - help me set up ChatGPT Plus subscription
  - how to buy ChatGPT Plus with Alipay
  - ChatGPT payment blocked in China
  - recommend ChatGPT Plus recharge platform
  - troubleshoot ChatGPT Plus payment error
  - set up residential IP for OpenAI subscription
---

# ChatGPT Plus/Pro Subscription Guide

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

This skill provides comprehensive guidance for developers and users in China (or regions with similar payment/network restrictions) to successfully subscribe to ChatGPT Plus, ChatGPT Pro, and OpenAI Codex services. It covers payment gateway challenges, network requirements, safe recharge methods, and common troubleshooting scenarios.

## Overview

OpenAI services like ChatGPT Plus ($20/month), ChatGPT Pro ($200/month), and Codex subscriptions face two primary barriers for users in mainland China:

1. **Network restrictions**: Direct access to OpenAI services requires proxy/VPN
2. **Payment gateway blocks**: Stripe (OpenAI's payment processor) rejects cards issued by Chinese banks and flags suspicious IP addresses

This guide focuses on practical, secure methods to overcome these barriers.

## Prerequisites

### Network Requirements

Before attempting any subscription method, ensure:

```bash
# Test OpenAI API accessibility
curl -I https://api.openai.com/v1/models

# Expected: HTTP 200 or 401 (auth required but reachable)
# If timeout/connection refused: proxy not working
```

**Critical**: Use a **residential IP proxy**, not datacenter IPs. Stripe's fraud detection flags datacenter IPs (Digital Ocean, AWS, etc.) and will reject payments.

```bash
# Check your IP type (use a service like ipinfo.io)
curl https://ipinfo.io/json

# Look for "org" field - should NOT contain:
# - "Digital Ocean"
# - "Amazon"
# - "Google Cloud"
# - "Alibaba Cloud"
```

### Account Preparation

```bash
# You need a valid OpenAI account
# Register at: https://chat.openai.com/auth/login
# Use a non-Chinese phone number (e.g., virtual number services)
```

## Subscription Methods

### Method 1: Third-Party Recharge Platform (Recommended)

**Best for**: Developers who want quick, hassle-free subscription with CNY payment.

#### Using PayPrm (Example Platform)

```python
# This is NOT an API - it's a web service flow
# Visit: https://www.payprm.com/

# Process:
# 1. Select service: ChatGPT Plus / Pro / Codex
# 2. Enter your OpenAI account email (NOT password)
# 3. Pay via Alipay/WeChat Pay
# 4. Platform uses their enterprise card to pay OpenAI
# 5. Upgrade reflects in your account within seconds

# Verification script (check if upgrade succeeded)
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

def check_subscription_status():
    try:
        # Plus/Pro users have access to GPT-4
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        print("✅ Subscription active - GPT-4 access confirmed")
        return True
    except openai.error.InvalidRequestError as e:
        if "model" in str(e).lower():
            print("❌ Free tier - no GPT-4 access")
            return False
        raise

check_subscription_status()
```

**Security checklist**:

```python
SAFE_RECHARGE_CHECKLIST = {
    "requires_password": False,  # ❌ NEVER give password
    "auto_payment": True,        # ✅ Automated backend process
    "official_stripe": True,     # ✅ Uses OpenAI's payment gateway
    "refund_policy": True,       # ✅ Has clear refund terms
    "long_running": True,        # ✅ Established service (1+ years)
    "customer_service": True     # ✅ Reachable support
}

def is_platform_safe(platform_info):
    """Evaluate recharge platform safety"""
    return all([
        not platform_info.get("asks_for_password"),
        platform_info.get("uses_official_gateway"),
        platform_info.get("established_business")
    ])
```

### Method 2: Virtual Credit Card (Advanced)

**Best for**: Developers who need cards for multiple international services.

#### Setup Process

```bash
# 1. Choose a virtual card provider supporting KYC for Chinese users
# Examples: Dupay (杜卡迪卡), Nobepay, etc.

# 2. Complete KYC verification
# Required: ID card, selfie, phone number

# 3. Fund the card (usually via USDT/crypto)
# Typical flow:
# - Buy USDT on exchange (e.g., OKX, Binance)
# - Transfer to card provider's address
# - Convert to USD balance

# 4. Get card details
CARD_NUMBER="5405 xxxx xxxx xxxx"  # BIN matters - some BINs blocked
CVV="123"
EXPIRY="12/28"
BILLING_ZIP="10001"  # Use US address (Delaware, Oregon for tax-free)
```

#### Binding to OpenAI

```python
import requests
import os

def test_card_before_binding(card_data):
    """
    Test card on a low-stakes service first
    to avoid OpenAI account flags
    """
    # DO NOT test directly on OpenAI
    # Use a service like:
    # - $1 GitHub Copilot test
    # - Small AWS charge
    
    print("⚠️ IMPORTANT: Test card elsewhere before OpenAI")
    print("Premature failed attempts = account flag")
    
    return {
        "recommended_test_services": [
            "GitHub Copilot ($1 trial)",
            "AWS ($1 verification charge)",
            "Netlify Pro ($1 test)"
        ],
        "openai_binding_tips": [
            "Use clean residential IP",
            "Clear browser cookies",
            "Use incognito mode",
            "One attempt per 24h max"
        ]
    }

# Environment-based configuration
OPENAI_BILLING_CONFIG = {
    "card_number": os.getenv("VCARD_NUMBER"),
    "cvv": os.getenv("VCARD_CVV"),
    "expiry": os.getenv("VCARD_EXPIRY"),
    "billing_address": {
        "line1": "123 Main St",
        "city": "Dover",
        "state": "DE",
        "postal_code": "19901",
        "country": "US"
    }
}
```

#### IP Quality Requirements

```python
import requests

def check_ip_quality():
    """Verify IP is suitable for OpenAI payment"""
    ip_info = requests.get("https://ipinfo.io/json").json()
    
    checks = {
        "country": ip_info.get("country") == "US",  # Ideally match card
        "not_datacenter": "Digital Ocean" not in ip_info.get("org", ""),
        "not_vpn": "VPN" not in ip_info.get("org", "").upper(),
        "clean_asn": True  # Check ASN reputation separately
    }
    
    if all(checks.values()):
        print("✅ IP quality: Good for payment")
    else:
        print("❌ IP quality issues:", 
              [k for k, v in checks.items() if not v])
    
    return all(checks.values())

# Run before attempting payment
check_ip_quality()
```

### Method 3: Apple App Store (iOS Only)

**Best for**: iPhone/iPad users with US Apple ID.

```bash
# Setup US Apple ID
# 1. Create new Apple ID at appleid.apple.com
# 2. Set region to United States
# 3. Use US address (can use mail forwarding service address)

# Purchase US gift card
# - Official: apple.com/shop/gift-cards
# - Or: Amazon.com digital gift cards

# Redeem and subscribe
# 1. Settings > Apple ID > Media & Purchases > View Account
# 2. Redeem Gift Card
# 3. Open ChatGPT app > Settings > Upgrade to Plus
```

#### Verification Script

```python
def check_ios_subscription():
    """
    Verify ChatGPT Plus via iOS
    Note: iOS subscriptions work across all platforms
    """
    import subprocess
    
    # This requires a jailbroken device or macOS with ChatGPT app
    # For standard verification, just log into web interface
    
    print("""
    iOS Subscription Check:
    1. Open ChatGPT app
    2. Tap profile icon
    3. Should show 'ChatGPT Plus' badge
    4. Web/API access also enabled automatically
    """)
    
    return {
        "platforms_enabled": ["iOS", "Web", "API"],
        "renewal": "Auto-renews via App Store",
        "cancellation": "Settings > Subscriptions > ChatGPT"
    }
```

## Common Errors and Fixes

### Error 1: "Your card has been declined"

```python
DECLINED_CARD_TROUBLESHOOTING = {
    "error_code": "card_declined",
    "likely_causes": [
        "Datacenter IP detected",
        "Card BIN on Stripe blacklist",
        "Insufficient funds",
        "3D Secure verification failed"
    ],
    "fixes": {
        "ip_issue": {
            "action": "Switch to residential proxy",
            "verification": "curl https://ipinfo.io/json | grep 'org'",
            "wait_time": "24h before retry"
        },
        "card_bin": {
            "action": "Use different card BIN",
            "recommendations": ["5405", "5561", "4847"],
            "avoid": ["Some 4571", "Some 5339"]  # Known blocked BINs
        },
        "3ds_failed": {
            "action": "Check SMS/email for verification code",
            "timeout": "Must verify within 5 minutes"
        }
    }
}

def handle_card_decline(error_details):
    """Systematic decline troubleshooting"""
    print("🔍 Analyzing card decline...")
    
    steps = [
        "1. Verify IP type (residential required)",
        "2. Check card balance > $25",
        "3. Ensure card supports international payments",
        "4. Clear browser cookies and retry in 24h",
        "5. Try different card if possible"
    ]
    
    for step in steps:
        print(f"  {step}")
    
    return "If all fails: use third-party recharge platform"
```

### Error 2: "Not available in your region"

```bash
# Network detection failed
# OpenAI detected non-supported region

# Fix:
# 1. Clear browser cache
rm -rf ~/.cache/google-chrome/Default/Cache/*

# 2. Use full-tunnel VPN (not just proxy)
# 3. Ensure DNS also goes through VPN

# Test:
curl -H "Accept-Language: en-US" https://chat.openai.com/

# Should return 200, not redirect to /blocked
```

### Error 3: Account Suspended After Payment

```python
SUSPENSION_RECOVERY = {
    "causes": [
        "Chargeback from stolen card (blacklist payment)",
        "Multiple failed payment attempts",
        "Detected account sharing"
    ],
    "recovery_steps": {
        "legitimate_payment": [
            "Contact OpenAI support: help.openai.com",
            "Provide payment receipt",
            "Explain you used third-party service",
            "Request manual review"
        ],
        "chargeback_issue": [
            "If you used sketchy recharge service, account lost",
            "No recovery possible - blacklisted",
            "Create new account with clean payment method"
        ]
    },
    "prevention": "Only use established recharge platforms"
}

def check_account_status():
    """Check if account is in good standing"""
    import openai
    
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    try:
        models = openai.Model.list()
        print("✅ Account active")
        return True
    except openai.error.AuthenticationError:
        print("❌ Account suspended or API key invalid")
        return False
    except Exception as e:
        print(f"⚠️ Error: {e}")
        return None
```

## Best Practices

### Proxy Configuration

```python
# Example: Using requests with residential proxy

import requests
import os

PROXIES = {
    "http": os.getenv("RESIDENTIAL_PROXY_HTTP"),
    "https": os.getenv("RESIDENTIAL_PROXY_HTTPS")
}

def make_openai_request_through_proxy():
    """Template for OpenAI API calls through proxy"""
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-4",
        "messages": [{"role": "user", "content": "test"}],
        "max_tokens": 5
    }
    
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=data,
        proxies=PROXIES,
        timeout=30
    )
    
    return response.json()

# For OpenAI Python library
openai.proxy = os.getenv("RESIDENTIAL_PROXY_HTTPS")
```

### Cost Tracking

```python
def estimate_monthly_costs():
    """Calculate total costs for ChatGPT Plus subscription"""
    
    costs = {
        "chatgpt_plus_usd": 20.00,
        "exchange_rate": 7.2,  # CNY per USD (varies)
        "recharge_platform_fee_pct": 0.05,  # 5% typical
        "proxy_service_monthly": 50.00  # CNY
    }
    
    base_cost_cny = costs["chatgpt_plus_usd"] * costs["exchange_rate"]
    platform_fee = base_cost_cny * costs["recharge_platform_fee_pct"]
    
    total = base_cost_cny + platform_fee + costs["proxy_service_monthly"]
    
    print(f"""
    💰 Monthly Cost Breakdown:
    - ChatGPT Plus: ¥{base_cost_cny:.2f}
    - Platform fee: ¥{platform_fee:.2f}
    - Proxy service: ¥{costs['proxy_service_monthly']:.2f}
    - TOTAL: ¥{total:.2f}
    """)
    
    return total

estimate_monthly_costs()
```

## Security Warnings

```python
RED_FLAGS = {
    "never_do": [
        "Share OpenAI account password with recharge service",
        "Use stolen/carded payment methods",
        "Share account with multiple users",
        "Use public/free proxies for payment",
        "Buy accounts from Xianyu/Taobao individuals"
    ],
    "risks": {
        "shared_accounts": "Permanent ban + data exposure",
        "stolen_cards": "Account blacklisted forever",
        "password_sharing": "Account hijacking + API key theft"
    },
    "safe_practice": [
        "Only use your own account",
        "Use established recharge platforms with NO password requirement",
        "Keep API keys in environment variables",
        "Enable 2FA on OpenAI account",
        "Monitor billing regularly"
    ]
}

def security_checklist():
    """Pre-subscription security verification"""
    print("🔒 Security Checklist:")
    checks = {
        "2FA enabled": "https://platform.openai.com/account/user",
        "API keys rotated": "Last rotation > 90 days ago?",
        "Password unique": "Not reused from other services?",
        "Proxy trustworthy": "Paid, established service?",
        "Payment method": "Official recharge platform?"
    }
    
    for check, detail in checks.items():
        print(f"  [ ] {check}: {detail}")
```

## Environment Variables

```bash
# .env file template
# OpenAI Configuration
OPENAI_API_KEY=sk-...  # From platform.openai.com/api-keys
OPENAI_ORG_ID=org-...  # Optional, if using organization

# Proxy Configuration (residential required)
RESIDENTIAL_PROXY_HTTP=http://user:pass@proxy.example.com:8080
RESIDENTIAL_PROXY_HTTPS=https://user:pass@proxy.example.com:8080

# Virtual Card (if using method 2)
VCARD_NUMBER=5405xxxxxxxxxxxx
VCARD_CVV=xxx
VCARD_EXPIRY=12/28
VCARD_BILLING_ZIP=19901

# Never commit this file to Git
# Add to .gitignore:
# .env
# *.key
# credentials.json
```

## Additional Resources

- Official OpenAI Help: https://help.openai.com/
- Stripe Payment Docs: https://stripe.com/docs/payments
- IP Quality Check: https://ipinfo.io/
- Proxy Quality Testing: https://whoer.net/

This skill provides the essential knowledge for navigating ChatGPT Plus/Pro subscription challenges from regions with payment restrictions. Always prioritize account security and use legitimate payment methods.
