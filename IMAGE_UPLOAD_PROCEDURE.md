# Image Upload Procedure - Complete Workflow

## Overview
The automation now follows a **complete, step-by-step procedure** for uploading images in both the Social Metadata section and the Customizable section. This ensures that all UI interaction steps are properly executed in the correct order.

---

## Complete Image Upload Procedure

### For Customizable Section

The automation follows these **6 distinct steps**:

#### **STEP 1/6: Locate File Upload Input**
- Searches for file input element on the page
- If not immediately visible, attempts to reveal it by clicking upload buttons
- **Validates** that upload mechanism is available before proceeding

#### **STEP 2/6: Attach File to Input (Trigger Upload)**
- Attaches the selected image file to the file input
- This **initiates the upload** to the server
- Logs the file path being uploaded

#### **STEP 3/6: Wait for Upload Complete & Media Gallery Load**
- Waits 3 seconds for file to upload to server
- Waits for Media Gallery modal to open
- Ensures modal DOM is fully populated and ready

---

### Media Gallery Selection Procedure (Steps 4-6)

Once the Media Gallery modal is open, the automation executes a detailed **7-step selection workflow**:

#### **STEP 1: Wait for Media Gallery Modal to Fully Load**
- Waits 5 seconds for modal animation and image rendering
- Accounts for Ant Design's modal visibility quirks
- Takes optional screenshot for debugging
- **Ensures gallery is ready** before proceeding

#### **STEP 2: Verify Uploaded Image Appears in Gallery Preview**
- Checks that images are visible in the gallery
- Counts total images available
- **Validates that upload succeeded** and image is ready for selection

#### **STEP 3: Click on Uploaded Image Thumbnail to Select It**
- Clicks on the first image (newly uploaded one)
- Uses multiple fallback strategies (direct click, parent click, force click)
- **Initiates the selection process**

#### **STEP 4: Wait for Image Selection Confirmation**
- Waits 1 second for selection animation
- Allows time for visual feedback (checkmark/highlight to appear)
- **Ensures selection was registered** by the UI

#### **STEP 5: Wait for "Select (1)" Button to Become Active**
- Polls for up to 5 seconds checking if button shows count
- Monitors button text to confirm it shows "Select (1)"
- **Validates that the system recognized** the image selection

#### **STEP 6: Click "Select (1)" Button to Confirm Selection**
- Uses JavaScript to reliably find and click the confirmation button
- Falls back to Playwright methods if JavaScript fails
- **Finalizes the selection** and triggers modal close

#### **STEP 7: Verify Modal Closed (Selection Applied)**
- Checks that the modal has closed
- Confirms selection was successfully applied
- **Procedure complete** - image is now attached to the form field

---

## Key Improvements

### 1. **Complete Procedure Compliance**
- Every expected UI interaction step is executed
- No shortcuts or skipped steps
- Follows the same flow a human user would follow

### 2. **Proper Waiting & Validation**
- Waits for each step to complete before proceeding
- Validates that each action succeeded
- Ensures visual feedback elements appear (checkmarks, highlights, button states)

### 3. **Enhanced Logging**
- Clear step-by-step progress logging
- Uses visual indicators (📋 for steps, ✓ for success, ⚠ for warnings)
- Logs include timing information and validation results

### 4. **Robust Error Handling**
- Multiple fallback strategies for each click action
- Validates prerequisites before each step
- Continues gracefully if non-critical steps fail

---

## Where This Applies

This complete procedure is used in **two locations**:

1. **Social Metadata Section** - Banner/OG image upload
2. **Customizable Section** - Content image upload

Both use the same `_handle_media_gallery_selection()` method, ensuring **consistent behavior** across the application.

---

## Code Changes Summary

### File: `automation.py`

#### Changed Method: `_add_customizable_section()`
- **Lines 974-1050**: Enhanced image upload section
- Added explicit step numbering (STEP 1/6 through 6/6)
- Added detailed logging for each procedure step
- Clarified that steps 4-6 are handled by the gallery handler

#### Changed Method: `_handle_media_gallery_selection()`
- **Lines 118-350**: Complete rewrite with 7-step procedure
- Each step now has clear documentation
- Added validation between steps
- Enhanced logging with visual indicators
- Improved error messages

---

## Testing & Validation

The automation will now log detailed information showing:
- When each step begins
- What action is being taken
- Validation results (success/failure)
- Timing information
- Screenshots (saved to `logs/` directory)

Check the console output for messages like:
```
📋 STEP 1: Waiting for Media Gallery modal to fully load...
✓ Media Gallery modal should be loaded and ready
📋 STEP 2: Verifying uploaded image appears in gallery...
→ Found 3 image(s) in gallery
✓ Uploaded image visible in gallery preview
📋 STEP 3: Clicking on the uploaded image thumbnail to select it...
...
```

---

## Summary

The automation now **follows the complete UI procedure** for image uploads:
- ✅ All interaction steps are executed in order
- ✅ Proper waiting between steps
- ✅ Validation that each step succeeded
- ✅ Clear logging for troubleshooting
- ✅ Robust error handling with fallbacks

**No functionality has been removed** - the automation still works fully automatically, but now follows the proper workflow that the UI expects.
