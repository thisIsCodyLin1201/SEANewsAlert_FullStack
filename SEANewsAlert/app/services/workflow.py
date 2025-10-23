"""
工作流程服務
封裝現有的新聞搜尋、分析、報告生成和郵件發送流程
"""
import sys
from pathlib import Path

# 確保可以導入專案根目錄的模組
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from agents import ResearchAgent, AnalystAgent, ReportGeneratorAgent, EmailAgent
from typing import Dict, Any
from datetime import datetime
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from config import Config
from .progress import task_manager, TaskStatus
import json
import traceback


class NewsReportWorkflow:
    """新聞報告工作流程"""
    
    def __init__(self):
        """初始化工作流程和所有 Agents"""
        print("🚀 初始化東南亞金融新聞搜尋系統...")
        
        self.research_agent = ResearchAgent()
        self.analyst_agent = AnalystAgent()
        self.report_agent = ReportGeneratorAgent()
        self.email_agent = EmailAgent()
        
        print("✅ 所有 Agents 初始化完成")
    
    def _parse_prompt(self, task_id: str, user_prompt: str) -> dict:
        """使用 LLM 解析用戶 prompt，提取關鍵字、時間指令和數量指令。"""
        try:
            task_manager.set_progress(task_id, 15, "prompt_parsing", "🧠 正在解析您的需求...")
            
            # 使用 Agent 包裝的 OpenAIChat
            parser_agent = Agent(
                name="需求解析專家",
                model=OpenAIChat(
                    id=Config.OPENAI_MODEL,
                    api_key=Config.OPENAI_API_KEY
                ),
                description="專門解析使用者需求的專家",
                instructions=[
                    "你是一個任務解析專家",
                    "從使用者的需求中提取關鍵資訊",
                    "你必須只回傳純 JSON 格式，不要有任何其他文字或解釋",
                    "不要使用 markdown 代碼塊，直接回傳 JSON 物件"
                ],
                markdown=False
            )
            
            prompt = f"""
            請從以下使用者需求中，提取出四個關鍵資訊：
            1. 'keywords': 核心的搜尋主題
            2. 'time_instruction': 時間範圍指令（如果沒有指定，預設為'最近7天內'）
            3. 'num_instruction': 需要的新聞數量（如果沒有指定，預設為'5-10篇'）
            4. 'language': 新聞來源的語言（如果沒有指定，預設為'English'。支援：'English', 'Chinese', 'Vietnamese', 'Thai', 'Malay', 'Indonesian'）

            使用者需求：{user_prompt}
            
            只回傳 JSON 格式，範例：
            {{"keywords": "主題", "time_instruction": "時間", "num_instruction": "數量", "language": "English"}}
            """
            
            response = parser_agent.run(prompt)
            
            if response and response.content:
                content = response.content.strip()
                
                # 嘗試提取 JSON（處理可能的 markdown 代碼塊）
                if '```json' in content:
                    import re
                    json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                    if json_match:
                        content = json_match.group(1)
                elif '```' in content:
                    import re
                    json_match = re.search(r'```\s*(.*?)\s*```', content, re.DOTALL)
                    if json_match:
                        content = json_match.group(1)
                
                # 解析 JSON
                parsed_data = json.loads(content)
                keywords = parsed_data.get("keywords", user_prompt)
                time_instruction = parsed_data.get("time_instruction", "最近7天內")
                num_instruction = parsed_data.get("num_instruction", "5-10篇")
                language = parsed_data.get("language", "English")
                
                task_manager.set_progress(
                    task_id, 20, "prompt_parsing",
                    f"✅ 需求解析完成：主題='{keywords}', 時間='{time_instruction}', 數量='{num_instruction}', 語言='{language}'"
                )
                
                return {
                    "keywords": keywords,
                    "time_instruction": time_instruction,
                    "num_instruction": num_instruction,
                    "language": language
                }

        except Exception as e:
            task_manager.set_progress(
                task_id, 20, "prompt_parsing",
                f"⚠️ 需求解析失敗，將使用原始輸入進行搜尋。錯誤: {str(e)}"
            )
        
        # 如果解析失敗，回退到原始輸入
        return {
            "keywords": user_prompt,
            "time_instruction": "最近7天內",
            "num_instruction": "5-10篇",
            "language": "English"
        }
    
    async def execute_task(self, task_id: str):
        """
        執行完整的新聞報告生成流程（背景任務）
        
        Args:
            task_id: 任務 ID
        """
        try:
            # 獲取任務詳情
            task_details = task_manager.get_task_details(task_id)
            if not task_details:
                raise Exception(f"任務不存在: {task_id}")
            
            user_prompt = task_details["user_prompt"]
            email = task_details["email"]
            language = task_details.get("language", "English")
            time_range = task_details.get("time_range", "最近 7 天內")
            count_hint = task_details.get("count_hint", "5-10篇")
            
            # 設置為執行中
            task_manager.set_running(task_id, 10)
            
            # ============ 步驟 1: 解析 Prompt & Web Search ============
            task_manager.set_progress(task_id, 15, "parsing", "🧠 正在解析您的研究需求...")
            
            # 解析用戶 Prompt
            parsed_prompt = self._parse_prompt(task_id, user_prompt)
            
            task_manager.set_progress(
                task_id, 25, "searching",
                f"🔍 正在搜尋關於「{parsed_prompt['keywords']}」的新聞({parsed_prompt['time_instruction']}, {parsed_prompt['num_instruction']}, {parsed_prompt['language']})..."
            )
            
            search_results = self.research_agent.search(
                query=parsed_prompt['keywords'],
                time_instruction=parsed_prompt['time_instruction'],
                num_instruction=parsed_prompt['num_instruction'],
                language=parsed_prompt['language']
            )
            
            if search_results.get("status") == "error":
                raise Exception(f"搜尋失敗: {search_results.get('error')}")
            
            task_manager.set_progress(task_id, 40, "searching", "✅ 新聞搜尋完成")
            
            # ============ 步驟 2: 資訊結構化 ============
            task_manager.set_progress(task_id, 45, "analyzing", "📊 正在分析並結構化資訊...")
            
            markdown_report, structured_news = self.analyst_agent.analyze(search_results)
            
            task_manager.set_progress(
                task_id, 60, "analyzing",
                f"✅ 資訊分析完成（共 {len(structured_news)} 則新聞）"
            )
            
            # ============ 步驟 3: 生成 PDF 和 Excel 報告 ============
            task_manager.set_progress(task_id, 65, "generating_report", "📄 正在生成 PDF 和 Excel 報告...")
            
            # 生成 PDF
            pdf_path = self.report_agent.generate_pdf(markdown_report)
            
            # 生成 Excel（使用相同的基礎文件名）
            excel_filename = pdf_path.stem + '.xlsx'
            excel_path = self.report_agent.generate_excel(structured_news, excel_filename)
            
            task_manager.set_progress(
                task_id, 80, "generating_report",
                f"✅ 報告生成完成: {pdf_path.name} 和 {excel_path.name}"
            )
            
            # ============ 步驟 4: 發送郵件 ============
            task_manager.set_progress(task_id, 85, "sending_email", "📧 正在發送郵件（含 PDF 和 Excel 附件）...")
            
            email_success = self.email_agent.send_report(
                recipients=email,
                pdf_path=pdf_path,
                excel_path=excel_path
            )
            
            if not email_success:
                raise Exception("郵件發送失敗")
            
            task_manager.set_progress(task_id, 95, "sending_email", "✅ 郵件發送完成（含 PDF 和 Excel）")
            
            # ============ 完成 ============
            task_manager.set_succeeded(
                task_id,
                pdf_path=str(pdf_path),
                xlsx_path=str(excel_path)
            )
            
            task_manager.set_progress(
                task_id, 100, "complete",
                f"🎉 所有步驟完成！報告已發送至: {email}（PDF + Excel）"
            )
            
            print(f"✅ 任務 {task_id} 執行成功")
            
        except Exception as e:
            error_msg = f"工作流程執行失敗: {str(e)}"
            print(f"❌ {error_msg}")
            print(traceback.format_exc())
            
            task_manager.set_failed(task_id, error_msg)


# 全域工作流程實例
workflow = NewsReportWorkflow()
