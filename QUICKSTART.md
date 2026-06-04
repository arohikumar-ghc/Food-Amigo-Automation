# Quick Start Guide

## Step 1: Test the Parser

The parser is fully functional and ready to use. Test it with the sample document:

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Run parser demo
python demo_parser.py
```

You should see structured output showing all extracted fields.

## Step 2: Parse Your Own Documents

Place your .docx files in the `seo_files/` directory and run:

```bash
python parser.py "seo_files/your-document.docx"
```

## Step 3: Set Up Automation (TODO)

### Current Status

✅ **Parser Module**: Complete and tested
✅ **Data Models**: Complete with validation
✅ **Configuration System**: Ready
✅ **Logging & Utils**: Implemented
🚧 **Automation Module**: Structure ready, needs Playwright selectors

### What's Needed

The `automation.py` file has all methods defined but needs actual Playwright selectors filled in. Look for `# TODO:` comments.

Example sections to complete:

```python
def login(self):
    self.page.goto(self.config.base_url)
    # TODO: Add actual selectors
    # self.page.fill("input[type='email']", self.config.email)
    # self.page.fill("input[type='password']", self.config.password)
    # self.page.click("button[type='submit']")
```

### How to Find Selectors

1. Run your existing Playwright recording (test.py)
2. Open Chrome DevTools (F12)
3. Use Elements tab to inspect each form field
4. Copy the selectors into the corresponding methods in automation.py

## Step 4: Configure Credentials

```bash
# Copy example file
cp .env.example .env

# Edit .env with your credentials
# FOODAMIGO_EMAIL=your-email@example.com
# FOODAMIGO_PASSWORD=your-password
# FOODAMIGO_RESTAURANT=Your Restaurant Name
```

## Step 5: Run Automation

### Single File

```bash
python main.py "seo_files/lamb-vindaloo.docx"
```

### Batch Processing

```bash
python main.py
```

This will process all .docx files in `seo_files/` directory.

## Testing Workflow

### Phase 1: Parser Only (✅ Ready Now)

```bash
python demo_parser.py
```

### Phase 2: With Automation (After selectors added)

```bash
# Test with one file first
python main.py "seo_files/test-page.docx"

# If successful, run batch
python main.py
```

## Current File Structure

```
✅ models.py          - Data classes (SEOPageData, FAQ)
✅ parser.py          - Word document parser
✅ config.py          - Configuration management
✅ utils.py           - Helper functions
✅ main.py            - Main orchestration
🚧 automation.py      - Playwright automation (needs selectors)
✅ demo_parser.py     - Parser demonstration
✅ test_parser.py     - Detailed parser test
✅ requirements.txt   - Dependencies
✅ .env.example       - Configuration template
✅ README.md          - Full documentation
```

## Integration Steps

To integrate with your existing Playwright recording:

1. **Open test.py** (your existing Playwright recording)
2. **Extract selectors** from each action
3. **Copy selectors** into corresponding methods in automation.py
4. **Test each method** individually
5. **Run complete workflow**

### Example Integration

From your recording in test.py:
```python
page.fill("input[name='email']", "user@example.com")
```

Copy to automation.py:
```python
def login(self):
    self.page.goto(self.config.base_url)
    self.page.fill("input[name='email']", self.config.email)
    self.page.fill("input[name='password']", self.config.password)
    self.page.click("button[type='submit']")
```

## Verification Checklist

- [ ] Parser extracts all fields correctly
- [ ] Validation passes for sample documents
- [ ] .env file configured
- [ ] Playwright selectors added to automation.py
- [ ] Single file test succeeds
- [ ] Batch processing succeeds

## Common Issues

### Parser Issues

**Problem**: Field not extracted
**Solution**: Check Word document format matches expected structure

**Problem**: FAQ parsing fails
**Solution**: Ensure FAQ format is "Title: Question" followed by "Description: Answer"

### Automation Issues (After implementation)

**Problem**: Element not found
**Solution**: Update selector in automation.py

**Problem**: Timeout
**Solution**: Increase timeout in .env: `FOODAMIGO_TIMEOUT=60000`

**Problem**: Login fails
**Solution**: Verify credentials in .env file

## Next Steps After Setup

1. Test parser with all your Word documents
2. Record a fresh Playwright session if needed
3. Extract and add all selectors to automation.py
4. Test with one document
5. Run batch processing
6. Review logs for any failures
7. Iterate and improve error handling

## Getting Help

Check these files for detailed information:
- `README.md` - Complete project documentation
- `demo_parser.py` - See parser in action
- `automation.py` - Review automation structure
- `logs/` - Check execution logs
