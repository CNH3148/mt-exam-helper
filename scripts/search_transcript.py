import json
import os

transcript_path = r'C:\Users\star0\.gemini\antigravity\brain\67ba8e5b-436e-4a35-a02e-6ba03074e5f2\.system_generated\logs\transcript_full.jsonl'
out_path = 'data_recovery.log'

found_questions = []

with open(transcript_path, 'r', encoding='utf-8') as f:
    for line in f:
        if '微生物學' not in line and '分子檢驗' not in line:
            continue
            
        data = json.loads(line)
        
        # Check tool calls
        for tc in data.get('tool_calls', []):
            if tc.get('name') == 'run_command':
                args = tc.get('args', {})
                for k, v in args.items():
                    if isinstance(v, str) and '"question":' in v:
                        found_questions.append((data.get('step_index'), len(v), v[:100].replace('\n', ' ')))
            elif tc.get('name') == 'write_to_file':
                args = tc.get('args', {})
                if 'CodeContent' in args and '"question":' in args['CodeContent']:
                    found_questions.append((data.get('step_index'), len(args['CodeContent']), args['CodeContent'][:100].replace('\n', ' ')))

with open(out_path, 'w', encoding='utf-8') as out:
    for step, size, preview in found_questions:
        out.write(f'Step {step}, Size: {size}, Preview: {preview}\n')
print(f'Done. Found {len(found_questions)} references.')

