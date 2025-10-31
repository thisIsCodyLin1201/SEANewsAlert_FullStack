#!/usr/bin/env python3
"""
修正所有 Python 檔案中的 emoji，避免 Windows cp950 編碼問題
"""
import os
import re

# 要替換的 emoji 映射
emoji_replacements = {
    '🚀': '[START]',
    '✅': '[OK]',
    '❌': '[ERROR]',
    '⚠️': '[WARNING]',
    '📊': '[ANALYSIS]',
    '📄': '[REPORT]',
    '📧': '[EMAIL]',
    '🔍': '[SEARCH]',
    '💡': '[INSIGHT]',
    '📋': '[LIST]',
    '📅': '[DATE]',
    '📰': '[NEWS]',
    '📎': '[ATTACHMENT]',
    '⚙️': '[CONFIG]',
    'ℹ️': '[INFO]',
    '❤️': '[HEALTH]',
    '🏗️': '[BUILD]',
}

# 要處理的檔案路徑
files_to_fix = [
    'SEANewsAlert/app/services/workflow.py',
    'SEANewsAlert/workflow.py',
    'SEANewsAlert/agents/research_agent.py',
    'SEANewsAlert/agents/analyst_agent.py',
    'SEANewsAlert/agents/report_agent.py',
    'SEANewsAlert/agents/email_agent.py',
    'SEANewsAlert/app/main.py',
]

def fix_emoji_in_file(filepath):
    """修正單個檔案中的 emoji"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content

        # 替換所有 emoji
        for emoji, replacement in emoji_replacements.items():
            content = content.replace(emoji, replacement)

        # 如果有變更，寫回檔案
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {filepath}")
            return True
        else:
            print(f"No changes needed: {filepath}")
            return False
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return False

def main():
    print("Starting emoji fix for Windows cp950 encoding...")

    fixed_count = 0
    for filepath in files_to_fix:
        if os.path.exists(filepath):
            if fix_emoji_in_file(filepath):
                fixed_count += 1
        else:
            print(f"File not found: {filepath}")

    print(f"\nCompleted! Fixed {fixed_count} files.")

if __name__ == "__main__":
    main()