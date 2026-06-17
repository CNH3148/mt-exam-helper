import json
import sys

with open('app/data/醫學分子檢驗學與臨床鏡檢學.json', encoding='utf-8') as f:
    data = json.load(f)
with open('app/data/topics_醫學分子檢驗學與臨床鏡檢學.json', encoding='utf-8') as f:
    topics = json.load(f)

known = set(topics.keys())
unknown_qs = [q for q in data if q.get('topic') not in known]
print(f"Unknown questions in Medical Molecular: {len(unknown_qs)}")

