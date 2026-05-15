from groq import Groq
from dotenv import load_dotenv
import os

from tools.file_reader import read_project_files

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def code_search_agent(issue_text):

    print("\n===== CODE SEARCH AGENT RUNNING =====\n")

    project_files = read_project_files()

    prompt = f"""
You are a backend code search AI.

IMPORTANT:
- ONLY use the repository files provided.
- DO NOT invent new files.
- Use only actual Python backend files.

GitHub Issue:
{issue_text}

ACTUAL REPOSITORY FILES:
{project_files}

TASK:
Identify:
1. Most relevant buggy file
2. Related helper files
3. Validation-related code
4. Authentication-related code

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

    print("\n===== CODE SEARCH RESULT =====\n")
    print(result)

    return result