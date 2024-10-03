# main.py

from get_user_input import get_user_input
from get_slope_aspect import get_slope_aspect
from get_weather_data import get_weather_data
from calculate_avalanche_risk import calculate_avalanche_risk

def main():
    # Prompt user for API keys
    print("Please enter your API keys. Leave blank if not required for the service.")
    elevation_api_key = input("Enter your Elevation API key (if required): ").strip()
    weather_api_key = input("Enter your OpenWeatherMap API key: ").strip()
    
    if not weather_api_key:
        print("Error: OpenWeatherMap API key is required.")
        return

    # Get user input for location and group size
    lat, lon, group_size = get_user_input()
    
    # Get slope angle and aspect
    slope_angle, aspect = get_slope_aspect(lat, lon, elevation_api_key)
    print(f"Slope angle: {slope_angle:.2f} degrees")
    print(f"Aspect direction: {aspect}")

    # Get weather data
    snowfall, wind_speed = get_weather_data(lat, lon, weather_api_key)
    print(f"Snowfall in last hour: {snowfall} mm")
    print(f"Wind speed: {wind_speed} m/s")

    # Convert units if necessary
    snowfall_cm = snowfall / 10  # Convert mm to cm
    wind_speed_kmh = wind_speed * 3.6  # Convert m/s to km/h

    # Calculate avalanche risk
    risk = calculate_avalanche_risk(slope_angle, aspect, snowfall_cm, wind_speed_kmh, group_size)
    print(f"\nAvalanche Risk Score: {risk:.2f}")

    # Interpret the risk score
    if risk < 1.5:
        risk_level = "Low"
    elif risk < 2.5:
        risk_level = "Moderate"
    elif risk < 3.5:
        risk_level = "Considerable"
    else:
        risk_level = "High"

    print(f"Risk Level: {risk_level}")

if __name__ == "__main__":
    main()
