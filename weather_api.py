import streamlit as st
import requests


# Weather data fetching function (can be modularized into its own file)
def get_weather_data(city_name, api_key):
    # Base URL for the OpenWeatherMap API
    base_url = "http://api.openweathermap.org/data/2.5/weather"

    # Parameters for the API request
    params = {
        'q': city_name,
        'appid': api_key,
        'units': 'metric'  # Use 'metric' for Celsius
    }

    # Make the API call
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        # Parse the response JSON
        data = response.json()
        return {
            "city": city_name,
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "weather_condition": data["weather"][0]["description"],
        }
    else:
        # Return an error message if the API call fails
        return {"error": response.json().get("message", "Unable to fetch weather data.")}


# Streamlit app code
def main():
    # Streamlit app title
    st.title("Weather Information App")

    # Input fields for location
    city_name = st.text_input("Enter City Name", "")
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your OpenWeatherMap API key

    # Button to fetch weather data
    if st.button("Get Weather"):
        if city_name:
            # Fetch weather data
            weather_data = get_weather_data(city_name, api_key)
#           from weather_api import get_weather_data

            # Display weather data if available
            if "error" in weather_data:
                st.error(f"Error: {weather_data['error']}")
            else:
                st.success("Weather Data Retrieved Successfully!")
                st.write(f"**City:** {weather_data['city']}")
                st.write(f"**Temperature:** {weather_data['temperature']}°C")
                st.write(f"**Weather Condition:** {weather_data['weather_condition'].capitalize()}")
                st.write(f"**Humidity:** {weather_data['humidity']}%")
        else:
            st.warning("Please enter a city name before fetching weather data.")


# Run the Streamlit app
if __name__ == "__main__":
    main()

