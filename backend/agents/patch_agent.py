from tools.file_reader import read_project_files
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def patch_agent(issue_text):

    print("\n===== PATCH AGENT RUNNING =====\n")
    project_files = read_project_files()

    print("\n===== PROJECT FILES =====\n")
    print(project_files)
    prompt = f"""
You are an autonomous backend debugging AI.

IMPORTANT RULES:
- ONLY use the files provided below.
- DO NOT invent new files.
- DO NOT mention Java, Flask, Express.js, or other frameworks.
- The project is a simple Python backend.
- Use ONLY the actual repo files provided.

GitHub Issue:
{issue_text}

ACTUAL REPOSITORY FILES:
{project_files}

TASKS:
1. Identify root cause
2. Identify EXACT buggy file
3. Explain buggy code
4. Suggest corrected code
5. Suggest validation improvements

Return concise technical analysis.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    print("\n===== PATCH SUGGESTION =====\n")
    print(result)

    return result