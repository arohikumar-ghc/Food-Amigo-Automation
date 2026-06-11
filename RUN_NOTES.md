# Updated: Layout 6 Selection + Image Upload

## Changes Made

### 1. Improved Layout 6 Selection (3 Strategies)
The automation now tries multiple methods to select Layout 6:

**Strategy 1:** Click the image directly
```python
img[src*="customizable/6.png"]
```

**Strategy 2:** Click the card containing both h6 and image
```python
div containing h6="6" AND img[src*="customizable/6.png"]
```

**Strategy 3:** Click the h6 element
```python
h6:text-is("6")
```

### 2. Added Image Upload for Customizable Section
After selecting Layout 6, the automation now:
1. Switches to the "Background" tab
2. Finds the file input
3. Uploads the hero image from the cache
4. Switches back to "General" tab

## HTML Structure (from your inspection)
```html
<div class="border-brand-primary">  <!-- Selected layout has this class -->
  <div>
    <h6>6</h6>
    <span class="ant-tag">image</span>
    <button>...</button>  <!-- Radio button -->
  </div>
  <div>
    <img src="https://.../customizable/6.png" />
  </div>
</div>
```

## To Test the Fix

### Option 1: Run full automation
```bash
python batch_automation.py
```

This will:
- Validate all restaurants
- Process each one
- **Try to select Layout 6** (with 3 fallback strategies)
- **Upload the hero image** (if available)
- Create FAQ section
- Update Google Sheet

### Option 2: Test just one restaurant
First, mark other restaurants as "Completed" in your Google Sheet, then run:
```bash
python batch_automation.py --validate-only  # Check first
python batch_automation.py                   # Run automation
```

## Expected Results

### Success Case
```
✓ Layout 6 selected (clicked image)
✓ Image uploaded: lamb-vindaloo-lancaster-pa.png
✓ Customizable section added
```

### Fallback Case (if image selector fails)
```
⚠ Strategy 1 failed: ...
✓ Layout 6 selected (clicked card)
✓ Image uploaded: lamb-vindaloo-lancaster-pa.png
✓ Customizable section added
```

### Complete Failure (uses default Layout 1)
```
⚠ Could not select Layout 6: All strategies failed
⚠ Screenshot saved at logs/layout_selection.png
⚠ Continuing with default layout...
✓ Customizable section added
```

## Troubleshooting

### If Layout 6 selection still fails:

1. **Check the screenshot:**
   ```bash
   start logs\layout_selection.png
   ```

2. **Run the debug script:**
   ```bash
   python debug_browser.py
   ```
   Then manually test the selector in Playwright Inspector

3. **Use Playwright Codegen** (if it loads):
   ```bash
   playwright codegen --target python https://restaurant.foodamigos.io/login
   ```
   Record the exact steps and share the code

### If image upload fails:

1. Check that images are in cache:
   ```bash
   ls cache/HWY\ TO\ INDIA/
   ```

2. Check image filenames match:
   - Doc expects: `lamb-vindaloo-lancaster-pa.jpg`
   - Drive has: `lamb-vindaloo-lancaster-pa.png`
   - Code handles extension mismatch automatically

3. Check that `data.image_filename` is set correctly in the Google Doc

## Next Steps

1. **Delete the existing pages** (Lamb Vindaloo, Chicken Tikka Masala) from Food Amigo
2. **Run the automation again:**
   ```bash
   python batch_automation.py
   ```

3. **Check the results:**
   - Layout 6 should be selected (image on right side)
   - Hero image should be uploaded
   - All sections should be present

4. **Review logs:**
   ```bash
   tail -50 logs/batch_automation.log
   ```

## Manual Verification

After automation completes:
1. Log into Food Amigo
2. Go to Storefront Editor
3. Open "Lamb Vindaloo" page
4. Click "edit" on Customizable section
5. **Verify:**
   - Layout says "Layout: 6" (not "Layout: 1")
   - Hero image is visible in the preview
   - All text fields are filled correctly

---

**Ready to test!** Run `python batch_automation.py` and let me know the results. 🚀
