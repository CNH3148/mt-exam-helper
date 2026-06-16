import re

css_path = r"C:\Users\star0\Desktop\刷題系統\app\public\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

old_css = """/* --- Markdown UI Enhancements --- */
.markdown-body strong {
    color: #e74c3c !important;
    background-color: #fadbd8;
    padding: 2px 4px;
    border-radius: 4px;
}
.nightMode .markdown-body strong {
    color: #ff7675 !important;
    background-color: #3b2020;
}"""

new_css = """/* --- Markdown UI Enhancements --- */
/* 一般文本的螢光筆效果 */
.markdown-body strong {
    color: inherit;
    font-weight: 600;
    background-image: linear-gradient(transparent 55%, rgba(59, 130, 246, 0.5) 55%);
    background-repeat: no-repeat;
    background-size: 100% 100%;
    padding: 0 2px;
    border-radius: 2px;
}
.nightMode .markdown-body strong {
    color: inherit;
    background-image: linear-gradient(transparent 55%, rgba(59, 130, 246, 0.6) 55%);
}

/* 表格內的強烈紅底凸顯效果 */
.markdown-body table strong {
    color: #e74c3c !important;
    background-color: #fadbd8;
    background-image: none;
    padding: 2px 4px;
    border-radius: 4px;
}
.nightMode .markdown-body table strong {
    color: #ff7675 !important;
    background-color: #3b2020;
}"""

if old_css in css:
    css = css.replace(old_css, new_css)
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css)
    print("Replaced successfully.")
else:
    print("Could not find the target CSS block.")

