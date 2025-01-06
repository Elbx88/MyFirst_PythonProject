# PythonProject4
 Erez Levy Enhanced Weather App:
 
 The app asks for a city name input.
 
Useing the requests library to make API calls and retrieve weather data.
The code extract and display relevant data such as temperature, weather conditions, and humidity.

The app  gets weather data for a city using the `requests` library. It uses a weather API (e.g., OpenWeatherMap API) to retrieve the temperature, weather conditions, and humidity.
You'll need an API key from OpenWeatherMap or a similar service.

The `units` parameter in the API request is set to `"metric"` so that temperatures are displayed in Celsius. Use `"imperial"` for Fahrenheit.

The app integrating the weather data script into a Streamlit application.
This includes input fields for location, fetching weather data using your existing weather function, and displaying results in a user-friendly UI.

- Users can enter multiple favorite locations in the sidebar (comma-separated) or type in a specific city in the input box, which takes priority.
- The app attempts to fetch weather data for all provided locations.
- The app calls the OpenWeatherMap API to retrieve weather data, including `latitude`, `longitude`, and `icon` details.
  
For each location retrieved app shows the folloeings:
1. Weather Data Displayed:
    - Temperature based  on user preference (Celsius/Fahrenheit).
    - Humidity, weather condition, and coordinates of the city.
    - Local date and time.
2. Weather Icon:
    - A weather condition icon is displayed to visually represent the city’s weather.
3. Map:
    - A map centered around the city’s latitude and longitude is shown.
Additional Notes:
1. Error Handling:
   Invalid cities return an error message while processing continues for valid ones.
2. Interactive Map:
   Displays pins on the map based on latitude and longitude retrieved from the API.

This enhanced app now delivers a richer, more visually organized weather-checking experience.


