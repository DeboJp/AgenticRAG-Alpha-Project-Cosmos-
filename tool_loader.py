# tool_loader.py
import json

"""
Loads the source code of the specified tools by reading their .py files based on names 
listed in the tool index. Returns the combined code as a single string.
"""
def load_tool_code(tool_names, index_path="tools/index.json"):
    with open(index_path, "r") as f:
        tools = json.load(f)

    code_blocks = []
    for tool in tools:
        if tool["name"] in tool_names:
            with open(tool["path"], "r") as tf:
                code_blocks.append(tf.read())

    return "\n\n".join(code_blocks)
