#!/bin/bash
cd "$(dirname "$0")/app"

echo "========================================================"
echo "        MT Exam Prep - Release Version 2.0 (Mac 版)"
echo "========================================================"
echo ""

# 檢查是否已經編譯過 server 執行檔
if [ -f "./server" ]; then
    echo "正在啟動伺服器..."
    echo "按下 Ctrl+C 或者是關閉這個黑色終端機視窗即可安全停止伺服器。"
    echo ""
    ./server
else
    echo "【錯誤】找不到伺服器執行檔 (app/server)！"
    echo "請確認您下載的是完整的 Mac 免安裝版，且沒有誤刪檔案。"
    echo ""
    read -p "按 Enter 鍵退出..."
fi
