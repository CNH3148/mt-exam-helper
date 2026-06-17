import fitz

pdf_path = r"C:\Users\star0\Desktop\刷題系統\歷屆考題\微生物學與臨床微生物學_merge.pdf"
doc = fitz.open(pdf_path)

with open("test_pages_structure.txt", "w", encoding="utf-8") as f:
    for i in range(len(doc)):
        page = doc.load_page(i)
        text = page.get_text()
        if "測驗式試題標準答案" in text:
            f.write(f"Page {i}: Answer Key\n")
        elif "類科名稱" in text and "科目名稱" in text and "測驗式試題標準答案" not in text:
            f.write(f"Page {i}: Exam Start\n")

