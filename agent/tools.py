def analyze_code_tool(code):
    """
    Takes code with error and prepares a structured prompt
    """
    return f"""
    You are a debugging assistant.

    Analyze the following code:
    - Identify errors
    - Explain the issue clearly
    - Provide corrected code

    Code:
    {code}
    """