import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, 'assistant/spotify_tokens.json')

def get_tokens():
    with open(TOKEN_PATH, 'r') as file:
        tokens = json.load(file)
    return tokens

def save_tokens(tokens):
    with open(TOKEN_PATH, 'w') as file:
        json.dump(tokens, file)

def refresh_access_token(refresh_token):
    url = "https://accounts.spotify.com/api/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    response = requests.post(url, data=data)
    response_json = response.json()
    if response.status_code == 200:
        access_token = response_json['access_token']
        # Update the tokens.json with the new access token
        tokens = get_tokens()
        tokens['access_token'] = access_token
        save_tokens(tokens)
        return access_token
    else:
        raise Exception("Failed to refresh token: " + response_json.get('error_description', 'Unknown error'))

def get_access_token():
    tokens = get_tokens()
    access_token = tokens['access_token']
    refresh_token = tokens['refresh_token']
    
    # Optionally, check if the token is expired and refresh it. 
    # Here, we assume the token needs refreshing.
    access_token = refresh_access_token(refresh_token)
    
    return access_token

if __name__ == "__main__":
    print(get_access_token())

