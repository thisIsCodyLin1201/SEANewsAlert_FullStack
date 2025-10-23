# 🌏 東南亞金融新聞智能搜尋與報告系統

基於 **FastAPI** 的前後端分離架構，提供自動化新聞搜尋、分析、報告生成和郵件發送的 RESTful API 服務。

## 📋 功能特色

- 🔍 **智能搜尋**: 使用 OpenAI GPT 自動解析需求並執行網路搜尋
- 📊 **自動分析**: 將搜尋結果結構化並整理成專業報告
- 📄 **雙格式報告**: 自動生成 PDF 和 Excel 格式報告
- 📧 **郵件寄送**: 透過 SMTP 自動發送報告至指定郵箱
- 🚀 **RESTful API**: 完整的後端 API，支援任務創建和狀態查詢
- 🌐 **前後端分離**: 簡易前端 + 完整 API 文件，方便前端整合

## 🏗️ 技術架構

### 核心技術棧
- **後端框架**: FastAPI 0.109.0+
- **Web 伺服器**: Uvicorn (ASGI)
- **語言**: Python 3.11+
- **套件管理**: pip
- **前端**: 簡易 HTML（public/index.html）+ 完整 API 供自訂前端使用
- **PDF 生成**: ReportLab
- **Excel 生成**: Pandas + openpyxl
- **AI 模型**: OpenAI GPT-5 (gpt-5-2025-08-07)
- **搜尋引擎**: DuckDuckGo
- **郵件服務**: SMTP (Gmail)

### Agent 架構
```
NewsReportWorkflow
├── ResearchAgent        # 搜尋代理（DuckDuckGo）
├── AnalystAgent         # 分析代理（GPT-5）
├── ReportGeneratorAgent # 報告生成代理（PDF + Excel）
└── EmailAgent           # 郵件代理（SMTP）
```

### API 架構
```
FastAPI Backend
├── /api/tasks/news-report (POST)  # 創建新聞搜尋任務
├── /api/tasks/{task_id} (GET)     # 查詢任務狀態
└── /health (GET)                  # 健康檢查
```

## 🚀 快速開始

### 前置需求
- Python 3.11 或更高版本
- Git（選用）

### 安裝步驟

1. **克隆專案**
```bash
git clone <repository-url>
cd SEANewsAlert
```

2. **配置環境變數**

複製 `.env.example` 並重命名為 `.env`，填入必要資訊：
```env
OPENAI_API_KEY=your_openai_api_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
```

> ⚠️ **Gmail 使用者**：請使用「應用程式密碼」，不是普通密碼
> 設定路徑：Google 帳戶 → 安全性 → 兩步驟驗證 → 應用程式密碼

3. **安裝依賴並啟動服務**

**方式 1: 一鍵啟動（推薦）**
```bash
# Windows
START-ALL.bat

# 會自動：
# 1. 檢查並安裝所需套件
# 2. 啟動 FastAPI 服務
# 3. 在瀏覽器開啟測試頁面
```

**方式 2: 手動啟動**
```bash
# 安裝依賴
pip install -r requirements-api.txt

# 啟動服務
START-FAST.bat
# 或
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

4. **驗證安裝**

瀏覽器開啟：
- API 文件：http://127.0.0.1:8000/docs
- 測試前端：http://127.0.0.1:8000/static/index.html
- 健康檢查：http://127.0.0.1:8000/health

## 💻 使用方式

### 方式 1: 測試前端（快速體驗）

1. 啟動服務後，開啟 http://127.0.0.1:8000/static/index.html
2. 輸入搜尋需求（例如：搜尋新加坡金融科技最新發展，要英文新聞）
3. 輸入接收郵箱
4. 點擊「開始搜尋」
5. 即時查看進度（自動輪詢）
6. 完成後報告會自動發送到郵箱

### 方式 2: API 整合（前端開發）

查看 **[FRONTEND_API.md](./FRONTEND_API.md)** 了解完整 API 文件。

**核心 2 個 API：**

```javascript
// 1. 創建任務
const response = await fetch('http://127.0.0.1:8000/api/tasks/news-report', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_prompt: '搜尋新加坡金融新聞',
    email: 'user@example.com'
  })
});
const { task_id } = await response.json();

