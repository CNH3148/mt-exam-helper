import os
import re

# 1. Update index.html
html_path = 'public/index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace the <header class="main-header" ...> ... </header> block
# We'll use a regex to replace everything from <header class="main-header" to </header>
header_pattern = re.compile(r'<header class="main-header".*?</header>', re.DOTALL)

new_header = """<header class="main-header" style="display: flex; justify-content: space-between; align-items: center; min-height: 40px; margin-bottom: 12px;">
                <div style="display:flex; align-items:center; gap:12px; flex-wrap:wrap;">
                    <!-- Breadcrumbs & Toggles in one line -->
                    <button class="btn btn-secondary btn-small" id="btn-sidebar-toggle" style="padding:4px 8px;">☰</button>
                    <div id="breadcrumb" style="font-size:14px; color:var(--text-secondary); display:flex; gap:8px; align-items:center;">
                        <span id="bc-subject" style="cursor:pointer; color:var(--primary); font-weight:500;">🏠 選擇科目</span>
                        <span id="bc-sep-topic" style="display:none;">›</span>
                        <span id="bc-topic" style="cursor:pointer; color:var(--primary); font-weight:500; display:none;">🏷️ 類群名稱</span>
                        <span id="bc-sep-practice" style="display:none;">›</span>
                        <span id="bc-practice" style="color:var(--accent); font-weight:500; display:none;">📝 一般練習</span>
                    </div>
                    <span style="font-size:14px; color:var(--text-secondary); display:none; margin-left:8px;" id="list-accuracy">正確率: --%</span>
                    <h1 id="current-subject-title" style="display:none;"></h1>
                </div>
                <!-- Practice Action Buttons & Mode Toggle -->
                <div style="display:flex; gap:16px; align-items:center;">
                    <div style="display:flex; gap:8px; align-items:center;" id="header-practice-actions">
                        <button class="btn btn-secondary" onclick="startWrongPractice()" id="btn-wrong-practice" style="display:none; padding:4px 12px; font-size:14px;">🔄 隨機錯題</button>
                        <button class="btn btn-secondary" onclick="startBookmarkPractice()" id="btn-bookmark-practice" style="display:none; padding:4px 12px; font-size:14px;">⭐ 收藏練習</button>
                    </div>
                    <div class="view-toggle" id="view-toggle-container" style="display:none; align-items:center; gap:8px;">
                        <span style="font-size:14px; color:var(--text-main); cursor:pointer;" id="label-mode-card">卡片</span>
                        <label class="switch">
                            <input type="checkbox" id="mode-toggle-checkbox">
                            <span class="slider round"></span>
                        </label>
                        <span style="font-size:14px; color:var(--text-secondary); cursor:pointer;" id="label-mode-list">清單</span>
                    </div>
                </div>
            </header>"""

html = header_pattern.sub(new_header, html)
with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

# 2. Update style.css
css_path = 'public/style.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

switch_css = """
/* Toggle Switch */
.switch {
  position: relative;
  display: inline-block;
  width: 44px;
  height: 24px;
}
.switch input { 
  opacity: 0;
  width: 0;
  height: 0;
}
.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: var(--glass-border);
  transition: .3s;
}
.slider:before {
  position: absolute;
  content: "";
  height: 18px;
  width: 18px;
  left: 3px;
  bottom: 3px;
  background-color: white;
  transition: .3s;
}
input:checked + .slider {
  background-color: var(--primary);
}
input:checked + .slider:before {
  transform: translateX(20px);
}
.slider.round {
  border-radius: 24px;
}
.slider.round:before {
  border-radius: 50%;
}
"""

if ".switch {" not in css:
    css += switch_css
    with open(css_path, 'w', encoding='utf-8') as f:
        f.write(css)


# 3. Update app.js
js_path = 'public/app.js'
with open(js_path, 'r', encoding='utf-8') as f:
    js = f.read()

# Replace button listeners with checkbox listeners
# btnModeCard.onclick = ... btnModeList.onclick = ...
# Instead of tracking down the old references (btnModeCard), we'll just append our logic to DOMContentLoaded or window.switchMode

js_replacement_logic = """
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
"""

# Let's inject into switchMode
switchMode_pattern = re.compile(r'function switchMode\(mode\)\s*\{.*?(?=})', re.DOTALL)
def switchMode_replacer(match):
    old_body = match.group(0)
    # remove old active toggling
    old_body = re.sub(r'btnModeCard\.classList\.(remove|add)\(\'active\'\);', '', old_body)
    old_body = re.sub(r'btnModeList\.classList\.(remove|add)\(\'active\'\);', '', old_body)
    # inject the new logic
    return old_body + js_replacement_logic

js = switchMode_pattern.sub(switchMode_replacer, js)

# Now we need to attach the event listener. 
# We'll just put it at the very bottom of the file
event_listener_injection = """
// New Toggle Switch Logic
const _modeCheckbox = document.getElementById('mode-toggle-checkbox');
const _lblCard = document.getElementById('label-mode-card');
const _lblList = document.getElementById('label-mode-list');

if (_modeCheckbox) {
    _modeCheckbox.addEventListener('change', (e) => {
        if (e.target.checked) switchMode('list');
        else switchMode('card');
    });
    _lblCard.addEventListener('click', () => {
        _modeCheckbox.checked = false;
        switchMode('card');
    });
    _lblList.addEventListener('click', () => {
        _modeCheckbox.checked = true;
        switchMode('list');
    });
}
"""

if "// New Toggle Switch Logic" not in js:
    js += "\n" + event_listener_injection

with open(js_path, 'w', encoding='utf-8') as f:
    f.write(js)

print("Done updating header!")

