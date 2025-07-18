import httpx
import json

class SpotifyManager:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_token = None
    
    def get_auth_token(self):
        url = "https://accounts.spotify.com/api/token" 
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'grant_type': 'client_credentials','client_id': self.client_id, 'client_secret': self.client_secret}
        try: 
            r = httpx.post(url, headers = header, data = data)
            r.raise_for_status()

            res = r.json()

            if "access_token" not in res:
                print("Error: no access_token in response")
                return False

            self.auth_token = res["access_token"]
            print("Successfully obtained access token")
            return True


        except httpx.HTTPStatusError as e:
            print(f"HTTP error occurred: {e.response.status_code} - {e.response.text}")
            return False
        except httpx.RequestError as e:
            print(f"Request error occurred: {e}")
            return False
        except json.JSONDecodeError:
            print("Error: Invalid JSON response")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False    