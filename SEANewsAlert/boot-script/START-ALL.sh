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
echo "    使用 uv 進行快速安裝..."
echo

# 檢查 uv 是否安裝
if ! command -v uv >/dev/null 2>&1; then
  echo "[警告] 未找到 uv，正在安裝..."
  $PY -m pip install --user uv
fi

# 檢查是否存在虛擬環境，如果不存在則創建
if [ ! -d ".venv" ]; then
  echo "正在創建虛擬環境..."
  uv venv .venv
fi

# 啟用虛擬環境
echo "啟用虛擬環境..."
# shellcheck source=/dev/null
source .venv/bin/activate

echo "正在使用 uv 安裝套件..."
if [ -f "requirements-api.txt" ]; then
  echo "使用 requirements-api.txt 安裝依賴..."
  uv pip install -r requirements-api.txt
else
  # fallback: 安裝常用套件（包括 openai）
  uv pip install fastapi "uvicorn[standard]" pydantic[email] agno reportlab pandas openpyxl python-dotenv openai
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

# 確保使用虛擬環境的 Python，只監控特定目錄
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload --reload-dir app --reload-dir agents --reload-dir utils
