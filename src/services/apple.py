import httpx
from urllib.parse import urlparse, parse_qs, urlencode

class AppleManager:
    def __init__(self, music_url=""):
        self.url = music_url
        self.track_id = None


    def extract_track_id(self):
        parsed_url = urlparse(self.url)
        query_params = parse_qs(parsed_url.query)
        self.track_id = query_params.get("i", [None])[0]
        return self.track_id is not None
    def get_itunes_url(self):

        if not self.track_id:
            self.extract_track_id()
        try:
            with httpx.Client() as client:
                location_response = client.get("https://ipapi.co/json/")
                location_data = location_response.json()
                if location_response.status_code == 200 and "country_code" in location_data:
                    country_code = location_data["country_code"]
                else:
                    country_code = "IN"
                    print(f"Could not determine location, using default country: {country_code}")
                base_url = "https://itunes.apple.com/lookup"
                params = {
                    "id": self.track_id,
                    "entity": "song",
                    "country": country_code
                }
                itunes_response = client.get(base_url, params=params)
                if itunes_response.status_code == 200:
                    return itunes_response.json()
                else:
                    print(f"iTunes API request failed with status code: {itunes_response.status_code}")
                    return None
        except Exception as e:
            print(f"Error getting iTunes data: {e}")
            return None
        
    def get_apple_music_url(self, trackName, artistName):
        track_name = trackName.strip().lower()
        artist_name = artistName.strip().lower()

        term = f"{artist_name.replace(' ', '+')}+{track_name.replace(' ', '+')}"

        # Manually construct the query string to preserve + characters
        query_string = f"term={term}&media=music&entity=song&limit=1"
        
        base_url = "https://itunes.apple.com/search"
        url = f"{base_url}?{query_string}"
        try:
            with httpx.Client() as client:
                response = client.get(url)
                if response.status_code == 200:
                    res = response.json()
                    if res.get('resultCount', 0) > 0:
                        track_url = res.get('results', [])[0].get('trackViewUrl', None)
                        if track_url:
                            return track_url.strip('"') 
                        return None
                    return None
        except Exception as e:
            print(f"Error getting Apple Music URL: {e}")
            return None
        