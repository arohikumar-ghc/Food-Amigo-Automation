"""
Debug script to examine Google Doc structure and understand parsing issues.
"""
import logging
from google.oauth2.credentials import Credentials
from google_doc_parser import GoogleDocParser, extract_doc_id

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Load credentials
creds = Credentials.from_authorized_user_file('token.json')
parser = GoogleDocParser(creds)

# The problematic document
doc_id = "1Bkh_Ipcrnt5t61izWNXDqCZ7wXZ_i_U1og2TU48XO5E"

logger.info(f"Downloading document content...")
text = parser._download_doc_as_text(doc_id)

logger.info(f"Document length: {len(text)} characters")

# Save to file for easier inspection
with open('debug_doc_content.txt', 'w', encoding='utf-8') as f:
    f.write(text)
logger.info("✓ Full document saved to debug_doc_content.txt")

logger.info(f"\n{'='*80}")
logger.info("FIRST 2000 CHARACTERS OF DOCUMENT:")
logger.info(f"{'='*80}")
# Use repr to safely show the text
print(text[:2000].encode('utf-8', errors='replace').decode('utf-8'))

logger.info(f"\n{'='*80}")
logger.info("LOOKING FOR DESCRIPTION FIELD PATTERNS:")
logger.info(f"{'='*80}")

# Find all instances of "Description:" in the document
import re
for match in re.finditer(r'Description:[^\n]*\n[^\n]*', text, re.IGNORECASE):
    logger.info(f"\nFound Description field at position {match.start()}:")
    logger.info(f"Context (100 chars before and after):")
    start = max(0, match.start() - 100)
    end = min(len(text), match.end() + 100)
    print(repr(text[start:end]))

logger.info(f"\n{'='*80}")
logger.info("PAGE DELIMITERS:")
logger.info(f"{'='*80}")
logger.info(f"Count of '=== PAGE START ===': {text.count('=== PAGE START ===')}")
logger.info(f"Count of '=== PAGE END ===': {text.count('=== PAGE END ===')}")

# Try to parse and see detailed errors
logger.info(f"\n{'='*80}")
logger.info("ATTEMPTING TO PARSE WITH DEBUG MODE:")
logger.info(f"{'='*80}")

try:
    pages = parser.parse_document(doc_id)
    logger.info(f"✓ Successfully parsed {len(pages)} pages!")
except Exception as e:
    logger.error(f"✗ Parsing failed: {e}")
