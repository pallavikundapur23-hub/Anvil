import subprocess


def create_git_commit(repo_path):

    try:

        # GIT ADD
        subprocess.run(
            ["git", "add", "."],
            cwd=repo_path,
            check=True
        )

        # GIT COMMIT
        subprocess.run(
            [
                "git",
                "commit",
                "-m",
                "AI AutoFix patch"
            ],
            cwd=repo_path,
            check=True
        )

        print("\n===== GIT COMMIT CREATED =====\n")

        return "Git commit created successfully"

    except Exception as e:

        print("\n===== GIT COMMIT ERROR =====\n")
        print(str(e))

        return str(e)