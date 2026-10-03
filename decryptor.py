import os
from cryptography.fernet import Fernet, InvalidToken
from key_manager import derive_key   # Student 1's function

def decrypt_file(encrypted_path: str, password: str, output_path: str = None) -> None:
    """
    Decrypt a .enc file created by the encryption module.

    Args:
        encrypted_path: Path to the encrypted file (must end with .enc)
        password: The password used during encryption
        output_path: Optional path for the decrypted file.
                     If None, the .enc extension is removed.
    """

    # --- 1. Basic checks ---
    if not os.path.isfile(encrypted_path):
        raise FileNotFoundError(f"Encrypted file not found: {encrypted_path}")

    if not encrypted_path.lower().endswith(".enc"):
        print("Warning: File does not have .enc extension")

    # --- 2. Read the entire encrypted file ---
    with open(encrypted_path, "rb") as f:
        data = f.read()

    if len(data) < 16:
        raise ValueError("File is too small or corrupted (missing salt)")

    # --- 3. Extract salt (first 16 bytes) and ciphertext ---
    salt = data[:16]
    ciphertext = data[16:]

    # --- 4. Derive the key using Student 1's function ---
    key = derive_key(password, salt)

    # --- 5. Decrypt with Fernet ---
    try:
        fernet = Fernet(key)
        plaintext = fernet.decrypt(ciphertext)
    except InvalidToken:
        raise ValueError("Decryption failed: wrong password or file has been tampered with.")

    # --- 6. Decide output filename ---
    if output_path is None:
        # Remove .enc extension
        if encrypted_path.lower().endswith(".enc"):
            output_path = encrypted_path[:-4]
        else:
            output_path = encrypted_path + ".decrypted"

    # --- 7. Write the original file ---
    with open(output_path, "wb") as f:
        f.write(plaintext)

    print(f"✓ Decryption successful!")
    print(f"  Output file → {os.path.abspath(output_path)}")


# ------------------------------------------------------------
# Simple CLI for testing (you can remove this later)
# ------------------------------------------------------------
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python decryptor.py <file.enc> <password> [output_file]")
        sys.exit(1)

    enc_file = sys.argv[1]
    password = sys.argv[2]
    out_file = sys.argv[3] if len(sys.argv) > 3 else None

    try:
        decrypt_file(enc_file, password, out_file)
    except (FileNotFoundError, ValueError) as e:
        print(f"✗ Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")
