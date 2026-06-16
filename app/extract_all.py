import os
import json
import re
import fitz
import glob

def parse_answers(doc, ans_page_id):
    page = doc.load_page(ans_page_id)
    text = page.get_text()
    
    trans = str.maketrans("ＡＢＣＤ", "ABCD")
    text = text.translate(trans)
    
    lines = text.split('\n')
    answers = []
    for line in lines:
        line = line.strip()
        if line in ['A', 'B', 'C', 'D', '#']:
            answers.append(line)
        elif line.startswith('答案'):
            ans = line.replace('答案', '').strip()
            if ans in ['A', 'B', 'C', 'D', '#']:
                answers.append(ans)
    return answers

def parse_questions(doc, q_pages):
    full_text = ""
    for pid in q_pages:
        full_text += doc.load_page(pid).get_text() + "\n"
        
    blocks = re.split(r'\n(?=\d{1,2}\.)', full_text)
    
    questions = []
    for block in blocks:
        block = block.strip()
        if not block or not re.match(r'^\d{1,2}\.', block):
            continue
            
        no_match = re.search(r'^(\d{1,2})\.', block)
        if not no_match:
            continue
        no = int(no_match.group(1))
        
        parts = re.split(r'\n(?=[A-D]\.)', block)
        
        question_text = parts[0]
        question_text = re.sub(r'^\d{1,2}\.', '', question_text).strip()
        
        choices = []
        for p in parts[1:]:
            p = p.strip()
            p = re.sub(r'^[A-D]\.', '', p).strip()
            choices.append(p)
            
        # Clean up question text and choices (e.g. remove pagination noise)
        question_text = re.sub(r'\n\s*---\s*PAGE.*', '', question_text)
        question_text = re.sub(r'\s+', ' ', question_text).strip()
        choices = [re.sub(r'\s+', ' ', c).strip() for c in choices]
        
        questions.append({
            "no": no,
            "question": question_text,
            "choices": choices
        })
        
    return questions

def process_pdf(pdf_path):
    print(f"\nProcessing {os.path.basename(pdf_path)}...")
    doc = fitz.open(pdf_path)
    
    exams = []
    current_ans_page = -1
    current_q_pages = []
    
    for i in range(len(doc)):
        text = doc.load_page(i).get_text()
        if "測驗式試題標準答案" in text:
            if current_ans_page != -1 and current_q_pages:
                # We finished an exam block
                exams.append((current_ans_page, current_q_pages))
            current_ans_page = i
            current_q_pages = []
        else:
            if current_ans_page != -1:
                current_q_pages.append(i)
                
    # Add the last one
    if current_ans_page != -1 and current_q_pages:
        exams.append((current_ans_page, current_q_pages))
        
    print(f"Found {len(exams)} exams in this PDF.")
    
    all_questions_for_subject = []
    exam_idx = 1
    
    for ans_page, q_pages in exams:
        answers = parse_answers(doc, ans_page)
        questions = parse_questions(doc, q_pages)
        
        if len(answers) != len(questions):
            print(f"  Warning: Exam {exam_idx} has {len(questions)} questions but {len(answers)} answers. Fixing by truncation or padding.")
        
        for idx, q in enumerate(questions):
            ans = answers[idx] if idx < len(answers) else "#"
            all_questions_for_subject.append({
                "exam_id": exam_idx,
                "no": q["no"],
                "question": q["question"],
                "choices": q["choices"],
                "answer": ans
            })
        exam_idx += 1
        
    return all_questions_for_subject

def main():
    pdf_dir = r"C:\Users\star0\Desktop\刷題系統\歷屆考題"
    output_dir = r"C:\Users\star0\Desktop\刷題系統\app\data"
    os.makedirs(output_dir, exist_ok=True)
    
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    total_q = 0
    for pdf_path in pdf_files:
        subject_name = os.path.basename(pdf_path).replace(".pdf", "").replace("_merge", "")
        questions = process_pdf(pdf_path)
        
        out_path = os.path.join(output_dir, f"{subject_name}.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(questions, f, ensure_ascii=False, indent=2)
            
        print(f"Saved {len(questions)} questions for {subject_name} to {out_path}")
        total_q += len(questions)
        
    print(f"\nAll done! Extracted a total of {total_q} questions.")

if __name__ == "__main__":
    main()

