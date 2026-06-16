# -*- coding: utf-8 -*-
import fitz
from pathlib import Path

pdf_dir = Path("../歷屆考題")
pdfs = list(pdf_dir.glob("*.pdf"))
target = None
for p in pdfs:
    if "血液" in p.name:
        target = p
        break

pdf_bytes = target.read_bytes()
doc = fitz.open("pdf", pdf_bytes)

ans_pages = []
for i in range(len(doc)):
    if "測驗式試題標準答案" in doc.load_page(i).get_text():
        ans_pages.append(i)

page = doc.load_page(ans_pages[0])
words = page.get_text("words")
words.sort(key=lambda w: (round(w[1]/5)*5, w[0]))

print("Row-wise reading:")
current_y = -1
line_text = ""
for w in words:
    y = round(w[1]/5)*5
    if y != current_y:
        if line_text:
            print(line_text)
        current_y = y
        line_text = w[4]
    else:
        line_text += "\t" + w[4]
if line_text:
    print(line_text)

