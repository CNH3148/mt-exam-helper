# 醫檢師國考小幫手 (MT Exam helper)

這是一個專為醫檢師國考設計的「**綠色免安裝便攜版**」本地端刷題系統。可直接放置於隨身碟中，帶到任何 Windows/Mac 電腦上即插即用。所有刷題進度與筆記皆會保存在本地，讓您隨時隨地保持最佳學習狀態。

---

## 快速一鍵安裝 (推薦)

只需複製以下指令並執行，系統將會**自動為您下載最新版本**、在桌面解壓縮，並處理好所有安全權限，完全不需手動操作！

### 🪟 Windows 使用者
1. 在 Windows 的「開始」按鈕按右鍵，選擇 **Windows PowerShell**（或終端機）。
2. 將以下整段指令複製，貼上到視窗中並按下 `Enter` 鍵：

```powershell
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $api = "https://api.github.com/repos/CNH3148/mt-exam-helper/releases/latest"; $url = (Invoke-RestMethod $api).assets | Where-Object name -match 'Windows.*\.zip$' | Select-Object -ExpandProperty browser_download_url; $desk = [Environment]::GetFolderPath('Desktop'); $zip = "$desk\temp_exam.zip"; iwr -Uri $url -OutFile $zip; Expand-Archive -Path $zip -DestinationPath "$desk\醫檢師刷題小幫手_Windows" -Force; rm $zip
```

> 執行完畢後，桌面會出現「**醫檢師刷題小幫手_Windows**」資料夾，進入並雙擊 `Start_App.bat` 即可開始刷題！

### 🍎 Mac 使用者 (Beta 版)

1. 按下 `Command + 空白鍵` 搜尋並打開 **「終端機 (Terminal)」**。
    
2. 將以下整段指令複製，貼上到視窗中並按下 `Enter` 鍵：

```Bash
cd ~/Desktop && URL=$(curl -s "https://api.github.com/repos/CNH3148/mt-exam-helper/releases/latest" | grep "browser_download_url" | grep -i "Mac" | cut -d '"' -f 4 | head -n 1) && curl -L -o temp_exam_mac.zip "$URL" && unzip -q temp_exam_mac.zip -d 醫檢師刷題系統_Mac && rm temp_exam_mac.zip && xattr -cr 醫檢師刷題系統_Mac
```

> 執行完畢後，桌面會出現「**醫檢師刷題系統_Mac**」資料夾，進入並雙擊 `Start_App.command` 即可開始刷題！（此指令已自動為您解除 Mac 煩人的隔離機制）

## 📂 手動下載 (替代方案)

若您的電腦環境無法執行終端機指令，請手動下載安裝：

1. 前往右側的 **[Releases](https://www.google.com/search?q=https://github.com/CNH3148/mt-exam-helper/releases/latest)** 頁面。
    
2. 下載最新版本對應的壓縮檔（`.zip`）。
    
3. 將其解壓縮至桌面或隨身碟。
    
4. 進入資料夾執行 `Start_App` 即可啟動。
    

## 💻 系統需求

- **支援環境**：Windows 10/11 (64-bit) 或 macOS。
    
- **硬體需求**：能順暢上網的電腦皆可執行。
    
- ⚠️ 目前暫不支援在手機或平板上以本機伺服器模式運行。
    

_Developed with ❤️ for Medical Technologists._
