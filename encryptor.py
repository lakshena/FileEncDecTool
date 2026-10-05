from cryptography.fernet import Fernet
from key_manager import generate_salt, derive_key, validate_key


def encrypt_file(file_path: str, password: str) -> str:
    """
    Encrypt a file using a password.

    The first 16 bytes of the output file contain the salt.
    The remaining bytes contain the Fernet-encrypted data.
    """

    try:
        # Generate a random salt
        salt = generate_salt()

        # Derive a Fernet-compatible key from the password and salt
        key = derive_key(password, salt)

        # Validate the derived key
        if not validate_key(key):
            raise ValueError("Invalid encryption key generated.")

        # Create Fernet cipher
        fernet = Fernet(key)

        # Read the original file in binary mode
        with open(file_path, "rb") as file:
            data = file.read()

        # Encrypt the file data
        encrypted_data = fernet.encrypt(data)

        # Create output filename
        output_path = file_path + ".enc"

        # Store salt first, followed by encrypted data
        with open(output_path, "wb") as file:
            file.write(salt)
            file.write(encrypted_data)

        return output_path

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    except PermissionError:
        raise PermissionError(f"Permission denied: {file_path}")

    except OSError as e:
        raise OSError(f"File operation failed: {e}")


if __name__ == "__main__":
    print("Encryption module loaded successfully.")