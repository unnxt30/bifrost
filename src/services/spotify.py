import httpx
import json
import time
import urllib.parse
from dotenv import load_dotenv
import os

load_dotenv()

class SpotifyManager:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.auth_token = None
        self.expiry = 0  
        self._refresh_token()  

    def _refresh_token(self):
        url = "https://accounts.spotify.com/api/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        try:
            r = httpx.post(url, headers=headers, data=data)
            r.raise_for_status()
            res = r.json()
            if "access_token" not in res:
                raise ValueError("No access_token in response")
            self.auth_token = res["access_token"]
            current_time = time.time()
            expires_in = res.get("expires_in", 3600)  # Default to 1 hour if missing
            self.expiry = current_time + expires_in - 60  # Buffer for safety
            # Avoid printing in production; use logging instead
            # print("Successfully obtained access token")
            return True
        except (httpx.HTTPStatusError, httpx.RequestError, json.JSONDecodeError, ValueError) as e:
            print(f"Error refreshing token: {e}")
            self.auth_token = None
            self.expiry = 0
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def is_token_valid(self):
        return self.auth_token is not None and time.time() < self.expiry
    
    def _get_location(self):
        try:
            with httpx.Client() as client:
                location_response = client.get("https://ipapi.co/json/")
                location_data = location_response.json()
                market = location_data.get("country_code", "IN")
                if location_response.status_code != 200:
                    print(f"Could not determine location, using default: {market}")
                    return None 
                return market
        except Exception as e:
            print(f"Error getting location: {e}")
            return None

    def get_track_info(self, search_type, track_name, artist_name):
        if not self.is_token_valid():
            if not self._refresh_token():
                return None  # Or raise an exception

        try:
            with httpx.Client() as client:
                market = self._get_location()
                if not market:
                    print("Could not determine location, using default market")
                    market = "IN"

                base_url = "https://api.spotify.com/v1/search"
                q_raw = f"track:{track_name} artist:{artist_name}" 
                params = {
                    'q': q_raw,
                    'type': search_type,  
                    'market': market,
                    'limit':1
                }
                headers = {
                    'Authorization': f'Bearer {self.auth_token}'
                }

                response = client.get(base_url, params=params, headers=headers)
                response.raise_for_status()
                return response.json() 

        except Exception as e:
            print(f"Error getting track info: {e}")
            return None
    
    def get_spotify_track(self, track_id):
        if not self.is_token_valid():
            if not self._refresh_token():
                return None
        try:
            with httpx.Client() as client:
                market = self._get_location()
                if not market:
                    print("Could not determine location, using default market")
                    market = "IN"
                params = {
                    'market': market
                }
                headers = {
                    'Authorization': f'Bearer {self.auth_token}'
                }
                response = client.get(f"https://api.spotify.com/v1/tracks/{track_id}", headers=headers, params=params)
                response.raise_for_status()
                return response.json()
        except Exception as e:
            print(f"Error getting Spotify track: {e}")
            return None

    def extract_track_id(self, url) :
        try:
            parsed = urllib.parse.urlparse(url)

            if parsed.netloc != 'open.spotify.com':
                print("not a spotify URL")
                return None
            
            path_parts = parsed.path.strip('/').split('/')

            if len(path_parts) != 2 or path_parts[0] != 'track':
                print("not a valid spotify track URL")
                return None
            
            track_id = path_parts[1]


            return track_id
        except Exception as e:
            print(f"Error extracting track ID: {e}")
            return None
