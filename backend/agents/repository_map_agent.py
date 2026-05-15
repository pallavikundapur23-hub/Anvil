from groq import Groq
from dotenv import load_dotenv
import os

from tools.file_reader import read_project_files

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def repository_map_agent(issue_text):

    print("\n===== REPOSITORY MAP AGENT RUNNING =====\n")

    repo_context = read_project_files()

    prompt = f"""
You are a repository analysis AI.

You must ONLY use the repository files provided.

GitHub Issue:
{issue_text}

REPOSITORY CONTEXT:
{repo_context}

TASKS:
1. List actual repository files
2. Identify relevant files for this issue
3. Explain why those files are relevant
4. Ignore unrelated files

IMPORTANT:
- DO NOT invent frameworks
- DO NOT invent controllers/services
- ONLY use discovered files

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

    print("\n===== REPOSITORY MAP RESULT =====\n")
    print(result)

    return result