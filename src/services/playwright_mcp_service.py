from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# pw = MCPService()
# await pw.start()
# # Everything below shares the same browser/page state:
# await pw.session.call_tool("browser_navigate", {"url": "https://example.com"})
# # ... later:
# await pw.session.call_tool("browser_type", {"ref": "page", "element": "body", "text": "hello", "submit": True})
# # ... even later:
# await pw.session.call_tool("browser_evaluate", {"expression": "document.title"})
# # when you're truly done:
# await pw.stop()

class PlaywrightMCPService:
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

    async def stop(self):
        if self._session:
            await self._session.__aexit__(None, None, None)
        if self._ctx:
            await self._ctx.__aexit__(None, None, None)

    @property
    def session(self):
        return self._session
