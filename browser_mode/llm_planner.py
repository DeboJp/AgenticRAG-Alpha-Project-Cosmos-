# llm_planner.py
"""
Uses Gemini to plan the next single browser action based on
current task and browser page state.
"""

import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(f"models/{os.getenv('MODEL_NAME')}")

def clean_json_block(text):
    if text.startswith("```"):
        return "\n".join(text.strip().split("\n")[1:-1])
    return text.strip()

def get_next_action(task, browser_state, prev_state=None, prev_action=None):
    prompt = f"""
You are a web automation agent. You help perform the task step-by-step using only what’s currently visible in the browser.

TASK:
"{task}"

--- CONTEXT FROM PREVIOUS STEP ---
PREVIOUS PAGE STATE:
{prev_state if prev_state else "None"}

PREVIOUS ACTION:
{json.dumps(prev_action) if prev_action else "None"}

--- IMPORTANT CONTEXT FOR CURRENT STEP ---

CURRENT PAGE STATE:
{browser_state}

RULES:
- First try to see if after action from previous step changed anything on current step. If not you might want to consider something different.
- If the input contains the query and the page is still the homepage, press Enter.
- If you already clicked something and it led to no page change, try a different element.
If the current URL contains "/search", do not immediately assume the task is done. Look for 
specific keywords or signs in the page content to determine if the task has been fulfilled.
- If you believe the current page state is what the user is looking for, you can report done.

Choose one of the following actions:
- type (provide selector and value)
- click (provide selector)
- press_enter (provide selector)
- done (if the task is complete)

Respond ONLY with a JSON object like:
{{ "action": "type", "selector": "[name='q']", "value": "example text" }}

If no further action is needed, respond with:
{{ "action": "done" }}
"""

    response = model.generate_content(prompt)

    try:
        raw = response.text.strip()
        print(task, browser_state, raw)
        cleaned = clean_json_block(raw)
        action_json = json.loads(cleaned)
        print("🤖 Next action:", action_json)

    except Exception as e:
        print("⚠️ Failed to parse LLM output:\n", response.text)
        raise e

    return action_json
