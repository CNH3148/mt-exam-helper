import sys

js_path = r"C:\Users\star0\Desktop\刷題系統\app\public\app.js"
with open(js_path, "r", encoding="utf-8") as f:
    js = f.read()

start_str = "if (aiTopicSummaries[topicName]) {"
end_str = "} else if (topicName.includes('未分類')) {"

start_idx = js.find(start_str)
end_idx = js.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_logic = """if (aiTopicSummaries[topicName]) {
        detailTopicDesc.innerHTML = `<div class="markdown-body">${marked.parse(aiTopicSummaries[topicName])}</div>`;
        
        const markdownBody = detailTopicDesc.querySelector('.markdown-body');
        const notesDiv = document.getElementById('detail-topic-desc').nextElementSibling;
        
        if (markdownBody && notesDiv) {
            const headings = Array.from(markdownBody.querySelectorAll('h1, h2, h3, h4, h5, h6'));
            const ankiHeading = headings.find(h => h.textContent.toLowerCase().includes('anki'));
            
            if (ankiHeading) {
                markdownBody.insertBefore(notesDiv, ankiHeading);
            }
        }

        const preBlocks = detailTopicDesc.querySelectorAll('pre');
        preBlocks.forEach((pre) => {
            const rawText = pre.innerText;
            if (rawText.includes('<ans>') || rawText.includes('ans&gt;')) {
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
                        setTimeout(() => { btn.innerHTML = orig; }, 2000);
                    });
                };
                
                pre.parentNode.insertBefore(wrapper, pre);
                wrapper.appendChild(pre);
                wrapper.appendChild(btn); 
                
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
                        cardDiv.onclick = function() { this.classList.toggle('flipped'); };
                        cardDiv.innerHTML = `
                            <div class="front-container"><div class="question">${front}</div></div>
                            <hr id="answer" style="display:none;">
                            <div class="back-container"><div class="answer">${back}</div></div>
                        `;
                        wallContainer.appendChild(cardDiv);
                    }
                });
                
                wallOuter.appendChild(wallContainer);
                wrapper.parentNode.insertBefore(wallOuter, wrapper.nextSibling);
            }
        });
    """
    js = js[:start_idx] + new_logic + js[end_idx:]
    with open(js_path, "w", encoding="utf-8") as f:
        f.write(js)
    print("Successfully replaced.")
else:
    print("Could not find markers.")

