#!/bin/bash
cd "$(dirname "$0")/app"

echo "========================================================"
echo "        MT Exam Prep - Release Version 2.0 (Mac ??"
echo "========================================================"
echo ""

# 瑼Ｘ?臬撌脩?蝺刻陌??server ?瑁?瑼?if [ -f "./server" ]; then
    echo "甇???隡箸???.."
    echo "?? Ctrl+C ??湔????蝡舀?閬??喳?迫隡箸??具?
    echo ""
    ./server
else
    echo "?隤扎銝蝺刻陌憟賜?隡箸??典銵? (server)嚗?
    echo "隢????瑁?憭惜??compile_mac.command 靘脰?蝺刻陌蝔???
    echo ""
    read -p "??Enter ?萇???.."
fi
