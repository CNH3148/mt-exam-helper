import re

# 1. Fix switchMode and loadSavedRules in app.js
with open("public/app.js", "r", encoding="utf-8") as f:
    app = f.read()

# Fix switchMode
old_switch_mode = """    if (mode === 'card') {
        switchView('practice');
        renderCardView();
        setTimeout(() => {
            if(qOptions.firstElementChild) qOptions.firstElementChild.focus();
        }, 50);
    } else {
        switchView('topic-detail');
        renderListView();
    }"""
new_switch_mode = """    if (mode === 'card') {
        switchView('practice');
        renderCardView();
        setTimeout(() => {
            if(qOptions.firstElementChild) qOptions.firstElementChild.focus();
        }, 50);
    } else {
        switchView('list');
        renderListView();
    }"""
app = app.replace(old_switch_mode, new_switch_mode)


# Fix loadSavedRules to remove builtIns
old_load_rules = """        // Hardcoded basic rules
        const builtIns = [
            { name: '免疫球蛋白題', query: '(Ig[GAMED]|免疫球蛋白)' },
            { name: '記憶口訣題', query: '口訣' }
        ];

        window.deleteSearchRule = async function(e, ruleName) {
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

new_load_rules = """        window.deleteSearchRule = async function(e, ruleName) {
            e.stopPropagation();
            if (!confirm(`確定要刪除規則「${ruleName}」嗎？`)) return;
            try {
                await fetch('/api/delete_search_rule/' + encodeURIComponent(ruleName), { method: 'DELETE' });
                loadSavedRules();
            } catch(err) { alert('刪除失敗'); }
        };

        rules.forEach(r => {
            const div = document.createElement('div');
            div.className = 'nav-item';
            div.style.paddingLeft = '8px';
            div.style.display = 'flex';
            div.style.justifyContent = 'space-between';
            div.style.alignItems = 'center';
            div.title = `Regex: ${r.query}`;
            
            div.innerHTML = `
                <span style="flex:1;">📌 ${r.name}</span>
                <span class="del-tag" style="display:none; color:#ffb3b3; font-weight:bold; cursor:pointer; padding:0 8px;">✕</span>
            `;
            
            div.onclick = () => {
                document.getElementById('adv-regex').value = r.query;
                document.getElementById('adv-tag-name').value = r.name;
                updateAdvPreview();
            };
            
            div.onmouseover = () => { const d = div.querySelector('.del-tag'); if(d) d.style.display='inline'; };
            div.onmouseout = () => { const d = div.querySelector('.del-tag'); if(d) d.style.display='none'; };
            const delBtn = div.querySelector('.del-tag');
            if (delBtn) delBtn.onclick = (e) => deleteSearchRule(e, r.name);
            
            savedSearchesList.appendChild(div);
        });"""
app = app.replace(old_load_rules, new_load_rules)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(app)

# 2. Update index.html to add Regex examples
with open("public/index.html", "r", encoding="utf-8") as f:
    html = f.read()

old_hint = """<div style="font-size: 13px; color: var(--text-muted); margin-bottom: 24px;">
                                提示：填寫完畢後點擊儲存，系統會自動切換為清單模式預覽符合的題目。
                            </div>"""
new_hint = """<div style="font-size: 13px; color: var(--text-muted); margin-bottom: 24px; line-height: 1.6;">
                                提示：填寫完畢後點擊純搜尋，系統會自動切換為清單模式預覽符合的題目。<br><br>
                                <strong style="color:var(--text-main);">Regex 常用範例：</strong><br>
                                • <code style="background:var(--bg-lighter); padding:2px 4px; border-radius:4px;">Ig[GAMED]</code>：精準搜尋 IgG, IgA, IgM, IgE, IgD。<br>
                                • <code style="background:var(--bg-lighter); padding:2px 4px; border-radius:4px;">口訣|記憶</code>：搜尋包含「口訣」或「記憶」的題目。<br>
                                • <code style="background:var(--bg-lighter); padding:2px 4px; border-radius:4px;">(?=.*小體)(?=.*內含物)</code>：同時包含「小體」與「內含物」的題目。
                            </div>"""
html = html.replace(old_hint, new_hint)

with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Phase 20 executed.")

