import re

js_path = r"C:\Users\star0\Desktop\刷題系統\app\public\app.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# The issue is `rawText.split('\n')` where the newline is literal inside single quotes.
# We want to replace it with `rawText.split('\\n')`
# The literal text is: `rawText.split('\n')`
# We can find it using regex: rawText\.split\('[\r\n]+'\)
js = re.sub(r"rawText\.split\('[\r\n]+'\)", r"rawText.split('\\n')", js)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js)

print("Fixed!")

