---
name: codex-auth-helper-chrome-extension
description: Chrome extension for securely exporting ChatGPT session credentials to generate Codex-compliant auth.json configuration files locally
triggers:
  - how do I export my ChatGPT credentials for Codex
  - help me install the Codex auth helper extension
  - generate auth.json from my ChatGPT session
  - extract ChatGPT authentication tokens locally
  - set up Codex authentication helper
  - how to backup ChatGPT session configuration
  - create auth.json file from browser session
  - install ChatGPT credential exporter
---

# Codex Auth Helper Chrome Extension

> Skill by [ara.so](https://ara.so) — Codex Skills collection.

## Overview

Codex Auth Helper is a Chrome extension that securely exports your logged-in ChatGPT session credentials and generates a Codex-compliant `auth.json` configuration file. All processing happens **100% locally** in the browser with no data sent to external servers.

**Key Features:**
- Automatic ChatGPT session detection
- Real-time token expiration countdown
- Synthetic JWT id_token generation for Codex authentication
- Local-only processing (no server uploads)
- Support for Free/Plus/Pro account types

## Installation

### Developer Mode Installation

1. Clone or download the repository:
```bash
git clone https://github.com/zhishile/codex-auth-helper.git
cd codex-auth-helper
```

2. Open Chrome and navigate to `chrome://extensions/`

3. Enable **Developer mode** (toggle in top-right corner)

4. Click **Load unpacked** (top-left)

5. Select the `extension` folder from the cloned repository

6. Pin the extension to your toolbar for easy access

### Verification

After installation, you should see the Codex Auth Helper icon in your Chrome toolbar. The extension requires these permissions:
- `downloads` - to save the generated auth.json file
- `https://chatgpt.com/*` - to read session credentials

## Usage

### Exporting auth.json

1. **Login to ChatGPT**: Navigate to [https://chatgpt.com/](https://chatgpt.com/) and ensure you're logged in

2. **Open Extension**: Click the Codex Auth Helper icon in your toolbar

3. **Verify Session**: The popup will automatically detect your session and display:
   - Your profile avatar
   - Email address
   - Subscription tier (Free/Plus/Pro)
   - Token expiration countdown

4. **Generate Config**: Click **"生成并保存 auth.json"** (Generate and Save auth.json)

5. **Download**: The file will automatically download to your default downloads folder

### auth.json Structure

The generated file follows this format:

```json
{
  "user": "your-email@example.com",
  "access_token": "eyJhbGc...",
  "id_token": "synthetic-jwt-token",
  "expires_at": 1234567890,
  "account_type": "plus"
}
```

**Fields:**
- `user`: Your ChatGPT account email
- `access_token`: Session access token from cookies
- `id_token`: Synthetically generated JWT for Codex authentication
- `expires_at`: Unix timestamp when the token expires
- `account_type`: `free`, `plus`, or `pro`

## Extension Architecture

### File Structure

```
extension/
├── manifest.json       # Extension configuration (Manifest V3)
├── popup.html         # UI interface
├── popup.js           # Frontend logic
├── background.js      # Service worker for token processing
├── styles.css         # Glassmorphism UI styling
└── icons/            # Extension icons
```

### Key Components

#### manifest.json

```json
{
  "manifest_version": 3,
  "name": "Codex 认证助手",
  "version": "1.0.0",
  "permissions": ["downloads"],
  "host_permissions": ["https://chatgpt.com/*"],
  "background": {
    "service_worker": "background.js"
  },
  "action": {
    "default_popup": "popup.html"
  }
}
```

#### Session Detection (popup.js pattern)

```javascript
// Check ChatGPT login status
async function checkAuthStatus() {
  try {
    const response = await fetch('https://chatgpt.com/api/auth/session');
    const data = await response.json();
    
    if (data.user) {
      // User is logged in
      displayUserInfo({
        email: data.user.email,
        avatar: data.user.image,
        accountType: data.user.account_type || 'free'
      });
    } else {
      // Show login prompt
      showLoginButton();
    }
  } catch (error) {
    console.error('Auth check failed:', error);
  }
}
```

#### Token Extraction (background.js pattern)

```javascript
// Extract tokens from cookies
chrome.cookies.getAll({
  domain: '.chatgpt.com'
}, (cookies) => {
  const accessToken = cookies.find(c => c.name === '__Secure-next-auth.session-token');
  
  if (accessToken) {
    // Generate synthetic JWT
    const syntheticToken = generateSyntheticJWT(accessToken.value);
    
    // Create auth.json structure
    const authConfig = {
      user: userEmail,
      access_token: accessToken.value,
      id_token: syntheticToken,
      expires_at: Math.floor(accessToken.expirationDate),
      account_type: accountType
    };
    
    // Trigger download
    downloadAuthFile(authConfig);
  }
});
```

#### Secure Local Download

```javascript
function downloadAuthFile(authData) {
  // Convert to JSON
  const jsonString = JSON.stringify(authData, null, 2);
  
  // Create data URL (no blob storage)
  const dataUrl = 'data:application/json;charset=utf-8,' + 
                  encodeURIComponent(jsonString);
  
  // Trigger download
  chrome.downloads.download({
    url: dataUrl,
    filename: 'auth.json',
    saveAs: true
  });
}
```

## Configuration

### Customizing Export Behavior

You can modify `popup.js` to customize the export behavior:

```javascript
// Custom filename with timestamp
const timestamp = new Date().toISOString().split('T')[0];
const filename = `auth_${timestamp}.json`;

chrome.downloads.download({
  url: dataUrl,
  filename: filename,
  saveAs: true // Set to false for automatic download
});
```

### Token Refresh Handling

```javascript
// Check token expiration
function checkTokenExpiry(expiresAt) {
  const now = Math.floor(Date.now() / 1000);
  const timeLeft = expiresAt - now;
  
  if (timeLeft < 3600) {
    // Less than 1 hour remaining
    showExpiryWarning('Token expires soon! Please re-login.');
  }
  
  // Update countdown display
  updateCountdown(timeLeft);
}
```

## Integration with Codex

### Using the Exported auth.json

After exporting, place `auth.json` in your Codex project directory:

```bash
# Typical Codex project structure
my-codex-project/
├── auth.json          # Place exported file here
├── codex.config.js
└── src/
```

### Environment Variable Alternative

For sensitive environments, convert auth.json to environment variables:

```bash
# .env
CODEX_USER=your-email@example.com
CODEX_ACCESS_TOKEN=eyJhbGc...
CODEX_ID_TOKEN=synthetic-jwt-token
CODEX_ACCOUNT_TYPE=plus
```

Then reference in your Codex configuration:

```javascript
// codex.config.js
module.exports = {
  auth: {
    user: process.env.CODEX_USER,
    access_token: process.env.CODEX_ACCESS_TOKEN,
    id_token: process.env.CODEX_ID_TOKEN,
    account_type: process.env.CODEX_ACCOUNT_TYPE
  }
};
```

## Troubleshooting

### Extension Not Detecting Session

**Problem:** Popup shows "Please login" even when logged into ChatGPT

**Solutions:**
1. Refresh the ChatGPT tab and reopen the extension
2. Clear ChatGPT cookies and re-login
3. Check if you're on the correct domain (`chatgpt.com` not `chat.openai.com`)
4. Verify extension has permission to access `https://chatgpt.com/*`

```javascript
// Debug session detection
chrome.cookies.getAll({domain: '.chatgpt.com'}, (cookies) => {
  console.log('Found cookies:', cookies.map(c => c.name));
});
```

### Token Expired Immediately

**Problem:** Generated auth.json shows token already expired

**Solution:** Re-login to ChatGPT to get fresh tokens:

```javascript
// Check cookie expiration before export
if (cookie.expirationDate && cookie.expirationDate < Date.now() / 1000) {
  alert('Session expired. Please re-login to ChatGPT.');
  return;
}
```

### Download Not Starting

**Problem:** "Generate and Save" button doesn't trigger download

**Solutions:**
1. Check Chrome download permissions
2. Verify `downloads` permission in manifest.json
3. Check browser console for errors:

```javascript
chrome.downloads.download({
  url: dataUrl,
  filename: 'auth.json',
  saveAs: true
}, (downloadId) => {
  if (chrome.runtime.lastError) {
    console.error('Download failed:', chrome.runtime.lastError);
  } else {
    console.log('Download started:', downloadId);
  }
});
```

### Permission Denied Errors

**Problem:** Extension can't read cookies or trigger downloads

**Solution:** Reinstall with correct permissions:

```json
{
  "permissions": ["downloads"],
  "host_permissions": ["https://chatgpt.com/*"],
  "optional_permissions": ["cookies"]
}
```

## Security Best Practices

### Safe Storage of auth.json

```bash
# Add to .gitignore
echo "auth.json" >> .gitignore

# Set restrictive permissions (Unix/Mac)
chmod 600 auth.json
```

### Verify Extension Integrity

Before using, verify the extension only contains expected files:

```bash
# Check for unexpected network requests
grep -r "fetch\|XMLHttpRequest" extension/
grep -r "http" extension/ | grep -v "chatgpt.com"
```

### Token Rotation

Implement automatic token refresh reminders:

```javascript
// Set up expiry notification
function scheduleExpiryCheck(expiresAt) {
  const checkTime = (expiresAt - Math.floor(Date.now() / 1000) - 3600) * 1000;
  
  setTimeout(() => {
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon128.png',
      title: 'Codex Auth Helper',
      message: 'Your ChatGPT token will expire soon. Please export a new auth.json.'
    });
  }, checkTime);
}
```

## Common Patterns

### Batch Export for Multiple Accounts

```javascript
// Export with account identifier
function exportWithIdentifier(email) {
  const sanitizedEmail = email.replace('@', '_at_').replace('.', '_');
  const filename = `auth_${sanitizedEmail}.json`;
  
  chrome.downloads.download({
    url: dataUrl,
    filename: filename,
    saveAs: false
  });
}
```

### Validation Before Export

```javascript
function validateAuthData(authData) {
  const required = ['user', 'access_token', 'id_token', 'expires_at'];
  
  for (const field of required) {
    if (!authData[field]) {
      throw new Error(`Missing required field: ${field}`);
    }
  }
  
  if (authData.expires_at < Date.now() / 1000) {
    throw new Error('Token already expired');
  }
  
  return true;
}
```

### Auto-Export on Login Detection

```javascript
// Monitor for login events
chrome.webNavigation.onCompleted.addListener((details) => {
  if (details.url.includes('chatgpt.com')) {
    checkAuthStatus().then((isLoggedIn) => {
      if (isLoggedIn) {
        // Optionally auto-export
        showNotification('ChatGPT session detected. Ready to export.');
      }
    });
  }
});
```
