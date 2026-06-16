import re

file_path = r"C:\Users\star0\Desktop\刷題系統\app\public\app.js"

with open(file_path, "r", encoding="utf-8") as f:
    app_js = f.read()

target_code = """    detailTopicTitle.textContent = topicName;
    // Render AI Summaries if available
    if (aiTopicSummaries[topicName]) {
        detailTopicDesc.innerHTML = `<div class="markdown-body">${marked.parse(aiTopicSummaries[topicName])}</div>`;
    } else if (topicName.includes('綜合性考題')) {"""

replacement_code = """    detailTopicTitle.textContent = topicName;
    // Render AI Summaries if available
    if (aiTopicSummaries[topicName]) {
        detailTopicDesc.innerHTML = `<div class="markdown-body">${marked.parse(aiTopicSummaries[topicName])}</div>`;
        
        // Inject Anki Copy Buttons
        const preBlocks = detailTopicDesc.querySelectorAll('pre');
        preBlocks.forEach(pre => {
            const btn = document.createElement('button');
            btn.textContent = '📋 複製 Anki 題卡';
            btn.style.marginTop = '10px';
            btn.style.padding = '8px 12px';
            btn.style.backgroundColor = '#007bff';
            btn.style.color = '#fff';
            btn.style.border = 'none';
            btn.style.borderRadius = '5px';
            btn.style.cursor = 'pointer';
            btn.onclick = () => {
                navigator.clipboard.writeText(pre.innerText).then(() => {
                    const originalText = btn.textContent;
                    btn.textContent = '✅ 已複製！';
                    btn.style.backgroundColor = '#28a745';
                    setTimeout(() => {
                        btn.textContent = originalText;
                        btn.style.backgroundColor = '#007bff';
                    }, 2000);
                });
            };
            pre.parentNode.insertBefore(btn, pre.nextSibling);
        });
        
    } else if (topicName.includes('綜合性考題')) {"""

new_app_js = app_js.replace(target_code, replacement_code)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_app_js)

print("Injected Anki copy button logic!")

