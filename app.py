
import streamlit as st
import requests
import pandas as pd
from datetime import datetime


# Fetch weather data for a specific location
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
            "pressure": data["main"]["pressure"],  # Pressure in hPa
            "wind_speed": data["wind"]["speed"],  # Wind speed
            "weather_condition": data["weather"][0]["description"],
            "latitude": data["coord"]["lat"],
            "longitude": data["coord"]["lon"],
            "icon": data["weather"][0]["icon"],  # Icon code
            "timezone": data["timezone"]
        }
    else:
        return {"error": response.json().get("message", "Unable to fetch weather data.")}


# Format local date and time
def format_local_datetime(timezone_offset):
    utc_now = datetime.utcnow()
    local_time = utc_now + pd.Timedelta(seconds=timezone_offset)
    return local_time.strftime("%A, %d %B %Y, %H:%M:%S")


# Main function
def main():
    # Sidebar configuration
    st.sidebar.header("Settings")

    # User input: Favorite locations
    st.sidebar.subheader("Your Favorite Locations")
    favorite_locations = st.sidebar.text_area(
        "Add your favorite locations (comma-separated):",
        value="London, New York, Mumbai"
    )
    location_list = [loc.strip() for loc in favorite_locations.split(",")]

    # User preference: Temperature unit
    temp_unit = st.sidebar.radio(
        "Choose temperature unit:",
        ("Celsius", "Fahrenheit"),
        index=0
    )
    units = "metric" if temp_unit == "Celsius" else "imperial"
    st.sidebar.markdown("---")

    # Main app title and input
    st.title("🌦️ Enhanced Weather Information App")
    st.header("Get Weather for Your Locations")
    city_name = st.text_input("Enter city name or prioritize it over saved locations:")

    st.info(
        "You can add multiple locations in the sidebar. If a city is entered manually, it takes precedence over saved locations.")
    st.markdown("---")

    # Set up API key (replace with your own key)
    api_key = "8960a7d651c4f421d47cc640cc3f0e23"

    # Process on button click
    if st.button("Get Weather"):
        # If a user manually enters a city, prioritize it
        if city_name:
            location_list = [city_name] + location_list

        # Fetch and display weather data for each location
        for location in location_list:
            weather_data = get_weather_data(location, api_key, units)

            if "error" in weather_data:
                st.error(f"Error for {location}: {weather_data['error']}")
            else:
                # Local date and time
                local_time = format_local_datetime(weather_data["timezone"])

                # Display weather details
                st.subheader(f"Weather in {weather_data['city']}")

                # Layout columns for better UI
                col1, col2 = st.columns([3, 1])

                # Primary weather data in column 1
                with col1:
                    st.markdown(f"**Temperature:** {weather_data['temperature']}°{temp_unit[0]}")
                    st.markdown(f"**Humidity:** {weather_data['humidity']}%")
                    st.markdown(f"**Pressure:** {weather_data['pressure']} hPa")
                    st.markdown(f"**Wind Speed:** {weather_data['wind_speed']} m/s")
                    st.markdown(f"**Weather Condition:** {weather_data['weather_condition'].capitalize()}")
                    st.markdown(f"**Coordinates:** {weather_data['latitude']}, {weather_data['longitude']}")
                    st.markdown(f"**Local Date and Time:** {local_time}")

                # Weather icon in column 2
                with col2:
                    icon_url = f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png"
                    st.image(icon_url, caption="Weather Icon", use_container_width=True)

                # Map
                st.map(pd.DataFrame({
                    "lat": [weather_data["latitude"]],
                    "lon": [weather_data["longitude"]]
                }))

    st.markdown("---")
    st.info("This enhanced app now includes wind speed, pressure, weather icons, and a better organized layout!")


# Run the app
if __name__ == "__main__":
    main()
