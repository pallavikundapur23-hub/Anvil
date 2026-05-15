def login_user(username, password):

    # ❌ Bug: wrong logic
    if password:
        return {"error": "Password required"}

    return "Login Success"