import requests

def get_elevation(lat, lon, api_key=""):
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={lat},{lon}"
    response = requests.get(url)

    # ✅ Check if request was successful
    if response.status_code != 200:
        raise Exception(f"Elevation API request failed with status {response.status_code}: {response.text}")

    data = response.json()

    # ✅ Debugging print (optional)
    print(f"API response for ({lat}, {lon}): {data}")

    # ✅ Check if 'results' exists in response
    if "results" not in data or not isinstance(data["results"], list) or len(data["results"]) == 0:
        raise Exception(f"Unexpected Elevation API response: {data}")

    # ✅ Extract elevation safely
    try:
        elevation = data['results'][0]['elevation']
        return elevation
    except (IndexError, KeyError):
        raise Exception("Elevation data missing in API response.")
