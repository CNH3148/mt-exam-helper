import os
import json
import fitz
import glob
import time
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Optional

API_KEY = "<YOUR_GEMINI_API_KEY>"
client = genai.Client(api_key=API_KEY)

class PreMMLUDatasetItem(BaseModel):
    no: int
    question: str
    choices: List[str]

class ExamContent(BaseModel):
    year: int
    term: int
    subject: str
    questions: List[PreMMLUDatasetItem]

class PreAnswerItem(BaseModel):
    no: int
    answer: str

def extract_answers_gemini(ans_pdf_path):
    prompt = """
    Please recognize the content of the file and extract the content of the file, then recompose the content into json format,
    you shold follow the rules below:
    1. only parse the question number and answer, and the format should match PreAnswerItem format.
    2. the question number should be an integer
    3. the answer should be a string (A, B, C, D, or #)
    """
    with open(ans_pdf_path, "rb") as f:
        pdf_bytes = f.read()
        
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[
                    types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                    prompt,
                ],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": list[PreAnswerItem],
                },
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"API Error Answers: {e}, retrying...")
            time.sleep(5)
    return []

def extract_questions_gemini(q_pdf_path):
    prompt = """
    Extract all the test questions from this exam paper.
    Also, look at the first page header to extract the exam 'year' (e.g., 113), the 'term' (e.g., 1 for 第一次, 2 for 第二次), and the 'subject'.
    Ensure you extract the question number (no), the exact question text (question), and the choices as a list of strings.
    Do NOT merge option texts (A, B, C, D) into the question text. Keep them in choices.
    """
    with open(q_pdf_path, "rb") as f:
        pdf_bytes = f.read()
        
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[
                    types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
                    prompt,
                ],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": ExamContent,
                },
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"API Error Questions: {e}, retrying...")
            time.sleep(5)
    return None

def extract_images_from_pages(doc, q_pages, subject_name, exam_idx, output_img_dir):
    # Map images geometrically with width/height filtering
    img_mappings = {}
    
    for pid in q_pages:
        page = doc.load_page(pid)
        images = page.get_images()
        if not images:
            continue
            
        blocks = page.get_text("blocks")
        q_positions = []
        import re
        for b in blocks:
            text = b[4].strip()
            match = re.match(r'^(\d{1,2})\.', text)
            if match:
                q_num = int(match.group(1))
                q_positions.append((q_num, b[1]))
                
        if not q_positions:
            continue
        q_positions.sort(key=lambda x: x[1])
        
        for img_idx, img in enumerate(images):
            xref = img[0]
            width, height = img[2], img[3]
            
            # FILTER: Ignore very small images (watermarks, separators)
            if width < 50 or height < 50:
                continue
                
            rects = page.get_image_rects(xref)
            if not rects:
                continue
                
            img_y0 = rects[0].y0
            
            assigned_q_num = None
            for q in reversed(q_positions):
                if q[1] <= img_y0 + 10:
                    assigned_q_num = q[0]
                    break
                    
            if assigned_q_num is None:
                assigned_q_num = q_positions[0][0]
                
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            img_filename = f"{subject_name}_exam{exam_idx}_q{assigned_q_num}_{img_idx}.{ext}"
            img_filepath = os.path.join(output_img_dir, img_filename)
            
            with open(img_filepath, "wb") as f:
                f.write(image_bytes)
                
            if assigned_q_num not in img_mappings:
                img_mappings[assigned_q_num] = []
            img_mappings[assigned_q_num].append(f"images/{img_filename}")
            
    return img_mappings

def process_pdf(pdf_path, output_dir, output_img_dir):
    subject_name = os.path.basename(pdf_path).replace(".pdf", "").replace("_merge", "")
    print(f"\nProcessing {subject_name} via Gemini...")
    doc = fitz.open(pdf_path)
    
    exams = []
    current_ans_page = -1
    current_q_pages = []
    
    for i in range(len(doc)):
        text = doc.load_page(i).get_text()
        if "測驗式試題標準答案" in text:
            if current_ans_page != -1 and current_q_pages:
                exams.append((current_ans_page, current_q_pages))
            current_ans_page = i
            current_q_pages = []
        else:
            if current_ans_page != -1:
                current_q_pages.append(i)
                
    if current_ans_page != -1 and current_q_pages:
        exams.append((current_ans_page, current_q_pages))
        
    print(f"Found {len(exams)} exams in {subject_name}.")
    
    all_questions = []
    
    for exam_idx, (ans_page, q_pages) in enumerate(exams, 1):
        print(f"  Extracting Exam {exam_idx}...")
        
        # Save temp PDFs for Gemini
        ans_doc = fitz.open()
        ans_doc.insert_pdf(doc, from_page=ans_page, to_page=ans_page)
        ans_doc.save("temp_ans.pdf")
        
        q_doc = fitz.open()
        q_doc.insert_pdf(doc, from_page=q_pages[0], to_page=q_pages[-1])
        q_doc.save("temp_q.pdf")
        
        # Call Gemini
        answers = extract_answers_gemini("temp_ans.pdf")
        exam_content = extract_questions_gemini("temp_q.pdf")
        
        # Image mapping
        img_mappings = extract_images_from_pages(doc, q_pages, subject_name, exam_idx, output_img_dir)
        
        ans_dict = {a["no"]: a["answer"] for a in answers}
        
        if exam_content and exam_content.get("questions"):
            year = exam_content.get("year", 0)
            term = exam_content.get("term", 0)
            subj = exam_content.get("subject", subject_name)
            
            for q in exam_content["questions"]:
                no = q["no"]
                ans = ans_dict.get(no, "#")
                images = img_mappings.get(no, [])
                
                # Format: 113-2-臨床血液學與血庫學-17
                auto_tag = f"{year}-{term}-{subj}-{no}"
                
                all_questions.append({
                    "exam_id": exam_idx,
                    "no": no,
                    "question": q["question"],
                    "choices": q["choices"],
                    "answer": ans,
                    "images": images,
                    "tags": [auto_tag]
                })
        
        # Clean up
        ans_doc.close()
        q_doc.close()
        os.remove("temp_ans.pdf")
        os.remove("temp_q.pdf")
        
    out_path = os.path.join(output_dir, f"{subject_name}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_questions, f, ensure_ascii=False, indent=2)
    print(f"Saved {subject_name} ({len(all_questions)} questions).")

def main():
    pdf_dir = r"C:\Users\star0\Desktop\刷題系統\歷屆考題"
    output_dir = r"C:\Users\star0\Desktop\刷題系統\app\data"
    output_img_dir = r"C:\Users\star0\Desktop\刷題系統\app\public\images"
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(output_img_dir, exist_ok=True)
    
    pdf_files = glob.glob(os.path.join(pdf_dir, "*.pdf"))
    
    for pdf_path in pdf_files:
        # We can process all of them
        process_pdf(pdf_path, output_dir, output_img_dir)
        
if __name__ == "__main__":
    main()

