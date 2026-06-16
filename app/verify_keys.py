import json
data = json.load(open('app/data/生物化學與臨床生化學.json', encoding='utf-8'))
cnt = 0
for q in data:
    if q.get('key_concept') and q.get('key_concept') != '無法提取':
        print(f"Q: {q['question']}")
        print(f"Key: {q['key_concept']}\n")
        cnt += 1
        if cnt >= 3:
            break

