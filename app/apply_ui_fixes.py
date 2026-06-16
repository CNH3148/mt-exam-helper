import re
import time

index_path = r"C:\Users\star0\Desktop\刷題系統\app\public\index.html"
css_path = r"C:\Users\star0\Desktop\刷題系統\app\public\style.css"
js_path = r"C:\Users\star0\Desktop\刷題系統\app\public\app.js"

# 1. Bust Cache in index.html
with open(index_path, "r", encoding="utf-8") as f:
    html = f.read()

ts = int(time.time())
html = re.sub(r'href="style\.css(\?v=\d+)?"', f'href="style.css?v={ts}"', html)
html = re.sub(r'src="app\.js(\?v=\d+)?"', f'src="app.js?v={ts}"', html)

with open(index_path, "w", encoding="utf-8") as f:
    f.write(html)

# 2. Fix app.js
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

# We need to completely rewrite the Anki injection part in app.js
# Let's find the start of `if (aiTopicSummaries[topicName]) {` and replace its block.
# Actually, the easiest way is to use regex or string replace for the whole block.
# I will just write a precise replacement.

start_marker = "// Re-order \"我的單元筆記\" to be before the Anki heading"
end_marker = "wrapper.parentNode.insertBefore(wallOuter, wrapper.nextSibling);"

pattern = re.compile(re.escape(start_marker) + r".*?" + re.escape(end_marker) + r"\s*\}\s*\);\s*", re.DOTALL)

new_logic = """// Re-order "我的單元筆記" to be before the Anki heading
          const markdownBody = detailTopicDesc.querySelector('.markdown-body');
          let notesDiv = document.getElementById('detail-topic-desc').nextElementSibling;
          
          if (markdownBody) {
              const headings = Array.from(markdownBody.querySelectorAll('h1, h2, h3, h4, h5, h6'));
              const ankiHeading = headings.find(h => h.textContent.toLowerCase().includes('anki'));
              
              if (ankiHeading && notesDiv) {
                  // Move notesDiv inside markdownBody, right before ankiHeading
                  markdownBody.insertBefore(notesDiv, ankiHeading);
              }
          }

          // Inject Anki Copy Buttons and Card Wall
          const preBlocks = detailTopicDesc.querySelectorAll('pre');
          preBlocks.forEach((pre, index) => {
              const rawText = pre.innerText;
              if (rawText.includes('<ans>') || rawText.includes('ans&gt;')) {
                  
                  // Wrap pre block for Obsidian-style copy button
                  const wrapper = document.createElement('div');
                  wrapper.className = 'code-block-wrapper';
                  
                  const btn = document.createElement('button');
                  btn.className = 'copy-obsidian-btn';
                  btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg> 複製'; 
                  btn.title = '複製 Anki 題卡';
                  btn.onclick = () => {
                      navigator.clipboard.writeText(rawText).then(() => {
                          const orig = btn.innerHTML;
                          btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg> 已複製';
                          setTimeout(() => {
                              btn.innerHTML = orig;
                          }, 2000);
                      });
                  };
                  
                  pre.parentNode.insertBefore(wrapper, pre);
                  wrapper.appendChild(pre);
                  wrapper.appendChild(btn); 
  
                  // Build Card Wall Container
                  const wallOuter = document.createElement('div');
                  wallOuter.style.marginTop = '30px';
                  wallOuter.style.width = '100%';
                  wallOuter.innerHTML = '<h3 style="margin-bottom:16px; color:var(--accent); font-size:1.2rem;">✨ 互動式卡片牆</h3>';
                  
                  const wallContainer = document.createElement('div');
                  wallContainer.className = 'anki-card-wrapper';
                  
                  const cardsData = rawText.split('\\n').filter(line => line.trim() !== '');
                  cardsData.forEach(line => {
                      let front = line;
                      let back = '';
                      
                      let ansIndex = line.indexOf('<ans>');
                      if (ansIndex === -1) ansIndex = line.indexOf('&lt;ans&gt;');
                      
                      if (ansIndex !== -1) {
                          let sepIndex = ansIndex;
                          if (line[ansIndex - 1] === ';' || line[ansIndex - 1] === '：' || line[ansIndex - 1] === ':' || line[ansIndex - 1] === ' ') {
                              sepIndex = ansIndex - 1;
                          }
                          front = line.substring(0, sepIndex).trim();
                          back = line.substring(ansIndex).trim();
                      } else {
                          const match = line.match(/[;；]/);
                          if (match) {
                              front = line.substring(0, match.index).trim();
                              back = line.substring(match.index + 1).trim();
                          }
                      }
                      
                      if (front) {
                          const cardDiv = document.createElement('div');
                          cardDiv.className = 'anki-card';
                          cardDiv.onclick = function() {
                              this.classList.toggle('flipped');
                          };
                          cardDiv.innerHTML = `
                              <div class="front-container">
                                  <div class="question">${front}</div>
                              </div>
                              <hr id="answer">
                              <div class="back-container">
                                  <div class="answer">${back}</div>
                              </div>
                          `;
                          wallContainer.appendChild(cardDiv);
                      }
                  });
                  
                  wallOuter.appendChild(wallContainer);
                  wrapper.parentNode.insertBefore(wallOuter, wrapper.nextSibling);
              }
          });
"""

