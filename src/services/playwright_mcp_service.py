import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class PlaywrightMCPService:
    def __init__(self):
        self._ctx = None
        self._session = None

    async def start(self):
        try:
            print("[MCP] Starting Playwright MCP server...")
            server = StdioServerParameters(
                command="npx",
                args=["@playwright/mcp@latest"],
            )
            print("[MCP] Creating stdio client...")
            self._ctx = stdio_client(server)
            self._read, self._write = await self._ctx.__aenter__()
            print("[MCP] stdio client created, creating session...")
            self._session_cm = ClientSession(self._read, self._write)
            self._session = await self._session_cm.__aenter__()
            print("[MCP] Session created, initializing...")
            await self._session.initialize()
            print("[MCP] Initialization complete!")
        except Exception as e:
            print(f"[MCP] ERROR starting service: {e}")
            import traceback
            traceback.print_exc()
            raise

    async def list_tools(self):
        try:
            print("[MCP] Listing tools...")
            tools = await self._session.list_tools()
            print(f"[MCP] Tools listed successfully: {len(tools.tools)} tools found")
            return tools.tools
        except Exception as e:
            print(f"[MCP] ERROR listing tools: {e}")
            raise
    
    async def call_tool(self, tool_name: str, parameters: dict):
        try:
            print(f"[MCP] Calling tool {tool_name} with parameters: {parameters}")
            # Add timeout to prevent hanging
            response = await asyncio.wait_for(
                self._session.call_tool(name=tool_name, arguments=parameters),
                timeout=60.0  # 60 second timeout
            )
            print(f"[MCP] Tool {tool_name} completed successfully: {response}")
            return response
        except asyncio.TimeoutError:
            print(f"[MCP] TIMEOUT: Tool {tool_name} took too long to complete")
            raise
        except Exception as e:
            print(f"[MCP] ERROR calling tool {tool_name}: {e}")
            import traceback
            traceback.print_exc()
            raise

    async def get_page_content(self) -> str:
        try:
            print("[MCP] Getting page content...")
            result = await self._session.call_tool("browser_evaluate", {"function": "() => document.documentElement.outerHTML"})
            content = result.content if hasattr(result, 'content') else str(result)
            print(f"[MCP] Page content retrieved, length: {len(content)}")
            return content
        except Exception as e:
            print(f"[MCP] ERROR getting page content: {e}")
            raise

    async def stop(self):
        print("[MCP] Stopping service...")
        if self._session:
            await self._session.__aexit__(None, None, None)
        if self._ctx:
            await self._ctx.__aexit__(None, None, None)
        print("[MCP] Service stopped")

    @property
    def session(self):
        return self._session