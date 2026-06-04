"""
Demo script to showcase parser functionality.
"""
from parser import parse_seo_document
from pathlib import Path


def demo_parser():
    """Demonstrate parser capabilities."""

    print("=" * 80)
    print("FOOD AMIGO SEO PARSER DEMO")
    print("=" * 80)

    seo_files = list(Path("seo_files").glob("*.docx"))

    if not seo_files:
        print("\nNo .docx files found in seo_files/ directory")
        return

    doc_path = str(seo_files[0])

    print(f"\nProcessing: {doc_path}")
    print("-" * 80)

    try:
        data = parse_seo_document(doc_path)

        print("\n1. BASIC INFO")
        print(f"   Href: {data.href}")
        print(f"   Page Name: {data.page_name}")

        print("\n2. SEO METADATA (General Tab)")
        print(f"   Title: {data.seo_title}")
        print(f"   Description: {data.seo_description[:100]}...")

        print("\n3. SOCIAL METADATA (Social Tab)")
        print(f"   [Will use same as SEO metadata]")
        print(f"   Title: {data.seo_title}")
        print(f"   Description: {data.seo_description[:100]}...")

        print("\n4. CUSTOMIZABLE SECTION (Layout 6)")
        print(f"   Subtitle: {data.subtitle}")
        print(f"   Title: {data.title}")
        print(f"   Description: {len(data.description)} characters")
        print(f"   Preview: {data.description[:150]}...")

        print("\n5. FAQ SECTION")
        print(f"   Total FAQs: {len(data.faqs)}")

        for i, faq in enumerate(data.faqs, 1):
            print(f"\n   FAQ #{i}")
            print(f"   Q: {faq.question}")
            print(f"   A: {faq.answer[:100]}...")

        print("\n" + "=" * 80)
        print("VALIDATION RESULT")
        print("=" * 80)

        missing = data.validate()

        if not missing:
            print("\n[SUCCESS] All required fields are present!")
            print("\nThis data is ready to be used for automation.")
        else:
            print("\n[ERROR] Missing required fields:")
            for field in missing:
                print(f"  - {field}")

        print("\n" + "=" * 80)
        print("DATA STRUCTURE")
        print("=" * 80)

        print("\nThe parsed data is returned as a structured object:")
        print(f"  - Type: {type(data).__name__}")
        print(f"  - Attributes: {len(data.__dataclass_fields__)} fields")
        print(f"  - Validation: Built-in")
        print(f"  - Ready for: Playwright automation")

        print("\n" + "=" * 80)
        print("NEXT STEPS")
        print("=" * 80)

        print("\n1. Complete Playwright selectors in automation.py")
        print("2. Set up .env file with credentials")
        print("3. Run: python main.py '<docx-file>' for single file")
        print("4. Run: python main.py for batch processing")

    except Exception as e:
        print(f"\n[ERROR] Failed to parse document: {e}")


if __name__ == "__main__":
    demo_parser()
