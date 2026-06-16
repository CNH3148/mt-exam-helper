import re

js_path = 'public/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Let's replace applyFilters entirely.
apply_filters_new = r"""
async function loadMultiSubjectData() {
    const selectedSubs = Array.from(document.querySelectorAll('.multi-subject-cb:checked')).map(cb => cb.value);
    let allQuestions = [];
    
    // Disable UI or show loading
    const oldTitle = currentSubjectTitle.textContent;
    currentSubjectTitle.textContent = '載入中...';
    currentSubjectTitle.style.display = 'block';
    
    for (const sub of selectedSubs) {
        if (sub === currentActiveSubject && currentData.length > 0) {
            allQuestions = allQuestions.concat(currentData.map(q => ({...q, subject: sub})));
        } else {
            try {
                const res = await fetch(`../data/${sub}.json?v=${Date.now()}`);
                if (res.ok) {
                    const data = await res.json();
                    allQuestions = allQuestions.concat(data.map(q => ({...q, subject: sub})));
                }
            } catch(e) { console.error("Fetch err", sub, e); }
        }
    }
    
    currentSubjectTitle.textContent = oldTitle;
    return allQuestions;
}

async function applyFilters() {
    bcTopic.style.display = 'none';
    bcSepTopic.style.display = 'none';
    bcPractice.style.display = 'none';
    bcSepPractice.style.display = 'none';
    viewToggleContainer.style.display = 'none';
    listAccuracy.style.display = 'none';
    
    const checkedYears = Array.from(document.querySelectorAll('.year-checkbox:checked')).map(cb => cb.value);
    
    if (globalMode === 'general') {
        const sub = filterSubject.value;
        if (!sub) {
            filteredData = [];
            topicGroups = {};
            switchView('topic-list');
            return;
        }
        
        currentSubjectTitle.textContent = `${sub}`;
        currentSubjectTitle.style.display = 'none'; // hide in general mode header
        
        filteredData = currentData.filter(q => {
            let hasYear = false;
            if (q.tags) {
                for (let t of q.tags) {
                    const match = t.match(/\d{3}-\d/);
                    if (match && checkedYears.includes(match[0])) { hasYear = true; break; }
                }
            }
            return hasYear || checkedYears.length === 0;
        });
        
        topicGroups = {};
        filteredData.forEach(q => {
            const t = q.topic || '未分類';
            if (!topicGroups[t]) topicGroups[t] = [];
            topicGroups[t].push(q);
        });
        
        renderTopicList();
        switchView('topic-list');
        
    } else {
        // Multi-subject modes: wrong, bookmark, search
        let multiData = await loadMultiSubjectData();
        
        // 1. Year filter
        multiData = multiData.filter(q => {
            let hasYear = false;
            if (q.tags) {
                for (let t of q.tags) {
                    const match = t.match(/\d{3}-\d/);
                    if (match && checkedYears.includes(match[0])) { hasYear = true; break; }
                }
            }
            return hasYear || checkedYears.length === 0;
        });
        
        // 2. Mode specific filter
        if (globalMode === 'wrong') {
            currentSubjectTitle.textContent = '❌ 跨科錯題';
            multiData = multiData.filter(q => getAnswerState(q) === 'wrong');
        } else if (globalMode === 'bookmark') {
            currentSubjectTitle.textContent = '⭐ 跨科收藏';
            multiData = multiData.filter(q => isBookmarked(q));
        } else if (globalMode === 'search') {
            currentSubjectTitle.textContent = '🔍 搜尋與標籤';
            const regexInput = document.getElementById('regex-search-input');
            const query = regexInput ? regexInput.value.trim() : '';
            
            // Selected custom tags (union)
            const checkedTags = Array.from(document.querySelectorAll('.custom-tag-cb:checked')).map(cb => cb.value);
            
            let regex = null;
            if (query) { try { regex = new RegExp(query, 'i'); } catch(e){} }
            
            multiData = multiData.filter(q => {
                // Check custom tags (Union logic)
                let hasTag = false;
                if (checkedTags.length > 0) {
                    const id = q.exam_id + '_' + q.no;
                    const subStore = getSubStore(q);
                    for (let tag of checkedTags) {
                        if (subStore.customTags && subStore.customTags[tag] && subStore.customTags[tag].includes(id)) {
                            hasTag = true;
                            break;
                        }
                    }
                    if (!hasTag) return false;
                }
                
                // Check Regex/Keyword
                if (query) {
                    const text = (q.question + " " + q.choices.join(" ") + " " + (q.tags ? q.tags.join(" ") : ""));
                    if (regex) {
                        if (!regex.test(text)) return false;
                    } else {
                        if (!text.toLowerCase().includes(query.toLowerCase())) return false;
                    }
                }
                return true;
            });
        }
        
        currentActiveTopicData = multiData;
        currentPracticeMode = globalMode === 'search' ? 'custom_tag' : globalMode; 
        
        switchView('practice');
        switchMode('list');
        startPractice();
    }
}
"""

