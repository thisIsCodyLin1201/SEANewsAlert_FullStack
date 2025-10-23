"""
工作流程編排
End-to-End 流程：搜尋 -> 分析 -> 生成報告 -> 發送郵件
"""
from agents import ResearchAgent, AnalystAgent, ReportGeneratorAgent, EmailAgent
from typing import Dict, Any, Optional
from pathlib import Path
import json
import re
from datetime import datetime
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from config import Config


class SEANewsWorkflow:
    """東南亞金融新聞工作流程"""
    
    def _parse_prompt(self, user_prompt: str) -> dict:
        """使用 LLM 解析用戶 prompt，提取關鍵字、時間指令和數量指令。"""
        try:
            self._update_progress(None, "prompt_parsing", "🧠 正在解析您的需求...")
            
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
                    # 提取 ```json ... ``` 之間的內容
                    import re
                    json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                    if json_match:
                        content = json_match.group(1)
                elif '```' in content:
                    # 提取 ``` ... ``` 之間的內容
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
                
                self._update_progress(None, "prompt_parsing", f"✅ 需求解析完成：主題='{keywords}', 時間='{time_instruction}', 數量='{num_instruction}', 語言='{language}'")
                
                return {
                    "keywords": keywords,
                    "time_instruction": time_instruction,
                    "num_instruction": num_instruction,
                    "language": language
                }

        except Exception as e:
            self._update_progress(None, "prompt_parsing", f"⚠️ 需求解析失敗，將使用原始輸入進行搜尋。錯誤: {str(e)}")
        
        # 如果解析失敗，回退到原始輸入
        return {
            "keywords": user_prompt,
            "time_instruction": "最近7天內",
            "num_instruction": "5-10篇",
            "language": "English"
        }

    def __init__(self):
        """初始化工作流程和所有 Agents"""
        print("🚀 初始化東南亞金融新聞搜尋系統...")
        
        self.research_agent = ResearchAgent()
        self.analyst_agent = AnalystAgent()
        self.report_agent = ReportGeneratorAgent()
        self.email_agent = EmailAgent()
        
        print("✅ 所有 Agents 初始化完成")
    
    def execute(
        self,
        search_query: str,
        recipient_emails: str,
        callback_func: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        執行完整的工作流程
        
        Args:
            search_query: 搜尋查詢
            recipient_emails: 收件人郵箱（逗號分隔）
            callback_func: 可選的回調函數，用於更新進度
            
        Returns:
            Dict: 包含執行結果的字典
        """
        result = {
            "status": "running",
            "steps": {},
            "errors": [],
            "start_time": datetime.now().isoformat()
        }
        
        try:
            # ============ 步驟 1: 解析 Prompt & Web Search ============
            self._update_progress(callback_func, "step1", "🧠 正在解析您的研究需求...")
            
            # 解析用戶 Prompt
            parsed_prompt = self._parse_prompt(search_query)
            
            self._update_progress(callback_func, "step1", f"🔍 正在搜尋關於「{parsed_prompt['keywords']}」的新聞({parsed_prompt['time_instruction']}, {parsed_prompt['num_instruction']}, {parsed_prompt['language']})...")
            
            search_results = self.research_agent.search(
                query=parsed_prompt['keywords'],
                time_instruction=parsed_prompt['time_instruction'],
                num_instruction=parsed_prompt['num_instruction'],
                language=parsed_prompt['language']
            )
            
            if search_results.get("status") == "error":
                raise Exception(f"搜尋失敗: {search_results.get('error')}")
            
            result["steps"]["search"] = {
                "status": "completed",
                "timestamp": datetime.now().isoformat()
            }
            self._update_progress(callback_func, "step1", "✅ 新聞搜尋完成")
            
            # ============ 步驟 2: 資訊結構化 ============
            self._update_progress(callback_func, "step2", "📊 正在分析並結構化資訊...")
            
            markdown_report, structured_news = self.analyst_agent.analyze(search_results)
            
            result["steps"]["analysis"] = {
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "report_length": len(markdown_report),
                "news_count": len(structured_news)
            }
            self._update_progress(callback_func, "step2", f"✅ 資訊分析完成（共 {len(structured_news)} 則新聞）")
            
            # ============ 步驟 3: 生成 PDF 和 Excel 報告 ============
            self._update_progress(callback_func, "step3", "📄 正在生成 PDF 和 Excel 報告...")
            
            # 生成 PDF
            pdf_path = self.report_agent.generate_pdf(markdown_report)
            
            # 生成 Excel（使用相同的基礎文件名）
            excel_filename = pdf_path.stem + '.xlsx'
            excel_path = self.report_agent.generate_excel(structured_news, excel_filename)
            
            result["steps"]["report_generation"] = {
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "pdf_path": str(pdf_path),
                "pdf_size": pdf_path.stat().st_size,
                "excel_path": str(excel_path),
                "excel_size": excel_path.stat().st_size
            }
            self._update_progress(callback_func, "step3", f"✅ 報告生成完成: {pdf_path.name} 和 {excel_path.name}")
            
            # ============ 步驟 4: 發送郵件 ============
            self._update_progress(callback_func, "step4", "📧 正在發送郵件（含 PDF 和 Excel 附件）...")
            
            email_success = self.email_agent.send_report(
                recipients=recipient_emails,
                pdf_path=pdf_path,
                excel_path=excel_path
            )
            
            if not email_success:
                raise Exception("郵件發送失敗")
            
            result["steps"]["email"] = {
                "status": "completed",
                "timestamp": datetime.now().isoformat(),
                "recipients": recipient_emails,
                "attachments": [str(pdf_path), str(excel_path)]
            }
            self._update_progress(callback_func, "step4", "✅ 郵件發送完成（含 PDF 和 Excel）")
            
            # ============ 完成 ============
            result["status"] = "success"
            result["end_time"] = datetime.now().isoformat()
            result["pdf_path"] = str(pdf_path)
            result["excel_path"] = str(excel_path)
            
            self._update_progress(
                callback_func, 
                "complete", 
                f"🎉 所有步驟完成！報告已發送至: {recipient_emails}（PDF + Excel）"
            )
            
            return result
            
        except Exception as e:
            error_msg = f"工作流程執行失敗: {str(e)}"
            print(f"❌ {error_msg}")
            
            result["status"] = "error"
            result["error"] = str(e)
            result["end_time"] = datetime.now().isoformat()
            result["errors"].append(error_msg)
            
            self._update_progress(callback_func, "error", f"❌ {error_msg}")
            
            return result
    
    def _update_progress(
        self,
        callback_func: Optional[callable],
        step: str,
        message: str
    ):
        """更新進度（內部方法）"""
        print(message)
        if callback_func:
            callback_func(step, message)
    
    def validate_agents(self) -> Dict[str, bool]:
        """驗證所有 Agents 是否正常運作"""
        validation_results = {
            "research_agent": False,
            "email_agent": False,
        }
        
        print("🔍 驗證 Agents...")
        
        try:
            validation_results["research_agent"] = self.research_agent.test_connection()
        except:
            pass
        
        try:
            validation_results["email_agent"] = self.email_agent.test_connection()
        except:
            pass
        
        all_valid = all(validation_results.values())
        
        if all_valid:
            print("✅ 所有 Agents 驗證通過")
        else:
            print("⚠️  部分 Agents 驗證失敗")
            for agent, status in validation_results.items():
                print(f"  - {agent}: {'✅' if status else '❌'}")
        
        return validation_results


if __name__ == "__main__":
    # 測試工作流程
    workflow = SEANewsWorkflow()
    
    # 驗證 Agents
    workflow.validate_agents()
    
    # 測試執行（請替換為實際的郵箱）
    # result = workflow.execute(
    #     search_query="新加坡金融科技發展趨勢",
    #     recipient_emails="test@example.com"
    # )
    # print(json.dumps(result, ensure_ascii=False, indent=2))