from src.config import WEBSITE_URL

# System prompt defining the agent's role and behavior
def default_system_prompt() -> str:
    website = WEBSITE_URL
    return """# Web Automation Specialist
    You are an expert web automation agent using Playwright MCP tools to complete tasks on **{website}**.

    ## YOUR ROLE
    - Analyze the current page state and user goal
    - Select the optimal single action from available MCP tools and page content
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

    ## RESPONSE FORMAT ( RESPONSE SHOULD ALWAYS BE IN BELOW JSON FORMAT NOT ANYTHING ELSE )
    
    Return ONLY valid JSON WHICH PLAYWRIGHT MCP EXPECTS FOR TOOL CALL:
    
    IF ACTION IS TO BE TAKEN:
    
    ```
    {{
    "tool": "tool_name",
    "params": {{"param": "value"}},
    "reasoning": "Clear explanation of why this action moves us toward the goal"
    }}```
    
    ELSE IF no suitable action exists, return:
    
    ```
    {{
    "tool": "none",
    "reasoning": "Specific explanation why no action is appropriate"
    }}```
    """.format(website=website)

def create_user_prompt(user_prompt: str, page_content, available_tools, actions_performed) -> str:
    return """
    Based on the GOAL, CURRENT PAGE CONTENT, AVAILABLE TOOLS, and ACTIONS ALREADY PERFORMED determine the next best action to take.
    
    GOAL (USER PROMPT):
    {user_prompt}

    CURRENT PAGE CONTENT TAKEN FROM PLAYWRIGHT MCP:
    {page_content}

    AVAILABLE TOOLS TAKEN FROM PLAYWRIGHT MCP:
    {available_tools}
    
    STEPS ALREADY TAKEN or PERFORMED PREVIOUSLY IN THIS SESSION TO BE NOT REPEATED:
    {actions_performed}

    ## RESPONSE FORMAT ( RESPONSE SHOULD ALWAYS BE IN BELOW JSON FORMAT NOT ANYTHING ELSE )
    
    Return ONLY valid JSON WHICH PLAYWRIGHT MCP EXPECTS FOR TOOL CALL:
    
    IF ACTION IS TO BE TAKEN:
    
    ```
    {{
    "tool": "tool_name",
    "params": {{"param": "value"}},
    "reasoning": "Clear explanation of why this action moves us toward the goal"
    }}```
    
    ELSE IF no suitable action exists, return:
    
    ```
    {{
    "tool": "none",
    "reasoning": "Specific explanation why no action is appropriate"
    }}```
    
    NOTE: Always respond in the specified JSON format without additional text and explanations all should be in reasoning if any extra texts are to be be added becasue I want response only in the JSON formats which I have provided.
    """.format(
        user_prompt=user_prompt,
        page_content=page_content,
        available_tools=available_tools,
        actions_performed=actions_performed
    )