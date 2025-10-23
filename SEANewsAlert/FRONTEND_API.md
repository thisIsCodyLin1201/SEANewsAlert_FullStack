# 📘 東南亞金融新聞搜尋系統 - 前端 API 文件

**版本**: 2.0.0  
**基礎 URL**: `http://127.0.0.1:8000`

---

## 🎯 概述

前端只需要整合 **2 個 API**：
1. **POST** - 創建新聞報告任務
2. **GET** - 查詢任務狀態（輪詢用）

系統會在背景執行任務，前端透過輪詢來顯示進度。

---

## 🛣️ API 端點

### 1️⃣ 創建新聞報告任務

創建一個新的新聞搜尋任務，立即返回任務 ID。

#### 請求

```http
POST /api/tasks/news-report
Content-Type: application/json

{
  "user_prompt": "搜尋最近一週關於新加坡金融科技的英文新聞，大約 8-10 篇",
  "email": "user@example.com"
}
```

#### 參數

| 欄位 | 類型 | 必填 | 說明 |
|------|------|------|------|
| `user_prompt` | `string` | ✅ | 使用者的搜尋需求 |
| `email` | `string` | ✅ | 收件者信箱（必須是有效 email 格式） |

#### 響應 (201 Created)

```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "message": "Task started"
}
```

#### 錯誤響應

**422 Unprocessable Entity** - 參數驗證失敗
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

**500 Internal Server Error** - 伺服器錯誤
```json
{
  "detail": "Failed to create task: <error_message>"
}
```

---

### 2️⃣ 查詢任務狀態

查詢任務的執行進度和狀態，用於輪詢。

#### 請求

```http
GET /api/tasks/{task_id}
```

#### 響應 (200 OK)

**執行中：**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "running",
  "progress": 45,
  "error": null,
  "artifacts": {
    "pdf_path": null,
    "xlsx_path": null
  },
  "current_step": "analyzing",
  "step_message": "📊 正在分析並結構化資訊..."
}
```

**完成：**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "succeeded",
  "progress": 100,
  "error": null,
  "artifacts": {
    "pdf_path": "C:\\reports\\報告_20250116_123456.pdf",
    "xlsx_path": "C:\\reports\\報告_20250116_123456.xlsx"
  },
  "current_step": "complete",
  "step_message": "🎉 所有步驟完成！報告已發送至: user@example.com"
}
```

**失敗：**
```json
{
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "status": "failed",
  "progress": 25,
  "error": "OpenAI API 連線失敗",
  "artifacts": {
    "pdf_path": null,
    "xlsx_path": null
  },
  "current_step": "searching",
  "step_message": "❌ 工作流程執行失敗"
}
```

#### 錯誤響應

**404 Not Found** - 任務不存在
```json
{
  "detail": "Task not found"
}
```

---

## 📊 資料模型

### TaskStatus (任務狀態)

| 值 | 說明 |
|------|------|
| `queued` | 已排隊，等待執行 |
| `running` | 執行中 |
| `succeeded` | 成功完成 |
| `failed` | 執行失敗 |

### 響應欄位說明

| 欄位 | 類型 | 說明 |
|------|------|------|
| `task_id` | `string` | 任務 ID（UUID） |
| `status` | `string` | 任務狀態 |
| `progress` | `number` | 進度 (0-100) |
| `error` | `string \| null` | 錯誤訊息（失敗時才有） |
| `artifacts.pdf_path` | `string \| null` | PDF 檔案路徑（完成時才有） |
| `artifacts.xlsx_path` | `string \| null` | Excel 檔案路徑（完成時才有） |
| `current_step` | `string \| null` | 當前步驟 |
| `step_message` | `string \| null` | 步驟說明（給使用者看的訊息） |

---

## 💻 前端實作

### TypeScript 類型定義

```typescript
// 任務狀態
type TaskStatus = 'queued' | 'running' | 'succeeded' | 'failed';

// 創建任務請求
interface CreateTaskRequest {
  user_prompt: string;
  email: string;
}

// 創建任務響應
interface CreateTaskResponse {
  task_id: string;
  message: string;
}

// 任務狀態響應
interface TaskStatusResponse {
  task_id: string;
  status: TaskStatus;
  progress: number;
  error: string | null;
  artifacts: {
    pdf_path: string | null;
    xlsx_path: string | null;
  };
  current_step: string | null;
  step_message: string | null;
}
```

