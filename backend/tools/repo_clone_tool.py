import subprocess
import shutil
import os


def clone_repository(repo_url):

    print("\n===== CLONING REPOSITORY =====\n")

    # FOLDER NAME
    repo_name = repo_url.split("/")[-1].replace(".git", "")

    # CLONE LOCATION
    clone_path = f"./cloned_repos/{repo_name}"

    # DELETE OLD COPY IF EXISTS
    if os.path.exists(clone_path):

        shutil.rmtree(clone_path)

    # CREATE cloned_repos FOLDER
    os.makedirs("./cloned_repos", exist_ok=True)

    # GIT CLONE
    subprocess.run(
        ["git", "clone", repo_url, clone_path],
        check=True
    )

    print(f"\nRepository cloned at: {clone_path}")

    return clone_path