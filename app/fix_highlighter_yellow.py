import re

css_path = r"C:\Users\star0\Desktop\刷題系統\app\public\style.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Replace the blue highlighter with yellow
css = css.replace("rgba(59, 130, 246, 0.5)", "rgba(250, 204, 21, 0.4)")
css = css.replace("rgba(59, 130, 246, 0.6)", "rgba(250, 204, 21, 0.5)")

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)
print("Changed to yellow highlighter.")

