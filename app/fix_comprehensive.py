"""
Comprehensive fix for app.js:
1. Fix broken switchMode function (the setTimeout was never closed properly)
2. Remove duplicate mode switching code at the bottom (switchGlobalMode vs updateSidebarUI)
3. Fix regexHistoryMenu references → use the correct regexHistoryDropdown
4. Remove references to non-existent DOM elements (search-input, subject-list, btn-wrong-practice, btn-bookmark-practice)
5. Unify the mode switching to use only switchGlobalMode
6. Fix the toggle switch initial state
"""

with open('public/app.js', 'r', encoding='utf-8') as f:
    content = f.read()

# ===== FIX 1: Fix the broken switchMode function (lines ~1023-1069) =====
# The card branch's setTimeout was never closed and toggle code got injected inside it
old_switchMode = '''function switchMode(mode) {
    currentMode = mode;
    // toggle class removed
    if (currentActiveTopicData.length === 0) {
        if (mode === 'card') {
            switchView('practice');
            const cc = document.getElementById('card-container');
            if (cc) cc.innerHTML = '<div style="padding:20px;text-align:center;color:var(--text-muted);">沒有符合條件的題目，請在左側選擇科目或調整過濾條件。</div>';
        } else {
            switchView('list');
            const lc = document.getElementById('list-container');
            if (lc) lc.innerHTML = '<div style="padding:20px;text-align:center;color:var(--text-muted);">沒有符合條件的題目，請在左側選擇科目或調整過濾條件。</div>';
        }
        return;
    }
    
    if (mode === 'card') {
        switchView('practice');
        renderCardView();
        setTimeout(() => {
            // No need to scroll, it's just one card
        
    // UI updates for the new toggle switch
    const modeCheckbox = document.getElementById('mode-toggle-checkbox');
    const lblCard = document.getElementById('label-mode-card');
    const lblList = document.getElementById('label-mode-list');
    
    if (modeCheckbox) {
        modeCheckbox.checked = (mode === 'list');
        if (mode === 'list') {
            lblList.style.color = 'var(--text-main)';
            lblCard.style.color = 'var(--text-secondary)';
        } else {
            lblCard.style.color = 'var(--text-main)';
            lblList.style.color = 'var(--text-secondary)';
        }
    }
}, 10);
    } else {
        switchView('list');
        renderListView();
        setTimeout(() => {
            const el = document.getElementById('list-card-' + currentIndex);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }
}'''

new_switchMode = '''function switchMode(mode) {
    currentMode = mode;
    
    // Update toggle switch UI
    const modeCheckbox = document.getElementById('mode-toggle-checkbox');
    const lblCard = document.getElementById('label-mode-card');
    const lblList = document.getElementById('label-mode-list');
    
    if (modeCheckbox) {
        modeCheckbox.checked = (mode === 'list');
        if (mode === 'list') {
            if (lblList) lblList.style.color = 'var(--text-main)';
            if (lblCard) lblCard.style.color = 'var(--text-secondary)';
        } else {
            if (lblCard) lblCard.style.color = 'var(--text-main)';
            if (lblList) lblList.style.color = 'var(--text-secondary)';
        }
    }
    
    if (currentActiveTopicData.length === 0) {
        if (mode === 'card') {
            switchView('practice');
            const qTextEl = document.getElementById('q-text');
            if (qTextEl) qTextEl.textContent = '沒有符合條件的題目，請在左側選擇科目或調整過濾條件。';
        } else {
            switchView('list');
            const lc = document.getElementById('list-container');
            if (lc) lc.innerHTML = '<div style="padding:20px;text-align:center;color:var(--text-muted);">沒有符合條件的題目，請在左側選擇科目或調整過濾條件。</div>';
        }
        return;
    }
    
    // Remember current question index for scrolling after switch
    const prevIndex = currentIndex;
    
    if (mode === 'card') {
        switchView('practice');
        renderCardView();
    } else {
        switchView('list');
        renderListView();
        setTimeout(() => {
            const el = document.getElementById('list-card-' + prevIndex);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }
}'''

content = content.replace(old_switchMode, new_switchMode)

# ===== FIX 2: Fix updateSidebarUI — remove references to non-existent elements =====
old_updateSidebarUI = '''function updateSidebarUI() {
    [modeBtnGeneral, modeBtnWrong, modeBtnBookmark, modeBtnSearch].forEach(b => {
        b.classList.remove('btn-primary');
        b.classList.add('btn-secondary');
    });
    
    if (globalPracticeMode === 'general') {
        modeBtnGeneral.classList.remove('btn-secondary');
        modeBtnGeneral.classList.add('btn-primary');
        filterSubject.style.display = 'block';
        filterSubjectMulti.style.display = 'none';
        searchModeTools.style.display = 'none';
        document.getElementById('search-input').style.display = 'block';
        document.getElementById('subject-list').style.display = 'block'; // the nav list
    } else {
        filterSubject.style.display = 'none';
        filterSubjectMulti.style.display = 'block';
        document.getElementById('search-input').style.display = 'none';
        document.getElementById('subject-list').style.display = 'none';
        
        if (globalPracticeMode === 'wrong') {
            modeBtnWrong.classList.remove('btn-secondary');
            modeBtnWrong.classList.add('btn-primary');
            searchModeTools.style.display = 'none';
        } else if (globalPracticeMode === 'bookmark') {
            modeBtnBookmark.classList.remove('btn-secondary');
            modeBtnBookmark.classList.add('btn-primary');
            searchModeTools.style.display = 'none';
        } else if (globalPracticeMode === 'search') {
            modeBtnSearch.classList.remove('btn-secondary');
            modeBtnSearch.classList.add('btn-primary');
            searchModeTools.style.display = 'flex';
            renderCustomTagsCheckboxes();
        }
        
        // Ensure years are loaded
        updateMultiYearCheckboxes();
    }
}'''

