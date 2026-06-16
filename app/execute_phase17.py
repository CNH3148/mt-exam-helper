import re

# 1. Update server.py
with open("server.py", "r", encoding="utf-8") as f:
    server = f.read()

new_endpoint = """@app.get("/api/get_search_rules")
def get_search_rules():
    rules_path = os.path.join("data", "saved_searches.json")
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.delete("/api/delete_search_rule/{rule_name}")
def delete_search_rule(rule_name: str):
    rules_path = os.path.join("data", "saved_searches.json")
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            rules = json.load(f)
        rules = [r for r in rules if r['name'] != rule_name]
        with open(rules_path, "w", encoding="utf-8") as f:
            json.dump(rules, f, ensure_ascii=False, indent=2)
    return {"status": "success"}"""

server = server.replace("""@app.get("/api/get_search_rules")
def get_search_rules():
    rules_path = os.path.join("data", "saved_searches.json")
    if os.path.exists(rules_path):
        with open(rules_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []""", new_endpoint)

with open("server.py", "w", encoding="utf-8") as f:
    f.write(server)


# 2. Update index.html
with open("public/index.html", "r", encoding="utf-8") as f:
    html = f.read()

old_buttons = """                    <div style="display:flex; gap:12px; align-items:center;">
                        <button class="btn btn-secondary" id="btn-adv-cancel" style="padding: 10px 20px;">取消</button>
                        <button class="btn btn-primary" id="btn-adv-save" style="padding: 10px 20px;">儲存並標記</button>
                    </div>"""
new_buttons = """                    <div style="display:flex; gap:12px; align-items:center;">
                        <button class="btn btn-secondary" id="btn-adv-cancel" style="padding: 10px 20px;">取消</button>
                        <button class="btn btn-secondary" id="btn-adv-search-only" style="padding: 10px 20px; background:var(--bg-lighter);">純搜尋</button>
                        <button class="btn btn-primary" id="btn-adv-save" style="padding: 10px 20px;">儲存並標記</button>
                    </div>"""
html = html.replace(old_buttons, new_buttons)

with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)


# 3. Update app.js
with open("public/app.js", "r", encoding="utf-8") as f:
    app = f.read()

# Fix searchInput switchView
old_search_input = """                    if (matched.length > 0) {
                        currentActiveTopicData = matched;
                        currentPracticeMode = 'normal';
                        showView('practice');
                        switchMode('list');
                        startPractice();
                    }"""
new_search_input = """                    if (matched.length > 0) {
                        currentActiveTopicData = matched;
                        currentPracticeMode = 'normal';
                        switchView('practice');
                        switchMode('list');
                        startPractice();
                    }"""
app = app.replace(old_search_input, new_search_input)

# Update loadSavedRules to support deletion
old_load_rules = """        [...builtIns, ...rules].forEach(r => {
            const div = document.createElement('div');
            div.className = 'nav-item';
            div.style.paddingLeft = '8px';
            div.textContent = `📌 ${r.name}`;
            div.title = `Regex: ${r.query}`;
            div.onclick = () => {
                document.getElementById('adv-regex').value = r.query;
                document.getElementById('adv-tag-name').value = r.name;
                updateAdvPreview();
            };
            savedSearchesList.appendChild(div);
        });"""

new_load_rules = """        window.deleteSearchRule = async function(e, ruleName) {
            e.stopPropagation();
            if (!confirm(`確定要刪除規則「${ruleName}」嗎？`)) return;
            try {
                await fetch('/api/delete_search_rule/' + encodeURIComponent(ruleName), { method: 'DELETE' });
                loadSavedRules();
            } catch(err) { alert('刪除失敗'); }
        };

        [...builtIns, ...rules].forEach(r => {
            const isBuiltIn = builtIns.some(b => b.name === r.name);
            const div = document.createElement('div');
            div.className = 'nav-item';
            div.style.paddingLeft = '8px';
            div.style.display = 'flex';
            div.style.justifyContent = 'space-between';
            div.style.alignItems = 'center';
            div.title = `Regex: ${r.query}`;
            
            div.innerHTML = `
                <span style="flex:1;">📌 ${r.name}</span>
                ${!isBuiltIn ? `<span class="del-tag" style="display:none; color:#ffb3b3; font-weight:bold; cursor:pointer; padding:0 8px;">✕</span>` : ''}
            `;
            
            div.onclick = () => {
                document.getElementById('adv-regex').value = r.query;
                document.getElementById('adv-tag-name').value = r.name;
                updateAdvPreview();
            };
            
            if (!isBuiltIn) {
                div.onmouseover = () => { const d = div.querySelector('.del-tag'); if(d) d.style.display='inline'; };
                div.onmouseout = () => { const d = div.querySelector('.del-tag'); if(d) d.style.display='none'; };
                const delBtn = div.querySelector('.del-tag');
                if (delBtn) delBtn.onclick = (e) => deleteSearchRule(e, r.name);
            }
            
            savedSearchesList.appendChild(div);
        });"""
app = app.replace(old_load_rules, new_load_rules)

# Update saveAdvancedSearch to call renderCustomTagsSidebar
old_saveAdv = """            // Switch to list view with matched questions
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

new_saveAdv = """            // Update custom tags sidebar before switching
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
            
        } catch(e) { alert('儲存失敗'); }"""
app = app.replace(old_saveAdv, new_saveAdv)


# Bind the new btnAdvSearchOnly button
# Find where btnAdvSave is bound and add our new button next to it.
old_bind = """    btnAdvSave.onclick = saveAdvancedSearch;"""
new_bind = """    btnAdvSave.onclick = saveAdvancedSearch;
    const btnAdvSearchOnly = document.getElementById('btn-adv-search-only');
    if (btnAdvSearchOnly) {
        btnAdvSearchOnly.onclick = () => {
            const rxStr = advRegex.value.trim();
            if (!rxStr || !filterSubject.value) return alert('請填寫搜尋語法與科目');
            let rx;
            try { rx = new RegExp(rxStr, 'i'); } catch(e) { return alert('Regex 語法錯誤'); }
            
            const matchedQs = [];
            currentData.forEach(q => {
                const text = q.question + " " + q.choices.join(" ");
                if (rx.test(text)) matchedQs.push(q);
            });
            
            if (matchedQs.length > 0) {
                currentActiveTopicData = matchedQs;
                currentPracticeMode = 'normal';
                advModal.style.display = 'none';
                switchView('practice');
                switchMode('list');
                startPractice();
            } else { alert('沒有符合條件的題目'); }
        };
    }"""
app = app.replace(old_bind, new_bind)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(app)

print("Phase 17 executed.")

