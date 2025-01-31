# get_slope_aspect.py

import math
from get_elevation import get_elevation

def get_slope_aspect(lat, lon, elevation_api_key):
    # Get elevation data around the point to calculate slope and aspect
    delta = 0.001  # Approx ~111 meters, adjust as needed

    # Define surrounding points
    points = {
        'center': (lat, lon),
        'north': (lat + delta, lon),
        'south': (lat - delta, lon),
        'east': (lat, lon + delta),
        'west': (lat, lon - delta)
    }

    elevations = {}
    for key, (p_lat, p_lon) in points.items():
        elevation = get_elevation(p_lat, p_lon, elevation_api_key)
        elevations[key] = elevation
        print(f"Elevation at {key}: {elevation} meters")

    # Calculate slopes in x and y directions
    # Convert degrees latitude to meters (approximate conversion)
    meters_per_degree = 111000  # Approximate value

    dz_dx = (elevations['east'] - elevations['west']) / (2 * delta * meters_per_degree)
    dz_dy = (elevations['north'] - elevations['south']) / (2 * delta * meters_per_degree)

    print(f"dz_dx: {dz_dx}")
    print(f"dz_dy: {dz_dy}")

    # Calculate slope angle in degrees
    slope_angle_rad = math.atan(math.sqrt(dz_dx**2 + dz_dy**2))
    slope_angle = math.degrees(slope_angle_rad)
    print(f"Slope angle (degrees): {slope_angle}")

    # Calculate aspect angle in degrees
    aspect_rad = math.atan2(dz_dy, -dz_dx)
    aspect = (math.degrees(aspect_rad) + 360) % 360  # Normalize aspect to 0-360 degrees
    print(f"Aspect angle (degrees): {aspect}")

    # Determine aspect direction
    if (aspect >= 0 and aspect < 45) or (aspect >= 315 and aspect <= 360):
        aspect_direction = 'north'
    elif aspect >= 45 and aspect < 135:
        aspect_direction = 'east'
    elif aspect >= 135 and aspect < 225:
        aspect_direction = 'south'
    else:
        aspect_direction = 'west'

    return slope_angle, aspect_direction
