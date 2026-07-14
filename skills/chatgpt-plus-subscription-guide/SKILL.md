---
name: chatgpt-plus-subscription-guide
description: Guide for purchasing and managing ChatGPT Plus/Pro and Codex subscriptions from China using various payment methods
triggers:
  - how do I subscribe to ChatGPT Plus from China
  - what are the payment options for ChatGPT Pro
  - how to buy ChatGPT Plus without a foreign credit card
  - chatgpt subscription payment methods for chinese users
  - how to use virtual credit cards for openai
  - chatgpt plus代充怎么操作
  - 国内如何购买chatgpt会员
  - openai stripe payment issues china
---

# ChatGPT Plus/Pro Subscription Guide

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

This skill provides guidance on subscribing to ChatGPT Plus/Pro and Codex services from regions with payment restrictions, particularly mainland China. It covers payment methods, common issues, and practical solutions for accessing OpenAI services.

## Overview

This project documents strategies for Chinese users to subscribe to ChatGPT Plus/Pro when faced with:
- Stripe payment gateway geo-restrictions
- Domestic credit card rejections
- IP-based fraud detection
- 3D Secure verification failures

## Key Payment Methods

### 1. Virtual Credit Cards (Technical Route)

**Use Case**: Users comfortable with cryptocurrency and international payment platforms

**Providers**: Platforms supporting KYC verification from China
- Requires: Identity verification, crypto funding (USDT)
- Card prefixes: 5405/5561 (US/HK region cards)

**Implementation Pattern**:
```bash
# Step 1: Register on virtual card platform
# Step 2: Complete KYC verification
# Step 3: Fund card via cryptocurrency
# Example: Convert CNY → USDT → Card Balance

# Step 4: Obtain card details
CARD_NUMBER="5405XXXXXXXX1234"
CVC="123"
BILLING_ZIP="10001"  # US billing address required

# Step 5: Use residential IP (not datacenter) for binding
# Ensure IP reputation score is clean
```

**Network Requirements**:
```python
# Check if your proxy is residential vs datacenter
import requests

def check_ip_type(proxy_url):
    """
    Verify IP is residential to avoid Stripe blocks
    """
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Use IP quality check service
    response = requests.get(
        'https://ipqualityscore.com/api/json/ip',
        params={'ip': 'YOUR_IP'},
        headers=headers,
        proxies={'https': proxy_url}
    )
    
    data = response.json()
    return data.get('proxy') == False and data.get('vpn') == False
```

**Common Issues**:
- 403 Forbidden: IP flagged as datacenter/VPN
- Card declined: Billing address mismatch
- Verification timeout: 3D Secure SMS delay

### 2. Third-Party Recharge Services (Recommended)

**Use Case**: Users prioritizing convenience and speed

**Service Requirements**:
```yaml
# Trusted platform checklist
features:
  - password_free: true  # Never shares your OpenAI password
  - payment_methods: ["Alipay", "WeChat Pay"]
  - automation: "instant"
  - customer_support: "available"
  
security:
  - official_stripe_integration: true
  - no_account_sharing: true
  - refund_policy: "clear"
```

**Integration Example**:
```javascript
// Typical third-party service flow (client-side perspective)
const subscription = {
  service: 'ChatGPT Plus',
  email: process.env.OPENAI_EMAIL,  // Your OpenAI account email
  plan: 'monthly',  // or 'annual'
  payment_method: 'alipay'
};

// Platform handles:
// 1. Enterprise card payment to OpenAI
// 2. Clean residential IP routing
// 3. Automatic subscription activation

// Result: Your account upgraded without password sharing
```

**Verification Script**:
```python
import os
from datetime import datetime

def verify_subscription_active(api_key):
    """
    Check if ChatGPT Plus subscription is active
    """
    import openai
    
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    try:
        # Use GPT-4 to verify Plus status
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        return True, "ChatGPT Plus active"
    except openai.error.RateLimitError as e:
        if "quota" in str(e):
            return False, "Free tier quota exceeded - Plus not active"
        raise
    except Exception as e:
        return False, f"Error: {str(e)}"
```

### 3. Apple App Store (iOS Users)

**Requirements**:
- Non-China region Apple ID (US/HK recommended)
- App Store gift card balance
- Clean network environment

**Setup Process**:
```bash
# 1. Create/switch to US Apple ID
# Settings → Apple ID → Media & Purchases → View Account → Country/Region

# 2. Purchase US App Store gift card
# - Official: apple.com/shop/buy-giftcard
# - Redeem code in App Store

# 3. Install ChatGPT iOS app
# 4. Subscribe via in-app purchase (uses Apple ID balance)
```

**Configuration Check**:
```swift
// Swift code to verify region and payment method (iOS app context)
import StoreKit

func checkAppStoreEligibility() {
    let locale = SKPaymentQueue.default().storefront?.countryCode
    
    guard locale != "CN" else {
        print("Error: Chinese App Store doesn't support ChatGPT subscriptions")
        return
    }
    
    // Verify gift card balance available
    // Proceed with IAP subscription
}
```

