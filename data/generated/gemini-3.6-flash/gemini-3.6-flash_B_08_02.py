import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def generate_key() -> bytes:
    """Generates a cryptographically secure 256-bit key."""
    return AESGCM.generate_key(bit_length=256)


def encrypt(key: bytes, plaintext: str) -> bytes:
    """Encrypts a string using AES-256-GCM authenticated encryption."""
    aesgcm = AESGCM(key)
    # Generate a cryptographically secure 96-bit (12-byte) nonce
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode("utf-8"), None)
    # Combine nonce and ciphertext for storage/transmission
    return nonce + ciphertext


def decrypt(key: bytes, encrypted_data: bytes) -> str:
    """Decrypts AES-256-GCM encrypted data and verifies authenticity."""
    aesgcm = AESGCM(key)
    # Extract the 12-byte nonce from the beginning of the payload
    nonce = encrypted_data[:12]
    ciphertext = encrypted_data[12:]
    plaintext_bytes = aesgcm.decrypt(nonce, ciphertext, None)
    return plaintext_bytes.decode("utf-8")


# Example usage:
if __name__ == "__main__":
    key = generate_key()
    original_message = "Secret Message: AES-GCM Encryption"

    encrypted_payload = encrypt(key, original_message)
    decrypted_message = decrypt(key, encrypted_payload)

    assert original_message == decrypted_message
    print("Original:", original_message)
    print("Encrypted (hex):", encrypted_payload.hex())
    print("Decrypted:", decrypted_message)
