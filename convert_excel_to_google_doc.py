"""
Convert Excel (.xlsx) SEO pages to Google Doc format with delimiters.

This helps migrate from old single-file Excel workflow to new batch Google Docs workflow.
"""
import sys
from pathlib import Path
import openpyxl
from models import SEOPageData


def parse_excel_file(excel_path: Path) -> list:
    """
    Parse Excel file and extract SEO page data.

    Assumes Excel structure:
    - Column A: Page Name
    - Column B: Href
    - Column C: SEO Title
    - Column D: SEO Description
    - (etc.)

    Args:
        excel_path: Path to Excel file

    Returns:
        List of page data dictionaries
    """
    print(f"Reading Excel file: {excel_path}")

    try:
        workbook = openpyxl.load_workbook(excel_path)
        sheet = workbook.active

        pages = []

        # Skip header row, start from row 2
        for row_idx, row in enumerate(sheet.iter_rows(min_row=2, values_only=True), start=2):
            if not row[0]:  # Skip empty rows
                continue

            page_data = {
                'page_name': row[0] if len(row) > 0 else '',
                'href': row[1] if len(row) > 1 else '',
                'seo_title': row[2] if len(row) > 2 else '',
                'seo_description': row[3] if len(row) > 3 else '',
                'subtitle': row[4] if len(row) > 4 else '',
                'title': row[5] if len(row) > 5 else '',
                'description': row[6] if len(row) > 6 else '',
                'image_filename': row[7] if len(row) > 7 else '',
                'faqs': []
            }

            # Extract FAQs (assume columns 8+ contain FAQ pairs)
            faq_col_start = 8
            i = 0
            while faq_col_start + (i * 2) < len(row):
                question_col = faq_col_start + (i * 2)
                answer_col = question_col + 1

                if answer_col < len(row):
                    question = row[question_col]
                    answer = row[answer_col]

                    if question and answer:
                        page_data['faqs'].append({
                            'question': str(question).strip(),
                            'answer': str(answer).strip()
                        })

                i += 1

            pages.append(page_data)
            print(f"  ✓ Row {row_idx}: {page_data['page_name']}")

        print(f"✓ Extracted {len(pages)} pages from Excel")
        return pages

    except Exception as e:
        print(f"✗ Error reading Excel: {e}")
        sys.exit(1)


def generate_google_doc_text(pages: list) -> str:
    """
    Generate Google Doc formatted text with delimiters.

    Args:
        pages: List of page data dictionaries

    Returns:
        Formatted text string
    """
    output = []

    for page in pages:
        output.append("=== PAGE START ===")
        output.append(f"Page Name: {page['page_name']}")
        output.append(f"Href: {page['href']}")
        output.append(f"SEO Title: {page['seo_title']}")
        output.append(f"SEO Description: {page['seo_description']}")
        output.append(f"Social Title: {page['seo_title']}")  # Reuse SEO title
        output.append(f"Social Description: {page['seo_description']}")  # Reuse SEO description

        if page['image_filename']:
            output.append(f"Image: {page['image_filename']}")
        else:
            output.append("Image: ")  # Empty but present

        output.append(f"Subtitle: {page['subtitle']}")
        output.append(f"Title: {page['title']}")
        output.append(f"Description: {page['description']}")

        # Add FAQs
        for i, faq in enumerate(page['faqs'], start=1):
            output.append(f"FAQ Question {i}: {faq['question']}")
            output.append(f"FAQ Answer {i}: {faq['answer']}")

        # If no FAQs, add empty ones (required)
        if not page['faqs']:
            output.append("FAQ Question 1: ")
            output.append("FAQ Answer 1: ")

        output.append("=== PAGE END ===")
        output.append("")  # Blank line between pages

    return "\n".join(output)


def main():
    """Main conversion workflow."""
    if len(sys.argv) < 2:
        print("Usage: python convert_excel_to_google_doc.py <excel_file.xlsx>")
        print("\nExample:")
        print("  python convert_excel_to_google_doc.py seo_pages.xlsx")
        sys.exit(1)

    excel_path = Path(sys.argv[1])

    if not excel_path.exists():
        print(f"✗ File not found: {excel_path}")
        sys.exit(1)

    print("="*70)
    print("EXCEL TO GOOGLE DOC CONVERTER")
    print("="*70)

    # Parse Excel
    pages = parse_excel_file(excel_path)

    # Generate Google Doc format
    print("\nGenerating Google Doc format...")
    doc_text = generate_google_doc_text(pages)

    # Save to text file
    output_path = excel_path.stem + "_google_doc_format.txt"
    output_file = Path(output_path)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(doc_text)

    print(f"✓ Saved to: {output_file}")

    print("\n" + "="*70)
    print("NEXT STEPS:")
    print("="*70)
    print(f"1. Open the file: {output_file}")
    print("2. Copy ALL content (Ctrl+A, Ctrl+C)")
    print("3. Create a new Google Doc")
    print("4. Paste content (Ctrl+V)")
    print("5. Review and fix any missing data")
    print("6. Use this Google Doc URL in your Google Sheet")
    print("="*70)


if __name__ == "__main__":
    main()
