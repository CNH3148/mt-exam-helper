import os
import json
import re
import fitz

def split_first_exam(pdf_path):
    doc = fitz.open(pdf_path)
    ans_pages = []
    q_pages = []
    
    ans_pages.append(0)
    for i in range(1, len(doc)):
        text = doc.load_page(i).get_text()
        if "測驗式試題標準答案" in text:
            break
        q_pages.append(i)
        
    return ans_pages, q_pages, doc

def parse_answers(doc, ans_pages):
    ans_dict = {}
    for pid in ans_pages:
        page = doc.load_page(pid)
        text = page.get_text()
        
        # Look for patterns like:
        # 01 D  or  1 D
        # 02 C
        matches = re.findall(r'^0?([1-9][0-9]?)\s+([A-D#])\s*$', text, re.MULTILINE)
        for m in matches:
            ans_dict[int(m[0])] = m[1]
    return ans_dict

def parse_questions(doc, q_pages):
    full_text = ""
    for pid in q_pages:
        full_text += doc.load_page(pid).get_text() + "\n"
        
    # Pattern to match question blocks
    # usually:
    # 1. 有關...
    # A. ...
    # B. ...
    # C. ...
    # D. ...
    
    # We split by 'number.'
    # regex to split:
    blocks = re.split(r'\n(?=\d{1,2}\.)', full_text)
    
    questions = []
    for block in blocks:
        block = block.strip()
        if not block or not re.match(r'^\d{1,2}\.', block):
            continue
            
        # extract number
        no_match = re.search(r'^(\d{1,2})\.', block)
        if not no_match:
            continue
        no = int(no_match.group(1))
        
        # Now find A, B, C, D
        # We split by \nA., \nB., \nC., \nD.
        parts = re.split(r'\n(?=[A-D]\.)', block)
        
        question_text = parts[0]
        # remove the '1.' prefix
        question_text = re.sub(r'^\d{1,2}\.', '', question_text).strip()
        
        choices = []
        for p in parts[1:]:
            p = p.strip()
            # remove A., B. prefix
            p = re.sub(r'^[A-D]\.', '', p).strip()
            choices.append(p)
            
        questions.append({
            "no": no,
            "question": question_text,
            "choices": choices
        })
        
    return questions

def main():
    pdf_path = r"C:\Users\star0\Desktop\刷題系統\歷屆考題\微生物學與臨床微生物學_merge.pdf"
    print("Reading PDF...")
    ans_pages, q_pages, doc = split_first_exam(pdf_path)
    
    print("Parsing Answers...")
    ans_dict = parse_answers(doc, ans_pages)
    print(f"Parsed {len(ans_dict)} answers.")
    
    print("Parsing Questions...")
    questions = parse_questions(doc, q_pages)
    print(f"Parsed {len(questions)} questions.")
    
    # Merge
    merged = []
    for q in questions:
        ans = ans_dict.get(q["no"], "#")
        merged.append({
            "no": q["no"],
            "question": q["question"],
            "choices": q["choices"],
            "answer": ans
        })
        
    with open("regex_first_exam.json", "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
        
    print(f"Extraction complete! Saved to regex_first_exam.json")
    
if __name__ == "__main__":
    main()

