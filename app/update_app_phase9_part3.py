import re

with open("public/app.js", "r", encoding="utf-8") as f:
    content = f.read()

# Update renderCardView UI Elements
card_ui_old2 = """<div class="tags-container" style="margin-top:16px;">${tagsHtml}</div>
                <div style="margin-top:20px; text-align:right;">
                    <button class="btn btn-secondary btn-small" onclick="document.getElementById('card-explanation').style.display='block'">查看解析</button>
                </div>"""
card_ui_new2 = """<div class="tags-container" style="margin-top:16px;">
                    ${tagsHtml}
                    <!-- Custom Tags rendering with hover X -->
                    ${(() => {
                        let html = '';
                        for (let t in globalCustomTags) {
                            if (globalCustomTags[t].includes(q.exam_id + '_' + q.no)) {
                                html += `<span class="badge" style="background:#8b5cf6; color:white; position:relative; cursor:pointer;" title="自訂標籤" onmouseover="this.querySelector('.del-tag').style.display='inline'" onmouseout="this.querySelector('.del-tag').style.display='none'">
                                    🏷️ ${t}
                                    <span class="del-tag" style="display:none; margin-left:4px; font-weight:bold; color:#ffb3b3;" onclick="removeCustomTagFromQ('${t}', '${q.exam_id}', '${q.no}')">✕</span>
                                </span>`;
                            }
                        }
                        return html;
                    })()}
                </div>
                <div style="margin-top:20px; display:flex; justify-content:space-between; align-items:center;">
                    <button class="btn btn-secondary btn-small" onclick="openImageUploadModal('${q.exam_id}', '${q.no}')">🔄 修改附圖</button>
                    <button class="btn btn-secondary btn-small" onclick="document.getElementById('card-explanation').style.display='block'">查看解析</button>
                </div>"""
content = content.replace(card_ui_old2, card_ui_new2)

# Bookmark star in card view
card_header_old = `<span class="badge" style="margin:0;">Q ${currentIndex + 1} / ${currentActiveTopicData.length}</span>`
card_header_new = `<span class="badge" style="margin:0;">Q ${currentIndex + 1} / ${currentActiveTopicData.length}</span>
                    <span style="cursor:pointer; font-size:18px; color:#facc15;" onclick="toggleBookmark('${q.exam_id}', '${q.no}')">
                        ${globalBookmarks.includes(q.exam_id + '_' + q.no) ? '★' : '☆'}
                    </span>`
content = content.replace(card_header_old, card_header_new)

# Explanation Area in Card view
card_exp_old = """if (q.explanation && q.topic) {
            qExplanation.innerHTML = `
                <div style="margin-bottom: 8px;"><strong>🏷️ 知識點：</strong><span class="badge" style="background:var(--primary); color:white;">${q.topic}</span></div>
                <div style="line-height: 1.6;">${q.explanation.replace(/\\n/g, '<br>')}</div>
            `;
        } else {
            qExplanation.innerHTML = `<p style="color:var(--text-muted);">本題尚無詳細解析，您可以嘗試自行分析各選項知識點。</p>`;
        }"""
card_exp_new = """const userExp = globalExplanations[q.exam_id + '_' + q.no] || q.explanation || '';
        qExplanation.innerHTML = `
            <div style="margin-bottom: 8px;"><strong>🏷️ 知識點：</strong><span class="badge" style="background:var(--primary); color:white;">${q.topic || '無'}</span></div>
            <textarea id="user-exp-${q.exam_id}-${q.no}" style="width:100%; height:100px; background:var(--bg-lighter); color:var(--text-main); border:1px solid var(--glass-border); padding:8px; border-radius:6px; resize:vertical;">${userExp}</textarea>
            <div style="text-align:right; margin-top:8px;">
                <button class="btn btn-primary btn-small" onclick="saveUserExplanation('${q.exam_id}', '${q.no}', document.getElementById('user-exp-${q.exam_id}-${q.no}').value)">儲存筆記</button>
            </div>
        `;"""
content = content.replace(card_exp_old, card_exp_new)

# Update renderListView UI Elements
list_header_old = `<span class="badge" style="margin:0;">Q ${idx + 1} / ${currentActiveTopicData.length}</span>`
list_header_new = `<span class="badge" style="margin:0;">Q ${idx + 1} / ${currentActiveTopicData.length}</span>
                    <span style="cursor:pointer; font-size:16px; color:#facc15; margin-left:8px;" onclick="toggleBookmark('${q.exam_id}', '${q.no}')">
                        ${globalBookmarks.includes(q.exam_id + '_' + q.no) ? '★' : '☆'}
                    </span>`
content = content.replace(list_header_old, list_header_new)

# List tags
list_tags_old = `<div class="tags-container">${tagsHtml}</div>`
list_tags_new = `<div class="tags-container">
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
                </div>`
content = content.replace(list_tags_old, list_tags_new)

# List Explanation & Replace Image
list_exp_old = """                    </div>
                    
                    <div class="list-explanation" id="list-exp-${idx}">
                        <div style="font-weight:bold; margin-bottom:8px; color:var(--accent);">正確解答：${q.answer}</div>
                        <div>${q.explanation ? q.explanation.replace(/\\n/g, '<br>') : '<span style="color:var(--text-muted);">尚無詳細解析</span>'}</div>
                    </div>
                </div>
            </div>`;"""
list_exp_new = """                    </div>
                    
                    <div class="list-explanation" id="list-exp-${idx}">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                            <div style="font-weight:bold; color:var(--accent);">正確解答：${q.answer}</div>
                            <button class="btn btn-secondary btn-small" onclick="openImageUploadModal('${q.exam_id}', '${q.no}')">🔄 修改附圖</button>
                        </div>
                        <textarea id="user-exp-list-${q.exam_id}-${q.no}" style="width:100%; height:80px; background:var(--bg-lighter); color:var(--text-main); border:1px solid var(--glass-border); padding:8px; border-radius:6px; resize:vertical;">${globalExplanations[q.exam_id + '_' + q.no] || q.explanation || ''}</textarea>
                        <div style="text-align:right; margin-top:8px;">
                            <button class="btn btn-primary btn-small" onclick="saveUserExplanation('${q.exam_id}', '${q.no}', document.getElementById('user-exp-list-${q.exam_id}-${q.no}').value)">儲存筆記</button>
                        </div>
                    </div>
                </div>
            </div>`;"""
content = content.replace(list_exp_old, list_exp_new)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated app.js part 3 successfully.")

