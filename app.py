
import streamlit as st
import requests
import pandas as pd
st.title('Weather App')

name = st.text_input('Enter your name', '')
if name:
    st.write(f'Hello {name}, welcome to the weather app!')

# To run this app, use the command line to navigate to the app's directory and type:
# streamlit run app.py

import streamlit as st
import requests
import pandas as pd
from datetime import datetime
from typing import List


# Function to fetch weather data for a single city
def get_weather_data(city_name, api_key, units="metric"):
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city_name,
        'appid': api_key,
        'units': units
    }
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        return {
            "city": city_name,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather_condition": data["weather"][0]["description"],
            "latitude": data["coord"]["lat"],
            "longitude": data["coord"]["lon"],
            "timezone": data["timezone"],
        }
    else:
        return {"error": response.json().get("message", "Unable to fetch weather data.")}


# Function to get local date and time
def format_local_datetime(timezone_offset):
    utc_now = datetime.utcnow()
    local_time = utc_now + pd.Timedelta(seconds=timezone_offset)
    return local_time.strftime("%A, %d %B %Y, %H:%M:%S")


# Main function to handle Streamlit app
def main():
    # Sidebar for user preferences
    st.sidebar.header("Settings")

    # Allow the user to add or select favorite locations
    st.sidebar.subheader("Your Favorite Locations")
    favorite_locations = st.sidebar.text_area(
        "Add your favorite locations (comma-separated):",
        value="London, New York, Mumbai"
    )

    # Convert the entered locations into a list
    location_list = [loc.strip() for loc in favorite_locations.split(",")]

    # User temperature preference
    temp_unit = st.sidebar.radio(
        "Choose temperature unit:",
        ("Celsius", "Fahrenheit"),
        index=0
    )
    units = "metric" if temp_unit == "Celsius" else "imperial"

    st.sidebar.markdown("---")

    # Main input field for city name
    st.title("🌦️ Weather Information App")
    st.header("Get Weather for Your Locations")
    city_name = st.text_input("Enter city name or choose from favorites:")

    # Instructions
    st.info(
        "You can add multiple locations in the sidebar. If a city name is entered above, it will override the default locations.")
    st.markdown("---")

    # Default API Key (replace with your own key)
    api_key = "8960a7d651c4f421d47cc640cc3f0e23"

    # Button to fetch weather
    if st.button("Get Weather"):
        # If a user manually enters a city, prioritize it
        if city_name:
            location_list = [city_name] + location_list

        # Handle weather data for multiple locations
        for location in location_list:
            weather_data = get_weather_data(location, api_key, units)

            # If an error occurs, display it without terminating the app
            if "error" in weather_data:
                st.error(f"Error for {location}: {weather_data['error']}")
            else:
                # Display weather information for each location
                st.subheader(f"Weather in {weather_data['city']}")

                # Retrieve and display local datetime
                local_time = format_local_datetime(weather_data["timezone"])

                # Display weather data
                st.write(f"**Temperature:** {weather_data['temperature']}°{temp_unit[0]}")
                st.write(f"**Humidity:** {weather_data['humidity']}%")
                st.write(f"**Condition:** {weather_data['weather_condition'].capitalize()}")
                st.write(f"**Local Date and Time:** {local_time}")

                # Display city on a map
                st.map(pd.DataFrame({
                    "lat": [weather_data["latitude"]],
                    "lon": [weather_data["longitude"]]
                }))

    st.markdown("---")
    st.info(
        "This app allows you to set your own preferences for favorite locations and temperature units. These are optional enhancements!")


# Run the Streamlit app
if __name__ == "__main__":
    main()