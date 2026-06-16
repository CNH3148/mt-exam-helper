import re

with open("public/app.js", "r", encoding="utf-8") as f:
    content = f.read()

if "let globalTopicNotes = {};" not in content:
    content = content.replace("let globalExplanations = {};", "let globalExplanations = {};\nlet globalTopicNotes = {};")

funcs = """
window.toggleTopicMarkdownEdit = function() {
    const preview = document.getElementById('topic-md-preview');
    const editor = document.getElementById('topic-md-editor');
    if (editor.style.display === 'none') {
        editor.style.display = 'block';
        preview.style.display = 'none';
    } else {
        editor.style.display = 'none';
        preview.style.display = 'block';
    }
};

window.saveTopicNote = function() {
    if (!currentActiveTopicData || currentActiveTopicData.length === 0) return;
    const topic = currentActiveTopicData[0].topic || '未分類';
    const val = document.getElementById('topic-note-input').value;
    globalTopicNotes[filterSubject.value + '_' + topic] = val;
    saveProgress();
    toggleTopicMarkdownEdit();
    document.getElementById('topic-md-preview').innerHTML = marked.parse(val || '*尚無筆記*');
    alert('單元筆記已儲存');
};

document.getElementById('btn-sidebar-toggle').addEventListener('click', () => {
    document.querySelector('.sidebar').classList.toggle('collapsed');
});

window.renameSlot = function(slot) {
    const newName = prompt('請輸入新的存檔名稱：', document.getElementById('slot-' + slot + '-title').innerText);
    if (newName !== null && newName.trim() !== '') {
        const names = JSON.parse(localStorage.getItem('slot_names') || '{}');
        names[slot] = newName.trim();
        localStorage.setItem('slot_names', JSON.stringify(names));
        document.getElementById('slot-' + slot + '-title').innerText = newName.trim();
    }
};

const slotNames = JSON.parse(localStorage.getItem('slot_names') || '{}');
for (let i=1; i<=3; i++) {
    if (slotNames[i]) {
        const el = document.getElementById('slot-' + i + '-title');
        if (el) el.innerText = slotNames[i];
    }
}
"""
if "window.toggleTopicMarkdownEdit" not in content:
    content += "\n" + funcs

content = content.replace("explanations: globalExplanations", "explanations: globalExplanations,\n            topicNotes: globalTopicNotes")
content = content.replace("globalExplanations = savedData.explanations || {};", "globalExplanations = savedData.explanations || {};\n        globalTopicNotes = savedData.topicNotes || {};")

old_topic_desc = "document.getElementById('detail-topic-desc').innerHTML = desc;"
new_topic_desc = """document.getElementById('detail-topic-desc').innerHTML = desc;
    const noteKey = filterSubject.value + '_' + topic;
    const savedNote = globalTopicNotes[noteKey] || '';
    document.getElementById('topic-note-input').value = savedNote;
    document.getElementById('topic-md-preview').innerHTML = marked.parse(savedNote || '*尚無筆記*');"""
content = content.replace(old_topic_desc, new_topic_desc)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Patch app.js part 2 completed")

