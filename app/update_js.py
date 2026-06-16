import re

js_path = 'public/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Add globalMode variable and its logic
if "let globalMode = 'general';" not in js:
    js = js.replace("let currentPracticeMode = 'normal';", "let currentPracticeMode = 'normal';\nlet globalMode = 'general'; // 'general', 'wrong', 'bookmark', 'search'")

# We need to add the switchGlobalMode function and event listeners
mode_logic = """
// --- Global Mode Logic ---
const modeGeneralBtn = document.getElementById('mode-general');
const modeWrongBtn = document.getElementById('mode-wrong');
const modeBookmarkBtn = document.getElementById('mode-bookmark');
const modeSearchBtn = document.getElementById('mode-search');
const filterSubjectMulti = document.getElementById('filter-subject-multi');
const searchModeTools = document.getElementById('search-mode-tools');

function switchGlobalMode(mode) {
    globalMode = mode;
    
    // Update button UI
    if(modeGeneralBtn) modeGeneralBtn.className = mode === 'general' ? 'btn btn-primary active' : 'btn btn-secondary';
    if(modeWrongBtn) modeWrongBtn.className = mode === 'wrong' ? 'btn btn-primary active' : 'btn btn-secondary';
    if(modeBookmarkBtn) modeBookmarkBtn.className = mode === 'bookmark' ? 'btn btn-primary active' : 'btn btn-secondary';
    if(modeSearchBtn) modeSearchBtn.className = mode === 'search' ? 'btn btn-primary active' : 'btn btn-secondary';
    
    // Update Sidebar UI
    if (mode === 'general') {
        filterSubject.style.display = 'block';
        if(filterSubjectMulti) filterSubjectMulti.style.display = 'none';
        if(searchModeTools) searchModeTools.style.display = 'none';
    } else {
        filterSubject.style.display = 'none';
        if(filterSubjectMulti) filterSubjectMulti.style.display = 'block';
        if(searchModeTools) searchModeTools.style.display = (mode === 'search') ? 'flex' : 'none';
    }
    
    applyFilters();
}

if (modeGeneralBtn) modeGeneralBtn.onclick = () => switchGlobalMode('general');
if (modeWrongBtn) modeWrongBtn.onclick = () => switchGlobalMode('wrong');
if (modeBookmarkBtn) modeBookmarkBtn.onclick = () => switchGlobalMode('bookmark');
if (modeSearchBtn) modeSearchBtn.onclick = () => switchGlobalMode('search');
"""

if "// --- Global Mode Logic ---" not in js:
    js += "\n" + mode_logic

# 2. Modify populateMultiSelect to populate #filter-subject-multi
multi_select_logic = """
function populateMultiSelect() {
    if (!filterSubjectMulti) return;
    filterSubjectMulti.innerHTML = '';
    const allOpt = document.createElement('label');
    allOpt.className = 'subject-multi-lbl';
    allOpt.innerHTML = `<input type="checkbox" id="multi-subject-all"> <b>全選 / 全不選</b>`;
    filterSubjectMulti.appendChild(allOpt);
    
    const checkboxes = [];
    const subjects = Array.from(filterSubject.options).map(o => o.value).filter(v => v);
    subjects.forEach(sub => {
        const lbl = document.createElement('label');
        lbl.className = 'subject-multi-lbl';
        lbl.innerHTML = `<input type="checkbox" class="multi-subject-cb" value="${sub}"> ${sub}`;
        filterSubjectMulti.appendChild(lbl);
        checkboxes.push(lbl.querySelector('input'));
    });
    
    const allCb = document.getElementById('multi-subject-all');
    allCb.onchange = (e) => {
        checkboxes.forEach(cb => cb.checked = e.target.checked);
        applyFilters();
    };
    checkboxes.forEach(cb => {
        cb.onchange = () => {
            allCb.checked = checkboxes.every(c => c.checked);
            applyFilters();
        };
    });
}
"""

if "function populateMultiSelect()" in js:
    js = re.sub(r'function populateMultiSelect\(\)\s*\{.*?\}', multi_select_logic, js, flags=re.DOTALL)
else:
    js += "\n" + multi_select_logic

# make sure it is called when subjects are loaded
if "populateMultiSelect();" not in js:
    # After loadSubjectList
    js = js.replace("loadSubjectList();", "loadSubjectList();\n    populateMultiSelect();")

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)
print("Updated JS global mode & multi select")

