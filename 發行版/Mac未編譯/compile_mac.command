#!/bin/bash
cd "$(dirname "$0")/app"

echo "========================================="
echo "  ????Mac 蝺刻陌??鋆???(PyInstaller)"
echo "========================================="

# 瑼Ｘ?臬??鋆?uv
if ! command -v uv &> /dev/null
then
    echo "?曆???uv嚗迤?函?典?鋆?uv (擃? Python 憟辣蝞∠???..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

echo "甇?雿輻 uvx 銝?銝血銵?PyInstaller ?脰?蝺刻陌..."
uvx --with fastapi --with uvicorn --with python-multipart --with pydantic pyinstaller --onefile server.py

if [ $? -eq 0 ]; then
    echo "========================================="
    echo "蝺刻陌??嚗迤?冽??摮?..."
    mv dist/server ./server
    rm -rf build dist server.spec
    echo "?剖?嚗ac ??鋆?撌脩?皞?摰??
    echo "隞亙??芾?暺? [Start_App.command] ?喳銝?萄??頂蝯梧?"
else
    echo "========================================="
    echo "蝺刻陌憭望?嚗?瑼Ｘ銝?隤方??胯?
fi

echo ""
read -p "??Enter ?菟??迨閬?..."
