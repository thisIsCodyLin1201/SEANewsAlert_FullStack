"""
測試 Agents 功能
"""
import pytest
import sys
from pathlib import Path

# 添加專案根目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents import ResearchAgent, AnalystAgent, ReportGeneratorAgent, EmailAgent
from config import Config


class TestResearchAgent:
    """測試 Research Agent"""
    
    def test_initialization(self):
        """測試 Agent 初始化"""
        agent = ResearchAgent()
        assert agent is not None
        assert agent.agent is not None
    
    @pytest.mark.skipif(not Config.OPENAI_API_KEY, reason="需要 OpenAI API Key")
    def test_search(self):
        """測試搜尋功能"""
        agent = ResearchAgent()
        result = agent.search("測試查詢")
        
        assert result is not None
        assert "status" in result
        assert "query" in result


class TestAnalystAgent:
    """測試 Analyst Agent"""
    
    def test_initialization(self):
        """測試 Agent 初始化"""
        agent = AnalystAgent()
        assert agent is not None
        assert agent.agent is not None
    
    def test_analyze(self):
        """測試分析功能"""
        agent = AnalystAgent()
        
        mock_results = {
            "status": "success",
            "query": "測試查詢",
            "content": "測試內容"
        }
        
        report = agent.analyze(mock_results)
        
        assert report is not None
        assert isinstance(report, str)
        assert len(report) > 0


class TestReportGeneratorAgent:
    """測試 Report Generator Agent"""
    
    def test_initialization(self):
        """測試 Agent 初始化"""
        agent = ReportGeneratorAgent()
        assert agent is not None
        assert agent.reports_dir.exists()
    
    def test_generate_pdf(self):
        """測試 PDF 生成"""
        agent = ReportGeneratorAgent()
        
        test_markdown = """
# 測試報告

## 內容
這是一個測試報告。
"""
        
        pdf_path = agent.generate_pdf(test_markdown, "test_report.pdf")
        
        assert pdf_path.exists()
        assert pdf_path.suffix == ".pdf"
        
        # 清理測試文件
        pdf_path.unlink()


class TestEmailAgent:
    """測試 Email Agent"""
    
    def test_initialization(self):
        """測試 Agent 初始化"""
        agent = EmailAgent()
        assert agent is not None
        assert agent.smtp_server is not None
    
    @pytest.mark.skipif(
        not all([Config.EMAIL_ADDRESS, Config.EMAIL_PASSWORD]),
        reason="需要郵件配置"
    )
    def test_connection(self):
        """測試郵件服務器連接"""
        agent = EmailAgent()
        result = agent.test_connection()
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
