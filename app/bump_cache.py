import re
import time

index_path = r"C:\Users\star0\Desktop\刷題系統\app\public\index.html"
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

html = re.sub(r'app\.js\?v=\d+', f'app.js?v={int(time.time())}', html)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

