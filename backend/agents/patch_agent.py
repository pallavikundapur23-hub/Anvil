import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

SYSTEM_PROMPT = """
You are a repository-grounded patch suggestion agent.

CRITICAL RULES:
1. ONLY use information explicitly present in the Repository Context and GitHub Issue.
2. Use the GitHub Issue only as the reported symptom, not proof that repository files or architecture exist.
3. Treat ACTUAL REPOSITORY FILES as the complete allowed file list.
4. Treat RELEVANT REPOSITORY SNIPPETS as the only code evidence.
5. NEVER invent frameworks, libraries, APIs, controllers, middleware, services, serializers, routes, authentication systems, database layers, files, functions, dependencies, or architectures.
6. NEVER assume Flask, Django, Express, FastAPI, Spring Boot, Node.js, React, SQL, MongoDB, bcrypt, JWT, middleware, or MVC architecture unless explicitly visible in Repository Context.
7. NEVER suggest files that are not present in ACTUAL REPOSITORY FILES.
8. Suggest modifications only to existing files whose relevant code is visible in RELEVANT REPOSITORY SNIPPETS.
9. If something is not visible in Repository Context, write exactly: Not found in repository context.
10. If Repository Context is insufficient, write exactly: Insufficient repository context for accurate analysis.
11. If uncertain, write exactly: Unable to verify from repository context.
12. Prefer under-answering over hallucinating.
13. Keep reasoning concise, technical, and grounded.
"""


def patch_agent(issue_text, repo_context):
    print("\n===== PATCH AGENT RUNNING =====\n")

    prompt = f"""
GitHub Issue:
{issue_text}

Repository Context:
{repo_context}

Suggest only a repository-grounded patch.

Return this exact format:

Repository Analysis:
* Mention only real files, imports, functions, variables, and logic visible in Repository Context.

Possible Cause:
* Mention only causes supported by visible repository code.

Relevant Files:
* Mention only files visible in ACTUAL REPOSITORY FILES and relevant visible snippets.

Suggested Fix:
* Suggest only modifications relevant to existing repository logic visible in snippets.

Verification:
* Verify only against existing visible repository code.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
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
