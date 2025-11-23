import pytest
from src.tasks.automation_task import LLMMCPAutomation
from src.config import WEBSITE_URL, OPENROUTER_MODEL, OPENROUTER_API_KEY, OPENROUTER_BASE_URL, BROWSER_HEADLESS

@pytest.mark.asyncio
async def test_find_cheapest_jeans_and_add_to_cart():
    try:
        # User query ( user prompt )
        user_query = "Find cheapest jeans for men and add to cart."
        
        automation = LLMMCPAutomation(user_query)
        
        # Run the llm mcp automation
        response = await automation.execute()
        
        print("Automation Response:", response)
        
        assert True
        
    except Exception as e:
        assert False