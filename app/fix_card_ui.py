import re
import time

css_path = r"C:\Users\star0\Desktop\刷題系統\app\public\style.css"
js_path = r"C:\Users\star0\Desktop\刷題系統\app\public\app.js"
index_path = r"C:\Users\star0\Desktop\刷題系統\app\public\index.html"

# 1. Clean up style.css
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# We will cut off everything starting from "/* --- 全局背景與字體設定 --- */" 
# or "/* --- 卡片容器設計 --- */" or ".card {" where the old subagent code begins.
cut_marker = "/* --- 全局背景與字體設定 --- */"
if cut_marker in css:
    css = css.split(cut_marker)[0]

new_css = """
/* --- 互動式卡片牆 --- */
.code-block-wrapper {
    position: relative;
    margin-top: 16px;
    margin-bottom: 24px;
}
.code-block-wrapper pre {
    background: #1e1e1e !important;
    padding: 16px;
    padding-top: 40px; 
    border-radius: 8px;
    overflow-x: auto;
    color: #d4d4d4 !important;
    font-family: 'Consolas', monospace;
    font-size: 14px;
    border: 1px solid var(--glass-border);
    margin: 0;
}
.copy-obsidian-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #94a3b8;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 4px;
}
.copy-obsidian-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    color: #fff;
}

.anki-card-wrapper {
    margin-top: 16px;
    padding: 20px;
    background: var(--bg-panel);
    border-radius: 12px;
    border: 1px solid var(--glass-border);
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    width: 100%;
}
@media (max-width: 1024px) {
    .anki-card-wrapper { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
    .anki-card-wrapper { grid-template-columns: 1fr; }
}

.anki-card {
    background: #1e1e1e;
    color: #e0e0e0;
    border-radius: 10px;
    padding: 20px;
    cursor: pointer;
    border: 1px solid #333;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    min-height: 120px;
    transition: all 0.2s ease;
    box-shadow: 0 4px 6px rgba(0,0,0,0.3);
}
.anki-card:hover {
    border-color: #555;
    background: #2a2a2a;
    transform: translateY(-2px);
}
.anki-card .card-front {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;
}
.anki-card .question {
    font-size: 15px;
    font-weight: 500;
    color: #f8fafc;
    line-height: 1.5;
}
.anki-card .card-back {
    display: none;
    width: 100%;
}
.anki-card .question-small {
    font-size: 13px;
    color: #94a3b8;
    margin-bottom: 12px;
    line-height: 1.4;
}
.anki-card .card-divider {
    width: 100%;
    border: none;
    border-top: 1px dashed #444;
    margin-bottom: 12px;
}
.anki-card .answer {
    font-size: 15px;
    color: #facc15;
    font-weight: 600;
    line-height: 1.5;
}

/* Flipped State */
.anki-card.flipped .card-front {
    display: none;
}
.anki-card.flipped .card-back {
    display: block;
}

/* Highlighted Answer text support for <ans> */
.anki-card ans, .anki-card .answer ans {
    color: #ef4444;
    background-color: rgba(239, 68, 68, 0.15);
    padding: 2px 6px;
    border-radius: 4px;
}
"""
css += new_css

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

# 2. Update app.js card innerHTML
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

old_html = """                        cardDiv.innerHTML = `
                            <div class="front-container"><div class="question">${front}</div></div>
                            <hr id="answer" style="display:none;">
                            <div class="back-container"><div class="answer">${back}</div></div>
                        `;"""

new_html = """                        cardDiv.innerHTML = `
                            <div class="card-front">
                                <div class="question">${front}</div>
                            </div>
                            <div class="card-back">
                                <div class="question-small">${front}</div>
                                <hr class="card-divider">
                                <div class="answer">${back}</div>
                            </div>
                        `;"""

js = js.replace(old_html, new_html)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

# 3. Bump cache
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()
html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)
html = re.sub(r'style\.css\?v=\d+', f'style.css?v={int(time.time())}', html)
with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

