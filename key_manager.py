import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# Constants
SALT_LENGTH = 16          # 16 bytes = 128 bits (standard & secure)
KEY_LENGTH = 32           # 32 bytes = 256 bits (required by Fernet)
ITERATIONS = 100_000      # Minimum recommended value (can be increased)


def generate_salt() -> bytes:
    """
    Generate a cryptographically secure random 16-byte salt.
    """
    return os.urandom(SALT_LENGTH)


def derive_key(password: str, salt: bytes) -> bytes:
    """
    Derive a 32-byte Fernet-compatible key from a password + salt
    using PBKDF2-HMAC-SHA256.

    Args:
        password: The user's password (string)
        salt: 16-byte random salt

    Returns:
        A URL-safe base64-encoded 32-byte key (ready for Fernet)
    """
    if not isinstance(password, str) or len(password) == 0:
        raise ValueError("Password cannot be empty")

    if not isinstance(salt, bytes) or len(salt) != SALT_LENGTH:
        raise ValueError(f"Salt must be exactly {SALT_LENGTH} bytes")

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_LENGTH,
        salt=salt,
        iterations=ITERATIONS,
        backend=default_backend()
    )

    # Derive the raw key and encode it the way Fernet expects
    key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
    return key


def validate_key(key: bytes) -> bool:
    """
    Validate that the derived key is the correct length for Fernet.
    Fernet keys must be 32 bytes after base64 decoding (44 characters when encoded).
    """
    try:
        decoded = base64.urlsafe_b64decode(key)
        return len(decoded) == KEY_LENGTH
    except Exception:
        return False


def save_salt(salt: bytes, filepath: str) -> None:
    """
    Optional helper: Save salt to a separate file (rarely needed,
    because we normally prepend the salt to the encrypted file).
    """
    with open(filepath, "wb") as f:
        f.write(salt)


def load_salt(filepath: str) -> bytes:
    """
    Optional helper: Load salt from a separate file.
    """
    with open(filepath, "rb") as f:
        salt = f.read()
    if len(salt) != SALT_LENGTH:
        raise ValueError("Invalid salt length in file")
    return salt


# ------------------------------------------------------------
# Quick self-test (you can run this file directly)
# ------------------------------------------------------------
if __name__ == "__main__":
    print("=== Testing Key Manager ===")

    password = "MySecurePassword123"
    salt = generate_salt()
    print(f"Generated salt ({len(salt)} bytes): {salt.hex()}")

    key = derive_key(password, salt)
    print(f"Derived key: {key.decode()}")

    is_valid = validate_key(key)
    print(f"Key is valid: {is_valid}")

    # Test that same password + salt always gives same key
    key2 = derive_key(password, salt)
    print(f"Keys match: {key == key2}")
