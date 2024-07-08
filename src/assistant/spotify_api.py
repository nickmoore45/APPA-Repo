import os
import requests
import base64
import json
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
TOKEN_URL = "https://accounts.spotify.com/api/token"
# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TOKEN_PATH = os.path.join(BASE_DIR, 'spotify_tokens.json')

class SpotifyAPI:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.load_tokens()
        self.is_playing = False

    def load_tokens(self):
        if os.path.exists(TOKEN_PATH) and os.path.getsize(TOKEN_PATH) > 0:
            with open(TOKEN_PATH, 'r') as f:
                tokens = json.load(f)
                self.access_token = tokens['access_token']
                self.refresh_token = tokens['refresh_token']
        else:
            print("Tokens file is missing or empty. Please authenticate first.")
            self.access_token = None
            self.refresh_token = None

    def save_tokens(self, access_token, refresh_token):
        tokens = {
            'access_token': access_token,
            'refresh_token': refresh_token
        }
        with open(TOKEN_PATH, 'w') as f:
            json.dump(tokens, f)

    def refresh_access_token(self):
        headers = {
            "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode(),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token
        }
        response = requests.post(TOKEN_URL, headers=headers, data=data)
        tokens = response.json()
        if 'access_token' in tokens:
            self.access_token = tokens['access_token']
            self.save_tokens(self.access_token, self.refresh_token)
        else:
            raise Exception("Failed to refresh token: " + tokens.get('error_description', 'Unknown error'))

    def get_headers(self):
        if not self.access_token:
            self.refresh_access_token()
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def get_devices(self):
        url = "https://api.spotify.com/v1/me/player/devices"
        response = requests.get(url, headers=self.get_headers())
        return response.json()

    def search_track(self, query):
        url = "https://api.spotify.com/v1/search"
        params = {
            "q": query,
            "type": "track",
            "limit": 1
        }
        response = requests.get(url, headers=self.get_headers(), params=params)
        return response.json()

    def play_track(self, track_uri, device_id):
        url = f"https://api.spotify.com/v1/me/player/play?device_id={device_id}"
        data = json.dumps({
            "uris": [track_uri]
        })
        response = requests.put(url, headers=self.get_headers(), data=data)
        if response.status_code == 204:
            print("Playback started successfully!")
            self.is_playing = True
            return response.status_code, {}
        else:
            print(f"Error: {response.status_code}")
            print(f"Response Text: {response.text}")
            return response.status_code, response.json() if response.text else {}

    def pause_playback(self, device_id=None):
        url = "https://api.spotify.com/v1/me/player/pause"
        if device_id:
            url += f"?device_id={device_id}"
        response = requests.put(url, headers=self.get_headers())
        if response.status_code == 204:
            print("Playback paused successfully!")
            self.is_playing = False
            return response.status_code, {}
        else:
            print(f"Error: {response.status_code}")
            print(f"Response Text: {response.text}")
            return response.status_code, response.json() if response.text else {}
        
    def get_playback_state(self):
        url = "https://api.spotify.com/v1/me/player"
        response = requests.get(url, headers=self.get_headers())
        if response.status_code == 200:
            state = response.json()
            self.is_playing = state['is_playing']
        else:
            print(f"Error: {response.status_code}")
            print(f"Response Text: {response.text}")

# Usage example:
# if __name__ == "__main__":
#     spotify = SpotifyAPI()
#     if spotify.access_token and spotify.refresh_token:
#         devices = spotify.get_devices()
#         print(devices)
#         search_result = spotify.search_track("Imagine Dragons Believer")
#         print(search_result)
#         if 'tracks' in search_result and 'items' in search_result['tracks']:
#             track_uri = search_result['tracks']['items'][0]['uri']
#             if 'devices' in devices and len(devices['devices']) > 0:
#                 device_id = devices['devices'][0]['id']
#                 status_code, response = spotify.play_track(track_uri, device_id)
#                 print(status_code, response)
#                 status_code, response = spotify.pause_playback(device_id)
#                 print(status_code, response)
#             else:
#                 print("No devices found.")
#         else:
#             print("No tracks found.")
#     else:
#         print("Please authenticate first.")


