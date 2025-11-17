import pytest
from src.tasks.llm_mcp_automation import LLMMCPAutomation

@pytest.mark.asyncio
async def test_find_cheapest_jeans_and_add_to_cart():
    """Test LLMMCPAutomation execute method for finding cheapest jeans and adding to cart."""
    user_query = "Find cheapest jeans and add to cart."

    # Create and execute automation with real services
    automation = LLMMCPAutomation()
    await automation.execute(user_query)