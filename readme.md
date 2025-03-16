# Avalanche Risk API

This is a FastAPI-based web service that calculates the avalanche risk at a given latitude and longitude using the Werner Munter reduction method.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Methodology](#methodology)
- [Assumptions and Limitations](#assumptions-and-limitations)
- [Disclaimer](#disclaimer)

## Introduction

The Avalanche Risk API assesses avalanche risk by considering factors such as slope angle, aspect, recent snowfall, wind speed, and group size. It fetches real-time data using external APIs and applies the Munter method to provide a risk assessment.

## Features

- REST API built using FastAPI
- Calculates slope angle and aspect using elevation data
- Fetches current weather data, including snowfall and wind speed
- Computes avalanche risk using the Munter method
- Returns a qualitative risk level interpretation (Low, Moderate, Considerable, High)
- CORS enabled for flexible frontend integration

## Requirements

- Python 3.x
- FastAPI
- Uvicorn
- External APIs for weather and elevation data

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/avalanche-risk-api.git
   cd avalanche-risk-api
   ```

2. **Create a Virtual Environment and Install Dependencies**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the API**

   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Usage

### Example Request

```bash
curl "http://localhost:8000/calculate_risk?lat=46.8523&lon=-121.7603&group_size=4&weather_api_key=YOUR_API_KEY"
```

### Example Response

```json
{
  "slope_angle": 35.2,
  "aspect": "North-East",
  "snowfall_cm": 12.5,
  "wind_speed_kmh": 45.0,
  "avalanche_risk_score": 3.2,
  "risk_level": "Considerable"
}
```

## API Endpoints

### `GET /`
**Description:** Health check endpoint to confirm the API is running.

**Response:**
```json
{"message": "Avalanche Risk API is up and running!"}
```

### `GET /calculate_risk`
**Description:** Computes the avalanche risk based on location, group size, and weather conditions.

**Parameters:**
- `lat` (float, required): Latitude of the location.
- `lon` (float, required): Longitude of the location.
- `group_size` (int, required): Number of people in the group.
- `elevation_api_key` (string, optional): API key for elevation data.
- `weather_api_key` (string, required): API key for weather data.

**Response:**
Returns a JSON object with calculated risk details.

## Methodology

**Werner Munter Reduction Method**

The Werner Munter method simplifies avalanche forecasting into quantifiable factors, allowing users to assess risk effectively.

### Key Components:
- **Slope Angle:** Slopes between 30° and 45° are most prone to avalanches.
- **Aspect:** Sun exposure and wind affect snow stability.
- **Weather Conditions:** Recent snowfall and strong winds increase risk.
- **Group Size:** Smaller groups and maintaining spacing reduce risk.

### Formula:
```
Avalanche Risk = (Slope Factor × Aspect Factor × Weather Factors) / Reduction Factor
```

## Assumptions and Limitations

- **Assumes uniform terrain** within a small area.
- **Uses real-time weather data** but does not predict future conditions.
- **Simplifies the Munter method** by excluding some factors.
- **Elevation data accuracy** depends on external APIs and may be imprecise.

## Disclaimer

This tool is intended for educational purposes and should not replace professional avalanche forecasting. Always consult local avalanche reports and exercise caution in avalanche-prone areas.

**Contributions and feedback are welcome!**

