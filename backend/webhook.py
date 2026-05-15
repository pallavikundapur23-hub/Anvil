from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Request

from agents.code_search_agent import code_search_agent
from agents.github_comment_agent import github_comment_agent
from agents.patch_agent import patch_agent
from agents.planner import planner_agent
from agents.repository_map_agent import repository_map_agent
from agents.verifier_agent import verifier_agent
from tools.file_reader import read_project_files
from tools.repo_clone_tool import clone_repository


router = APIRouter()


def run_ai_pipeline(
    repo_name,
    repo_url,
    issue_number,
    full_issue
):
    print("\n===== AI PIPELINE STARTED =====\n")

    try:
        repo_path = clone_repository(repo_url)
        print("\n===== REPOSITORY CLONED =====\n")
        print(repo_path)

        repo_context = read_project_files(
            repo_path,
            full_issue
        )
        print("\n===== REPOSITORY CONTEXT READY =====\n")

        repo_map_result = repository_map_agent(
            full_issue,
            repo_context
        )

        planner_result = planner_agent(
            full_issue,
            repo_context
        )

        code_result = code_search_agent(
            full_issue,
            repo_context
        )

        patch_result = patch_agent(
            full_issue,
            repo_context
        )

        verification_result = verifier_agent(
            full_issue,
            patch_result,
            repo_context
        )

        fix_result = (
            "No automatic code edit was applied. "
            "The current repository-agnostic pipeline posts grounded analysis "
            "and a patch suggestion only."
        )
        print("\n===== FIX RESULT =====\n")
        print(fix_result)

        commit_result = (
            "No commit created because no repository-agnostic code edit "
            "was applied."
        )
        print("\n===== COMMIT RESULT =====\n")
        print(commit_result)

        final_comment = f"""
# AI Debugging Analysis

## Repository Analysis
{repo_map_result}

---

## Planner Analysis
{planner_result}

---

## Code Search Result
{code_result}

---

## Suggested Patch
{patch_result}

---

## Verification Result
{verification_result}

---

## Code Diff
```diff
{fix_result}
```

---

## Git Commit Status
{commit_result}
"""

        github_comment_agent(
            repo_name,
            issue_number,
            final_comment
        )
        print("\n===== GITHUB COMMENT POSTED =====\n")

    except Exception as exc:
        print("\n===== BACKGROUND PIPELINE ERROR =====\n")
        print(str(exc))
    finally:
        print("\n===== AI PIPELINE COMPLETED =====\n")


@router.post("/github-webhook")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks
):
    try:
        payload = await request.json()
        print("\n===== WEBHOOK RECEIVED =====\n")

        if "issue" not in payload:
            return {
                "message": "Not an issue event"
            }

        issue_title = payload["issue"].get(
            "title",
            ""
        )
        issue_body = payload["issue"].get(
            "body",
            ""
        )
        repo_name = payload["repository"][
            "full_name"
        ]
        repo_url = payload["repository"][
            "clone_url"
        ]
        issue_number = payload["issue"][
            "number"
        ]

        full_issue = f"""
Title:
{issue_title}

Description:
{issue_body}
"""

        print("\n===== ISSUE DETAILS =====\n")
        print(full_issue)
        print("\n===== REPOSITORY URL =====\n")
        print(repo_url)

        background_tasks.add_task(
            run_ai_pipeline,
            repo_name,
            repo_url,
            issue_number,
            full_issue
        )

        return {
            "status": "AI pipeline started asynchronously"
        }

    except Exception as exc:
        print("\n===== WEBHOOK ERROR =====\n")
        print(str(exc))

        return {
            "status": "error",
            "message": str(exc)
        }