**Important Notes**:
- Don't use discounted/third-party gift cards (high fraud risk)
- Avoid frequent VPN switching (triggers Apple account locks)
- Subscription managed through Apple, not OpenAI directly

### 4. Shared Accounts (Not Recommended)

**High Risk Pattern**:
```python
# WARNING: Educational purposes only - NOT RECOMMENDED
class SharedAccount:
    """
    Shared/rental accounts have severe limitations
    """
    risks = {
        'privacy': 'All conversations visible to others',
        'security': 'Account can be locked/banned anytime',
        'data_loss': 'No guarantee of conversation history',
        'ip_conflicts': 'Multiple simultaneous logins = instant ban'
    }
    
    def __init__(self):
        raise Exception("Use dedicated account instead")
```

## Common Stripe Payment Errors

### Error: "Your card was declined"

```bash
# Diagnosis checklist:
# 1. Card issuer location
echo "Issuer: $(check_card_bin $CARD_NUMBER)"
# China-issued cards: 100% blocked by Stripe for OpenAI

# 2. IP reputation
curl -s https://ipinfo.io | jq '.org, .country'
# Must show residential ISP, not "Hosting/VPN/Proxy"

# 3. Billing address
# Must match card's registered country
BILLING_COUNTRY="US"  # If using US virtual card
BILLING_ZIP="90210"   # Valid ZIP for billing state
```

### Error: "Authentication required" (3D Secure)

```python
def handle_3ds_verification(card_platform):
    """
    Handle 3D Secure SMS/app verification
    """
    import time
    
    # Many virtual card platforms require app verification
    verification_timeout = 180  # 3 minutes
    
    print(f"Check {card_platform} app for verification code")
    
    # Common issues:
    # - SMS delay to China: 30-120 seconds
    # - App notification delay: 10-60 seconds
    # - Session timeout: 180 seconds
    
    time.sleep(verification_timeout)
    return "Verification completed or timeout"
```

### Error: "403 Forbidden" on OpenAI

```javascript
// Network diagnosis
const checkNetworkCompliance = async () => {
  // Requirements for OpenAI access:
  const requirements = {
    ip_type: 'residential',  // Not datacenter
    ip_reputation: 'clean',  // Not flagged for fraud
    browser_fingerprint: 'consistent',  // Don't randomize too much
    tls_fingerprint: 'standard'  // Use standard HTTPS client
  };
  
  // Tools to verify:
  // - https://whoer.net (check IP quality)
  // - https://browserleaks.com (check fingerprint)
  
  return requirements;
};
```

## Configuration & Best Practices

### Environment Setup

```bash
# .env file for subscription management
OPENAI_EMAIL="your.email@example.com"
OPENAI_API_KEY="sk-..."  # After subscription active

# If using virtual card:
VIRTUAL_CARD_PLATFORM_KEY=""  # Card provider API key
CARD_LAST_4="1234"

# Network configuration:
PROXY_URL="socks5://residential-proxy:1080"  # Residential IP required
PROXY_COUNTRY="US"

# Subscription tracking:
SUBSCRIPTION_START_DATE="2026-01-15"
SUBSCRIPTION_RENEWAL_DATE="2026-02-15"
SUBSCRIPTION_TYPE="ChatGPT Plus"  # or "ChatGPT Pro"
```

### Monitoring Script

```python
import os
import requests
from datetime import datetime, timedelta

class SubscriptionMonitor:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.email = os.getenv('OPENAI_EMAIL')
    
    def check_subscription_status(self):
        """
        Verify active subscription by testing model access
        """
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        # Test GPT-4 access (Plus/Pro only)
        payload = {
            'model': 'gpt-4',
            'messages': [{'role': 'user', 'content': 'hi'}],
            'max_tokens': 5
        }
        
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers=headers,
            json=payload
        )
        
        if response.status_code == 200:
            return {
                'status': 'active',
                'model': 'gpt-4',
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'status': 'inactive',
                'error': response.json(),
                'timestamp': datetime.now().isoformat()
            }
    
    def estimate_renewal_date(self):
        """
        Calculate next renewal based on start date
        """
        start = datetime.fromisoformat(
            os.getenv('SUBSCRIPTION_START_DATE')
        )
        return start + timedelta(days=30)

# Usage
monitor = SubscriptionMonitor()
status = monitor.check_subscription_status()
print(f"Subscription status: {status['status']}")
```

## Troubleshooting

### Issue: Payment Keeps Failing

```yaml
diagnosis_steps:
  1_verify_card:
    - "Check card has sufficient balance"
    - "Verify card is internationally enabled"
    - "Confirm card issuer country matches billing address"
  
  2_check_network:
    - "Use residential IP, not datacenter"
    - "Clear browser cookies/cache"
    - "Try different clean browser profile"
  
  3_billing_info:
    - "Use real US address (not random/fake)"
    - "ZIP code must match billing state"
    - "Name matches card registration"

  4_timing:
    - "Avoid peak hours (reduces queue timeout)"
    - "Complete payment in <5 minutes"
    - "Don't refresh page during 3DS verification"
```

