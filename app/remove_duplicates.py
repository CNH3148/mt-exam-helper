import json
import os
import glob

def deduplicate_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    unique_questions = []
    seen = set()
    dup_count = 0
    
    for q in data:
        if q.get('tags') and len(q['tags']) > 0:
            uid = q['tags'][0]
        else:
            uid = q['question'] + str(q['no'])
            
        if uid not in seen:
            seen.add(uid)
            unique_questions.append(q)
        else:
            # We want to preserve the topic if the duplicate happened to be classified
            # But the one we already appended might not have a topic, while the duplicate might!
            if 'topic' in q and 'topic' not in unique_questions[-1]:
                # Update the preserved one with the topic
                for uq in unique_questions:
                    if (uq.get('tags') and len(uq['tags']) > 0 and uq['tags'][0] == uid) or (uq['question'] + str(uq['no']) == uid):
                        uq['topic'] = q['topic']
            dup_count += 1
            
    if dup_count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(unique_questions, f, ensure_ascii=False, indent=2)
        print(f"Removed {dup_count} duplicates from {os.path.basename(filepath)}. Now has {len(unique_questions)} questions.")
    else:
        print(f"No duplicates in {os.path.basename(filepath)}. ({len(unique_questions)} questions)")

def main():
    data_dir = r"C:\Users\star0\Desktop\刷題系統\app\data"
    for file in glob.glob(os.path.join(data_dir, "*.json")):
        if "taxonomy" in file or "topics" in file:
            continue
        deduplicate_json(file)

if __name__ == "__main__":
    main()

