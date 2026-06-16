# -*- coding: utf-8 -*-
import fitz
from pathlib import Path

pdf_dir = Path("../歷屆考題")
pdfs = list(pdf_dir.glob("*.pdf"))
for pdf_path in pdfs:
    if "臨床血液學與血庫學" in pdf_path.name:
        doc = fitz.open(pdf_path)
        ans_pages = []
        for i in range(len(doc)):
            if "測驗式試題標準答案" in doc.load_page(i).get_text():
                ans_pages.append(i)
        
        if ans_pages:
            print(f"Found answer page for 114-2 (Exam 1) at index: {ans_pages[0]}")
            text = doc.load_page(ans_pages[0]).get_text("text")
            lines = text.split("\n")
            for j, line in enumerate(lines[:100]):
                print(f"{j}: {line}")

