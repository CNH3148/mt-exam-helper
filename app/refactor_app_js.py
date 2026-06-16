import re

with open('app/public/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Add getQuestionId function near the top, after global variables
func = """
function getQuestionId(q) {
    if (!q) return '';
    return (q.year || 'unknown') + '_' + q.exam_id + '_' + q.no;
}
"""
# Find a good place to insert it
code = re.sub(r'(let globalPinnedTopics = \[\];)', r'\1\n' + func, code)

# Replace all inline ID constructions
code = re.sub(r"const id = q\.exam_id \+ '_' \+ q\.no;", r"const id = getQuestionId(q);", code)
code = re.sub(r"const id = mq\.exam_id \+ '_' \+ mq\.no;", r"const id = getQuestionId(mq);", code)

# Some functions take exam_id and no
code = re.sub(r"const id = exam_id \+ '_' \+ no;", r"// WARNING: Replaced manual id with exam_id + no, but missing year!\n    const id = exam_id + '_' + no; // TODO: FIX ME", code)

with open('app/public/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Replaced successfully")

