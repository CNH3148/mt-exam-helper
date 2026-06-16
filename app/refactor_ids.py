import re

with open('app/public/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix toggleBookmark
code = re.sub(r'toggleBookmark\(event, \'\$\{q\.exam_id\}\', \'\$\{q\.no\}\'\)', r'toggleBookmark(event, \'${getQuestionId(q)}\')', code)
code = re.sub(r'toggleBookmark\(e, q\.exam_id, q\.no\)', r'toggleBookmark(e, getQuestionId(q))', code)
code = re.sub(r'window\.toggleBookmark = function\(e, exam_id, no\) \{', r'window.toggleBookmark = function(e, id) {', code)
# Clean up the TODO from previous run
code = re.sub(r'// WARNING: Replaced manual id with exam_id \+ no, but missing year!\n\s*const id = exam_id \+ \'_\' \+ no; // TODO: FIX ME', r'', code)

# Fix removeCustomTagFromQ
code = re.sub(r'removeCustomTagFromQ\(\'\$\{t\}\', \'\$\{q\.exam_id\}\', \'\$\{q\.no\}\'\)', r'removeCustomTagFromQ(\'${t}\', \'${getQuestionId(q)}\')', code)
code = re.sub(r'window\.removeCustomTagFromQ = function\(tag, exam_id, no\) \{', r'window.removeCustomTagFromQ = function(tag, id) {', code)
code = re.sub(r'x => x\.exam_id == exam_id && x\.no == no', r'x => getQuestionId(x) === id', code)

# Fix saveUserExplanation
code = re.sub(r'saveUserExplanation\(\'\$\{q\.exam_id\}\', \'\$\{q\.no\}\',', r'saveUserExplanation(\'${getQuestionId(q)}\',', code)
code = re.sub(r'window\.saveUserExplanation = function\(exam_id, no, val\) \{', r'window.saveUserExplanation = function(id, val) {', code)

# Fix user-exp-card HTML ids (replace ${q.exam_id}-${q.no} with ${getQuestionId(q)})
code = re.sub(r'\$\{q\.exam_id\}-\$\{q\.no\}', r'${getQuestionId(q)}', code)

# Fix AI explanation generation calls
code = re.sub(r'generateAIExplanation\(q\.exam_id, q\.no\)', r'generateAIExplanation(getQuestionId(q))', code)
code = re.sub(r'function generateAIExplanation\(exam_id, no\)', r'function generateAIExplanation(id)', code)
code = re.sub(r'x\.exam_id == exam_id && x\.no == no', r'getQuestionId(x) === id', code)

# Replace remaining getQuestionId issues
code = re.sub(r'saveUserExplanation\(exam_id, no, textarea.value\)', r'saveUserExplanation(getQuestionId(q), textarea.value)', code)

with open('app/public/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Refactored HTML and function signatures")

