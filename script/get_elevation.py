# get_elevation.py

import requests

def get_elevation(lat, lon, api_key):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    response = requests.get(url)
    data = response.json()
    print(f"API response for ({lat}, {lon}): {data}")
    elevation = data['results'][0]['elevation']
    return elevation

