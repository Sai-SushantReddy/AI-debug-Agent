def analyze_code_tool(code):
    """
    Takes code with error and prepares a structured prompt
    """
    return f"""
    You are an expert debugging assistant.

    Analyze the following code carefully.

    Tasks:
    1. Identify the error
    2. Explain why the issue occurs
    3. Provide corrected code
    4. Suggest improvements if possible

    Code:
    {code}
    """