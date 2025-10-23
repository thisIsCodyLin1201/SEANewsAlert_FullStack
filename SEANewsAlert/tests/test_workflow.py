"""
測試工作流程
"""
import pytest
import sys
from pathlib import Path

# 添加專案根目錄到路徑
sys.path.insert(0, str(Path(__file__).parent.parent))

from workflow import SEANewsWorkflow
from config import Config


class TestWorkflow:
    """測試工作流程"""
    
    def test_initialization(self):
        """測試工作流程初始化"""
        workflow = SEANewsWorkflow()
        
        assert workflow is not None
        assert workflow.research_agent is not None
        assert workflow.analyst_agent is not None
        assert workflow.report_agent is not None
        assert workflow.email_agent is not None
    
    def test_validate_agents(self):
        """測試 Agents 驗證"""
        workflow = SEANewsWorkflow()
        results = workflow.validate_agents()
        
        assert isinstance(results, dict)
        assert "research_agent" in results
        assert "email_agent" in results
    
    @pytest.mark.skipif(
        not all([Config.OPENAI_API_KEY, Config.EMAIL_ADDRESS]),
        reason="需要完整配置"
    )
    def test_execute_workflow(self):
        """測試完整工作流程（僅在有配置時）"""
        workflow = SEANewsWorkflow()
        
        # 使用測試查詢
        result = workflow.execute(
            search_query="測試查詢",
            recipient_emails=Config.EMAIL_ADDRESS
        )
        
        assert result is not None
        assert "status" in result
        assert "steps" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
