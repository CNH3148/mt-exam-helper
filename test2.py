import urllib.request, json
req = urllib.request.Request('http://127.0.0.1:8080/data/%E8%87%A8%E5%BA%8A%E7%94%9F%E7%90%86%E5%AD%B8%E8%88%87%E7%97%85%E7%90%86%E5%AD%B8.json?v=123')
res = urllib.request.urlopen(req).read().decode('utf-8')
data = json.loads(res)
matches = [q for q in data if q.get('exam_id') == 1 and q.get('no') == 5]
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(str(matches))

