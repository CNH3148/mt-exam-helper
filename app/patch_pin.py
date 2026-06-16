import re

js_path = r"C:\Users\star0\Desktop\刷題系統\app\public\app.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# 1. Add globalPinnedTopics
if "let globalPinnedTopics = [];" not in js:
    js = js.replace("let globalTopicNotes = {}; // { \"id1\": \"user explanation\" }",
"""let globalTopicNotes = {}; // { "id1": "user explanation" }
let globalPinnedTopics = []; // [ "topic1", "topic2" ]""")

# 2. Add togglePinTopic
if "window.togglePinTopic" not in js:
    js = js.replace("window.setCoverageSort = function",
"""window.togglePinTopic = function(topic, event) {
    if (event) event.stopPropagation();
    if (globalPinnedTopics.includes(topic)) {
        globalPinnedTopics = globalPinnedTopics.filter(t => t !== topic);
    } else {
        globalPinnedTopics.push(topic);
    }
    saveProgress();
    renderTopicList();
};

window.setCoverageSort = function""")

# 3. Update selectSlot
if "globalPinnedTopics = data.pinnedTopics || [];" not in js:
    js = js.replace("globalTopicNotes = data.topicNotes || {};",
"""globalTopicNotes = data.topicNotes || {};
    globalPinnedTopics = data.pinnedTopics || [];""")

# 4. Update resetSlot
if "globalPinnedTopics = [];" not in js:
    js = js.replace("globalTopicNotes = {};", "globalTopicNotes = {}; globalPinnedTopics = [];")

# 5. Update saveProgress
if "pinnedTopics: globalPinnedTopics" not in js:
    js = js.replace("topicNotes: globalTopicNotes\n        };",
"""topicNotes: globalTopicNotes,
            pinnedTopics: globalPinnedTopics
        };""")
    # Also handle the case where it might be slightly different
    js = js.replace("topicNotes: globalTopicNotes\r\n        };",
"""topicNotes: globalTopicNotes,
            pinnedTopics: globalPinnedTopics
        };""")

# 6. Update rendering logic
if "const isPinnedA = globalPinnedTopics.includes(a);" not in js:
    old_sort_logic = """    const topics = Object.keys(topicGroups).sort((a, b) => {
        const isUncategorizedA = a.includes('未分類') || a.includes('等待 AI 進行');
        const isUncategorizedB = b.includes('未分類') || b.includes('等待 AI 進行');"""
    
    new_sort_logic = """    const topics = Object.keys(topicGroups).sort((a, b) => {
        const isPinnedA = globalPinnedTopics.includes(a);
        const isPinnedB = globalPinnedTopics.includes(b);

        if (isPinnedA && !isPinnedB) return -1;
        if (!isPinnedA && isPinnedB) return 1;

        const isUncategorizedA = a.includes('未分類') || a.includes('等待 AI 進行');
        const isUncategorizedB = b.includes('未分類') || b.includes('等待 AI 進行');"""
    js = js.replace(old_sort_logic, new_sort_logic)

# 7. Update card HTML
if "togglePinTopic" not in js.split("card.innerHTML = `")[1][:300]:
    old_card_html = """        const card = document.createElement('div');
        card.className = 'topic-card';
        card.innerHTML = `
            <h3>${t}</h3>"""
            
    new_card_html = """        const isPinned = globalPinnedTopics.includes(t);
        const pinIconColor = isPinned ? 'var(--accent)' : 'var(--text-muted)';
        const pinIconFill = isPinned ? 'currentColor' : 'none';

        const card = document.createElement('div');
        card.className = 'topic-card';
        card.style.position = 'relative';
        card.innerHTML = `
            <div style="position: absolute; top: 12px; right: 12px; cursor: pointer; color: ${pinIconColor}; transition: color 0.2s, transform 0.2s;" onclick="togglePinTopic('${t}', event)" title="釘選/取消釘選" onmouseover="this.style.transform='scale(1.2)'" onmouseout="this.style.transform='scale(1)'">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="${pinIconFill}" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <line x1="12" y1="17" x2="12" y2="22"></line>
                    <path d="M5 17h14v-1.76a2 2 0 0 0-1.11-1.79l-1.78-.9A2 2 0 0 1 15 11.2V6a3 3 0 0 0-6 0v5.2a2 2 0 0 1-1.11 1.35l-1.78.9A2 2 0 0 0 5 15.24Z"></path>
                </svg>
            </div>
            <h3 style="margin-right: 24px;">${t}</h3>"""
    
    js = js.replace(old_card_html, new_card_html)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)
print("Patched pins successfully.")

