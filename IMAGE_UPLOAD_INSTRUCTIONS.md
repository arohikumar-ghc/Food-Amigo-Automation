# Image Upload Feature - Installation Instructions

## Files Created

I've created two new files with all image upload features integrated:

1. **automation_updated.py** - Complete automation module with image upload
2. **main_updated.py** - Complete main script with folder creation

## How to Install

### Step 1: Backup Your Current Files (Recommended)
```bash
cp automation.py automation_backup.py
cp main.py main_backup.py
```

### Step 2: Replace with Updated Files
```bash
# On Windows (PowerShell or Command Prompt)
move automation_updated.py automation.py
move main_updated.py main.py
```

Or simply:
1. Delete your current `automation.py` and `main.py`
2. Rename `automation_updated.py` → `automation.py`
3. Rename `main_updated.py` → `main.py`

## Image Setup

### Folder Structure
```
Food Amigo Automation/
├── images/                          ← Create this folder
│   ├── blog page 1 image.jpg       ← Page 1 image
│   ├── blog page 2 image.png       ← Page 2 image
│   ├── blog page 3 image.jpg       ← Page 3 image
│   └── ...
├── automation.py                    ← Updated file
├── main.py                          ← Updated file
└── ...
```

### Image Naming Convention
- **Format:** `blog page {N} image.{jpg|png}`
- **Examples:**
  - `blog page 1 image.jpg` → Used for SEO Page 1
  - `blog page 2 image.png` → Used for SEO Page 2
  - `blog page 3 image.jpg` → Used for SEO Page 3

### Supported Formats
- `.jpg`
- `.png`

The script checks for `.jpg` first, then `.png`.

## What Changed

### automation.py Changes:
1. ✅ Added `_find_image_for_page_number()` helper method (line ~73)
2. ✅ Updated `create_seo_page()` signature to accept `page_num` parameter (line ~222)
3. ✅ Updated `_fill_social_metadata()` to accept `page_num` and upload image (line ~295)
4. ✅ Updated `_add_customizable_section()` to accept `page_num` and upload image (line ~359)
5. ✅ Added `navigate_to_dashboard()` method for multi-page support (line ~196)

### main.py Changes:
1. ✅ Added auto-creation of `images/` folder (line ~26-28)
2. ✅ Updated call to `automation.create_seo_page()` to pass `page_num` (line ~84)
3. ✅ Added call to `automation.navigate_to_dashboard()` before each page (line ~81)

## How Images Are Uploaded

Images are uploaded in **TWO locations** for each page:

1. **Customizable Section** - After Description field is filled
2. **Social Tab** - After Social Description field is filled

### Upload Process:
1. Script checks if `page_num` is provided
2. Looks for `images/blog page {N} image.jpg` or `.png`
3. If found: uploads via Playwright's `.set_input_files()`
4. If not found: logs "Image for Page X not found, skipping upload..." and continues

### Expected Log Output

**With image:**
```
→ Filling social metadata (Social tab)...
  → Uploading image for Page 1 in Social tab...
  ✓ Image uploaded in Social tab
→ Adding customizable section...
  → Uploading image for Page 1 in Customizable section...
  ✓ Image uploaded in Customizable section
```

**Without image:**
```
Image for Page 2 not found, skipping upload...
→ Filling social metadata (Social tab)...
  ✓ Social metadata saved
```

## Testing

1. Create the `images/` folder
2. Add one test image: `blog page 1 image.jpg`
3. Run your automation script
4. Check logs to confirm upload

## Troubleshooting

**Issue:** "Image for Page X not found"
- **Solution:** Check filename exactly matches `blog page {N} image.jpg` or `.png`
- Case-sensitive on Linux/Mac, not on Windows
- Space between "blog", "page", "{N}", and "image" is required

**Issue:** Upload fails with error
- **Solution:** Check the Playwright selector `input[type='file']` is correct
- May need to adjust selector if Food Amigo UI changes
- Error is caught and logged, script continues

**Issue:** Images folder not created
- **Solution:** Check write permissions in project directory
- Script logs: "Images directory ready: {path}"

## Rollback

If you need to revert to your old files:
```bash
cp automation_backup.py automation.py
cp main_backup.py main.py
```

## Notes

- ✅ No existing logic was changed
- ✅ All your current functionality is preserved
- ✅ Image upload is optional - script works fine without images
- ✅ Script won't crash if images are missing
- ✅ Detailed logging shows exactly what's happening

---

**Ready to use!** Just replace the files, create the images folder, add your images, and run the script. 🚀
