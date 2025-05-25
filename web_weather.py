from flask import Flask, render_template_string, request
import requests
import re

app = Flask(__name__)

class WeatherApp:
    def __init__(self):
        self.base_url = "https://wttr.in/"
        self.ip_url = "https://ipinfo.io/json"

    def is_valid_city(self, city):
        # Basic validation: city should only contain letters, spaces, and basic punctuation
        return bool(re.match(r'^[A-Za-z\s\-\',\.]+$', city))

    def get_current_location(self):
        try:
            response = requests.get(self.ip_url)
            response.raise_for_status()
            data = response.json()
            city = data.get('city', '')
            region = data.get('region', '')
            if city and region:
                return f"{city}, {region}"
            return city or 'Unknown'
        except requests.exceptions.RequestException as e:
            return None

    def get_weather(self, city):
        try:
            if not self.is_valid_city(city):
                raise ValueError("Invalid city name. Please enter a valid city name.")

            params = {
                'format': '%l|%C|%t|%h|%w|%p',  # Custom format for parsing
                'units': 'm'
            }
            
            response = requests.get(f"{self.base_url}{city}", params=params)
            response.raise_for_status()
            
            # Parse the response
            location, condition, temp, humidity, wind, precip = response.text.strip().split('|')
            
            # Additional validation for the response
            if 'Unknown location' in location or 'probably' in location.lower():
                raise ValueError("City not found. Please check the spelling and try again.")
            
            return {
                'location': location,
                'condition': condition,
                'temperature': temp,
                'humidity': humidity,
                'wind': wind,
                'precipitation': precip
            }
            
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError("Unable to fetch weather data. Please try a different city.")

# HTML template with modern styling
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Weather Information</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        .container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 30px;
            box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            max-width: 500px;
            width: 100%;
        }
        h1 {
            color: #333;
            margin-bottom: 30px;
            text-align: center;
            font-size: 24px;
        }
        .weather-card {
            text-align: center;
        }
        .location {
            font-size: 24px;
            color: #333;
            margin-bottom: 20px;
        }
        .temperature {
            font-size: 48px;
            color: #1a73e8;
            margin-bottom: 20px;
        }
        .condition {
            font-size: 20px;
            color: #666;
            margin-bottom: 30px;
        }
        .details {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 20px;
        }
        .detail-item {
            padding: 15px;
            background: #f5f5f5;
            border-radius: 10px;
        }
        .detail-label {
            font-size: 14px;
            color: #666;
            margin-bottom: 5px;
        }
        .detail-value {
            font-size: 16px;
            color: #333;
        }
        form {
            margin-top: 30px;
            display: flex;
            gap: 10px;
        }
        input[type="text"] {
            flex: 1;
            padding: 10px 15px;
            border: 2px solid #ddd;
            border-radius: 10px;
            font-size: 16px;
        }
        button {
            padding: 10px 20px;
            background: #1a73e8;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background: #1557b0;
        }
        .error {
            color: #dc3545;
            margin-top: 20px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Weather Information</h1>
        {% if weather %}
        <div class="weather-card">
            <div class="location">{{ weather.location }}</div>
            <div class="temperature">{{ weather.temperature }}</div>
            <div class="condition">{{ weather.condition }}</div>
            <div class="details">
                <div class="detail-item">
                    <div class="detail-label">Humidity</div>
                    <div class="detail-value">{{ weather.humidity }}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Wind</div>
                    <div class="detail-value">{{ weather.wind }}</div>
                </div>
                <div class="detail-item">
                    <div class="detail-label">Precipitation</div>
                    <div class="detail-value">{{ weather.precipitation }}</div>
                </div>
            </div>
        </div>
        {% endif %}
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        <form method="GET">
            <input type="text" name="city" placeholder="Enter city name" value="{{ request.args.get('city', '') }}">
            <button type="submit">Get Weather</button>
        </form>
    </div>
</body>
</html>
'''

weather_app = WeatherApp()

@app.route('/')
def index():
    city = request.args.get('city')
    error = None
    weather_data = None

    if not city:
        # Try to get weather for current location
        city = weather_app.get_current_location()
    
    if city:
        try:
            weather_data = weather_app.get_weather(city)
        except ValueError as e:
            error = str(e)
        except Exception as e:
            error = "An unexpected error occurred. Please try again."
    
    return render_template_string(
        HTML_TEMPLATE,
        weather=weather_data,
        error=error
    )

if __name__ == '__main__':
    app.run(debug=True) 