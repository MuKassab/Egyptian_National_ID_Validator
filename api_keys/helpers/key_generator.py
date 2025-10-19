import secrets
import hashlib
import string

def generate_api_key() -> str:
    """
    Generate a cryptographically secure API key.
    Always generates a 64-character key.
    
    Returns:
        str: A cryptographically secure random API key (64 characters)
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(64))

def hash_api_key(api_key: str) -> str:
    """
    Hash an API key using SHA-512.
    
    Args:
        api_key (str): The API key to hash
        
    Returns:
        str: SHA-512 hash of the API key
    """
    return hashlib.sha512(api_key.encode()).hexdigest()

def verify_api_key(api_key: str, stored_hash: str) -> bool:
    """
    Verify an API key against its stored hash.
    
    Args:
        api_key (str): The API key to verify
        stored_hash (str): The stored hash to compare against
        
    Returns:
        bool: True if the API key matches the hash
    """
    return hash_api_key(api_key) == stored_hash