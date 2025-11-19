import json
from openai import OpenAI
from src.services.llm_service import LLMService
from src.services.playwright_mcp_service import PlaywrightMCPService
from src.config import WEBSITE_URL, OPENROUTER_MODEL, OPENROUTER_API_KEY, OPENROUTER_BASE_URL, BROWSER_HEADLESS
from src.utils.prompt_utils import default_system_prompt, create_user_prompt
from src.utils.automation_utils import extract_json_from_response, extract_actions_performed, validate_llm_response

class LLMMCPAutomation:
    
    # Initialize LLM service and Playwright MCP service
    def __init__(self):
        self.context = []
        self.llm_service = LLMService(model=OPENROUTER_MODEL, client = OpenAI(api_key=OPENROUTER_API_KEY, base_url=OPENROUTER_BASE_URL))
        self.playwright_mcp_service = PlaywrightMCPService(headless=BROWSER_HEADLESS)
    
    # Executes or performs the LLM-driven MCP automation
    async def execute(self, user_query: str):
        print("Started LLM Automation execution...")
        
        # start MCP service
        await self.playwright_mcp_service.start()
        
        # Start automation by going to website
        await self.playwright_mcp_service.call_tool(tool_name="browser_navigate", parameters={"url": WEBSITE_URL})
        
        # safety limit to prevent infinite loops
        max_iterations = 20
        
        while max_iterations>0:
            
            # Get current page content and available tools by calling MCP service
            try:
                page_content = await self.playwright_mcp_service.get_page_content()
                tools_list = await self.playwright_mcp_service.list_tools()
                available_tools = [tool.name for tool in tools_list]
            
            except Exception as e:
                print(f"An error occurred while fetching page content or tools: {e}")
                raise e
            
            # Get next best action to perform from LLM
            try:
                # Create user prompt for LLM using page content, available tools, and actions which are already performed
                actions_performed = extract_actions_performed(self.context)
                user_prompt = create_user_prompt(user_query, page_content, available_tools, actions_performed)
                
                # Using the user prompt of all details our LLM predicts the next best step to take
                llm_message = [{ "role": "system", "content": default_system_prompt() }, { "role": "user", "content": user_prompt }]
                llm_response = self.llm_service.generate_response(llm_message)
            
                print("LLM Response for next best action", "\n", llm_response, "\n")
            
            except Exception as e:
                print(f"Error getting LLM response: {e}")
                break
            
            # Extract JSON from LLM response (handles markdown code blocks) which contains tool call information, parameters information, and reasoning why that step is taken.
            try:
                json_response = extract_json_from_response(llm_response)
                action_data = json.loads(json_response)
                
                tool_name = action_data.get('tool', None)
                parameters = action_data.get('params', {})
                reasoning = action_data.get('reasoning', 'No data provided by the LLM')
                
                # Validate the results given by LLMs
                validate_llm_response(tool = tool_name, parameters = parameters, available_tools = available_tools)
        
            except Exception as e:
                print(f"Error parsing LLM response: {e}, response was: {llm_response}")
                raise e
            
            # Execute the call_tool action on MCP which saves the actions in the same session
            if tool_name is not None and tool_name != "none":
                try:
                    await self.playwright_mcp_service.call_tool(tool_name, parameters)
                    print(f"Successfully executed action tool: {tool_name}, params: {parameters}")
                    
                    # As this action is executed properly via MCP we need to send the same parsed llm_response in return for API interaction in form of yield
                    
                except Exception as e:
                    print(f"Error executing MCP action with tool: {action_data}, parameters: {parameters}: {e}")
                    raise e
                
            else:
                print(f"No action to be taken reason: {reasoning}")
                # stopping condition met so break the loop
                break
        
            # Add the interaction to context which will help us to maintain the history of actions performed by the LLM which helps in sending the LLM this response to cut down infinite looping
            self.context.append({ "role": "user", "content": user_prompt })
            self.context.append({ "role": "assistant", "content": llm_response })
            
            max_iterations -= 1
        
        # Stop MCP service
        await self.playwright_mcp_service.stop()
        
        print("LLM Automation execution completed.")