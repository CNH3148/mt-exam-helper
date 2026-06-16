import re
import os

css_path = r"C:\Users\star0\Desktop\刷題系統\app\public\style.css"
js_path = r"C:\Users\star0\Desktop\刷題系統\app\public\app.js"

# 1. Update CSS
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Modify .anki-wall
css = re.sub(r'\.anki-wall\s*\{[^}]+\}', '''.anki-wall {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin-top: 30px;
}
@media (max-width: 1024px) {
    .anki-wall { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
    .anki-wall { grid-template-columns: 1fr; }
}''', css)

# Modify .front-container, .back-container max-width
css = css.replace('max-width: 600px;', 'width: 100%; box-sizing: border-box;')

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

# 2. Update JS to move Anki cards below the "我的單元筆記" block
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# Replace the Anki insertion logic
target = "pre.parentNode.insertBefore(btn, pre);"
replacement = """
                // Move <pre> block and everything below "我的單元筆記"
                const notesDiv = document.getElementById('detail-topic-desc').nextElementSibling;
                if (notesDiv) {
                    notesDiv.parentNode.insertBefore(btn, notesDiv.nextSibling);
                    notesDiv.parentNode.insertBefore(pre, btn.nextSibling);
                    notesDiv.parentNode.insertBefore(wallTitle, pre.nextSibling);
                    notesDiv.parentNode.insertBefore(wallDiv, wallTitle.nextSibling);
                } else {
                    pre.parentNode.insertBefore(btn, pre);
                    pre.parentNode.insertBefore(wallTitle, pre.nextSibling);
                    pre.parentNode.insertBefore(wallDiv, wallTitle.nextSibling);
                }
"""

js = js.replace("pre.parentNode.insertBefore(btn, pre);", replacement)

# Remove the old insertBefore calls
js = js.replace("pre.parentNode.insertBefore(wallTitle, pre.nextSibling);", "")
js = js.replace("pre.parentNode.insertBefore(wallDiv, wallTitle.nextSibling);", "")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

print("UI successfully updated: 4-column grid and moved Anki cards below topic notes.")

