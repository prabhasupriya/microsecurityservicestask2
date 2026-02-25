#!/usr/bin/env python3
import os
import base64
import pyotp
from datetime import datetime, timezone

# 1. Read hex seed from persistent storage
SEED_PATH = "/data/seed.txt"

def run_cron():
    try:
        if not os.path.exists(SEED_PATH):
            # Handle file not found errors gracefully
            print(f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')} - Seed file not found")
            return

        with open(SEED_PATH, "r") as f:
            hex_seed = f.read().strip()

        # 2. Generate current TOTP code
        seed_bytes = bytes.fromhex(hex_seed)
        base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
        totp = pyotp.TOTP(base32_seed)
        code = totp.now()

        # 3. Get current UTC timestamp (critical!)
        # Format: YYYY-MM-DD HH:MM:SS
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

        # 4. Output formatted line
        # Format: "{timestamp} - 2FA Code: {code}"
        print(f"{timestamp} - 2FA Code: {code}")

    except Exception as e:
        print(f"Error in cron script: {e}")

if __name__ == "__main__":
    run_cron()