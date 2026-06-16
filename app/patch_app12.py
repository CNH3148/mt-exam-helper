import re

with open("public/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update startPractice to not load history for wrong/bookmark practice
old_startPractice = """    answeredState = {};
    currentActiveTopicData.forEach((q, i) => {
        const id = q.exam_id + '_' + q.no;
        if (globalAnsweredState[id]) {
            // Keep the whole object so we can show first_answer in UI if needed
            answeredState[i] = globalAnsweredState[id];
        }
    });"""
new_startPractice = """    answeredState = {};
    if (typeof currentPracticeMode === 'undefined' || (currentPracticeMode !== 'wrong' && currentPracticeMode !== 'bookmark')) {
        currentActiveTopicData.forEach((q, i) => {
            const id = q.exam_id + '_' + q.no;
            if (globalAnsweredState[id]) {
                answeredState[i] = globalAnsweredState[id];
            }
        });
    }"""
content = content.replace(old_startPractice, new_startPractice)


# 2. Update toggleBookmark to animate directly
old_toggleBookmark = """window.toggleBookmark = function(exam_id, no) {
    if (window.event) window.event.stopPropagation();
    const id = exam_id + '_' + no;
    const idx = globalBookmarks.indexOf(id);
    if (idx === -1) globalBookmarks.push(id);
    else globalBookmarks.splice(idx, 1);
    saveProgress();
    if (document.getElementById('view-mode').value === 'card') renderCardView();
    else renderListView();
};"""
new_toggleBookmark = """window.toggleBookmark = function(exam_id, no) {
    let evt = window.event;
    if (evt) evt.stopPropagation();
    const id = exam_id + '_' + no;
    const idx = globalBookmarks.indexOf(id);
    if (idx === -1) globalBookmarks.push(id);
    else globalBookmarks.splice(idx, 1);
    saveProgress();
    
    if (evt && evt.currentTarget && evt.currentTarget.classList.contains('star-icon')) {
        const el = evt.currentTarget;
        if (idx === -1) {
            el.classList.add('active');
            el.classList.remove('inactive');
            el.innerHTML = '★';
        } else {
            el.classList.remove('active');
            el.classList.add('inactive');
            el.innerHTML = '☆';
        }
    } else {
        if (document.getElementById('view-mode').value === 'card') renderCardView();
        else renderListView();
    }
};"""
content = content.replace(old_toggleBookmark, new_toggleBookmark)

# Make sure star-icon class is applied to ALL stars (it failed in Phase 11)
old_star1 = """onclick="toggleBookmark('${q.exam_id}', '${q.no}')" style="cursor:pointer; color:#facc15; margin-left:8px;\">"""
new_star1 = """onclick="toggleBookmark('${q.exam_id}', '${q.no}')" class="star-icon ${isBookmarked ? 'active' : 'inactive'}" style="cursor:pointer; margin-left:8px;\">"""
# First reset any weird states
content = re.sub(r'onclick="toggleBookmark.*?style="cursor:pointer; color:#facc15; margin-left:8px;"(?: class="star-icon")?>',
                 """onclick="toggleBookmark('${q.exam_id}', '${q.no}')" class="star-icon ${isBookmarked ? 'active' : 'inactive'}" style="cursor:pointer; margin-left:8px;">""", content)


# 3. Update saveAdvancedSearch to switch to List mode
old_saveSearch = """            alert(`成功！已將 ${matchedQs.length} 題標記為「${tagName}」並儲存規則。`);
            await loadSavedRules();
            document.getElementById('advanced-search-modal').style.display = 'none';"""
new_saveSearch = """            alert(`成功！已將 ${matchedQs.length} 題標記為「${tagName}」並儲存規則。`);
            await loadSavedRules();
            document.getElementById('advanced-search-modal').style.display = 'none';
            
            // Show list view for these questions
            currentActiveTopicData = currentData.filter(q => matchedQs.some(m => m.exam_id === q.exam_id && m.no === q.no));
            currentPracticeMode = 'normal';
            showView('view-topic-detail');
            switchMode('list');
            startPractice();"""
content = content.replace(old_saveSearch, new_saveSearch)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(content)
print("app.js patched.")

