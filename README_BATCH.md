# 🎯 Food Amigo Batch SEO Automation

**Automated SEO page creation for 100+ restaurants from Google Sheets**

---

## 📚 Documentation Index

Start here based on your needs:

### 🚀 **First Time Setup**
→ **[QUICKSTART.md](QUICKSTART.md)** - 5-minute setup guide

### 📖 **Complete Guide**
→ **[BATCH_AUTOMATION_GUIDE.md](BATCH_AUTOMATION_GUIDE.md)** - Full documentation
- Setup instructions
- Google Sheet structure
- Google Doc format
- Image folder structure
- Running automation
- Troubleshooting

### 📋 **Templates**
→ **[GOOGLE_DOC_TEMPLATE.txt](GOOGLE_DOC_TEMPLATE.txt)** - Copy-paste template for Google Docs

### 🔧 **Technical Details**
→ **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Architecture and implementation

---

## ⚡ Quick Command Reference

```bash
# Setup (first time only)
python setup_google_apis.py

# Validate data before automation
python batch_automation.py --sheet-url "YOUR_SHEET_URL" --validate-only

# Run full automation
python batch_automation.py --sheet-url "YOUR_SHEET_URL"
```

---

## 🎯 What It Does

1. **Reads** Google Sheet with restaurant list
2. **Validates** all data (docs, images, structure)
3. **Creates** SEO pages for each restaurant automatically
4. **Updates** Google Sheet with completion status

---

## ✨ Key Features

- ✅ **Scale**: Process 100+ restaurants
- ✅ **Safe**: Idempotent (no duplicates on retry)
- ✅ **Smart**: Pre-validation catches errors early
- ✅ **Robust**: Continues despite page-level failures
- ✅ **Tracked**: Auto-updates status in Google Sheet

---

## 📊 Data Flow

```
Google Sheet (restaurants)
    ↓
Google Docs (page content)
    ↓
Google Drive (images)
    ↓
Validation Phase
    ↓
Food Amigo Automation
    ↓
Status Update (back to sheet)
```

---

## 📁 Project Structure

```
Core Modules:
├── batch_automation.py        - Main orchestrator
├── google_sheet_handler.py    - Read/write Google Sheets
├── google_doc_parser.py       - Parse Google Docs
├── google_drive_handler.py    - Download images
├── validator.py               - Pre-validation phase
├── automation.py              - Food Amigo Playwright automation
├── models.py                  - Data models (SEOPageData, FAQ)
└── config.py                  - Configuration management

Setup:
├── setup_google_apis.py       - Interactive setup wizard
└── requirements.txt           - Dependencies

Documentation:
├── QUICKSTART.md              - Quick start guide
├── BATCH_AUTOMATION_GUIDE.md  - Complete guide
├── GOOGLE_DOC_TEMPLATE.txt    - Google Doc template
├── IMPLEMENTATION_SUMMARY.md  - Technical details
└── README_BATCH.md            - This file
```

---

## 🎓 Workflow

### Phase 1: Load Data
- Read Google Sheet
- Find pending restaurants (Completed != "Yes")

### Phase 2: Validation
- Download all images to local cache
- Parse all documents
- Verify all image references exist
- Check document structure

### Phase 3: Automation
- Login to Food Amigo
- Select restaurant
- Create all SEO pages
- Skip existing pages (idempotent)

### Phase 4: Update Status
- Mark completed in Google Sheet
- Add notes with details/errors

---

## 🛡️ Error Handling

**Restaurant-level errors** (skip restaurant):
- Login failed
- Restaurant not found
- Doc not accessible
- Drive folder not accessible

**Page-level errors** (skip page, continue):
- Missing required field
- Image not found
- Upload timeout

**Image-level errors** (create page without image):
- Image upload fails after retry

---

## 📈 Scalability

**Current (10-100 restaurants):**
- Sequential processing
- Local image cache
- Pre-validation
- ~30 seconds per page
- ~50 minutes per 100-page restaurant

**Future (100+ restaurants):**
- Parallel processing (3-5 instances)
- SQLite for page tracking
- Cloud storage (S3) for images

---

## 🎯 Start Here

1. **Read**: [QUICKSTART.md](QUICKSTART.md)
2. **Setup**: Run `python setup_google_apis.py`
3. **Prepare**: Create sheet, docs, images
4. **Validate**: Test with `--validate-only`
5. **Run**: Full automation
6. **Scale**: Add more restaurants!

---

## 📞 Support

- Check logs: `logs/batch_automation.log`
- Review guide: [BATCH_AUTOMATION_GUIDE.md](BATCH_AUTOMATION_GUIDE.md)
- See templates: [GOOGLE_DOC_TEMPLATE.txt](GOOGLE_DOC_TEMPLATE.txt)

---

**Built with ❤️ for scale. Process 100+ restaurants effortlessly!**
