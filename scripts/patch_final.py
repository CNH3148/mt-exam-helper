import json

with open('app/public/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix 1: Inject subject into currentData in onSubjectChange
js = js.replace('currentData = await res.json();\n', 'currentData = await res.json();\n        currentData.forEach(q => q.subject = sub);\n')

# Fix 2: Fix PDF URL
old_pdf_url = 'let pdfUrl = `../pdfs/${q.year}/${encodeURIComponent(q.subject)}.pdf`;'
new_pdf_url = 'let pdfUrl = `../pdfs/${encodeURIComponent(q.subject)}/${q.year}.pdf`;'
js = js.replace(old_pdf_url, new_pdf_url)

with open('app/public/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

with open('app/public/style.css', 'r', encoding='utf-8') as f:
    css = f.read()

# Fix 3: Add !important to eye-icon hover opacity
css = css.replace('.native-tag:hover .eye-icon {\n    opacity: 1;\n}', '.native-tag:hover .eye-icon {\n    opacity: 1 !important;\n}')
css = css.replace('.native-tag:hover .eye-icon { opacity: 1; }', '.native-tag:hover .eye-icon { opacity: 1 !important; }')

# Fix 4: Fix list-option hiding
css = css.replace('.options-grid.pdf-mode .option-text, .list-card-options.pdf-mode .list-option span { display: none !important; }',
                  '.options-grid.pdf-mode .option-text, .list-card-options.pdf-mode .list-option .option-content { display: none !important; }')

with open('app/public/style.css', 'w', encoding='utf-8') as f:
    f.write(css)


