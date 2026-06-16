import re

with open("public/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update checkAnswer logic in renderCardView
# Currently it checks:
# const isSelected = answeredState[currentIndex] === letter;
# We need to change it to answeredState[currentIndex] && answeredState[currentIndex].current_answer === letter
content = content.replace(
    "const isSelected = answeredState[currentIndex] === letter;",
    "const isSelected = answeredState[currentIndex] && answeredState[currentIndex].current_answer === letter;"
)

# And fix the class adding logic:
old_class_logic = """        if (hasAnswered) {
            if (isSelected && isCorrect) div.classList.add('correct');
            if (isSelected && !isCorrect) div.classList.add('wrong');
            if (!isSelected && isCorrect) div.classList.add('correct');
        }"""
new_class_logic = """        if (hasAnswered) {
            if (isSelected && isCorrect) div.classList.add('correct');
            if (isSelected && !isCorrect) div.classList.add('wrong');
            // Remove the automatic green highlight for correct answer when user selected wrong
            if (!isSelected && isCorrect) div.classList.add('correct');
        }"""
# Wait, the user said: "我希望選錯的選項變紅，正確答案自動變綠 (就像清單模式一樣)。"
# If so, the original logic WAS correct. But the issue was `isSelected` was ALWAYS false!
# So the old class logic is actually fine once `isSelected` is fixed! 

# 2. Tag UI Refinements
# I need to change manual tag input.
old_tag_input_card = """<div style="display:inline-flex; align-items:center; gap:4px; margin-left:8px;">
                    <input type="text" id="manual-tag-${q.exam_id}-${q.no}" placeholder="自訂標籤..." style="padding:2px 6px; border-radius:4px; border:1px solid var(--glass-border); background:var(--bg-lighter); color:var(--text-main); font-size:12px; width:80px;">
                    <button class="btn btn-secondary btn-small" style="padding:2px 6px; font-size:12px;" onclick="addManualTag('${q.exam_id}', '${q.no}')">➕</button>
                </div>"""
new_tag_input_card = """<input type="text" class="manual-tag-input" placeholder="新增標籤..." onkeypress="if(event.key==='Enter') { window.addManualCustomTag('${q.exam_id}', '${q.no}', this.value); this.value=''; }">"""
content = content.replace(old_tag_input_card, new_tag_input_card)

old_tag_input_list = """<span class="badge" style="background:var(--primary); color:white; display:flex; align-items:center; gap:4px;">
                            ➕ <input type="text" class="manual-tag-input" placeholder="新增標籤" onkeypress="if(event.key==='Enter') addManualCustomTag('${q.exam_id}', '${q.no}', this.value)">
                        </span>"""
new_tag_input_list = """<input type="text" class="manual-tag-input" placeholder="新增標籤..." onkeypress="if(event.key==='Enter') { window.addManualCustomTag('${q.exam_id}', '${q.no}', this.value); this.value=''; }">"""
content = content.replace(old_tag_input_list, new_tag_input_list)

# 3. Card to List Scroll Sync
old_switch_mode = """function switchMode(mode) {
    currentMode = mode;
    btnModeCard.classList.toggle('active', mode === 'card');
    btnModeList.classList.toggle('active', mode === 'list');
    
    if (currentActiveTopicData.length === 0) return;
    
    if (mode === 'card') {
        switchView('practice');
        renderCardView();
    } else {
        switchView('list');
        renderListView();
    }
}"""
new_switch_mode = """function switchMode(mode) {
    currentMode = mode;
    btnModeCard.classList.toggle('active', mode === 'card');
    btnModeList.classList.toggle('active', mode === 'list');
    
    if (currentActiveTopicData.length === 0) return;
    
    if (mode === 'card') {
        switchView('practice');
        renderCardView();
    } else {
        switchView('list');
        renderListView();
        setTimeout(() => {
            const el = document.getElementById('list-exp-' + currentIndex);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }
}"""
content = content.replace(old_switch_mode, new_switch_mode)

# 4. Heatmap enhancements
old_heatmap = """        // Heatmap generation
        let qNos = topicGroups[t].map(q => parseInt(q.no));
        let heatmapBlocks = '';
        for(let i=1; i<=80; i++) {
            const isActive = qNos.includes(i);
            const bg = isActive ? 'var(--accent)' : 'var(--bg-lighter)';
            heatmapBlocks += `<div style="width:3px; height:12px; background:${bg}; flex-shrink:0;" title="題號: ${i}"></div>`;
        }"""
new_heatmap = """        // Heatmap generation
        let noCounts = {};
        topicGroups[t].forEach(q => {
            let n = parseInt(q.no);
            noCounts[n] = (noCounts[n] || 0) + 1;
        });
        let maxCount = Math.max(1, ...Object.values(noCounts));
        let heatmapBlocks = '';
        for(let i=1; i<=80; i++) {
            const count = noCounts[i] || 0;
            let bg = 'var(--bg-lighter)';
            if (count > 0) {
                const alpha = Math.max(0.3, count / maxCount);
                bg = `rgba(239, 68, 68, ${alpha})`;
            }
            let borderRight = (i % 5 === 0) ? 'border-right: 1px solid rgba(255,255,255,0.1);' : '';
            heatmapBlocks += `<div style="width:3px; height:12px; background:${bg}; flex-shrink:0; ${borderRight}" title="題號: ${i} (共 ${count} 題)"></div>`;
        }
        let axisHtml = '<div style="display:flex; width:100%; max-width:320px; position:relative; height:15px; margin-top:2px;">';
        for(let i=5; i<=80; i+=5) {
            axisHtml += `<div style="position:absolute; left:${(i/80)*100}%; font-size:9px; color:var(--text-muted); transform:translateX(-50%);">${i}</div>`;
        }
        axisHtml += '</div>';"""
content = content.replace(old_heatmap, new_heatmap)

old_heatmap_render = """            <td style="padding:8px;">
                <div style="display:flex; gap:1px; width:100%; max-width:320px; border-radius:2px; overflow:hidden;">
                    ${heatmapBlocks}
                </div>
            </td>"""
new_heatmap_render = """            <td style="padding:8px; padding-bottom:12px;">
                <div style="display:flex; gap:1px; width:100%; max-width:320px; border-radius:2px; overflow:hidden;">
                    ${heatmapBlocks}
                </div>
                ${axisHtml}
            </td>"""
content = content.replace(old_heatmap_render, new_heatmap_render)

# 5. Show practice buttons in openSubject
old_btn_display = """    document.getElementById('btn-wrong-practice').style.display = 'block';
    document.getElementById('btn-bookmark-practice').style.display = 'block';"""
# It might already exist in openSubject. Let's just make sure it's shown.
# Wait, let's just add it dynamically if not present.
if "document.getElementById('btn-wrong-practice').style.display = 'block';" not in content:
    content = content.replace("currentSubjectTitle.textContent = filterSubject.value;", "currentSubjectTitle.textContent = filterSubject.value;\n    document.getElementById('btn-wrong-practice').style.display = 'block';\n    document.getElementById('btn-bookmark-practice').style.display = 'block';")

# 6. Delete tag function verify
# It's called removeCustomTagFromQ. Let's make sure it updates the UI immediately.
remove_tag_update = """    saveProgress();
    renderCustomTagsSidebar();"""
if "removeCustomTagFromQ" in content and "if (document.getElementById('view-mode').value === 'card') renderCardView();" not in content.split("removeCustomTagFromQ")[1][:500]:
    content = content.replace(
        "renderCustomTagsSidebar();",
        "renderCustomTagsSidebar();\n    if (document.getElementById('view-mode').value === 'card') renderCardView();\n    else renderListView();"
    )

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(content)
print("app.js patched for Phase 11")