# This function is obsoleted by switchGlobalMode below. Let's replace it.
new_updateSidebarUI = '''function updateSidebarUI() {
    // This is now handled by switchGlobalMode
    switchGlobalMode(globalPracticeMode);
}'''

content = content.replace(old_updateSidebarUI, new_updateSidebarUI)

# ===== FIX 3: Fix the mode button event listeners (lines ~1831-1834) =====
# These use globalPracticeMode but the correct unified variable is globalMode
# Also, they call executeMultiModePractice which uses '.subject-filter-cb' (wrong class name)
# Replace them to call switchGlobalMode instead
old_modeListeners = """modeBtnGeneral.addEventListener('click', () => { globalPracticeMode = 'general'; updateSidebarUI(); if(filterSubject.value) onSubjectChange(); });
modeBtnWrong.addEventListener('click', () => { globalPracticeMode = 'wrong'; updateSidebarUI(); executeMultiModePractice(); });
modeBtnBookmark.addEventListener('click', () => { globalPracticeMode = 'bookmark'; updateSidebarUI(); executeMultiModePractice(); });
modeBtnSearch.addEventListener('click', () => { globalPracticeMode = 'search'; updateSidebarUI(); /* execute is triggered manually by btn */ });"""

new_modeListeners = """// Mode button clicks are handled by switchGlobalMode (see bottom of file)
// Removed duplicate listeners here to avoid conflicts."""

content = content.replace(old_modeListeners, new_modeListeners)

# ===== FIX 4: Fix onSubjectChange — remove references to non-existent elements =====
old_subjectRefs = """    currentSubjectTitle.textContent = sub;
    document.getElementById('btn-wrong-practice').style.display = 'block';
    document.getElementById('btn-bookmark-practice').style.display = 'block';"""

new_subjectRefs = """    currentSubjectTitle.textContent = sub;"""

content = content.replace(old_subjectRefs, new_subjectRefs)

# ===== FIX 5: Fix switchGlobalMode at the bottom to be the single source of truth =====
old_switchGlobalMode = '''function switchGlobalMode(mode) {
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
if (modeSearchBtn) modeSearchBtn.onclick = () => switchGlobalMode('search');'''

new_switchGlobalMode = '''function switchGlobalMode(mode) {
    globalMode = mode;
    globalPracticeMode = mode; // Keep both in sync
    
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
        filterYearContainer.style.display = (filterSubject.value) ? 'block' : 'none';
    } else {
        filterSubject.style.display = 'none';
        if(filterSubjectMulti) filterSubjectMulti.style.display = 'block';
        if(searchModeTools) searchModeTools.style.display = (mode === 'search') ? 'flex' : 'none';
        if (mode === 'search') renderCustomTagsCheckboxes();
    }
    
    // Hide the big h1 title — everything is in the breadcrumb now
    currentSubjectTitle.style.display = 'none';
    
    applyFilters();
}

if (modeGeneralBtn) modeGeneralBtn.onclick = () => switchGlobalMode('general');
if (modeWrongBtn) modeWrongBtn.onclick = () => switchGlobalMode('wrong');
if (modeBookmarkBtn) modeBookmarkBtn.onclick = () => switchGlobalMode('bookmark');
if (modeSearchBtn) modeSearchBtn.onclick = () => switchGlobalMode('search');'''

content = content.replace(old_switchGlobalMode, new_switchGlobalMode)

# ===== FIX 6: Fix all regexHistoryMenu references → regexHistoryDropdown =====
content = content.replace('regexHistoryMenu.style.display', 'regexHistoryDropdown.style.display')
content = content.replace('regexHistoryMenu.innerHTML', 'regexHistoryDropdown.innerHTML')
content = content.replace('regexHistoryMenu.contains', 'regexHistoryDropdown.contains')
content = content.replace('regexHistoryMenu.appendChild', 'regexHistoryDropdown.appendChild')

# ===== FIX 7: Fix the h1 title always being hidden =====
# In applyFilters, the currentSubjectTitle is sometimes set to display: 'block'
# We want it always hidden since the breadcrumb handles everything
content = content.replace(
    "currentSubjectTitle.textContent = '載入中...';\n    currentSubjectTitle.style.display = 'block';",
    "// Loading handled by breadcrumb\n    // currentSubjectTitle.style.display = 'none';"
)

# Also hide it in applyFilters general mode
content = content.replace(
    "currentSubjectTitle.style.display = 'none'; // hide in general mode header",
    "currentSubjectTitle.style.display = 'none';"
)

with open('public/app.js', 'w', encoding='utf-8') as f:
    f.write(content)

print("All fixes applied to app.js!")

