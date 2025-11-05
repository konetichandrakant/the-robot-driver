from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPService:
    def __init__(self):
        self._ctx = None
        self._session = None

    async def start(self):
        server = StdioServerParameters(
            command="npx",
            args=["@playwright/mcp@latest"],
        )
        self._ctx = stdio_client(server)
        self._read, self._write = await self._ctx.__aenter__()
        self._session_cm = ClientSession(self._read, self._write)
        self._session = await self._session_cm.__aenter__()
        await self._session.initialize()

    async def list_tools(self):
        if not self._session:
            raise RuntimeError("MCP session not started. Call start() first.")
        return await self._session.list_tools()
    
    async def get_page_content(self) -> str:
        if not self._session:
            raise RuntimeError("MCP session not started. Call start() first.")
        result = await self._session.call_tool("browser_evaluate", {"expression": "document.documentElement.outerHTML"})
        return result.get('content', '') if isinstance(result, dict) else str(result)
    
    async def call_tool(self, tool_name: str, parameters: dict):
        if not self._session:
            raise RuntimeError("MCP session not started. Call start() first.")
        return await self._session.call_tool(tool_name, parameters)

    async def stop(self):
        if self._session:
            await self._session.__aexit__(None, None, None)
        if self._ctx:
            await self._ctx.__aexit__(None, None, None)

    @property
    def session(self):
        return self._session
