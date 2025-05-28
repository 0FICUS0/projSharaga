from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
from base64 import urlsafe_b64encode
import os

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    return urlsafe_b64encode(kdf.derive(password.encode()))

def generate_salt() -> bytes:
    return os.urandom(16)

def encrypt_note(text: str, key: bytes) -> bytes:
    fernet = Fernet(key)
    return fernet.encrypt(text.encode())

def decrypt_note(token: bytes, key: bytes) -> str:
    fernet = Fernet(key)
    return fernet.decrypt(token).decode()