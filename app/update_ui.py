import re
import os

css_path = r"C:\Users\star0\Desktop\刷題系統\app\public\style.css"
js_path = r"C:\Users\star0\Desktop\刷題系統\app\public\app.js"

# 1. Append CSS
new_css = """
/* --- Markdown UI Enhancements --- */
.markdown-body strong {
    color: #e74c3c !important;
    background-color: #fadbd8;
    padding: 2px 4px;
    border-radius: 4px;
}
.nightMode .markdown-body strong {
    color: #ff7675 !important;
    background-color: #3b2020;
}
.markdown-body table {
    border-collapse: collapse;
    width: 100%;
}
.markdown-body th, .markdown-body td {
    border: 1px solid #bdc3c7 !important;
    padding: 8px;
}
.nightMode .markdown-body th, .nightMode .markdown-body td {
    border: 1px solid #444 !important;
}

/* --- 全局背景與字體設定 --- */
.card {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 20px;
    text-align: center;
    color: #333333;
    background-color: #f4f6f8; /* 柔和的淺灰藍色背景，減少眼睛疲勞 */
    line-height: 1.6;
    margin: 0;
    padding: 20px 10px;
    cursor: pointer;
    user-select: none;
    margin-bottom: 20px;
}

/* --- 卡片容器設計 --- */
.front-container, .back-container {
    max-width: 600px;
    margin: 0 auto;
    background: #ffffff;
    padding: 25px 30px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.05); /* 輕微的浮凸陰影 */
}

.back-container {
    margin-top: 15px;
    border-top: 5px solid #2ecc71; /* 綠色頂部邊框，象徵「解答」 */
    text-align: center; /* 置中對齊 */
}

/* --- 文字排版 --- */
.question {
    font-size: 26px;
    font-weight: bold;
    color: #2c3e50;
}

.question-small {
    font-size: 18px;
    font-weight: normal;
    color: #7f8c8d;
}

.answer {
    font-size: 24px;
    color: #2c3e50;
}

/* --- 隱藏預設分隔線 --- */
.card hr {
    display: none; 
}

/* --- 重點字詞 (卡片背面第一行) --- */
ans {
    color: #e74c3c; /* 國考紅 */
    background-color: #fadbd8; /* 淺紅底色 */
    padding: 2px 6px;
    border-radius: 6px;
    font-weight: bold;
}

/* --- 圖片自適應與美化 (專為你手動加圖設計) --- */
.card img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    margin-top: 20px;
    margin-bottom: 10px;
    display: block;
    margin-left: auto;
    margin-right: auto;
}

/* =========================================
   夜間模式 (Dark Mode) 自動切換
   ========================================= */
.nightMode .card {
    background-color: #121212;
    color: #e0e0e0;
}

.nightMode .front-container, .nightMode .back-container {
    background: #1e1e1e;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}

.nightMode .back-container {
    border-top: 5px solid #27ae60;
}

.nightMode .question {
    color: #ecf0f1;
}

.nightMode .question-small {
    color: #95a5a6;
}

.nightMode .answer {
    color: #ecf0f1;
}

.nightMode ans {
    color: #ff7675;
    background-color: #3b2020; /* 深色背景下的柔和紅底 */
}

.nightMode .card img {
    opacity: 0.9; /* 降低圖片亮度，避免夜間刺眼 */
}

/* Anki Wall Grid */
.anki-wall {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 30px;
}
"""
with open(css_path, "r", encoding="utf-8") as f:
    current_css = f.read()

if ".anki-wall" not in current_css:
    with open(css_path, "a", encoding="utf-8") as f:
        f.write(new_css)

# 2. Update JS
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace the previous inject logic with the new Anki Wall rendering
target_js = """        // Inject Anki Copy Buttons
        const preBlocks = detailTopicDesc.querySelectorAll('pre');"""

new_js = """        // Advanced Anki Extraction and Wall Rendering
        const summaryText = aiTopicSummaries[topicName];
        
        // Find code blocks containing Anki cards (separated by semicolon)
        const preBlocks = detailTopicDesc.querySelectorAll('pre');
        preBlocks.forEach(pre => {
            const codeText = pre.innerText;
            if(codeText.includes(';') && codeText.includes('<ans>')) {
                // Add Copy Button
                const btn = document.createElement('button');
                btn.innerHTML = '📋 複製純文字題卡 (匯入 Anki 專用)';
                btn.className = 'btn btn-primary';
                btn.style.margin = '10px 0';
                btn.style.display = 'block';
                btn.onclick = () => {
                    navigator.clipboard.writeText(codeText).then(() => {
                        const original = btn.innerHTML;
                        btn.innerHTML = '✅ 已複製！';
                        setTimeout(() => btn.innerHTML = original, 2000);
                    });
                };
                pre.parentNode.insertBefore(btn, pre);
                
                // Build Anki Wall
                const lines = codeText.split('\\n');
                const wallDiv = document.createElement('div');
                wallDiv.className = 'anki-wall';
                
                lines.forEach(line => {
                    if(!line.trim()) return;
                    const parts = line.split(';');
                    if(parts.length >= 2) {
                        const front = parts[0].trim();
                        const back = parts.slice(1).join(';').trim();
                        
                        const cardDiv = document.createElement('div');
                        cardDiv.className = 'card';
                        
                        // Default state: Front only
                        cardDiv.innerHTML = `
                            <div class="front-container">
                                <div class="question">${front}</div>
                            </div>
                        `;
                        
                        let isFlipped = false;
                        cardDiv.onclick = () => {
                            isFlipped = !isFlipped;
                            if(isFlipped) {
                                cardDiv.innerHTML = `
                                    <div class="front-container">
                                        <div class="question-small">${front}</div>
                                    </div>
                                    <hr id="answer">
                                    <div class="back-container">
                                        <div class="answer">${back}</div>
                                    </div>
                                `;
                            } else {
                                cardDiv.innerHTML = `
                                    <div class="front-container">
                                        <div class="question">${front}</div>
                                    </div>
                                `;
                            }
                        };
                        wallDiv.appendChild(cardDiv);
                    }
                });
                
                // Append the Anki Wall below the code block
                const wallTitle = document.createElement('h3');
                wallTitle.textContent = '💡 互動式卡片牆 (點擊翻面)';
                wallTitle.style.marginTop = '40px';
                wallTitle.style.borderTop = '2px solid #eee';
                wallTitle.style.paddingTop = '20px';
                pre.parentNode.insertBefore(wallTitle, pre.nextSibling);
                pre.parentNode.insertBefore(wallDiv, wallTitle.nextSibling);
            }
        });"""

js_content = js_content.replace(target_js + "\n        preBlocks.forEach(pre => {\n            const btn = document.createElement('button');\n            btn.textContent = '📋 複製 Anki 題卡';\n            btn.style.marginTop = '10px';\n            btn.style.padding = '8px 12px';\n            btn.style.backgroundColor = '#007bff';\n            btn.style.color = '#fff';\n            btn.style.border = 'none';\n            btn.style.borderRadius = '5px';\n            btn.style.cursor = 'pointer';\n            btn.onclick = () => {\n                navigator.clipboard.writeText(pre.innerText).then(() => {\n                    const originalText = btn.textContent;\n                    btn.textContent = '✅ 已複製！';\n                    btn.style.backgroundColor = '#28a745';\n                    setTimeout(() => {\n                        btn.textContent = originalText;\n                        btn.style.backgroundColor = '#007bff';\n                    }, 2000);\n                });\n            };\n            pre.parentNode.insertBefore(btn, pre.nextSibling);\n        });", new_js)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print("UI updated successfully.")

