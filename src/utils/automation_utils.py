import re

def extract_json_from_response(response: str) -> str:
    # First, try to find JSON in code blocks
    code_block_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    matches = re.findall(code_block_pattern, response, re.DOTALL)
    if matches:
        return matches[0].strip()

    # Then, try to find JSON object directly in the response
    json_pattern = r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}'
    matches = re.findall(json_pattern, response, re.DOTALL)

    # Return the last match (most likely to be the complete JSON)
    if matches:
        return matches[-1].strip()

    # If no JSON found, return the original response
    return response.strip()

def extract_actions_performed(context: list[dict]) -> str:
    actions = []
    for message in context:
        if message['role'] == 'assistant':
            actions.append(message['content'])
    return "\n".join(actions)

def validate_llm_response(tool: str, parameters: dict, available_tools: list):
    if not tool or not isinstance(parameters, dict):
        raise KeyError("Invalid tool or params in LLM response")
    if tool not in available_tools and tool != "none":
        raise KeyError(f"Tool '{tool}' not in available tools: {available_tools}")