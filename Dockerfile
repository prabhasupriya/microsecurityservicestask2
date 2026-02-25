# Stage 1: Builder
FROM python:3.10-slim AS builder
WORKDIR /build
# Copy dependency file
COPY requirements.txt .
# Install dependencies into a local folder to copy later
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim AS runtime

# Set TZ=UTC environment variable (critical!)
ENV TZ=UTC
ENV PATH=/root/.local/bin:$PATH

WORKDIR /app

# Install system dependencies (cron, tzdata)
RUN apt-get update && apt-get install -y \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Configure timezone to UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Copy dependencies from builder
COPY --from=builder /root/.local /root/.local

# Copy application code & scripts
COPY . .

# Setup cron job
# 1. Copy cron file
COPY cron/2fa-cron /etc/cron.d/2fa-cron
# 2. Set permissions on cron file (0644)
RUN chmod 0644 /etc/cron.d/2fa-cron
# 3. Install cron file with crontab
RUN crontab /etc/cron.d/2fa-cron

# Create volume mount points (/data and /cron) with 755 permissions
RUN mkdir -p /data /cron && chmod -R 755 /data /cron
RUN mkdir -p /cron && chmod 0777 /cron
RUN touch /var/log/cron.log && chmod 0666 /var/log/cron.log
# EXPOSE 8080
EXPOSE 8080

# Start cron and application
# - Start cron daemon
# - Start HTTP server on 0.0.0.0:8080
CMD ["sh", "-c", "service cron start && uvicorn app.main:app --host 0.0.0.0 --port 8080"]