# -*- coding: utf-8 -*-
import fitz
import json
from pathlib import Path

pdf_dir = Path("../歷屆考題")
json_dir = Path("data")

for pdf_path in pdf_dir.glob("*.pdf"):
    subject = pdf_path.stem.replace("_merge", "")
    doc = fitz.open("pdf", pdf_path.read_bytes())
    
    ans_pages = []
    q_pages = []
    for i in range(len(doc)):
        if "標準答案" in doc.load_page(i).get_text():
            ans_pages.append(i)
        else:
            q_pages.append(i)
            
    q_blocks = []
    curr_block = []
    for i in q_pages:
        if not curr_block or i == curr_block[-1] + 1:
            curr_block.append(i)
        else:
            q_blocks.append(curr_block)
            curr_block = [i]
    if curr_block: q_blocks.append(curr_block)
    
    chunks = list(zip(q_blocks, ans_pages))
    json_path = json_dir / f"{subject}.json"
    if json_path.exists():
        data = json.loads(json_path.read_text(encoding="utf-8"))
        exam_ids = sorted(list(set(q["exam_id"] for q in data)))
        print(f"{subject}:")
        print(f"  PDF Chunks: {len(chunks)}")
        print(f"  JSON Exams: {len(exam_ids)} (IDs: {exam_ids})")
        
        q1 = next(q for q in data if q["exam_id"] == 1 and q["no"] == 1)
        print(f"  JSON Exam 1 Q1: {q1['question'][:30]}")
    else:
        print(f"{subject}: JSON not found!")

