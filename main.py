# main.py
from task_router import index_tools, match_tools

# Step 1: Index the tools
index_tools()

task = "search something on the internet"
print(f"Task: {task}")

matched = match_tools(task)
print(f"Best Matching Tools: {matched}")
