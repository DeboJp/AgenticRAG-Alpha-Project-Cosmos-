from task_router import match_tools, index_tools
from tool_loader import get_tool_path
from gemini_agent import generate_script
from runner import run_tool
import time
# from selenium import webdriver
# import undetected_chromedriver as uc

index_tools()  # index once at start

print("🧠 ToolAgent is ready.")

while True:
    task = input("\n📥 What do you want to do? (type 'exit' to quit): ")
    if task.lower() == "exit":
        break

    matched = match_tools(task)
    if not matched:
        print("❌ No matching tool found.")
        continue

    tool_name = matched[0]
    print(f"🔧 Matched tool: {tool_name}")

    tool_code = get_tool_path(tool_name)

    print(f"\n▶️ Running tool {tool_code}\n")

    run_tool(tool_code)

#search distance from oliv madison to computer science building on google maps. use maps.google.com