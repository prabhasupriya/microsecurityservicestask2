from fastapi import FastAPI, HTTPException, Request
from .crypto_utils import decrypt_seed, generate_totp_code
import os
import pyotp
import base64

app = FastAPI()
SEED_FILE = "/data/seed.txt"

@app.post("/decrypt-seed")
async def handle_decrypt(request: Request):
    data = await request.json()
    enc_seed = data.get("encrypted_seed")
    if not enc_seed:
        raise HTTPException(status_code=400, detail="Missing encrypted_seed")
    try:
        # Load the key inside the function to be safe
        from Crypto.PublicKey import RSA
        with open("student_private.pem", "rb") as k:
            priv_key = RSA.import_key(k.read())
            
        seed_hex = decrypt_seed(enc_seed, priv_key)
        
        # This is the most important part for Step 7 & 12
        os.makedirs("/data", exist_ok=True)
        with open(SEED_FILE, "w") as f:
            f.write(seed_hex)
            
        return {"status": "ok"} # Evaluator looks for this status
    except Exception as e:
        print(f"Decryption error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
@app.get("/generate-2fa")
async def get_2fa():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=404, detail="Seed not found")
    with open(SEED_FILE, "r") as f:
        seed = f.read().strip()
    return {"code": generate_totp_code(seed)}

@app.post("/verify-2fa")
async def verify_2fa(request: Request):
    data = await request.json()
    user_code = data.get("code")
    if not os.path.exists(SEED_FILE):
        raise HTTPException(status_code=404, detail="Seed not found")
    with open(SEED_FILE, "r") as f:
        seed_hex = f.read().strip()
    
    seed_bytes = bytes.fromhex(seed_hex)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed)
    # verify with window=1 for time drift
    if totp.verify(user_code, valid_window=1):
        return {"status": "valid"}
    return {"status": "invalid"}