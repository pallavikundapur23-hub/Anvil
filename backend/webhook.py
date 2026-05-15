from fastapi import APIRouter
from fastapi import Request
from fastapi import BackgroundTasks
# =========================
# AGENTS
# =========================
from agents.planner import planner_agent
from agents.repository_map_agent import repository_map_agent
from agents.code_search_agent import code_search_agent
from agents.patch_agent import patch_agent
from agents.verifier_agent import verifier_agent
from agents.github_comment_agent import github_comment_agent
# =========================
# TOOLS
# =========================
from tools.repo_clone_tool import clone_repository
from tools.code_editor import fix_login_bug
from tools.git_commit_tool import create_git_commit
router = APIRouter()
# =========================================================
# MAIN AI PIPELINE
# =========================================================
def run_ai_pipeline(
 repo_name,
 repo_url,
 issue_number,
 full_issue
):
 print("\n===== AI PIPELINE STARTED =====\n")
 try:
 # =========================================================
 # CLONE REPOSITORY
 # =========================================================
    repo_path = clone_repository(repo_url)
    print("\n===== REPOSITORY CLONED =====\n")
    print(repo_path)
 # =========================================================
 # REPOSITORY MAP AGENT
 # =========================================================
    repo_map_result = repository_map_agent(
    full_issue
    )
 # =========================================================
 # PLANNER AGENT
 # =========================================================
    planner_result = planner_agent(
    full_issue
    )
 # =========================================================
 # CODE SEARCH AGENT
 # =========================================================
    code_result = code_search_agent(
    full_issue
    )
 # =========================================================
 # PATCH AGENT
 # =========================================================
    patch_result = patch_agent(
    full_issue
    )
 # =========================================================
 # VERIFIER AGENT
 # =========================================================
    verification_result = verifier_agent(
    patch_result
    )
 # =========================================================
 # CODE FIX
 # =========================================================
    fix_result = fix_login_bug(
    repo_path
    )
    print("\n===== FIX RESULT =====\n")
    print(fix_result)
 # =========================================================
 # GIT COMMIT
 # =========================================================
    commit_result = create_git_commit(
    repo_path
    )
    print("\n===== COMMIT RESULT =====\n")
    print(commit_result)
    # =========================================================
    # FINAL COMMENT
    # =========================================================
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
 # =========================================================
 # GITHUB COMMENT AGENT
 # =========================================================
    github_comment_agent(
 repo_name,
 issue_number,
 final_comment
 )
    print("\n===== GITHUB COMMENT POSTED =====\n")
 except Exception as e:
    print("\n===== BACKGROUND PIPELINE ERROR =====\n")
    print(str(e))
    print("\n===== AI PIPELINE COMPLETED =====\n")
# =========================================================
# WEBHOOK ENDPOINT
# =========================================================
@router.post("/github-webhook")
async def github_webhook(
 request: Request,
 background_tasks: BackgroundTasks
):
    try:
        payload = await request.json()
        print("\n===== WEBHOOK RECEIVED =====\n")
        # IGNORE NON-ISSUE EVENTS
        if "issue" not in payload:
            return {
                "message": "Not an issue event"
            }

        # =========================================================
        # EXTRACT ISSUE DATA
        # =========================================================
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
        # =========================================================
        # START BACKGROUND TASK
        # =========================================================
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
    except Exception as e:
        print("\n===== WEBHOOK ERROR =====\n")
        print(str(e))
        return {
            "status": "error",
            "message": str(e)
        }
