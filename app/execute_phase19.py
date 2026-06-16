import re
import os
import json

# 1. Update app.js to finally add the Delete cross for Advanced Search history
with open("public/app.js", "r", encoding="utf-8") as f:
    app = f.read()

old_load_rules = """        [...builtIns, ...rules].forEach(r => {
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

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(app)


# 2. Scrub JSON files to remove incorrectly injected custom tags
data_dir = "data"
for filename in os.listdir(data_dir):
    if filename.endswith(".json") and filename != "saved_searches.json":
        filepath = os.path.join(data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        # For each question, if "tags" exists and has more than 1 element, truncate it to 1
        for q in data:
            if "tags" in q and isinstance(q["tags"], list):
                if len(q["tags"]) > 1:
                    # Keep only the first native tag
                    q["tags"] = q["tags"][:1]
                    
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

print("Phase 19 executed.")

