import re

with open('app/server.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Add get_question_id function
func = """
def get_question_id(q):
    return f"{q.get('year', 'unknown')}_{q.get('exam_id')}_{q.get('no')}"
"""
code = re.sub(r'(app = FastAPI\(\))', r'\1\n' + func, code)

# Fix TagUpdate
code = re.sub(r'    question_no: int\n    exam_id: int', r'    id: str', code)
code = re.sub(r'        if q\["no"\] == update\.question_no and q\["exam_id"\] == update\.exam_id:', r'        if get_question_id(q) == update.id:', code)

# Fix TagBatchUpdate
# The questions field is list[dict], I'll leave it as list[dict], but the dict will have 'id' instead of 'exam_id' and 'no'
code = re.sub(r'    target_qs = \{\(q\["exam_id"\], q\["no"\]\) for q in update\.questions\}', r'    target_qs = {q["id"] for q in update.questions}', code)
code = re.sub(r'        if \(q\["exam_id"\], q\["no"\]\) in target_qs:', r'        if get_question_id(q) in target_qs:', code)

# Fix upload_image
code = re.sub(r'    exam_id: int = Form\(\.\.\),\n    no: int = Form\(\.\.\)', r'    id: str = Form(...)', code)
code = re.sub(r'            if q\["exam_id"\] == exam_id and q\["no"\] == no:', r'            if get_question_id(q) == id:', code)

# Fix ResetImageRequest
code = re.sub(r'    exam_id: int\n    no: int', r'    id: str', code)
code = re.sub(r'        if q\["exam_id"\] == req\.exam_id and q\["no"\] == req\.no:', r'        if get_question_id(q) == req.id:', code)

with open('app/server.py', 'w', encoding='utf-8') as f:
    f.write(code)

with open('app/public/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()

# Fix app.js calls to add_tag_batch
app_js = re.sub(r'questions: \[\{exam_id: targetQ\.exam_id, no: targetQ\.no\}\]', r'questions: [{id: getQuestionId(targetQ)}]', app_js)
app_js = re.sub(r'matchedQs\.push\(\{exam_id: q\.exam_id, no: q\.no\}\);', r'matchedQs.push({id: getQuestionId(q)});', app_js)
app_js = re.sub(r'if \(matchedQs\.some\(mq => mq\.exam_id === q\.exam_id && mq\.no === q\.no\)\) \{', r'if (matchedQs.some(mq => mq.id === getQuestionId(q))) {', app_js)

# Fix upload image calls
# formData.append('exam_id', ...) -> formData.append('id', ...)
app_js = re.sub(r'formData\.append\(\'exam_id\', exam_id\);\n\s*formData\.append\(\'no\', no\);', r'formData.append(\'id\', id);', app_js)
app_js = re.sub(r'body: JSON\.stringify\(\{\n\s*subject: subStore\.subject \|\| currentActiveSubject,\n\s*exam_id: parseInt\(exam_id\),\n\s*no: parseInt\(no\)\n\s*\}\)', r'body: JSON.stringify({ subject: subStore.subject || currentActiveSubject, id: id })', app_js)

with open('app/public/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js)

print("Refactored API server and app.js")

