# calculate_avalanche_risk.py

def calculate_avalanche_risk(slope_angle, aspect, snowfall, wind_speed, group_size):
    # Slope factor: risk increases for steep slopes
    slope_factor = 1.5 if slope_angle > 30 else 1

    # Aspect factor: riskier on north/east slopes in Northern Hemisphere
    if aspect in ["north", "east"]:
        aspect_factor = 1.3
    else:
        aspect_factor = 1

    # Weather factors
    weather_factor = 1.5 if snowfall > 20 else 1  # Snowfall in cm
    wind_factor = 1.4 if wind_speed > 30 else 1   # Wind speed in km/h

    # Reduction factor: safer with small groups
    reduction_factor = 0.9 if group_size <= 4 else 1.2

    # Calculate risk
    risk = (slope_factor * aspect_factor * weather_factor * wind_factor) / reduction_factor
    return risk
