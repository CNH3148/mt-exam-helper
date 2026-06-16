import json

for sub in ['醫學分子檢驗學與臨床鏡檢學', '臨床血液學與血庫學']:
    with open(f'app/data/{sub}.json', encoding='utf-8') as f:
        data = json.load(f)
    missing = [q for q in data if q.get('year') == '113-2' and q.get('topic') in [None, '', '未分類']]
    total_113_2 = [q for q in data if q.get('year') == '113-2']
    print(f"{sub}: 113-2 has {len(total_113_2)} total questions, {len(missing)} unclassified.")
    
    missing_all = [q for q in data if q.get('topic') in [None, '', '未分類']]
    print(f"{sub}: TOTAL unclassified: {len(missing_all)}")

