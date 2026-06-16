import re

with open('app/public/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# Fix addManualCustomTag
code = re.sub(r'window\.addManualCustomTag = function\(exam_id, no, val\) \{', r'window.addManualCustomTag = function(id, val) {', code)
code = re.sub(r'window\.addManualCustomTag\(\'\$\{q\.exam_id\}\', \'\$\{q\.no\}\',', r'window.addManualCustomTag(\'${getQuestionId(q)}\',', code)

# Fix openImageUploadModal
code = re.sub(r'window\.openImageUploadModal = function\(exam_id, no\) \{', r'window.openImageUploadModal = function(id) {', code)
code = re.sub(r'openImageUploadModal\(\'\$\{q\.exam_id\}\', \'\$\{q\.no\}\'\)', r'openImageUploadModal(\'${getQuestionId(q)}\')', code)

# Replace the inner workings where they construct the id manually
code = re.sub(r'const id = exam_id \+ \'_\' \+ no;', r'', code) # Remove leftover manual ID creations in those functions (since 'id' is now passed directly)
# Wait, some places might still be using `exam_id` instead of `id` if I just delete it.
# Let's verify what `addManualCustomTag` and `openImageUploadModal` look like.

with open('app/refactor_ids2.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("Refactored more IDs")

