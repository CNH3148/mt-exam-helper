import urllib.request, json
data = json.dumps({'subject': '臨床生理學與病理學', 'year': '115-1', 'exam_id': 1, 'no': 5, 'new_answer': 'AD'}).encode('utf-8')
req = urllib.request.Request('http://127.0.0.1:8080/api/update_correct_answer', data=data, headers={'Content-Type': 'application/json'})
print(urllib.request.urlopen(req).read().decode('utf-8'))

