import re

with open("public/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# We need to replace the list view card template.
# Let's locate the start and end of it.
pattern = re.compile(r"card\.innerHTML = `\n              <div class=\"list-card-left\"></div>.*?<div class=\"list-card-right-text\">查看詳細解析</div>\n              </div>\n          `;", re.DOTALL)

new_card = """card.innerHTML = `
            <div class="list-card-left"></div>
            <div class="list-card-main">
                <div class="list-card-header">
                    <span class="badge" style="margin:0;">Q ${idx + 1} / ${currentActiveTopicData.length}</span>
                    <span style="cursor:pointer; font-size:18px; color:#facc15; margin-left:8px;" onclick="toggleBookmark('${q.exam_id}', '${q.no}')">
                        ${globalBookmarks.includes(q.exam_id + '_' + q.no) ? '★' : '☆'}
                    </span>
                </div>
                <div class="list-card-body">
                    ${q.question}
                    ${imgHtml}
                </div>
                ${optionsHtml}
                
                <div class="list-explanation" id="list-exp-${idx}" style="display:none; margin-top:12px; padding:12px; border:1px solid var(--glass-border); border-radius:8px;">
                    <div class="tags-container" style="margin-bottom:12px;">
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
                        <span class="badge" style="background:var(--primary); color:white; display:flex; align-items:center; gap:4px;">
                            ➕ <input type="text" class="manual-tag-input" placeholder="新增標籤" onkeypress="if(event.key==='Enter') addManualCustomTag('${q.exam_id}', '${q.no}', this.value)">
                        </span>
                    </div>
                    
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                        <div style="font-weight:bold; color:var(--accent);">正確解答：${q.answer}</div>
                        <button class="btn btn-secondary btn-small" onclick="openImageUploadModal('${q.exam_id}', '${q.no}')">🔄 修改附圖</button>
                    </div>
                    <div id="md-preview-list-${q.exam_id}-${q.no}" class="markdown-body" style="background:var(--bg-lighter); padding:12px; border-radius:6px; min-height:60px;">${marked.parse(globalExplanations[q.exam_id + '_' + q.no] || q.explanation || '*尚無筆記*')}</div>
                    <div id="md-editor-list-${q.exam_id}-${q.no}" style="display:none; margin-top:8px;">
                        <textarea id="user-exp-list-${q.exam_id}-${q.no}" style="width:100%; height:80px; background:var(--bg-lighter); color:var(--text-main); border:1px solid var(--glass-border); padding:8px; border-radius:6px; resize:vertical;">${globalExplanations[q.exam_id + '_' + q.no] || q.explanation || ''}</textarea>
                        <div style="text-align:right; margin-top:8px;">
                            <button class="btn btn-primary btn-small" onclick="saveUserExplanation('${q.exam_id}', '${q.no}', document.getElementById('user-exp-list-${q.exam_id}-${q.no}').value); toggleMarkdownEdit('list-${q.exam_id}-${q.no}'); document.getElementById('md-preview-list-${q.exam_id}-${q.no}').innerHTML = marked.parse(document.getElementById('user-exp-list-${q.exam_id}-${q.no}').value || '*尚無筆記*');">儲存筆記</button>
                        </div>
                    </div>
                    <div style="text-align:right; margin-top:8px;">
                        <button class="btn btn-secondary btn-small" onclick="toggleMarkdownEdit('list-${q.exam_id}-${q.no}')">✏️ 編輯筆記</button>
                    </div>
                </div>
                
                <div class="list-card-footer">
                    <div class="${answerAreaClass}" id="list-answer-area-${idx}">
                        答案：<span class="blurred-answer">${q.answer}</span>
                    </div>
                </div>
            </div>
            <div class="list-card-right" onclick="toggleListExp(${idx})">
                <div class="list-card-right-text">查看詳細解析</div>
            </div>
        `;"""

new_content, count = pattern.subn(new_card, content)
if count > 0:
    print(f"Successfully replaced list view card template {count} times.")
    with open("public/app.js", "w", encoding="utf-8") as f:
        f.write(new_content)
else:
    print("Could not match the regex for list card!")

