# Quick Fix Guide - Batch Automation Issues

## TL;DR - What You Need to Do

Your batch automation is failing because **your authentication token doesn't have the right permissions**. Follow these steps:

### Step 1: Regenerate Token (REQUIRED ⚠)
```bash
python regenerate_token.py
```

This will:
- Open your browser for Google authentication
- Ask you to grant permissions to read Sheets, Docs, and Drive
- Create a new `token.json` with full permissions

### Step 2: Test Access
```bash
python test_doc_access.py
```

This will verify you can access the Google Doc from your sheet.

### Step 3: Run Validation
```bash
python batch_automation.py --validate-only
```

This will validate all restaurant data without running the automation.

### Step 4: Run Full Automation
```bash
python batch_automation.py
```

---

## What Was Wrong?

### ✓ FIXED: Unicode Encoding Errors
**Problem:** Windows console couldn't display Unicode characters (→, ✓, ✗)
**Solution:** Applied UTF-8 encoding fix to all logging handlers
**Status:** ✓ Fixed in batch_automation.py and batch_automation_excel.py

### ⚠ ACTION REQUIRED: Insufficient Token Scopes
**Problem:** Your `token.json` only has Sheets scope, but needs Docs + Drive too
**Solution:** Run `python regenerate_token.py` to get a new token
**Status:** ⚠ Needs your action

**Why this happened:**
- You probably ran the sheet handler first, which only needs Sheets scope
- The token was saved with just that one scope
- Now when trying to read Docs, Google API rejects it (403 Forbidden)

**What scopes are needed:**
```
✓ spreadsheets          - Read restaurant list from Google Sheets
✗ documents.readonly    - Read page content from Google Docs (MISSING!)
✗ drive.readonly        - Download images from Google Drive (MISSING!)
```

---

## Detailed Steps

### 1. Regenerate Authentication Token

```bash
cd "C:\Users\Arohi\Desktop\Food Amigo Automation"
python regenerate_token.py
```

**What happens:**
1. Script backs up your old token to `token.json.bak`
2. Browser opens to Google authentication page
3. You'll be asked to grant permissions:
   - ✓ "See, edit, create, and delete all your Google Sheets spreadsheets"
   - ✓ "See all your Google Docs documents"
   - ✓ "See and download all your Google Drive files"
4. After approval, new `token.json` is created

**Important:** Use the **same Google account** that has access to your restaurant sheets and docs!

### 2. Verify Document Access

```bash
python test_doc_access.py
```

**Expected output if successful:**
```
✓ SUCCESS! Document is accessible.

Document Title: HWY TO INDIA SEO Pages
Document ID: 1G4JqWbPXmYrhfyWj6QEGZEvQELnpyS1hU5CNdU5kkPc
```

**If it fails with 404:**
- The document doesn't exist or was deleted
- Open the URL in your browser to verify:
  https://docs.google.com/document/d/1G4JqWbPXmYrhfyWj6QEGZEvQELnpyS1hU5CNdU5kkPc/edit
- If it doesn't open, you need to create the document or update the sheet URL

### 3. Check Your Sheet Data

```bash
python diagnose_sheet.py
```

This shows exactly what's in your Google Sheet, including:
- Restaurant names
- Google Doc URLs and IDs
- Google Drive folder URLs and IDs
- Current status and any issues

### 4. Run Validation (Dry Run)

```bash
python batch_automation.py --validate-only
```

This validates everything **without running automation**:
- ✓ Checks all Google Docs are accessible
- ✓ Checks all images exist in Drive folders
- ✓ Validates document structure and required fields
- ✓ Shows you what would be processed

**Expected output:**
```
PHASE 2: VALIDATION
----------------------------------------------------------------------
[1/1] Validating HWY TO INDIA...
✓ Google Doc parsed successfully
✓ Found 2 pages
✓ All required fields present
✓ Hero images found
✓ Gallery images found

VALIDATION SUMMARY
----------------------------------------------------------------------
✓ Passed: 1
✗ Failed: 0
```

### 5. Run Full Automation

Once validation passes, run the full automation:

```bash
python batch_automation.py
```

This will:
1. Validate all data
2. Process each pending restaurant:
   - Parse Google Doc
   - Download images from Drive
   - Log into Food Amigo
   - Create SEO pages
   - Upload images
3. Update Google Sheet with results

---

## Common Issues and Solutions

### "Request had insufficient authentication scopes"
**Cause:** Token doesn't have all required permissions
**Fix:** Run `python regenerate_token.py`

### "HTTP 404" when accessing document
**Cause:** Document doesn't exist or URL is wrong
**Fix:** 
1. Check the URL in your browser
2. Update the Google Sheet with correct URL
3. Ensure document is accessible by your Google account

### "HTTP 403" (Forbidden)
**Cause:** You don't have permission to access the document/folder
**Fix:**
1. Ensure document/folder is shared with you
2. Or ensure you own the document/folder
3. Use the same Google account for authentication

### Unicode encoding errors (✓, ✗, → not showing)
**Cause:** Windows console encoding issue
**Status:** ✓ Already fixed in the code

---

## File Overview

**Main Scripts:**
- `batch_automation.py` - Main batch processor (Google Docs workflow)
- `batch_automation_excel.py` - Alternative Excel workflow

**Diagnostic Tools:**
- `diagnose_sheet.py` - Shows what's in your Google Sheet
- `test_doc_access.py` - Tests if you can access the Google Doc
- `regenerate_token.py` - Fixes authentication token scopes

**Documentation:**
- `TROUBLESHOOTING.md` - Detailed troubleshooting guide
- `QUICK_FIX_GUIDE.md` - This file (quick reference)
- `README_BATCH.md` - Complete batch automation documentation

---

## Still Having Issues?

1. Check the logs: `logs/batch_automation.log`
2. Run diagnostics: `python diagnose_sheet.py`
3. Verify authentication: `python test_doc_access.py`
4. Check Google Sheet structure matches expected format:
   - Column A: Restaurant Name
   - Column B: Google Doc URL
   - Column C: Image Folder URL
   - Column D: Number of Pages
   - Column E: Completed (Yes/No)
   - Column F: Last Run
   - Column G: Notes

---

## Next Steps After Fix

Once everything is working:

1. **Validate first** (always!)
   ```bash
   python batch_automation.py --validate-only
   ```

2. **Run automation**
   ```bash
   python batch_automation.py
   ```

3. **Check results** in Google Sheet:
   - "Completed" column updated to "Yes"
   - "Last Run" timestamp updated
   - "Notes" shows success/error details

4. **Review logs** for any warnings:
   ```bash
   tail -f logs/batch_automation.log
   ```

Happy automating! 🚀
