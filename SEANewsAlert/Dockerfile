# 使用 Python 3.11 官方映像檔
FROM python:3.11-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴（ReportLab 和 WeasyPrint 需要）
RUN apt-get update && apt-get install -y \
    gcc \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libffi-dev \
    libcairo2 \
    libcairo2-dev \
    libgdk-pixbuf2.0-0 \
    libgdk-pixbuf2.0-dev \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY requirements-api.txt .

# 安裝 Python 依賴
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements-api.txt

# 複製專案文件
COPY config.py .
COPY workflow.py .
COPY agents/ ./agents/
COPY app/ ./app/
COPY utils/ ./utils/
COPY templates/ ./templates/
COPY public/ ./public/

# 建立報告目錄
RUN mkdir -p reports

# 暴露 FastAPI 端口
EXPOSE 8000

# 健康檢查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# 啟動命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
