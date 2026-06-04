# Food Amigo SEO Page Automation

Automated system for creating SEO pages in Food Amigo platform by parsing Word documents and using Playwright for browser automation.

## Project Overview

This tool eliminates manual work by:
1. Reading structured data from Word (.docx) files
2. Automatically logging into Food Amigo
3. Creating and populating SEO pages with the extracted data

## Project Structure

```
foodamigo-automation/
├── main.py              # Main entry point
├── parser.py            # Word document parser
├── automation.py        # Playwright automation
├── config.py            # Configuration management
├── models.py            # Data models
├── utils.py             # Utility functions
├── seo_files/           # Directory for .docx files
├── logs/                # Auto-generated logs
├── .env.example         # Example environment config
└── README.md            # This file
```

## Setup

### 1. Install Dependencies

```bash
# Activate virtual environment
.\venv\Scripts\activate

# Install required packages
pip install python-docx playwright

# Install Playwright browsers
playwright install chromium
```

### 2. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```env
FOODAMIGO_EMAIL=your-email@example.com
FOODAMIGO_PASSWORD=your-password
FOODAMIGO_RESTAURANT=Your Restaurant Name
FOODAMIGO_HEADLESS=false
FOODAMIGO_TIMEOUT=30000
```

### 3. Prepare SEO Files

Place your Word documents in the `seo_files/` directory.

## Word Document Format

Each `.docx` file should follow this structure:

```
Href in English: <page-url>
Name in English: <page-slug>
Title: <seo-title>
Description: <seo-description>

Customizable (Food Amigos- Customizable)

Subtitle: <subtitle>
Title: <section-title>
Description: <long-description>

Internal Links: ...

Title: <faq-question-1>
Description: <faq-answer-1>

Title: <faq-question-2>
Description: <faq-answer-2>
...
```

## Usage

### Test Parser Only

```bash
# Parse a single document and display extracted data
python parser.py "seo_files/your-document.docx"
```

### Single File Mode

```bash
# Process one document
python main.py "seo_files/your-document.docx"
```

### Batch Mode

```bash
# Process all .docx files in seo_files/
python main.py
```

## Modules

### models.py

Data classes for structured data:
- `FAQ`: Question and answer pair
- `SEOPageData`: Complete page data with validation

### parser.py

Word document parser:
- Extracts href, name, SEO metadata
- Parses customizable section content
- Extracts FAQ items
- Validates required fields

### config.py

Configuration management:
- Loads settings from environment variables
- Validates configuration
- Supports .env file loading

### automation.py

Browser automation using Playwright:
- `FoodAmigoAutomation` class with context manager
- Methods for each workflow step
- Error handling and screenshot capture

**Note**: Playwright selectors are marked with `# TODO` and need to be filled in based on actual website structure.

### utils.py

Helper functions:
- Logging setup
- File operations
- Progress tracking
- Duration formatting

### main.py

Main orchestration:
- Single file processing
- Batch processing
- Progress reporting
- Summary generation

## Current Status

### ✅ Completed

- Project structure
- Word document parser with validation
- Data models
- Configuration system
- Logging infrastructure
- Utility functions
- Batch processing framework

### 🚧 In Progress

- Playwright automation implementation
- Selectors need to be added based on actual Food Amigo website structure

### 📋 TODO

- Complete Playwright selectors in `automation.py`
- Test end-to-end workflow
- Add error recovery mechanisms
- Implement retry logic
- Add more robust FAQ parsing for edge cases

## Development

### Testing Parser

```bash
# View parsed data
python test_parser.py

# Debug document structure
python debug_doc.py
```

### Logging

Logs are automatically created in `logs/` directory with timestamps:
- Console output for immediate feedback
- File logs for detailed debugging

### Adding New Features

1. Update `models.py` if new data fields are needed
2. Extend `parser.py` extraction methods
3. Add corresponding automation steps in `automation.py`
4. Update validation in `models.py` and `config.py`

## Validation

The system validates:
- Required fields in Word documents
- Configuration settings
- Credentials
- Directory existence

Missing or invalid data is reported before automation runs.

## Error Handling

- Validation errors prevent execution
- Runtime errors are logged with full traceback
- Screenshots captured on errors (when enabled)
- Individual file failures don't stop batch processing

## Best Practices

1. **Always validate first**: Use parser.py to test document format
2. **Start with headless=false**: Watch automation to verify behavior
3. **Check logs**: Review logs/ directory for detailed execution info
4. **Backup data**: Keep original .docx files safe
5. **Test single file first**: Before running batch mode

## Troubleshooting

### Parser Issues

```bash
# If parsing fails, debug structure
python debug_doc.py
```

### Missing Fields

Check Word document follows exact format with:
- "Href in English:"
- "Name in English:"
- "Title:"
- "Description:"
- "Customizable" section
- FAQ items with "Title:" and "Description:"

### Automation Failures

1. Check credentials in .env
2. Verify restaurant name is exact match
3. Review screenshots in logs/ directory
4. Check browser console for JavaScript errors

## Security Notes

- Never commit `.env` file
- Keep credentials secure
- Review `.gitignore` to exclude sensitive files

## Future Enhancements

- [ ] Support multiple Word document formats
- [ ] Add preview mode (parse without creating)
- [ ] Implement undo/rollback functionality
- [ ] Add web interface for monitoring
- [ ] Email notifications on completion
- [ ] Parallel processing for batch mode
- [ ] Integration with Google Docs
- [ ] Automated testing suite

## License

Internal use only - Food Amigo team

## Support

For issues or questions, contact the development team.

# 1. Project folder ke andar jaane ke liye
cd "C:\Users\Arohi\Desktop\Food Amigo Automation"

# 2. Virtual environment (tools) active karne ke liye
.\venv\Scripts\activate

# 3. Main automation program ko chalu karne ke liye
python main.py "seo_files/hyw to india new.docx"

python restore_backup.py
