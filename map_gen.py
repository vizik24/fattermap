# map_gen.py

from get_user_input import get_user_input
from get_slope_aspect import get_slope_aspect
from get_weather_data import get_weather_data
from calculate_avalanche_risk import calculate_avalanche_risk
import requests
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors  # Import colors module
import math
import cartopy.crs as ccrs  # Import Cartopy for map projection
import cartopy.feature as cfeature  # Import Cartopy features for basemap

# Function to get elevation data in bulk
def get_elevation_bulk(locations, api_key):
    # Prepare the locations string for the API call
    locations_str = '|'.join(f"{lat},{lon}" for lat, lon in locations)
    url = f"https://api.open-elevation.com/api/v1/lookup?locations={locations_str}"
    response = requests.get(url)
    data = response.json()
    
    # Check for errors
    if 'results' not in data or not data['results']:
        print(f"Error fetching elevation data for bulk locations")
        return None  # Return None if data is missing

    elevations = [result['elevation'] for result in data['results']]
    return elevations

# Function to get slope angle and aspect using bulk elevation data
def get_slope_aspect_bulk(latitudes, longitudes, elevations, grid_size):
    slope_angles = np.zeros((grid_size, grid_size))
    aspects = np.full((grid_size, grid_size), '', dtype=object)

    # Convert degrees latitude to meters (approximate conversion)
    meters_per_degree = 111000  # Approximate value

    for i in range(1, grid_size - 1):
        for j in range(1, grid_size - 1):
            # Get elevations for current point and its neighbors
            z_center = elevations[i][j]
            z_north = elevations[i - 1][j]
            z_south = elevations[i + 1][j]
            z_east = elevations[i][j + 1]
            z_west = elevations[i][j - 1]

            # Calculate slopes in x and y directions
            delta_lat = (latitudes[i - 1] - latitudes[i + 1]) * meters_per_degree
            delta_lon = (longitudes[j + 1] - longitudes[j - 1]) * meters_per_degree * math.cos(math.radians(latitudes[i]))

            dz_dx = (z_east - z_west) / delta_lon
            dz_dy = (z_north - z_south) / delta_lat

            # Calculate slope angle in degrees
            slope_angle_rad = math.atan(math.sqrt(dz_dx**2 + dz_dy**2))
            slope_angle = math.degrees(slope_angle_rad)

            # Calculate aspect angle in degrees
            aspect_rad = math.atan2(dz_dy, -dz_dx)
            aspect = (math.degrees(aspect_rad) + 360) % 360  # Normalize aspect to 0-360 degrees

            # Determine aspect direction
            if (aspect >= 0 and aspect < 45) or (aspect >= 315 and aspect <= 360):
                aspect_direction = 'north'
            elif aspect >= 45 and aspect < 135:
                aspect_direction = 'east'
            elif aspect >= 135 and aspect < 225:
                aspect_direction = 'south'
            else:
                aspect_direction = 'west'

            # Store the results
            slope_angles[i][j] = slope_angle
            aspects[i][j] = aspect_direction

    return slope_angles, aspects

