import os
from cryptography.fernet import Fernet, InvalidToken
from key_manager import derive_key


def decrypt_file(encrypted_path: str, password: str, output_path: str = None) -> str:
    """
    Decrypt a file that was encrypted using the encryptor module.

    The first 16 bytes of the encrypted file contain the salt.
    The remaining bytes contain the Fernet-encrypted data.
    """

    try:
        # Check if the encrypted file exists
        if not os.path.isfile(encrypted_path):
            raise FileNotFoundError(f"Encrypted file not found: {encrypted_path}")

        # Read the entire encrypted file
        with open(encrypted_path, "rb") as file:
            data = file.read()

        if len(data) < 16:
            raise ValueError("File is too small or corrupted (missing salt).")

        # Extract salt (first 16 bytes) and the encrypted content
        salt = data[:16]
        encrypted_data = data[16:]

        # Derive the key using the same method as encryption
        key = derive_key(password, salt)

        # Decrypt the data
        fernet = Fernet(key)
        decrypted_data = fernet.decrypt(encrypted_data)

        # Decide the output filename
        if output_path is None:
            if encrypted_path.lower().endswith(".enc"):
                output_path = encrypted_path[:-4]          # remove .enc
            else:
                output_path = encrypted_path + ".decrypted"

        # Write the original file back
        with open(output_path, "wb") as file:
            file.write(decrypted_data)

        return output_path

    except InvalidToken:
        raise ValueError("Decryption failed: Wrong password or file has been tampered with.")

    except FileNotFoundError as e:
        raise FileNotFoundError(str(e))

    except PermissionError:
        raise PermissionError(f"Permission denied while accessing: {encrypted_path}")

    except OSError as e:
        raise OSError(f"File operation failed: {e}")


if __name__ == "__main__":
    print("Decryption module loaded successfully.")
