import subprocess
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def sign_message(message: str, private_key) -> bytes:
    # 1. Encode commit hash as ASCII bytes
    message_bytes = message.encode('utf-8')
    
    # 2. Sign using RSA-PSS with SHA-256
    signature = private_key.sign(
        message_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def encrypt_with_public_key(data: bytes, public_key) -> bytes:
    # 1. Encrypt signature bytes using RSA/OAEP with SHA-256
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def main():
    try:
        # 1. Get current commit hash
        commit_hash = subprocess.check_output(['git', 'log', '-1', '--format=%H']).decode('ascii').strip()
        
        # 2. Load student private key
        with open("student_private.pem", "rb") as key_file:
            student_private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None
            )

        # 3. Sign commit hash
        signature = sign_message(commit_hash, student_private_key)

        # 4. Load instructor public key
        # Make sure the filename matches exactly (no extra spaces!)
        with open("instructor_public.pem", "rb") as key_file:
            instructor_public_key = serialization.load_pem_public_key(
                key_file.read()
            )

        # 5. Encrypt signature
        encrypted_signature = encrypt_with_public_key(signature, instructor_public_key)

        # 6. Base64 encode
        final_proof = base64.b64encode(encrypted_signature).decode('utf-8')

        print("\n" + "="*50)
        print(f"COMMIT HASH: {commit_hash}")
        print("-" * 50)
        print(f"ENCRYPTED SIGNATURE (PROOF):\n{final_proof}")
        print("="*50 + "\n")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()