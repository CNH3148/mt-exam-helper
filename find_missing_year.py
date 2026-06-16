import json
import glob
files = glob.glob('app/data/*.json')
count = 0
for f in files:
    if 'topics_' in f or 'taxonomy_' in f: continue
    if 'saved_searches' in f: continue
    data = json.load(open(f, encoding='utf-8'))
    for q in data:
        has_year = False
        for t in q.get('tags', []):
            if '-' in t and t[:3].isdigit():
                has_year = True
        if not has_year:
            print(f"Missing year tag in {f}: Exam {q.get('exam_id')} No {q.get('no')} - {q.get('question')[:50]}")
            count += 1
print(f'Total missing year tags: {count}')

