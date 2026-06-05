# 📍 Where to Add Google Sheet Link

You have **3 options** to provide your Google Sheet URL:

---

## ✅ **OPTION 1: Command Line (Recommended)**

Pass the URL when running the script:

```bash
python batch_automation.py --sheet-url "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
```

**Pros:**
- ✅ No file editing needed
- ✅ Easy to change for different sheets
- ✅ Works immediately

---

## ✅ **OPTION 2: Add to .env File (Easiest)**

### Step 1: Edit `.env` file

Open `.env` in notepad and add your sheet URL:

```env
# Batch Automation: Google Sheet URL (for batch workflow)
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit
```

**Example:**
```env
FOODAMIGO_EMAIL=antlerdemo@tabless.io
FOODAMIGO_PASSWORD=UdV3B80OV7Hr
FOODAMIGO_RESTAURANT=HWY TO INDIA
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/1ABC123XYZ/edit

FOODAMIGO_HEADLESS=false
FOODAMIGO_TIMEOUT=30000
```

### Step 2: Run without --sheet-url

```bash
python batch_automation.py
```

It will automatically read from `.env`!

**Pros:**
- ✅ Set it once, use forever
- ✅ No need to type URL every time
- ✅ Cleaner command

---

## ✅ **OPTION 3: Create Batch File (Windows)**

### Create `run_automation.bat` file:

```batch
@echo off
python batch_automation.py --sheet-url "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
pause
```

### Then just double-click `run_automation.bat` to run!

**Pros:**
- ✅ One-click execution
- ✅ No command line needed
- ✅ Easy for non-technical users

---

## 🎯 **WHICH OPTION SHOULD I USE?**

### **If you always use the SAME sheet:**
→ Use **Option 2** (Add to `.env`)

### **If you switch between DIFFERENT sheets:**
→ Use **Option 1** (Command line)

### **If you want ONE-CLICK execution:**
→ Use **Option 3** (Batch file)

---

## 📝 **EXAMPLES**

### **Option 1 Example:**
```bash
# Google Docs version
python batch_automation.py --sheet-url "https://docs.google.com/spreadsheets/d/1ABC123/edit"

# Excel version
python batch_automation_excel.py --sheet-url "https://docs.google.com/spreadsheets/d/1ABC123/edit"

# Validation only
python batch_automation.py --sheet-url "https://docs.google.com/spreadsheets/d/1ABC123/edit" --validate-only
```

### **Option 2 Example:**

**Step 1:** Edit `.env`:
```env
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/1ABC123/edit
```

**Step 2:** Run:
```bash
python batch_automation.py
```

Done! 🎉

### **Option 3 Example:**

Create `run_automation.bat`:
```batch
@echo off
echo Starting Food Amigo Batch Automation...
python batch_automation.py --sheet-url "https://docs.google.com/spreadsheets/d/1ABC123/edit"
echo.
echo Automation complete!
pause
```

Double-click the file to run!

---

## ⚠️ **IMPORTANT NOTES**

### **URL Format:**
Always use the full URL including `/edit`:
```
✅ CORRECT: https://docs.google.com/spreadsheets/d/1ABC123XYZ/edit
❌ WRONG: 1ABC123XYZ (just the ID)
```

### **Quotes Required:**
When using command line, wrap URL in quotes:
```bash
✅ CORRECT: --sheet-url "https://docs.google.com/spreadsheets/..."
❌ WRONG: --sheet-url https://docs.google.com/spreadsheets/...
```

### **Priority:**
If you provide BOTH (command line AND .env):
- Command line takes priority
- .env is ignored

---

## 🆘 **TROUBLESHOOTING**

### "No Google Sheet URL provided!"

**Problem:** Neither command line nor .env has the URL

**Solution:**
```bash
# Either use command line:
python batch_automation.py --sheet-url "YOUR_URL"

# Or add to .env:
GOOGLE_SHEET_URL=YOUR_URL
```

### "Could not extract spreadsheet ID from URL"

**Problem:** URL format is wrong

**Solution:** Make sure URL includes `/spreadsheets/d/...`:
```
https://docs.google.com/spreadsheets/d/1ABC123/edit
                                    ^^^^^^^^^
                                    This part is required!
```

---

## 📂 **FILES TO EDIT**

- **Option 1:** No file editing (use command line)
- **Option 2:** Edit `.env` file (in project root)
- **Option 3:** Create `run_automation.bat` file (in project root)

---

**That's it! Choose the option that works best for you.** 🚀
