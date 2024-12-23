document.addEventListener('DOMContentLoaded', () => {
    const fetchWeatherData = (lat, lon) => {
        fetch(`/weather?lat=${lat}&lon=${lon}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    // Update UI with weather data
                    document.querySelector('.weather-info').innerHTML = `
                        <h2>Weather in ${data.name}</h2>
                        <p>Temperature: ${data.main.temp}°C</p>
                        <p>Condition: ${data.weather[0].description}</p>
                        <p>Humidity: ${data.main.humidity}%</p>
                        <p>Wind Speed: ${data.wind.speed} m/s</p>
                    `;
                }
            })
            .catch(error => console.error('Error fetching weather:', error));
    };

    // Fetch weather by geolocation
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
            const { latitude, longitude } = position.coords;
            fetchWeatherData(latitude, longitude);
        });
    }
});
