# tool_loader.py
import json

"""
Loads the source code of the specified tools by reading their .py files based on names 
listed in the tool index. Returns the path of the starting helper code.
"""
def get_tool_path(tool_name, index_path="tools/index.json"):
    with open(index_path, "r") as f:
        tools = json.load(f)

    for tool in tools:
        if tool["name"] == tool_name:
            return tool["path"]

    raise ValueError(f"No tool named '{tool_name}' found in {index_path}")
