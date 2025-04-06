# main.py
from task_router import index_tools, match_tools
from tool_loader import load_tool_code
from gemini_agent import generate_script
from runner import run_generated_script


# Step 1: Index the tools
index_tools()

task = "search distance from oliv madison to computer science building on google maps. use maps.google.com"
print(f"Task: {task}")

tool_names_matched = match_tools(task)
print(f"Best Matching Tools: {tool_names_matched}")
# print(tool_names_matched)
# Load tool code
tool_code = load_tool_code(tool_names_matched[0])

# Generate final script
script = generate_script(task, tool_code)

# Show generated result
print("\n🧾 Generated Script:\n")
print(script)

driver = None
stdout, stderr = run_generated_script(script)

print("\n📤 Script Output:\n")
print(stdout)

if stderr:
    print("\n⚠️ Script Errors:\n")
    print(stderr)
