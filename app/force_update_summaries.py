import json
import os
import time
from enhanced_classify import update_topic_summary

def force_update_summaries(subject):
    db_path = f"app/data/{subject}.json"
    topics_path = f"app/data/topics_{subject}.json"
    
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    with open(topics_path, "r", encoding="utf-8") as f:
        topic_summaries = json.load(f)
        
    topics_modified = set()
    for q in data:
        if q.get('year') == '112-2':
            topic = q.get('topic')
            if topic and topic != '未分類':
                topics_modified.add(topic)
                
    print(f"Found {len(topics_modified)} modified topics to update.")
    
    # Check if they really need updating?
    # Well, we'll just re-run update for all of them.
    for topic in topics_modified:
        print(f"Updating summary for: {topic}...")
        all_qs_in_topic = [q for q in data if q.get('topic') == topic]
        old_summary = topic_summaries.get(topic, "")
        
        new_summary = update_topic_summary(topic, old_summary, all_qs_in_topic)
        topic_summaries[topic] = new_summary
        
        with open(topics_path, "w", encoding="utf-8") as f:
            json.dump(topic_summaries, f, ensure_ascii=False, indent=2)
            
    print("Done updating summaries.")

if __name__ == "__main__":
    force_update_summaries("生物化學與臨床生化學")

