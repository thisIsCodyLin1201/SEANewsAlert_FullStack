import React, { useEffect, useState } from "react";
import "./Dashboard.css";

type TaskStatus = "idle" | "creating" | "running" | "completed" | "failed";

interface TaskResponse {
  task_id: string;
  message: string;
}

interface TaskProgress {
  task_id: string;
  status: string;
  progress: number;
  error: string | null;
  current_step?: string;
  step_message?: string;
  artifacts?: {
    report_pdf_path?: string;
    email_sent_to?: string;
  };
}

const NewsReportForm: React.FC = () => {
  const [userPrompt, setUserPrompt] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [taskId, setTaskId] = useState<string | null>(null);
  const [progress, setProgress] = useState<TaskProgress | null>(null);
  const [status, setStatus] = useState<TaskStatus>("idle");
  const [errorMessage, setErrorMessage] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  const BASE_URL = "http://localhost:8000/api/tasks";

  const validateEmail = (email: string) =>
    /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.toLowerCase());

  const handleGenerateReport = async () => {
    console.log("🚀 開始生成報告...");
    setErrorMessage("");
    setSuccessMessage("");

    if (!userPrompt.trim()) {
      setErrorMessage("請輸入搜尋需求");
      return;
    }
    if (!userEmail.trim()) {
      setErrorMessage("請輸入電子郵件");
      return;
    }
    if (!validateEmail(userEmail)) {
      setErrorMessage("請輸入正確的電子郵件格式");
      return;
    }

    setStatus("creating");
    setProgress(null);
    setTaskId(null);

    console.log("📡 準備發送 API 請求到:", `${BASE_URL}/news-report`);

    try {
      const response = await fetch(`${BASE_URL}/news-report`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user_prompt: userPrompt,
          email: userEmail,
          language: "Chinese",
          time_range: "最近7天內",
          count_hint: "5-10篇",
        }),
      });

      console.log("📡 API 回應狀態:", response.status);

      if (!response.ok) {
        const err = await response.json();
        console.error("❌ API 錯誤:", err);
        if (err.detail?.[0]?.msg?.includes("quota")) {
          throw new Error("API 配額已用完，請稍後再試");
        }
        throw new Error("系統忙碌，請稍後再試");
      }

      const data: TaskResponse = await response.json();
      console.log("✅ 任務建立成功，Task ID:", data.task_id);
      console.log("✅ 完整回應資料:", data);
      setTaskId(data.task_id);
      setStatus("running");
      console.log("🔄 已設定 taskId，useEffect 應該會開始輪詢");
    } catch (error: unknown) {
      console.error("❌ 建立任務失敗:", error);
      setErrorMessage(
        error instanceof Error ? error.message : "建立任務時發生錯誤"
      );
      setStatus("idle");
    }
  };

  useEffect(() => {
    if (!taskId) return;

    console.log("🔄 開始輪詢任務進度，Task ID:", taskId);

    const interval = setInterval(async () => {
      try {
        const res = await fetch(`${BASE_URL}/${taskId}`);
        if (!res.ok) throw new Error("查詢任務失敗");
        
        const data: TaskProgress = await res.json();
        console.log("📊 後端回傳的進度資料:", JSON.stringify(data, null, 2));
        
        setProgress(data);

        // ✅ 成功狀態
        if (data.status === "succeeded") {
          console.log("✅ 任務成功完成");
          clearInterval(interval);
          setStatus("idle");
          setSuccessMessage(
            `🎉 所有步驟完成！報告已發送至: ${
              data.artifacts?.email_sent_to || userEmail
            }`
          );
          setTaskId(null);
          setProgress(null);
        } 
        // ❌ 失敗狀態（顯示實際錯誤）
        else if (data.status === "failed") {
          console.log("❌ 任務失敗:", data.error);
          clearInterval(interval);
          setStatus("idle");
          setErrorMessage(data.error || "任務執行失敗，請稍後再試");
          setTaskId(null);
          setProgress(null);
        }
        // ℹ️ 其他狀態（pending、running 等）繼續輪詢
        else {
          console.log(`ℹ️ 任務進行中 - 狀態: ${data.status}, 進度: ${data.progress}%, 步驟: ${data.current_step}`);
        }
      } catch (err) {
        console.error("❌ 查詢任務時發生錯誤:", err);
        clearInterval(interval);
        setStatus("idle");
        setErrorMessage("無法連接到伺服器，請檢查後端是否啟動");
        setTaskId(null);
        setProgress(null);
      }
    }, 2000);

    return () => {
      console.log("🛑 停止輪詢");
      clearInterval(interval);
    };
  }, [taskId, userEmail]);

  return (
    <div className="dashboard-container" style={{ fontFamily: "'Source Han Serif SC', '思源宋體', serif" }}>
      <div className="dashboard-header">
        <h1>AI 新聞報告產生器</h1>
        <p>輸入搜尋需求與你的信箱，AI 將生成報告並寄送給你。</p>
      </div>

      <div className="section">
        <h3>搜尋需求</h3>
        <textarea
          value={userPrompt}
          onChange={(e) => setUserPrompt(e.target.value)}
          placeholder={`請詳述你的需求，例如：
請幫我檢查近兩個月的金融科技新聞，大約五篇`}
          className="prompt-input"
        />
      </div>

      <div className="section">
        <h3>收件信箱</h3>
        <input
          type="email"
          placeholder="your.email@example.com"
          value={userEmail}
          onChange={(e) => setUserEmail(e.target.value)}
          className={`email-input ${
            userEmail && !validateEmail(userEmail) ? "input-error" : ""
          }`}
        />
        {userEmail && !validateEmail(userEmail) && (
          <p className="error-message">⚠ 請輸入正確的電子郵件格式</p>
        )}
      </div>

      <div className="generate-section">
        <button
          onClick={handleGenerateReport}
          disabled={status === "creating" || status === "running"}
          className={`action-button ${status === "running" ? "loading" : ""}`}
        >
          {status === "running"
            ? "生成中..."
            : status === "creating"
            ? "建立任務中..."
            : "生成報告"}
        </button>
      </div>

      {/* ✅ Debug 訊息 */}
      <div style={{ margin: "20px 0", padding: "15px", backgroundColor: "#e3f2fd", border: "2px solid #2196F3", borderRadius: "5px" }}>
        <h3 style={{ margin: "0 0 10px 0", color: "#1976D2" }}>🐛 Debug 資訊</h3>
        <p><strong>taskId:</strong> {taskId || "null"}</p>
        <p><strong>status:</strong> {status}</p>
        <p><strong>progress 是否存在:</strong> {progress ? "是 ✅" : "否 ❌"}</p>
        {progress && (
          <div>
            <p><strong>progress.status:</strong> {progress.status}</p>
            <p><strong>progress.progress:</strong> {progress.progress}%</p>
            <p><strong>progress.current_step:</strong> {progress.current_step || "無"}</p>
          </div>
        )}
      </div>

      {/* ✅ 進度條 - 強制顯示測試版 */}
      {progress && (
        <div style={{ 
          border: "3px solid red", 
          padding: "20px", 
          margin: "20px 0",
          backgroundColor: "yellow",
          borderRadius: "8px",
          position: "relative",
          zIndex: 9999
        }}>
          <h2 style={{ color: "red", fontSize: "24px" }}>進度區塊 - 如果你看到這個就是有渲染！</h2>
          <p style={{ fontSize: "16px", marginBottom: "10px" }}>
            <strong>⏳ 任務狀態：{progress.status}</strong>
          </p>
          <p style={{ fontSize: "16px", marginBottom: "10px" }}>
            <strong>📈 進度：{progress.progress}%</strong>
          </p>
          <div style={{ 
            backgroundColor: "#e0e0e0", 
            borderRadius: "10px", 
            overflow: "hidden",
            height: "30px",
            marginBottom: "15px",
            border: "2px solid blue"
          }}>
            <div
              style={{ 
                width: `${progress.progress}%`,
                backgroundColor: "#4CAF50",
                height: "100%",
                transition: "width 0.3s ease",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                color: "white",
                fontWeight: "bold",
                fontSize: "14px"
              }}
            >
              {progress.progress}%
            </div>
          </div>
          {progress.current_step && (
            <p style={{ fontSize: "14px", marginBottom: "10px", color: "#000", backgroundColor: "white", padding: "10px" }}>
              <strong>🔍 步驟：{progress.current_step}</strong>
            </p>
          )}
          {progress.step_message && (
            <div style={{ 
              backgroundColor: "#fff", 
              padding: "15px", 
              borderRadius: "5px",
              border: "2px solid green",
              marginTop: "10px",
              whiteSpace: "pre-wrap",
              fontFamily: "monospace",
              fontSize: "13px",
              lineHeight: "1.6",
              maxHeight: "300px",
              overflowY: "auto",
              color: "black"
            }}>
              <strong>訊息內容：</strong><br/>
              {progress.step_message}
            </div>
          )}
          <hr/>
          <pre style={{ fontSize: "11px", backgroundColor: "white", padding: "10px", border: "1px solid black" }}>
            {JSON.stringify(progress, null, 2)}
          </pre>
        </div>
      )}

      {errorMessage && <div className="error-message">{errorMessage}</div>}
      {successMessage && <div className="success-message">{successMessage}</div>}

      {progress?.artifacts?.report_pdf_path && (
        <div className="report-result">
          <a
            href={`http://localhost:8000${progress.artifacts.report_pdf_path}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            📎 點此下載報告 PDF
          </a>
        </div>
      )}
    </div>
  );
};

export default NewsReportForm;
