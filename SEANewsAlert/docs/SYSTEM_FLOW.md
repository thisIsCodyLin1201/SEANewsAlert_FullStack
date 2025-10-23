# 🔄 系統流程圖

## 整體架構流程

```
┌─────────────────────────────────────────────────────────────────┐
│                         使用者介面層                              │
│                                                                   │
│  ┌─────────────────┐                    ┌──────────────────┐   │
│  │  Streamlit Web  │                    │   CLI Interface   │   │
│  │    Interface    │                    │                   │   │
│  └────────┬────────┘                    └────────┬─────────┘   │
│           │                                       │              │
└───────────┼───────────────────────────────────────┼──────────────┘
            │                                       │
            └───────────────────┬───────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                      工作流程編排層                               │
│                                                                   │
│              ┌──────────────────────────────┐                   │
│              │   SEANewsWorkflow            │                   │
│              │   (workflow.py)              │                   │
│              │                              │                   │
│              │  • 協調 4 個 Agents          │                   │
│              │  • 進度追蹤與回調            │                   │
│              │  • 錯誤處理與恢復            │                   │
│              └──────────┬───────────────────┘                   │
└─────────────────────────┼───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                      Multi-Agent 層                               │
│                     (Agno Framework)                              │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Research    │  │   Analyst    │  │   Report     │          │
│  │   Agent      │  │    Agent     │  │  Generator   │          │
│  │              │  │              │  │    Agent     │          │
│  │ • Web Search │  │ • Structure  │  │ • MD to PDF  │          │
│  │ • ChatGPT    │──▶│ • Analysis   │──▶│ • Styling    │──┐      │
│  │ • DuckDuckGo │  │ • Markdown   │  │ • Chinese    │  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘  │      │
│                                                          │      │
│                                            ┌─────────────▼────┐ │
│                                            │   Email Agent    │ │
│                                            │                  │ │
│                                            │ • SMTP Send      │ │
│                                            │ • Attachment     │ │
│                                            │ • Template       │ │
│                                            └─────────┬────────┘ │
└──────────────────────────────────────────────────────┼──────────┘
                                                       │
                                                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                      外部服務層                                   │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   OpenAI     │  │  DuckDuckGo  │  │  WeasyPrint  │          │
│  │     API      │  │    Search    │  │   (PDF)      │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  ┌──────────────────────────────────────────────────┐           │
│  │              SMTP Server (Gmail)                  │           │
│  └──────────────────────────────────────────────────┘           │
└─────────────────────────────────────────────────────────────────┘
```

## 詳細執行流程

### 步驟 1: 用戶輸入
```
用戶 → Web/CLI 介面
│
├─ 輸入搜尋查詢: "新加坡金融科技趨勢"
└─ 輸入收件人: "user@example.com"
```

### 步驟 2: 工作流程啟動
```
Workflow.execute()
│
├─ 初始化所有 Agents
├─ 驗證輸入參數
└─ 開始執行 4 個步驟
```

### 步驟 3: Research Agent 執行
```
ResearchAgent.search()
│
├─ 構建增強型提示詞
├─ 調用 ChatGPT + DuckDuckGo
├─ 收集 5-10 條新聞
└─ 返回結構化結果
    │
    └─ Output: {
          "status": "success",
          "content": "新聞內容...",
          "sources": [...]
        }
```

### 步驟 4: Analyst Agent 執行
```
AnalystAgent.analyze()
│
├─ 接收搜尋結果
├─ AI 分析與結構化
├─ 生成 Markdown 報告
└─ 添加資料來源
    │
    └─ Output: "# 東南亞金融新聞報告\n..."
```

### 步驟 5: Report Generator 執行
```
ReportGeneratorAgent.generate_pdf()
│
├─ Markdown → HTML 轉換
├─ 應用 CSS 樣式
├─ WeasyPrint 生成 PDF
└─ 儲存到 reports/
    │
    └─ Output: Path("reports/report_20250101.pdf")
```

### 步驟 6: Email Agent 執行
```
EmailAgent.send_report()
│
├─ 構建 HTML 郵件
├─ 附加 PDF 文件
├─ SMTP 連接與認證
└─ 發送郵件
    │
    └─ Output: True (發送成功)
```

### 步驟 7: 完成回報
```
Workflow 返回結果
│
├─ 狀態: success
├─ PDF 路徑
├─ 執行時長
└─ 各步驟狀態
    │
    └─ 用戶收到郵件！
```

## 數據流轉圖

```
[用戶輸入]
    ↓
"新加坡金融科技趨勢"
    ↓
[Research Agent]
    ↓
{
  "results": [
    {
      "title": "新加坡推動數位銀行...",
      "url": "https://...",
      "summary": "..."
    }
  ]
}
    ↓
[Analyst Agent]
    ↓
"# 東南亞金融新聞報告
## 報告摘要
新加坡金融科技持續發展...
### 1. 數位銀行突破
- **來源**: [Bloomberg](https://...)
- **摘要**: ...
"
    ↓
[Report Generator]
    ↓
📄 report_20250101_120000.pdf
    ↓
[Email Agent]
    ↓
📧 發送至: user@example.com
    ↓
[用戶收到報告] ✅
```

