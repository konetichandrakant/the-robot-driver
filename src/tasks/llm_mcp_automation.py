import json
from openai import OpenAI
from src.services.llm_service import LLMService
from src.services.playwright_mcp_service import PlaywrightMCPService
from src.config import WEBSITE_URL, OPENROUTER_MODEL, OPENROUTER_API_KEY, OPENROUTER_BASE_URL, BROWSER_HEADLESS
from src.utils.prompt_utils import default_system_prompt, create_user_prompt
from src.utils.automation_utils import extract_json_from_response, combine_actions_performed

class LLMMCPAutomation:
    def __init__(self):
        self.context = []
        self.llm_service = LLMService(model=OPENROUTER_MODEL, client = OpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL))
        self.playwright_mcp_service = PlaywrightMCPService(headless=BROWSER_HEADLESS)
    
    async def execute(self, user_query: str):
        print("Started LLM Automation execution...")
        
        await self.playwright_mcp_service.start() # start MCP service
        await self.playwright_mcp_service.call_tool(tool_name="browser_navigate", parameters={"url": WEBSITE_URL}) # Start automation by going to website
        
        done = False # flag to confirm completion of automation
        max_iterations = 20  # safety limit to prevent infinite loops
        
        while not done and max_iterations>0:
            # Get current page content and available tools from MCP
            try:
                page_content = await self.playwright_mcp_service.get_page_content()
                tools_list = await self.playwright_mcp_service.list_tools()
                available_tools = [tool.name for tool in tools_list]
            except Exception as e:
                print(f"An error occurred while fetching page content or tools: {e}")
                break
            
            # Get next best action to perform from LLM
            try:
                # Create user prompt for LLM
                actions_performed = combine_actions_performed(self.context)
                user_prompt = create_user_prompt(user_query, page_content, available_tools, actions_performed)
                
                # Generate LLM response to perform next best action
                llm_message = [{ "role": "system", "content": default_system_prompt() }, { "role": "user", "content": user_prompt }]
                llm_response = self.llm_service.generate_response(llm_message)
                
                print(f"LLM Response: {llm_response}")

                # Extract JSON from LLM response (handles markdown code blocks)
                try:
                    json_response = extract_json_from_response(llm_response)
                    action_data = json.loads(json_response)
                    tool = action_data.get('tool')
                    params = action_data.get('params', {})
                    reasoning = action_data.get('reasoning', '')
                    if not tool or not isinstance(params, dict):
                        raise KeyError("Invalid tool or params in LLM response")
                    if tool not in available_tools and tool != "none":
                        raise KeyError(f"Tool '{tool}' not in available tools: {available_tools}")
                    print(f"Parsed action: tool={tool}, params={params}")
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"Error parsing LLM response: {e}, response was: {llm_response}")
                    break
                
                # Execute the action on MCP
                if tool != "none":
                    try:
                        await self.playwright_mcp_service.call_tool(tool_name=tool, parameters=params)
                        print(f"Successfully executed action tool: {tool}, params: {params}")
                    except Exception as e:
                        print(f"Error executing MCP action with tool: {action_data}, params: {params}: {e}")
                        break
                else:
                    print(f"No action to be taken reason: {reasoning}")
                    done = True  # stopping condition met
            
                # Add the interaction to context
                self.context.append({ "role": "user", "content": user_prompt })
                self.context.append({ "role": "assistant", "content": llm_response })
            except Exception as e:
                print(f"Error getting LLM response: {e}")
                break
            
            max_iterations -= 1
        
        await self.playwright_mcp_service.stop() # Stop MCP service
        
        print("\n\n=========== CONTEXT: ===========\n", self.context, "\n=================================\n")
        
        print("LLM Automation execution completed.")