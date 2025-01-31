# Avalanche Risk Assessment Tool

This is a Python program that calculates the avalanche risk at a given latitude and longitude using the Werner Munter reduction method.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Notes](#notes)
- [Disclaimer](#disclaimer)

## Introduction

The program assesses avalanche risk by considering factors such as slope angle, aspect, recent snowfall, wind speed, and group size. It uses various APIs to fetch real-time data necessary for the calculations.

## Features

- Calculates slope angle and aspect based on elevation data.
- Retrieves current weather data, including snowfall and wind speed.
- Computes avalanche risk using the Munter method.
- Provides a risk level interpretation (Low, Moderate, Considerable, High).

## Requirements

- Python 3.x
- `requests` library

## Installation

1. **Clone the Repository**

   git clone https://github.com/yourusername/avalanche-risk-assessment.git
   cd avalanche-risk-assessment

2. **Install Dependencies**

Install the requests library if you haven't already:

    pip install requests

## Usage
1. **Obtain API Keys**

Weather API Key: Sign up at OpenWeatherMap to get a free API key.
Elevation API Key: The script uses the Open-Elevation API by default, which doesn't require an API key. If you prefer a different service that requires an API key, obtain it accordingly. This should be left blank in the current version

2. **Run the Program**

Navigate to the directory to which the project was cloned to and run the main script:

    python avalanche_risk_assessment.py

3. **Provide Input**

The program will prompt you to:

- Enter your API keys
- Elevation API key: Leave blank in current version.
- OpenWeatherMap API key: Required.
- Enter location and group details
- Latitude (e.g., 46.8523)
- Longitude (e.g., -121.7603)
- Group size (e.g., 4)

4. **View Results**

The program will display:

- Slope angle and aspect direction
- Snowfall and wind speed
- Avalanche risk score and risk level interpretation

## Methodology

**Werner Munter Reduction Method**

The Werner Munter reduction method is a decision-making framework for assessing avalanche risk in mountainous terrain. Developed by Swiss mountain guide Werner Munter, the method simplifies complex avalanche forecasting into quantifiable factors, allowing users to make informed decisions in the field.

**Key Components:**
- Slope Angle: Slopes between 30° and 45° are most prone to avalanches.
- Aspect: The direction a slope faces affects snow stability due to sun exposure and wind patterns.
- Weather Conditions: Recent snowfall and wind increase avalanche risk.
- Group Size and Behavior: Smaller groups and maintaining spacing reduce risk.

**The Munter Formula:**
The risk is calculated using:
*Avalanche Risk = (Slope Factor × Aspect Factor × Weather Factors) / Reduction Factor*

**Implementation in the Program**
The program translates the Munter method into code by:

1. **Calculating Slope Angle and Aspect:**

Uses elevation data from surrounding points to calculate gradients.
Converts these gradients into slope angle and aspect direction.

2. **Fetching Weather Data:**

Retrieves current snowfall and wind speed using the OpenWeatherMap API.

3. **Applying the Munter Formula:**

    risk = (slope_factor * aspect_factor * weather_factor * wind_factor) / reduction_factor

4. **Interpreting the Risk Score:**

The computed risk score is mapped to qualitative risk levels.

## Assumptions and Limitations

**Assumptions in the Code**
**Uniform Terrain:** Assumes that the area around the point is representative of the slope.
Static Weather Conditions: Uses current weather data without accounting for rapid changes.
**Simplified Factors:** Not all variables from the original Munter method are included.
Limitations of the Werner Munter Method
**Simplification:** The method simplifies complex avalanche dynamics, potentially overlooking critical factors.
**Human Factors:** Does not account for human errors, experience levels, or decision-making nuances.
**Local Variations:** May not account for microclimates or localized terrain features.

## Data Source Limitations

**Elevation Data**

**Resolution:** Open-Elevation may not provide high-resolution data needed for precise calculations.
**Accuracy:** Elevation data might be outdated or imprecise in some regions.
Weather Data:

**Snowfall Measurements:** Current weather APIs may not provide accurate or real-time snowfall data.
**Wind Data:** Wind speed at ground level may differ significantly from higher elevations.

## Notes
**Unit Conversions:**

Snowfall is converted from millimeters to centimeters.
Wind speed is converted from meters per second to kilometers per hour.
**Error Handling:**

The program includes error handling for missing data and API errors.
Provides default values when data is unavailable. Slope angle for example, is assumed 0 if it cannot be determined. This is a potential source of error, so be wary if the avalanche risk is 0 in an area where this would not be expected.

## Disclaimer
This tool is intended for educational purposes and should not be solely relied upon for making safety decisions in avalanche-prone areas. Avalanche forecasting is complex and requires professional expertise.

Always consult local avalanche forecasts and consider hiring a qualified mountain guide.

Use this tool at your own risk. The developers are not responsible for any incidents arising from its use.

**Contributions and feedback are welcome.**

License: Non-Profit Open Software License 3.0 (NPOSL-3.0)