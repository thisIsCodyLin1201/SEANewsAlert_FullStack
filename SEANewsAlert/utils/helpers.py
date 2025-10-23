"""
輔助工具函數
"""
from typing import List, Dict, Any
import re
from datetime import datetime


def validate_email(email: str) -> bool:
    """
    驗證郵箱格式
    
    Args:
        email: 郵箱地址
        
    Returns:
        bool: 格式是否正確
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def parse_emails(email_string: str) -> List[str]:
    """
    解析郵箱字串，支援逗號分隔
    
    Args:
        email_string: 郵箱字串
        
    Returns:
        List[str]: 郵箱列表
    """
    emails = [e.strip() for e in email_string.split(',')]
    return [e for e in emails if validate_email(e)]


def format_timestamp(timestamp: str = None) -> str:
    """
    格式化時間戳
    
    Args:
        timestamp: ISO 格式時間戳（可選）
        
    Returns:
        str: 格式化後的時間字串
    """
    if timestamp:
        dt = datetime.fromisoformat(timestamp)
    else:
        dt = datetime.now()
    
    return dt.strftime("%Y年%m月%d日 %H:%M:%S")


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截斷文字
    
    Args:
        text: 原始文字
        max_length: 最大長度
        suffix: 後綴
        
    Returns:
        str: 截斷後的文字
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def clean_markdown(markdown_text: str) -> str:
    """
    清理 Markdown 文字中的多餘空白和格式
    
    Args:
        markdown_text: Markdown 文字
        
    Returns:
        str: 清理後的文字
    """
    # 移除多餘的空行
    lines = markdown_text.split('\n')
    cleaned_lines = []
    prev_empty = False
    
    for line in lines:
        is_empty = not line.strip()
        if not (is_empty and prev_empty):
            cleaned_lines.append(line)
        prev_empty = is_empty
    
    return '\n'.join(cleaned_lines)


def extract_urls(text: str) -> List[str]:
    """
    從文字中提取 URL
    
    Args:
        text: 原始文字
        
    Returns:
        List[str]: URL 列表
    """
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(url_pattern, text)


if __name__ == "__main__":
    # 測試工具函數
    print("測試郵箱驗證:")
    print(validate_email("test@example.com"))  # True
    print(validate_email("invalid-email"))      # False
    
    print("\n測試解析郵箱:")
    print(parse_emails("test1@example.com, test2@example.com"))
    
    print("\n測試格式化時間:")
    print(format_timestamp())
    
    print("\n測試截斷文字:")
    print(truncate_text("這是一段很長的文字" * 10, 50))
