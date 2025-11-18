import pytest
from src.services.playwright_mcp_service import PlaywrightMCPService
from src.utils.automation_utils import get_website

@pytest.mark.asyncio
async def test_mcp_service():
    service = PlaywrightMCPService(headless=False, browser="chrome")
    try:
        print("=== Starting MCP Test ===")
        await service.start()
        
        print("=== Listing Tools ===")
        tools = await service.list_tools()
        print(f"Found {len(tools)} tools")
        
        print("=== Testing browser_navigate ===")
        await service.call_tool("browser_navigate", {"url": get_website()})
        print("Navigation done")

        print("=== Getting page content ===")
        content = await service.get_page_content()
        print(f"Page content length: {len(content)}")
        
        print("=== Stopping MCP ===")
        await service.stop()
        
        print("=== Test completed successfully! ===")
        
    except Exception as e:
        print(f"=== Test FAILED: {e} ===")
        import traceback
        traceback.print_exc()
        raise