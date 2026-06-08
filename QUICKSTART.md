# 🚀 Food Amigo Batch Automation - Quick Start

**Process 100+ restaurants automatically from Google Sheets!**

---

## ⚡ 5-Minute Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install chromium
```

### 2. Run Setup Wizard
```bash
python setup_google_apis.py
```

This will guide you through:
- ✅ Google API authentication
- ✅ Creating `.env` file
- ✅ Verifying credentials

### 3. Prepare Your Data

#### Create Google Sheet
```
| Restaurant Name | Doc Link           | Image Folder       | No. of Pages | Completed | Last Run | Notes |
| HWY TO INDIA    | [Google Doc URL]   | [Drive Folder URL] | 100          | No        |          |       |
```

#### Create Google Docs
- Copy template from `GOOGLE_DOC_TEMPLATE.txt`
- Fill in your pages using delimiter format
- Share doc with your Google account

#### Upload Images to Drive
- Create folder per restaurant
- Name images: `001-item-name.jpg`, `002-item-name.jpg`, etc.
- Share folder with your Google account

---

## 🎯 Run Automation

### Test with Validation
```bash
python batch_automation.py \
  --sheet-url "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit" \
  --validate-only
```

This checks:
- ✅ All docs accessible
- ✅ All images downloadable
- ✅ Document structure valid
- ✅ Image references match files

### Run Full Automation
```bash
python batch_automation.py \
  --sheet-url "https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit"
```

### Monitor Progress
Watch terminal output:
```
[1/3] Restaurant: HWY TO INDIA
  ✓ Validation passed
  [Page 1/100] Butter Chicken
    ✓ Page created successfully
  [Page 2/100] Garlic Naan
    ⊙ Page already exists, skipped
  ...
```

Check `logs/batch_automation.log` for details.

---

## 📖 Full Documentation

- **Setup Guide**: `BATCH_AUTOMATION_GUIDE.md` (comprehensive)
- **Doc Template**: `GOOGLE_DOC_TEMPLATE.txt` (copy-paste ready)
- **Implementation**: `IMPLEMENTATION_SUMMARY.md` (technical details)

---

## ✨ Key Features

✅ **Scalable**: Process 100+ restaurants  
✅ **Safe**: Idempotent (no duplicates on retry)  
✅ **Smart**: Pre-validation catches errors early  
✅ **Robust**: Continues despite page-level failures  
✅ **Tracked**: Auto-updates Google Sheet with status  

---

## 🆘 Common Issues

### "Authentication failed"
```bash
rm token.json
python setup_google_apis.py
```

### "Restaurant not found"
- Check restaurant name matches Food Amigo exactly
- Check for extra spaces or case differences

### "Image not found"
- Verify filename spelling matches doc
- Check image exists in Drive folder
- Re-run validation to see specific errors

---

## 📊 What Happens

1. **Load**: Read pending restaurants from sheet
2. **Validate**: Check all data (docs, images, structure)
3. **Automate**: Create pages for each validated restaurant
4. **Update**: Mark completed in sheet

---

## 🎉 Start Small, Scale Up

**First time?**
1. Start with 1 restaurant, 5 pages
2. Run validation
3. Fix any errors
4. Run automation
5. Verify pages created
6. **Then** scale to 100 restaurants!

---

**Need help? Check `BATCH_AUTOMATION_GUIDE.md` for full details!**
