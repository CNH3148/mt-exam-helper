import re

with open("public/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add star bookmark to Card mode question header
old_header = """                        <div class="question-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                            <div>
                                <span class="badge" id="q-no">Q 1</span>
                                <span style="font-size: 12px; color: var(--text-secondary); margin-left: 12px;">💡 小提示：框選文字後按下 `T` 鍵即可將其加為標籤</span>
                            </div>"""
new_header = """                        <div class="question-header" style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                            <div style="display:flex; align-items:center; gap:8px;">
                                <span class="badge" id="q-no" style="margin:0;">Q 1</span>
                                <div id="q-bookmark" class="bookmark-btn" style="margin:0;">☆</div>
                                <span style="font-size: 12px; color: var(--text-secondary); margin-left: 12px;">💡 小提示：框選文字後按下 `T` 鍵即可將其加為標籤</span>
                            </div>"""
html = html.replace(old_header, new_header)
with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)


with open("public/style.css", "r", encoding="utf-8") as f:
    css = f.read()

# 2. Fix layout grid
css = css.replace("grid-template-columns: 1fr 1fr;", "grid-template-columns: 2fr 1fr;")
with open("public/style.css", "w", encoding="utf-8") as f:
    f.write(css)


with open("public/app.js", "r", encoding="utf-8") as f:
    app = f.read()

# 3. Update toggleBookmark
old_toggle = """window.toggleBookmark = function(e, exam_id, no) {
    e.stopPropagation();
    
    const id = exam_id + '_' + no;
    const idx = globalBookmarks.indexOf(id);
    if (idx > -1) globalBookmarks.splice(idx, 1);
    else globalBookmarks.push(id);
    saveProgress();
    if (document.getElementById('view-mode').value === 'card') renderCardView();
    else renderListView();
};"""
new_toggle = """window.toggleBookmark = function(e, exam_id, no) {
    if(e) e.stopPropagation();
    
    const id = exam_id + '_' + no;
    const idx = globalBookmarks.indexOf(id);
    if (idx > -1) globalBookmarks.splice(idx, 1);
    else globalBookmarks.push(id);
    saveProgress();
    
    // Animation
    if(e && e.target) {
        e.target.classList.toggle('active');
        e.target.style.transform = 'scale(1.2)';
        setTimeout(() => e.target.style.transform = 'scale(1)', 200);
    }
};"""
app = app.replace(old_toggle, new_toggle)

# 4. Fix renderCustomTagsSidebar
old_renderCustom = """window.renderCustomTagsSidebar = function() {
    const container = document.getElementById('custom-tags-sidebar');
    if (!container) return; // in case we haven't added it to index.html yet
    let html = '<ul style="list-style:none; padding:0; margin:0; margin-top:12px;">';
    for (let tag in globalCustomTags) {
        html += `<li style="padding: 8px 12px; cursor: pointer; color: var(--text-secondary); border-radius: 6px; margin-bottom: 4px; display:flex; justify-content:space-between; align-items:center;" class="sidebar-item" onclick="filterByCustomTag('${tag}')">
            <span>🏷️ ${tag}</span>
            <span style="font-size:12px; background:var(--glass-border); padding:2px 6px; border-radius:10px;">${globalCustomTags[tag].length}</span>
        </li>`;
    }
    html += '</ul>';
    container.innerHTML = html;
};"""
new_renderCustom = """window.renderCustomTagsSidebar = function() {
    const container = document.getElementById('custom-tags-container');
    if (!container) return; 
    let html = '<div style="font-size:12px; color:var(--text-muted); margin-bottom:8px;">自訂標籤</div>';
    html += '<ul style="list-style:none; padding:0; margin:0;">';
    for (let tag in globalCustomTags) {
        html += `<li style="padding: 8px 12px; cursor: pointer; color: var(--text-secondary); border-radius: 6px; margin-bottom: 4px; display:flex; justify-content:space-between; align-items:center;" class="sidebar-item" onclick="filterByCustomTag('${tag}')">
            <span>🏷️ ${tag}</span>
            <span style="font-size:12px; background:var(--glass-border); padding:2px 6px; border-radius:10px;">${globalCustomTags[tag].length}</span>
        </li>`;
    }
    html += '</ul>';
    container.innerHTML = html;
    container.style.display = 'block';
};"""
app = app.replace(old_renderCustom, new_renderCustom)

