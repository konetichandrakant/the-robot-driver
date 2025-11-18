import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class PlaywrightMCPService:
    def __init__(self, headless: bool = True, browser: str = "chrome"):
        self.headless = headless
        self.browser = browser
        self._ctx = None
        self._session_cm = None
        self._session = None
        self._read = None
        self._write = None

    async def start(self):
        args = [
            "@playwright/mcp@latest",
            f"--browser={self.browser}",
            "--isolated",
            "--no-sandbox",
        ]

        if self.headless:
            args.append("--headless")

        server = StdioServerParameters(
            command="npx",
            args=args,
        )

        # stdio client context
        self._ctx = stdio_client(server)
        self._read, self._write = await self._ctx.__aenter__()

        # MCP session context
        self._session_cm = ClientSession(self._read, self._write)
        self._session = await self._session_cm.__aenter__()

        # Initialize MCP session
        await self._session.initialize()

    async def list_tools(self):
        if not self._session:
            raise RuntimeError("MCP session not started. Call start() first.")
        tools = await self._session.list_tools()
        return tools.tools

    async def call_tool(self, tool_name: str, parameters: dict, timeout: float = 60.0):
        if not self._session:
            raise RuntimeError("MCP session not started. Call start() first.")

        try:
            response = await asyncio.wait_for(
                self._session.call_tool(name=tool_name, arguments=parameters),
                timeout=timeout,
            )
            return response
        except asyncio.TimeoutError:
            raise TimeoutError(
                f"MCP tool '{tool_name}' timed out after {timeout} seconds"
            )

    async def get_page_content(self) -> str:
        if not self._session:
            raise RuntimeError("MCP session not started. Call start() first.")

        result = await self.call_tool("browser_snapshot", {})

        texts: list[str] = []
        if hasattr(result, "content") and result.content:
            for item in result.content:
                text = getattr(item, "text", None)
                if text:
                    texts.append(text)

        return "\n\n".join(texts)

    async def stop(self):
        if self._session_cm is not None:
            await self._session_cm.__aexit__(None, None, None)
            self._session_cm = None
            self._session = None

        if self._ctx is not None:
            await self._ctx.__aexit__(None, None, None)
            self._ctx = None
            self._read = None
            self._write = None

    @property
    def session(self):
        return self._session
