import httpx
import json
import time
import urllib.parse
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()

class SpotifyManager:
    def __init__(self):
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
        self.auth_token = None
        self.expiry = 0  
        
        # Try to load cached token first
        cached_token, cached_expiry = self._load_cached_token()
        if cached_token and time.time() < cached_expiry:
            self.auth_token = cached_token
            self.expiry = cached_expiry
        else:
            self._refresh_token()

    def _get_cache_file_path(self):
        """Get the path to the token cache file"""
        cache_dir = Path.home() / '.bifrost'
        cache_dir.mkdir(exist_ok=True)
        return cache_dir / 'spotify_token.json'

    def _load_cached_token(self):
        """Load token from cache file if it exists and is valid"""
        cache_file = self._get_cache_file_path()
        try:
            if cache_file.exists():
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                    token = data.get('access_token')
                    expiry = data.get('expiry', 0)
                    if token and time.time() < expiry:
                        return token, expiry
        except (json.JSONDecodeError, KeyError, OSError) as e:
            print(f"Cache file corrupted, ignoring: {e}")
        return None, 0

    def _save_token_to_cache(self, token, expiry):
        """Save token to cache file"""
        cache_file = self._get_cache_file_path()
        try:
            cache_data = {
                'access_token': token,
                'expiry': expiry,
                'cached_at': time.time()
            }
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f, indent=2)
        except OSError as e:
            print(f"Could not save token to cache: {e}")

    def _clear_cached_token(self):
        """Remove cached token file"""
        cache_file = self._get_cache_file_path()
        try:
            if cache_file.exists():
                cache_file.unlink()
        except OSError as e:
            print(f"Could not clear cache: {e}")

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
            
            # Save token to cache
            self._save_token_to_cache(self.auth_token, self.expiry)
            
            return True
        except (httpx.HTTPStatusError, httpx.RequestError, json.JSONDecodeError, ValueError) as e:
            print(f"Error refreshing token: {e}")
            self.auth_token = None
            self.expiry = 0
            # Clear any stale cache
            self._clear_cached_token()
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
    
    def get_spotify_track(self, url):
        if not self.is_token_valid():
            if not self._refresh_token():
                return None
            
        track_id = self.extract_track_id(url)
        if not track_id:
            print("Failed to extract track ID from URL")
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
