import re

with open("public/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. toggleBookmark fix
content = content.replace("event.stopPropagation();", "if (window.event) window.event.stopPropagation();")

# 2. Add manual tag function
add_funcs = """
window.addManualCustomTag = function(exam_id, no, val) {
    val = val.trim();
    if (!val) return;
    if (!globalCustomTags[val]) globalCustomTags[val] = [];
    const id = exam_id + '_' + no;
    if (!globalCustomTags[val].includes(id)) {
        globalCustomTags[val].push(id);
        saveProgress();
        renderCustomTagsSidebar();
        if (document.getElementById('view-mode').value === 'card') renderCardView();
        else renderListView();
    }
};

window.toggleMarkdownEdit = function(id) {
    const preview = document.getElementById('md-preview-' + id);
    const editor = document.getElementById('md-editor-' + id);
    if (editor.style.display === 'none') {
        editor.style.display = 'block';
        preview.style.display = 'none';
    } else {
        editor.style.display = 'none';
        preview.style.display = 'block';
    }
};

window.resetImage = async function() {
    const exam_id = document.getElementById('upload-modal-exam-id').value;
    const no = document.getElementById('upload-modal-no').value;
    
    const res = await fetch('/api/reset_image', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ subject: filterSubject.value, exam_id: parseInt(exam_id), no: parseInt(no) })
    });
    const d = await res.json();
    if (d.status === 'success') {
        alert('附圖已還原！');
        document.getElementById('image-upload-modal').style.display = 'none';
        const q = currentData.find(x => x.exam_id == exam_id && x.no == no);
        if (q) q.images = d.images;
        if (document.getElementById('view-mode').value === 'card') renderCardView();
        else renderListView();
    } else {
        alert(d.message);
    }
};
"""
if "addManualCustomTag" not in content:
    content += "\n" + add_funcs

# 3. Card View Changes
# Hide tags initially
content = content.replace(
    "const qTags = document.getElementById('q-tags');\n        qTags.innerHTML = tagsHtml;",
    "const qTags = document.getElementById('q-tags');\n        qTags.innerHTML = tagsHtml;\n        qTags.style.display = 'none';"
)
# Add manual tag input to tagsHtml
content = content.replace(
    "                        return html;\n                    })()}\n                </div>",
    "                        return html;\n                    })()}\n                    <span class=\"badge\" style=\"background:var(--primary); color:white; display:flex; align-items:center; gap:4px;\">➕ <input type=\"text\" class=\"manual-tag-input\" placeholder=\"新增標籤\" onkeypress=\"if(event.key==='Enter') addManualCustomTag('${q.exam_id}', '${q.no}', this.value)\"></span>\n                </div>"
)
# Show tags when answered
content = content.replace(
    "explanationPanel.style.display = 'block';",
    "explanationPanel.style.display = 'block';\n        document.getElementById('q-tags').style.display = 'flex';"
)

# Render Markdown in Card View Explanation
card_exp_old = """<textarea id="user-exp-${q.exam_id}-${q.no}" style="width:100%; height:100px; background:var(--bg-lighter); color:var(--text-main); border:1px solid var(--glass-border); padding:8px; border-radius:6px; resize:vertical;">${userExp}</textarea>
            <div style="text-align:right; margin-top:8px;">
                <button class="btn btn-primary btn-small" onclick="saveUserExplanation('${q.exam_id}', '${q.no}', document.getElementById('user-exp-${q.exam_id}-${q.no}').value)">儲存筆記</button>
            </div>"""
card_exp_new = """
            <div id="md-preview-${q.exam_id}-${q.no}" class="markdown-body" style="background:var(--bg-lighter); padding:12px; border-radius:6px; min-height:60px;">${marked.parse(userExp || '*尚無筆記*')}</div>
            <div id="md-editor-${q.exam_id}-${q.no}" style="display:none; margin-top:8px;">
                <textarea id="user-exp-${q.exam_id}-${q.no}" style="width:100%; height:120px; background:var(--bg-lighter); color:var(--text-main); border:1px solid var(--glass-border); padding:8px; border-radius:6px; resize:vertical;">${userExp}</textarea>
                <div style="text-align:right; margin-top:8px;">
                    <button class="btn btn-primary btn-small" onclick="saveUserExplanation('${q.exam_id}', '${q.no}', document.getElementById('user-exp-${q.exam_id}-${q.no}').value); toggleMarkdownEdit('${q.exam_id}-${q.no}'); document.getElementById('md-preview-${q.exam_id}-${q.no}').innerHTML = marked.parse(document.getElementById('user-exp-${q.exam_id}-${q.no}').value || '*尚無筆記*');">儲存筆記</button>
                </div>
            </div>
            <div style="text-align:right; margin-top:8px;">
                <button class="btn btn-secondary btn-small" onclick="toggleMarkdownEdit('${q.exam_id}-${q.no}')">✏️ 編輯筆記</button>
            </div>"""
content = content.replace(card_exp_old, card_exp_new)


with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Patch app.js part 1 completed")

