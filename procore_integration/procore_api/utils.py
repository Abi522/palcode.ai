import requests
import logging

#from procore_api.models import Project

#from procore_api.models import Project
# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_projects():
    # Replace this with a function to dynamically get the token
    access_token = "https://api.procore.com/vapid/projects"
    if not access_token:
        logger.error("Missing access token.")
        return

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://api.procore.com/vapid/projects"

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            projects = response.json()
            logger.info(f"Fetched {len(projects)} projects from Procore.")

            for project in projects:
                Project.objects.update_or_create(
                    procore_id=project["id"],
                    defaults={
                        "name": project["name"],
                        "status": project["status"],
                        "created_at": project.get("created_at"),  # Use .get() to avoid KeyError
                        "updated_at": project.get("updated_at"),
                    }
                )
                logger.info(f"Updated project: {project['name']} (ID: {project['id']})")

        else:
            logger.error(f"Procore API Error {response.status_code}: {response.text}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {str(e)}")


import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API credentials from environment variables (or use defaults)
PROCORE_CLIENT_ID = os.getenv("PROCORE_CLIENT_ID", "AZsCLk86ZBbgsNY6QBU3HQrBh24oZx8MF2lGcb_wXg0")
PROCORE_CLIENT_SECRET = os.getenv("PROCORE_CLIENT_SECRET", "o4TCMzK6_3DUyNYYNykxM4yoQxIoVhAYj7ZLPLqp97E")
PROCORE_AUTH_CODE = os.getenv("PROCORE_AUTH_CODE",
                              "yUTpyoMLzyBOxG3omCP1fPm85dhpYN206kfOFMsRRdE")  # From Procore OAuth redirect
PROCORE_REDIRECT_URI = os.getenv("PROCORE_REDIRECT_URI","http://localhost")
# Updated default webhook URL to match your ngrok tunnel (ensure trailing slash is present)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://randomname.ngrok.io/procore-webhook-handler/")


def get_access_token():
    """
    Exchanges the authorization code for an access token.
    """
    token_url = "https://login.procore.com/oauth/token"
    payload = {
        "grant_type": "authorization_code",
        "client_id": PROCORE_CLIENT_ID,
        "client_secret": PROCORE_CLIENT_SECRET,
        "code": PROCORE_AUTH_CODE,
        "redirect_uri": PROCORE_REDIRECT_URI
    }
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(token_url, data=payload, headers=headers)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        print("✅ Access token received successfully.")
        return access_token
    else:
        print(f"❌ Failed to get access token. Status Code: {response.status_code}")
        print("📌 Response:", response.text)
        return None

def register_webhook(access_token):
    """
    Registers a webhook with Procore to receive project events (create, update, delete).
    """
    if not WEBHOOK_URL:
        print("❌ Error: WEBHOOK_URL is missing. Check your .env file.")
        return

    url = "https://api.procore.com/rest/v1.0/webhook_subscriptions"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": "Project Notifications",
        "webhook_url": WEBHOOK_URL,
        "resource": "projects",
        "events": ["create", "update", "delete"]
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("✅ Webhook registered successfully.")
        print("📌 Response:", response.json())
    else:
        print(f"❌ Failed to register webhook. Status Code: {response.status_code}")
        print("📌 Response:", response.text)

if __name__ == "__main__":
    access_token = get_access_token()
    if access_token:
        register_webhook(access_token)
