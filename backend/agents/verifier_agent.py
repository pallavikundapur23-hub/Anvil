from groq import Groq
from dotenv import load_dotenv
import os

from tools.file_reader import read_project_files

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def verifier_agent(patch_text):

    print("\n===== VERIFIER AGENT RUNNING =====\n")

    project_files = read_project_files()

    prompt = f"""
You are a backend verification AI.

IMPORTANT:
- ONLY use the repository files provided.
- DO NOT invent frameworks or files.
- Validate patch against actual Python backend code.

ACTUAL REPOSITORY FILES:
{project_files}

PATCH RESULT:
{patch_text}

TASKS:
1. Verify fix correctness
2. Identify possible risks
3. Suggest validation improvements
4. Identify remaining edge cases

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

    print("\n===== VERIFICATION RESULT =====\n")
    print(result)

    return result