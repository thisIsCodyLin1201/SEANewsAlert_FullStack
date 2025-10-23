#!/usr/bin/env bash
set -euo pipefail

PY=python3
if ! command -v "$PY" >/dev/null 2>&1; then
  if command -v python >/dev/null 2>&1; then
    PY=python
  else
    echo "找不到 python3 或 python，請先安裝 Python 3" >&2
    exit 1
  fi
fi

echo "========================================"
echo "🚀 一鍵安裝所有依賴並啟動 (macOS / Linux)"
echo "========================================"
echo

echo "[1/2] 安裝所有必要套件..."
echo "    建議在虛擬環境中執行： $PY -m venv .venv && source .venv/bin/activate"
echo

# 如果傳入 --venv 則自動建立並啟用 .venv
if [ "${1:-}" = "--venv" ]; then
  echo "建立並啟用虛擬環境 .venv..."
  $PY -m venv .venv
  # shellcheck source=/dev/null
  source .venv/bin/activate
fi

echo "正在更新 pip 並安裝套件..."
$PY -m pip install --upgrade pip
if [ -f "requirements-api.txt" ]; then
  echo "使用 requirements-api.txt 安裝依賴..."
  $PY -m pip install -r requirements-api.txt
else
  # fallback: 安裝常用套件（包括 openai）
  $PY -m pip install fastapi "uvicorn[standard]" pydantic[email] ddgs agno reportlab pandas openpyxl python-dotenv openai
fi

echo "    ✅ 套件安裝完成"
echo
echo "[2/2] 啟動 FastAPI 服務..."
echo
echo "========================================"
echo "🎉 服務啟動成功！"
echo "========================================"
echo "📚 API 文檔:   http://127.0.0.1:8000/docs"
echo "🌐 測試前端:   http://127.0.0.1:8000/static/index.html"
echo "❤️  健康檢查:   http://127.0.0.1:8000/health"
echo "========================================"
echo "按 Ctrl+C 停止服務"
echo "========================================"
echo

$PY -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
