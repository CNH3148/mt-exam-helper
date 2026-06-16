with open('app/public/app.js', 'r', encoding='utf-8') as f:
    js = f.read()

old_svg = '<svg class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
new_svg = '<svg class="eye-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px; height:16px; position:absolute; top:50%; left:50%; transform:translate(-50%, -50%); opacity:0; transition:opacity 0.3s; pointer-events:none; color:#3b82f6;">'

js = js.replace(old_svg, new_svg)

old_header = '<div class="list-card-header">'
new_header = '<div class="list-card-header" style="align-items: center;">'
js = js.replace(old_header, new_header)

with open('app/public/app.js', 'w', encoding='utf-8') as f:
    f.write(js)

