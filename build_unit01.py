import os
import shutil
import glob

src_app = r"C:\Users\star0\Desktop\刷題系統\app"
dest_app = r"C:\Users\star0\Desktop\刷題系統\初號雞"

# 1. Create directories
os.makedirs(dest_app, exist_ok=True)
os.makedirs(os.path.join(dest_app, "data"), exist_ok=True)
os.makedirs(os.path.join(dest_app, "public", "images"), exist_ok=True)
os.makedirs(os.path.join(dest_app, "saves"), exist_ok=True)

# 2. Copy server.py
shutil.copy2(os.path.join(src_app, "server.py"), os.path.join(dest_app, "server.py"))

# 3. Copy public files
public_files = ["index.html", "app.js", "style.css", "markdown.css"]
for f in public_files:
    src_file = os.path.join(src_app, "public", f)
    if os.path.exists(src_file):
        shutil.copy2(src_file, os.path.join(dest_app, "public", f))

# Copy images
for img in glob.glob(os.path.join(src_app, "public", "images", "*.*")):
    shutil.copy2(img, os.path.join(dest_app, "public", "images", os.path.basename(img)))

# 4. Copy data files
data_exts = ["*.json", "*.txt"]
for ext in data_exts:
    for f in glob.glob(os.path.join(src_app, "data", ext)):
        if "bak" not in f:
            shutil.copy2(f, os.path.join(dest_app, "data", os.path.basename(f)))

print("Copied all pure files to 初號雞 successfully.")