js = re.sub(r'function applyFilters\(\)\s*\{.*?(?=function renderTopicList)', lambda m: apply_filters_new + "\n", js, flags=re.DOTALL)


# Also remove `searchInput` reference at the top if it fails, actually `searchInput` was removed from HTML.
js = re.sub(r'const searchInput = document.getElementById\(\'search-input\'\);\n?', '', js)
js = re.sub(r'const btnAdvancedSearch = document.getElementById\(\'btn-advanced-search\'\);\n?', '', js)

# 2. Add History Dropdown and Batch Tag logic
history_logic = r"""
// --- Search Mode Tools Logic ---
const regexInput = document.getElementById('regex-search-input');
const regexHistoryToggle = document.getElementById('regex-history-toggle');
const regexHistoryMenu = document.getElementById('regex-history-menu');
const batchTagInput = document.getElementById('batch-tag-input');
const btnBatchTag = document.getElementById('btn-batch-tag');

function loadRegexHistory() {
    if (!regexHistoryMenu) return;
    const history = JSON.parse(localStorage.getItem('regexHistory') || '[]');
    regexHistoryMenu.innerHTML = '';
    if (history.length === 0) {
        regexHistoryMenu.innerHTML = '<div style="padding:8px 12px; color:var(--text-muted); font-size:13px;">無歷史紀錄</div>';
    } else {
        history.forEach((h, i) => {
            const div = document.createElement('div');
            div.className = 'dropdown-item';
            div.innerHTML = `<span>${h}</span><span class="del-btn">✖</span>`;
            div.querySelector('span').onclick = () => {
                if(regexInput) regexInput.value = h;
                regexHistoryMenu.style.display = 'none';
                applyFilters();
            };
            div.querySelector('.del-btn').onclick = (e) => {
                e.stopPropagation();
                history.splice(i, 1);
                localStorage.setItem('regexHistory', JSON.stringify(history));
                loadRegexHistory();
            };
            regexHistoryMenu.appendChild(div);
        });
    }
}

if (regexHistoryToggle) {
    regexHistoryToggle.onclick = (e) => {
        e.stopPropagation();
        loadRegexHistory();
        regexHistoryMenu.style.display = regexHistoryMenu.style.display === 'none' ? 'block' : 'none';
    };
    document.addEventListener('click', (e) => {
        if (regexHistoryMenu && !regexHistoryMenu.contains(e.target) && e.target !== regexHistoryToggle) {
            regexHistoryMenu.style.display = 'none';
        }
    });
}

if (regexInput) {
    regexInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            const val = regexInput.value.trim();
            if (val) {
                const history = JSON.parse(localStorage.getItem('regexHistory') || '[]');
                if (!history.includes(val)) {
                    history.unshift(val);
                    if (history.length > 20) history.pop();
                    localStorage.setItem('regexHistory', JSON.stringify(history));
                }
            }
            applyFilters();
        }
    });
}

if (btnBatchTag) {
    btnBatchTag.onclick = () => {
        const tag = batchTagInput.value.trim();
        if (!tag) { alert("請輸入標籤名稱"); return; }
        if (!currentActiveTopicData || currentActiveTopicData.length === 0) { alert("目前沒有可標記的題目"); return; }
        
        let count = 0;
        currentActiveTopicData.forEach(q => {
            const id = q.exam_id + '_' + q.no;
            const subStore = getSubStore(q);
            if (!subStore.customTags) subStore.customTags = {};
            if (!subStore.customTags[tag]) subStore.customTags[tag] = [];
            
            if (!subStore.customTags[tag].includes(id)) {
                subStore.customTags[tag].push(id);
                count++;
            }
        });
        
        saveProgress();
        batchTagInput.value = '';
        alert(`成功標記 ${count} 題為 [${tag}]！`);
        
        // Re-render custom tags in sidebar
        renderCustomTagsSidebar();
    };
}
"""
if "// --- Search Mode Tools Logic ---" not in js:
    js += "\n" + history_logic

