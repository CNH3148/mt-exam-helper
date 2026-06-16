import json
log_path = r'C:\Users\star0\.gemini\antigravity\brain\67ba8e5b-436e-4a35-a02e-6ba03074e5f2\.system_generated\logs\transcript.jsonl'
out_path = r'C:\Users\star0\Desktop\刷題系統\app\transcript_hints.txt'
with open(log_path, 'r', encoding='utf-8') as f, open(out_path, 'w', encoding='utf-8') as out:
    for line in f:
        data = json.loads(line)
        if data.get('type') == 'USER_INPUT' and data.get('content'):
            text = data['content']
            if '提醒' in text or '其他科目' in text or '分析' in text or 'Gemini' in text or '提示' in text:
                out.write(f'--- Step {data.get("step_index")} ---\n')
                out.write(text[:800] + '\n\n')

