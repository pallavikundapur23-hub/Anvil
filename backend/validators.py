def validate_email(email):

    if "@" not in email:
        return False

    return True