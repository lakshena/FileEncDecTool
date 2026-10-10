# File Encryption & Decryption Tool

A simple command-line tool that allows you to securely encrypt and decrypt any file using a password.

Once a file is encrypted, its contents become unreadable. Only someone who knows the correct password can decrypt it and restore the original file.

---
## Features

- Encrypt any file (text, PDF, image, etc.)
- Decrypt encrypted files using the same password
- Uses strong cryptography (Fernet + PBKDF2-HMAC-SHA256)
- Password is never stored in the encrypted file
- Clean command-line interface
- Password input is hidden while typing

---
## Project Structure

```
FileEncDecTool/
├── key_manager.py      # Handles salt generation and key derivation
├── encryptor.py        # Encrypts files
├── decryptor.py        # Decrypts files
├── main.py             # Main menu / CLI
└── README.md
```

---
## How It Works

### Encryption Process:
1. User provides a file and a password
2. A random 16-byte salt is generated
3. A secure key is derived from the password + salt using PBKDF2
4. The file is encrypted using Fernet
5. The salt is prepended to the encrypted data
6. A new file is created with `.enc` extension

### Decryption Process:
1. User provides the `.enc` file and the same password
2. The salt is extracted from the first 16 bytes
3. The key is re-derived using the password + salt
4. The file is decrypted and restored

---
## Requirements

- Python 3.7 or higher
- `cryptography` library

Install the required library:

```bash
pip install cryptography
```

---
## How to Run

```bash
python main.py
# or: python3 main.py
```

You will see a menu:

```
=============================================
     FILE ENCRYPTION & DECRYPTION TOOL
=============================================
1. Encrypt a file
2. Decrypt a file
3. Exit
---------------------------------------------
```

### Example Usage
**Encrypt a file:**
```
Enter your choice (1-3): 1
Enter the path of the file to encrypt: test.txt
Enter password: ********
Success! Encrypted file created: test.txt.enc
```

**Decrypt a file:**
```
Enter your choice (1-3): 2
Enter the path of the .enc file: test.txt.enc
Enter password: ********
Success! Decrypted file created: test.txt
```

---
## Important Notes

- The password is **never stored** in the encrypted file.
- Always remember your password. If you forget it, the file cannot be recovered.
- After encryption, you can safely delete the original file if you want.
- Make sure you enter the full name of the encrypted file (including `.enc`) while decrypting.

---

## Modules Explanation
| Module            | Responsibility                              |
|-------------------|---------------------------------------------|
| `key_manager.py`  | Generates salt and derives encryption key   |
| `encryptor.py`    | Encrypts files and creates `.enc` files     |
| `decryptor.py`    | Decrypts `.enc` files and restores original |
| `main.py`         | Provides a simple menu interface            |

---
