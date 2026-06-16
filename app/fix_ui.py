import re

css_path = r"C:\Users\star0\Desktop\刷題系統\app\public\style.css"
js_path = r"C:\Users\star0\Desktop\刷題系統\app\public\app.js"

# 1. Update CSS
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Replace .anki-card-wrapper to have grid
css = re.sub(r'\.anki-card-wrapper\s*\{[^}]+\}', '''.anki-card-wrapper {
    margin-top: 24px;
    padding: 20px;
    background: var(--bg-panel);
    border-radius: 12px;
    border: 1px solid var(--glass-border);
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
}
@media (max-width: 1024px) {
    .anki-card-wrapper { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
    .anki-card-wrapper { grid-template-columns: 1fr; }
}''', css)

# Fix max-width of cards
css = css.replace('max-width: 600px;', 'width: 100%; box-sizing: border-box;')

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

# 2. Update JS
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# Replace the specific DOM injection logic for Anki Wall in app.js
# Currently it is: btn.parentNode.insertBefore(wallContainer, btn.nextSibling);
target = "btn.parentNode.insertBefore(wallContainer, btn.nextSibling);"
replacement = """
                // Move the <pre> block, the copy button, and the wallContainer 
                // to the parent container, specifically AFTER the "我的單元筆記" div.
                const notesDiv = document.getElementById('detail-topic-desc').nextElementSibling;
                if (notesDiv && notesDiv.parentNode) {
                    // Create a wrapper for all anki elements to keep them grouped
                    const ankiSection = document.createElement('div');
                    ankiSection.style.marginTop = '20px';
                    ankiSection.appendChild(btn);
                    ankiSection.appendChild(pre);
                    ankiSection.appendChild(wallContainer);
                    
                    // Insert after the notes div
                    notesDiv.parentNode.insertBefore(ankiSection, notesDiv.nextSibling);
                } else {
                    btn.parentNode.insertBefore(wallContainer, btn.nextSibling);
                }
"""

js = js.replace(target, replacement)

# We also need to remove the btn insertion from detail-topic-desc to avoid duplicates if it was already moved
js = js.replace("pre.parentNode.insertBefore(btn, pre.nextSibling);", "")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

print("UI successfully patched.")

