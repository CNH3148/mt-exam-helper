import json, glob, os
count = 0
for f in glob.glob('app/data/*.json'):
    base = os.path.basename(f)
    if base.startswith('topics_') or base.startswith('taxonomy_') or base.startswith('regex'): continue
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        for q in data:
            if 'year' not in q or not q['year']:
                count += 1
                print(f'Missing year in {f}: {q.get("exam_id")}-{q.get("no")}')
print(f'Total missing year: {count}')

