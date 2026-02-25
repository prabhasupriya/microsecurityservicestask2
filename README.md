# Microservices Security Task 2: 2FA & RSA Implementation

This project implements a secure, containerized 2FA (TOTP) generation service. It utilizes RSA-PSS for digital signatures and RSA-OAEP for asymmetric encryption, ensuring the integrity and confidentiality of the 2FA seed and commit proof.

##  System Architecture
- **Language:** Python 3.10-slim
- **Encryption:** RSA (4096-bit) with OAEP padding
- **Signature:** RSA-PSS with SHA-256
- **Automation:** Linux Cron Service
- **Containerization:** Docker & Docker Compose

##  Components
1. **API Service:** A FastAPI/Flask application that handles seed decryption and manual TOTP verification.
2. **Cron Job:** A background process that generates a new TOTP code every 60 seconds.
3. **Persistence:** Docker volumes used to store the decrypted seed securely across container restarts.

##  How to Run

### 1. Start the Container
```bash
docker-compose up -d --build
```
2. Decrypt the Seed
Send the encrypted seed to the /decrypt-seed endpoint using Postman or cURL.

3. Verify Cron Output
Wait 60 seconds, then check the automated log file:

``` Bash
docker exec microsecurityservicestask2-app-1 cat /cron/last_code.txt
```
##  Security Features
Timezone Synchronization: System set to UTC to ensure TOTP consistency.

Key Management: RSA keys are used for secure communication between the student and instructor.

Process Isolation: The cron job and API run within a restricted Docker environment.

## Submission Details
Commit Hash: [69cd9183a98a4a63414c6027395b75ac26e67618]


Repository: https://github.com/prabhasupriya/microsecurityservicestask2.git
