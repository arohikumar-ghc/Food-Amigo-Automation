# System Architecture

## High-Level Flow

```
┌─────────────────┐
│  Word Documents │
│   (.docx files) │
│   in seo_files/ │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   parser.py     │ ◄────── Extracts structured data
│                 │
│ • Read .docx    │
│ • Extract fields│
│ • Validate data │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  SEOPageData    │ ◄────── Data model (models.py)
│                 │
│ • href          │
│ • page_name     │
│ • seo_title     │
│ • description   │
│ • subtitle      │
│ • title         │
│ • description   │
│ • faqs[]        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  automation.py  │ ◄────── Browser automation
│                 │
│ • Login         │
│ • Navigate      │
│ • Fill forms    │
│ • Submit        │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Food Amigo     │
│   SEO Pages     │
│   Created ✓     │
└─────────────────┘
```

---

## Module Dependencies

```
main.py
   │
   ├─── config.py ◄───── .env file
   │      │
   │      └─── AutomationConfig
   │
   ├─── parser.py ◄───── seo_files/*.docx
   │      │
   │      ├─── models.py (SEOPageData, FAQ)
   │      └─── python-docx library
   │
   ├─── automation.py
   │      │
   │      ├─── models.py (SEOPageData)
   │      ├─── config.py (AutomationConfig)
   │      └─── playwright library
   │
   └─── utils.py
          │
          ├─── Logging
          ├─── Progress tracking
          └─── Helper functions
```

---

## Data Flow Detail

### 1. Input Phase
```
Word Document (.docx)
    │
    ├─ Paragraph 1: "Href in English: ..."
    ├─ Paragraph 2: "Name in English: ..."
    ├─ Paragraph 3: "Title: ..."
    ├─ Paragraph 4: "Description: ..."
    ├─ ...
    ├─ Paragraph N: "Customizable Section"
    │     ├─ Subtitle
    │     ├─ Title
    │     └─ Description
    │
    └─ FAQ Items
          ├─ Title: Question 1
          ├─ Description: Answer 1
          ├─ Title: Question 2
          └─ Description: Answer 2
```

### 2. Parsing Phase
```
SEODocumentParser
    │
    ├─ _find_field_value()
    │     └─ Regex: "^field_name\\s*:\\s*(.*)$"
    │
    ├─ _extract_customizable_section()
    │     ├─ Find "Customizable" marker
    │     ├─ Extract subtitle
    │     ├─ Extract title
    │     └─ Collect description paragraphs
    │
    └─ _extract_faqs()
          ├─ Find "Internal Links" marker
          ├─ Parse "Title:" as question
          └─ Parse "Description:" as answer
```

### 3. Validation Phase
```
SEOPageData.validate()
    │
    ├─ Check href exists
    ├─ Check page_name exists
    ├─ Check seo_title exists
    ├─ Check seo_description exists
    ├─ Check subtitle exists
    ├─ Check title exists
    ├─ Check description exists
    └─ Check faqs list not empty
    │
    └─ Return: [] (valid) or [missing_fields]
```

### 4. Automation Phase
```
FoodAmigoAutomation
    │
    ├─ start_browser()
    │     └─ Playwright.chromium.launch()
    │
    ├─ login()
    │     ├─ page.goto(base_url)
    │     ├─ page.fill(email)
    │     ├─ page.fill(password)
    │     └─ page.click(submit)
    │
    ├─ select_restaurant()
    │     ├─ page.fill(search)
    │     └─ page.click(restaurant_name)
    │
    ├─ open_storefront_editor()
    │     ├─ page.click(website_icon)
    │     ├─ page.click(open_storefront)
    │     └─ page.click(open_editor)
    │
    ├─ create_seo_page()
    │     │
    │     ├─ _click_add_page_button()
    │     │
    │     ├─ _fill_basic_info()
    │     │     ├─ page.fill(href)
    │     │     ├─ page.fill(name)
    │     │     └─ page.click(save)
    │     │
    │     ├─ _fill_seo_metadata()
    │     │     ├─ page.click(general_tab)
    │     │     ├─ page.fill(page_title)
    │     │     ├─ page.fill(description)
    │     │     └─ page.click(save)
    │     │
    │     ├─ _fill_social_metadata()
    │     │     ├─ page.click(social_tab)
    │     │     ├─ page.fill(social_title)
    │     │     ├─ page.fill(social_description)
    │     │     └─ page.click(save)
    │     │
    │     ├─ _add_customizable_section()
    │     │     ├─ page.click(add_feature)
    │     │     ├─ page.click(customizable_section)
    │     │     ├─ page.click(layout_6)
    │     │     ├─ page.fill(subtitle)
    │     │     ├─ page.fill(title)
    │     │     ├─ page.fill(description)
    │     │     └─ page.click(save)
    │     │
    │     ├─ _add_faq_section()
    │     │     ├─ page.click(add_feature)
    │     │     ├─ page.click(faq)
    │     │     ├─ For each FAQ:
    │     │     │     ├─ _add_single_faq()
    │     │     │     ├─ page.fill(question)
    │     │     │     └─ page.fill(answer)
    │     │     └─ page.click(save)
    │     │
    │     └─ _submit_page()
    │           └─ page.click(submit)
    │
    └─ close()
          └─ browser.close()
```

