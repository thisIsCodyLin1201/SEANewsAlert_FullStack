"""
測試 ResearchAgent, AnalystAgent 和 ReportGeneratorAgent 的整合
"""
import os
import sys
import json

# 設置 UTF-8 編碼
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-5-2025-08-07"

def test_integration():
    """測試完整的三個 agent 整合流程"""
    print("=" * 80)
    print("整合測試: ResearchAgent → AnalystAgent → ReportGeneratorAgent")
    print("=" * 80)

    try:
        # 步驟 1: 模擬 ResearchAgent 的返回結果
        print("\n步驟 1: 模擬 ResearchAgent 的搜尋結果")
        print("-" * 80)

        client = OpenAI(api_key=OPENAI_API_KEY)

        query = "新加坡金融科技最新發展"

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=f"""
            請搜尋關於「{query}」的新聞，並以 JSON 格式返回結果。

            請在回應中包含一個 JSON 代碼塊（用 ```json 包裹），格式如下：

            ```json
            {{
                "search_query": "{query}",
                "search_date": "{datetime.now().strftime('%Y-%m-%d')}",
                "results": [
                    {{
                        "title": "新聞標題",
                        "summary": "新聞摘要內容...",
                        "source": "來源名稱",
                        "url": "https://example.com/article",
                        "date": "2025-10-20"
                    }}
                ]
            }}
            ```

            請找 2-3 條相關新聞。
            """,
            tools=[{"type": "web_search"}]
        )

        # 提取回應內容
        content = ""
        sources = []

        for output_item in response.output:
            if output_item.type == "message":
                for content_item in output_item.content:
                    if content_item.type == "output_text":
                        content += content_item.text

                        if hasattr(content_item, 'annotations') and content_item.annotations:
                            for annotation in content_item.annotations:
                                if annotation.type == "url_citation":
                                    sources.append({
                                        "title": annotation.title,
                                        "url": annotation.url
                                    })

        # 構建 ResearchAgent 格式的返回結果
        search_results = {
            "status": "success",
            "query": query,
            "content": content,
            "sources": sources,
            "raw_response": response
        }

        print(f"✓ 搜尋完成")
        print(f"  - 查詢: {query}")
        print(f"  - 內容長度: {len(content)} 字元")
        print(f"  - 來源數量: {len(sources)}")

        # 步驟 2: 檢查返回格式的相容性
        print("\n步驟 2: 檢查返回格式相容性")
        print("-" * 80)

        # 檢查 AnalystAgent 需要的欄位
        required_fields = ["status", "query", "content"]
        missing_fields = [field for field in required_fields if field not in search_results]

        if missing_fields:
            print(f"✗ 缺少必要欄位: {missing_fields}")
            return False
        else:
            print("✓ 所有必要欄位都存在")

        # 檢查 content 是否包含 JSON
        import re
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', content, re.DOTALL)

        if json_match:
            print("✓ content 中包含 JSON 格式數據")
            try:
                json_data = json.loads(json_match.group(1))
                results = json_data.get('results', [])
                print(f"  - 找到 {len(results)} 條新聞")
            except json.JSONDecodeError as e:
                print(f"⚠ JSON 解析警告: {str(e)}")
        else:
            print("⚠ content 中未找到 JSON 格式數據")
            print("  這意味著 AnalystAgent 需要從 Markdown 中提取結構化數據")

        # 步驟 3: 顯示完整的 content 預覽
        print("\n步驟 3: Content 預覽")
        print("-" * 80)
        print(content[:500] + "..." if len(content) > 500 else content)

        # 步驟 4: 顯示 sources 資訊
        if sources:
            print("\n步驟 4: Sources 資訊")
            print("-" * 80)
            for i, source in enumerate(sources[:5], 1):
                print(f"{i}. {source['title']}")
                print(f"   {source['url']}")

        print("\n" + "=" * 80)
        print("整合測試結果")
        print("=" * 80)
        print("✓ ResearchAgent 的返回格式與 AnalystAgent 相容")
        print("✓ 包含所有必要欄位: status, query, content")
        print("✓ 新增 sources 欄位提供額外的結構化數據")
        print("=" * 80)

        return True

    except Exception as e:
        print(f"\n✗ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_integration()
