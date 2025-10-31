"""
Analyst Agent
負責將搜尋結果結構化並整理成專業報告
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from config import Config
from typing import Dict, Any, List, Tuple
from datetime import datetime
import json
import re


class AnalystAgent:
    """分析代理 - 將原始搜尋結果整理成結構化報告"""
    
    def __init__(self):
        """初始化 Analyst Agent"""
        self.agent = Agent(
            name="金融新聞分析師",
            model=OpenAIChat(
                id=Config.OPENAI_MODEL,
                api_key=Config.OPENAI_API_KEY,
                # max_tokens=4096,  # 增加輸出 token 限制，允許更詳細的報告
            ),
            description="專業的金融新聞分析師，擅長整理和結構化資訊",
            instructions=[
                "你是一位專業的金融分析師，負責整理新聞資訊",
                "將搜尋結果整理成清晰、專業的繁體中文報告",
                "報告結構應包含：標題、摘要、詳細內容、資料來源",
                "使用 Markdown 格式輸出",
                "每條新聞都要附上來源超連結",
                "去除重複和冗餘資訊",
                "按照重要性和時間順序排列",
                "使用專業但易懂的語言",
                "提供詳細且深入的分析，不要過於簡短",
                "每條新聞的摘要應該詳細完整，至少 150-300 字",
                "市場洞察部分應該提供 5-8 點深入的分析"
            ],
            markdown=True,
        )
    
    def analyze(self, search_results: Dict[str, Any]) -> Tuple[str, List[Dict[str, str]]]:
        """
        分析並結構化搜尋結果
        
        Args:
            search_results: 來自 Research Agent 的搜尋結果
            
        Returns:
            Tuple[str, List[Dict]]: (Markdown 格式的報告, 結構化新聞列表)
        """
        print("📊 Analyst Agent 開始分析...")
        
        # 提取搜尋內容
        content = search_results.get("content", "")
        query = search_results.get("query", "")
        
        # 構建分析提示
        analysis_prompt = f"""
        請將以下搜尋結果整理成一份專業的繁體中文金融報告。
        
        原始查詢：{query}
        搜尋結果：
        {content}
        
        **重要**：你必須嚴格遵循以下格式，每則新聞都必須包含「來源」、「日期」、「摘要」、「重點分析」四個欄位，且使用 **粗體標記**。
        
        報告格式要求：
        
        # 東南亞金融新聞報告
        
        ## 報告摘要
        [用 2-3 句話總結本報告的核心內容]
        
        ## 搜尋主題
        {query}
        
        ## 報告日期
        {datetime.now().strftime("%Y年%m月%d日")}
        
        ## 新聞詳情
        
        ### 1. [新聞標題翻譯成繁體中文]
        - **來源**：[來源名稱]([網址])
        - **日期**：[YYYY-MM-DD 格式]
        - **摘要**：[新聞的詳細摘要，100-300字，說明新聞的主要內容]
        - **重點分析**：[關鍵資訊的條列式分析，用 1) 2) 3) 編號]
        
        ### 2. [新聞標題翻譯成繁體中文]
        - **來源**：[來源名稱]([網址])
        - **日期**：[YYYY-MM-DD 格式]
        - **摘要**：[新聞的詳細摘要，100-300字，說明新聞的主要內容]
        - **重點分析**：[關鍵資訊的條列式分析，用 1) 2) 3) 編號]
        
        （每則新聞都按照上述格式，不要省略任何欄位）
        
        ## 市場洞察
        [基於以上新聞，提供 3-5 點關鍵洞察]
        
        ## 資料來源
        - [來源1標題](網址)
        - [來源2標題](網址)
        ...
        
        ---
        **報告生成時間**：{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        **系統**：{Config.APP_NAME}
        
        注意事項：
        1. 所有內容必須使用繁體中文
        2. 超連結格式：[標題](網址)
        3. 去除重複資訊
        4. 保持專業且易讀
        5. 如果沒有找到相關新聞，請明確說明
        """
        
        try:
            # 使用 Agent 執行分析
            response = self.agent.run(analysis_prompt)
            
            # 提取 Markdown 內容
            if hasattr(response, 'content'):
                markdown_report = response.content
            else:
                markdown_report = str(response)
            
            # 提取結構化新聞數據
            structured_news = self._extract_structured_data(markdown_report, content, query)
            
            print("✅ Analyst Agent 分析完成")
            return markdown_report, structured_news
            
        except Exception as e:
            print(f"❌ Analyst Agent 分析失敗: {str(e)}")
            # 返回錯誤報告
            error_report = f"""
# 報告生成失敗

## 錯誤資訊
{str(e)}

## 原始搜尋查詢
{query}

請檢查系統設定並重試。
"""
            return error_report, []
    
    def _extract_structured_data(self, markdown_report: str, raw_content: str, query: str) -> List[Dict[str, str]]:
        """
        從 Markdown 報告和原始內容中提取結構化新聞數據
        
        優先從 Markdown 報告中提取，因為其中的標題已經被翻譯成中文
        
        Args:
            markdown_report: Markdown 格式的報告（包含已翻譯的中文標題）
            raw_content: 來自搜尋的原始內容
            query: 搜尋查詢（作為關鍵字）
            
        Returns:
            List[Dict]: 結構化的新聞列表
        """
        structured_news = []
        
        try:
            # 優先從 Markdown 報告中提取（標題已翻譯成中文）
            print("📝 從 Markdown 報告中提取結構化數據（含中文標題）...")
            structured_news = self._extract_from_markdown(markdown_report, query)
            
            # 如果 Markdown 提取失敗，才嘗試從 JSON 解析
            if not structured_news:
                print("⚠️ Markdown 提取失敗，嘗試從 JSON 解析...")
                json_match = re.search(r'```json\s*(\{.*?\})\s*```', raw_content, re.DOTALL)
                if json_match:
                    json_data = json.loads(json_match.group(1))
                    results = json_data.get('results', [])
                    
                    for result in results:
                        # 提取國家資訊（從來源或標題中）
                        country = self._extract_country(
                            result.get('title', ''),
                            result.get('source', ''),
                            result.get('summary', '')
                        )
                        
                        structured_news.append({
                            '新聞標題（中文）': result.get('title', ''),
                            '來源國家': country,
                            '關鍵字': query,
                            '來源網站連結': result.get('url', ''),
                            '發布日期': result.get('date', ''),
                            '來源': result.get('source', '')
                        })
        
        except Exception as e:
            print(f"⚠️ 結構化數據提取失敗: {str(e)}")
            # 作為後備，再次嘗試從 Markdown 中提取
            structured_news = self._extract_from_markdown(markdown_report, query)
        
        if structured_news:
            print(f"✅ 成功提取 {len(structured_news)} 則新聞（標題已為中文）")
        else:
            print("⚠️ 未能提取到任何新聞數據")
        
        return structured_news
    
    def _extract_country(self, title: str, source: str, summary: str) -> str:
        """從文本中提取國家資訊"""
        text = f"{title} {source} {summary}".lower()
        
        countries = {
            'singapore': '新加坡',
            'malaysia': '馬來西亞',
            'thailand': '泰國',
            'indonesia': '印尼',
            'vietnam': '越南',
            'philippines': '菲律賓',
            '新加坡': '新加坡',
            '馬來西亞': '馬來西亞',
            '泰國': '泰國',
            '印尼': '印尼',
            '越南': '越南',
            '菲律賓': '菲律賓'
        }
        
        for key, value in countries.items():
            if key in text:
                return value
        
        return '東南亞'
    
    def _extract_from_markdown(self, markdown_report: str, query: str) -> List[Dict[str, str]]:
        """從 Markdown 報告中提取新聞資訊"""
        structured_news = []
        
        # 使用正則表達式匹配新聞標題和相關資訊
        news_pattern = r'###\s+\d+\.\s+(.*?)\n(.*?)(?=###|\Z)'
        matches = re.findall(news_pattern, markdown_report, re.DOTALL)
        
        for title, content in matches:
            title = title.strip()
            
            # 提取來源和網址
            source_match = re.search(r'\*\*來源\*\*[：:]\s*\[?(.*?)\]?\(?(https?://[^\s\)]+)', content)
            source = ''
            url = ''
            if source_match:
                source = source_match.group(1).strip()
                url = source_match.group(2).strip()
            else:
                # 嘗試另一種格式
                url_match = re.search(r'(https?://[^\s\)]+)', content)
                if url_match:
                    url = url_match.group(1).strip()
            
            # 提取日期 - 改進的日期提取邏輯
            date = ''
            # 首先嘗試匹配 "**日期**：YYYY-MM-DD" 格式
            date_match = re.search(r'\*\*日期\*\*[：:]\s*([^\n*]+)', content)
            if date_match:
                date = date_match.group(1).strip()
            else:
                # 嘗試匹配其他常見日期格式
                # 格式如：2025-10-13, 2025/10/13, 2025.10.13
                date_pattern = r'(\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2})'
                date_match2 = re.search(date_pattern, content)
                if date_match2:
                    date = date_match2.group(1)
                else:
                    # 嘗試中文日期格式：2025年10月13日
                    date_pattern_cn = r'(\d{4}年\d{1,2}月\d{1,2}日)'
                    date_match3 = re.search(date_pattern_cn, content)
                    if date_match3:
                        date = date_match3.group(1)
            
            # 提取摘要 - 改進的正則表達式，支援多行內容
            summary = ''
            # 嘗試匹配摘要內容，直到遇到下一個粗體項目或結束
            summary_match = re.search(r'\*\*摘要\*\*[：:]\s*([^\n]*(?:\n(?!\s*[-\*]\s*\*\*)[^\n]*)*)', content, re.DOTALL)
            if summary_match:
                summary = summary_match.group(1).strip()
            
            # 提取重點分析 - 改進的正則表達式，支援多行和條列式內容
            analysis = ''
            # 嘗試匹配重點分析內容，直到遇到下一個標題或結束
            analysis_match = re.search(r'\*\*重點分析\*\*[：:]\s*([^\n]*(?:\n(?!\s*###|\s*##|\s*[-\*]\s*\*\*(?!.*分析))[^\n]*)*)', content, re.DOTALL)
            if analysis_match:
                analysis = analysis_match.group(1).strip()
            
            # 提取國家
            country = self._extract_country(title, source, content)
            
            structured_news.append({
                '新聞標題（中文）': title,
                '來源國家': country,
                '關鍵字': query,
                '來源網站連結': url,
                '發布日期': date,
                '摘要': summary,
                '重點分析': analysis,
                '來源': source
            })
        
        return structured_news


if __name__ == "__main__":
    # 測試 Analyst Agent
    agent = AnalystAgent()
    
    # 模擬搜尋結果
    mock_results = {
        "status": "success",
        "query": "新加坡股市動態",
        "content": "測試內容：新加坡海峽時報指數上漲..."
    }
    
    report = agent.analyze(mock_results)
    print(report)
