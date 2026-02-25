from Crypto.PublicKey import RSA

def generate_rsa_keypair(key_size: int = 4096):
    """
    Generate RSA key pair per specifications:
    - 4096 bits
    - Public exponent: 65537
    - Format: PEM
    """
    # 1. Generate the RSA key
    # The RSA.generate function uses 65537 as the default exponent
    key = RSA.generate(key_size)

    # 2. Export Private Key in PEM format
    private_key_pem = key.export_key(format='PEM')
    
    # 3. Export Public Key in PEM format
    public_key_pem = key.publickey().export_key(format='PEM')

    # 4. Save to files
    with open("student_private.pem", "wb") as priv_file:
        priv_file.write(private_key_pem)
        
    with open("student_public.pem", "wb") as pub_file:
        pub_file.write(public_key_pem)

    print("✅ student_private.pem and student_public.pem generated successfully.")
    return key, key.publickey()

if __name__ == "__main__":
    generate_rsa_keypair()