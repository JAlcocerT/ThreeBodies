# Dockerfile for Logto Sample Flask App + Webhook Receiver
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY logto-sample.py ./
COPY logto-webhook-receiver.py ./
COPY .env.example ./

# Expose port (Flask default)
EXPOSE 5088

# Entrypoint: run both Flask apps (sample & webhook) with one process for demo (use production WSGI for real use)
CMD ["python3", "logto-sample.py"]
# To run the webhook receiver, use: docker run ... python3 logto-webhook-receiver.py
