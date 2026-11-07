from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """Generates a secret key for Fernet symmetric encryption."""
    return Fernet.generate_key()


def encrypt_message(message: str, key: bytes) -> bytes:
    """Encrypts a plaintext string message using the provided key."""
    fernet = Fernet(key)
    return fernet.encrypt(message.encode("utf-8"))


def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
    """Decrypts an encrypted message (bytes) using the provided key."""
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_message).decode("utf-8")


# Example Usage:
if __name__ == "__main__":
    original_message = "Hello, World! This is a secret message."

    # 1. Generate key
    key = generate_key()
    print(f"Generated Key: {key.decode()}")

    # 2. Encrypt message
    encrypted = encrypt_message(original_message, key)
    print(f"Encrypted Message: {encrypted}")

    # 3. Decrypt message
    decrypted = decrypt_message(encrypted, key)
    print(f"Decrypted Message: {decrypted}")
