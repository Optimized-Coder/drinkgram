# validation
import re

def validate_password(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$", password):
        raise ValueError("Password must contain at least one number, one uppercase letter, one lowercase letter, and one special character")
    else:
        return True
    
def validate_username(username):
    if len(username) < 4:
        raise ValueError("Username must be at least 4 characters long")
    if not re.match(r"^[a-zA-Z0-9_]{4,}$", username):
        raise ValueError("Username must contain only letters and numbers")
    else:
        return True

def validate_email(email):
    if not re.match(r"^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$", email):
        raise ValueError("Invalid email address")
    else:
        return True