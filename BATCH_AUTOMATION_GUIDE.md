# Food Amigo Batch SEO Automation Guide

Complete guide for setting up and running batch automation across multiple restaurants.

---

## 📋 Table of Contents

1. [Setup](#setup)
2. [Google Sheet Structure](#google-sheet-structure)
3. [Google Doc Format](#google-doc-format)
4. [Image Folder Structure](#image-folder-structure)
5. [Running the Automation](#running-the-automation)
6. [Troubleshooting](#troubleshooting)

---

## 🚀 Setup

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
playwright install chromium
```

### Step 2: Google API Credentials

#### 2.1 Enable APIs

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Enable these APIs:
   - Google Sheets API
   - Google Docs API
   - Google Drive API

#### 2.2 Create OAuth2 Credentials

1. Go to **APIs & Services > Credentials**
2. Click **Create Credentials > OAuth client ID**
3. Application type: **Desktop app**
4. Download credentials
5. Save as `credentials.json` in project root

#### 2.3 First-Time Authentication

Run this command to authenticate (browser will open):

```bash
python google_sheet_handler.py
```

This creates `token.json` for future runs (no browser needed).

### Step 3: Food Amigo Credentials

Create `.env` file:

```env
FOODAMIGO_EMAIL=your-email@example.com
FOODAMIGO_PASSWORD=your-password
FOODAMIGO_RESTAURANT=dummy-value  # Will be overridden by sheet
```

**Note:** Restaurant name comes from Google Sheet, not `.env`.

---

## 📊 Google Sheet Structure

### Column Layout

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| Restaurant Name | Doc Link | Image Folder | No. of Pages | Completed | Last Run | Notes |

### Example Sheet

```
Restaurant Name    | Doc Link                               | Image Folder                          | No. of Pages | Completed | Last Run           | Notes
HWY TO INDIA       | https://docs.google.com/document/d/... | https://drive.google.com/drive/fo...  | 100          | No        |                    |
Diyo Fusion        | https://docs.google.com/document/d/... | https://drive.google.com/drive/fo...  | 50           | Yes       | 2026-06-05 10:30   | Completed: 50 pages
Hot Breads         | https://docs.google.com/document/d/... | https://drive.google.com/drive/fo...  | 75           | No        |                    |
```

### Column Descriptions

- **Restaurant Name**: Exact name as it appears in Food Amigo
- **Doc Link**: Full Google Doc URL containing all SEO pages
- **Image Folder**: Full Google Drive folder URL with images
- **No. of Pages**: Expected page count (for validation)
- **Completed**: Leave blank or "No" (automation updates to "Yes")
- **Last Run**: Automatically filled by automation
- **Notes**: Automatically filled with status/errors

### Sheet Setup

1. Create a new Google Sheet
2. Add header row with columns above
3. Share sheet with your Google account (same account as credentials.json)
4. Fill in restaurant data
5. Copy sheet URL for automation

---

## 📄 Google Doc Format

### Strict Template

Each restaurant has ONE Google Doc containing ALL SEO pages.

### Document Structure

```
=== PAGE START ===
Page Name: Butter Chicken
Href: /butter-chicken
SEO Title: Order Butter Chicken Online | HWY TO INDIA
SEO Description: Creamy butter chicken with aromatic spices. Order now for delivery.
Social Title: Order Butter Chicken Online | HWY TO INDIA
Social Description: Creamy butter chicken with aromatic spices. Order now for delivery.
Image: 001-butter-chicken.jpg
Subtitle: Authentic Indian Cuisine
Title: Butter Chicken
Description: Rich and creamy butter chicken made with traditional spices and fresh ingredients.
FAQ Question 1: Is butter chicken spicy?
FAQ Answer 1: Mild to medium spice level, suitable for most palates.
FAQ Question 2: Does it contain nuts?
FAQ Answer 2: Yes, contains cashew paste.
=== PAGE END ===

=== PAGE START ===
Page Name: Garlic Naan
Href: /garlic-naan
SEO Title: Fresh Garlic Naan Bread | HWY TO INDIA
SEO Description: Soft and fluffy garlic naan bread baked fresh to order.
Social Title: Fresh Garlic Naan Bread | HWY TO INDIA
Social Description: Soft and fluffy garlic naan bread baked fresh to order.
Image: 002-garlic-naan.jpg
Subtitle: Authentic Indian Breads
Title: Garlic Naan
Description: Hand-stretched naan bread topped with fresh garlic and butter.
FAQ Question 1: Is the naan vegetarian?
FAQ Answer 1: Yes, our naan is 100% vegetarian.
FAQ Question 2: How many naans per order?
FAQ Answer 2: Each order contains 2 naans.
=== PAGE END ===

... (repeat for all pages)
```

### Required Fields (Per Page)

✅ **Must have:**
- `Page Name` - Unique page name
- `Href` - URL path (e.g., `/butter-chicken`)
- `SEO Title` - Meta title for SEO
- `SEO Description` - Meta description for SEO
- `Social Title` - Open Graph title
- `Social Description` - Open Graph description
- `Image` - Filename (e.g., `001-butter-chicken.jpg`)
- `Subtitle` - Customizable section subtitle
- `Title` - Customizable section title
- `Description` - Customizable section description
- `FAQ Question 1` - At least one FAQ question
- `FAQ Answer 1` - At least one FAQ answer

✅ **Can have multiple FAQs:**
```
FAQ Question 1: ...
FAQ Answer 1: ...
FAQ Question 2: ...
FAQ Answer 2: ...
FAQ Question 3: ...
FAQ Answer 3: ...
```

### Important Rules

1. **Delimiters are EXACT**: `=== PAGE START ===` and `=== PAGE END ===`
2. **Field names are case-sensitive**: `Page Name` not `page name`
3. **Colons required**: `Page Name: Butter Chicken` (space after colon)
4. **Href must start with `/`**: `/butter-chicken` not `butter-chicken`
5. **Image filename matches Drive**: Case-insensitive but spelling must match

### Document Checklist

- [ ] All pages have START and END delimiters
- [ ] All required fields present for each page
- [ ] Image filenames match files in Drive folder
- [ ] Hrefs are unique (no duplicates)
- [ ] At least 1 FAQ per page

---

## 🖼️ Image Folder Structure

### Folder Setup

Each restaurant has a dedicated Google Drive folder containing all images.

### Naming Convention

```
001-butter-chicken.jpg
002-garlic-naan.jpg
003-paneer-tikka.jpg
004-biryani.jpg
...
100-mango-lassi.jpg
```

### Naming Rules

✅ **Format:** `{number}-{name}.{ext}`

- **Number**: 3 digits with leading zeros (001, 002, ..., 100)
- **Name**: Lowercase with hyphens (no spaces, no underscores)
- **Extension**: `.jpg`, `.jpeg`, `.png`, `.gif`, or `.webp`

✅ **Valid Examples:**
```
001-butter-chicken.jpg
042-garlic-naan.png
099-mango-lassi.jpg
```

❌ **Invalid Examples:**
```
1-naan.jpg              # Wrong: Not 3 digits
001 butter chicken.jpg  # Wrong: Has spaces
001_butter_chicken.jpg  # Wrong: Uses underscores
butterChicken.jpg       # Wrong: No number prefix
```

### Folder Permissions

1. Create folder in Google Drive
2. Upload all images
3. Share folder with your Google account (same as credentials.json)
4. Copy folder URL for Google Sheet

### Image Checklist

- [ ] All images follow naming convention
- [ ] Filenames match references in Google Doc
- [ ] Folder shared with correct Google account
- [ ] No duplicate filenames

---

## 🏃 Running the Automation

### Command Format

```bash
python batch_automation.py --sheet-url "YOUR_GOOGLE_SHEET_URL"
```

### Full Example

```bash
python batch_automation.py \
  --sheet-url "https://docs.google.com/spreadsheets/d/1ABC123XYZ.../edit" \
  --credentials credentials.json \
  --token token.json
```

### Validation-Only Mode

Test data without running automation:

```bash
python batch_automation.py \
  --sheet-url "YOUR_SHEET_URL" \
  --validate-only
```

This checks:
- ✅ All Google Docs accessible
- ✅ All Drive folders accessible
- ✅ All images downloadable
- ✅ Document structure valid
- ✅ Image references match files

### What Happens During Run

**Phase 1: Load Data**
- Reads Google Sheet
- Finds restaurants where `Completed != "Yes"`

**Phase 2: Validation**
- Downloads all images to local cache
- Parses all documents
- Verifies all image references exist
- Reports any errors

**Phase 3: Automation**
- Processes each validated restaurant sequentially
- For each restaurant:
  - Logs into Food Amigo
  - Selects restaurant
  - Creates all SEO pages
  - Skips pages that already exist (idempotent)
  - Updates Google Sheet with status

**Phase 4: Cleanup**
- Prints summary statistics
- Logs saved in `logs/batch_automation.log`

### Progress Monitoring

Watch the terminal output:

```
[1/3] Restaurant: HWY TO INDIA
  ✓ Validation passed
  → Processing 100 pages...
  [Page 1/100] Butter Chicken
    ✓ Page created successfully
  [Page 2/100] Garlic Naan
    ⊙ Page already exists, skipped
  ...

Waiting 30 seconds before next restaurant...

[2/3] Restaurant: Diyo Fusion
  ...
```

### Output Files

- `logs/batch_automation.log` - Detailed execution log
- `cache/{restaurant-name}/` - Downloaded images (kept for debugging)

---

## 🛠️ Troubleshooting

### Issue: "Authentication failed"

**Solution:**
```bash
# Delete token and re-authenticate
rm token.json
python google_sheet_handler.py
```

### Issue: "Restaurant not found in Food Amigo"

**Causes:**
- Restaurant name in sheet doesn't match Food Amigo exactly
- Case sensitivity issue
- Extra spaces in name

**Solution:**
1. Log into Food Amigo manually
2. Copy exact restaurant name from dropdown
3. Update Google Sheet with exact name

### Issue: "Image not found: 001-butter-chicken.jpg"

**Causes:**
- Filename mismatch (spelling, case, format)
- Image not in Drive folder
- Folder permissions wrong

**Solution:**
1. Check image exists in Drive folder
2. Verify filename matches exactly (case-insensitive but spelling must match)
3. Re-run validation: `python batch_automation.py --sheet-url "..." --validate-only`

### Issue: "Document parsing failed"

**Causes:**
- Missing delimiters (`=== PAGE START ===` / `=== PAGE END ===`)
- Missing required fields
- Typo in field names

**Solution:**
1. Open Google Doc
2. Verify all pages have START and END delimiters
3. Check all required fields present
4. Use template from this guide

### Issue: "Page creation failed"

**Causes:**
- Food Amigo UI changed
- Network timeout
- Browser crash

**Solution:**
1. Check logs: `logs/batch_automation.log`
2. Retry: Automation will skip pages that already exist
3. If persistent, report selector issue

### Issue: "Some pages created, some failed"

**Expected behavior:**
- Automation handles page-level errors gracefully
- Sheet updated with partial status
- Failed pages logged in Notes column

**Next steps:**
1. Check Notes column for specific errors
2. Fix issues (images, data)
3. Re-run: Already-created pages will be skipped

---

## 📈 Best Practices

### For 10-20 Restaurants

- Run sequentially (default)
- Monitor terminal output
- Use `--validate-only` first

### For 50+ Restaurants

- Run validation separately first
- Fix all validation errors before automation
- Run overnight (long duration)
- Check logs next day

### Data Preparation

1. ✅ Create template Google Doc with 1-2 pages
2. ✅ Validate template document structure
3. ✅ Upload images with correct naming
4. ✅ Test with 1 restaurant first
5. ✅ Once working, scale to all restaurants

### Error Recovery

- **Automation is idempotent**: Safe to re-run
- **Already-created pages skipped**: No duplicates
- **Fix errors and retry**: Failed restaurants can be retried

---

## 📞 Support

### Logs Location

All logs saved in `logs/` directory:
- `batch_automation.log` - Main log file
- `layout_selection.png` - Screenshot if layout selection fails

### Debugging

Enable debug logging:

```python
# In batch_automation.py, change:
level=logging.INFO
# to:
level=logging.DEBUG
```

---

## 🎯 Quick Start Checklist

- [ ] Install dependencies
- [ ] Create Google Cloud project
- [ ] Enable Google APIs (Sheets, Docs, Drive)
- [ ] Download `credentials.json`
- [ ] Authenticate (creates `token.json`)
- [ ] Create `.env` with Food Amigo credentials
- [ ] Create Google Sheet with restaurant data
- [ ] Create Google Docs with page content (use template)
- [ ] Upload images to Drive folders (correct naming)
- [ ] Run validation: `python batch_automation.py --sheet-url "..." --validate-only`
- [ ] Fix any validation errors
- [ ] Run automation: `python batch_automation.py --sheet-url "..."`
- [ ] Monitor progress
- [ ] Check Google Sheet for completion status

---

**Happy Automating! 🚀**
