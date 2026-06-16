import json
import os
import time
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


API_KEY = "<YOUR_GEMINI_API_KEY>"
genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-2.5-pro', generation_config={"response_mime_type": "application/json"})

def classify_batch(questions, taxonomy, data_path, original_questions):
    valid_topics = [t["topic"] for t in taxonomy]
    batch_size = 50
    updated_count = 0

    for i in range(0, len(questions), batch_size):
        batch_qs = questions[i:i+batch_size]
        
        needs_classification = [q for q in batch_qs if q.get("topic") not in valid_topics]
        if not needs_classification:
            continue

        simplified_qs = []
        for q in needs_classification:
            simplified_qs.append({
                "exam_id": q["exam_id"],
                "no": q["no"],
                "q": q["question"],
                "options": q["choices"]
            })

        print(f"Processing batch ({len(needs_classification)} questions)...")

        prompt = f"""
你是一位權威的「醫事檢驗師國考」命題專家。
我這裡有一份已經制定好的「知識點綱要 (Taxonomy)」：
{json.dumps(taxonomy, ensure_ascii=False)}

我將給你一批考題。請仔細閱讀每一題，並從上述 Taxonomy 中，挑選出「最符合該題測驗核心背景知識」的 1 個 `topic` 名稱。

要求：
1. `topic` 必須「完全等於」我提供的知識點綱要中的其中一個名稱，請勿自行創造新名稱。
2. 即使題目橫跨多個概念，也請選出「最核心」或「最能代表該題考點」的唯一一個類群。

請輸出嚴格的 JSON 陣列格式：
[
  {{
    "exam_id": "題目的 exam_id",
    "no": "題目的 no",
    "topic": "分類的類群名稱"
  }},
  ...
]

以下為考題清單：
{json.dumps(simplified_qs, ensure_ascii=False)}
"""
        try:
            response = generate_with_retry(model, prompt)
            text = response.text.strip()
            if text.startswith('```json'): text = text[7:]
            if text.startswith('```'): text = text[3:]
            if text.endswith('```'): text = text[:-3]
            text = text.strip()
            
            result = json.loads(text)
            
            for res_q in result:
                for q in original_questions:
                    if q["exam_id"] == res_q["exam_id"] and str(q["no"]) == str(res_q["no"]):
                        if res_q["topic"] in valid_topics:
                            q["topic"] = res_q["topic"]
                            updated_count += 1
                        break
            
            with open(data_path, "w", encoding="utf-8") as f:
                json.dump(original_questions, f, ensure_ascii=False, indent=2)
                
            time.sleep(2)
        except Exception as e:
            print(f"Failed on batch: {e}")
            
    return updated_count

def main(subject_name):
    data_path = rf"C:\Users\star0\Desktop\刷題系統\app\data\{subject_name}.json"
    tax_path = rf"C:\Users\star0\Desktop\刷題系統\app\data\taxonomy_{subject_name}.json"
    
    if not os.path.exists(data_path) or not os.path.exists(tax_path):
        print("Missing data files.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    with open(tax_path, "r", encoding="utf-8") as f:
        taxonomy = json.load(f)

    valid_topics = [t["topic"] for t in taxonomy]

    # Retry loop until 100% classified
    max_retries = 5
    for attempt in range(max_retries):
        missing = [q for q in questions if q.get("topic") not in valid_topics]
        if not missing:
            print(f"100% Classification achieved for {subject_name}!")
            break
            
        print(f"Attempt {attempt+1}: {len(missing)} questions need classification.")
        classify_batch(missing, taxonomy, data_path, questions)
        
        with open(data_path, "r", encoding="utf-8") as f:
            questions = json.load(f)
            
    missing_final = [q for q in questions if q.get("topic") not in valid_topics]
    if missing_final:
        print(f"Warning: {len(missing_final)} questions are still unclassified after {max_retries} attempts.")

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

