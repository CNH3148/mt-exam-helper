import fitz
import sys

pdf_path = r"C:\Users\star0\Desktop\刷題系統\歷屆考題\微生物學與臨床微生物學_merge.pdf"
doc = fitz.open(pdf_path)

print(f"Total pages: {len(doc)}")

with open("test_pages.txt", "w", encoding="utf-8") as f:
    for i in range(min(5, len(doc))):
        page = doc.load_page(i)
        text = page.get_text()
        f.write(f"--- PAGE {i} ---\n")
        f.write(text)
        f.write("\n")

