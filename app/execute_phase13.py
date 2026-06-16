import re

with open("public/app.js", "r", encoding="utf-8") as f:
    app = f.read()

# 1. Req 1: switchView should toggle practice action buttons
old_switchView = """function switchView(viewName) {
    viewTopicList.classList.remove('active');
    viewTopicDetail.classList.remove('active');
    viewPractice.classList.remove('active');
    viewList.classList.remove('active');"""

new_switchView = """function switchView(viewName) {
    viewTopicList.classList.remove('active');
    viewTopicDetail.classList.remove('active');
    viewPractice.classList.remove('active');
    viewList.classList.remove('active');
    
    // Req 1: Only show practice buttons on topic list
    const pBtns = document.getElementById('header-practice-actions');
    if (pBtns) {
        pBtns.style.display = (viewName === 'topic-list') ? 'flex' : 'none';
    }"""
app = app.replace(old_switchView, new_switchView)

# 2. Req 2 & 3: view-mode check -> currentMode
app = app.replace("document.getElementById('view-mode').value === 'card'", "currentMode === 'card'")

# 3. Req 4: renderListView ID and switchMode scrollIntoView
app = app.replace("card.className = 'list-card';", "card.className = 'list-card';\n        card.id = 'list-card-' + idx;")

old_switchMode_scroll = """    if (mode === 'card') {
        switchView('practice');
        renderCardView();
    } else {
        switchView('list');
        renderListView();
        setTimeout(() => {
            const el = document.getElementById('list-exp-' + currentIndex);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }"""
new_switchMode_scroll = """    if (mode === 'card') {
        switchView('practice');
        renderCardView();
        setTimeout(() => {
            // No need to scroll, it's just one card
        }, 10);
    } else {
        switchView('list');
        renderListView();
        setTimeout(() => {
            const el = document.getElementById('list-card-' + currentIndex);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }"""
app = app.replace(old_switchMode_scroll, new_switchMode_scroll)

# 4. Req 5: General Search Enter to list mode
old_listeners = """    // Listeners
    filterSubject.addEventListener('change', onSubjectChange);
    searchInput.addEventListener('input', applyFilters);"""
new_listeners = """    // Listeners
    filterSubject.addEventListener('change', onSubjectChange);
    searchInput.addEventListener('input', applyFilters);
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            const q = searchInput.value.toLowerCase().trim();
            if (q) {
                let matched = [];
                currentData.forEach(question => {
                    const text = question.question + " " + question.choices.join(" ");
                    if (text.toLowerCase().includes(q)) matched.push(question);
                });
                if (matched.length > 0) {
                    currentActiveTopicData = matched;
                    currentPracticeMode = 'normal';
                    showView('practice');
                    switchMode('list');
                    startPractice();
                }
            }
        }
    });"""
app = app.replace(old_listeners, new_listeners)

# Fix loadSavedRules header and onclick behavior
old_loadRules = """async function loadSavedRules() {
    try {
        const res = await fetch('/api/get_search_rules');
        const rules = await res.json();
        savedSearchesList.innerHTML = '<h3 style="font-size:12px; color:var(--text-secondary); margin-bottom:8px; padding-left:16px;">常用自訂規則</h3>';
        rules.forEach(r => {
            const div = document.createElement('div');
            div.className = 'nav-item';
            div.textContent = `📌 ${r.name}`;
            div.title = `Regex: ${r.query}`;
            div.onclick = () => {
                searchInput.value = r.query;
                applyFilters();
            };
            savedSearchesList.appendChild(div);
        });"""
new_loadRules = """async function loadSavedRules() {
    try {
        const res = await fetch('/api/get_search_rules');
        const rules = await res.json();
        // Clear previous
        savedSearchesList.innerHTML = '';
        
        // Hardcoded basic rules
        const builtIns = [
            { name: '免疫球蛋白題', query: '(Ig[GAMED]|免疫球蛋白)' },
            { name: '記憶口訣題', query: '口訣' }
        ];
        
        [...builtIns, ...rules].forEach(r => {
            const div = document.createElement('div');
            div.className = 'nav-item';
            div.style.paddingLeft = '8px';
            div.textContent = `📌 ${r.name}`;
            div.title = `Regex: ${r.query}`;
            div.onclick = () => {
                document.getElementById('adv-regex').value = r.query;
                document.getElementById('adv-tag-name').value = r.name;
            };
            savedSearchesList.appendChild(div);
        });"""
app = app.replace(old_loadRules, new_loadRules)


with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(app)

print("app.js fully patched.")


# Now fix index.html
with open("public/index.html", "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace('max-width:800px;', 'max-width:900px;')

with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("index.html patched.")

