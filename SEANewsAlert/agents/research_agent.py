"""
Research Agent
負責使用 ChatGPT 進行深度網路搜尋
"""
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from config import Config
import json
from typing import Dict, Any


class ResearchAgent:
    """研究代理 - 執行深度網路搜尋"""
    
    # 指定的18個可信新聞來源網站
    TRUSTED_NEWS_SOURCES = [
        {"name": "VietJo", "domain": "viet-jo.com", "region": "Vietnam"},
        {"name": "Cafef", "domain": "cafef.vn", "region": "Vietnam"},
        {"name": "VNExpress", "domain": "vnexpress.net", "region": "Vietnam"},
        {"name": "Vietnam Finance", "domain": "vietnamfinance.vn", "region": "Vietnam"},
        {"name": "Vietnam Investment Review", "domain": "vir.com.vn", "region": "Vietnam"},
        {"name": "Vietnambiz", "domain": "vietnambiz.vn", "region": "Vietnam"},
        {"name": "Tap Chi Tai chinh", "domain": "tapchikinhtetaichinh.vn", "region": "Vietnam"},
        {"name": "Bangkok Post", "domain": "bangkokpost.com", "region": "Thailand"},
        {"name": "Techsauce", "domain": "techsauce.co", "region": "Thailand"},
        {"name": "Fintech Singapore", "domain": "fintechnews.sg", "region": "Singapore"},
        {"name": "Fintech Philippines", "domain": "fintechnews.ph", "region": "Philippines"},
        {"name": "Khmer Times", "domain": "khmertimeskh.com", "region": "Cambodia"},
        {"name": "柬中時報", "domain": "cc-times.com", "region": "Cambodia"},
        {"name": "The Phnom Penh Post", "domain": "phnompenhpost.com", "region": "Cambodia"},
        {"name": "Deal Street Asia", "domain": "dealstreetasia.com", "region": "Southeast Asia"},
        {"name": "Tech in Asia", "domain": "techinasia.com", "region": "Southeast Asia"},
        {"name": "Nikkei Asia", "domain": "asia.nikkei.com", "region": "Southeast Asia"},
        {"name": "Heaptalk", "domain": "heaptalk.com", "region": "Southeast Asia"},
    ]
    
    def __init__(self):
        """初始化 Research Agent"""
        # 生成可信來源列表文字
        sources_list = "\n".join([
            f"  - {src['name']} (site:{src['domain']}) - {src['region']}" 
            for src in self.TRUSTED_NEWS_SOURCES
        ])
        
        # 生成域名列表用於驗證
        allowed_domains = ", ".join([src['domain'] for src in self.TRUSTED_NEWS_SOURCES])
        
        # 確保使用一致的 OpenAI 端點
        self.agent = Agent(
            name="東南亞金融新聞研究員",
            model=OpenAIChat(
                id=Config.OPENAI_MODEL,
                api_key=Config.OPENAI_API_KEY,
                # max_tokens=2048,
            ),
            tools=[DuckDuckGoTools()],
            description="專門搜尋和分析東南亞金融市場新聞的研究員",
            instructions=[
                "你是一位專業的金融新聞研究員，專注於東南亞市場",
                "使用搜尋工具查找最新、最相關的金融新聞",
                f"**重要限制**: 你必須只從以下18個指定的可信新聞來源網站搜尋新聞：\n{sources_list}",
                f"**搜尋技巧**: 使用 DuckDuckGo 的 site: 語法來限制搜尋範圍，例如：'site:viet-jo.com 金融科技'",
                f"**域名驗證**: 確保所有新聞 URL 的域名必須是以下之一：{allowed_domains}",
                "**多樣性建議**: 建議對多個不同網站進行搜尋，盡量使用 3-4 個或以上不同來源，但優先確保新聞質量和相關性",
                "**分區域搜尋策略**: 可以對越南、泰國、新加坡、菲律賓、柬埔寨等區域的網站分別進行搜尋",
                "搜尋時優先關注：新加坡、馬來西亞、泰國、印尼、越南、菲律賓、柬埔寨等國家",
                "關注主題包括：股市、匯率、經濟政策、投資趨勢、企業動態、金融科技",
                "收集至少 5-10 條高質量新聞資訊",
                "記錄每條新聞的完整來源網址",
                "以 JSON 格式整理結果",
                "**最終驗證**: 輸出前必須再次驗證所有 URL 都來自指定的18個可信網站，且來源多樣化"
            ],
            markdown=True,
        )
    
    def search(self, query: str, time_instruction: str = "最近 7 天內", num_instruction: str = "5-10篇", language: str = "English") -> Dict[str, Any]:
        """
        執行搜尋
        
        Args:
            query: 用戶的搜尋查詢
            time_instruction: 時間範圍指令 (例如: "最近一個月內")
            num_instruction: 新聞數量指令 (例如: "約15篇")
            language: 新聞來源語言 (例如: "English", "Chinese", "Vietnamese", "Thai", "Malay", "Indonesian")
            
        Returns:
            Dict: 包含搜尋結果和來源的字典
        """
        print(f"🔍 Research Agent 開始搜尋: {query} ({time_instruction}, {num_instruction}, 語言: {language})")
        
        # 建立語言相關的搜尋關鍵字
        language_keywords = {
            "English": "in English",
            "Chinese": "中文 OR 華語 OR Chinese",
            "Vietnamese": "tiếng Việt OR Vietnamese",
            "Thai": "ภาษาไทย OR Thai",
            "Malay": "Bahasa Melayu OR Malay",
            "Indonesian": "Bahasa Indonesia OR Indonesian"
        }
        
        language_hint = language_keywords.get(language, "in English")
        
        # 生成可信來源列表
        sources_list = "\n".join([
            f"  - {src['name']} (site:{src['domain']}) - {src['region']}" 
            for src in self.TRUSTED_NEWS_SOURCES
        ])
        
        # 生成 site: 搜尋字串組合（用於建議搜尋範例）
        site_examples = [
            f"site:{src['domain']}" 
            for src in self.TRUSTED_NEWS_SOURCES[:5]  # 只取前5個作為範例
        ]
        site_search_example = " OR ".join(site_examples)
        
        # 生成域名列表用於驗證
        allowed_domains = [src['domain'] for src in self.TRUSTED_NEWS_SOURCES]
        allowed_domains_str = ", ".join(allowed_domains)
        
        # 強化搜尋提示詞，使用 site: 語法限制來源
        enhanced_query = f"""
        請扮演一位頂尖的金融研究員，深入搜尋關於「{query}」的東南亞金融新聞。

        **核心任務指令:**
        1.  **搜尋範圍**: 嚴格鎖定東南亞國家（新加坡、馬來西亞、泰國、印尼、越南、菲律賓、柬埔寨）。
        2.  **時間要求**: 嚴格篩選在 **{time_instruction}** 內發布的新聞。
        3.  **數量要求**: 你的目標是找到並提供 **{num_instruction}** 的高品質新聞。你必須盡力達成這個數量目標。
        4.  **語言要求**: 請優先搜尋 **{language}** 語言的新聞來源。在搜尋時加上關鍵字：{language_hint}
        
        5.  **來源限制（非常重要）**: 你**必須只**從以下18個指定的可信新聞網站搜尋新聞：

{sources_list}

        6.  **搜尋技巧 - 強制多樣性策略（非常重要）**:
            
            ⚠️ **必須遵守**: 為了確保新聞來源的多樣性，你**必須**對多個不同網站進行**獨立搜尋**。
            
            **推薦策略 - 分區域獨立搜尋**:
            
            a) 🇻🇳 **越南區域** (至少搜尋 2-3 個網站):
               - "site:viet-jo.com {query}"
               - "site:vnexpress.net {query}"
               - "site:cafef.vn {query}"
               - "site:vietnamfinance.vn {query}"
            
            b) 🇹🇭 **泰國區域** (至少搜尋 1-2 個網站):
               - "site:bangkokpost.com {query}"
               - "site:techsauce.co {query}"
            
            c) 🇸🇬 **新加坡/區域媒體** (至少搜尋 2-3 個網站):
               - "site:fintechnews.sg {query}"
               - "site:techinasia.com {query}"
               - "site:dealstreetasia.com {query}"
               - "site:asia.nikkei.com {query}"
            
            d) 🇵🇭 **菲律賓區域**:
               - "site:fintechnews.ph {query}"
            
            e) 🇰🇭 **柬埔寨區域**:
               - "site:khmertimeskh.com {query}"
               - "site:phnompenhpost.com {query}"
        
        7.  **多樣性建議**: 
            - 💡 **建議做法**: 盡量使用 3-4 個或以上不同的新聞來源
            - 🔄 **執行方式**: 對不同區域進行搜尋，嘗試從多個網站收集新聞
            - 📊 **平衡策略**: 優先選擇最相關和高質量的新聞，同時適度考慮來源多樣性
            - 使用不同的關鍵字變化（中英文、同義詞等）
            
        8.  **域名驗證**: 
            - 確保所有新聞 URL 的域名必須是以下之一：{allowed_domains_str}
            - 嚴格排除任何不在上述列表中的網站
            
        9.  **資訊完整性**: 每條新聞都必須包含清晰的「標題」、「摘要」、「來源網站」、「完整網址」和「發布日期」。

        **輸出格式要求:**
        你必須嚴格遵循下面的 JSON 格式返回結果。`results` 陣列必須包含所有找到的新聞。

        ```json
        {{
            "search_query": "{query}",
            "search_date": "YYYY-MM-DD",
            "results": [
                {{
                    "title": "新聞標題範例 1",
                    "summary": "這是第一則新聞的摘要內容...",
                    "source": "新聞來源 A",
                    "url": "https://example.com/news-article-1",
                    "date": "YYYY-MM-DD"
                }},
                {{
                    "title": "新聞標題範例 2",
                    "summary": "這是第二則新聞的摘要內容...",
                    "source": "新聞來源 B",
                    "url": "https://example.com/news-article-2",
                    "date": "YYYY-MM-DD"
                }}
            ]
        }}
        ```
        """
        
        try:
            # 使用 Agent 執行搜尋
            response = self.agent.run(enhanced_query)
            
            # 提取回應內容
            if hasattr(response, 'content'):
                content = response.content
            else:
                content = str(response)
            
            print("✅ Research Agent 搜尋完成")
            
            return {
                "status": "success",
                "query": query,
                "content": content,
                "raw_response": response
            }
            
        except Exception as e:
            print(f"❌ Research Agent 搜尋失敗: {str(e)}")
            return {
                "status": "error",
                "query": query,
                "error": str(e)
            }
    
    def test_connection(self) -> bool:
        """測試 Agent 連接是否正常"""
        try:
            test_response = self.agent.run("測試連接")
            return True
        except Exception as e:
            print(f"❌ 連接測試失敗: {str(e)}")
            return False


if __name__ == "__main__":
    # 測試 Research Agent
    agent = ResearchAgent()
    result = agent.search("新加坡股市最新動態")
    print(json.dumps(result, ensure_ascii=False, indent=2))
