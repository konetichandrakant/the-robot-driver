import os
import json
import asyncio
from openai import OpenAI
from services.openai_llm_service import LLMService
from services.playwright_mcp_service import PlaywrightMCPService

# pw = PlaywrightMCP()
# await pw.start()
# # Everything below shares the same browser/page state:
# await pw.session.call_tool("browser_navigate", {"url": "https://example.com"})
# # ... later:
# await pw.session.call_tool("browser_type", {"ref": "page", "element": "body", "text": "hello", "submit": True})
# # ... even later:
# await pw.session.call_tool("browser_evaluate", {"expression": "document.title"})
# # when you're truly done:
# await pw.stop()

# 1) Use MCP service to get the current page content and possible actions that can be performed on that page
# 2) Use LLM to determine the next best action based on tools which can be performed on the particular step
    # Necessary actions to ensure better results:
    # Generate system prompt for better outputs based on the initial page and prompt given by user
    # Use the current page content as context for LLM to decide the next best action
    # Provide the list of available tools/actions that can be performed on the current page using MCP
    # Ask the LLM to choose the next best action from the list of available tools/actions and page content
    # Expect the LLM to respond with a structured format that includes the chosen action and any necessary parameters
# 3) Then apply the action given by LLM on MCP service which is the tool that needs to be applied on the given page
# Repeat step 1-3 until the goal is achieved or a stopping condition is met

class LLMMCPAutomation:
    def __init__(self):
        self.context = []
        self.llm_service = LLMService(client = OpenAI(api_key=os.getenv("OPENROUTER_API_KEY"), base_url=os.getenv("OPENROUTER_BASE_URL")))
        self.playwright_mcp_service = PlaywrightMCPService()

    def next_best_action(self, page_content: str) -> str:
        pass

    def _default_system_prompt(self):
        return f"""# Web Automation Specialist
            You are an expert web automation agent using Playwright MCP tools to complete tasks on **{os.getenv('WEBSITE_URL')}**.

            ## YOUR ROLE
            - Analyze the current page state and user goal
            - Select the optimal single action from available MCP tools
            - Execute step-by-step towards goal completion
            - Adapt strategy based on page changes

            ## DECISION FRAMEWORK
            1. **Assess**: What's on the current page? What's the goal?
            2. **Plan**: What sequence of actions achieves the goal?
            3. **Execute**: Choose the most specific, reliable action
            4. **Validate**: Did the action move us forward?

            ## ACTION SELECTION PRIORITY
            - Prefer semantic selectors: `text=`, `[aria-label]`, `[role]`
            - Use specific over generic selectors
            - Choose direct paths over indirect ones
            - Handle forms, navigation, and interactions methodically

            ## RESPONSE FORMAT
            Return ONLY valid JSON FOR PLAYWRIGHT MCP IF ACTION IS TO BE TAKEN:
            ```json
            {
            "tool": "tool_name",
            "parameters": {"param": "value"},
            "reasoning": "Clear explanation of why this action moves us toward the goal"
            }```
            
            ELSE IF no suitable action exists, return:
            ```json
            {
            "tool": "none",
            "reasoning": "Specific explanation why no action is appropriate"
            }```
            """

    def _create_user_prompt(self, user_prompt: str, page_content: str, available_tools: list) -> str:
        prompt = f"""
            GOAL (USER PROMPT): {user_prompt}

            CURRENT PAGE CONTENT:
            {page_content}

            AVAILABLE TOOLS:
            {available_tools}

            ## RESPONSE FORMAT
            Return ONLY valid JSON FOR PLAYWRIGHT MCP IF ACTION IS TO BE TAKEN:
            ```json
            {
            "tool": "tool_name",
            "parameters": {"param": "value"},
            "reasoning": "Clear explanation of why this action moves us toward the goal"
            }```
            
            ELSE IF no suitable action exists, return:
            ```json
            {
            "tool": "none",
            "reasoning": "Specific explanation why no action is appropriate"
            }```
            
            Based on the GOAL, CURRENT PAGE CONTENT, and AVAILABLE TOOLS, determine the next best action to take.
            """
        return prompt
    
    def _check_stopping_condition(self) -> bool:
        # Placeholder for stopping condition logic
        return False
    
    async def automate(self, user_prompt: str):
        # setup for automation
        
        # start MCP service
        await self.playwright_mcp_service.start()
        
        # main automation loop
        done = False        
        
        while not done:
            
            # 1) Get current page content and available actions from MCP
            try:
                # Use browser_evaluate to get page content
                page_content_result = await self.playwright_mcp_service.session.call_tool("browser_evaluate", {"expression": "document.documentElement.outerHTML"})
                page_content = page_content_result.get('content', '') if isinstance(page_content_result, dict) else str(page_content_result)
                # List of available Playwright MCP tools
                available_tools = ["browser_navigate", "browser_click", "browser_type", "browser_evaluate", "browser_wait_for_selector", "browser_screenshot"]
            except Exception as e:
                print(f"Error getting page content from MCP: {e}")
                break
            
            # 2) Create prompt for LLM
            modified_user_prompt = self._create_user_prompt(user_prompt, page_content, available_tools)
            self.context.append({
                "role": "user",
                "content": modified_user_prompt
            })
            
            # 3) Get next best action from LLM
            try:
                llm_response = await asyncio.to_thread(
                    self.llm_service.generate_response,
                    [{
                        "role": "system",
                        "content": self._default_system_prompt()
                    }, {
                        "role": "user",
                        "content": modified_user_prompt
                    }]
                )
                self.context.append({
                    "role": "assistant",
                    "content": llm_response
                })
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
                    print(f"Error executing MCP action {action_tool}: {e}")
                    # Continue to next iteration even if action fails
            
            # Check for stopping condition (to be implemented)
            done = self._check_stopping_condition()

        # Clean up MCP service
        await self.playwright_mcp_service.stop()


async def main():
    # Example usage
    automation = LLMMCPAutomation()

    # Example user prompt - you can modify this
    user_prompt = "Navigate to a website and perform a task"

    try:
        await automation.automate(user_prompt)
    except KeyboardInterrupt:
        print("\nAutomation interrupted by user")
    except Exception as e:
        print(f"Error during automation: {e}")


if __name__ == "__main__":
    asyncio.run(main())