"""Test script to verify parser output in detail."""
from parser import parse_seo_document

doc_path = "seo_files/hyw to india new.docx"

data = parse_seo_document(doc_path)

print("=" * 80)
print("COMPLETE PARSED DATA")
print("=" * 80)

print("\n[BASIC INFO]")
print(f"Href: {data.href}")
print(f"Page Name: {data.page_name}")

print("\n[SEO METADATA]")
print(f"Title: {data.seo_title}")
print(f"Description: {data.seo_description}")

print("\n[CUSTOMIZABLE SECTION]")
print(f"Subtitle: {data.subtitle}")
print(f"Title: {data.title}")
print(f"\nDescription ({len(data.description)} chars):")
print(data.description)

print("\n[FAQs]")
print(f"Total: {len(data.faqs)} items\n")
for i, faq in enumerate(data.faqs, 1):
    print(f"FAQ {i}:")
    print(f"  Q: {faq.question}")
    print(f"  A: {faq.answer}")
    print()

print("=" * 80)
print("VALIDATION")
print("=" * 80)

if data.is_valid():
    print("\n[OK] All required fields present")
else:
    print("\n[ERROR] Missing fields:")
    for field in data.validate():
        print(f"  - {field}")
