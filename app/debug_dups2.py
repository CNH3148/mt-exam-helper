import json

def check_exam_tags():
    with open('data/微生物學與臨床微生物學.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    exam_tag_map = {}
    for q in data:
        exam_id = q['exam_id']
        if q.get('tags') and len(q['tags']) > 0:
            match = q['tags'][0].split('-')[:2]
            year = "-".join(match)
            if exam_id not in exam_tag_map:
                exam_tag_map[exam_id] = set()
            exam_tag_map[exam_id].add(year)
            
    for e_id in sorted(exam_tag_map.keys()):
        print(f"Exam {e_id}: {exam_tag_map[e_id]}")

check_exam_tags()

