import sys
import re

with open(r"C:\Users\star0\Desktop\刷題系統\app\public\app.js", "r", encoding="utf-8") as f:
    code = f.read()

# Simple strip of string literals and comments
# First comments
text = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
text = re.sub(r"//.*", "", text)
# Then strings (multiline `` included)
text = re.sub(r'`.*?`', '``', text, flags=re.DOTALL)
text = re.sub(r'".*?(?<!\\)"', '""', text)
text = re.sub(r"'.*?(?<!\\)'", "''", text)


stack = []
for i, char in enumerate(text):
    if char in "{[(":
        stack.append((char, i))
    elif char in "}])":
        if not stack:
            print(f"Unmatched {char} at index {i}")
            sys.exit(1)
        top, pos = stack.pop()
        if (char == '}' and top != '{') or (char == ']' and top != '[') or (char == ')' and top != '('):
            print(f"Mismatched {char} for {top} at index {pos}")
            sys.exit(1)

if stack:
    print(f"Unclosed: {stack[-5:]}")
else:
    print("All balanced!")

