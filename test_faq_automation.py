"""
Test script to verify FAQ automation works correctly.
"""
from parser import parse_seo_document

# Parse the document
doc_path = "seo_files/hyw to india new.docx"
data = parse_seo_document(doc_path)

print("=" * 80)
print("FAQ AUTOMATION TEST")
print("=" * 80)

print(f"\nTotal FAQs to process: {len(data.faqs)}")
print("\nFAQs that will be added:\n")

for i, faq in enumerate(data.faqs, 1):
    print(f"FAQ {i}/{len(data.faqs)}:")
    print(f"  Question: {faq.question}")
    print(f"  Answer: {faq.answer[:80]}...")
    print()

print("=" * 80)
print("AUTOMATION FLOW")
print("=" * 80)

print("""
The automation will:
1. Click 'plus Features' button
2. Click 'FAQ' option
3. Click 'plus' in Elements
4. Toggle visibility switch
5. Click edit button
6. Click 'FAQ Items' tab
7. For EACH FAQ item:
   a. Wait for 'plus Add' button to be visible
   b. Click 'plus Add' button
   c. Wait for dialog to open
   d. Fill Question (Title)
   e. Fill Answer (Description)
   f. Click Save
   g. Close dialog if open
   h. Wait before next iteration
8. Close the drawer

Expected behavior: All FAQs added automatically without manual intervention
""")

print("=" * 80)
print("Ready to test! Run: python main.py \"seo_files/hyw to india new.docx\"")
print("=" * 80)
