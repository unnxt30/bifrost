import httpx
from urllib.parse import urlparse, parse_qs

class AppleManager:
    def __init__(self, music_url):
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
