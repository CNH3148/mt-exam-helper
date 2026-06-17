import json
with open('app/data/臨床血液學與血庫學.json', encoding='utf-8') as f:
    data = json.load(f)

for q in data:
    if q.get('topic'):
        print(json.dumps(q, ensure_ascii=False, indent=2))
        break