---

## Error Handling Flow

```
try:
    Parse document
    │
    ├─ Success ──► Validate data
    │                  │
    │                  ├─ Valid ──► Create page
    │                  │                │
    │                  │                ├─ Success ──► Log success
    │                  │                │
    │                  │                └─ Error ──► Screenshot + Log
    │                  │
    │                  └─ Invalid ──► Log missing fields
    │
    └─ Error ──► Log parsing error

finally:
    Close browser
    Write logs
```

---

## Configuration Loading

```
main.py starts
    │
    ├─ Check .env file
    │     │
    │     ├─ Exists ──► Load variables
    │     │                │
    │     │                └─► os.environ
    │     │
    │     └─ Not exists ──► Check environment variables
    │
    ├─ AutomationConfig.from_env()
    │     │
    │     ├─ Read FOODAMIGO_EMAIL
    │     ├─ Read FOODAMIGO_PASSWORD
    │     ├─ Read FOODAMIGO_RESTAURANT
    │     ├─ Read FOODAMIGO_HEADLESS (optional)
    │     └─ Read FOODAMIGO_TIMEOUT (optional)
    │
    └─ config.validate()
          │
          ├─ Valid ──► Proceed
          │
          └─ Invalid ──► Exit with error message
```

---

## Logging Architecture

```
main.py
    │
    └─ setup_logging()
          │
          ├─ Create logs/ directory
          │
          ├─ Create timestamped log file
          │     └─ logs/automation_20260602_123456.log
          │
          └─ Configure handlers
                │
                ├─ FileHandler ──► logs/*.log
                │                      │
                │                      └─ Full details
                │                          • DEBUG level
                │                          • Tracebacks
                │                          • All events
                │
                └─ StreamHandler ──► Console
                                         │
                                         └─ User-friendly
                                             • INFO level
                                             • Progress
                                             • Summaries
```

---

## Batch Processing Flow

```
main.py (no arguments)
    │
    ├─ get_docx_files("seo_files/")
    │     │
    │     └─ Returns: [file1.docx, file2.docx, ...]
    │
    ├─ ProgressTracker(total=N)
    │
    └─ For each file:
          │
          ├─ Parse document ──► SEOPageData
          │
          ├─ Validate ──► Pass/Fail
          │
          ├─ Create page
          │     │
          │     ├─ Success ──► Add to success_list
          │     │
          │     └─ Failure ──► Add to failed_list
          │
          ├─ Update progress (N/total)
          │
          └─ Continue to next file
                │
                └─ Final summary:
                      • Total processed
                      • Success count
                      • Failure count
                      • Duration
                      • Lists of successful/failed files
```

---

## Class Relationships

```
SEOPageData (dataclass)
    ├─ href: str
    ├─ page_name: str
    ├─ seo_title: str
    ├─ seo_description: str
    ├─ subtitle: str
    ├─ title: str
    ├─ description: str
    └─ faqs: List[FAQ]
          │
          └─ FAQ (dataclass)
                ├─ question: str
                └─ answer: str

AutomationConfig (dataclass)
    ├─ email: str
    ├─ password: str
    ├─ restaurant_name: str
    ├─ base_url: str = "https://..."
    ├─ headless: bool = False
    └─ timeout: int = 30000

SEODocumentParser
    ├─ doc_path: Path
    ├─ doc: Document (python-docx)
    ├─ paragraphs: List[str]
    │
    └─ Methods:
          ├─ _find_field_value() → str
          ├─ _extract_customizable_section() → tuple
          ├─ _extract_faqs() → List[FAQ]
          └─ parse() → SEOPageData

FoodAmigoAutomation
    ├─ config: AutomationConfig
    ├─ browser: Browser
    ├─ page: Page
    │
    └─ Methods:
          ├─ start_browser()
          ├─ login()
          ├─ select_restaurant()
          ├─ open_storefront_editor()
          ├─ create_seo_page(data: SEOPageData)
          ├─ _fill_basic_info(data)
          ├─ _fill_seo_metadata(data)
          ├─ _fill_social_metadata(data)
          ├─ _add_customizable_section(data)
          ├─ _add_faq_section(data)
          ├─ _submit_page()
          └─ close()
```