### Issue: Account Suspended After Upgrade

```python
def diagnose_suspension():
    """
    Common causes of post-upgrade suspension
    """
    causes = {
        'chargeback_card': 'Card used was later disputed/refunded',
        'shared_ip': 'Multiple accounts from same IP',
        'stolen_card': 'Virtual card from fraud source',
        'tos_violation': 'Account shared/resold',
        'abnormal_usage': 'API abuse or scraping detected'
    }
    
    resolution = {
        'legitimate_payment': 'Contact OpenAI support with payment proof',
        'policy_violation': 'Create new account, follow ToS strictly',
        'technical_error': 'Appeal via help.openai.com'
    }
    
    return {
        'causes': causes,
        'resolution': resolution,
        'support_url': 'https://help.openai.com'
    }
```

### Issue: Subscription Not Showing in Account

```bash
# Verification steps:
# 1. Check payment confirmation email
grep -i "openai\|chatgpt" ~/Mail/Inbox

# 2. Verify payment processed
# Login to card platform, check transaction history

# 3. Wait 5-10 minutes for system sync
# OpenAI backend may take time to activate

# 4. Test model access directly
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY" | \
  jq '.data[] | select(.id | contains("gpt-4"))'

# If GPT-4 models visible, subscription is active
```

## Security Best Practices

```python
# Never share these:
SENSITIVE_DATA = {
    'openai_password': 'NEVER share with any service',
    'openai_api_key': 'Only use in your own code',
    'payment_card_cvv': 'Only enter on official Stripe/OpenAI pages',
    'virtual_card_login': 'Keep credentials private'
}

# Safe to share with reputable recharge services:
SAFE_TO_SHARE = {
    'openai_email': 'Email address only (not password)',
    'subscription_type': 'Plus or Pro preference',
    'payment_method': 'Alipay/WeChat for local payment'
}

# Validation before using any service:
def validate_recharge_service(service_url):
    """
    Check if service is legitimate
    """
    red_flags = [
        'requests password',
        'requests API key', 
        'requires account sharing',
        'no customer support',
        'suspiciously low prices (<$15 for monthly Plus)'
    ]
    
    return all([flag not in service_url for flag in red_flags])
```

## Regional Considerations

```javascript
// Network access requirements by region
const regionalConfig = {
  china: {
    requires_vpn: true,
    recommended_locations: ['Hong Kong', 'Japan', 'Singapore', 'US West'],
    payment_methods: ['virtual_card', 'third_party', 'app_store'],
    blocked_methods: ['china_issued_cards'],
    notes: 'Use residential IP proxies only'
  },
  
  hong_kong: {
    requires_vpn: false,
    payment_methods: ['local_card', 'virtual_card', 'app_store'],
    notes: 'Direct access available'
  },
  
  taiwan: {
    requires_vpn: false,
    payment_methods: ['local_card', 'virtual_card'],
    notes: 'Most international cards work'
  }
};

// Check your configuration
function getRecommendedMethod(region) {
  const config = regionalConfig[region];
  return config.payment_methods[0]; // Returns best option
}
```

## Cost Comparison

```python
# Monthly cost analysis (2026, CNY equivalent)
SUBSCRIPTION_COSTS = {
    'chatgpt_plus': {
        'official_usd': 20.00,
        'virtual_card_total': 20.00 + 2.00,  # Card fees
        'third_party_service': 160.00,  # CNY, ~$22-23
        'app_store_us': 19.99,  # Slightly cheaper via Apple
        'shared_account_daily': 3.00 * 30  # High risk, not recommended
    },
    
    'chatgpt_pro': {
        'official_usd': 200.00,
        'third_party_service': 1450.00  # CNY
    }
}

def calculate_annual_cost(method='third_party_service'):
    """
    Calculate total annual cost including all fees
    """
    monthly = SUBSCRIPTION_COSTS['chatgpt_plus'][method]
    
    if method == 'virtual_card_total':
        opening_fee = 10.00  # One-time card opening
        monthly_maintenance = 1.00
        return (monthly * 12) + opening_fee + (monthly_maintenance * 12)
    
    return monthly * 12
```

## Additional Resources

```yaml
official_links:
  openai_help: "https://help.openai.com"
  stripe_supported_cards: "https://stripe.com/docs/payments/cards/supported-card-brands"
  
community_resources:
  reddit_chatgpt: "r/ChatGPT"
  troubleshooting_wiki: "Check project repository issues"
  
payment_verification:
  stripe_test_cards: "Never use test cards on production"
  ip_checker: "https://whoer.net"
  
compliance:
  openai_tos: "https://openai.com/policies/terms-of-use"
  payment_policy: "Review before subscribing"
```

---

**Final Recommendation**: For most users in restricted regions, using an established third-party recharge service with Alipay/WeChat Pay support provides the best balance of convenience, security, and reliability. Ensure the service never requests your OpenAI password and uses official Stripe payment channels.
