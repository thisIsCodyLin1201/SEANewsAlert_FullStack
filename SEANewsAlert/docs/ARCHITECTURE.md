# 🏗️ 系統架構文件

## 概述

東南亞金融新聞智能搜尋與報告系統是一個基於 **Agno Multi-Agent 框架**的 End-to-End 自動化工作流系統。

## 整體架構

```
┌─────────────────────────────────────────────────────────────┐
│                        User Interface                        │
│                    (Streamlit Web App)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   Workflow Orchestrator                      │
│                     (workflow.py)                            │
└──────────────┬──────────────────────────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────────────────────────┐
│                    Agno Agent System                          │
├───────────────┬──────────────┬──────────────┬────────────────┤
│   Research    │   Analyst    │    Report    │     Email      │
│    Agent      │    Agent     │  Generator   │     Agent      │
│               │              │    Agent     │                │
│  - Web Search │ - Structure  │ - MD to PDF  │ - SMTP Send    │
│  - ChatGPT    │ - Analysis   │ - Styling    │ - Attachment   │
│  - DuckDuckGo │ - Report Gen │ - Chinese    │ - Template     │
└───────────────┴──────────────┴──────────────┴────────────────┘
               │                │              │                │
               ▼                ▼              ▼                ▼
┌─────────────────────────────────────────────────────────────┐
│                      External Services                       │
├────────────────┬───────────────┬─────────────┬───────────────┤
│  OpenAI API    │  DuckDuckGo   │  WeasyPrint │  SMTP Server  │
│  (ChatGPT)     │  (Search)     │  (PDF)      │  (Gmail)      │
└────────────────┴───────────────┴─────────────┴───────────────┘
```

## 核心組件

### 1. User Interface Layer (app.py)

**職責**: 提供用戶友好的 Web 介面

**技術**: Streamlit

**功能**:
- 搜尋查詢輸入
- 收件人郵箱管理
- 進度即時顯示
- 結果視覺化

**關鍵代碼**:
```python
st.text_area("搜尋主題")
st.text_input("收件人郵箱")
st.button("開始搜尋並寄送報告")
```

### 2. Workflow Orchestrator (workflow.py)

**職責**: 協調所有 Agents 的執行順序和數據流轉

**關鍵方法**:
- `execute()`: 執行完整工作流程
- `_update_progress()`: 更新執行進度
- `validate_agents()`: 驗證 Agents 狀態

**執行流程**:
```python
def execute(search_query, recipient_emails):
    1. Research Agent: search(query)
    2. Analyst Agent: analyze(results)
    3. Report Generator: generate_pdf(report)
    4. Email Agent: send_report(pdf, emails)
```

### 3. Agent Layer

#### 3.1 Research Agent (research_agent.py)

**職責**: 執行深度網路搜尋

**使用模型**: ChatGPT (GPT-5)

**工具**: DuckDuckGoTools

**工作流程**:
```
User Query → Enhanced Prompt → ChatGPT + Search → Structured Results
```

**關鍵配置**:
```python
Agent(
    model=OpenAIChat(id="gpt-5-2025-08-07"),
    tools=[DuckDuckGoTools()],
    instructions=[專門的搜尋指令]
)
```

#### 3.2 Analyst Agent (analyst_agent.py)

**職責**: 將搜尋結果結構化並生成報告

**輸入**: 搜尋結果 JSON

**輸出**: Markdown 格式報告

**報告結構**:
```markdown
# 東南亞金融新聞報告
## 報告摘要
## 搜尋主題
## 新聞詳情
### 新聞 1
- 來源: [標題](URL)
- 摘要: ...
## 市場洞察
## 資料來源
```

#### 3.3 Report Generator Agent (report_agent.py)

**職責**: 將 Markdown 轉換為專業 PDF

**技術**: WeasyPrint + Markdown

**功能**:
- Markdown → HTML 轉換
- CSS 樣式應用
- 中文字體支援
- 頁碼和頁首頁尾

**樣式特點**:
- A4 紙張大小
- 專業排版
- 繁體中文優化
- 超連結保留

#### 3.4 Email Agent (email_agent.py)

**職責**: 發送郵件和附件

**協議**: SMTP (TLS)

**功能**:
- HTML 郵件模板
- PDF 附件
- 多收件人支援
- 發送狀態追蹤

**郵件模板**:
- 品牌化頁首
- 報告資訊摘要
- 專業頁尾

## 數據流

```
1. 用戶輸入
   ↓
   Query: "新加坡金融科技趨勢"
   Email: "user@example.com"

2. Research Agent
   ↓
   {
     "status": "success",
     "content": "搜尋結果...",
     "sources": [...]
   }

3. Analyst Agent
   ↓
   "# 東南亞金融新聞報告\n## 報告摘要\n..."

4. Report Generator
   ↓
   Path("reports/report_20250101_120000.pdf")

5. Email Agent
   ↓
   發送成功 → True

6. 用戶收到郵件
   ↓
   包含 PDF 附件的專業郵件
```

## 配置管理 (config.py)

**職責**: 集中管理所有配置

