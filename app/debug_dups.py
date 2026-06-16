import json
from collections import Counter

def check_duplicates():
    with open('data/微生物學與臨床微生物學.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    exam_counts = Counter([q['exam_id'] for q in data])
    print('Total questions:', len(data))
    print('Exam counts:', exam_counts)
    
    # Let's see tags for exam_id = 110-1 or something. 
    # Actually exam_id is an integer (1 to 11).
    # Tags contain year like "110-1"
    
    year_counts = Counter()
    for q in data:
        if q.get('tags') and len(q['tags']) > 0:
            match = q['tags'][0].split('-')[:2]
            year = "-".join(match)
            year_counts[year] += 1
            
    print('Year tag counts:', year_counts)

check_duplicates()

