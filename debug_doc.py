"""Debug script to examine document structure line by line."""
from docx import Document

doc = Document("seo_files/hyw to india new.docx")

print("Document structure (line by line):")
print("=" * 80)

for i, para in enumerate(doc.paragraphs):
    text = para.text.strip()
    if text:
        print(f"{i:3d}: {repr(text)}")
