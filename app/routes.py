from flask import render_template, request, redirect, url_for
from app import app
from app.weather import get_weather

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    if request.method == 'POST':
        city = request.form['city']
        weather_data = get_weather(city)
        if not weather_data:
            return redirect(url_for('home'))
    return render_template('home.html', weather_data=weather_data)

