import os
import base64
import hashlib

def generate_salt() -> bytes:
    """Generate a random 16-byte cryptographic salt."""
    return os.urandom(16)

def derive_key(password: str, salt: bytes, iterations: int = 100_000) -> bytes:
    """
    Derive a key from password + salt using PBKDF2-HMAC-SHA256.
    Returns a URL-safe base64-encoded 32-byte key compatible with Fernet.
    """
    raw_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        iterations,
        dklen=32
    )
    return base64.urlsafe_b64encode(raw_key)

def validate_key(key: bytes) -> bool:
    """Validate that the derived key decodes to the correct 32-byte length."""
    try:
        decoded = base64.urlsafe_b64decode(key)
        return len(decoded) == 32
    except Exception:
        return False