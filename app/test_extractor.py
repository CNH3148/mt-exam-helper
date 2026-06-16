import os
import json
import fitz
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List

# Set up API key
API_KEY = "<YOUR_GEMINI_API_KEY>"
client = genai.Client(api_key=API_KEY)

class PreMMLUDatasetItem(BaseModel):
    no: int
    question: str
    choices: List[str]

class PreAnswerItem(BaseModel):
    no: int
    answer: str

def split_first_exam(pdf_path):
    doc = fitz.open(pdf_path)
    ans_pages = []
    q_pages = []
    
    # Simple logic to find the first exam based on our previous observation
    # Page 0 is Answer Key, Page 1-15 is questions. Page 16 is next Answer Key.
    ans_pages.append(0)
    for i in range(1, len(doc)):
        text = doc.load_page(i).get_text()
        if "測驗式試題標準答案" in text:
            break
        q_pages.append(i)
        
    ans_doc = fitz.open()
    ans_doc.insert_pdf(doc, from_page=ans_pages[0], to_page=ans_pages[0])
    ans_doc.save("temp_ans.pdf")
    
    q_doc = fitz.open()
    q_doc.insert_pdf(doc, from_page=q_pages[0], to_page=q_pages[-1])
    q_doc.save("temp_q.pdf")
    
    return "temp_q.pdf", "temp_ans.pdf"

def extract_questions(q_pdf_path):
    prompt = """
    Please recognize the content of the file and extract the content of the file, then recompose the content into json format,
    the format should match MMLU Dataset format.
    Ensure you extract the question number (no), the question text (question), and the choices as a list of strings (choices).
    """
    
    with open(q_pdf_path, "rb") as f:
        pdf_bytes = f.read()
        
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=[
            types.Part.from_bytes(data=pdf_bytes, mime_type="application/pdf"),
            prompt,
        ],
        config={
            "response_mime_type": "application/json",
            "response_schema": list[PreMMLUDatasetItem],
        },
    )
    return json.loads(response.text)

def extract_answers(ans_pdf_path):
    prompt = """
    Please recognize the content of the file and extract the content of the file, then recompose the content into json format,
    you shold follow the rules below:
    1. only parse the question number and answer, and the format should match PreAnswerItem format.
    2. the question number should be an integer
    3. the answer should be a string (A, B, C, or D)
    """
    
    with open(ans_pdf_path, "rb") as f:
        pdf_bytes = f.read()
        
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

def main():
    pdf_path = r"C:\Users\star0\Desktop\刷題系統\歷屆考題\微生物學與臨床微生物學_merge.pdf"
    print("Splitting PDF...")
    q_pdf, ans_pdf = split_first_exam(pdf_path)
    
    print("Extracting Answers via Gemini...")
    answers = extract_answers(ans_pdf)
    
    print("Extracting Questions via Gemini...")
    questions = extract_questions(q_pdf)
    
    # Merge
    ans_dict = {a["no"]: a["answer"] for a in answers}
    
    merged = []
    for q in questions:
        ans = ans_dict.get(q["no"], "#")
        merged.append({
            "no": q["no"],
            "question": q["question"],
            "choices": q["choices"],
            "answer": ans
        })
        
    with open("first_exam.json", "w", encoding="utf-8") as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)
        
    print(f"Extraction complete! Extracted {len(merged)} questions.")
    
if __name__ == "__main__":
    main()

