---
name: chatgpt-plus-subscription-guide
description: Guide for purchasing and managing ChatGPT Plus/Pro and Codex subscriptions from China mainland
triggers:
  - how do I subscribe to ChatGPT Plus from China
  - what are the payment methods for ChatGPT Plus in mainland China
  - how to buy ChatGPT Plus without a foreign credit card
  - ChatGPT Plus代充服务怎么用
  - stripe payment blocked for ChatGPT subscription
  - virtual credit card for OpenAI services
  - ChatGPT Plus upgrade tutorial for Chinese users
  - how to avoid ChatGPT subscription payment failures
---

# ChatGPT Plus/Pro Subscription Guide (China Mainland)

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

This skill provides guidance on subscribing to ChatGPT Plus, ChatGPT Pro, and Codex services from mainland China, where direct payment methods are restricted due to OpenAI's geographic and payment gateway limitations.

## Overview

This project documents the challenges Chinese users face when attempting to subscribe to OpenAI services and provides multiple solution paths:

1. **Payment Gateway Restrictions**: Stripe (OpenAI's payment processor) blocks mainland China-issued credit cards
2. **IP-based Fraud Detection**: Public VPN/proxy IPs trigger automatic fraud prevention
3. **3D Secure Verification**: Cross-border verification often fails for Chinese users

## Subscription Methods

### Method 1: Third-Party Top-Up Services (Recommended)

The most accessible method for non-technical users is using authorized top-up platforms.

**Recommended Platform**: [PayPrm.com](https://www.payprm.com/)

**Key Features**:
- No password required (proxy payment model)
- WeChat Pay/Alipay support
- Automated fulfillment
- Official Stripe payment channel

**Usage Flow**:
```bash
# Step 1: Visit the platform
# Navigate to: https://www.payprm.com/

# Step 2: Select service
# - ChatGPT Plus (Monthly)
# - ChatGPT Pro (Monthly)
# - Codex Subscription

# Step 3: Enter your OpenAI account email
# (DO NOT provide password)

# Step 4: Complete payment via WeChat/Alipay
# Payment in CNY, platform handles USD conversion

# Step 5: Wait for automatic upgrade (typically <5 minutes)
```

**Risk Assessment**:
- ✅ Security: High (no password sharing)
- ✅ Ban Risk: Minimal (official payment channel)
- ⚠️ Cost: Premium over official price (service fee + exchange rate)
- ⚠️ Dependency: Requires trusted third-party

### Method 2: Virtual Credit Cards

For technical users comfortable with cryptocurrency and KYC processes.

**Prerequisites**:
- Access to residential proxy/clean IP
- Cryptocurrency wallet (USDT recommended)
- Identity verification documents

**Common Virtual Card Providers**:
- Supports US billing address generation
- Card BINs typically 5405/5561 (Mastercard)

**Implementation Example**:
```bash
# Step 1: Obtain virtual card
# - Complete KYC on card platform
# - Fund card with USDT or other supported methods
# - Receive card details: number, CVV, expiry, billing address

# Step 2: Configure clean network environment
# Residential proxy configuration (example with Clash):
cat > ~/.config/clash/config.yaml <<EOF
proxies:
  - name: "US-Residential-01"
    type: http
    server: your-residential-proxy.com
    port: 8080
    username: $PROXY_USER
    password: $PROXY_PASS
EOF

# Step 3: Add payment method to ChatGPT
# Navigate to: https://platform.openai.com/account/billing
# Use card details with US billing address
# Complete 3D Secure verification if prompted

# Step 4: Subscribe to Plus/Pro
# Visit: https://chat.openai.com/
# Click "Upgrade to Plus" or "Upgrade to Pro"
```

**Environment Variables**:
```bash
export PROXY_USER="your-proxy-username"
export PROXY_PASS="your-proxy-password"
export VIRTUAL_CARD_NUMBER="card-number-from-provider"
export VIRTUAL_CARD_CVV="cvv-code"
export VIRTUAL_CARD_BILLING_ZIP="90210"  # Example US ZIP
```

**Common Pitfalls**:
- ❌ Using datacenter IPs (triggers Stripe fraud detection)
- ❌ Frequent IP changes during payment flow
- ❌ Mismatched billing address format
- ❌ Insufficient card balance for authorization hold

### Method 3: Apple App Store (iOS Users)

Leverages Apple's in-app purchase system to bypass Stripe.

**Prerequisites**:
- US or non-China Apple ID
- Access to US App Store gift cards

**Implementation**:
```bash
# Step 1: Create/switch to US Apple ID
# Settings → [Your Name] → Media & Purchases → Sign Out
# Sign in with US Apple ID

# Step 2: Redeem US gift card
# App Store → [Profile Icon] → Redeem Gift Card or Code
# Enter gift card code

# Step 3: Download ChatGPT app
# Search "ChatGPT" in US App Store
# Download official OpenAI app

# Step 4: Subscribe via in-app purchase
# Open ChatGPT app
# Tap "Upgrade to Plus"
# Complete purchase with Apple ID balance
```

**Limitations**:
- Higher price due to Apple's 30% commission
- Subscription managed through Apple (not transferable to web)
- Risk of Apple ID region lock if network behavior is suspicious

### Method 4: Shared/Temporary Accounts (Not Recommended)

**⚠️ Security Warning**: This method poses significant privacy and security risks.

**Characteristics**:
- Extremely low cost (daily/weekly rentals)
- Multiple users share single account
- Chat history visible to all users
- High ban probability
- Zero privacy protection

**Never Use For**:
- Company code/proprietary information
- Personal data processing
- Long-term projects
- Any production work

## Network Requirements

All methods require stable access to OpenAI services. Recommended proxy configurations:

```bash
# Example: Verify connectivity before subscription
curl -x socks5h://localhost:1080 https://chat.openai.com/api/auth/session

# Should return JSON response, not error
# If blocked, try different proxy server
```

**Residential Proxy Checklist**:
```bash
# Test IP reputation
curl -x http://proxy-server:port https://ipinfo.io/json

# Verify response shows:
# - "type": "hosting" ❌ (will be blocked)
# - "type": "isp" ✅ (residential, preferred)
# - Clean IP not in blacklists
```

## Subscription Comparison Table

| Method | Difficulty | Security | Cost | Ban Risk | Recommended For |
|--------|-----------|----------|------|----------|-----------------|
| Third-party (PayPrm) | ⭐☆☆☆☆ | ⭐⭐⭐⭐⭐ | 💰💰💰 | Low | General users |
| Virtual Card | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐☆ | 💰💰 | Medium | Tech-savvy users |
| App Store | ⭐⭐⭐☆☆ | ⭐⭐⭐⭐☆ | 💰💰💰💰 | Low | iOS ecosystem users |
| Shared Account | ⭐☆☆☆☆ | ⭐☆☆☆☆ | 💰 | Very High | Testing only |

## Troubleshooting

### Common Stripe Errors

**Error: "Your card was declined"**
```bash
# Causes:
# 1. Card BIN blocked for China region
# 2. Insufficient funds + authorization hold
# 3. 3D Secure verification failure

# Solutions:
# - Ensure card has $25+ balance (Plus needs $20 + hold)
# - Use residential proxy, clear cookies, retry
# - Contact card provider to enable international transactions
```

**Error: "We couldn't verify your payment method"**
```bash
# Causes:
# 1. IP mismatch (datacenter IP or frequent changes)
# 2. Billing address format incorrect
# 3. Card not activated for online purchases

# Solutions:
# - Use consistent residential IP throughout flow
# - Format address exactly as card provider specifies
# - Ensure card supports CNP (Card Not Present) transactions
```

**Error: "This card cannot be used for this payment"**
```bash
# Causes:
# 1. Card BIN explicitly blocked by Stripe
# 2. Velocity limits (too many attempts)

# Solutions:
# - Wait 24 hours before retry
# - Try different virtual card provider
# - Consider alternative subscription method
```

### Verification Loop Issues

```bash
# If stuck in endless 3D Secure verification:

# 1. Clear browser data
rm -rf ~/.cache/google-chrome
rm -rf ~/Library/Application\ Support/Google/Chrome  # macOS

# 2. Use private/incognito window
# 3. Disable browser extensions temporarily
# 4. Try different device (mobile vs desktop)
```

## Configuration Best Practices

### Proxy Setup for Payment Flow

```bash
# Example: Configure system-wide proxy for stable session
export http_proxy="http://residential-proxy:8080"
export https_proxy="http://residential-proxy:8080"
export PROXY_USER="username"
export PROXY_PASS="password"

# Start browser with consistent fingerprint
chromium --proxy-server="$http_proxy" \
         --user-data-dir="/tmp/chatgpt-session" \
         --disable-features=WebRtcHideLocalIpsWithMdns
```

### Environment Variables

```bash
# Virtual card payment environment
export CHATGPT_CARD_NUMBER="card-from-provider"
export CHATGPT_CARD_CVV="cvv-code"
export CHATGPT_CARD_EXP="MM/YY"
export CHATGPT_BILLING_ZIP="postal-code"
export CHATGPT_BILLING_COUNTRY="US"

# Proxy configuration
export CHATGPT_PROXY_HOST="residential-proxy-hostname"
export CHATGPT_PROXY_PORT="port-number"
export CHATGPT_PROXY_USERNAME="proxy-auth-user"
export CHATGPT_PROXY_PASSWORD="proxy-auth-pass"
```

## Platform-Specific Notes

### Windows Users

```powershell
# Set proxy via PowerShell
$env:HTTP_PROXY = "http://proxy:port"
$env:HTTPS_PROXY = "http://proxy:port"

# Verify connectivity
Invoke-WebRequest -Uri "https://chat.openai.com" -UseBasicParsing
```

### macOS Users

```bash
# System-wide proxy (GUI alternative)
# System Preferences → Network → Advanced → Proxies
# Enable "Web Proxy (HTTP)" and "Secure Web Proxy (HTTPS)"

# Verify from terminal
curl --proxy socks5h://localhost:1080 https://chat.openai.com
```

### Linux Users

```bash
# Add to ~/.bashrc or ~/.zshrc for persistence
cat >> ~/.bashrc <<'EOF'
export http_proxy="socks5h://localhost:1080"
export https_proxy="socks5h://localhost:1080"
EOF

source ~/.bashrc
```

## Security Considerations

**DO**:
- ✅ Use platforms that never ask for your OpenAI password
- ✅ Enable 2FA on your OpenAI account
- ✅ Use unique, strong passwords
- ✅ Verify platform HTTPS certificates
- ✅ Keep payment methods separate from primary accounts

**DON'T**:
- ❌ Share OpenAI credentials with any third party
- ❌ Use public/shared proxies for payment
- ❌ Store card details in plain text
- ❌ Use same password across services
- ❌ Trust platforms requiring account password

## Additional Resources

- Official OpenAI Billing: https://platform.openai.com/account/billing
- ChatGPT Subscription: https://chat.openai.com/
- Stripe Payment Status: https://stripe.com/docs/declines

## License

MIT License - See repository for details.
