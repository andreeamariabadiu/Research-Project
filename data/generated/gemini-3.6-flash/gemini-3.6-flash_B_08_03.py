from cryptography.fernet import Fernet


def generate_key() -> bytes:
    """Generates a cryptographically secure random key for symmetric encryption."""
    return Fernet.generate_key()


def encrypt_message(message: str, key: bytes) -> bytes:
    """Encrypts a plaintext message using AES-128 in CBC mode with HMAC authentication."""
    cipher = Fernet(key)
    return cipher.encrypt(message.encode("utf-8"))


def decrypt_message(ciphertext: bytes, key: bytes) -> str:
    """Decrypts a ciphertext message back to plaintext."""
    cipher = Fernet(key)
    return cipher.decrypt(ciphertext).decode("utf-8")


# Example Usage
if __name__ == "__main__":
    # Generate a secure key
    key = generate_key()

    # Original message
    original_message = "Hello, World! This is a secure message."

    # Encrypt
    encrypted_data = encrypt_message(original_message, key)

    # Decrypt
    decrypted_data = decrypt_message(encrypted_data, key)

    print(f"Key: {key.decode()}")
    print(f"Encrypted: {encrypted_data.decode()}")
    print(f"Decrypted: {decrypted_data}")
