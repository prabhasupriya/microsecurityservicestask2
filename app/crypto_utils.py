import base64
import re
import pyotp
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256

def decrypt_seed(encrypted_seed_b64: str, private_key) -> str:
    """Step 5: Decrypt base64-encoded encrypted seed using RSA/OAEP."""
    try:
        ciphertext = base64.b64decode(encrypted_seed_b64)
        cipher = PKCS1_OAEP.new(key=private_key, hashAlgo=SHA256)
        decrypted_bytes = cipher.decrypt(ciphertext)
        seed_hex = decrypted_bytes.decode('utf-8').strip()

        if len(seed_hex) == 64 and re.fullmatch(r'[0-9a-f]{64}', seed_hex):
            return seed_hex
        else:
            raise ValueError(f"Invalid seed format: {len(seed_hex)} chars")
    except Exception as e:
        raise e

def generate_totp_code(hex_seed: str) -> str:
    """
    Step 6: Generate current TOTP code from hex seed.
    Configuration: Algorithm=SHA-1, Period=30s, Digits=6.
    """
    # 1. Convert hex seed to bytes
    seed_bytes = bytes.fromhex(hex_seed)
    
    # 2. Convert bytes to base32 encoding
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    
    # 3. Create TOTP object (pyotp uses SHA-1, 30s, 6 digits by default)
    totp = pyotp.TOTP(base32_seed)
    
    # 4. Generate and return current code
    return totp.now()

def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    """
    Step 6: Verify TOTP code with time window tolerance.
    window=1 accounts for ±30 seconds of clock skew.
    """
    # 1. Convert hex seed to base32
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    
    # 2. Create TOTP object
    totp = pyotp.TOTP(base32_seed)
    
    # 3. Verify code with valid_window (default 1 = ±30s)
    return totp.verify(code, valid_window=valid_window)