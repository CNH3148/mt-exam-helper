import json
import os

SUBJECTS = [
    '臨床化學',
    '臨床血液學與血庫學',
    '臨床血清免疫學與臨床病毒學',
    '臨床生理學與病理學',
    '醫學分子檢驗學與臨床鏡檢學',
    '微生物學與臨床微生物學',
    '生物化學與臨床生化學'
]

for sub in SUBJECTS:
    data_path = f'app/data/{sub}.json'
    topics_path = f'app/data/topics_{sub}.json'
    
    if not os.path.exists(data_path):
        continue
        
    try:
        with open(topics_path, encoding='utf-8') as f:
            topics = json.load(f)
        with open(data_path, encoding='utf-8') as f:
            data = json.load(f)
            
        topics_in_data = set(q.get('topic') for q in data if q.get('topic') and q.get('topic') != '未分類')
        missing = topics_in_data - set(topics.keys())
        
        has_113_2 = any(q.get('year') == '113-2' for q in data)
        
        print(f"[{sub}]")
        print(f" - Contains 113-2: {has_113_2}")
        print(f" - Topics in data: {len(topics_in_data)}, Summaries: {len(topics.keys())}")
        if missing:
            print(f"   => Missing summaries: {len(missing)}")
    except Exception as e:
        print(f"[{sub}] ERROR: {e}")

