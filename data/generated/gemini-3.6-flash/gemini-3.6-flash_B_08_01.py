from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """Generates a cryptographically secure key for symmetric encryption."""
    return Fernet.generate_key()


def encrypt_message(message: str, key: bytes) -> bytes:
    """Encrypts a string message using AES-128 in CBC mode with HMAC (Fernet)."""
    cipher = Fernet(key)
    return cipher.encrypt(message.encode("utf-8"))


def decrypt_message(encrypted_data: bytes, key: bytes) -> str:
    """Decrypts an encrypted ciphertext back to the original string message."""
    cipher = Fernet(key)
    decrypted_bytes = cipher.decrypt(encrypted_data)
    return decrypted_bytes.decode("utf-8")


if __name__ == "__main__":
    # Example usage
    key = generate_key()
    original_message = "This is a highly secret message!"

    # Encrypt
    ciphertext = encrypt_message(original_message, key)

    # Decrypt
    decrypted_message = decrypt_message(ciphertext, key)

    print(f"Key: {key.decode()}")
    print(f"Encrypted: {ciphertext.decode()}")
    print(f"Decrypted: {decrypted_message}")
