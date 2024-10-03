# get_weather_data.py

import requests

def get_weather_data(lat, lon, weather_api_key):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={weather_api_key}"
    response = requests.get(url)
    data = response.json()
    print(f"Weather API response: {data}")

    if response.status_code != 200 or 'wind' not in data:
        print(f"Error fetching weather data: {data.get('message', 'Unknown error')}")
        return 0, 0  # Default values

    # Extract wind speed
    wind_speed = data['wind'].get('speed', 0)

    # Snowfall in the last hour (if available)
    snowfall = data.get('snow', {}).get('1h', 0)  # Snowfall in mm
    return snowfall, wind_speed
