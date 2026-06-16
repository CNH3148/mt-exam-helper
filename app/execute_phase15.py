import re

# 1. Update index.html
with open("public/index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Update Breadcrumb default
html = html.replace('📝 隨機練習', '📝 一般練習')

# Update Card Mode Star
html = html.replace('class="bookmark-btn"', 'class="star-icon" style="cursor:pointer;"')

# Update Card Mode Explanation Heading (Remove AI 詳解 heading)
old_explanation_panel = """                    <div class="explanation-panel" id="explanation-panel" style="display: none;">
                        <h3>💡 AI 詳解 (知識點統整)</h3>
                        <p id="q-explanation">載入中...</p>
                        <p class="answer-reveal">標準答案是：<strong id="correct-answer">A</strong></p>
                    </div>"""
new_explanation_panel = """                    <div class="explanation-panel" id="explanation-panel" style="display: none; border: 1px solid var(--glass-border); border-radius: 8px; padding: 16px; background: rgba(30, 41, 59, 0.5);">
                        <div id="q-explanation">載入中...</div>
                        <div class="answer-reveal" style="margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--glass-border);">標準答案是：<strong id="correct-answer" style="color: var(--accent);">A</strong></div>
                    </div>"""
html = html.replace(old_explanation_panel, new_explanation_panel)

# Update Advanced Modal Layout to Two Separate Boxes
old_adv_modal = """    <div id="advanced-search-modal" class="modal" style="display:none;">
        <div class="modal-content" style="max-width:900px;">
            <h3>進階 Regex 搜尋與自訂標籤</h3>
            <p style="font-size:12px; color:var(--text-secondary);">輸入 Regex 以搜尋題幹與選項，並建立您的專屬關聯規則。</p>
            
            <div class="adv-search-layout">
                <div class="adv-search-left">
                    <div>
                        <label style="display:block; margin-bottom:4px; font-size:14px; font-weight:600;">規則名稱 / 自訂標籤</label>
                        <input type="text" id="adv-tag-name" class="search-input" placeholder="例如: 補體系統口訣題" style="width:100%; box-sizing:border-box;">
                    </div>
                    <div>
                        <label style="display:block; margin-bottom:4px; font-size:14px; font-weight:600;">Regex 搜尋語法</label>
                        <input type="text" id="adv-regex" class="search-input" placeholder="例如: (Ig[GAMED]|免疫球蛋白)" style="width:100%; box-sizing:border-box; font-family:monospace;">
                    </div>
                    <div style="font-size:12px; color:var(--text-muted);">
                        提示：填寫完畢後點擊儲存，系統會自動切換為清單模式預覽符合的題目。
                    </div>
                </div>
                
                <div class="adv-search-right">
                    <h4 style="font-size:13px; margin-bottom:8px; color:var(--text-secondary);">常用自訂規則</h4>
                    <div id="saved-searches-list">
                        <!-- Saved rules injected here -->
                    </div>
                </div>
            </div>

            <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--glass-border); padding-top:12px; margin-top:8px;">
                <span id="adv-preview" style="font-size:14px; color:var(--text-secondary);">等待輸入...</span>
                <div style="display:flex; gap:8px; align-items:center;">
                    <button class="btn btn-secondary" id="btn-adv-cancel">取消</button>
                    <button class="btn btn-primary" id="btn-adv-save">儲存並標記</button>
                </div>
            </div>
        </div>
    </div>"""

new_adv_modal = """    <div id="advanced-search-modal" class="modal" style="display:none; padding: 20px;">
        <div style="display: flex; gap: 24px; max-width: 1000px; width: 100%; align-items: stretch; justify-content: center; margin: 0 auto;">
            <!-- Left Box -->
            <div class="modal-content" style="flex: 2; margin: 0; display: flex; flex-direction: column;">
                <h3>進階 Regex 搜尋與自訂標籤</h3>
                <p style="font-size:13px; color:var(--text-secondary); margin-bottom: 24px;">輸入 Regex 以搜尋題幹與選項，並建立您的專屬關聯規則。</p>
                
                <div style="display:flex; flex-direction:column; gap:16px; margin-bottom: 24px; flex: 1;">
                    <div>
                        <label style="display:block; margin-bottom:8px; font-size:15px; font-weight:600;">規則名稱 / 自訂標籤</label>
                        <input type="text" id="adv-tag-name" class="search-input" placeholder="例如: 補體系統口訣題" style="width:100%; box-sizing:border-box; padding: 12px; font-size: 15px;">
                    </div>
                    <div>
                        <label style="display:block; margin-bottom:8px; font-size:15px; font-weight:600;">Regex 搜尋語法</label>
                        <input type="text" id="adv-regex" class="search-input" placeholder="例如: (Ig[GAMED]|免疫球蛋白)" style="width:100%; box-sizing:border-box; font-family:monospace; padding: 12px; font-size: 15px;">
                    </div>
                    <div style="font-size:13px; color:var(--text-muted); margin-top: auto;">
                        提示：填寫完畢後點擊儲存，系統會自動切換為清單模式預覽符合的題目。
                    </div>
                </div>

                <div style="display:flex; justify-content:space-between; align-items:center; border-top:1px solid var(--glass-border); padding-top:16px;">
                    <span id="adv-preview" style="font-size:14px; color:var(--text-secondary);">等待輸入...</span>
                    <div style="display:flex; gap:12px; align-items:center;">
                        <button class="btn btn-secondary" id="btn-adv-cancel" style="padding: 10px 20px;">取消</button>
                        <button class="btn btn-primary" id="btn-adv-save" style="padding: 10px 20px;">儲存並標記</button>
                    </div>
                </div>
            </div>

            <!-- Right Box -->
            <div class="modal-content" style="flex: 1; margin: 0; display: flex; flex-direction: column; background: var(--bg-panel);">
                <h4 style="font-size:16px; margin-bottom:16px; color:var(--text-main); border-bottom: 1px solid var(--glass-border); padding-bottom: 12px;">常用自訂規則</h4>
                <div id="saved-searches-list" style="flex: 1; overflow-y: auto;">
                    <!-- Saved rules injected here -->
                </div>
            </div>
        </div>
    </div>"""
html = html.replace(old_adv_modal, new_adv_modal)

with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(html)


# 2. Update app.js
with open("public/app.js", "r", encoding="utf-8") as f:
    app = f.read()

# Fix List Mode star-icon class
app = app.replace('class="bookmark-btn', 'class="star-icon" style="cursor:pointer; font-size: 20px;"')

# Fix Card Mode renderCardView bookmark-btn
app = app.replace("starBtn.className = isBookmarked ? 'bookmark-btn active' : 'bookmark-btn';", "starBtn.className = isBookmarked ? 'star-icon active' : 'star-icon';\n        starBtn.textContent = isBookmarked ? '★' : '☆';")

# Fix toggleBookmark function UI animation
old_toggle = """    // Animation
    if(e && e.target) {
        e.target.classList.toggle('active');
        e.target.style.transform = 'scale(1.2)';
        setTimeout(() => e.target.style.transform = 'scale(1)', 200);
    }"""
new_toggle = """    // Animation
    if(e && e.target) {
        const isActive = e.target.classList.toggle('active');
        e.target.textContent = isActive ? '★' : '☆';
        e.target.style.transform = 'scale(1.3)';
        setTimeout(() => e.target.style.transform = 'scale(1)', 200);
    }"""
app = app.replace(old_toggle, new_toggle)


# Breadcrumb Practice update
old_startPractice = """function startPractice() {
    if (currentActiveTopicData.length === 0) return;
    
    bcPractice.style.display = 'inline';
    bcSepPractice.style.display = 'inline';
    viewToggleContainer.style.display = 'flex';
    listAccuracy.style.display = 'block';"""

new_startPractice = """function startPractice() {
    if (currentActiveTopicData.length === 0) return;
    
    bcPractice.style.display = 'inline';
    bcSepPractice.style.display = 'inline';
    viewToggleContainer.style.display = 'flex';
    listAccuracy.style.display = 'block';
    
    if (currentPracticeMode === 'wrong') bcPractice.innerHTML = '📝 錯題練習';
    else if (currentPracticeMode === 'bookmark') bcPractice.innerHTML = '📝 收藏練習';
    else bcPractice.innerHTML = '📝 一般練習';"""
app = app.replace(old_startPractice, new_startPractice)


# Make Card Mode qExplanation exactly match List mode markdown structure
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
            
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
                <strong>📝 您的筆記 (支援 Markdown)：</strong>
                <button class="btn btn-secondary btn-small" onclick="toggleEditUserExp('${q.exam_id}', '${q.no}')">✏️ 編輯筆記</button>
            </div>
            <div id="user-exp-view-${q.exam_id}-${q.no}" class="markdown-body" style="padding:12px; background:var(--bg-lighter); border:1px solid var(--glass-border); border-radius:6px; min-height:40px;">
                ${userExp.trim() ? marked.parse(userExp) : '<span style="color:var(--text-muted);">點擊編輯撰寫 Markdown 筆記...</span>'}
            </div>
            <div id="user-exp-edit-container-${q.exam_id}-${q.no}" style="display:none;">
                <textarea id="user-exp-${q.exam_id}-${q.no}" style="width:100%; height:150px; background:var(--bg-lighter); color:var(--text-main); border:1px solid var(--glass-border); padding:8px; border-radius:6px; resize:vertical;">${userExp}</textarea>
                <div style="text-align:right; margin-top:8px;">
                    <button class="btn btn-primary btn-small" onclick="saveAndRenderUserExp('${q.exam_id}', '${q.no}')">儲存並預覽</button>
                </div>
            </div>
        `;"""

new_card_exp = """        qExplanation.innerHTML = `
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
            
            <div id="md-preview-card-${q.exam_id}-${q.no}" class="markdown-body" style="background:var(--bg-lighter); padding:12px; border-radius:6px; min-height:60px;">${marked.parse(userExp || '*尚無筆記*')}</div>
            <div id="md-editor-card-${q.exam_id}-${q.no}" style="display:none; margin-top:8px;">
                <textarea id="user-exp-card-${q.exam_id}-${q.no}" style="width:100%; height:150px; background:var(--bg-lighter); color:var(--text-main); border:1px solid var(--glass-border); padding:8px; border-radius:6px; resize:vertical;">${userExp}</textarea>
                <div style="text-align:right; margin-top:8px;">
                    <button class="btn btn-primary btn-small" onclick="saveUserExplanation('${q.exam_id}', '${q.no}', document.getElementById('user-exp-card-${q.exam_id}-${q.no}').value); toggleMarkdownEdit('card-${q.exam_id}-${q.no}'); document.getElementById('md-preview-card-${q.exam_id}-${q.no}').innerHTML = marked.parse(document.getElementById('user-exp-card-${q.exam_id}-${q.no}').value || '*尚無筆記*');">儲存筆記</button>
                </div>
            </div>
            <div style="text-align:right; margin-top:8px;">
                <button class="btn btn-secondary btn-small" onclick="toggleMarkdownEdit('card-${q.exam_id}-${q.no}')">✏️ 編輯筆記</button>
            </div>
        `;"""
app = app.replace(old_card_exp, new_card_exp)

with open("public/app.js", "w", encoding="utf-8") as f:
    f.write(app)

print("Phase 15 executed.")

