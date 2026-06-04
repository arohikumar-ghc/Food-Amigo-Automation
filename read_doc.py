from docx import Document

doc = Document("seo_files/hyw to india new.docx")

for i, para in enumerate(doc.paragraphs):
    print(f"{i}: {para.text}")