import json
import os
import google.generativeai as genai

import random
import time
def generate_with_retry(model, prompt, max_retries=10, initial_delay=5):
    delay = initial_delay
    for i in range(max_retries):
        try:
            return model.generate_content(prompt)
        except Exception as e:
            err_msg = str(e)
            if "429" in err_msg or "ResourceExhausted" in err_msg or "Quota" in err_msg:
                if i == max_retries - 1:
                    raise e
                sleep_time = delay + random.uniform(0, 2)
                print(f"API Rate limit hit. Retrying in {sleep_time:.2f} seconds... (Attempt {i+1}/{max_retries})")
                time.sleep(sleep_time)
                delay *= 1.5  # Exponential backoff
            else:
                raise e


# Setup API Key
API_KEY = "<YOUR_GEMINI_API_KEY>"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-pro', generation_config={"response_mime_type": "application/json"})

def main(subject_name):
    data_path = rf"C:\Users\star0\Desktop\刷題系統\app\data\{subject_name}.json"
    out_path = rf"C:\Users\star0\Desktop\刷題系統\app\data\taxonomy_{subject_name}.json"
    syllabus_path = r"C:\Users\star0\Desktop\刷題系統\app\data\syllabus.txt"
    
    if not os.path.exists(data_path):
        print(f"File not found: {data_path}")
        return
        
    if os.path.exists(out_path):
        print(f"Taxonomy already exists: {out_path}. Skipping.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        questions = json.load(f)
        
    syllabus_text = ""
    if os.path.exists(syllabus_path):
        with open(syllabus_path, "r", encoding="utf-8") as f:
            syllabus_text = f.read()

    print(f"Loaded {len(questions)} questions for {subject_name}.")

    simplified_qs = []
    for q in questions:
        simplified_qs.append({
            "no": q["no"],
            "q": q["question"],
            "options": q["choices"]
        })

    prompt = f"""
你是一位權威的「醫事檢驗師國考」{subject_name}的命題專家。
我將給你本科目過去幾年的所有歷屆考題 (共 {len(questions)} 題)。

你的任務是進行「由上而下 (Top-Down)」的知識點萃取。
請仔細閱讀這些題目，並將它們所測驗的核心醫學知識進行歸納，建立一份系統性的「知識點綱要 (Taxonomy)」。

要求：
1. 請設計約 30 到 50 個「知識點類群 (Topics)」。
2. 分類標準必須是「解題所需背景知識的接近程度」。例如：考驗相同細菌特性、相同抗生素機轉、或相同培養基特性的題目應在同一類群。
3. 類群名稱必須專業、明確。不要使用過於籠統的名稱 (如: 其他)。
4. 請針對每個類群給出明確的 `definition` (定義與涵蓋範圍)，說明哪種類型的題目應該被分到這個類群。
5. 取消常態性設立「綜合性考題」的機制。只有當題目真正極端跨域時，才允許給出跨域標籤；平常則強制必須選擇最核心的一個單元。

請輸出嚴格的 JSON 陣列格式：
[
  {{
    "topic": "類群名稱",
    "definition": "該類群涵蓋的知識點範圍與題目類型說明"
  }},
  ...
]

以下為考選部官方命題大綱 (僅供參考，請以此為輔助，仍須依據「解題所需背景知識」進行分類)：
{syllabus_text}

以下為所有題目的清單：
{json.dumps(simplified_qs, ensure_ascii=False)}
"""

    print("Sending request to Gemini 2.5 Pro... This may take a few minutes.")
    response = generate_with_retry(model, prompt)
    
    try:
        text = response.text.strip()
        if text.startswith('```json'): text = text[7:]
        if text.startswith('```'): text = text[3:]
        if text.endswith('```'): text = text[:-3]
        text = text.strip()
            
        result = json.loads(text)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        print(f"Successfully generated taxonomy with {len(result)} topics.")
    except Exception as e:
        print("Failed to parse JSON response.")
        print(response.text)
        print("Error:", e)

if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sub = os.environ.get("SUBJECT_NAME")
    if len(sys.argv) > 1 and sys.argv[1].strip():
        sub = sys.argv[1]
    if sub:
        main(sub)
    else:
        print("Please provide subject name.")