---

## File System Layout

```
C:\Users\Arohi\Desktop\Food Amigo Automation\
│
├─ Core Application
│  ├─ main.py ..................... Entry point
│  ├─ parser.py ................... Document parsing ✅
│  ├─ automation.py ............... Browser automation 🚧
│  ├─ models.py ................... Data structures ✅
│  ├─ config.py ................... Configuration ✅
│  └─ utils.py .................... Utilities ✅
│
├─ Testing & Demos
│  ├─ demo_parser.py .............. Parser demonstration ✅
│  ├─ test_parser.py .............. Detailed testing ✅
│  ├─ debug_doc.py ................ Debug tool ✅
│  ├─ read_doc.py ................. Simple reader ✅
│  └─ test.py ..................... Playwright test ✅
│
├─ Configuration
│  ├─ .env ........................ Credentials (create this)
│  ├─ .env.example ................ Template ✅
│  ├─ requirements.txt ............ Dependencies ✅
│  └─ .gitignore .................. Git exclusions ✅
│
├─ Documentation
│  ├─ README.md ................... Main documentation ✅
│  ├─ QUICKSTART.md ............... Setup guide ✅
│  ├─ PROJECT_SUMMARY.md .......... Overview ✅
│  └─ ARCHITECTURE.md ............. This file ✅
│
├─ Data Directories
│  ├─ seo_files/ .................. Input documents 📁
│  │  └─ *.docx ................... Word files
│  │
│  └─ logs/ ....................... Output logs 📁
│     ├─ automation_*.log ......... Execution logs
│     └─ error_*.png .............. Error screenshots
│
└─ Environment
   └─ venv/ ....................... Virtual environment ✅
      └─ [Python packages]
```

---

## Technology Stack

```
┌──────────────────────────────────────┐
│           Application Layer          │
│  ┌────────────────────────────────┐  │
│  │     main.py (Orchestration)    │  │
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
                  │
    ┌─────────────┴─────────────┐
    │                           │
┌───▼──────────┐     ┌──────────▼────┐
│ Parser Layer │     │ Automation    │
│              │     │ Layer         │
│ • parser.py  │     │               │
│ • models.py  │     │ • automation  │
│              │     │   .py         │
│ Libraries:   │     │               │
│ python-docx  │     │ Libraries:    │
│ lxml         │     │ playwright    │
└───┬──────────┘     └──────────┬────┘
    │                           │
    └─────────────┬─────────────┘
                  │
         ┌────────▼─────────┐
         │ Support Layer    │
         │                  │
         │ • config.py      │
         │ • utils.py       │
         │                  │
         │ Libraries:       │
         │ logging (stdlib) │
         │ pathlib (stdlib) │
         └──────────────────┘
```

---

## Execution Modes

### Mode 1: Single File
```
$ python main.py "seo_files/example.docx"

┌─────────────────────┐
│  Load config        │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Parse one file     │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Validate           │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Create page        │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Log result         │
└─────────────────────┘
```

### Mode 2: Batch Processing
```
$ python main.py

┌─────────────────────┐
│  Load config        │
└──────────┬──────────┘
           │
┌──────────▼──────────┐
│  Find all .docx     │
│  in seo_files/      │
└──────────┬──────────┘
           │
           │ For each file:
           │
┌──────────▼──────────┐
│  Parse document     │◄─────┐
└──────────┬──────────┘      │
           │                 │
┌──────────▼──────────┐      │
│  Validate           │      │
└──────────┬──────────┘      │
           │                 │
┌──────────▼──────────┐      │
│  Create page        │      │
└──────────┬──────────┘      │
           │                 │
┌──────────▼──────────┐      │
│  Track result       │      │
└──────────┬──────────┘      │
           │                 │
           └─────────────────┘
           │ Next file
           │
┌──────────▼──────────┐
│  Print summary      │
│  • Total            │
│  • Success          │
│  • Failed           │
│  • Duration         │
└─────────────────────┘
```

---

## Future Enhancements

```
Current System
      │
      ├─ Add retry logic
      │     └─ Retry failed pages 3 times
      │
      ├─ Add parallel processing
      │     └─ Process N files concurrently
      │
      ├─ Add preview mode
      │     └─ Show what would be created
      │
      ├─ Add rollback capability
      │     └─ Delete pages on error
      │
      ├─ Add web dashboard
      │     ├─ Upload .docx files
      │     ├─ Monitor progress
      │     └─ View history
      │
      └─ Add notifications
            ├─ Email on completion
            └─ Slack integration
```

---

This architecture provides a solid foundation for automated SEO page creation with clear separation of concerns, robust error handling, and easy extensibility.
