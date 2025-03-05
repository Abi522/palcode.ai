from fastapi import FastAPI, HTTPException, Request
import json
import logging
from typing import Dict

# Initialize FastAPI
app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.post("/webhook")  # ✅ Only allows POST requests
async def receive_webhook(request: Request) -> Dict[str, str]:
    try:
        # Parse JSON payload
        payload = await request.json()

        # Log the payload
        logger.info("🔹 Webhook Received: %s", json.dumps(payload, indent=2))

        # Process the event
        event_type = payload.get("event", "unknown")
        logger.info(f"✅ Processing event: {event_type}")

        return {"message": "Webhook received", "status": "success"}
    except Exception as e:
        logger.error(f"❌ Error processing webhook: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

# ✅ Optional: Add a GET route for debugging
@app.get("/webhook")
async def test_webhook():
    return {"message": "Webhook endpoint is active!"}
