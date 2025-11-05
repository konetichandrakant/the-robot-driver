import os
import json
import asyncio
from openai import OpenAI
from src.services.llm_service import LLMService
from src.services.mcp_service import MCPService
from utils.automation_utils import get_website, get_llm_api_key
from utils.prompt_utils import default_system_prompt, create_user_prompt

class LLMMCPAutomation:
    def __init__(self):
        self.context = []
        self.llm_service = LLMService(client = OpenAI(api_key=get_llm_api_key(), base_url=get_website()))
        self.playwright_mcp_service = MCPService()
    
    async def execute(self, user_query: str):
        # start MCP service
        await self.playwright_mcp_service.start()
                
        # flag to confirm completion of automation
        done = False
        
        while not done:
            # Get current page content and available tools from MCP
            try:
                page_content = await self.playwright_mcp_service.get_page_content()
                available_tools = await self.playwright_mcp_service.list_tools()
            except Exception as e:
                print(f"Error getting page content from MCP: {e}")
                break
            
            # Get next best action from LLM
            try:
                # Create user prompt for LLM
                user_prompt = create_user_prompt(user_query, page_content, available_tools)
                
                # Generate LLM response to perform next best action
                llm_message = [{ "role": "system", "content": default_system_prompt() }, { "role": "user", "content": user_prompt }]
                llm_response = self.llm_service.generate_response(llm_message)
                
                # Add the interaction to context
                self.context.append({ "role": "user", "content": user_prompt })
                self.context.append({ "role": "assistant", "content": llm_response })
            except Exception as e:
                print(f"Error getting LLM response: {e}")
                break
            
            # Parse LLM response as JSON
            try:
                action_data = json.loads(llm_response)
                action_tool = action_data['tool']
                action_params = action_data['parameters']
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error parsing LLM response: {e}")
                print(f"Raw response: {llm_response}")
                action_tool = "none"
                action_params = {}
            
            # 4) Execute the action on MCP
            if action_tool != "none":
                try:
                    await self.playwright_mcp_service.session.call_tool(action_tool, action_params)
                    print(f"Successfully executed action: {action_tool} with params: {action_params}")
                except Exception as e:
                    print(f"Error executing MCP action {action_tool}, with params {action_params}: {e}")
                    break
            elif action_tool == "none":
                print(f"No action taken as per LLM response: {action_data.get('reasoning', '')}")
                done = True  # stopping condition met

        # Clean up MCP service
        await self.playwright_mcp_service.stop()