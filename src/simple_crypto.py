def encrypt_string(text: str, key: str = "SECRET") -> str:
    """Encrypt a string using XOR cipher with a key."""
    # Extend key to match text length
    key_extended = key * (len(text) // len(key) + 1)
    key_extended = key_extended[: len(text)]

    # XOR each character with corresponding key character
    encrypted = "".join(
        chr(ord(c) ^ ord(k)) for c, k in zip(text, key_extended)
    )
    # Convert to hex for safe storage/transmission
    return encrypted.encode().hex()


def decrypt_string(encrypted_hex: str, key: str = "SECRET") -> str:
    """Decrypt a hex string using XOR cipher with the same key."""
    # Convert hex back to string
    encrypted = bytes.fromhex(encrypted_hex).decode()

    # Extend key to match text length
    key_extended = key * (len(encrypted) // len(key) + 1)
    key_extended = key_extended[: len(encrypted)]

    # XOR each character with corresponding key character
    return "".join(
        chr(ord(c) ^ ord(k)) for c, k in zip(encrypted, key_extended)
    )
