import streamlit as st
import requests
import pandas as pd
from datetime import datetime


# Function to fetch weather data
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
            "icon": data["weather"][0]["icon"],  # Icon code for display
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
    # Sidebar settings
    st.sidebar.header("Settings")

    # Allow user to input multiple favorite locations
    st.sidebar.subheader("Your Favorite Locations")
    favorite_locations = st.sidebar.text_area(
        "Add your favorite locations (comma-separated):",
        value="London, New York, Mumbai"
    )
    location_list = [loc.strip() for loc in favorite_locations.split(",")]

    # Temperature preference
    temp_unit = st.sidebar.radio(
        "Choose temperature unit:",
        ("Celsius", "Fahrenheit"),
        index=0
    )
    units = "metric" if temp_unit == "Celsius" else "imperial"
    st.sidebar.markdown("---")

    # Main input field
    st.title("🌦️ Weather Information App")
    st.header("Get Weather for Your Locations")
    city_name = st.text_input("Enter city name or choose from favorites:")

    st.info(
        "You can add multiple locations in the sidebar. If a city name is entered above, it will override the default locations.")
    st.markdown("---")

    # Default API Key (replace with your own key!)
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"

    # Fetch weather button
    if st.button("Get Weather"):
        # If a city name is entered, prioritize it
        if city_name:
            location_list = [city_name] + location_list

        # Process each location
        for location in location_list:
            weather_data = get_weather_data(location, api_key, units)

            if "error" in weather_data:
                st.error(f"Error for {location}: {weather_data['error']}")
            else:
                # Local time
                local_time = format_local_datetime(weather_data["timezone"])

                # Display weather information
                st.subheader(f"Weather in {weather_data['city']}")
                col1, col2 = st.columns([3, 1])

                # Output main weather details
                with col1:
                    st.write(f"**Temperature:** {weather_data['temperature']}°{temp_unit[0]}")
                    st.write(f"**Humidity:** {weather_data['humidity']}%")
                    st.write(f"**Condition:** {weather_data['weather_condition'].capitalize()}")
                    st.write(f"**Coordinates:** {weather_data['latitude']}, {weather_data['longitude']}")
                    st.write(f"**Local Date and Time:** {local_time}")

                # Display weather icon
                with col2:
                    icon_url = f"http://openweathermap.org/img/wn/{weather_data['icon']}@2x.png"
                    st.image(icon_url, caption="Weather Icon", use_column_width=True)

                # Display location on a map
                st.map(pd.DataFrame({
                    "lat": [weather_data["latitude"]],
                    "lon": [weather_data["longitude"]]
                }))

    st.markdown("---")
    st.info(
        "You can use this app to explore weather information for multiple locations along with icons for weather conditions!")


# Run the Streamlit app
if __name__ == "__main__":
    main()

