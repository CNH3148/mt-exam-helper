# -*- coding: utf-8 -*-
import json
import os
import time
from pathlib import Path
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Optional

# API Key and Client initialization
API_KEY = "<YOUR_GEMINI_API_KEY>"
client = genai.Client(api_key=API_KEY)

# Define target JSON directory
json_dir = Path("C:/Users/star0/Desktop/刷題系統/app/data")

# Pydantic schemas for structured output
class ExplanationItem(BaseModel):
    no: int
    topic: str
    explanation: str

class ExplanationBatch(BaseModel):
    results: List[ExplanationItem]

def generate_batch_explanations(subject: str, questions: list) -> dict:
    """
    Sends a batch of questions to Gemini 2.5 Flash for explanation and knowledge point extraction.
    Returns a dictionary mapping question `no` to its `topic` and `explanation`.
    """
    # Construct the prompt text for the batch
    prompt = f"你現在是一位資深的醫事檢驗師國考名師。請為以下《{subject}》的選擇題生成「高質量的考題詳解」與「知識點歸納」。\n\n"
    prompt += "要求：\n"
    prompt += "1. topic (知識點分類)：請用 5~15 字精確總結這題測驗的核心知識單元（例如：免疫球蛋白結構、血液凝固機轉）。\n"
    prompt += "2. explanation (詳解)：解析為何正確選項是錯的/對的，並提煉出「必背關鍵字」或口訣。字數大約 150~300 字內，要排版易讀。\n\n"
    
    prompt += "以下是本次需要解析的題目：\n"
    for q in questions:
        prompt += f"--- 題號: {q['no']} ---\n"
        prompt += f"題目: {q['question']}\n"
        for i, choice in enumerate(q['choices']):
            prompt += f"選項 {'ABCD'[i]}: {choice}\n"
        prompt += f"正確答案: {q['answer']}\n"
    
    # Retry mechanism for API calls
    for attempt in range(3):
        try:
            # Using flash to save money and time
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "response_schema": ExplanationBatch,
                    "temperature": 0.3,
                },
            )
            
            # Parse the JSON response
            output = json.loads(response.text)
            
            # Map results
            results_map = {}
            for res in output.get("results", []):
                results_map[res["no"]] = {
                    "topic": res["topic"],
                    "explanation": res["explanation"]
                }
            return results_map
            
        except Exception as e:
            print(f"API Error (Attempt {attempt+1}): {e}")
            time.sleep(5)
            
    return {}

def process_subject(file_path: Path):
    print(f"Loading {file_path.name}...")
    data = json.loads(file_path.read_text(encoding="utf-8"))
    
    # Identify questions that need explanation
    pending_questions = [q for q in data if "explanation" not in q or "topic" not in q]
    
    if not pending_questions:
        print(f"  All questions in {file_path.name} already have explanations. Skipping.")
        return
        
    print(f"  {len(pending_questions)} questions pending. Starting batch processing...")
    
    batch_size = 10
    total_processed = 0
    
    for i in range(0, len(pending_questions), batch_size):
        batch = pending_questions[i:i+batch_size]
        print(f"    Processing batch {i//batch_size + 1} ({len(batch)} questions)...")
        
        results_map = generate_batch_explanations(file_path.stem, batch)
        
        if not results_map:
            print("    Failed to generate batch. Skipping for now.")
            continue
            
        # Apply results back to the original data structure
        updated_count = 0
        for q in data:
            if q["no"] in results_map and q in batch:
                q["topic"] = results_map[q["no"]]["topic"]
                q["explanation"] = results_map[q["no"]]["explanation"]
                updated_count += 1
                total_processed += 1
                
        # Save after every batch to prevent data loss
        if updated_count > 0:
            file_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            
        # Respect rate limits
        time.sleep(1)
        
    print(f"  Finished {file_path.name}. Added explanations to {total_processed} questions.\n")

def run():
    for json_file in json_dir.glob("*.json"):
        process_subject(json_file)

if __name__ == "__main__":
    run()

