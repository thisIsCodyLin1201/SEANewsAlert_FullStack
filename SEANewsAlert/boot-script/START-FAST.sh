#!/usr/bin/env bash
set -euo pipefail

PY=python3
if ! command -v "$PY" >/dev/null 2>&1; then
  if command -v python >/dev/null 2>&1; then
    PY=python
  else
    echo "[錯誤] 找不到 python，請先安裝 Python 3.11+" >&2
    exit 1
  fi
fi

echo "========================================"
echo "東南亞金融新聞搜尋系統 - 快速啟動"
echo "========================================"
echo

echo "[步驟 1/3] 檢查套件..."

check_and_install() {
  module="$1"
  pkg="$2"
  if ! "$PY" -c "import ${module}" >/dev/null 2>&1; then
    echo "    安裝 ${pkg}..."
    "$PY" -m pip install "${pkg}"
  fi
}

check_and_install fastapi fastapi
check_and_install uvicorn "uvicorn[standard]"
check_and_install pydantic "pydantic[email]"
check_and_install ddgs ddgs
check_and_install agno agno
check_and_install reportlab reportlab
if ! "$PY" -c "import pandas" >/dev/null 2>&1; then
  echo "    安裝 Pandas (及 openpyxl)..."
  "$PY" -m pip install pandas openpyxl
fi

echo "    套件檢查完成"

echo "[步驟 2/3] 檢查依賴..."
if [ -f "requirements-api.txt" ]; then
  echo "    安裝 API 依賴 (requirements-api.txt)..."
  "$PY" -m pip install -r requirements-api.txt
fi

echo "[步驟 3/3] 啟動服務..."
echo
echo "========================================"
echo "🚀 服務啟動中..."
echo "========================================"
echo "📚 API 文檔:   http://127.0.0.1:8000/docs"
echo "🌐 測試前端:   http://127.0.0.1:8000/static/index.html"
echo "❤️  健康檢查:   http://127.0.0.1:8000/health"
echo "========================================"
echo "按 Ctrl+C 停止服務"
echo "========================================"
echo

# 使用系統 Python 啟動（不強制使用虛擬環境）
"$PY" -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
