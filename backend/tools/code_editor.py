from tools.git_diff_tool import generate_diff
import os


def fix_login_bug(repo_path):

    login_file = None

    # FIND login.py
    for root, dirs, files in os.walk(repo_path):

        if "login.py" in files:

            login_file = os.path.join(
                root,
                "login.py"
            )

            break

    # FILE NOT FOUND
    if login_file is None:

        return "login.py not found"

    # READ ORIGINAL CODE
    with open(login_file, "r") as f:

        original_code = f.read()

    print("\n===== ORIGINAL CODE =====\n")
    print(original_code)

    # APPLY FIX
    updated_code = original_code.replace(
        'raise Exception("Server Crash")',
        'return {"error": "Password required"}'
    )

    # WRITE UPDATED CODE
    with open(login_file, "w") as f:

        f.write(updated_code)

    print("\n===== UPDATED CODE =====\n")
    print(updated_code)

    # GENERATE DIFF
    diff_result = generate_diff(
        original_code,
        updated_code
    )

    print("\n===== GENERATED DIFF =====\n")
    print(diff_result)

    return diff_result