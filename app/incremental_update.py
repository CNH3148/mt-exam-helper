import os
import json
import time
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Optional

# Same key used in other scripts
API_KEY = "<YOUR_GEMINI_API_KEY>"
client = genai.Client(api_key=API_KEY)

SUBJECTS = [
    '臨床化學',
    '臨床血液學與血庫學',
    '臨床血清免疫學與臨床病毒學',
    '臨床生理學與病理學',
    '醫學分子檢驗學與臨床鏡檢學',
    '微生物學與臨床微生物學',
    '生物化學與臨床生化學'
]

class QuestionClassification(BaseModel):
    selected_topic: str
    is_new_topic: bool
    new_topic_definition: str

def classify_question(q, existing_taxonomy_with_examples):
    taxonomy_str = ""
    for t in existing_taxonomy_with_examples:
        examples = "\n    ".join([f"- {ex}" for ex in t.get('examples', [])])
        taxonomy_str += f"- **{t['topic']}**: {t['definition']}\n    Examples of key concepts in this topic:\n    {examples}\n"
    
    prompt = f"""
    You are an expert medical technologist instructor.
    We have a new multiple-choice question from a medical technologist licensing exam.
    
    Question: {q.get('question')}
    Choices: {json.dumps(q.get('choices'), ensure_ascii=False)}
    Answer: {q.get('answer')}
    Question's Key Concept (破題關鍵): {q.get('key_concept', 'N/A')}
    
    Task:
    1. Review the "Question's Key Concept" provided above.
    2. Review the existing topics, their definitions, and their examples of key concepts below.
    3. Assign this question to the most suitable existing topic by semantically matching its key concept to the topic's examples. 
    4. ONLY create a new topic if the question's core concept completely deviates from ALL existing topics (avoid redundancy).
    
    Existing Topics:
    {taxonomy_str if taxonomy_str else "No existing topics."}
    """
    
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[prompt],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": QuestionClassification,
                    "temperature": 0.1
                }
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"Error classifying question {q.get('tags', [''])[0]}: {e}")
            time.sleep(5)
    return None

def update_topic_summary(topic_name, old_summary, all_questions):
    qs_str = json.dumps([{
        "year": q.get("year"),
        "no": q.get("no"),
        "question": q.get("question"),
        "choices": q.get("choices"),
        "answer": q.get("answer")
    } for q in all_questions], ensure_ascii=False, indent=2)
    
    prompt = f"""
    You are an expert medical technologist instructor preparing a study guide for the topic "{topic_name}".
    
    We have recently added new questions to this topic.
    Here is the OLD topic summary (markdown):
    ---
    {old_summary}
    ---
    
    Here is the FULL list of ALL questions currently classified under this topic:
    {qs_str}
    
    Task:
    Incrementally update the topic summary based on the FULL list of questions.
    - DO NOT rewrite the summary from scratch. Keep the existing structure and useful insights.
    - Focus on updating or expanding the "高頻考點" (High-frequency concepts), "趨勢預測" (Trend analysis), and "Anki 記憶卡" (Anki tables) to reflect any new concepts introduced by the newly added questions.
    - If there is a table, ensure the table is expanded or updated with new knowledge points.
    - Output ONLY the updated markdown text (no markdown code block ticks ```markdown).
    """
    
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=[prompt],
                config={
                    "temperature": 0.2
                }
            )
            # Clean potential markdown ticks
            text = response.text.strip()
            if text.startswith("```markdown"):
                text = text[11:]
            elif text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            return text.strip()
        except Exception as e:
            print(f"Error updating summary for topic {topic_name}: {e}")
            time.sleep(5)
    return old_summary

def process_subject(subject):
    print(f"\n========== Processing {subject} ==========")
    db_path = f"app/data/{subject}.json"
    tax_path = f"app/data/taxonomy_{subject}.json"
    topics_path = f"app/data/topics_{subject}.json"
    
    if not os.path.exists(db_path):
        print("Database missing, skipping.")
        return
        
    with open(db_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    taxonomy = []
    if os.path.exists(tax_path):
        with open(tax_path, "r", encoding="utf-8") as f:
            taxonomy = json.load(f)
            
    # Extract key_concept examples for each topic
    import random
    existing_taxonomy_with_examples = []
    for t in taxonomy:
        topic_name = t['topic']
        qs_in_topic = [q for q in data if q.get('topic') == topic_name and q.get('key_concept')]
        unique_concepts = list({q['key_concept'] for q in qs_in_topic})
        examples = random.sample(unique_concepts, min(5, len(unique_concepts)))
        existing_taxonomy_with_examples.append({
            'topic': topic_name,
            'definition': t.get('definition', ''),
            'examples': examples
        })
            
    topic_summaries = {}
    if os.path.exists(topics_path):
        with open(topics_path, "r", encoding="utf-8") as f:
            topic_summaries = json.load(f)
            
    # Phase 1: Identify unclassified and classify
    unclassified = [q for q in data if not q.get('topic') or q.get('topic') == '未分類']
    if not unclassified:
        print("No unclassified questions found.")
        return
        
    print(f"Found {len(unclassified)} unclassified questions. Classifying...")
    
    modified_topics = set()
    new_topics_added = False
    
    for i, q in enumerate(unclassified):
        print(f"  Classifying {i+1}/{len(unclassified)}: {q.get('tags', [''])[0]}...")
        res = classify_question(q, existing_taxonomy_with_examples)
        
        # Rate limit protection: sleep 4s after each classification attempt to stay within 15 RPM
        time.sleep(4)
        
        if res:
            selected_topic = res['selected_topic']
            # Safety check, if model outputted something entirely new but didn't set is_new_topic
            if selected_topic not in [t['topic'] for t in taxonomy]:
                res['is_new_topic'] = True
                if not res.get('new_topic_definition'):
                    res['new_topic_definition'] = "自動生成之定義。"
                    
            if res['is_new_topic']:
                print(f"    -> Created new topic: {selected_topic}")
                taxonomy.append({
                    "topic": selected_topic,
                    "definition": res['new_topic_definition']
                })
                topic_summaries[selected_topic] = f"# {selected_topic}\n\n此為新建立的類群，說明即將生成。"
                new_topics_added = True
            else:
                print(f"    -> Assigned to: {selected_topic}")
                
            q['topic'] = selected_topic
            modified_topics.add(selected_topic)
        else:
            print(f"    -> Failed to classify.")
            
    # Save db with updated topics
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    if new_topics_added:
        with open(tax_path, "w", encoding="utf-8") as f:
            json.dump(taxonomy, f, ensure_ascii=False, indent=2)
            
    # Phase 2: Incremental update of summaries (DISABLED)
    print(f"\nPhase 2: Skipping update of topic summaries as requested.")
    # for topic in modified_topics:
    #     print(f"  Updating summary for: {topic}...")
    #     all_qs_in_topic = [q for q in data if q.get('topic') == topic]
    #     old_summary = topic_summaries.get(topic, "")
    #     
    #     new_summary = update_topic_summary(topic, old_summary, all_qs_in_topic)
    #     topic_summaries[topic] = new_summary
    #     
    #     # Save after each topic update to prevent data loss
    #     with open(topics_path, "w", encoding="utf-8") as f:
    #         json.dump(topic_summaries, f, ensure_ascii=False, indent=2)
            
    print(f"Finished {subject}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        target = sys.argv[1]
        process_subject(target)
    else:
        for sub in SUBJECTS:
            process_subject(sub)

