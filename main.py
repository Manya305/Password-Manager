import argparse
import getpass
import os
from db_manager import create_db, add_password, get_password
from encryption import generate_key, load_key, encrypt_message, decrypt_message

def add_new_password(service, username, password, fernet_key):
    encrypted_password = encrypt_message(password, fernet_key)
    add_password(service, username, encrypted_password)
    print("Password added successfully.")

def retrieve_password(service, fernet_key):
    result = get_password(service)
    if result:
        username_hash, encrypted_password = result
        decrypted_password = decrypt_message(encrypted_password, fernet_key)
        print(f"Username hash: {username_hash}")
        print(f"Password: {decrypted_password}")
    else:
        print("Service not found.")

def main():
    parser = argparse.ArgumentParser(description='Password Manager')
    parser.add_argument('action', choices=['add', 'get'], help='Action to perform')
    parser.add_argument('--service', required=True, help='Service name')
    parser.add_argument('--username', help='Username (required for adding a new password)')
    args = parser.parse_args()

    create_db()

    master_password = getpass.getpass("Enter the master password: ")

    if not os.path.exists("secret.key"):
        fernet_key = generate_key(master_password)
    else:
        fernet_key = load_key(master_password)

    if args.action == 'add':
        if not args.username:
            print("Username is required for adding a new password.")
            return
        password = getpass.getpass("Enter the password: ")
        add_new_password(args.service, args.username, password, fernet_key)
    elif args.action == 'get':
        retrieve_password(args.service, fernet_key)

if __name__ == "__main__":
    main()


 # master password = abcdef@123