import hashlib
import hmac

import os

from flask import Flask, abort, request

app = Flask(__name__)

# The same secret you typed in GitHub > Settings > Webhooks > Secret
SECRET = os.environ["WEBHOOK_SECRET"].encode()

def signature_is_valid(body: bytes, header: str | None) -> bool:
    """Check that the message really came from GitHub."""
    if not header or not header.startswith("sha256="):
        return False
    expected = "sha256=" + hmac.new(SECRET, body, hashlib.sha256).hexdigest()
    # compare_digest avoids leaking information through timing
    return hmac.compare_digest(expected, header)


@app.post("/webhook")
def webhook():
    body = request.get_data() # the raw bytes, exactly as GitHub sent them
    if not signature_is_valid(body, request.headers.get("X-Hub-Signature-256")):
        abort(401)
    event = request.headers.get("X-GitHub-Event", "unknown")
    payload = request.get_json(silent=True) or {}
    if event == "ping":
        return {"message": "pong"}
    if event == "push":
        print(f"Push to {payload.get('ref')} by {payload.get('pusher',{}).get('name')}")
        return {"received": event}