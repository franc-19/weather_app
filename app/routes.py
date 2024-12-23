import requests
from flask import Flask, render_template, request, redirect, url_for, jsonify
from app import app
import os
from dotenv import load_dotenv

# Load the environment variables from .env file
load_dotenv()

# Fetch the API Key from environment variables
API_KEY = os.getenv("API_KEY")

# Updated function to fetch weather data from OpenWeather API with 401 status check
def get_weather(city=None, lat=None, lon=None):
    try:
        if city:
            # Fetch weather data using OpenWeather API based on city
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        elif lat and lon:
            # Fetch weather data using OpenWeather API based on lat/lon
            url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        else:
            return None

        response = requests.get(url)
        if response.status_code == 401:
            print("Unauthorized access. Please check your API key.")
            return None
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        data = response.json()

        # Ensure the API response contains valid data
        if data.get('cod') != 200:
            return None  # Return None if API response is not successful

        return data

    except requests.RequestException as e:
        print(f"Error fetching weather data: {e}")
        return None


# Function to fetch hourly forecast data
def get_hourly_forecast(lat, lon):
    try:
        # Fetch hourly forecast data using OpenWeather One Call API
        url = f"http://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=minutely,daily,alerts&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()

        # Return forecast data if valid
        if 'hourly' in data:
            return data
        return None

    except requests.RequestException as e:
        print(f"Error fetching forecast data: {e}")
        return None


# Function to fetch 5-day forecast data
def get_daily_forecast(lat, lon):
    try:
        # Fetch 5-day forecast data using OpenWeather API
        url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()  # Raise HTTPError for bad responses
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching 5-day forecast data: {e}")
        return None


@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city', '').strip()
        if city:
            weather_data = get_weather(city=city)
        if not weather_data:
            return redirect(url_for('home', error="Invalid city name. Please try again."))

    return render_template('home.html', weather_data=weather_data)


@app.route('/weather', methods=['GET'])
def weather():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required.'}), 400

    # Fetch current weather data based on lat/lon
    weather_data = get_weather(lat=lat, lon=lon)
    if weather_data:
        return jsonify(weather_data)
    else:
        return jsonify({'error': 'Unable to fetch weather data'}), 400


@app.route('/hourly-forecast', methods=['GET'])
def hourly_forecast():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required.'}), 400

    # Fetch hourly forecast data based on lat/lon
    forecast_data = get_hourly_forecast(lat=lat, lon=lon)
    if forecast_data:
        return jsonify(forecast_data)
    else:
        return jsonify({'error': 'Unable to fetch hourly forecast data'}), 400


@app.route('/daily-forecast', methods=['GET'])
def daily_forecast():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude are required.'}), 400

    # Fetch 5-day forecast data based on lat/lon
    forecast_data = get_daily_forecast(lat=lat, lon=lon)
    if forecast_data:
        return jsonify(forecast_data)
    else:
        return jsonify({'error': 'Unable to fetch daily forecast data'}), 400


if __name__ == '__main__':
    app.run(debug=True)
