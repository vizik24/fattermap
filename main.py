from fastapi import FastAPI, HTTPException
from get_slope_aspect import get_slope_aspect
from get_weather_data import get_weather_data
from calculate_avalanche_risk import calculate_avalanche_risk

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Avalanche Risk API is up and running!"}

@app.get("/calculate_risk")
def calculate_risk(lat: float, lon: float, group_size: int, elevation_api_key: str = "", weather_api_key: str = ""):
    if not weather_api_key:
        raise HTTPException(status_code=400, detail="OpenWeatherMap API key is required.")

    # Get slope angle and aspect
    slope_angle, aspect = get_slope_aspect(lat, lon, elevation_api_key)

    # Get weather data
    snowfall, wind_speed = get_weather_data(lat, lon, weather_api_key)

    # Convert units
    snowfall_cm = snowfall / 10  # Convert mm to cm
    wind_speed_kmh = wind_speed * 3.6  # Convert m/s to km/h

    # Calculate avalanche risk
    risk = calculate_avalanche_risk(slope_angle, aspect, snowfall_cm, wind_speed_kmh, group_size)

    # Interpret the risk score
    if risk < 1.5:
        risk_level = "Low"
    elif risk < 2.5:
        risk_level = "Moderate"
    elif risk < 3.5:
        risk_level = "Considerable"
    else:
        risk_level = "High"

    return {
        "slope_angle": slope_angle,
        "aspect": aspect,
        "snowfall_cm": snowfall_cm,
        "wind_speed_kmh": wind_speed_kmh,
        "avalanche_risk_score": risk,
        "risk_level": risk_level
    }
