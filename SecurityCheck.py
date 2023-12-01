import re

def check_password_strength(password):
    """
    Check the strength of a password.
    Returns True if the password is strong, False otherwise.
    A strong password is defined as one that is at least 8 characters long,
    and contains both alphabets and numbers.
    """
    if len(password) < 8:
        return False

    # Check for the presence of both alphabets and numbers
    # Check for the presence of alphabets, numbers, and special characters
    if (re.search("[a-z]", password) and
        re.search("[A-Z]", password) and
        re.search("[0-9]", password) and
        re.search("[!@#$%^&*()_+]", password)):
        return True
    else:
        return False
    
def check_email(email):
    """
    Check if the email is valid.
    Returns True if the email is valid, False otherwise.
    """
    if re.search("[a-zA-Z0-9]+@[a-zA-Z]+\.[a-zA-Z]+", email):
        return True
    else:
        return False
