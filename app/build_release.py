import os
import sys
import shutil

def create_bat(target_dir, release_name):
    bat_path = os.path.join(target_dir, "start.bat")
    content = f"""@echo off
echo =========================================
echo   啟動國考刷題系統 - {release_name} (純淨版)
echo =========================================
echo.
echo 正在啟動伺服器...
echo 您的學習紀錄將統一存放到 saves 資料夾內。
echo.
echo (伺服器啟動後，請不要關閉這個黑色視窗)
echo.

set "UV_PATH=C:\\Users\\star0\\.local\\bin\\uv.exe"
IF EXIST "%UV_PATH%" (
    start http://127.0.0.1:8080/
    "%UV_PATH%" run --with fastapi --with uvicorn --with python-multipart --with pydantic python server.py
    pause
    exit /b
)

python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [錯誤] 找不到 Python 或 uv 環境！
    echo 請先安裝 Python，或確認 Python 已加入環境變數 PATH 中。
    pause
    exit /b
)

python -c "import fastapi, uvicorn, multipart, pydantic" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [系統準備] 偵測到環境中缺少運行網頁伺服器所需的套件...
    echo [系統準備] 正在自動為您安裝相關套件
    python -m pip install fastapi uvicorn python-multipart pydantic --break-system-packages
    echo 套件安裝完成！
    echo.
)

start http://127.0.0.1:8080/
python server.py

pause
"""
    with open(bat_path, "w", encoding="cp950", errors="replace") as f:
        f.write(content)

def create_readme(target_dir, release_name):
    md_path = os.path.join(target_dir, "使用說明.md")
    content = f"""# 國考刷題系統 ({release_name} 純淨版) - 使用說明書

歡迎使用國考刷題系統！這是一個專為國家考試量身打造的離線單機版網頁應用程式。本系統結合了強大的 AI 知識點分析、個人化題庫學習儀表板，以及可隨身攜帶的實體存檔機制。

## 🚀 快速啟動

1. **確認環境**：如果您是開發者，系統會自動偵測您的 `uv` 環境；如果您是在全新的電腦上，請確保電腦已安裝 [Python](https://www.python.org/downloads/)。
2. **啟動系統**：雙擊資料夾內的 `start.bat`。系統若發現缺少必要元件，會自動為您下載安裝。
3. **進入網頁**：腳本會自動在背景啟動伺服器，並開啟瀏覽器進入 `http://127.0.0.1:8080/`。
4. **結束使用**：直接關閉瀏覽器分頁，並將啟動時彈出的黑色命令提示字元視窗（CMD）關閉即可。

> **⚠️ 注意事項**：
> 伺服器運行期間，請勿關閉那個黑色視窗（CMD），否則網頁將無法存取資料與存檔。

---

## 📂 資料夾結構與備份說明

本系統為真正的「綠色軟體」，您可以隨意將整個資料夾移動到隨身碟或其他電腦中使用。

- `start.bat`：一鍵啟動腳本。
- `server.py`：本機伺服器後端程式（負責提供網頁與存檔 API）。
- `data/`：存放所有科目題庫、AI 分類樹與重點整理的唯讀檔案，請勿隨意更動。
- `public/`：存放網頁介面、樣式表與您上傳的圖片檔（`public/images/`）。
- **`saves/`：您的個人學習存檔目錄（最重要！）**

### 💾 存檔與備份指南

本系統採用實體檔案化架構。
當您在系統中點選進度儲存時，系統會自動建立 `saves/` 資料夾，並將紀錄寫入對應的 JSON 檔案中。

- **如何備份**：如果您想要備份所有的作答紀錄、釘選類別與自訂標籤，只需複製這個 `saves/` 資料夾並妥善保存即可。
- **如何還原**：日後若您將系統移動到新電腦，或是升級了新版程式，只要把舊的 `saves/` 資料夾複製貼上覆蓋回去，再次開啟系統就能無縫接軌！
"""
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(content)

def build_release():
    if len(sys.argv) > 1:
        release_name = sys.argv[1]
    else:
        release_name = input("請輸入發行版名稱 (例如: 貳號機): ").strip()
        if not release_name:
            print("發行版名稱不能為空。")
            return

    # Define paths
    app_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(app_dir)
    releases_dir = os.path.join(root_dir, "發行版")
    target_dir = os.path.join(releases_dir, release_name)

    print(f"準備建置發行版: {release_name}")
    print(f"目標路徑: {target_dir}")

    if os.path.exists(target_dir):
        print(f"[錯誤] 目標資料夾已經存在：{target_dir}")
        print("請刪除該資料夾，或是使用不同的發行版名稱。")
        return

    os.makedirs(target_dir, exist_ok=True)

    # 複製 public
    print("正在複製 public 資料夾...")
    shutil.copytree(os.path.join(app_dir, "public"), os.path.join(target_dir, "public"))

    # 複製 data
    print("正在複製 data 資料夾...")
    # 可以加入 ignore pattern 來排除特定的開發檔
    shutil.copytree(
        os.path.join(app_dir, "data"), 
        os.path.join(target_dir, "data"),
        ignore=shutil.ignore_patterns("*.py", "*.log")
    )

    # 複製 server.py
    print("正在複製 server.py...")
    shutil.copy2(os.path.join(app_dir, "server.py"), os.path.join(target_dir, "server.py"))

    # 產生 start.bat
    print("正在產生 start.bat...")
    create_bat(target_dir, release_name)

    # 產生 使用說明.md
    print("正在產生 使用說明.md...")
    create_readme(target_dir, release_name)

    print("\n正在將發行版壓縮成 ZIP 檔...")
    shutil.make_archive(target_dir, 'zip', target_dir)

    print("\n[完成] 發行版打包成功！")
    print(f"您的純淨版本資料夾存放於: {target_dir}")
    print(f"您的發行壓縮檔存放於: {target_dir}.zip (可直接分享給別人)")

if __name__ == "__main__":
    build_release()

