"""
FastAPI 主應用程式
東南亞金融新聞搜尋系統 - 後端 API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
import sys

# 確保可以導入專案根目錄的模組
project_root = Path(__file__).parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from config import Config
from app.routers import tasks

# 創建 FastAPI 應用
app = FastAPI(
    title="東南亞金融新聞搜尋系統 API",
    description="提供新聞搜尋、分析、報告生成和郵件發送功能的 RESTful API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5500",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:5500",
        "null"  # 允許本地文件訪問
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(tasks.router)

# 掛載靜態文件目錄（用於提供前端頁面）
public_dir = project_root / "public"
if public_dir.exists():
    app.mount("/static", StaticFiles(directory=str(public_dir)), name="static")


@app.get("/", response_class=HTMLResponse)
async def root():
    """根路徑 - 提供基本資訊"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>東南亞金融新聞搜尋系統 API</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 50px auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .container {
                background-color: white;
                padding: 30px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            h1 {
                color: #1a5490;
            }
            a {
                color: #2c5aa0;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
            .link-list {
                list-style: none;
                padding: 0;
            }
            .link-list li {
                margin: 10px 0;
                padding: 10px;
                background-color: #f8f9fa;
                border-radius: 4px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🌏 東南亞金融新聞搜尋系統 API</h1>
            <p>歡迎使用東南亞金融新聞搜尋系統後端 API</p>
            
            <h2>📚 文檔連結</h2>
            <ul class="link-list">
                <li>📖 <a href="/docs">Swagger UI 文檔</a> - 互動式 API 文檔</li>
                <li>📄 <a href="/redoc">ReDoc 文檔</a> - 替代 API 文檔</li>
                <li>🎨 <a href="/static/index.html">測試前端頁面</a> - 簡易測試介面</li>
            </ul>
            
            <h2>🔌 API 端點</h2>
            <ul class="link-list">
                <li><strong>POST</strong> /api/tasks/news-report - 創建新聞報告任務</li>
                <li><strong>GET</strong> /api/tasks/{task_id} - 查詢任務狀態</li>
            </ul>
            
            <h2>ℹ️ 系統資訊</h2>
            <p>版本: 2.0.0</p>
            <p>架構: FastAPI + RESTful API</p>
        </div>
    </body>
    </html>
    """


@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {
        "status": "healthy",
        "service": "SEA News Alert API",
        "version": "2.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    
    print("=" * 60)
    print("🚀 啟動東南亞金融新聞搜尋系統 API")
    print("=" * 60)
    print(f"📍 API 文檔: http://127.0.0.1:8000/docs")
    print(f"📍 測試前端: http://127.0.0.1:8000/static/index.html")
    print("=" * 60)
    
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
