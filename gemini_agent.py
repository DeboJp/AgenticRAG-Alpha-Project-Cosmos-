# gemini_agent.py - not in use.
import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(f"models/{os.getenv('MODEL_NAME')}")

"""
Uses Gemini to generate a runnable Python script based on a task and tool code.
"""
def generate_script(task, tool_code):
    prompt = f"""
        You are an intelligent developer assistant.

        Your goal is to write a Python script that solves the following task:

        TASK:
        {task}

        You have access to the following TOOL:
        {tool_code}

        Write a runnable Python script that uses this tool to complete the task. 
        The tool is a mere template, edit it to maintain the task. But do minimal changes where possible.
        Do not explain anything—just output the script.
    """

    response = model.generate_content(prompt)
    print(response.text.strip())
    return response.text.strip()
