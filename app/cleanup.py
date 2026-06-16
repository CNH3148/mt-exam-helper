import re

with open('public/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# remove modal btn events
js = re.sub(r'// Modal\s*btnAdvancedSearch.*?btnAdvSearchOnly.*?\}\;', '', js, flags=re.DOTALL)
js = re.sub(r'const btnAdvancedSearch.*?getElementById.*?\;', '', js)

with open('public/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

