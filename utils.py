import hashlib


def hash_password(password: str) -> str:
    """Хэширует пароль с использованием SHA-512"""
    binary_password: bytes = password.encode()
    hashed_password: str = hashlib.sha512(binary_password).hexdigest()
    return hashed_password
