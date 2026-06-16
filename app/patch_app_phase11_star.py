import re

with open("public/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Replace star HTML in renderCardView and renderListView
old_star = "color:#facc15; margin-left:8px;\""
new_star = "color:#facc15; margin-left:8px;\" class=\"star-icon\""
content = content.replace(old_star, new_star)

# Fix openSubject to ensure practice buttons are displayed.
# Looking for currentSubjectTitle.textContent = filterSubject.value;
if "btn-wrong-practice" not in content.split("function openSubject")[1][:500]:
    content = content.replace(
        "currentSubjectTitle.textContent = filterSubject.value;",
        "currentSubjectTitle.textContent = filterSubject.value;\n    document.getElementById('btn-wrong-practice').style.display = 'block';\n    document.getElementById('btn-bookmark-practice').style.display = 'block';"
    )

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Star and openSubject patched.")

