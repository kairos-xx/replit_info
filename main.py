from src.simple_crypto import decrypt_string, encrypt_string

# Example usage
text = "Hello, World!"
print(f"Original text: {text}")

# Encrypt
encrypted = encrypt_string(text)
print(f"Encrypted (hex): {encrypted}")

# Decrypt
decrypted = decrypt_string(encrypted)
print(f"Decrypted: {decrypted}")
