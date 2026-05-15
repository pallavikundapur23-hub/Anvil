import requests
import os
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def github_comment_agent(repo_name, issue_number, comment_text):

    print("\n===== GITHUB COMMENT AGENT RUNNING =====\n")

    url = f"https://api.github.com/repos/{repo_name}/issues/{issue_number}/comments"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    data = {
        "body": comment_text
    }

    response = requests.post(
        url,
        headers=headers,
        json=data
    )

    print("GitHub Status Code:", response.status_code)

    print("GitHub Response:")
    print(response.json())

    return response.json()