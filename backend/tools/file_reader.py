import os


def read_project_files():

    # TARGET REPOSITORY
    repo_path = "../../buggy-todo-api"

    formatted_context = ""

    discovered_files = []

    # ALLOWED FILE TYPES
    allowed_extensions = [
        ".py",
        ".js",
        ".ts",
        ".java"
    ]

    print("\n===== SCANNING REPOSITORY FILES =====\n")

    # WALK THROUGH REPOSITORY
    for root, dirs, files in os.walk(repo_path):

        for file in files:

            # CHECK EXTENSION
            if any(
                file.endswith(ext)
                for ext in allowed_extensions
            ):

                file_path = os.path.join(root, file)

                discovered_files.append(file)

                try:

                    with open(
                        file_path,
                        "r",
                        encoding="utf-8"
                    ) as f:

                        code = f.read()

                        print(f"Reading File: {file_path}")

                        formatted_context += f"""

FILE: {file}

FULL PATH:
{file_path}

CODE:
{code}

========================================
"""

                except Exception as e:

                    print(
                        f"Error reading {file_path}: {e}"
                    )

    # CREATE FILE LIST STRING
    discovered_files_text = "\n".join(discovered_files)

    # FINAL REPO CONTEXT
    final_context = f"""
ACTUAL REPOSITORY FILES:
{discovered_files_text}

========================================

REPOSITORY CODEBASE:
{formatted_context}
"""

    return final_context