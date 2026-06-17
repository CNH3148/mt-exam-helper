import json
with open('app/data/微生物學與臨床微生物學.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for q in data[:100]:
    if 'images' in q and q['images']:
        print(f"Question {q['no']} has images: {q['images']}")

