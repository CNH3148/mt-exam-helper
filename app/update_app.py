import re
import os

with open("public/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add global save slot variables
vars_insert = """
let currentSaveSlot = null;
let globalAnsweredState = {};

function loadSlotUI() {
    for (let i = 1; i <= 3; i++) {
        const dataStr = localStorage.getItem('save_slot_' + i);
        const desc = document.getElementById('slot-' + i + '-desc');
        if (dataStr) {
            try {
                const data = JSON.parse(dataStr);
                const count = Object.keys(data).length;
                desc.textContent = `已作答 ${count} 題`;
            } catch(e) { desc.textContent = "資料損毀"; }
        } else {
            desc.textContent = "尚未建立紀錄";
        }
    }
}

window.selectSlot = function(slot) {
    currentSaveSlot = slot;
    const dataStr = localStorage.getItem('save_slot_' + slot);
    globalAnsweredState = dataStr ? JSON.parse(dataStr) : {};
    document.getElementById('slot-selection-modal').style.display = 'none';
    if (filterSubject.value) applyFilters(); // refresh dashboard if already loaded
};

window.resetSlot = function(slot) {
    if (confirm(`確定要清空存檔 ${slot} 嗎？此動作無法復原！`)) {
        localStorage.removeItem('save_slot_' + slot);
        if (currentSaveSlot === slot) {
            globalAnsweredState = {};
            if (filterSubject.value) applyFilters();
        }
        loadSlotUI();
    }
};

function saveProgress() {
    if (currentSaveSlot) {
        localStorage.setItem('save_slot_' + currentSaveSlot, JSON.stringify(globalAnsweredState));
    }
}
"""

content = content.replace("let answeredState = {};", vars_insert + "\nlet answeredState = {};")

# 2. Modify init() to show modal
content = content.replace("async function init() {", "async function init() {\n    document.getElementById('slot-selection-modal').style.display = 'flex';\n    loadSlotUI();")

# 3. Modify renderTopicList() to include completion meter, heatmap, and expand/collapse
old_render_topic = """function renderTopicList() {
    topicCardsContainer.innerHTML = '';
    statTotalQ.textContent = `${filteredData.length} 題`;"""

new_render_topic = """let isAnalyticsExpanded = false;
window.toggleAnalytics = function() {
    isAnalyticsExpanded = !isAnalyticsExpanded;
    renderTopicList();
};

function renderTopicList() {
    topicCardsContainer.innerHTML = '';
    statTotalQ.textContent = `${filteredData.length} 題`;
    
    // Completion Meter logic
    let correctCount = 0;
    filteredData.forEach(q => {
        const id = q.exam_id + '_' + q.no;
        if (globalAnsweredState[id] === q.answer) {
            correctCount++;
        }
    });
    const completionMeterContainer = document.getElementById('completion-meter-container');
    const dashboardProgressFill = document.getElementById('dashboard-progress-fill');
    const dashboardProgressText = document.getElementById('dashboard-progress-text');
    
    if (filteredData.length > 0) {
        completionMeterContainer.style.display = 'flex';
        const pct = Math.round((correctCount / filteredData.length) * 100);
        dashboardProgressFill.style.width = pct + '%';
        dashboardProgressText.textContent = `${pct}% (${correctCount}/${filteredData.length})`;
    } else {
        completionMeterContainer.style.display = 'none';
    }"""

content = content.replace(old_render_topic, new_render_topic)

# Heatmap replacement inside renderTopicList
# We need to replace the old table creation
old_analytics_html = """let analyticsHTML = `<table style="width:100%; border-collapse: collapse; margin-top:12px;">
        <tr style="border-bottom: 1px solid var(--glass-border);">
            <th style="text-align:left; padding:8px;">類別 (依頻率)</th>
            <th style="text-align:center; padding:8px;">題數</th>
            <th style="text-align:center; padding:8px;">佔比</th>
            <th style="text-align:center; padding:8px;">累積掌握</th>
            <th style="text-align:left; padding:8px;">出題落點區間分佈 (1~80題)</th>
        </tr>`;"""

new_analytics_html = """let analyticsHTML = `<table style="width:100%; border-collapse: collapse; margin-top:12px;">
        <tr style="border-bottom: 1px solid var(--glass-border);">
            <th style="text-align:left; padding:8px;">類別 (依頻率)</th>
            <th style="text-align:center; padding:8px;">題數</th>
            <th style="text-align:center; padding:8px;">佔比</th>
            <th style="text-align:center; padding:8px;">累積掌握</th>
            <th style="text-align:left; padding:8px;">出題落點分佈熱圖 (1~80題)</th>
        </tr>`;"""

content = content.replace(old_analytics_html, new_analytics_html)

# Now the loop logic
content = re.sub(r'let ranges = .*?analyticsHTML \+= `.*?</tr>`;', r'''
        // Heatmap generation
        let qNos = topicGroups[t].map(q => parseInt(q.no));
        let heatmapBlocks = '';
        for(let i=1; i<=80; i++) {
            const isActive = qNos.includes(i);
            const bg = isActive ? 'var(--accent)' : 'var(--bg-lighter)';
            heatmapBlocks += `<div style="width:3px; height:12px; background:${bg}; flex-shrink:0;" title="題號: ${i}"></div>`;
        }
        
        let cumColor = "var(--text-main)";
        if (cumPct >= 60 && cumPct < 80) cumColor = "#4ade80";
        if (cumPct >= 80) cumColor = "#facc15";
        
        const rowHTML = `
        <tr style="border-bottom: 1px solid var(--glass-border); font-size:13px;">
            <td style="padding:8px; color:var(--primary); cursor:pointer; text-decoration:underline;" onclick="openTopicDetail('${t}')">${t}</td>
            <td style="text-align:center; padding:8px;">${count}</td>
            <td style="text-align:center; padding:8px;">${pct}%</td>
            <td style="text-align:center; padding:8px; color:${cumColor}; font-weight:bold;">${cumPct}%</td>
            <td style="padding:8px;">
                <div style="display:flex; gap:1px; width:100%; max-width:320px; border-radius:2px; overflow:hidden;">
                    ${heatmapBlocks}
                </div>
            </td>
        </tr>`;
        
        analyticsRows.push(rowHTML);
''', content, flags=re.DOTALL)

# Insert analyticsRows array and mapping
content = content.replace("let cumulative = 0;", "let cumulative = 0;\n    let analyticsRows = [];")

# After the loop, render the table with expand/collapse
content = re.sub(r'analyticsHTML \+= `</table>`;.*?if\(analyticsContainer\) analyticsContainer\.style\.display = topics\.length > 0 \? \'block\' : \'none\';', r'''
    const limit = isAnalyticsExpanded ? analyticsRows.length : Math.min(5, analyticsRows.length);
    analyticsHTML += analyticsRows.slice(0, limit).join('');
    analyticsHTML += `</table>`;
    
    if (analyticsRows.length > 5) {
        const btnText = isAnalyticsExpanded ? "⬆️ 收合表格" : "⬇️ 展開全部";
        analyticsHTML += `<div style="text-align:center; margin-top:12px;"><button class="btn btn-secondary btn-small" onclick="toggleAnalytics()">${btnText}</button></div>`;
    }
    
    const analyticsChart = document.getElementById('coverage-chart');
    if(analyticsChart) analyticsChart.innerHTML = analyticsHTML;
    const analyticsContainer = document.getElementById('subject-analytics');
    if(analyticsContainer) analyticsContainer.style.display = topics.length > 0 ? 'block' : 'none';
''', content, flags=re.DOTALL)

# 4. Modify startPractice() to load answeredState from globalAnsweredState
content = re.sub(r'answeredState = {};\n    currentIndex = 0;', r'''answeredState = {};
    currentActiveTopicData.forEach((q, i) => {
        const id = q.exam_id + '_' + q.no;
        if (globalAnsweredState[id]) {
            answeredState[i] = globalAnsweredState[id];
        }
    });
    currentIndex = 0;''', content)

# 5. Modify onclick inside renderCardView and listOption to save progress
content = content.replace("answeredState[currentIndex] = letter;\n                renderCardView();", "answeredState[currentIndex] = letter;\n                globalAnsweredState[q.exam_id + '_' + q.no] = letter;\n                saveProgress();\n                renderCardView();")
content = content.replace("answeredState[idx] = selectedLetter;\n    updateAccuracy();", "answeredState[idx] = selectedLetter;\n    globalAnsweredState[currentActiveTopicData[idx].exam_id + '_' + currentActiveTopicData[idx].no] = selectedLetter;\n    saveProgress();\n    updateAccuracy();")

# 6. Modify List View Question Number Display
# In renderListView():
content = re.sub(r'<span class="badge" style="margin:0;">第 \$\{q\.no\} 題</span>', r'<span class="badge" style="margin:0;">Q ${idx + 1}/${currentActiveTopicData.length}</span> <span style="font-size:11px; color:var(--text-secondary); margin-left:8px;">(原始題號: ${q.no})</span>', content)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated app.js successfully.")

