# Troubleshooting Guide

## Issue 1: Unicode Encoding Errors (FIXED ✓)

### Problem
When running `batch_automation.py`, you were seeing Unicode encoding errors like:
```
UnicodeEncodeError: 'charmap' codec can't encode character '→' in position 62
```

This was caused by Windows console (cp1252 encoding) not being able to display Unicode characters (→, ✓, ✗) used in log messages.

### Solution
**Fixed in commit**: The logging setup now forces UTF-8 encoding for console output.

**Files updated:**
- `batch_automation.py` - Added UTF-8 encoding for console handler
- `batch_automation_excel.py` - Added UTF-8 encoding for console handler

The scripts now work correctly on Windows with Unicode characters displaying properly.

---

## Issue 2: Insufficient Authentication Scopes (ACTION REQUIRED ⚠)

### Problem
```
HttpError 403: Request had insufficient authentication scopes
ACCESS_TOKEN_SCOPE_INSUFFICIENT
```

Your `token.json` only has the **Sheets scope**, but batch automation needs **Docs and Drive scopes** too.

**Current scopes in token.json:**
- ✓ `spreadsheets` (for reading restaurant list)

**Missing scopes:**
- ✗ `documents.readonly` (for reading Google Docs)
- ✗ `drive.readonly` (for downloading images)

### Solution: Regenerate Token

Run this script to create a new token with all required scopes:
```bash
python regenerate_token.py
```

This will:
1. Backup your old `token.json` to `token.json.bak`
2. Open your browser to re-authenticate
3. Create a new `token.json` with all required permissions

After regenerating the token, run validation again:
```bash
python batch_automation.py --validate-only
```

---

## Issue 3: Google Doc Access Issues

### Problem
After fixing the token scopes, you might still see:
```
ERROR - Failed to download document: Failed to download doc: HTTP 404
```

The Google Doc ID `1G4JqWbPXmYrhfyWj6QEGZEvQELnpyS1hU5CNdU5kkPc` from your Google Sheet may not exist or be accessible.

### Diagnosis
Run the diagnostic script to check your sheet data:
```bash
python diagnose_sheet.py
```

This will show you:
- All restaurants in the sheet
- Their Google Doc links and IDs
- Their Google Drive folder links and IDs
- Current status and any issues

### Possible Causes

1. **Document doesn't exist**
   - The document was deleted
   - The URL is incorrect
   - Solution: Create the document or update the sheet with the correct URL

2. **Permission denied**
   - The service account doesn't have access to the document
   - Solution: Share the document with the email address from your `credentials.json`

3. **Using wrong workflow**
   - Your sheet notes say: "Failed: Excel file not found: hyw to india"
   - This suggests you may have been using the Excel-based workflow
   - Solution: Use `batch_automation_excel.py` instead of `batch_automation.py`

### Solutions

#### Option A: Use Google Docs (current setup)
1. Create or fix the Google Doc for "HWY TO INDIA"
2. Share it with the service account email
3. Update the Google Sheet with the correct Doc URL
4. Run: `python batch_automation.py --validate-only`

#### Option B: Use Excel files (alternative)
1. Place Excel files in a local directory
2. Update your Excel file paths in the sheet
3. Run: `python batch_automation_excel.py --validate-only`

---

## How to Check What's in Your Google Sheet

Run this command to see all restaurant data:
```bash
python diagnose_sheet.py
```

Example output:
```
[1] HWY TO INDIA
----------------------------------------------------------------------
  Doc Link:       https://docs.google.com/document/d/1G4Jq.../edit
  Doc ID:         1G4JqWbPXmYrhfyWj6QEGZEvQELnpyS1hU5CNdU5kkPc
  Image Folder:   https://drive.google.com/drive/folders/1wuA-.../
  Folder ID:      1wuA-90cxcn8bV9Avj2-pBbk9Chjf1dnq
  No. of Pages:   2
  Completed:      No
  Last Run:       2026-06-05 16:00:38
  Is Pending:     True
  Notes:          Failed: Excel file not found: hyw to india
```

---

## Next Steps

1. **Verify your Google Doc exists:**
   - Open this URL in your browser: `https://docs.google.com/document/d/1G4JqWbPXmYrhfyWj6QEGZEvQELnpyS1hU5CNdU5kkPc/edit`
   - If it says "404", the document doesn't exist - you need to create it or update the sheet

2. **Share the document with your service account:**
   - Open `credentials.json` and find the `client_email` field
   - Share the Google Doc with that email address
   - Give it "Viewer" or "Editor" permissions

3. **Run validation again:**
   ```bash
   python batch_automation.py --validate-only
   ```

4. **If still failing, try Excel workflow:**
   ```bash
   python batch_automation_excel.py --validate-only
   ```

---

## Common Commands

```bash
# Check what's in your Google Sheet
python diagnose_sheet.py

# Validate restaurants (Google Docs workflow)
python batch_automation.py --validate-only

# Validate restaurants (Excel workflow)
python batch_automation_excel.py --validate-only

# Run full automation (Google Docs)
python batch_automation.py

# Run full automation (Excel)
python batch_automation_excel.py
```

---

## Getting Help

If you're still stuck:
1. Check the diagnostic output from `diagnose_sheet.py`
2. Verify the Google Doc URL is correct and accessible
3. Make sure the service account has permissions to the document
4. Check the logs in `logs/batch_automation.log` for detailed errors
