# 醫檢師國考刷題系統 (MT Exam Prep System)

這是一個專為醫檢師國考設計的「**綠色免安裝便攜版**」本地端刷題系統。您可以將整個程式放在隨身碟中，帶到任何 Windows 電腦（如圖書館、醫院公用電腦）上即插即用。所有刷題進度、錯題本、重點螢光筆紀錄都會保存在隨身碟中，讓您隨時隨地保持最佳學習狀態。

---

## ⚡ Windows 快速一鍵安裝 (推薦)

如果您是第一次使用，或想把這個系統分享給同學，請直接使用這段指令。它會自動從 GitHub 下載最新版的系統，並解壓縮到您的桌面上，完全不需要手動操作！

**步驟：**
1. 在 Windows 的「開始」按鈕按右鍵，選擇 **Windows PowerShell**（或終端機）。
2. 將以下整段指令複製，貼上到黑色/藍色視窗中，並按下 `Enter` 鍵。

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $desk = [Environment]::GetFolderPath('Desktop'); $url = "https://github.com/CNH3148/mt-exam-helper/releases/download/v2.0.115-2/MT_Exam_Prep_Portable_v2.0_115-2_Windows.zip"; $zip = "$desk\temp_exam.zip"; iwr -Uri $url -OutFile $zip; Expand-Archive -Path $zip -DestinationPath "$desk\醫檢師刷題系統" -Force; rm $zip
```
*(執行完畢後，您的桌面上就會出現一個名為「醫檢師刷題系統」的資料夾，點擊裡面的 `Start_App.bat` 即可開始刷題！)*

---

## 📂 手動下載與解壓縮 (替代方案)

如果您不習慣使用指令，或是電腦環境不允許執行 PowerShell，您也可以手動下載安裝：

1. 前往本專案右側的 **Releases** 頁面。
2. 找到最新版本，點擊下方 Assets 中的 `MT_Exam_Prep_Portable_v2.0_115-2_Windows.zip` 進行下載。
3. 下載完成後，對該壓縮檔 **按右鍵 -> 解壓縮全部...**。
4. 將解壓縮出來的資料夾放到桌面或隨身碟中。
5. 進入資料夾，雙擊執行 `Start_App.bat` 即可開始刷題！

---

## 📖 系統核心功能簡介

1. **多模式刷題**：支援「循序模式」、「隨機模式」與「錯題模式」，滿足不同階段的複習需求。
2. **智慧錯題本**：答錯的題目會自動加上紅色標記，並收錄至錯題本中。當您在錯題本中重新答對時，系統會自動將其標記為已更正 (Fixed)。
3. **客製化標籤與筆記**：每一題都可以加上自訂標籤（如 `#寄生蟲`、`#必考`）與個人文字筆記。
4. **Anki 記憶卡整合**：一鍵將複雜的題目或筆記匯出為 Anki 格式，方便匯入手機背誦。
5. **高度安全與隱私**：本機伺服器限制於 `127.0.0.1`，其他人無法從外部網路偷窺或竄改您的進度。

---

## ⚙️ 技術細節與建構過程 (給想學程式的你)

這個系統是如何從零被打造出來的？為了讓非資訊背景的同學也能看懂，以下將用最淺顯的語言拆解它的技術架構。

### 1. 資料解析層 (Data Extraction)
所有的考題最初都是缺乏結構的 PDF 或純文字。我們使用了 **Python** 搭配 **Google Gemini API (AI 大語言模型)** 來進行「資料清洗」。AI 負責閱讀那些充滿無規律排版的考題，並將題目、選項 (A/B/C/D)、標準答案精準地提取出來，轉化為電腦最喜歡的 `JSON` 格式（一種有著整齊標籤的資料格式）。

### 2. 本機伺服器層 (Backend Server)
如果您只用雙擊兩下打開 HTML 網頁，瀏覽器基於安全理由（CORS 政策），會禁止網頁直接去讀取您電腦裡的資料夾。
因此，我們使用 **Python 的 FastAPI 框架** 架設了一個超輕量的「本機伺服器」。它就像一個微型網站管家：
- 當網頁需要題目時，它會去 `data/` 資料夾把 JSON 考題拿給網頁。
- 當您點擊選項或寫筆記時，它會負責把進度寫入到 `saves/` 目錄中儲存。

