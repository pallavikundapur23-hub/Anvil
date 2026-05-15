from fastapi import APIRouter, Request
from agents.planner import planner_agent

router = APIRouter()

@router.post("/github-webhook")
async def github_webhook(request: Request):

    try:
        payload = await request.json()

        print("\n===== FULL PAYLOAD =====")
        print(payload)

        # Check if issue exists
        if "issue" not in payload:
            return {"message": "Not an issue event"}

        issue_title = payload["issue"].get("title", "")
        issue_body = payload["issue"].get("body", "")

        print("\n===== ISSUE RECEIVED =====")
        print("Title:", issue_title)
        print("Body:", issue_body)

        # Run agent
        result = planner_agent(issue_title)

        print("\n===== AGENT OUTPUT =====")
        print(result)

        return {
            "status": "success",
            "agent_result": result
        }

    except Exception as e:
        print("\nERROR:")
        print(str(e))

        return {
            "status": "error",
            "message": str(e)
        }