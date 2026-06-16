import sys

with open(r"C:\Users\star0\Desktop\刷題系統\app\public\app.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    # remove comments naive
    if "//" in line:
        line = line.split("//")[0]
    
    # ignore backticks for now
    
    sq = line.replace("\\'", "").count("'")
    dq = line.replace('\\"', '').count('"')
    
    if sq % 2 != 0:
        print(f"Line {i+1} has unclosed single quote: {line.strip()}")
    if dq % 2 != 0:
        print(f"Line {i+1} has unclosed double quote: {line.strip()}")


