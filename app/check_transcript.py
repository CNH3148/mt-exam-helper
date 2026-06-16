import json
log_path = r'C:\Users\star0\.gemini\antigravity\brain\67ba8e5b-436e-4a35-a02e-6ba03074e5f2\.system_generated\logs\transcript.jsonl'
with open(log_path, 'r', encoding='utf-8') as f:
    for line in f:
        data = json.loads(line)
        if data.get('type') == 'USER_INPUT' and data.get('content'):
            text = data['content']
            if '提醒' in text or '科目' in text or '分析' in text or 'Gemini' in text or '提示' in text:
                print(f'--- Step {data.get("step_index")} ---')
                print(text[:800])