# Wait, if the target is not found, we can also use string slicing based on indexOf.
# Since app.js has different versions, let's just replace from `// Re-order "我的單元筆記"` to `wrapper.parentNode.insertBefore(wallOuter, wrapper.nextSibling);` plus `              }` and `          });`.
# We'll use a robust regex.

js_new = pattern.sub(new_logic, js)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_new)

# 3. Fix style.css
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

new_styles = """
/* Code Block & Obsidian Button */
.code-block-wrapper {
    position: relative;
    margin-top: 16px;
    margin-bottom: 24px;
}
.code-block-wrapper pre {
    background: #1e1e1e !important;
    padding: 16px;
    padding-top: 40px; /* Space for the button */
    border-radius: 8px;
    overflow-x: auto;
    color: #d4d4d4 !important;
    font-family: 'Consolas', monospace;
    font-size: 14px;
    border: 1px solid var(--glass-border);
    margin: 0;
}
.copy-obsidian-btn {
    position: absolute;
    top: 8px;
    right: 8px;
    background: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #94a3b8;
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    align-items: center;
    gap: 4px;
}
.copy-obsidian-btn:hover {
    background: rgba(255, 255, 255, 0.2);
    color: #fff;
}

/* Card Wall Tweaks */
.anki-card-wrapper {
    margin-top: 16px;
    padding: 20px;
    background: var(--bg-panel);
    border-radius: 12px;
    border: 1px solid var(--glass-border);
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    width: 100%;
}
@media (max-width: 1024px) {
    .anki-card-wrapper { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 600px) {
    .anki-card-wrapper { grid-template-columns: 1fr; }
}

.anki-card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    text-align: center;
    line-height: 1.5;
    margin: 0;
    border-radius: 10px;
    cursor: pointer;
    transition: transform 0.2s;
    background-color: #1a1a1a;
    color: #e0e0e0;
    display: flex;
    flex-direction: column;
    height: 100%;
    border: 1px solid #333;
}
.anki-card:hover {
    transform: translateY(-2px);
    border-color: #444;
}
.anki-card .front-container, .anki-card .back-container {
    width: 100%; 
    box-sizing: border-box;
    padding: 16px 20px;
    border-radius: 10px;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
}
.anki-card .back-container {
    border-top: 3px solid #27ae60;
}
.anki-card .question {
    font-size: 16px;
    color: #ecf0f1;
    font-weight: 500;
}
.anki-card .answer {
    font-size: 16px;
    color: #a78bfa;
}
"""

# Append new styles if they don't exist
if "code-block-wrapper pre" not in css:
    css += new_styles
else:
    # We could replace the old ones, but to be safe we just replace the whole file's end portion
    # Wait, let's just do a blanket replacement of the anki-card styles
    css = re.sub(r'\.anki-card-wrapper\s*\{.*?\}', '', css, flags=re.DOTALL)
    css = re.sub(r'@media.*?\.\anki-card-wrapper.*?\}', '', css, flags=re.DOTALL)
    css = re.sub(r'\.anki-card\s*\{.*?\}', '', css, flags=re.DOTALL)
    css = re.sub(r'\.anki-card:hover\s*\{.*?\}', '', css, flags=re.DOTALL)
    css = re.sub(r'\.anki-card \.front-container.*?\.\anki-card \.back-container\s*\{.*?\}', '', css, flags=re.DOTALL)
    css = re.sub(r'\.anki-card \.back-container\s*\{.*?\}', '', css, flags=re.DOTALL)
    css = re.sub(r'\.anki-card \.question\s*\{.*?\}', '', css, flags=re.DOTALL)
    css = re.sub(r'\.anki-card \.answer\s*\{.*?\}', '', css, flags=re.DOTALL)
    css += new_styles

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)

print("Done")

