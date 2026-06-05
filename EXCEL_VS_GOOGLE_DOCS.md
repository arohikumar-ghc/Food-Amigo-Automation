# Excel Files vs Google Docs - Which Should You Use?

You have **2 options** for batch automation:

---

## 📊 **Option 1: Keep Using Excel Files** (Easier Migration)

### What You Keep
- ✅ Your existing **Excel files** (.xlsx) with SEO data
- ✅ Same Excel structure you're already using
- ✅ Existing parser works as-is

### What Changes
- ✅ Google Sheet for **restaurant list** (instead of .env)
- ✅ Google Drive for **images** (instead of local folder)

### Google Sheet Structure (Option 1)

```
| Restaurant Name | Excel File Path                     | Image Folder          | No. of Pages | Completed | Last Run | Notes |
| HWY TO INDIA    | C:\Users\...\hwy-to-india.xlsx      | [Drive Folder URL]    | 100          | No        |          |       |
| Diyo Fusion     | C:\Users\...\diyo-fusion.xlsx       | [Drive Folder URL]    | 50           | No        |          |       |
```

**Column B = Local Excel file path** (not Google Doc URL)

### How to Run (Option 1)

```bash
python batch_automation_excel.py --sheet-url "YOUR_SHEET_URL"
```

### ✅ Pros
- Keep your existing Excel files
- No need to convert to Google Docs
- Faster migration

### ❌ Cons
- Excel files must be on local disk
- Can't edit files from anywhere (need local access)
- Harder to collaborate (share Excel files manually)

---

## 📄 **Option 2: Switch to Google Docs** (New System)

### What Changes
- ✅ Google Sheet for **restaurant list**
- ✅ **Google Docs** for page content (instead of Excel)
- ✅ Google Drive for **images**

### Google Sheet Structure (Option 2)

```
| Restaurant Name | Doc Link                              | Image Folder          | No. of Pages | Completed | Last Run | Notes |
| HWY TO INDIA    | https://docs.google.com/document/...  | [Drive Folder URL]    | 100          | No        |          |       |
| Diyo Fusion     | https://docs.google.com/document/...  | [Drive Folder URL]    | 50           | No        |          |       |
```

**Column B = Google Doc URL** (not local file path)

### How to Run (Option 2)

```bash
python batch_automation.py --sheet-url "YOUR_SHEET_URL"
```

### ✅ Pros
- Edit from anywhere (cloud-based)
- Easy collaboration (share Google Docs)
- No local file management
- Everything in Google ecosystem

### ❌ Cons
- Need to convert Excel → Google Doc format
- Different format (delimiter-based)

---

## 🔄 **How to Convert Excel → Google Doc**

If you choose **Option 2** and want to convert existing Excel files:

### Step 1: Run Converter

```bash
pip install openpyxl
python convert_excel_to_google_doc.py seo_pages.xlsx
```

This creates: `seo_pages_google_doc_format.txt`

### Step 2: Copy to Google Doc

1. Open the `.txt` file
2. Copy ALL content (Ctrl+A, Ctrl+C)
3. Create new Google Doc
4. Paste (Ctrl+V)
5. Review and fix any missing data

### Step 3: Use Google Doc URL

Copy the Google Doc URL and put it in your Google Sheet (column B).

---

## 🤔 **Which Option Should You Choose?**

### Choose **Option 1 (Excel)** if:
- ✅ You already have many Excel files ready
- ✅ You want to migrate quickly with minimal changes
- ✅ You're comfortable managing files locally
- ✅ You don't need to collaborate with others on content

### Choose **Option 2 (Google Docs)** if:
- ✅ You want everything cloud-based
- ✅ You need to edit content from anywhere
- ✅ You want to collaborate with team on content
- ✅ You're starting fresh (no existing Excel files)

---

## 📝 **Side-by-Side Comparison**

| Feature | Option 1 (Excel) | Option 2 (Google Docs) |
|---------|------------------|------------------------|
| **Content Storage** | Local Excel files | Google Docs (cloud) |
| **Restaurant List** | Google Sheet | Google Sheet |
| **Images** | Google Drive | Google Drive |
| **Edit Anywhere** | ❌ No (need local files) | ✅ Yes |
| **Collaboration** | ❌ Hard (share files) | ✅ Easy (share URLs) |
| **Migration Effort** | ✅ Low | ⚠️ Medium (convert) |
| **Format** | Excel rows/columns | Delimiter-based text |
| **Script to Run** | `batch_automation_excel.py` | `batch_automation.py` |

---

## 🚀 **Quick Start Examples**

### Option 1 (Excel) - Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 2. Setup Google APIs (for Sheets + Drive)
python setup_google_apis.py

# 3. Create Google Sheet with Excel file paths
# | Restaurant Name | Excel File Path | Image Folder URL | ...
# | HWY TO INDIA    | C:\path\to.xlsx | drive.google... | ...

# 4. Run automation
python batch_automation_excel.py --sheet-url "YOUR_SHEET_URL"
```

### Option 2 (Google Docs) - Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt
playwright install chromium

# 2. Setup Google APIs (for Sheets + Docs + Drive)
python setup_google_apis.py

# 3. Convert Excel to Google Doc (if you have Excel files)
python convert_excel_to_google_doc.py seo_pages.xlsx
# Copy output to Google Doc

# 4. Create Google Sheet with Google Doc URLs
# | Restaurant Name | Doc Link                | Image Folder URL | ...
# | HWY TO INDIA    | docs.google.com/doc...  | drive.google... | ...

# 5. Run automation
python batch_automation.py --sheet-url "YOUR_SHEET_URL"
```

---

## 💡 **My Recommendation**

**If you're just starting or have <10 restaurants:**
→ Use **Option 2 (Google Docs)** - Everything cloud-based, easier long-term

**If you already have 50+ Excel files ready:**
→ Use **Option 1 (Excel)** - Migrate faster, convert to Google Docs later if needed

**You can also mix both:**
- Start with Option 1 (Excel) for quick migration
- Convert to Option 2 (Google Docs) later for specific restaurants

---

## 🔧 **Files You Need**

### Option 1 (Excel)
- ✅ `batch_automation_excel.py` (created)
- ✅ Your existing Excel files (.xlsx)
- ✅ Google Sheet with restaurant list
- ✅ Google Drive folders with images

### Option 2 (Google Docs)
- ✅ `batch_automation.py` (created)
- ✅ Google Docs with page content (delimiter format)
- ✅ Google Sheet with restaurant list
- ✅ Google Drive folders with images

### Both Options Need
- ✅ `credentials.json` (Google API credentials)
- ✅ `token.json` (created on first auth)
- ✅ `.env` (Food Amigo login credentials)

---

## 📞 **Need Help?**

**For Option 1 (Excel):**
- Your existing Excel structure should work
- Column B in Google Sheet = local file path
- Run: `batch_automation_excel.py`

**For Option 2 (Google Docs):**
- See: `BATCH_AUTOMATION_GUIDE.md`
- Use: `GOOGLE_DOC_TEMPLATE.txt` for format
- Run: `batch_automation.py`

**To Convert Excel → Google Doc:**
- Run: `python convert_excel_to_google_doc.py your_file.xlsx`
- Copy output to Google Doc

---

**Choose the option that works best for you! Both are fully supported.** 🚀
