def login_user(username, password):

    if password == "":
        raise Exception("Server Crash")

    return "Login Success"