from encryption import generate_key, encrypt_message, decrypt_message

def test_encryption():
    # Generate a key
    generate_key()
    print("Encryption key generated and saved.")

    # Test encryption
    message = "mysecretpassword"
    encrypted_message = encrypt_message(message)
    print(f"Encrypted message: {encrypted_message}")

    # Test decryption
    decrypted_message = decrypt_message(encrypted_message)
    print(f"Decrypted message: {decrypted_message}")

if __name__ == "__main__":
    test_encryption()
