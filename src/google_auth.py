import os
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

SCOPES = ['https://www.googleapis.com/auth/calendar']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(BASE_DIR, 'assistant/credentials.json')
TOKEN_PATH = os.path.join(BASE_DIR, 'assistant/token.pkl')


def authenticate_google_calendar():
    credentials = None
    # Check if token file exists and load it
    if os.path.exists(TOKEN_PATH):
        try:
            with open(TOKEN_PATH, "rb") as token:
                credentials = pickle.load(token)
            logging.info("Token loaded successfully from pickle.")
        except Exception as e:
            logging.error("Failed to load token from pickle: %s", e)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            try:
                credentials.refresh(Request())
                logging.info("Token refreshed successfully.")
            except Exception as e:
                logging.error("Token refresh failed: %s", e)
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)
            logging.info("New authentication flow completed.")

        try:
            with open(TOKEN_PATH, "wb") as token:
                pickle.dump(credentials, token)
                logging.info("Token saved to pickle.")
        except Exception as e:
            logging.error("Failed to save token to pickle: %s", e)

    return credentials

def get_calendar_service():
    credentials = authenticate_google_calendar()
    service = build("calendar", "v3", credentials=credentials)
    return service


