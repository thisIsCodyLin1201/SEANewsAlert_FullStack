"""
任務路由
處理新聞報告任務的 API 端點
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from ..services.progress import task_manager
from ..services.workflow import workflow

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


class NewsReportRequest(BaseModel):
    """新聞報告請求模型"""
    user_prompt: str = Field(..., description="使用者輸入的搜尋需求", min_length=1)
    email: EmailStr = Field(..., description="收件者郵箱")
    language: str = Field(default="English", description="新聞語言")
    time_range: str = Field(default="最近 7 天內", description="時間範圍指示")
    count_hint: str = Field(default="5-10篇", description="數量提示")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_prompt": "新加坡金融科技發展趨勢",
                "email": "user@example.com",
                "language": "English",
                "time_range": "最近 7 天內",
                "count_hint": "5-10篇"
            }
        }


class TaskResponse(BaseModel):
    """任務創建響應"""
    task_id: str
    message: str


class TaskStatusResponse(BaseModel):
    """任務狀態響應"""
    task_id: str
    status: str
    progress: int
    error: Optional[str] = None
    artifacts: dict
    current_step: Optional[str] = None
    step_message: Optional[str] = None


@router.post("/news-report", response_model=TaskResponse, status_code=201)
async def create_news_report_task(
    request: NewsReportRequest,
    background_tasks: BackgroundTasks
):
    """
    創建新聞報告任務
    
    - **user_prompt**: 使用者輸入的搜尋需求（必填）
    - **email**: 收件者郵箱（必填）
    - **language**: 新聞語言（選填，預設 'English'）
    - **time_range**: 時間範圍（選填，預設 '最近 7 天內'）
    - **count_hint**: 數量提示（選填，預設 '5-10篇'）
    """
    try:
        # 創建任務
        task_id = task_manager.create_task(
            user_prompt=request.user_prompt,
            email=request.email,
            language=request.language,
            time_range=request.time_range,
            count_hint=request.count_hint
        )
        
        # 加入背景任務
        background_tasks.add_task(workflow.execute_task, task_id)
        
        return TaskResponse(
            task_id=task_id,
            message="Task started"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@router.get("/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str):
    """
    獲取任務狀態
    
    - **task_id**: 任務 ID
    """
    task = task_manager.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskStatusResponse(**task)