// 2. 輪詢狀態（每 2 秒）
const status = await fetch(`http://127.0.0.1:8000/api/tasks/${task_id}`);
const data = await status.json();
console.log(`進度: ${data.progress}% - ${data.step_message}`);
```

### 方式 3: Swagger UI（API 測試）

開啟 http://127.0.0.1:8000/docs 直接測試 API。

## 📁 專案結構

```
SEANewsAlert/
├── app/                        # FastAPI 後端應用
│   ├── main.py                 # FastAPI 主程式
│   ├── routers/                # API 路由
│   │   └── tasks.py            # 任務相關 API
│   └── services/               # 業務邏輯
│       ├── progress.py         # 任務狀態管理
│       └── workflow.py         # 工作流程編排
├── agents/                     # Agent 模組
│   ├── research_agent.py       # 搜尋代理
│   ├── analyst_agent.py        # 分析代理
│   ├── report_agent.py         # 報告生成代理
│   └── email_agent.py          # 郵件代理
├── public/                     # 前端靜態文件
│   └── index.html              # 測試用前端頁面
├── reports/                    # 生成的報告（PDF + Excel）
├── templates/                  # 報告模板
├── docs/                       # 技術文件
│   ├── ARCHITECTURE.md         # 架構說明
│   └── SYSTEM_FLOW.md          # 系統流程
├── utils/                      # 工具函數
├── workflow.py                 # 工作流程（給 agents 使用）
├── config.py                   # 配置管理
├── .env                        # 環境變數（不提交）
├── .env.example                # 環境變數範例
├── requirements-api.txt        # Python 依賴
├── pyproject.toml              # 專案配置
├── START-FAST.bat              # 快速啟動腳本（推薦）
├── START-ALL.bat               # 一鍵安裝並啟動
├── REBUILD-VENV.bat            # 重建虛擬環境
├── README.md                   # 📖 專案說明（本文件）
├── FRONTEND_API.md             # 📘 前端 API 文件
├── PRD.md                      # 📋 產品需求文件
├── HOW_TO_START.md             # 🚀 啟動指南
└── TROUBLESHOOTING.md          # 🔧 故障排除
```

## 🎯 工作流程

```mermaid
graph TD
    A[前端提交任務] --> B[FastAPI 創建任務]
    B --> C[返回 task_id]
    C --> D[前端輪詢狀態]
    D --> E[ResearchAgent 搜尋新聞]
    E --> F[AnalystAgent 分析整理]
    F --> G[ReportGenerator 生成 PDF+Excel]
    G --> H[EmailAgent 發送郵件]
    H --> I[任務完成]
    D --> D
```

### 詳細步驟

## 🔄 工作流程

1. **需求解析** → 使用 GPT-5 自動解析使用者輸入 (0-24%)
2. **網路搜尋** → DuckDuckGo 搜尋新聞 (25-49%)
3. **資訊分析** → GPT-5 整理並生成 Markdown 報告 (50-74%)
4. **報告生成** → ReportLab 生成 PDF，Pandas 生成 Excel (75-89%)
5. **郵件發送** → SMTP 發送報告 (90-100%)

##  疑難排解

完整故障排除請查看 **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)**

**常見問題**：
- 啟動失敗 → 執行 `python -m uvicorn app.main:app`
- OpenAI 錯誤 → 檢查 `.env` 的 `OPENAI_API_KEY`
- 郵件失敗 → Gmail 必須使用「應用程式密碼」
- PDF 中文問題 → 系統已自動處理跨平台字體

## 📝 版本記錄

- **v2.0.0**: FastAPI 架構，前後端分離，RESTful API
- **v1.0.0**: 初始版本（Streamlit，已淘汰）

## 📚 相關文件

- **[FRONTEND_API.md](./FRONTEND_API.md)** - API 完整文件
- **[HOW_TO_START.md](./HOW_TO_START.md)** - 啟動指南
- **[TROUBLESHOOTING.md](./TROUBLESHOOTING.md)** - 故障排除

---

**版本**: 2.0.0 | **架構**: FastAPI + OpenAI GPT-5 + DuckDuckGo + ReportLab
