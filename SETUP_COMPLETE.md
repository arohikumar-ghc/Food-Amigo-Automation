# Complete Setup Guide

## Prerequisites Checklist

Before running batch automation, ensure all these are installed:

### ✓ 1. Python Environment
```bash
python --version  # Should be Python 3.8+
```

### ✓ 2. Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate  # Windows
```

### ✓ 3. Python Packages
```bash
pip install -r requirements.txt
```

### ⚠ 4. Playwright Browsers (REQUIRED!)
```bash
playwright install chromium
```

**Why?** Playwright needs actual browser binaries to automate web interactions.

**Size:** ~300MB download for Chromium

**Location:** `C:\Users\<YourUser>\AppData\Local\ms-playwright\`

**Common Error if missing:**
```
BrowserType.launch: Executable doesn't exist at C:\Users\...\chromium-1161\chrome-win\chrome.exe
```

### ✓ 5. Google API Credentials

**Files needed:**
- `credentials.json` - OAuth2 credentials from Google Cloud Console
- `token.json` - Generated after running authentication

**To generate token with correct scopes:**
```bash
python regenerate_token.py
```

### ✓ 6. Environment Variables

**File:** `.env`

```bash
# Food Amigo credentials
FOODAMIGO_EMAIL=your-email@example.com
FOODAMIGO_PASSWORD=your-password

# Google Sheet URL
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit

# Optional settings
FOODAMIGO_HEADLESS=false
FOODAMIGO_TIMEOUT=30000
```

## Installation Steps

### Step 1: Clone/Download Project
```bash
cd "C:\Users\Arohi\Desktop\Food Amigo Automation"
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/Scripts/activate
```

### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Install Playwright Browsers ⚠ IMPORTANT
```bash
playwright install chromium
```

**This step is crucial!** Without it, the automation will fail immediately when trying to launch the browser.

### Step 5: Setup Google Credentials

1. Download `credentials.json` from Google Cloud Console
2. Place it in the project root
3. Generate token:
   ```bash
   python regenerate_token.py
   ```
4. Follow browser prompts to authenticate

### Step 6: Configure Environment
```bash
cp .env.example .env
# Edit .env with your credentials
```

### Step 7: Test Setup
```bash
# Check Google Sheet connection
python diagnose_sheet.py

# Check Google Doc access
python test_doc_access.py

# Validate restaurant data
python batch_automation.py --validate-only
```

### Step 8: Run Automation
```bash
python batch_automation.py
```

## Verification Commands

Run these to verify everything is set up correctly:

```bash
# 1. Check Python version
python --version

# 2. Check virtual environment is active
which python  # Should show venv path

# 3. Check Playwright installation
playwright --version

# 4. Check Playwright browsers
playwright show-trace  # Opens Playwright inspector (if browsers installed)

# 5. Check credentials
ls -l credentials.json token.json

# 6. Check environment variables
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(f'Email: {os.getenv(\"FOODAMIGO_EMAIL\")}'); print(f'Sheet: {os.getenv(\"GOOGLE_SHEET_URL\")}')"

# 7. Test Google APIs
python diagnose_sheet.py

# 8. Validate data
python batch_automation.py --validate-only
```

## Common Setup Issues

### Issue: "playwright: command not found"
**Solution:**
```bash
source venv/Scripts/activate  # Ensure venv is active
pip install playwright
playwright install chromium
```

### Issue: "Executable doesn't exist at ...chromium..."
**Solution:**
```bash
playwright install chromium
```

### Issue: "No module named 'dotenv'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue: "credentials.json not found"
**Solution:**
1. Go to Google Cloud Console
2. Create OAuth2 credentials
3. Download as `credentials.json`
4. Place in project root

### Issue: "Request had insufficient authentication scopes"
**Solution:**
```bash
python regenerate_token.py
```

### Issue: "HTTP 403" or "HTTP 404" on Google Doc
**Solution:**
- Ensure document exists
- Share document with your Google account
- Verify URL in Google Sheet is correct

## Ready to Run Checklist

Before running `python batch_automation.py`, verify:

- [ ] Virtual environment is active (`venv` in prompt)
- [ ] `pip list` shows all required packages
- [ ] `playwright install chromium` has completed
- [ ] `credentials.json` exists in project root
- [ ] `token.json` exists (generated via `regenerate_token.py`)
- [ ] `.env` file configured with correct credentials
- [ ] `python diagnose_sheet.py` shows your restaurants
- [ ] `python batch_automation.py --validate-only` passes

## System Requirements

**Operating System:**
- Windows 10/11
- macOS 10.15+
- Linux (Ubuntu 20.04+)

**Python:**
- Version 3.8 or higher
- Virtual environment support

**Disk Space:**
- ~500MB for Playwright browsers
- ~50MB for Python packages
- ~100MB for image cache (per restaurant)

**Internet:**
- Required for Google API calls
- Required for downloading images
- Required for Food Amigo access

**Browser:**
- Playwright installs its own Chromium
- No need for Chrome/Firefox/Edge

## Next Steps

Once setup is complete:

1. **Validate:** `python batch_automation.py --validate-only`
2. **Run:** `python batch_automation.py`
3. **Monitor:** `tail -f logs/batch_automation.log`
4. **Check Results:** View updated Google Sheet

---

**Need help?** Run diagnostic tools:
- `python diagnose_sheet.py` - Check sheet data
- `python test_doc_access.py` - Check doc access
- `python list_drive_images.py` - Check images

**Documentation:**
- `QUICK_FIX_GUIDE.md` - Common issues and solutions
- `TROUBLESHOOTING.md` - Detailed troubleshooting
- `VALIDATION_SUCCESS.md` - Post-validation guide
- `README_BATCH.md` - Complete batch automation docs