# 3. Modify renderCustomTagsSidebar to populate checkboxes
custom_tags_logic = r"""
function renderCustomTagsSidebar() {
    const container = document.getElementById('custom-tags-checkboxes');
    if (!container) return;
    
    // Gather all tags across all subjects
    let allTags = new Set();
    for (let sub in globalSaveData) {
        if (globalSaveData[sub].customTags) {
            Object.keys(globalSaveData[sub].customTags).forEach(t => allTags.add(t));
        }
    }
    
    // Remember previously checked tags
    const checked = new Set(Array.from(document.querySelectorAll('.custom-tag-cb:checked')).map(cb => cb.value));
    
    container.innerHTML = '';
    if (allTags.size === 0) {
        container.innerHTML = '<div style="color:var(--text-muted); font-size:12px;">尚無標籤</div>';
        return;
    }
    
    Array.from(allTags).sort().forEach(tag => {
        // count total questions
        let count = 0;
        for (let sub in globalSaveData) {
            if (globalSaveData[sub].customTags && globalSaveData[sub].customTags[tag]) {
                count += globalSaveData[sub].customTags[tag].length;
            }
        }
        
        const lbl = document.createElement('label');
        lbl.style.display = 'flex';
        lbl.style.alignItems = 'center';
        lbl.style.gap = '8px';
        lbl.style.fontSize = '13px';
        lbl.style.cursor = 'pointer';
        
        const isChecked = checked.has(tag) ? 'checked' : '';
        lbl.innerHTML = `<input type="checkbox" class="custom-tag-cb" value="${tag}" ${isChecked}> 🏷️ ${tag} (${count})`;
        
        lbl.querySelector('input').addEventListener('change', () => applyFilters());
        container.appendChild(lbl);
    });
}
"""

js = re.sub(r'function renderCustomTagsSidebar\(\)\s*\{.*?\}', lambda m: custom_tags_logic, js, flags=re.DOTALL)

# 4. Modify startPractice to bypass state loading for ALL non-general modes
js = js.replace("if (typeof currentPracticeMode === 'undefined' || (currentPracticeMode !== 'wrong' && currentPracticeMode !== 'bookmark' && currentPracticeMode !== 'custom_tag'))", "if (globalMode === 'general')")


# 5. Fix breadcrumbs logic
js = js.replace("bcSubject.onclick = () => {", "bcSubject.onclick = () => { switchGlobalMode('general');")

# Remove old advanced search functions
js = re.sub(r'function openAdvancedSearchModal\(\)\s*\{.*?\}', '', js, flags=re.DOTALL)
js = re.sub(r'function closeAdvancedSearchModal\(\)\s*\{.*?\}', '', js, flags=re.DOTALL)
js = re.sub(r'function executeAdvancedSearch\(\)\s*\{.*?\}', '', js, flags=re.DOTALL)
js = re.sub(r'function deleteSearchRule\(e, name\)\s*\{.*?\}', '', js, flags=re.DOTALL)
js = re.sub(r'function renderSavedSearches\(\)\s*\{.*?\}', '', js, flags=re.DOTALL)
js = re.sub(r'window\.filterByCustomTag = async function\(tag\)\s*\{.*?\}\;', '', js, flags=re.DOTALL)

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated JS logic part 2")

