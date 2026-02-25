import requests
import json

# --- UPDATED CONFIGURATION ---
STUDENT_ID = "23A91A6106"
# Exact URL provided by you
GITHUB_REPO_URL = "https://github.com/prabhasupriya/microsecurityservicestask2.git"
API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def request_seed(student_id: str, github_repo_url: str, api_url: str):
    """
    Request encrypted seed from instructor API per specifications.
    """
    try:
        # 1. Read student public key from PEM file
        with open("student_public.pem", "r") as f:
            public_key = f.read().strip()

        # 2. Prepare HTTP POST request payload
        # The 'requests' library handles newlines in JSON automatically
        payload = {
            "student_id": student_id,
            "github_repo_url": github_repo_url,
            "public_key": public_key
        }

        # 3. Send POST request to instructor API with timeout handling
        print(f"Requesting seed for {student_id}...")
        response = requests.post(
            api_url, 
            json=payload, 
            headers={"Content-Type": "application/json"},
            timeout=15 
        )

        # 4. Parse JSON response
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                # Extract 'encrypted_seed' field
                encrypted_seed = data.get("encrypted_seed")
                
                # 5. Save encrypted seed to file as plain text
                with open("encrypted_seed.txt", "w") as seed_file:
                    seed_file.write(encrypted_seed)
                
                print(" SUCCESS: 'encrypted_seed.txt' has been generated.")
            else:
                print(f" API Error: {data}")
        else:
            print(f" HTTP Error {response.status_code}: {response.text}")

    except FileNotFoundError:
        print(" Error: 'student_public.pem' not found. Run setup_keys.py first.")
    except Exception as e:
        print(f" Unexpected Error: {e}")

if __name__ == "__main__":
    request_seed(STUDENT_ID, GITHUB_REPO_URL, API_URL)