## 錯誤處理流程

```
任一 Agent 執行失敗
    ↓
捕獲異常
    ↓
記錄錯誤日誌
    ↓
返回錯誤狀態
    │
    ├─ 顯示友好錯誤訊息
    ├─ 提供錯誤詳情
    └─ 建議解決方案
        ↓
    用戶獲得反饋
```

## 進度追蹤流程

```
執行過程中
    │
    ├─ Step 1: 🔍 正在搜尋...
    │   └─ callback("step1", "搜尋中...")
    │
    ├─ Step 2: 📊 正在分析...
    │   └─ callback("step2", "分析中...")
    │
    ├─ Step 3: 📄 正在生成 PDF...
    │   └─ callback("step3", "生成中...")
    │
    ├─ Step 4: 📧 正在發送郵件...
    │   └─ callback("step4", "發送中...")
    │
    └─ Complete: ✅ 全部完成！
        └─ callback("complete", "成功！")
```

## 配置載入流程

```
系統啟動
    ↓
載入 .env 文件
    ↓
初始化 Config 類
    │
    ├─ OPENAI_API_KEY
    ├─ EMAIL_ADDRESS
    ├─ EMAIL_PASSWORD
    └─ 其他配置
        ↓
驗證必要配置
    │
    ├─ ✅ 配置完整 → 繼續
    └─ ❌ 配置缺失 → 報錯
```

## Agent 初始化流程

```
系統啟動
    ↓
SEANewsWorkflow.__init__()
    │
    ├─ ResearchAgent()
    │   └─ 初始化 OpenAIChat + DuckDuckGoTools
    │
    ├─ AnalystAgent()
    │   └─ 初始化 OpenAIChat
    │
    ├─ ReportGeneratorAgent()
    │   └─ 初始化 WeasyPrint
    │
    └─ EmailAgent()
        └─ 初始化 SMTP 配置
            ↓
        所有 Agents 就緒
```

## 完整執行時序圖

```
時間軸 →
────────────────────────────────────────────────────────────

T0:  用戶點擊「開始搜尋」按鈕
T1:  Workflow 開始執行
T2:  Research Agent 啟動
     └─ ChatGPT API 調用
T15: Research Agent 完成（~13 秒）
T16: Analyst Agent 啟動
     └─ ChatGPT API 調用
T40: Analyst Agent 完成（~24 秒）
T41: Report Generator 啟動
     └─ PDF 生成
T46: Report Generator 完成（~5 秒）
T47: Email Agent 啟動
     └─ SMTP 連接與發送
T49: Email Agent 完成（~2 秒）
T50: Workflow 完成
     └─ 返回結果給用戶

總時長: ~50 秒
```

## 系統互動圖

```
┌─────────┐         ┌──────────┐         ┌─────────────┐
│  用戶   │         │  系統    │         │ 外部服務    │
└────┬────┘         └────┬─────┘         └──────┬──────┘
     │                   │                       │
     │ 1. 輸入查詢       │                       │
     │──────────────────▶│                       │
     │                   │                       │
     │                   │ 2. 調用 OpenAI        │
     │                   │──────────────────────▶│
     │                   │                       │
     │                   │ 3. 返回搜尋結果       │
     │                   │◀──────────────────────│
     │                   │                       │
     │                   │ 4. 生成 PDF           │
     │                   │─┐                     │
     │                   │ │                     │
     │                   │◀┘                     │
     │                   │                       │
     │                   │ 5. 發送郵件           │
     │                   │──────────────────────▶│
     │                   │                       │
     │ 6. 顯示完成       │                       │
     │◀──────────────────│                       │
     │                   │                       │
     │ 7. 收到郵件       │                       │
     │◀──────────────────────────────────────────│
     │                   │                       │
```

## 部署架構流程

### 本地部署
```
開發機器
    │
    ├─ Python 3.11+
    ├─ UV 虛擬環境
    ├─ Streamlit 服務
    └─ localhost:8501
```

### Docker 部署
```
Docker Host
    │
    ├─ Docker Container
    │   ├─ Python Runtime
    │   ├─ Agno Agents
    │   └─ Streamlit App
    │
    └─ Port 8501 映射
```

### 雲端部署
```
雲端平台 (GCP/AWS/Azure)
    │
    ├─ Container Service
    │   └─ Docker Image
    │       └─ 應用程式
    │
    ├─ Load Balancer
    │   └─ HTTPS 加密
    │
    └─ Auto Scaling
        └─ 依流量調整
```

---

**文件版本**: 1.0  
**最後更新**: 2025-01  
**維護團隊**: Development Team
