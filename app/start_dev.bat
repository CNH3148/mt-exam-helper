@echo off
echo =========================================
echo   啟動國考刷題系統 - 開發環境
echo =========================================
echo.
echo 正在啟動伺服器...
echo 開發環境的進度將直接儲存在 app\saves 資料夾內。
echo.

set "UV_PATH=C:\Users\star0\.local\bin\uv.exe"
IF EXIST "%UV_PATH%" (
    start http://127.0.0.1:8080/
    "%UV_PATH%" run --with fastapi --with uvicorn --with python-multipart --with pydantic python server.py
    pause
    exit /b
)

python -c "import fastapi" 2>nul
IF %ERRORLEVEL% NEQ 0 (
    echo [系統準備] 開發環境正在為您安裝套件...
    python -m pip install fastapi uvicorn python-multipart pydantic --break-system-packages
)

start http://127.0.0.1:8080/
python server.py

pause
