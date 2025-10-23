#!/bin/bash

echo "===================================="
echo "  啟動 Financial News Search 前端"
echo "===================================="
echo ""

# 取得腳本所在目錄
cd "$(dirname "$0")"

echo "正在檢查依賴..."
if [ ! -d "node_modules" ]; then
    echo "首次啟動，正在安裝依賴..."
    npm install
fi

echo ""
echo "正在啟動開發伺服器..."
echo "伺服器啟動後會自動開啟瀏覽器"
echo ""
echo "按 Ctrl+C 可以停止伺服器"
echo ""

# 在背景等待3秒後開啟瀏覽器
(sleep 3 && open http://localhost:5173) &

npm run dev
