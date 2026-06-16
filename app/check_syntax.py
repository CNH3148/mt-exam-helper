import esprima
import sys
import re

try:
    with open('public/app.js', 'r', encoding='utf-8') as f:
        content = f.read()
    # Strip optional chaining for esprima
    content = content.replace('?.', '.')
    # Also strip object spread operator
    content = re.sub(r'\{\s*\.\.\.[^}]+\}', '{}', content)
    
    esprima.parseScript(content)
    print("Syntax OK")
except Exception as e:
    print(f"Syntax Error: {e}")

