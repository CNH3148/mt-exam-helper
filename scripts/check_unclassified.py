import json

for sub in ['醫學分子檢驗學與臨床鏡檢學', '臨床血液學與血庫學']:
    with open(f'app/data/{sub}.json', encoding='utf-8') as f:
        data = json.load(f)
    unclassified = [q for q in data if not q.get('topic') or q.get('topic') == '未分類']
    print(f"{sub}: {len(unclassified)} unclassified")

