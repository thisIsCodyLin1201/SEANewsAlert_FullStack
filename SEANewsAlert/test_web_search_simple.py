"""
簡單測試 OpenAI Responses API web_search 功能
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def test():
    print("測試開始...")

    try:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        print("發送請求...")
        response = client.responses.create(
            model="gpt-5-2025-08-07",
            input="What is the capital of France?",
            tools=[{"type": "web_search"}]
        )

        print("\n處理回應...")
        for output_item in response.output:
            print(f"Output type: {output_item.type}")

            if output_item.type == "message":
                for content_item in output_item.content:
                    if content_item.type == "output_text":
                        print(f"\nResponse: {content_item.text}")

        print("\n測試成功!")

    except Exception as e:
        print(f"\n測試失敗: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test()
