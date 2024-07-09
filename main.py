import argparse
import getpass
import os
from db_manager import create_db, add_password, get_password, get_all_passwords, search_passwords, backup_database, restore_database
from encryption import generate_key, load_key, encrypt_message, decrypt_message
from password_generator import generate_password
from password_strength import check_password_strength
from datetime import datetime, timedelta

def add_new_password(service, username, password, fernet_key):
    is_strong, strength = check_password_strength(password)
    if not is_strong:
        print("Password is not strong enough. Strength criteria not met:", strength)
        return
    encrypted_password = encrypt_message(password, fernet_key)
    add_password(service, username, encrypted_password)
    print("Password added successfully.")

def retrieve_password(service, fernet_key):
    result = get_password(service)
    if result:
        username_hash, encrypted_password, creation_date = result
        decrypted_password = decrypt_message(encrypted_password, fernet_key)
        print(f"Username hash: {username_hash}")
        print(f"Password: {decrypted_password}")
        print(f"Creation Date: {creation_date}")
    else:
        print("Service not found.")

def check_password_expiry(expiry_days=90):
    all_passwords = get_all_passwords()
    current_date = datetime.now()
    for service_hash, username_hash, creation_date in all_passwords:
        creation_date = datetime.strptime(creation_date, '%Y-%m-%d %H:%M:%S')
        if (current_date - creation_date) > timedelta(days=expiry_days):
            print(f"Password for service hash {service_hash} (username hash {username_hash}) is older than {expiry_days} days and should be changed.")

def search_passwords_by_query(query):
    results = search_passwords(query)
    if results:
        for service_hash, username_hash in results:
            print(f"Service hash: {service_hash}, Username hash: {username_hash}")
    else:
        print("No matching services found.")

def main():
    parser = argparse.ArgumentParser(description='Password Manager')
    parser.add_argument('action', choices=['add', 'get', 'generate', 'check_expiry', 'search', 'backup', 'restore'], help='Action to perform')
    parser.add_argument('--service', help='Service name (required for adding or retrieving a password)')
    parser.add_argument('--username', help='Username (required for adding a new password)')
    parser.add_argument('--length', type=int, default=16, help='Length of the generated password (default: 16)')
    parser.add_argument('--expiry_days', type=int, default=90, help='Number of days to check for password expiry (default: 90)')
    parser.add_argument('--query', help='Query to search for services')
    parser.add_argument('--backup_path', help='Path to backup the database and keys')
    parser.add_argument('--restore_path', help='Path to restore the database and keys from')
    args = parser.parse_args()

    create_db()

    master_password = getpass.getpass("Enter the master password: ")

    if not os.path.exists("secret.key"):
        fernet_key = generate_key(master_password)
    else:
        fernet_key = load_key(master_password)

    if args.action == 'add':
        if not args.service or not args.username:
            print("Service name and username are required for adding a new password.")
            return
        password = getpass.getpass("Enter the password: ")
        add_new_password(args.service, args.username, password, fernet_key)
    
    elif args.action == 'get':
        if not args.service:
            print("Service name is required for retrieving a password.")
            return
        retrieve_password(args.service, fernet_key)
    
    elif args.action == 'generate':
        password = generate_password(args.length)
        print(f"Generated password: {password}")
    
    elif args.action == 'check_expiry':
        check_password_expiry(args.expiry_days)
    
    elif args.action == 'search':
        if not args.query:
            print("Query is required for searching.")
            return
        search_passwords_by_query(args.query)
    
    elif args.action == 'backup':
        if not args.backup_path:
            print("Backup path is required for backing up the database and keys.")
            return
        backup_database(args.backup_path)
    
    elif args.action == 'restore':
        if not args.restore_path:
            print("Restore path is required for restoring the database and keys.")
            return
        restore_database(args.restore_path)

if __name__ == "__main__":
    main()



 # master password = abcdef@123
 
 
 