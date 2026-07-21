"""
Test Description field parsing for both formats.
"""
import logging
from google_doc_parser import GoogleDocParser

logging.basicConfig(level=logging.ERROR)

def test_description_parsing():
    """Test both Description formats."""

    # Mock parser instance
    parser = GoogleDocParser.__new__(GoogleDocParser)
    parser.REQUIRED_FIELDS = [
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

    # Test Format 1: Description on same line
    print("Testing Format 1 (Description on same line):")
    print("=" * 80)
    content1 = """
Page Name: Test Page
Href: /test-page
SEO Title: Test SEO Title
SEO Description: Test SEO Description
Social Title: Test Social Title
Social Description: Test Social Description
Image: test.jpg
Subtitle: Test Subtitle
Title: Test Title
Description: This is a test description on the same line.
FAQ Question 1: Question 1?
FAQ Answer 1: Answer 1.
"""

    try:
        page1 = parser._parse_page_content(content1.strip(), 1)
        print(f"[OK] Parsed successfully")
        print(f"  Description: '{page1.description}'")
        print(f"  Length: {len(page1.description)} chars")
        assert page1.description == "This is a test description on the same line."
        print(f"[OK] Format 1 test PASSED\n")
    except Exception as e:
        print(f"[FAIL] Format 1 test FAILED: {e}\n")
        return False

    # Test Format 2: Description on next line
    print("Testing Format 2 (Description on next line):")
    print("=" * 80)
    content2 = """
Page Name: Test Page
Href: /test-page
SEO Title: Test SEO Title
SEO Description: Test SEO Description
Social Title: Test Social Title
Social Description: Test Social Description
Image: test.jpg
Subtitle: Test Subtitle
Title: Test Title
Description:
This is a test description on the next line with a URL https://example.com/test.
FAQ Question 1: Question 1?
FAQ Answer 1: Answer 1.
"""

    try:
        page2 = parser._parse_page_content(content2.strip(), 2)
        print(f"[OK] Parsed successfully")
        print(f"  Description: '{page2.description}'")
        print(f"  Length: {len(page2.description)} chars")
        expected = "This is a test description on the next line with a URL https://example.com/test."
        assert page2.description == expected, f"Expected: {expected}, Got: {page2.description}"
        print(f"[OK] Format 2 test PASSED\n")
    except Exception as e:
        print(f"[FAIL] Format 2 test FAILED: {e}\n")
        return False

    # Test Format 3: Multi-line Description starting on next line
    print("Testing Format 3 (Multi-line Description on next line):")
    print("=" * 80)
    content3 = """
Page Name: Test Page
Href: /test-page
SEO Title: Test SEO Title
SEO Description: Test SEO Description
Social Title: Test Social Title
Social Description: Test Social Description
Image: test.jpg
Subtitle: Test Subtitle
Title: Test Title
Description:
This is the first line of description.
This is the second line with URL https://example.com/order.
This is the third line.
FAQ Question 1: Question 1?
FAQ Answer 1: Answer 1.
"""

    try:
        page3 = parser._parse_page_content(content3.strip(), 3)
        print(f"[OK] Parsed successfully")
        print(f"  Description: '{page3.description}'")
        print(f"  Length: {len(page3.description)} chars")
        assert "first line" in page3.description
        assert "second line" in page3.description
        assert "third line" in page3.description
        assert "https://example.com/order" in page3.description
        print(f"[OK] Format 3 test PASSED\n")
    except Exception as e:
        print(f"[FAIL] Format 3 test FAILED: {e}\n")
        return False

    print("=" * 80)
    print("ALL TESTS PASSED!")
    print("=" * 80)
    return True

if __name__ == "__main__":
    success = test_description_parsing()
    exit(0 if success else 1)
