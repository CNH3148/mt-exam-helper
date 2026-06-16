import os
import json
import time
from google import genai
from google.genai import types
from pydantic import BaseModel
from typing import List, Optional

API_KEY = "<YOUR_GEMINI_API_KEY>"
client = genai.Client(api_key=API_KEY)

SUBJECTS = [
    '臨床生理學與病理學',
    '臨床血液學與血庫學',
    '醫學分子檢驗學與臨床鏡檢學',
    '微生物學與臨床微生物學',
    '生物化學與臨床生化學',
    '臨床血清免疫學與臨床病毒學'
]

class EnhancedQuestionClassification(BaseModel):
    selected_topic: str
    reasoning: str

def classify_question_enhanced(q, existing_taxonomy, topic_context_map):
    # topic_context_map: { 'topic_name': ['key1', 'key2', ...] }
    
    # Build a rich context string
    taxonomy_blocks = []
    for t in existing_taxonomy:
        t_name = t['topic']
        t_def = t['definition']
        sample_keys = topic_context_map.get(t_name, [])
        # Provide up to 10 key concepts as examples for this topic
        keys_str = "\n    - ".join(sample_keys[:10])
        
        block = f"### 類別：{t_name}\n- **定義**：{t_def}\n- **收錄題目的破題關鍵範例**：\n    - {keys_str if keys_str else '尚無範例'}"
        taxonomy_blocks.append(block)
        
    rich_taxonomy_str = "\n\n".join(taxonomy_blocks)
    
    # We ask the model to ONLY pick an existing topic
    prompt = f"""
    You are an expert medical technologist instructor.
    We have a multiple-choice question from a medical technologist licensing exam.
    
    Question: {q.get('question')}
    Choices: {json.dumps(q.get('choices'), ensure_ascii=False)}
    Answer: {q.get('answer')}
    Question's Key Concept: {q.get('key_concept', '未提取')}
    
    Task:
    Review the highly detailed existing taxonomy below, which includes the definitions and examples of "Key Concepts" (破題關鍵) of questions already classified in each topic.
    Assign this question to the single most suitable EXISTING topic.
    DO NOT CREATE NEW TOPICS. You MUST pick exactly one topic name from the existing list.
    
    Existing Taxonomy:
    {rich_taxonomy_str}
    """
    
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-pro", # Using PRO for high accuracy reasoning based on rich context
                contents=[prompt],
                config={
                    "response_mime_type": "application/json",
                    "response_schema": EnhancedQuestionClassification,
                    "temperature": 0.1
                }
            )
            res = json.loads(response.text)
            
            # Validation: ensure it's an existing topic
            valid_topics = [t['topic'] for t in existing_taxonomy]
            if res['selected_topic'] not in valid_topics:
                print(f"Warning: Model picked non-existent topic '{res['selected_topic']}'. Retrying...")
                continue
                
            return res['selected_topic']
        except Exception as e:
            print(f"Error classifying question {q.get('tags', [''])[0]}: {e}")
            time.sleep(2)
    
    # Fallback to the first topic if it utterly fails
    return existing_taxonomy[0]['topic'] if existing_taxonomy else "未分類"

def update_topic_summary(topic_name, old_summary, all_questions):
    qs_str = json.dumps([{
        "year": q.get("year"),
        "no": q.get("no"),
        "question": q.get("question"),
        "choices": q.get("choices"),
        "answer": q.get("answer"),
        "key_concept": q.get("key_concept")
    } for q in all_questions], ensure_ascii=False, indent=2)
    
    prompt = f"""
    You are an expert medical technologist instructor preparing a study guide for the topic "{topic_name}".
    
    We have recently added new questions to this topic.
    Here is the OLD topic summary (markdown):
    ---
    {old_summary}
    ---
    
    Here is the FULL list of ALL questions currently classified under this topic, including their core key concepts:
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
    print(f"\n========== Enhanced Classification Processing {subject} ==========")
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
            
    if not taxonomy:
        print("No taxonomy found. This script requires an existing taxonomy to work.")
        return
            
    topic_summaries = {}
    if os.path.exists(topics_path):
        with open(topics_path, "r", encoding="utf-8") as f:
            topic_summaries = json.load(f)
            
    # Build topic context map from ALREADY classified questions
    topic_context_map = {}
    for t in taxonomy:
        topic_context_map[t['topic']] = []
        
    for q in data:
        t = q.get('topic')
        kc = q.get('key_concept')
        if t and t != '未分類' and t in topic_context_map and kc and kc != '無法提取':
            topic_context_map[t].append(kc)
            
    # Phase 1: Identify unclassified and classify
    unclassified = [q for q in data if not q.get('topic') or q.get('topic') == '未分類']
    if not unclassified:
        print("No unclassified questions found.")
        return
        
    print(f"Found {len(unclassified)} unclassified questions. Classifying with enhanced context...")
    
    modified_topics = set()
    
    for i, q in enumerate(unclassified):
        print(f"  Classifying {i+1}/{len(unclassified)}: {q.get('tags', [''])[0]}...")
        # Ensure it has a key concept first (it should if upgrade_db_keys.py was run)
        if not q.get('key_concept') or q.get('key_concept') == '無法提取':
            print("    Warning: This question has no key_concept. It might classify poorly.")
            
        selected_topic = classify_question_enhanced(q, taxonomy, topic_context_map)
        
        try:
            print(f"    -> Assigned to: {selected_topic}")
        except UnicodeEncodeError:
            print(f"    -> Assigned to: {selected_topic.encode('cp950', errors='replace').decode('cp950')}")
        q['topic'] = selected_topic
        modified_topics.add(selected_topic)
            
    # Save db with updated topics
    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
            
    # Phase 2: Incremental update of summaries
    print(f"\nPhase 2: Updating {len(modified_topics)} modified topic summaries...")
    for topic in modified_topics:
        print(f"  Updating summary for: {topic}...")
        all_qs_in_topic = [q for q in data if q.get('topic') == topic]
        old_summary = topic_summaries.get(topic, "")
        
        new_summary = update_topic_summary(topic, old_summary, all_qs_in_topic)
        topic_summaries[topic] = new_summary
        
        # Save after each topic update
        with open(topics_path, "w", encoding="utf-8") as f:
            json.dump(topic_summaries, f, ensure_ascii=False, indent=2)
            
    print(f"Finished {subject}.")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        process_subject(sys.argv[1])
    else:
        for sub in SUBJECTS:
            process_subject(sub)

