import pytest
from src.tasks.llm_mcp_automation import LLMMCPAutomation

@pytest.mark.asyncio
async def test_find_cheapest_jeans_and_add_to_cart():
    user_query = "Find cheapest jeans for men and add to cart."
    
    automation = LLMMCPAutomation()
    await automation.execute(user_query)