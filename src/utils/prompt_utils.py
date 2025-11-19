from src.config import WEBSITE_URL

# System prompt defining the agent's role and behavior
def default_system_prompt() -> str:
    website = WEBSITE_URL
    return """# Web Automation Specialist
    You are an expert web automation agent using Playwright MCP tools to complete tasks on **{website}**.

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
    
    Return ONLY valid JSON WHICH PLAYWRIGHT MCP EXPECTS FOR TOOL CALL IF ACTION IS TO BE TAKEN:
    ```json
    {{
    "tool": "tool_name",
    "params": {{"param": "value"}},
    "reasoning": "Clear explanation of why this action moves us toward the goal"
    }}```
    
    ELSE IF no suitable action exists, return:
    ```json
    {{
    "tool": "none",
    "reasoning": "Specific explanation why no action is appropriate"
    }}```
    """.format(website=website)

def create_user_prompt(user_prompt: str, page_content, available_tools) -> str:
    return """
    Based on the GOAL, CURRENT PAGE CONTENT, and AVAILABLE TOOLS, determine the next best action to take.
    
    GOAL (USER PROMPT):
    {user_prompt}

    CURRENT PAGE CONTENT TAKEN FROM PLAYWRIGHT MCP:
    {page_content}

    AVAILABLE TOOLS TAKEN FROM PLAYWRIGHT MCP:
    {available_tools}

    ## RESPONSE FORMAT
    
    Return ONLY valid JSON WHICH PLAYWRIGHT MCP EXPECTS FOR TOOL CALL IF ACTION IS TO BE TAKEN:
    ```json
    {{
    "tool": "tool_name",
    "params": {{"param": "value"}},
    "reasoning": "Clear explanation of why this action moves us toward the goal"
    }}```
    
    ELSE IF no suitable action exists, return:
    ```json
    {{
    "tool": "none",
    "reasoning": "Specific explanation why no action is appropriate"
    }}```
    """.format(
        user_prompt=user_prompt,
        page_content=page_content,
        available_tools=available_tools
    )