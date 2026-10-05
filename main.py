import os
import getpass
from encryptor import encrypt_file
from decryptor import decrypt_file


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def main():
    while True:
        clear_screen()
        print("=" * 45)
        print("     FILE ENCRYPTION & DECRYPTION TOOL")
        print("=" * 45)
        print("1. Encrypt a file")
        print("2. Decrypt a file")
        print("3. Exit")
        print("-" * 45)

        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            print("\n--- ENCRYPT FILE ---")
            file_path = input("Enter the path of the file to encrypt: ").strip()
            password = getpass.getpass("Enter password: ")   # ← Password is hidden

            if not file_path or not password:
                print("\nError: File path and password cannot be empty.")
                input("\nPress Enter to continue...")
                continue

            try:
                output = encrypt_file(file_path, password)
                print(f"\nSuccess! Encrypted file created: {output}")
            except Exception as e:
                print(f"\nError: {e}")

            input("\nPress Enter to continue...")

        elif choice == "2":
            print("\n--- DECRYPT FILE ---")
            file_path = input("Enter the path of the .enc file: ").strip()
            password = getpass.getpass("Enter password: ")   # ← Password is hidden

            if not file_path or not password:
                print("\nError: File path and password cannot be empty.")
                input("\nPress Enter to continue...")
                continue

            try:
                output = decrypt_file(file_path, password)
                print(f"\nSuccess! Decrypted file created: {output}")
            except Exception as e:
                print(f"\nError: {e}")

            input("\nPress Enter to continue...")

        elif choice == "3":
            print("\nThank you for using the tool. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please enter 1, 2 or 3.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()