# Main function
def main():
    # Prompt user for API keys
    print("Please enter your API keys. Leave blank if not required for the service.")
    elevation_api_key = input("Enter your Elevation API key (if required): ").strip()
    weather_api_key = input("Enter your OpenWeatherMap API key: ").strip()

    if not weather_api_key:
        print("Error: OpenWeatherMap API key is required.")
        return

    # Get user input for location and group size
    lat_center, lon_center, group_size = get_user_input()

    # Get weather data at the center point
    snowfall, wind_speed = get_weather_data(lat_center, lon_center, weather_api_key)
    if snowfall is None or wind_speed is None:
        print("Weather data is unavailable.")
        return

    # Convert units if necessary
    snowfall_cm = snowfall / 10  # Convert mm to cm
    wind_speed_kmh = wind_speed * 3.6  # Convert m/s to km/h

    # Create a grid of points within a 3 km x 3 km area, points every 300 meters
    grid_spacing = 0.0027  # Approx 300 meters in degrees (0.001 degrees ≈ 111 meters)
    grid_size = int(3 / 0.3) + 1  # 3 km area with points every 0.3 km (300 m)
    grid_size = max(grid_size, 3)  # Ensure grid_size is at least 3

    latitudes = np.linspace(lat_center - 0.0135, lat_center + 0.0135, grid_size)
    longitudes = np.linspace(lon_center - 0.0135, lon_center + 0.0135, grid_size)

    # Generate all grid points
    grid_points = [(lat, lon) for lat in latitudes for lon in longitudes]

    # Fetch elevation data for all grid points in bulk
    elevations_flat = get_elevation_bulk(grid_points, elevation_api_key)
    if elevations_flat is None:
        print("Elevation data is unavailable.")
        return

    # Reshape elevations to match the grid
    elevations = np.array(elevations_flat).reshape((grid_size, grid_size))

    # Calculate slope angles and aspects for the grid
    slope_angles, aspects = get_slope_aspect_bulk(latitudes, longitudes, elevations, grid_size)

    # Initialize risk level matrix
    risk_levels = np.full((grid_size, grid_size), '', dtype=object)
    risk_scores = np.zeros((grid_size, grid_size))

    # Iterate over the grid and calculate risk scores
    for i in range(1, grid_size - 1):
        for j in range(1, grid_size - 1):
            slope_angle = slope_angles[i][j]
            aspect = aspects[i][j]

            if aspect == '':
                continue  # Skip if data is missing

            # Calculate avalanche risk
            risk = calculate_avalanche_risk(slope_angle, aspect, snowfall_cm, wind_speed_kmh, group_size)
            risk_scores[i][j] = risk

            # Determine risk level
            if risk < 1.5:
                risk_level = "Low"
            elif risk < 2.5:
                risk_level = "Moderate"
            elif risk < 3.5:
                risk_level = "Considerable"
            else:
                risk_level = "High"

            risk_levels[i][j] = risk_level

    # Plot the risk map using Matplotlib and Cartopy for the basemap
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Define risk level to numerical value for color mapping
    risk_numeric = np.zeros_like(risk_scores)
    for i in range(grid_size):
        for j in range(grid_size):
            if risk_levels[i][j] == "Low":
                risk_numeric[i][j] = 1
            elif risk_levels[i][j] == "Moderate":
                risk_numeric[i][j] = 2
            elif risk_levels[i][j] == "Considerable":
                risk_numeric[i][j] = 3
            elif risk_levels[i][j] == "High":
                risk_numeric[i][j] = 4
            else:
                risk_numeric[i][j] = np.nan  # Missing data

    # Create a colormap
    cmap = plt.cm.get_cmap('RdYlGn_r', 4)
    bounds = [0.5, 1.5, 2.5, 3.5, 4.5]
    norm = mcolors.BoundaryNorm(bounds, cmap.N)  # Use mcolors instead of plt.colors

    # Plot the risk levels on top of the basemap
    extent = [longitudes[0], longitudes[-1], latitudes[0], latitudes[-1]]
    im = ax.imshow(risk_numeric, extent=extent, origin='lower', cmap=cmap, norm=norm, transform=ccrs.PlateCarree())

    # Add Cartopy features like coastlines and borders
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Add a colorbar with risk levels
    cbar = plt.colorbar(im, ax=ax, ticks=[1, 2, 3, 4], orientation='horizontal', pad=0.05)
    cbar.ax.set_xticklabels(['Low', 'Moderate', 'Considerable', 'High'])
    cbar.set_label('Avalanche Risk Level')

    # Add labels and title
    ax.set_title('Avalanche Risk Map', fontsize=15)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    # Optionally, add the center point
    ax.plot(lon_center, lat_center, 'k+', markersize=12, label='Center Point', transform=ccrs.PlateCarree())

    plt.legend(loc='upper right')

    # Save the figure
    plt.savefig('avalanche_risk_map_with_basemap.png', dpi=300)
    print("Avalanche risk map has been saved to 'avalanche_risk_map_with_basemap.png'")

    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()
