import string

def check_password_strength(password):
    strength = {"length": False, "digits": False, "uppercase": False, "lowercase": False, "punctuation": False}

    if len(password) >= 8:
        strength["length"] = True
    if any(char.isdigit() for char in password):
        strength["digits"] = True
    if any(char.isupper() for char in password):
        strength["uppercase"] = True
    if any(char.islower() for char in password):
        strength["lowercase"] = True
    if any(char in string.punctuation for char in password):
        strength["punctuation"] = True

    return all(strength.values()), strength
