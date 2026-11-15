from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """Generate a random Fernet encryption key."""
    return Fernet.generate_key()


def encrypt_message(message: str, key: bytes) -> bytes:
    """Encrypt a string message using the provided key."""
    fernet = Fernet(key)
    return fernet.encrypt(message.encode())


def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    """Decrypt an encrypted message using the provided key."""
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode()


# Example usage
if __name__ == "__main__":
    key = generate_key()
    original_message = "Hello, Secure World!"

    encrypted = encrypt_message(original_message, key)
    decrypted = decrypt_message(encrypted, key)

    print(f"Original:  {original_message}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")
