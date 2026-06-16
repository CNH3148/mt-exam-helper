import re

with open("public/index.html", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Remove from sidebar
content = re.sub(r'<div id="saved-searches-list"[\s\S]*?</div>\n', '', content)
content = re.sub(r'<button class="btn btn-primary" style="margin-top:20px; width:100%;" onclick="startWrongPractice.*?隨機錯題練習</button>', '', content)

# 2. Rewrite Advanced Search Modal
new_modal = """    <!-- Advanced Search Modal -->
    <div id="advanced-search-modal" class="modal" style="display:none;">
        <div class="modal-content" style="max-width:800px;">
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
    </div>
"""

content = re.sub(r'<!-- Advanced Search Modal -->[\s\S]*?(?=<!-- Image Upload Modal -->)', new_modal, content)

with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(content)
print("index.html patched.")

