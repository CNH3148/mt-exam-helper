import re

with open("public/app.js", "r", encoding="utf-8") as f:
    app = f.read()

# 1. Update saveAdvancedSearch to use Custom Tags instead of add_tag_batch
old_saveAdv = """async function saveAdvancedSearch() {
    const rxStr = advRegex.value.trim();
    const tagName = advTagName.value.trim();
    if (!rxStr || !tagName || !filterSubject.value) return alert('請填寫完整條件');
    
    let rx;
    try { rx = new RegExp(rxStr, 'i'); } 
    catch(e) { return alert('Regex 語法錯誤'); }

    btnAdvSave.disabled = true;
    btnAdvSave.textContent = '處理中...';

    const matchedQs = [];
    currentData.forEach(q => {
        const text = q.question + " " + q.choices.join(" ");
        if (rx.test(text)) {
            matchedQs.push({exam_id: q.exam_id, no: q.no});
            if (!q.tags) q.tags = [];
            if (!q.tags.includes(tagName)) q.tags.push(tagName);
        }
    });

    if (matchedQs.length > 0) {
        try {
            await fetch('/api/add_tag_batch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    subject: filterSubject.value,
                    questions: matchedQs,
                    tag: tagName
                })
            });
            await fetch('/api/save_search_rule', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: tagName, query: rxStr })
            });
            
            alert(`成功！已將 ${matchedQs.length} 題標記為「${tagName}」並儲存規則。`);
            await loadSavedRules();
            advModal.style.display = 'none';
            
            // Update custom tags sidebar before switching
            renderCustomTagsSidebar();
            
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
            
        } catch(e) { alert('儲存失敗'); }
    } else { alert('沒有符合條件的題目'); }
    
    btnAdvSave.disabled = false;
    btnAdvSave.textContent = '儲存並標記';
}"""

new_saveAdv = """async function saveAdvancedSearch() {
    const rxStr = advRegex.value.trim();
    const tagName = advTagName.value.trim();
    if (!rxStr || !tagName || !filterSubject.value) return alert('請填寫完整條件');
    
    let rx;
    try { rx = new RegExp(rxStr); } 
    catch(e) { return alert('Regex 語法錯誤'); }

    btnAdvSave.disabled = true;
    btnAdvSave.textContent = '處理中...';

    const matchedQs = [];
    currentData.forEach(q => {
        const text = q.question + " " + q.choices.join(" ");
        if (rx.test(text)) {
            matchedQs.push({exam_id: q.exam_id, no: q.no});
        }
    });

    if (matchedQs.length > 0) {
        try {
            // Add to Custom Tags instead of global JSON
            if (!globalCustomTags[tagName]) globalCustomTags[tagName] = [];
            matchedQs.forEach(mq => {
                const id = mq.exam_id + '_' + mq.no;
                if (!globalCustomTags[tagName].includes(id)) {
                    globalCustomTags[tagName].push(id);
                }
            });
            saveProgress();

            await fetch('/api/save_search_rule', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name: tagName, query: rxStr })
            });
            
            alert(`成功！已將 ${matchedQs.length} 題標記為自訂標籤「${tagName}」並儲存規則。`);
            await loadSavedRules();
            advModal.style.display = 'none';
            
            // Update custom tags sidebar before switching
            renderCustomTagsSidebar();
            
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
            
        } catch(e) { alert('儲存失敗'); }
    } else { alert('沒有符合條件的題目'); }
    
    btnAdvSave.disabled = false;
    btnAdvSave.textContent = '儲存並標記';
}"""

app = app.replace(old_saveAdv, new_saveAdv)

# 2. Update btnAdvSearchOnly to be case-sensitive (remove 'i' flag)
old_btnSearchOnly = """    if (btnAdvSearchOnly) {
        btnAdvSearchOnly.onclick = () => {
            const rxStr = advRegex.value.trim();
            if (!rxStr || !filterSubject.value) return alert('請填寫搜尋語法與科目');
            let rx;
            try { rx = new RegExp(rxStr, 'i'); } catch(e) { return alert('Regex 語法錯誤'); }
            
            const matchedQs = [];"""

new_btnSearchOnly = """    if (btnAdvSearchOnly) {
        btnAdvSearchOnly.onclick = () => {
            const rxStr = advRegex.value.trim();
            if (!rxStr || !filterSubject.value) return alert('請填寫搜尋語法與科目');
            let rx;
            try { rx = new RegExp(rxStr); } catch(e) { return alert('Regex 語法錯誤'); }
            
            const matchedQs = [];"""

app = app.replace(old_btnSearchOnly, new_btnSearchOnly)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(app)

print("Phase 18 executed.")

