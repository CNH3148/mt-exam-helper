import re

with open("public/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Add Image upload and Custom Tags Sidebar render functions
add_funcs = """
window.toggleBookmark = function(exam_id, no) {
    event.stopPropagation();
    const id = exam_id + '_' + no;
    const idx = globalBookmarks.indexOf(id);
    if (idx > -1) globalBookmarks.splice(idx, 1);
    else globalBookmarks.push(id);
    saveProgress();
    if (document.getElementById('view-mode').value === 'card') renderCardView();
    else renderListView();
};

window.startWrongPractice = function() {
    if (!filterSubject.value) return;
    const allQ = currentData;
    const wrongQs = allQ.filter(q => {
        const id = q.exam_id + '_' + q.no;
        const state = globalAnsweredState[id];
        return state && state.is_fixed === false && state.first_answer !== q.answer;
    });
    if (wrongQs.length === 0) {
        alert('太棒了！目前沒有未修正的錯題。');
        return;
    }
    // Shuffle
    for (let i = wrongQs.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [wrongQs[i], wrongQs[j]] = [wrongQs[j], wrongQs[i]];
    }
    currentActiveTopicData = wrongQs;
    currentPracticeMode = 'wrong';
    startPractice();
    showView('view-topic-detail');
};

window.startBookmarkPractice = function() {
    if (!filterSubject.value) return;
    const allQ = currentData;
    const bookmarkedQs = allQ.filter(q => globalBookmarks.includes(q.exam_id + '_' + q.no));
    if (bookmarkedQs.length === 0) {
        alert('目前沒有收藏的題目。');
        return;
    }
    currentActiveTopicData = bookmarkedQs;
    currentPracticeMode = 'bookmark';
    startPractice();
    showView('view-topic-detail');
};

window.renderCustomTagsSidebar = function() {
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
};

window.filterByCustomTag = function(tag) {
    if (!filterSubject.value) return;
    const ids = globalCustomTags[tag] || [];
    currentActiveTopicData = currentData.filter(q => ids.includes(q.exam_id + '_' + q.no));
    currentPracticeMode = 'normal';
    document.getElementById('view-mode').value = 'list';
    startPractice();
    showView('view-topic-detail');
};

window.removeCustomTagFromQ = function(tag, exam_id, no) {
    event.stopPropagation();
    const id = exam_id + '_' + no;
    if (globalCustomTags[tag]) {
        globalCustomTags[tag] = globalCustomTags[tag].filter(x => x !== id);
        if (globalCustomTags[tag].length === 0) delete globalCustomTags[tag];
        saveProgress();
        renderCustomTagsSidebar();
        if (document.getElementById('view-mode').value === 'card') renderCardView();
        else renderListView();
    }
};

window.saveUserExplanation = function(exam_id, no, val) {
    const id = exam_id + '_' + no;
    globalExplanations[id] = val;
    saveProgress();
    alert('筆記已儲存');
};

window.openImageUploadModal = function(exam_id, no) {
    const pdfUrl = '/pdf/' + filterSubject.value + '_merge.pdf';
    window.open(pdfUrl, '_blank');
    
    document.getElementById('upload-modal-exam-id').value = exam_id;
    document.getElementById('upload-modal-no').value = no;
    document.getElementById('image-upload-modal').style.display = 'flex';
};

window.uploadImage = async function() {
    const exam_id = document.getElementById('upload-modal-exam-id').value;
    const no = document.getElementById('upload-modal-no').value;
    const fileInput = document.getElementById('upload-modal-file');
    if (!fileInput.files || fileInput.files.length === 0) return;
    
    const formData = new FormData();
    formData.append('subject', filterSubject.value);
    formData.append('exam_id', exam_id);
    formData.append('no', no);
    formData.append('file', fileInput.files[0]);
    
    try {
        const res = await fetch('/api/upload_image', {
            method: 'POST',
            body: formData
        });
        const d = await res.json();
        if (d.status === 'success') {
            alert('附圖已更新！請重新載入以查看新圖。');
            document.getElementById('image-upload-modal').style.display = 'none';
            // update in current data array too
            const q = currentData.find(x => x.exam_id == exam_id && x.no == no);
            if (q) q.images = [d.image_url];
            if (document.getElementById('view-mode').value === 'card') renderCardView();
            else renderListView();
        }
    } catch(e) {
        alert('上傳失敗');
    }
};

"""

content += "\n" + add_funcs

# --- 5. Custom Tags Application in applyAdvancedSearch ---
search_old = """    fetch('/api/add_tag_batch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            subject: filterSubject.value,
            questions: qList,
            tag: searchTag.value
        })
    }).then(res => res.json()).then(res => {
        if(res.status === 'success') {
            alert(`已成功將標籤 ${searchTag.value} 加至 ${res.updated_count} 個題目！\\n(若需重新載入，請按 F5 或重新選擇科目)`);
            document.getElementById('advanced-search-modal').style.display = 'none';
            // Optional: Auto refresh the subject data
            loadSubjectData(filterSubject.value).then(() => {
                applyFilters();
            });
        }
    });"""
search_new = """    
    if (!globalCustomTags[searchTag.value]) globalCustomTags[searchTag.value] = [];
    const ids = qList.map(q => q.exam_id + '_' + q.no);
    const setIds = new Set([...globalCustomTags[searchTag.value], ...ids]);
    globalCustomTags[searchTag.value] = Array.from(setIds);
    saveProgress();
    renderCustomTagsSidebar();
    
    alert(`已成功將標籤 ${searchTag.value} 加至 ${qList.length} 個題目！`);
    document.getElementById('advanced-search-modal').style.display = 'none';
    
    // Direct Search to List View
    currentActiveTopicData = results;
    currentPracticeMode = 'normal';
    document.getElementById('view-mode').value = 'list';
    startPractice();
    showView('view-topic-detail');
"""
content = content.replace(search_old, search_new)

# if searchTag is empty but they just search, also redirect to list view
search_logic_old = """    let results = currentData;
    
    // Parse complex syntax
    const commands = searchQuery.value.split(/\\s+/);"""
search_logic_new = """    let results = currentData;
    
    // Parse complex syntax
    const commands = searchQuery.value.split(/\\s+/);
    if (!searchTag.value.trim() && commands.length > 0 && searchQuery.value.trim()) {
        setTimeout(() => {
            currentActiveTopicData = results;
            currentPracticeMode = 'normal';
            document.getElementById('view-mode').value = 'list';
            startPractice();
            showView('view-topic-detail');
            document.getElementById('advanced-search-modal').style.display = 'none';
        }, 100);
    }"""
content = content.replace(search_logic_old, search_logic_new)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated app.js part 2 successfully.")

