import re
import os

with open('app/public/app.js', 'r', encoding='utf-8') as f:
    code = f.read()

# We want to replace `q.exam_id + '_' + q.no` with `q.year + '_' + q.exam_id + '_' + q.no`
code = code.replace("q.exam_id + '_' + q.no", "q.year + '_' + q.exam_id + '_' + q.no")
code = code.replace("mq.exam_id + '_' + mq.no", "mq.year + '_' + mq.exam_id + '_' + mq.no")

# Function signatures and usages that take (exam_id, no) should take (exam_id, no, year)
# 1. toggleBookmark
code = code.replace("toggleBookmark(event, '${q.exam_id}', '${q.no}')", "toggleBookmark(event, '${q.exam_id}', '${q.no}', '${q.year}')")
code = code.replace("toggleBookmark(e, q.exam_id, q.no)", "toggleBookmark(e, q.exam_id, q.no, q.year)")
code = code.replace("window.toggleBookmark = function(e, exam_id, no) {", "window.toggleBookmark = function(e, exam_id, no, year) {")
code = code.replace("const id = exam_id + '_' + no;", "const id = year + '_' + exam_id + '_' + no;")

# 2. removeCustomTagFromQ
code = code.replace("removeCustomTagFromQ('${t}', '${q.exam_id}', '${q.no}')", "removeCustomTagFromQ('${t}', '${q.exam_id}', '${q.no}', '${q.year}')")
code = code.replace("window.removeCustomTagFromQ = function(tag, exam_id, no) {", "window.removeCustomTagFromQ = function(tag, exam_id, no, year) {")
code = code.replace("x => x.exam_id == exam_id && x.no == no", "x => x.exam_id == exam_id && x.no == no && x.year == year")

# 3. addManualCustomTag
code = code.replace("window.addManualCustomTag('${q.exam_id}', '${q.no}', this.value)", "window.addManualCustomTag('${q.exam_id}', '${q.no}', '${q.year}', this.value)")
code = code.replace("window.addManualCustomTag = function(exam_id, no, val) {", "window.addManualCustomTag = function(exam_id, no, year, val) {")
# Note: addManualCustomTag uses addManualTag
code = code.replace("addManualTag(exam_id, no);", "addManualTag(exam_id, no, year);")

# 4. addManualTag
code = code.replace("window.addManualTag = function(exam_id, no) {", "window.addManualTag = function(exam_id, no, year) {")
# inside addManualTag:
# const q = currentData.find(...)
# Wait, addManualTag doesn't construct `id`, it just finds `q`
code = code.replace("x => x.exam_id == exam_id && x.no == no", "x => x.exam_id == exam_id && x.no == no && x.year == year")

# 5. openImageUploadModal
code = code.replace("openImageUploadModal('${q.exam_id}', '${q.no}')", "openImageUploadModal('${q.exam_id}', '${q.no}', '${q.year}')")
code = code.replace("window.openImageUploadModal = function(exam_id, no) {", "window.openImageUploadModal = function(exam_id, no, year) {")
code = code.replace("document.getElementById('upload-modal-exam-id').value = exam_id;", "document.getElementById('upload-modal-exam-id').value = exam_id;\\n    document.getElementById('upload-modal-year').value = year || '';")

# 6. saveUserExplanation
code = code.replace("saveUserExplanation('${q.exam_id}', '${q.no}', document.getElementById('user-exp-card-${q.exam_id}-${q.no}').value)", "saveUserExplanation('${q.exam_id}', '${q.no}', '${q.year}', document.getElementById('user-exp-card-${q.exam_id}-${q.no}').value)")
code = code.replace("saveUserExplanation('${q.exam_id}', '${q.no}', document.getElementById('user-exp-list-${q.exam_id}-${q.no}').value)", "saveUserExplanation('${q.exam_id}', '${q.no}', '${q.year}', document.getElementById('user-exp-list-${q.exam_id}-${q.no}').value)")
code = code.replace("window.saveUserExplanation = function(exam_id, no, val) {", "window.saveUserExplanation = function(exam_id, no, year, val) {")

# 7. toggleMarkdownEdit / toggleEditUserExp / saveAndRenderUserExp
# Let's see if they use exam_id, no.
# Actually toggleMarkdownEdit takes the ID prefix: `toggleMarkdownEdit('card-${q.exam_id}-${q.no}')`
# Since these are DOM element IDs, they must match!
# If there are duplicates in the DOM, that's bad.
# Let's replace `${q.exam_id}-${q.no}` with `${q.year}-${q.exam_id}-${q.no}` globally!
code = code.replace("${q.exam_id}-${q.no}", "${q.year}-${q.exam_id}-${q.no}")
# And `currentActiveTopicData[idx].exam_id + '_' + currentActiveTopicData[idx].no;`
code = code.replace("currentActiveTopicData[idx].exam_id + '_' + currentActiveTopicData[idx].no;", "currentActiveTopicData[idx].year + '_' + currentActiveTopicData[idx].exam_id + '_' + currentActiveTopicData[idx].no;")

# API `/api/add_tag_batch`
code = code.replace("{exam_id: targetQ.exam_id, no: targetQ.no}", "{exam_id: targetQ.exam_id, no: targetQ.no, year: targetQ.year}")
code = code.replace("{exam_id: q.exam_id, no: q.no}", "{exam_id: q.exam_id, no: q.no, year: q.year}")
code = code.replace("mq.exam_id === q.exam_id && mq.no === q.no", "mq.exam_id === q.exam_id && mq.no === q.no && mq.year === q.year")

# FormData for image upload
code = code.replace("formData.append('exam_id', exam_id);", "formData.append('exam_id', exam_id);\\n        formData.append('year', document.getElementById('upload-modal-year').value);")
code = code.replace("exam_id: parseInt(exam_id),", "exam_id: parseInt(exam_id),\\n                year: document.getElementById('upload-modal-year').value,")

with open('app/public/app.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Modified app.js successfully.")