---

### JavaScript 範例

```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';

// 1. 創建任務
async function createTask(userPrompt, email) {
  const response = await fetch(`${API_BASE_URL}/api/tasks/news-report`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      user_prompt: userPrompt,
      email: email
    })
  });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  
  const data = await response.json();
  return data.task_id;
}

// 2. 查詢任務狀態
async function getTaskStatus(taskId) {
  const response = await fetch(`${API_BASE_URL}/api/tasks/${taskId}`);
  
  if (response.status === 404) {
    throw new Error('任務不存在');
  }
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
  
  return await response.json();
}

// 3. 輪詢直到完成
async function pollUntilComplete(taskId, onProgress) {
  return new Promise((resolve, reject) => {
    const intervalId = setInterval(async () => {
      try {
        const status = await getTaskStatus(taskId);
        
        // 回調進度更新
        if (onProgress) {
          onProgress(status);
        }
        
        // 檢查是否完成
        if (status.status === 'succeeded' || status.status === 'failed') {
          clearInterval(intervalId);
          resolve(status);
        }
      } catch (error) {
        clearInterval(intervalId);
        reject(error);
      }
    }, 2000); // 每 2 秒輪詢一次
  });
}

// 使用範例
async function main() {
  try {
    // 創建任務
    const taskId = await createTask(
      '搜尋新加坡金融科技新聞',
      'user@example.com'
    );
    console.log(`任務已創建: ${taskId}`);
    
    // 輪詢並顯示進度
    const result = await pollUntilComplete(taskId, (status) => {
      console.log(`${status.progress}% - ${status.step_message}`);
    });
    
    if (result.status === 'succeeded') {
      console.log('任務完成！');
    } else {
      console.error(`任務失敗: ${result.error}`);
    }
  } catch (error) {
    console.error('錯誤:', error);
  }
}
```

---

### React Hook 範例

```typescript
import { useState, useEffect } from 'react';

interface TaskStatus {
  task_id: string;
  status: 'queued' | 'running' | 'succeeded' | 'failed';
  progress: number;
  error: string | null;
  step_message: string | null;
}

export function useNewsReport() {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<TaskStatus | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // 創建任務
  const createTask = async (userPrompt: string, email: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/tasks/news-report', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_prompt: userPrompt, email })
      });
      
      if (!response.ok) {
        throw new Error('創建任務失敗');
      }
      
      const data = await response.json();
      setTaskId(data.task_id);
    } catch (err) {
      setError(err instanceof Error ? err.message : '未知錯誤');
      setLoading(false);
    }
  };

  // 輪詢任務狀態
  useEffect(() => {
    if (!taskId) return;

    const intervalId = setInterval(async () => {
      try {
        const response = await fetch(`http://127.0.0.1:8000/api/tasks/${taskId}`);
        const data = await response.json();
        setStatus(data);

        if (data.status === 'succeeded' || data.status === 'failed') {
          setLoading(false);
          clearInterval(intervalId);
        }
      } catch (err) {
        setError('獲取狀態失敗');
        setLoading(false);
        clearInterval(intervalId);
      }
    }, 2000);

    return () => clearInterval(intervalId);
  }, [taskId]);

  return { createTask, status, loading, error };
}

// 使用範例
function NewsReportForm() {
  const { createTask, status, loading, error } = useNewsReport();
  const [prompt, setPrompt] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await createTask(prompt, email);
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <textarea
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="搜尋需求..."
          required
        />
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="your.email@example.com"
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? '處理中...' : '開始搜尋'}
        </button>
      </form>

      {status && (
        <div>
          <progress value={status.progress} max={100} />
          <p>{status.step_message}</p>
          
          {status.status === 'succeeded' && (
            <div>✅ 報告已發送至您的郵箱！</div>
          )}
          
          {status.status === 'failed' && (
            <div>❌ 任務失敗: {status.error}</div>
          )}
        </div>
      )}

      {error && <div className="error">{error}</div>}
    </div>
  );
}
```

---

## 🔄 完整流程

```
1. 使用者填寫表單
   ↓
