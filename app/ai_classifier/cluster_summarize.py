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

model = genai.GenerativeModel('gemini-2.5-pro')

def main(subject_name):
    data_path = rf"C:\Users\star0\Desktop\刷題系統\app\data\{subject_name}.json"
    tax_path = rf"C:\Users\star0\Desktop\刷題系統\app\data\taxonomy_{subject_name}.json"
    out_path = rf"C:\Users\star0\Desktop\刷題系統\app\data\topics_{subject_name}.json"
    
    if not os.path.exists(data_path) or not os.path.exists(tax_path):
        print("Missing data files.")
        return

    with open(data_path, "r", encoding="utf-8") as f:
        questions = json.load(f)

    with open(tax_path, "r", encoding="utf-8") as f:
        taxonomy = json.load(f)
        
    topic_summaries = {}
    if os.path.exists(out_path):
        with open(out_path, "r", encoding="utf-8") as f:
            topic_summaries = json.load(f)

    grouped = {}
    for q in questions:
        t = q.get("topic")
        if t:
            if t not in grouped:
                grouped[t] = []
            grouped[t].append(q)

    print(f"Loaded {len(grouped)} populated topics.")

    for idx, tax in enumerate(taxonomy):
        topic_name = tax["topic"]
        if topic_name in topic_summaries:
            continue
        
        qs = grouped.get(topic_name, [])
        if not qs:
            continue
            
        print(f"Summarizing {idx+1}/{len(taxonomy)}: {topic_name} ({len(qs)} questions)...")
        
        simplified_qs = []
        # USE ALL QUESTIONS AS REQUESTED!
        for q in qs:
            simplified_qs.append(q["question"] + " / 答案: " + q["answer"])

        prompt = f"""
你是一位權威的醫事檢驗師。你正在撰寫國考《{subject_name}》的知識點總結與預測。

知識點名稱：{topic_name}
知識點定義：{tax['definition']}

以下是被歸類在此類別中的「所有歷屆考題」：
{json.dumps(simplified_qs, ensure_ascii=False)}

請你深入分析這些考題，萃取出解題所需的「所有背景知識」，並預測未來可能的考法趨勢。
請嚴格遵守以下格式與排版精神輸出 (直接輸出 Markdown，不要包裝在 code block 裡)：

## 核心趨勢與高頻考點
請簡短總結這個單元中最常考的概念、常見的問法變化，以及知識間的邏輯因果（例如：生理機轉A → 檢驗數值變化B → 臨床診斷C）。

## 關鍵字反射表
請使用「矩陣式對比表格」統整所有考點。
- 縱軸必須是「疾病/病原體/生理狀態」或「檢驗項目」。
- 橫軸是具體的比較維度（如：致病機轉、生化指標變化、尿液試紙反應、鏡檢特徵、干擾物質等）。盡量合併成一個大表格。
- 表格內文請【極致精簡】，絕對不要使用完整的敘述句！一律使用「名詞、短語、箭頭符號 (↑/↓)」。
- 務必將表格內「最具有鑑別度」的字眼加上**粗體**。

## Anki 聯想卡
請根據你整理出的重點，製作適合匯入 Anki 的閃卡。
【嚴格格式要求】
1. 絕對不要產生 Markdown 表格！請將所有卡片內容包裝在一個 ` ``` ` 程式碼區塊內。
2. 每張卡片獨立佔據一行。
3. 卡片的「正面」與「背面」之間，請統一使用「分號 (;)」隔開。
4. 背面內容若需換行，一律使用 `<br>` 代替，絕對不可使用實體換行。
5. 背面的直接答案，請使用 `<ans>答案</ans>` 標籤包覆。
6. 重點字眼請使用 `<b>重點</b>` 包覆。
7. 正面必須極度簡短 (例如單一疾病名、特定異常)；背面第一行為直接答案，空一行 (`<br><br>`) 後列出陷阱或連動知識。

範例：
```
AFP (甲型胎兒蛋白) 【主要應用癌別】？;<ans>肝細胞癌 (HCC) 與 卵黃囊瘤 (Yolk sac tumor)</ans><br><br>📌連動：睪丸腫瘤的診斷常需要將 AFP 與「游離 β-hCG」搭配評估。
肺氣腫 (Emphysema) 【肺臟順應性 (Compliance)】 變化？;<ans>增加</ans><br><br>⚠️陷阱：彈性纖維被破壞，像鬆掉的塑膠袋，容易充氣但無法回縮。
```
"""
        try:
            response = generate_with_retry(model, prompt)
            topic_summaries[topic_name] = response.text.strip()
            
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(topic_summaries, f, ensure_ascii=False, indent=2)
            
            time.sleep(2)
        except Exception as e:
            print(f"Failed to summarize {topic_name}: {e}")

    print("Finished summarizing topics.")

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