# 5. Fix filterByCustomTag
old_filterBy = """window.filterByCustomTag = function(tag) {
    if (!filterSubject.value) return;
    const ids = globalCustomTags[tag] || [];
    currentActiveTopicData = currentData.filter(q => ids.includes(q.exam_id + '_' + q.no));
    currentPracticeMode = 'normal';
    document.getElementById('view-mode').value = 'list';
    startPractice();
    showView('view-topic-detail');
};"""
new_filterBy = """window.filterByCustomTag = function(tag) {
    if (!filterSubject.value) return;
    const ids = globalCustomTags[tag] || [];
    currentActiveTopicData = currentData.filter(q => ids.includes(q.exam_id + '_' + q.no));
    currentPracticeMode = 'normal';
    switchView('practice');
    switchMode('list');
    startPractice();
};"""
app = app.replace(old_filterBy, new_filterBy)

# 6. Fix duplicate code in addManualCustomTag
old_addManual = """window.addManualCustomTag = function(exam_id, no, val) {
    val = val.trim();
    if (!val) return;
    if (!globalCustomTags[val]) globalCustomTags[val] = [];
    const id = exam_id + '_' + no;
    if (!globalCustomTags[val].includes(id)) {
        globalCustomTags[val].push(id);
        saveProgress();
        renderCustomTagsSidebar();
    if (currentMode === 'card') renderCardView();
    else renderListView();
        if (currentMode === 'card') renderCardView();
        else renderListView();
    }
};"""
new_addManual = """window.addManualCustomTag = function(exam_id, no, val) {
    val = val.trim();
    if (!val) return;
    if (!globalCustomTags[val]) globalCustomTags[val] = [];
    const id = exam_id + '_' + no;
    if (!globalCustomTags[val].includes(id)) {
        globalCustomTags[val].push(id);
        saveProgress();
        renderCustomTagsSidebar();
        if (currentMode === 'card') renderCardView();
        else renderListView();
    }
};"""
app = app.replace(old_addManual, new_addManual)

# 7. Fix duplicate code in removeCustomTagFromQ
old_removeCustom = """window.removeCustomTagFromQ = function(tag, exam_id, no) {
    const id = exam_id + '_' + no;
    if (globalCustomTags[tag]) {
        globalCustomTags[tag] = globalCustomTags[tag].filter(x => x !== id);
        if (globalCustomTags[tag].length === 0) delete globalCustomTags[tag];
        saveProgress();
        renderCustomTagsSidebar();
    if (currentMode === 'card') renderCardView();
    else renderListView();
        if (currentMode === 'card') renderCardView();
        else renderListView();
    }
};"""
new_removeCustom = """window.removeCustomTagFromQ = function(tag, exam_id, no) {
    const id = exam_id + '_' + no;
    if (globalCustomTags[tag]) {
        globalCustomTags[tag] = globalCustomTags[tag].filter(x => x !== id);
        if (globalCustomTags[tag].length === 0) delete globalCustomTags[tag];
        saveProgress();
        renderCustomTagsSidebar();
        if (currentMode === 'card') renderCardView();
        else renderListView();
    }
};"""
app = app.replace(old_removeCustom, new_removeCustom)

# 8. Save Advanced Search automatically switch to list mode
old_saveAdv = """            alert(`成功！已將 ${matchedQs.length} 題標記為「${tagName}」並儲存規則。`);
            await loadSavedRules();
            applyFilters();
            advModal.style.display = 'none';
        } catch(e) { alert('儲存失敗'); }"""
new_saveAdv = """            alert(`成功！已將 ${matchedQs.length} 題標記為「${tagName}」並儲存規則。`);
            await loadSavedRules();
            advModal.style.display = 'none';
            
            // Switch to list view with matched questions
            let matchedQuestionsObjects = [];
            currentData.forEach(q => {
                if (matchedQs.some(mq => mq.exam_id === q.exam_id && mq.no === q.no)) {
                    matchedQuestionsObjects.push(q);
                }
            });
            currentActiveTopicData = matchedQuestionsObjects;
            currentPracticeMode = 'normal';
            switchView('practice');
            switchMode('list');
            startPractice();
            
        } catch(e) { alert('儲存失敗'); }"""
app = app.replace(old_saveAdv, new_saveAdv)

# 9. Update renderCardView with Star Button logic
# We need to find the `qNo.textContent` line and inject logic right after.
old_renderCard_qNo = """    qNo.textContent = `Q ${currentIndex + 1} / ${currentActiveTopicData.length}`;
    
    qTags.innerHTML = '';"""
new_renderCard_qNo = """    qNo.textContent = `Q ${currentIndex + 1} / ${currentActiveTopicData.length}`;
    const starBtn = document.getElementById('q-bookmark');
    if (starBtn) {
        const isBookmarked = globalBookmarks.includes(q.exam_id + '_' + q.no);
        starBtn.className = isBookmarked ? 'bookmark-btn active' : 'bookmark-btn';
        starBtn.onclick = (e) => toggleBookmark(e, q.exam_id, q.no);
    }
    
    qTags.innerHTML = '';"""
app = app.replace(old_renderCard_qNo, new_renderCard_qNo)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(app)

print("Phase 14 executed.")

