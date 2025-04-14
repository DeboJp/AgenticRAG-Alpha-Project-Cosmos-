# agentic_loop.py
"""
Main agent loop that drives the browser step-by-step based on
LLM guidance using Gemini and real-time browser state.
"""

from browser_controller import BrowserController
from llm_planner import get_next_action

def run_task(task, browser=None):
    if browser is None:
        browser = BrowserController()
        browser.navigate("https://www.google.com")  # start from Google

    action_history = []

    try:
        while True:
            state = browser.get_state()

            action = get_next_action(task, state)

            if action in action_history[-3:]:
                print("⚠️ Detected repeated action. Stopping.")
                break

            if action["action"] == "done":
                print("✅ Agent considers task complete. You can take over or provide a new prompt.")
                break

            elif action["action"] == "click":
                browser.click(action["selector"])

            elif action["action"] == "type":
                browser.type(action["selector"], action["value"])

            elif action["action"] == "press_enter":
                browser.press_enter(action["selector"])

            else:
                print("⚠️ Unknown action:", action)
                break

            action_history.append(action)

            # Allow next steps even if on results page
            if "/search" in state["url"] and action["action"] == "press_enter":
                continue

    except Exception as e:
        print("💥 Agent failed:", str(e))

    print(action_history)
    return browser

if __name__ == "__main__":
    browser = None
    while True:
        task = input("🧠 Enter your next task (or type 'exit' to quit): ")
        if task.lower() == "exit":
            break
        browser = run_task(task, browser)

    if browser:
        print("🛑 Closing browser...")
        browser.quit()
