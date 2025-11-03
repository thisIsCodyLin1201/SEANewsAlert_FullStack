#!/usr/bin/env bash
set -euo pipefail

echo "========================================"
echo "完全重建虛擬環境"
echo "========================================"
echo
echo "[警告] 這會刪除現有的 .venv 目錄"
echo
read -r -p "確定要繼續並刪除 .venv 嗎？(y/N): " confirm
if [[ ! "${confirm,,}" =~ ^y(es)?$ ]]; then
  echo "已取消。"
  exit 0
fi

echo "[1/3] 刪除舊的虛擬環境..."
if [ -d ".venv" ]; then
  rm -rf .venv
  echo "    已刪除"
else
  echo "    不存在舊環境"
fi

echo "[2/3] 創建新的虛擬環境..."
PY=python3
if ! command -v "$PY" >/dev/null 2>&1; then
  if command -v python >/dev/null 2>&1; then
    PY=python
  else
    echo "[錯誤] 找不到 python，請先安裝 Python 3" >&2
    exit 1
  fi
fi

# 檢查並安裝 uv
if ! command -v uv >/dev/null 2>&1; then
  echo "    正在安裝 uv 套件管理器..."
  "$PY" -m pip install uv
fi

uv venv .venv
echo "    創建成功 (使用 uv)"

echo "[3/3] 安裝基礎套件..."
# shellcheck source=/dev/null
source .venv/bin/activate
uv pip install fastapi "uvicorn[standard]" "pydantic[email]"

echo
echo "========================================"
echo "虛擬環境重建完成！"
echo "========================================"
echo
echo "現在請執行: ./START-ALL.sh 或 ./START-FAST.sh"
