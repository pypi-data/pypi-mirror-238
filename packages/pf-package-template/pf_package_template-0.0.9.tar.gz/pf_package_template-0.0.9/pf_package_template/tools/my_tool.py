from promptflow import tool

@tool
def example_python_tool(input_text: str) -> str:
    return "Your prompt was: " + input_text