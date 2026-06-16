import re

with open("public/app.js", "r", encoding="utf-8") as f:
    app = f.read()

# Fix ReferenceError for tagsHtml and add Image Modify button in renderCardView
old_card_exp = """        qExplanation.innerHTML = `
            <div style="margin-bottom: 12px; display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
                <strong>🏷️ 標籤：</strong>
                ${tagsHtml}
                ${(() => {
                    let html = '';
                    for (let t in globalCustomTags) {
                        if (globalCustomTags[t].includes(q.exam_id + '_' + q.no)) {
                            html += `<span class="badge" style="background:#8b5cf6; color:white; position:relative; cursor:pointer;" onmouseover="this.querySelector('.del-tag').style.display='inline'" onmouseout="this.querySelector('.del-tag').style.display='none'">
                                🏷️ ${t}
                                <span class="del-tag" style="display:none; margin-left:4px; font-weight:bold; color:#ffb3b3;" onclick="removeCustomTagFromQ('${t}', '${q.exam_id}', '${q.no}')">✕</span>
                            </span>`;
                        }
                    }
                    return html;
                })()}
                <input type="text" class="manual-tag-input" placeholder="新增標籤..." onkeypress="if(event.key==='Enter') { window.addManualCustomTag('${q.exam_id}', '${q.no}', this.value); this.value=''; }">
            </div>
            
            <div id="md-preview-card-${q.exam_id}-${q.no}" class="markdown-body" style="background:var(--bg-lighter); padding:12px; border-radius:6px; min-height:60px;">${marked.parse(userExp || '*尚無筆記*')}</div>"""

new_card_exp = """        let tagsHtml = q.tags ? q.tags.map(t => `<span class="tag" style="background:transparent; border:1px solid #ddd; color:#888;">${t}</span>`).join('') : '';
        if (q.topic) tagsHtml += `<span class="tag" style="background:rgba(59,130,246,0.1); color:#3b82f6; border-color:rgba(59,130,246,0.3);">🏷️ ${q.topic}</span>`;

        qExplanation.innerHTML = `
            <div style="margin-bottom: 12px; display:flex; flex-wrap:wrap; gap:8px; align-items:center;">
                <strong>🏷️ 標籤：</strong>
                ${tagsHtml}
                ${(() => {
                    let html = '';
                    for (let t in globalCustomTags) {
                        if (globalCustomTags[t].includes(q.exam_id + '_' + q.no)) {
                            html += `<span class="badge" style="background:#8b5cf6; color:white; position:relative; cursor:pointer;" onmouseover="this.querySelector('.del-tag').style.display='inline'" onmouseout="this.querySelector('.del-tag').style.display='none'">
                                🏷️ ${t}
                                <span class="del-tag" style="display:none; margin-left:4px; font-weight:bold; color:#ffb3b3;" onclick="removeCustomTagFromQ('${t}', '${q.exam_id}', '${q.no}')">✕</span>
                            </span>`;
                        }
                    }
                    return html;
                })()}
                <input type="text" class="manual-tag-input" placeholder="新增標籤..." onkeypress="if(event.key==='Enter') { window.addManualCustomTag('${q.exam_id}', '${q.no}', this.value); this.value=''; }">
            </div>
            
            <div style="display:flex; justify-content:flex-end; align-items:center; margin-bottom:8px;">
                <button class="btn btn-secondary btn-small" onclick="openImageUploadModal('${q.exam_id}', '${q.no}')">🔄 修改附圖</button>
            </div>
            
            <div id="md-preview-card-${q.exam_id}-${q.no}" class="markdown-body" style="background:var(--bg-lighter); padding:12px; border-radius:6px; min-height:60px;">${marked.parse(userExp || '*尚無筆記*')}</div>"""
            
app = app.replace(old_card_exp, new_card_exp)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(app)

print("Phase 16 executed.")

