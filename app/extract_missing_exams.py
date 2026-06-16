# -*- coding: utf-8 -*-
import fitz
import json
import os
from pathlib import Path
from extract_all_gemini import extract_questions_gemini, extract_images_from_pages
from fix_answers import extract_answers_from_page

pdf_dir = Path("C:/Users/star0/Desktop/刷題系統/歷屆考題")
json_dir = Path("C:/Users/star0/Desktop/刷題系統/app/data")
img_dir = Path("C:/Users/star0/Desktop/刷題系統/app/public/images")

def process_missing():
    for pdf_path in pdf_dir.glob("*.pdf"):
        subject = pdf_path.stem.replace("_merge", "")
        print(f"Checking {subject}...")
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
        data = []
        exam_ids = set()
        if json_path.exists():
            data = json.loads(json_path.read_text(encoding="utf-8"))
            exam_ids = set(q["exam_id"] for q in data)
            
        for chunk_idx, (q_pages, ans_page_idx) in enumerate(chunks):
            if chunk_idx in exam_ids:
                continue
                
            print(f"  Missing exam chunk {chunk_idx}. Extracting...")
            
            # 1. Extract answers via PyMuPDF
            ans_page = doc.load_page(ans_page_idx)
            real_answers = extract_answers_from_page(ans_page)
            
            # 2. Extract questions via Gemini
            q_doc = fitz.open()
            q_doc.insert_pdf(doc, from_page=q_pages[0], to_page=q_pages[-1])
            temp_q = f"temp_q_{chunk_idx}.pdf"
            q_doc.save(temp_q)
            q_doc.close()
            
            exam_content = extract_questions_gemini(temp_q)
            os.remove(temp_q)
            
            # 3. Extract images
            img_mappings = extract_images_from_pages(doc, q_pages, subject, chunk_idx, str(img_dir))
            
            if exam_content and exam_content.get("questions"):
                year = exam_content.get("year", 0)
                term = exam_content.get("term", 0)
                subj = exam_content.get("subject", subject)
                
                new_questions = 0
                for q in exam_content["questions"]:
                    no = q["no"]
                    ans = real_answers.get(no, "#")
                    images = img_mappings.get(no, [])
                    auto_tag = f"{year}-{term}-{subj}-{no}"
                    
                    data.append({
                        "exam_id": chunk_idx,
                        "no": no,
                        "question": q["question"],
                        "choices": q["choices"],
                        "answer": ans,
                        "images": images,
                        "tags": [auto_tag]
                    })
                    new_questions += 1
                print(f"  -> Added {new_questions} questions for chunk {chunk_idx}.")
            else:
                print(f"  -> Failed to extract questions for chunk {chunk_idx}.")
                
        # Save back to json
        if data:
            # Sort by exam_id, then by no
            data.sort(key=lambda x: (x["exam_id"], x["no"]))
            json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            
if __name__ == "__main__":
    process_missing()

