# -*- coding: utf-8 -*-
import fitz
import json
from pathlib import Path

pdf_dir = Path("C:/Users/star0/Desktop/刷題系統/歷屆考題")
json_dir = Path("C:/Users/star0/Desktop/刷題系統/app/data")

def extract_answers_from_page(page):
    words = page.get_text("words")
    words.sort(key=lambda w: (round(w[1]/5)*5, w[0]))
    
    answers = {}
    current_y = -1
    line_words = []
    
    lines = []
    for w in words:
        y = round(w[1]/5)*5
        if y != current_y:
            if line_words: lines.append(line_words)
            current_y = y
            line_words = [w[4]]
        else:
            line_words.append(w[4])
    if line_words: lines.append(line_words)
        
    for i in range(len(lines)):
        row_str = "".join(lines[i])
        if ("題號" in row_str or "題序" in row_str) and i + 1 < len(lines):
            next_str = "".join(lines[i+1])
            if "答案" in next_str:
                q_row = lines[i]
                a_row = lines[i+1]
                
                q_nums = []
                for w in q_row:
                    if w.isdigit(): q_nums.append(int(w))
                        
                a_vals = []
                for w in a_row:
                    w_clean = w.replace("答案", "").replace("　", "").strip()
                    w_clean = w_clean.translate(str.maketrans("ＡＢＣＤ＃", "ABCD#"))
                    for char in w_clean:
                        if char in "ABCD#":
                            a_vals.append(char)
                            
                for qn, ans in zip(q_nums, a_vals):
                    answers[qn] = ans
                    
    return answers

def process_all():
    total_fixed = 0
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
        if not json_path.exists(): continue
            
        data = json.loads(json_path.read_text(encoding="utf-8"))
        exam_ids = set(q["exam_id"] for q in data)
        for exam_id in exam_ids:
            if exam_id < len(chunks):
                ans_page_idx = chunks[exam_id][1]
                ans_page = doc.load_page(ans_page_idx)
                real_answers = extract_answers_from_page(ans_page)
                
                if len(real_answers) != 80:
                    print(f"WARN: {subject} Exam {exam_id} Page {ans_page_idx} extracted {len(real_answers)} answers!")
                
                count = 0
                for q in data:
                    if q["exam_id"] == exam_id:
                        correct_ans = real_answers.get(q["no"], "#")
                        if q["answer"] != correct_ans:
                            q["answer"] = correct_ans
                            count += 1
                total_fixed += count
                
        json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        
    print(f"Total answers fixed: {total_fixed}")

if __name__ == "__main__":
    process_all()

