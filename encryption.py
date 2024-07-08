from cryptography.fernet import Fernet
import hashlib
import base64

def generate_key(master_password):
    # Generate a 32-byte key from the master password using SHA-256
    key = hashlib.sha256(master_password.encode()).digest()
    # Generate a Fernet key
    fernet_key = Fernet.generate_key()
    # Encrypt the Fernet key with the hashed master password key
    encrypted_fernet_key = Fernet(base64.urlsafe_b64encode(key)).encrypt(fernet_key)
    with open("secret.key", "wb") as key_file:
        key_file.write(encrypted_fernet_key)
    return fernet_key

def load_key(master_password):
    # Generate a 32-byte key from the master password using SHA-256
    key = hashlib.sha256(master_password.encode()).digest()
    # Load and decrypt the Fernet key with the hashed master password key
    with open("secret.key", "rb") as key_file:
        encrypted_fernet_key = key_file.read()
    fernet_key = Fernet(base64.urlsafe_b64encode(key)).decrypt(encrypted_fernet_key)
    return fernet_key

def encrypt_message(message, fernet_key):
    f = Fernet(fernet_key)
    encrypted_message = f.encrypt(message.encode())
    return encrypted_message

def decrypt_message(encrypted_message, fernet_key):
    f = Fernet(fernet_key)
    decrypted_message = f.decrypt(encrypted_message).decode()
    return decrypted_message
