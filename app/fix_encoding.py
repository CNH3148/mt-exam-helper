import re

with open("public/app.js", "r", encoding="utf-8") as f:
    content = f.read()

fixes = {
    "${globalBookmarks.includes(q.exam_id + '_' + q.no) ? '?? : '??}": "${globalBookmarks.includes(q.exam_id + '_' + q.no) ? '★' : '☆'}",
    "?儭?": "🏷️ ",
    "??/span>": "✕</span>",
    "甇?Ⅱ閫??嚗?": "正確解答：",
    "?? 靽格??": "🔄 修改附圖",
    "?脣?蝑?": "儲存筆記"
}

for bad, good in fixes.items():
    content = content.replace(bad, good)

# Fix any stray encoding issues in the card view as well
fixes2 = {
    "${globalBookmarks.includes(q.exam_id + '_' + q.no) ? '??' : '??'}": "${globalBookmarks.includes(q.exam_id + '_' + q.no) ? '★' : '☆'}",
    "??/span>": "✕</span>",
    "?儭? ${t}": "🏷️ ${t}"
}
for bad, good in fixes2.items():
    content = content.replace(bad, good)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Encoding fixes applied.")