2. 前端呼叫 POST /api/tasks/news-report
   ↓
3. 後端返回 task_id
   ↓
4. 前端開始輪詢 GET /api/tasks/{task_id}（每 2 秒）
   ↓
5. 前端更新進度條和訊息
   ↓
6. 任務完成（status: succeeded/failed）
   ↓
7. 前端停止輪詢，顯示結果
```

---

## 📊 進度階段

| 進度 | 說明 | 預估時間 |
|------|------|----------|
| 0% | 排隊中 | 1-2 秒 |
| 1-24% | 解析需求 | 5-10 秒 |
| 25-49% | 搜尋新聞 | 30-60 秒 |
| 50-74% | 分析資訊 | 30-60 秒 |
| 75-89% | 生成報告 | 20-40 秒 |
| 90-99% | 發送郵件 | 5-10 秒 |
| 100% | 完成 | - |

**總時間**: 約 2-5 分鐘

---

## 🚨 錯誤處理

### HTTP 狀態碼

| 狀態碼 | 意義 | 前端處理 |
|--------|------|----------|
| 201 | 任務創建成功 | 保存 task_id，開始輪詢 |
| 404 | 任務不存在 | 顯示「任務已過期」，提示重新提交 |
| 422 | 參數驗證失敗 | 顯示欄位錯誤訊息 |
| 500 | 伺服器錯誤 | 顯示「系統錯誤，請稍後再試」 |

### 任務狀態處理

```javascript
if (status.status === 'succeeded') {
  // 顯示成功訊息
  showSuccess('報告已發送至您的郵箱！');
}

if (status.status === 'failed') {
  // 顯示錯誤訊息
  showError(`任務失敗: ${status.error}`);
}
```

---

## 💡 建議事項

### 1. 輪詢間隔
```javascript
const POLL_INTERVAL = 2000; // 2 秒（推薦）
```

### 2. 逾時處理
```javascript
const MAX_POLL_TIME = 10 * 60 * 1000; // 10 分鐘
const startTime = Date.now();

const intervalId = setInterval(() => {
  if (Date.now() - startTime > MAX_POLL_TIME) {
    clearInterval(intervalId);
    handleTimeout(); // 顯示逾時錯誤
  }
  // ...
}, 2000);
```

### 3. 使用者體驗
- ✅ 顯示友善的進度訊息（使用 `step_message`）
- ✅ 提交時禁用按鈕，防止重複提交
- ✅ 顯示進度條（使用 `progress`）
- ✅ 完成後提供重新搜尋選項

---

## 🛠️ 測試工具

### Swagger UI
http://127.0.0.1:8000/docs

可以直接在瀏覽器測試兩個 API。

### 測試前端
http://127.0.0.1:8000/static/index.html

參考現有實作。

### cURL 測試

```bash
# 創建任務
curl -X POST http://127.0.0.1:8000/api/tasks/news-report \
  -H "Content-Type: application/json" \
  -d '{"user_prompt":"測試搜尋","email":"test@example.com"}'

# 查詢狀態
curl http://127.0.0.1:8000/api/tasks/{task_id}
```

---

## ❓ 常見問題

**Q: 為什麼要輪詢而不是 WebSocket？**  
A: 當前版本使用輪詢機制，簡單且穩定。未來版本可能會加入 WebSocket。

**Q: 任務 ID 會過期嗎？**  
A: 會。伺服器重啟後記憶體會清空，所有任務 ID 失效。

**Q: 可以下載報告檔案嗎？**  
A: 目前不行。報告會自動發送到指定 email。

**Q: 可以同時創建多個任務嗎？**  
A: 可以。每個任務使用不同的 task_id。

**Q: 輪詢會造成效能問題嗎？**  
A: 不會。每 2 秒一次的輪詢非常輕量。

---

## 📝 總結

前端只需要實作：
1. ✅ 表單（搜尋需求 + Email）
2. ✅ POST API 創建任務
3. ✅ GET API 輪詢狀態（每 2 秒）
4. ✅ 進度條顯示
5. ✅ 結果顯示（成功/失敗）

就這麼簡單！🎉

---

**文件版本**: 2.0.0  
**最後更新**: 2025-10-16
