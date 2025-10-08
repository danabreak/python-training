import string


class WeakPasswordError(Exception):
    pass


def strong_password(password: str) -> bool:
    if len(password) >= 8:
        if any(ch.isupper() for ch in password):
            if any(ch.isdigit() for ch in password):
                if any(ch in string.punctuation for ch in password):
                    return True
                else:
                    raise WeakPasswordError(
                        "Password doesn't contain any special characters"
                    )
            else:
                raise WeakPasswordError("Password doesn't contain any digit")
        else:
            raise WeakPasswordError("Password doesn't contain an uppercase")
    else:
        raise WeakPasswordError("Password is too short")
