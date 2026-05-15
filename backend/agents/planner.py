from groq import Groq
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Read API key
api_key = os.getenv("GROQ_API_KEY")

# Create Groq client
client = Groq(api_key=api_key)

def planner_agent(issue_text):

    print("\n===== PLANNER AGENT RUNNING =====\n")

    prompt = f"""
    You are a senior software engineer.

    Analyze this GitHub issue and create debugging steps.

    GitHub Issue:
    {issue_text}

    Return:
    1. Possible cause
    2. Files to inspect
    3. Suggested debugging steps
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

    ai_result = response.choices[0].message.content

    print("\n===== AI RESPONSE =====\n")
    print(ai_result)

    return ai_result