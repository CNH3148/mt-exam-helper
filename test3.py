import json
data = json.load(open('app/data/臨床生理學與病理學.json', encoding='utf-8'))
print(len([q for q in data if q.get('no') == 5]))

