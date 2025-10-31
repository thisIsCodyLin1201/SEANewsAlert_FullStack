"""
測試 Research Agent 的 OpenAI Responses API web_search 功能
"""
import os
import sys
import json

# 設置 UTF-8 編碼
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# 手動設置配置以避免 config.py 的編碼問題
from openai import OpenAI
from datetime import datetime

# 從環境變數載入配置
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-5-2025-08-07"

def test_simple_search():
    """測試簡單的 web search"""
    print("=" * 60)
    print("測試 1: 簡單的網路搜尋")
    print("=" * 60)

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        response = client.responses.create(
            model=OPENAI_MODEL,
            input="列出本週台股重大事件並附來源",
            tools=[{"type": "web_search"}]
        )

        print("\n搜尋結果:")
        print("-" * 60)

        for output_item in response.output:
            if output_item.type == "web_search_call":
                print(f"網路搜尋狀態: {output_item.status}")

            elif output_item.type == "message":
                for content_item in output_item.content:
                    if content_item.type == "output_text":
                        print(f"\n回應內容:\n{content_item.text}\n")

                        # 顯示來源
                        if hasattr(content_item, 'annotations') and content_item.annotations:
                            print("\n來源列表:")
                            for i, annotation in enumerate(content_item.annotations, 1):
                                if annotation.type == "url_citation":
                                    print(f"{i}. {annotation.title}")
                                    print(f"   URL: {annotation.url}")

        print("\n✓ 測試成功!")
        return True

    except Exception as e:
        print(f"\n✗ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_sea_finance_search():
    """測試東南亞金融新聞搜尋"""
    print("\n" + "=" * 60)
    print("測試 2: 東南亞金融新聞搜尋")
    print("=" * 60)

    try:
        client = OpenAI(api_key=OPENAI_API_KEY)

        query = """
        請搜尋最近 7 天內的東南亞金融科技新聞，特別關注:
        - 新加坡、馬來西亞、泰國、越南、菲律賓
        - 主題: 金融科技、數位支付、區塊鏈、加密貨幣
        - 請盡量從不同的新聞來源收集 5-10 篇新聞

        請以 JSON 格式回覆，包含標題、摘要、來源網站、URL、發布日期
        """

        response = client.responses.create(
            model=OPENAI_MODEL,
            input=query,
            tools=[{"type": "web_search"}]
        )

        print("\n搜尋結果:")
        print("-" * 60)

        content = ""
        sources = []

        for output_item in response.output:
            if output_item.type == "web_search_call":
                print(f"網路搜尋狀態: {output_item.status}")

            elif output_item.type == "message":
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

        print(f"\n回應內容:\n{content}\n")

        if sources:
            print(f"\n找到 {len(sources)} 個來源:")
            for i, source in enumerate(sources, 1):
                print(f"{i}. {source['title']}")
                print(f"   {source['url']}")

        print("\n✓ 測試成功!")
        return True

    except Exception as e:
        print(f"\n✗ 測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("開始測試 OpenAI Responses API Web Search 功能\n")

    # 執行測試
    test1_result = test_simple_search()
    test2_result = test_sea_finance_search()

    # 總結
    print("\n" + "=" * 60)
    print("測試總結")
    print("=" * 60)
    print(f"測試 1 (簡單搜尋): {'✓ 通過' if test1_result else '✗ 失敗'}")
    print(f"測試 2 (東南亞金融搜尋): {'✓ 通過' if test2_result else '✗ 失敗'}")
    print("=" * 60)
