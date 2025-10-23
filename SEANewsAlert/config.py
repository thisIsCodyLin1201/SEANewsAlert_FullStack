"""
配置管理模組
負責載入和管理所有環境變數
"""
import os
from dotenv import load_dotenv
from pathlib import Path

# 載入環境變數
load_dotenv()

class Config:
    """應用程式配置類"""
    
    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    OPENAI_MODEL = "gpt-5-2025-08-07"
    OPENAI_API_BASE = "https://api.openai.com/v1"  # 確保端點一致
    
    # Email Configuration
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    
    # Application Configuration
    APP_NAME = os.getenv("APP_NAME", "東南亞金融新聞搜尋系統")
    APP_VERSION = os.getenv("APP_VERSION", "2.0.0")
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"
    
    # Agno Configuration
    AGNO_TELEMETRY = os.getenv("AGNO_TELEMETRY", "false").lower() == "true"
    
    # Paths
    BASE_DIR = Path(__file__).parent
    REPORTS_DIR = BASE_DIR / "reports"
    TEMPLATES_DIR = BASE_DIR / "templates"
    
    # 確保目錄存在
    REPORTS_DIR.mkdir(exist_ok=True)
    TEMPLATES_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def validate(cls):
        """驗證必要的配置是否存在"""
        required_configs = {
            "OPENAI_API_KEY": cls.OPENAI_API_KEY,
            "EMAIL_ADDRESS": cls.EMAIL_ADDRESS,
            "EMAIL_PASSWORD": cls.EMAIL_PASSWORD,
        }
        
        missing = [key for key, value in required_configs.items() if not value]
        
        if missing:
            raise ValueError(f"缺少必要的環境變數: {', '.join(missing)}")
        
        return True

# 驗證配置
try:
    Config.validate()
    print("✅ 配置驗證成功")
except ValueError as e:
    print(f"⚠️  配置驗證失敗: {e}")
