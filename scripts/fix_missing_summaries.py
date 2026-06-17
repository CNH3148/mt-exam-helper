import json
import os
import time

try:
    from openai import OpenAI
except ImportError:
    print("Please run: pip install openai")
    exit(1)

client = OpenAI()

def update_missing_summaries(subject):
    print(f"Checking {subject}...")
    db_path = f"app/data/{subject}.json"
    tax_path = f"app/data/taxonomy_{subject}.json"
    topics_path = f"app/data/topics_{subject}.json"
    
    if not os.path.exists(db_path) or not os.path.exists(tax_path) or not os.path.exists(topics_path):
        return

    with open(db_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    with open(tax_path, 'r', encoding='utf-8') as f:
        taxonomy = json.load(f)
    with open(topics_path, 'r', encoding='utf-8') as f:
        topics = json.load(f)

    # Find all topics that exist in data but not in topics.json
    all_topics_in_data = set(q.get('topic') for q in data if q.get('topic') and q.get('topic') != '未分類')
    missing_topics = all_topics_in_data - set(topics.keys())
    
    if not missing_topics:
        print(f"  [{subject}] All summaries are up-to-date!")
        return

    print(f"  [{subject}] Found {len(missing_topics)} missing summaries.")
    
    # Generate missing summaries
    for t in missing_topics:
        print(f"  -> Generating summary for: {t}")
        # Find the definition from taxonomy
        definition = next((x['definition'] for x in taxonomy if x['topic'] == t), "自動生成之定義。")
        
        prompt = f"""
請為醫學檢驗與生物技術學系國考科目「{subject}」中的這個知識點（類群）撰寫一段整體的重點說明，以及該類群必須掌握的核心關鍵字。
請使用 Markdown 格式，並包含兩個區塊：
1. **整體說明**（約 100~150 字，說明此類群的國考重點與常考概念）
2. **必備關鍵字**（列出 5~10 個專有名詞或重要指標）

類群名稱：{t}
類群定義/涵蓋範圍：{definition}

輸出格式必須如下（請直接輸出 Markdown 內容，不要加上 ```markdown）：
# {t}
（整體說明內容...）
### 必備關鍵字
- 關鍵字1
- 關鍵字2
"""
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "你是一位專業的醫學檢驗國考導師，擅長歸納考題重點並撰寫精簡扼要的複習指引。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
            )
            content = response.choices[0].message.content.strip()
            # remove markdown backticks if any
            if content.startswith("```markdown"): content = content[11:]
            if content.startswith("```"): content = content[3:]
            if content.endswith("```"): content = content[:-3]
            
            topics[t] = content.strip()
            print(f"     Done.")
            time.sleep(1) # rate limit prevention
        except Exception as e:
            print(f"     Failed to generate for {t}: {e}")
            
    # Save back to topics.json
    with open(topics_path, 'w', encoding='utf-8') as f:
        json.dump(topics, f, ensure_ascii=False, indent=4)
    print(f"  [{subject}] Updated topics_*.json successfully.")

if __name__ == "__main__":
    subjects = [
        "醫學分子檢驗學與臨床鏡檢學",
        "臨床血液學與血庫學",
        "臨床生理學與病理學",
        "微生物學與臨床微生物學",
        "生物化學與臨床生化學",
        "臨床血清免疫學與臨床病毒學"
    ]
    for s in subjects:
        update_missing_summaries(s)
    print("All missing summaries have been checked and updated!")

