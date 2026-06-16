import re

with open('public/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# We only want to replace UI logic, not the definitions or `loadSubjectState`
# So we skip the first 300 lines (or we just use careful regex)

def replacer(match):
    return match.group(0)

# Replace getting answer: globalAnsweredState[q.exam_id + '_' + q.no] => getAnswerState(q)
content = re.sub(r'globalAnsweredState\[q\.exam_id \+ \'_(?:_\)?|\' \+) \+ q\.no\]', r'getAnswerState(q)', content)
content = re.sub(r'globalAnsweredState\[id\]', r'getAnswerState(q)', content) # Need to be careful here if `q` is not in scope. Usually it is `q`.
content = re.sub(r'globalAnsweredState\[qid\]', r'getAnswerState(q)', content)

# Wait, the regex approach is too risky because `q` might be named something else (e.g., `mq`, `currentActiveTopicData[idx]`).

