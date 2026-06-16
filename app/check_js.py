import sys

with open(r"C:\Users\star0\Desktop\刷題系統\app\public\app.js", "r", encoding="utf-8") as f:
    code = f.read()

# Let's count braces and parenthesis
brace_count = 0
paren_count = 0

lines = code.split("\n")
for i, line in enumerate(lines):
    # This is a naive check but might spot obvious unclosed blocks
    pass

import esprima # Might not be installed, let's just use regex or print the trailing block
# print the tail 50 lines to see if there's an obvious missing bracket
print("\n".join(lines[-50:]))

