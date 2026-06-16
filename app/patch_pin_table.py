import re

js_path = r"C:\Users\star0\Desktop\刷題系統\app\public\app.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# 1. Update the sorting logic for baseTopics (used for table)
old_sort_logic = """    const topics = Object.keys(topicGroups).sort((a, b) => {
        const isPinnedA = globalPinnedTopics.includes(a);
        const isPinnedB = globalPinnedTopics.includes(b);

        if (isPinnedA && !isPinnedB) return -1;
        if (!isPinnedA && isPinnedB) return 1;

        const isUncategorizedA = a.includes('未分類') || a.includes('等待 AI 進行');
        const isUncategorizedB = b.includes('未分類') || b.includes('等待 AI 進行');
        if (isUncategorizedA) return 1;
        if (isUncategorizedB) return -1;

        if (coverageSortMode === 'frequency') {
            return topicGroups[b].length - topicGroups[a].length;
        } else {
            // Calculate mean question number (position)
            const meanA = topicGroups[a].reduce((sum, q) => sum + parseInt(q.no), 0) / topicGroups[a].length;
            const meanB = topicGroups[b].reduce((sum, q) => sum + parseInt(q.no), 0) / topicGroups[b].length;
            if (meanA === meanB) {
                return topicGroups[b].length - topicGroups[a].length;
            }
            return meanA - meanB;
        }
    });

    let totalQuestions = 0;
    topics.forEach(t => totalQuestions += topicGroups[t].length);"""

new_sort_logic = """    const baseTopics = Object.keys(topicGroups).sort((a, b) => {
        const isUncategorizedA = a.includes('未分類') || a.includes('等待 AI 進行');
        const isUncategorizedB = b.includes('未分類') || b.includes('等待 AI 進行');
        if (isUncategorizedA) return 1;
        if (isUncategorizedB) return -1;

        if (coverageSortMode === 'frequency') {
            return topicGroups[b].length - topicGroups[a].length;
        } else {
            const meanA = topicGroups[a].reduce((sum, q) => sum + parseInt(q.no), 0) / topicGroups[a].length;
            const meanB = topicGroups[b].reduce((sum, q) => sum + parseInt(q.no), 0) / topicGroups[b].length;
            if (meanA === meanB) {
                return topicGroups[b].length - topicGroups[a].length;
            }
            return meanA - meanB;
        }
    });

    let totalQuestions = 0;
    baseTopics.forEach(t => totalQuestions += topicGroups[t].length);"""

if old_sort_logic in js:
    js = js.replace(old_sort_logic, new_sort_logic)

# 2. Update the iteration to use baseTopics for the table, and move card generation to a second loop
old_loop_start = """    let cumulative = 0;
    let analyticsRows = [];

    topics.forEach(t => {"""

new_loop_start = """    let cumulative = 0;
    let analyticsRows = [];

    baseTopics.forEach(t => {"""

if old_loop_start in js:
    js = js.replace(old_loop_start, new_loop_start)

# 3. Extract card generation and put it in a separate loop using cardTopics
old_card_gen = """        analyticsRows.push(rowHTML);


        const isPinned = globalPinnedTopics.includes(t);
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
            <h3 style="margin-right: 24px;">${t}</h3>
            <div class="topic-meta">${count} 題</div>
        `;
        card.onclick = () => openTopicDetail(t);
        topicCardsContainer.appendChild(card);
    });"""

new_card_gen = """        analyticsRows.push(rowHTML);
    });

    const cardTopics = [...baseTopics].sort((a, b) => {
        const isPinnedA = globalPinnedTopics.includes(a);
        const isPinnedB = globalPinnedTopics.includes(b);
        if (isPinnedA && !isPinnedB) return -1;
        if (!isPinnedA && isPinnedB) return 1;
        return 0; // retain baseTopics order for the rest
    });

    cardTopics.forEach(t => {
        const count = topicGroups[t].length;
        const isPinned = globalPinnedTopics.includes(t);
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
            <h3 style="margin-right: 24px;">${t}</h3>
            <div class="topic-meta">${count} 題</div>
        `;
        card.onclick = () => openTopicDetail(t);
        topicCardsContainer.appendChild(card);
    });"""

if old_card_gen in js:
    js = js.replace(old_card_gen, new_card_gen)

# 4. Fix analyticsContainer display check from topics to baseTopics
if "topics.length > 0 ? 'block' : 'none';" in js:
    js = js.replace("topics.length > 0 ? 'block' : 'none';", "baseTopics.length > 0 ? 'block' : 'none';")

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)
print("Patched app.js table logic successfully.")

