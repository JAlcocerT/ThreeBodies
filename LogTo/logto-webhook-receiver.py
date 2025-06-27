import os
import hmac
import hashlib
import json
from flask import Flask, request, abort

app = Flask(__name__)

# Set your webhook secret here or via environment variable
WEBHOOK_SECRET = os.environ.get("LOGTO_WEBHOOK_SECRET", "your-very-secret-value")

@app.route("/logto-webhook", methods=["POST"])
def webhook():
    signature = request.headers.get("X-Logto-Signature")
    payload = request.data
    if not signature or not verify_signature(payload, signature):
        abort(401)
    event = request.json
    print("Received Logto webhook event:")
    print(json.dumps(event, indent=2))
    # Optionally, write to a file for persistence
    with open("webhook_events.log", "a") as f:
        f.write(json.dumps(event) + "\n")
    return "OK", 200

def verify_signature(payload, signature):
    mac = hmac.new(WEBHOOK_SECRET.encode(), payload, hashlib.sha256)
    expected = mac.hexdigest()
    return hmac.compare_digest(expected, signature)

if __name__ == "__main__":
    # For local testing, run: python3 logto-webhook-receiver.py
    app.run(host="0.0.0.0", port=5088)
