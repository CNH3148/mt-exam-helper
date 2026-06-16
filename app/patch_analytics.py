import os

js_path = r"C:\Users\star0\Desktop\刷題系統\app\public\app.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# 1. Add global variable and toggle function
if "let coverageSortMode" not in js:
    js = js.replace("function renderTopicList() {", 
"""let coverageSortMode = 'frequency'; // 'frequency' or 'position'
window.setCoverageSort = function(mode) {
    if (coverageSortMode === mode) return;
    coverageSortMode = mode;
    renderTopicList();
};

function renderTopicList() {""")

# 2. Update the sorting logic
old_sort = """    const topics = Object.keys(topicGroups).sort((a, b) => {
        if (a.includes('未分類')) return 1;
        if (b.includes('未分類')) return -1;
        return topicGroups[b].length - topicGroups[a].length;
    });"""

new_sort = """    const topics = Object.keys(topicGroups).sort((a, b) => {
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
    });"""

if old_sort in js:
    js = js.replace(old_sort, new_sort)

# 3. Update the table headers
old_table = """    let analyticsHTML = `<table style="width:100%; border-collapse: collapse; margin-top:12px;">
        <tr style="border-bottom: 1px solid var(--glass-border);">
            <th style="text-align:left; padding:8px;">類別 (依頻率)</th>
            <th style="text-align:center; padding:8px;">題數</th>
            <th style="text-align:center; padding:8px;">佔比</th>
            <th style="text-align:center; padding:8px;">累積掌握</th>
            <th style="text-align:left; padding:8px;">出題落點分佈熱圖 (1~80題)</th>
        </tr>`;"""

new_table = """    let analyticsHTML = `<table style="width:100%; border-collapse: collapse; margin-top:12px;">
        <tr style="border-bottom: 1px solid var(--glass-border);">
            <th style="text-align:left; padding:8px;">類別 (${coverageSortMode === 'frequency' ? '依頻率' : '依平均落點'})</th>
            <th style="text-align:center; padding:8px;">題數</th>
            <th style="text-align:center; padding:8px; cursor:pointer; user-select:none; color:${coverageSortMode === 'frequency' ? 'var(--accent)' : 'inherit'};" onclick="setCoverageSort('frequency')" title="點擊以依頻率排序">
                佔比 ${coverageSortMode === 'frequency' ? '↓' : ''}
            </th>
            <th style="text-align:center; padding:8px;">累積掌握</th>
            <th style="text-align:left; padding:8px; cursor:pointer; user-select:none; color:${coverageSortMode === 'position' ? 'var(--accent)' : 'inherit'};" onclick="setCoverageSort('position')" title="點擊以依落點排序">
                出題落點分佈熱圖 (1~80題) ${coverageSortMode === 'position' ? '↓' : ''}
            </th>
        </tr>`;"""

if old_table in js:
    js = js.replace(old_table, new_table)
elif "let analyticsHTML = `<table" in js:
    # If the text has slight differences (e.g. from previous AI edits)
    import re
    js = re.sub(
        r"let analyticsHTML = `<table.*?</tr>`;",
        new_table,
        js,
        flags=re.DOTALL
    )

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)
print("Patched app.js successfully.")