### 3. 獨立執行檔打包 (PyInstaller)
為了達到「**免安裝 Python 環境 (綠色軟體)**」的目標，我們使用了 **PyInstaller** 技術。它就像一個巨大的保鮮盒，把 Python 執行檔、FastAPI 伺服器程式碼、以及所有需要用到的套件，全部封裝成一個單一的 `server.exe`。這也是為什麼您只要點擊 `Start_App.bat`，系統就能在任何一台乾淨的 Windows 電腦上跑起來。

### 4. 響應式前端介面 (Frontend UI)
前端並沒有使用龐大的現代框架（如 React 或 Vue），而是反璞歸真使用了最純粹的 **Vanilla JavaScript (原生 JS)** 與 **CSS**。這種做法極大地降低了系統的負擔，讓網頁載入速度達到毫秒級。
狀態管理方面，我們使用了一個全域物件（`globalAnsweredState`）來在記憶體中追蹤使用者的每一題作答（`current_answer`）與是否更正（`is_fixed`）。

---

## 📂 專案程式碼發展史 (Repository Scripts)

這個專案經歷了多次的迭代與進化。以下依照建立時間，列出本 Repo 中各個小腳本與程式的演進歷史。它們見證了這個系統如何從一個簡單的資料處理腳本，長成一個功能完整的應用程式：

| 開發階段 | 代表程式檔名 (依照時間排序) | 程式功能簡介 |
| :--- | :--- | :--- |
| **Phase 1: 資料爬取與清洗** | `test_extractor.py`<br>`regex_extractor.py`<br>`extract_all_gemini.py` | 利用正規表達式與 Gemini AI，將混亂的歷屆考題原始檔抓取出來，並標準化轉成 JSON 格式。 |
| **Phase 2: 圖片與選項驗證** | `map_images.py`<br>`check_ans.py`<br>`fix_answers.py` | 自動校對提取出來的答案是否符合邏輯，並將題目中附帶的圖片（如顯微鏡圖）正確映射到對應的題號上。 |
| **Phase 3: 網頁雛形建立** | `server.py`<br>`update_app.py` | 建立核心的 FastAPI 後端伺服器，並寫出第一版的 HTML 與 JavaScript，讓題目可以呈現在瀏覽器上。 |
| **Phase 4: 功能擴張與打磨** | `patch_app_*.py`<br>`execute_phase*.py` | 這是開發最密集的階段。透過大量的腳本動態修改前端 JS 檔案，陸續加入了「錯題本」、「螢光筆」、「Anki 匯出」、「暗黑模式」等進階功能。 |
| **Phase 5: UI/UX 最佳化** | `patch_style.py`<br>`fix_ui.py`<br>`update_css.py` | 微調按鈕位置、優化視窗縮放的排版邏輯，確保版面在各種電腦螢幕解析度與視窗大小下都不會跑版。 |
| **Phase 6: 資料庫重構** | `restructure_db.py`<br>`refactor_ids.py` | 隨著題目增加，為了避免 ID 衝突，將每道題目的身分證字號改為「年份_考科_題號」的複合鍵 (Composite Key)，讓進度儲存更加穩固。 |
| **Phase 7: 發行版封裝** | `build_release.py`<br>`Start_App.bat` | 最終階段，使用 PyInstaller 將後端打包為獨立的 `server.exe`，並撰寫一鍵啟動的批次檔，完成隨身碟綠色版的最終型態。 |

---

## 🙏 致謝與參考資料 (Acknowledgments)

本專案的誕生，特別感謝開源社群的貢獻。在系統開發初期，我們參考了 [pofeng/exams_tw](https://github.com/pofeng/exams_tw) 專案中的程式碼架構與歷屆考題資料處理邏輯。感謝原作者的開源精神，為本系統的資料清洗與題庫建立提供了寶貴的啟發與基礎！

---

## 💸 血淚開發成本 (Development Cost)

為了讓系統擁有高品質的歷屆考題與詳解資料，我們在開發初期投入了大量的 AI 運算資源進行資料清洗與提取。在此特別紀錄這段開發血淚史 QQ：

- **Google Gemini API 使用費**：約 **NT$ 2,883.72**
- 此費用主要用於百萬字級別的考題 PDF 轉換、選項萃取與答案驗證。

![Gemini API Spend](./GeminiAPIspend.png)

---

## 🧠 系統設計想法 (Design Thoughts)

> *(作者保留區塊：之後將補上開發這個醫檢師刷題系統的初衷、遇到的痛點，以及未來可能的擴充計畫等心得。)*

---
*Developed with ❤️ for Medical Technologists.*
