import re

css_path = r"C:\Users\star0\Desktop\刷題系統\app\public\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Replace the translucent yellow with an opaque, vibrant golden yellow suitable for dark mode
css = css.replace("rgba(250, 204, 21, 0.4)", "#a16207") # Yellow-700
css = css.replace("rgba(250, 204, 21, 0.5)", "#b45309") # Amber-700

# Let's also make the text color of the highlighted text explicitly a bright yellow instead of inherit
# We can just change "color: inherit;" to "color: #fef08a !important;" (Yellow-200) inside the markdown-body strong block
# But we need to make sure we don't mess up the table strong block

block_to_replace = """/* 一般文本的螢光筆效果 */
.markdown-body strong {
    color: inherit;
    font-weight: 600;
    background-image: linear-gradient(transparent 55%, #a16207 55%);
    background-repeat: no-repeat;
    background-size: 100% 100%;
    padding: 0 2px;
    border-radius: 2px;
}
.nightMode .markdown-body strong {
    color: inherit;
    background-image: linear-gradient(transparent 55%, #b45309 55%);
}"""

new_block = """/* 一般文本的螢光筆效果 */
.markdown-body strong {
    color: #fef08a !important; /* 明亮的淺黃色文字 */
    font-weight: 600;
    background-image: linear-gradient(transparent 55%, #854d0e 55%); /* 不透明的深金色底 */
    background-repeat: no-repeat;
    background-size: 100% 100%;
    padding: 0 2px;
    border-radius: 2px;
}
.nightMode .markdown-body strong {
    color: #fef08a !important;
    background-image: linear-gradient(transparent 55%, #854d0e 55%);
}"""

css = css.replace(block_to_replace, new_block)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

