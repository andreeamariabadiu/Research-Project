from cryptography.fernet import Fernet


class CryptoManager:

    @staticmethod
    def generate_key() -> bytes:
        """Generates a new Fernet secret key."""
        return Fernet.generate_key()

    @staticmethod
    def encrypt_message(message: str, key: bytes) -> bytes:
        """Encrypts a plaintext string message using the provided key."""
        fernet = Fernet(key)
        return fernet.encrypt(message.encode("utf-8"))

    @staticmethod
    def decrypt_message(encrypted_message: bytes, key: bytes) -> str:
        """Decrypts an encrypted byte message back to plaintext string using the key."""
        fernet = Fernet(key)
        return fernet.decrypt(encrypted_message).decode("utf-8")


# Example Usage
if __name__ == "__main__":
    # 1. Generate a key
    key = CryptoManager.generate_key()
    print(f"Generated Key: {key.decode()}\n")

    # 2. Original Message
    original_message = "Hello! This is a secret message."
    print(f"Original Message:  {original_message}")

    # 3. Encrypt the message
    encrypted_msg = CryptoManager.encrypt_message(original_message, key)
    print(f"Encrypted Message: {encrypted_msg.decode()}")

    # 4. Decrypt the message
    decrypted_msg = CryptoManager.decrypt_message(encrypted_msg, key)
    print(f"Decrypted Message: {decrypted_msg}")
