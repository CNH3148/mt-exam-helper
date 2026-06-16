import os
import json
import time
import asyncio
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Optional

API_KEY = "<YOUR_GEMINI_API_KEY>"
client = genai.Client(api_key=API_KEY)

SUBJECTS = [
    '臨床生理學與病理學',
    '臨床血液學與血庫學',
    '醫學分子檢驗學與臨床鏡檢學',
    '微生物學與臨床微生物學',
    '生物化學與臨床生化學',
    '臨床血清免疫學與臨床病毒學'
]

class KeyConceptExtraction(BaseModel):
    key_concept: str

async def extract_key_concept(q, semaphore):
    async with semaphore:
        prompt = f"""
        Question: {q.get('question')}
        Choices: {json.dumps(q.get('choices'), ensure_ascii=False)}
        Answer: {q.get('answer')}
        
        Task:
        提取這道醫檢師國考題的「破題關鍵」或「解題所需核心背景知識」。
        請用「繁體中文」寫出「精簡的一句話」。
        """
        
        for attempt in range(4):
            try:
                # To use async client:
                response = await client.aio.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=[prompt],
                    config={
                        "response_mime_type": "application/json",
                        "response_schema": KeyConceptExtraction,
                        "temperature": 0.1
                    }
                )
                res = json.loads(response.text)
                return res['key_concept']
            except Exception as e:
                # Retry logic
                await asyncio.sleep(2 ** attempt)
                
        print(f"Failed to extract for question {q.get('tags', [''])[0]}")
        return "無法提取"

async def process_subject(subject):
    print(f"========== Processing {subject} ==========")
    db_path = f"app/data/{subject}.json"
    
    if not os.path.exists(db_path):
        print("Database missing, skipping.")
        return
        
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    # Find questions that need processing
    tasks_q = []
    for q in data:
        if not q.get('key_concept') or q.get('key_concept') == '無法提取':
            tasks_q.append(q)
            
    if not tasks_q:
        print(f"[{subject}] All questions already have key_concept.")
        return
        
    print(f"[{subject}] Extracting key concepts for {len(tasks_q)} questions...")
    
    # Process with semaphore
    semaphore = asyncio.Semaphore(50) # 50 concurrent requests for Flash
    
    async def process_q(q):
        kc = await extract_key_concept(q, semaphore)
        q['key_concept'] = kc
        
    batch_size = 200
    for i in range(0, len(tasks_q), batch_size):
        batch = tasks_q[i:i+batch_size]
        print(f"[{subject}] Processing batch {i//batch_size + 1}/{(len(tasks_q)+batch_size-1)//batch_size}...")
        await asyncio.gather(*(process_q(q) for q in batch))
        
        # Save incrementally
        with open(db_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            
    print(f"[{subject}] Finished extracting.")

async def main():
    for sub in SUBJECTS:
        await process_subject(sub)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        asyncio.run(process_subject(sys.argv[1]))
    else:
        asyncio.run(main())