**配置項**:
```python
class Config:
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-5-2025-08-07"
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    
    # Email
    SMTP_SERVER: str
    SMTP_PORT: int
    EMAIL_ADDRESS: str
    EMAIL_PASSWORD: str
    
    # Paths
    REPORTS_DIR: Path
    TEMPLATES_DIR: Path
```

**特點**:
- 環境變數載入
- 配置驗證
- 預設值設定
- 路徑管理

## 錯誤處理

### 分層錯誤處理

```
Level 1: Agent 層
- 捕獲 API 錯誤
- 返回錯誤狀態
- 記錄錯誤訊息

Level 2: Workflow 層
- 監控各步驟執行
- 錯誤傳播
- 回滾機制

Level 3: UI 層
- 顯示用戶友好訊息
- 提供錯誤詳情
- 引導用戶操作
```

### 常見錯誤處理

```python
try:
    result = agent.execute()
except OpenAIAPIError:
    # API 配額或連接錯誤
    return error_response("API 錯誤")
except SMTPException:
    # 郵件發送失敗
    return error_response("郵件發送失敗")
except Exception as e:
    # 其他未預期錯誤
    return error_response(str(e))
```

## 性能優化

### 1. Agent 初始化優化

```python
# 單例模式，避免重複初始化
@cached_property
def research_agent(self):
    return ResearchAgent()
```

### 2. 並行處理（未來優化）

```python
# 可並行的操作
async def parallel_search():
    tasks = [
        search_news(),
        search_reports(),
        search_analysis()
    ]
    return await asyncio.gather(*tasks)
```

### 3. 快取機制（未來優化）

```python
# 快取搜尋結果
@lru_cache(maxsize=100)
def cached_search(query: str):
    return research_agent.search(query)
```

## 安全性

### API Key 管理

```python
# 使用環境變數
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 驗證必要配置
Config.validate()
```

### 輸入驗證

```python
# 郵箱格式驗證
from email_validator import validate_email

# 查詢長度限制
max_chars=500
```

### 輸出清理

```python
# 移除敏感資訊
def sanitize_log(log: str):
    return re.sub(r'sk-[a-zA-Z0-9]+', '***', log)
```

## 擴展性

### 添加新 Agent

```python
# 1. 創建新 Agent
class NewsFilterAgent(Agent):
    def filter(self, news_list):
        pass

# 2. 在 Workflow 中註冊
self.filter_agent = NewsFilterAgent()

# 3. 添加到執行流程
filtered = self.filter_agent.filter(results)
```

### 添加新功能

```python
# 支援多語言
class MultiLangAnalyst(AnalystAgent):
    def analyze(self, results, lang="zh-TW"):
        if lang == "en":
            return self._analyze_en(results)
        return self._analyze_zh(results)
```

## 監控與日誌

### 日誌級別

```
DEBUG:   Agent 內部執行細節
INFO:    正常執行流程
WARNING: 可恢復的錯誤
ERROR:   嚴重錯誤
```

### 關鍵指標

```python
metrics = {
    "search_time": search_duration,
    "analysis_time": analysis_duration,
    "pdf_size": pdf_file_size,
    "success_rate": successful / total
}
```

## 測試策略

### 單元測試

```python
# 測試單個 Agent
def test_research_agent():
    agent = ResearchAgent()
    result = agent.search("test")
    assert result["status"] == "success"
```

### 整合測試

```python
# 測試完整工作流程
def test_workflow():
    workflow = SEANewsWorkflow()
    result = workflow.execute(query, email)
    assert result["status"] == "success"
```

### E2E 測試

```bash
# 使用實際 API 測試
python main.py cli -q "測試" -e "test@example.com"
```

## 部署架構

### 本地開發

```
[Developer] → [Local Python] → [Streamlit] → [localhost:8501]
```

### Docker 部署

```
[User] → [Docker Container] → [Streamlit App] → [Port 8501]
                               ↓
                         [Agno Agents]
```

### 雲端部署

```
[User] → [Load Balancer] → [Cloud Run] → [Container]
                                           ↓
                                    [Agno Agents]
                                           ↓
                                    [External APIs]
```

## 依賴關係

```
pyproject.toml
├── agno >= 2.0.0          # Multi-Agent 框架
├── openai >= 1.0.0        # ChatGPT API
├── streamlit >= 1.32.0    # Web 介面
├── weasyprint >= 60.0     # PDF 生成
├── markdown >= 3.5.0      # Markdown 處理
└── aiosmtplib >= 3.0.0    # 非同步郵件
```

## 未來規劃

### Phase 2: 功能增強
- [ ] 支援定時自動執行
- [ ] 報告模板自定義
- [ ] 多語言支援
- [ ] 資料庫儲存

### Phase 3: 性能優化
- [ ] 結果快取
- [ ] 並行處理
- [ ] 增量搜尋

### Phase 4: 企業功能
- [ ] 用戶管理
- [ ] 權限控制
- [ ] 審計日誌
- [ ] API 介面

---

**維護者**: Development Team  
**最後更新**: 2025-01
