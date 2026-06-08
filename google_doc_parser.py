"""
Google Docs parser with strict delimiter-based structure.

Parses documents in format:
=== PAGE START ===
Page Name: ...
Href: ...
...
=== PAGE END ===
"""
import logging
import re
from typing import List, Dict, Optional
from io import BytesIO
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import requests
from models import SEOPageData, FAQ


logger = logging.getLogger("foodamigo_automation.google_doc_parser")


class ParseError(Exception):
    """Custom exception for parsing errors."""
    pass


class GoogleDocParser:
    """Parser for Google Docs with delimiter-based SEO page structure."""

    PAGE_START_DELIMITER = "=== PAGE START ==="
    PAGE_END_DELIMITER = "=== PAGE END ==="

    REQUIRED_FIELDS = [
        "Page Name",
        "Href",
        "SEO Title",
        "SEO Description",
        "Social Title",
        "Social Description",
        "Image",
        "Subtitle",
        "Title",
        "Description"
    ]

    def __init__(self, credentials: Credentials):
        """
        Initialize parser with Google credentials.

        Args:
            credentials: Google OAuth2 credentials
        """
        self.credentials = credentials
        self.service = build('docs', 'v1', credentials=credentials)

    def parse_document(self, doc_id: str) -> List[SEOPageData]:
        """
        Parse Google Doc and extract all SEO pages.

        Args:
            doc_id: Google Doc ID

        Returns:
            List of SEOPageData objects

        Raises:
            ParseError: If document structure is invalid
        """
        logger.info(f"Parsing Google Doc: {doc_id}")

        # Download document content as plain text
        text = self._download_doc_as_text(doc_id)

        # Parse pages
        pages = self._parse_pages(text)

        logger.info(f"✓ Parsed {len(pages)} pages from document")
        return pages

    def _download_doc_as_text(self, doc_id: str) -> str:
        """
        Download Google Doc content as plain text.

        Args:
            doc_id: Google Doc ID

        Returns:
            Document text content

        Raises:
            Exception: If download fails
        """
        try:
            # Export as plain text
            export_url = f"https://docs.google.com/document/d/{doc_id}/export?format=txt"

            # Use credentials to download
            headers = {'Authorization': f'Bearer {self.credentials.token}'}
            response = requests.get(export_url, headers=headers)

            if response.status_code != 200:
                raise Exception(f"Failed to download doc: HTTP {response.status_code}")

            text = response.text
            logger.debug(f"Downloaded {len(text)} characters from doc")
            return text

        except Exception as e:
            logger.error(f"Failed to download document: {e}")
            raise ParseError(f"Could not download Google Doc: {e}")

    def _parse_pages(self, text: str) -> List[SEOPageData]:
        """
        Parse pages from document text using delimiters.

        Args:
            text: Document text content

        Returns:
            List of SEOPageData objects

        Raises:
            ParseError: If parsing fails
        """
        pages = []

        # Split by PAGE START delimiter
        page_blocks = text.split(self.PAGE_START_DELIMITER)

        if len(page_blocks) <= 1:
            raise ParseError(f"No pages found. Document must contain '{self.PAGE_START_DELIMITER}' delimiters.")

        # Skip first block (content before first page)
        page_blocks = page_blocks[1:]

        for i, block in enumerate(page_blocks, start=1):
            try:
                # Check for PAGE END delimiter
                if self.PAGE_END_DELIMITER not in block:
                    logger.warning(f"Page {i}: Missing '{self.PAGE_END_DELIMITER}' delimiter, skipping")
                    continue

                # Extract content between START and END
                page_content = block.split(self.PAGE_END_DELIMITER)[0].strip()

                # Parse page data
                page_data = self._parse_page_content(page_content, page_number=i)
                pages.append(page_data)

                logger.debug(f"✓ Parsed page {i}: {page_data.page_name}")

            except ParseError as e:
                logger.error(f"✗ Page {i} parse error: {e}")
                # Continue to next page (don't fail entire document)
                continue
            except Exception as e:
                logger.error(f"✗ Page {i} unexpected error: {e}")
                continue

        if not pages:
            raise ParseError("No valid pages found in document")

        return pages

    def _parse_page_content(self, content: str, page_number: int) -> SEOPageData:
        """
        Parse a single page content block.

        Args:
            content: Page content between delimiters
            page_number: Page number for error reporting

        Returns:
            SEOPageData object

        Raises:
            ParseError: If required fields missing or invalid
        """
        # Parse key-value pairs
        fields = {}
        current_key = None

        for line in content.split('\n'):
            line = line.strip()

            if not line:
                continue

            # Check if line is a field (contains colon)
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip()

                fields[key] = value
                current_key = key
            elif current_key:
                # Multi-line value continuation
                fields[current_key] += ' ' + line

        # Validate required fields
        missing_fields = [f for f in self.REQUIRED_FIELDS if f not in fields or not fields[f]]
        if missing_fields:
            raise ParseError(f"Page {page_number}: Missing required fields: {', '.join(missing_fields)}")

        # Extract FAQs
        faqs = self._extract_faqs(fields)

        if not faqs:
            raise ParseError(f"Page {page_number}: At least one FAQ is required")

        # Build SEOPageData object
        page_data = SEOPageData(
            href=fields['Href'],
            page_name=fields['Page Name'],
            seo_title=fields['SEO Title'],
            seo_description=fields['SEO Description'],
            subtitle=fields['Subtitle'],
            title=fields['Title'],
            description=fields['Description'],
            faqs=faqs
        )

        # Store additional fields (social, image) as attributes
        page_data.social_title = fields.get('Social Title', fields['SEO Title'])
        page_data.social_description = fields.get('Social Description', fields['SEO Description'])
        page_data.image_filename = fields.get('Image', '')

        return page_data

    def _extract_faqs(self, fields: Dict[str, str]) -> List[FAQ]:
        """
        Extract FAQ questions and answers from fields.

        Args:
            fields: Parsed field dictionary

        Returns:
            List of FAQ objects
        """
        faqs = []

        # Find all FAQ Question X and FAQ Answer X pairs
        i = 1
        while True:
            question_key = f"FAQ Question {i}"
            answer_key = f"FAQ Answer {i}"

            if question_key not in fields or answer_key not in fields:
                break

            question = fields[question_key].strip()
            answer = fields[answer_key].strip()

            if question and answer:
                faqs.append(FAQ(question=question, answer=answer))

            i += 1

        return faqs


def extract_doc_id(doc_url: str) -> str:
    """
    Extract document ID from Google Docs URL.

    Args:
        doc_url: Full Google Docs URL

    Returns:
        Document ID

    Example:
        URL: https://docs.google.com/document/d/1ABC123.../edit
        Returns: 1ABC123...
    """
    match = re.search(r'/document/d/([a-zA-Z0-9-_]+)', doc_url)
    if match:
        return match.group(1)
    raise ValueError(f"Could not extract document ID from URL: {doc_url}")


# Example usage
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Example: Parse a document
    from google.oauth2.credentials import Credentials

    # Load credentials (token.json)
    creds = Credentials.from_authorized_user_file('token.json')

    parser = GoogleDocParser(creds)

    doc_url = "YOUR_GOOGLE_DOC_URL"
    doc_id = extract_doc_id(doc_url)

    try:
        pages = parser.parse_document(doc_id)
        print(f"Successfully parsed {len(pages)} pages")

        for i, page in enumerate(pages, 1):
            print(f"\nPage {i}:")
            print(f"  Name: {page.page_name}")
            print(f"  Href: {page.href}")
            print(f"  FAQs: {len(page.faqs)}")

    except ParseError as e:
        print(f"Parse error: {e}")
