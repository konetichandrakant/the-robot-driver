import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from src.tasks.llm_mcp_automation import LLMMCPAutomation

@pytest.mark.asyncio
async def test_llm_mcp_automation_execute():
    """Test LLMMCPAutomation execute method with mocked dependencies."""
    user_query = "I would like to find out the cheapest jeans available on the website and add them to my cart."

    with patch('src.tasks.llm_mcp_automation.PlaywrightMCPService') as mock_mcp_service_class, \
         patch('src.tasks.llm_mcp_automation.LLMService') as mock_llm_service_class:

        # Setup mocks
        mock_llm_service = MagicMock()
        mock_mcp_service = AsyncMock()

        mock_llm_service_class.return_value = mock_llm_service
        mock_mcp_service_class.return_value = mock_mcp_service

        # Mock page content and tools
        mock_mcp_service.get_page_content.return_value = "<html><body>Test page content</body></html>"
        mock_mcp_service.list_tools.return_value = [
            {"name": "click", "description": "Click on an element"},
            {"name": "type", "description": "Type text into an element"},
            {"name": "goto", "description": "Navigate to a URL"}
        ]

        # Mock LLM response
        mock_llm_service.generate_response.return_value = '{"tool": "none", "params": {}, "reasoning": "Task completed successfully"}'

        # Execute test
        automation = LLMMCPAutomation()
        await automation.execute(user_query)

        # Verify the automation completed without exceptions
        # and that the expected methods were called
        mock_mcp_service.start.assert_called_once()
        mock_mcp_service.stop.assert_called_once()
        mock_llm_service.generate_response.assert_called()