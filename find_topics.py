import json

db_path = 'app/data/生物化學與臨床生化學.json'
with open(db_path, 'r', encoding='utf-8') as f:
    current = json.load(f)

topics_modified = set()
for q in current:
    if q.get('year') == '112-2':
        topic = q.get('topic')
        if topic and topic != '未分類':
            topics_modified.add(topic)

with open('topics.txt', 'w', encoding='utf-8') as f:
    f.write(', '.join(topics_modified))

