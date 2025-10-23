"""
任務進度管理服務
使用內存字典儲存任務狀態
"""
from typing import Dict, Optional, Any
from datetime import datetime
from enum import Enum
import uuid


class TaskStatus(str, Enum):
    """任務狀態"""
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class TaskProgress:
    """任務進度管理"""
    
    def __init__(self):
        """初始化任務進度管理器"""
        self._tasks: Dict[str, Dict[str, Any]] = {}
    
    def create_task(self, user_prompt: str, email: str, language: str = "English", 
                   time_range: str = "最近 7 天內", count_hint: str = "5-10篇") -> str:
        """
        創建新任務
        
        Args:
            user_prompt: 使用者輸入的搜尋需求
            email: 收件者郵箱
            language: 新聞語言
            time_range: 時間範圍
            count_hint: 數量提示
            
        Returns:
            str: 任務 ID
        """
        task_id = str(uuid.uuid4())
        
        self._tasks[task_id] = {
            "task_id": task_id,
            "status": TaskStatus.QUEUED,
            "progress": 0,
            "error": None,
            "artifacts": {
                "pdf_path": None,
                "xlsx_path": None
            },
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "user_prompt": user_prompt,
            "email": email,
            "language": language,
            "time_range": time_range,
            "count_hint": count_hint,
            "current_step": None,
            "step_message": None
        }
        
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        獲取任務狀態
        
        Args:
            task_id: 任務 ID
            
        Returns:
            Optional[Dict]: 任務狀態字典，若不存在則返回 None
        """
        task = self._tasks.get(task_id)
        if task:
            # 返回用於 API 的簡化版本
            return {
                "task_id": task["task_id"],
                "status": task["status"],
                "progress": task["progress"],
                "error": task["error"],
                "artifacts": task["artifacts"],
                "current_step": task.get("current_step"),
                "step_message": task.get("step_message")
            }
        return None
    
    def update_task(self, task_id: str, **kwargs):
        """
        更新任務狀態
        
        Args:
            task_id: 任務 ID
            **kwargs: 要更新的欄位
        """
        if task_id in self._tasks:
            self._tasks[task_id].update(kwargs)
            self._tasks[task_id]["updated_at"] = datetime.now().isoformat()
    
    def set_running(self, task_id: str, progress: int = 10):
        """設置任務為執行中"""
        self.update_task(task_id, status=TaskStatus.RUNNING, progress=progress)
    
    def set_progress(self, task_id: str, progress: int, step: str = None, message: str = None):
        """更新任務進度"""
        update_data = {"progress": progress}
        if step:
            update_data["current_step"] = step
        if message:
            update_data["step_message"] = message
        self.update_task(task_id, **update_data)
    
    def set_succeeded(self, task_id: str, pdf_path: str = None, xlsx_path: str = None):
        """設置任務成功完成"""
        artifacts = {}
        if pdf_path:
            artifacts["pdf_path"] = pdf_path
        if xlsx_path:
            artifacts["xlsx_path"] = xlsx_path
        
        self.update_task(
            task_id,
            status=TaskStatus.SUCCEEDED,
            progress=100,
            artifacts=artifacts
        )
    
    def set_failed(self, task_id: str, error: str):
        """設置任務失敗"""
        self.update_task(
            task_id,
            status=TaskStatus.FAILED,
            error=error
        )
    
    def get_task_details(self, task_id: str) -> Optional[Dict[str, Any]]:
        """獲取完整任務詳情（包含內部資訊）"""
        return self._tasks.get(task_id)


# 全域任務管理器實例
task_manager = TaskProgress()
