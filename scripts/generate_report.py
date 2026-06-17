import json

subjects = ['臨床血液學與血庫學', '醫學分子檢驗學與臨床鏡檢學']
report = []

for sub in subjects:
    try:
        with open(f'app/data/{sub}.json', encoding='utf-8') as f:
            data = json.load(f)
        with open(f'app/data/topics_{sub}.json', encoding='utf-8') as f:
            topics = json.load(f)
            
        known_topics = set(topics.keys())
        
        # Questions whose topic is NOT in known_topics
        missing_qs = [q for q in data if q.get('topic') and q.get('topic') != '未分類' and q.get('topic') not in known_topics]
        
        # Group by topic
        missing_topics_dict = {}
        for q in missing_qs:
            t = q['topic']
            missing_topics_dict[t] = missing_topics_dict.get(t, 0) + 1
            
        report.append(f"### {sub}")
        report.append(f"- 總共有 {len(missing_qs)} 題被 UI 誤判為「未分類」")
        report.append(f"- 這批題目共產生了 {len(missing_topics_dict)} 個新類群：")
        
        for t, count in sorted(missing_topics_dict.items(), key=lambda x: x[1], reverse=True):
            report.append(f"  - **{t}** (包含 {count} 題)")
            
        report.append("")
        
    except Exception as e:
        report.append(f"Error reading {sub}: {e}")

with open('missing_topics_report.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(report))

