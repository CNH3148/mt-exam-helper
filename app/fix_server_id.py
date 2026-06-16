import re
import os

with open('app/public/index.html', 'r', encoding='utf-8') as f:
    html = f.read()
# Add year hidden input to the image upload modal
html = html.replace('<input type="hidden" id="upload-modal-exam-id">', '<input type="hidden" id="upload-modal-exam-id">\\n        <input type="hidden" id="upload-modal-year">')
with open('app/public/index.html', 'w', encoding='utf-8') as f:
    f.write(html)


with open('app/server.py', 'r', encoding='utf-8') as f:
    server = f.read()

# Update TagBatchUpdate
server = server.replace('questions: list[dict] # [{"exam_id": 1, "no": 2}]', 'questions: list[dict] # [{"exam_id": 1, "no": 2, "year": "115-1"}]')
server = server.replace('target_qs = {(q["exam_id"], q["no"]) for q in update.questions}', 'target_qs = {(q.get("year"), q["exam_id"], q["no"]) for q in update.questions}')
server = server.replace('if (q["exam_id"], q["no"]) in target_qs:', 'if (q.get("year"), q["exam_id"], q["no"]) in target_qs or (None, q["exam_id"], q["no"]) in target_qs:')

# Update upload_image
server = server.replace('exam_id: int = Form(...),', 'exam_id: int = Form(...),\\n    year: str = Form(None),')
server = server.replace('if q["exam_id"] == exam_id and q["no"] == no:', 'if q["exam_id"] == exam_id and q["no"] == no and (year is None or q.get("year") == year):')

# Update reset_image
server = server.replace('class QuestionUpdate(BaseModel):\\n    subject: str\\n    question_no: int\\n    exam_id: int', 'class QuestionUpdate(BaseModel):\\n    subject: str\\n    question_no: int\\n    exam_id: int\\n    year: str = None')
server = server.replace('if q["no"] == update.question_no and q["exam_id"] == update.exam_id:', 'if q["no"] == update.question_no and q["exam_id"] == update.exam_id and (update.year is None or q.get("year") == update.year):')
server = server.replace('if q["exam_id"] == req.exam_id and q["no"] == req.no:', 'if q["exam_id"] == req.exam_id and q["no"] == req.no and (req.year is None or q.get("year") == req.year):')

with open('app/server.py', 'w', encoding='utf-8') as f:
    f.write(server)

print("Modified index.html and server.py successfully.")

