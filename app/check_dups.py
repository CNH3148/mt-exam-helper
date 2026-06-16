import json, glob, collections, os

dups = 0
for f in glob.glob('app/data/*.json'):
    base = os.path.basename(f)
    if base.startswith('topics_') or base.startswith('taxonomy_') or base.startswith('regex'): continue
    with open(f, 'r', encoding='utf-8') as file:
        data = json.load(file)
        ids = [f"{q.get('exam_id')}-{q.get('no')}" for q in data]
        c = collections.Counter(ids)
        for k, v in c.items():
            if v > 1:
                print(f'Duplicate {k} in {f}')
                dups += 1
print(f'Total duplicates: {dups}')

