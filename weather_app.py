import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class WeatherApp:
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY')
        if not self.api_key:
            raise ValueError("OPENWEATHER_API_KEY environment variable is not set")
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        try:
            # Make API request
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric'
            }
            
            # Add User-Agent header
            headers = {
                'User-Agent': 'Mozilla/5.0'
            }
            
            response = requests.get(self.base_url, params=params, headers=headers)
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")
            
            response.raise_for_status()
            
            # Parse weather data
            weather_data = response.json()
            
            # Extract relevant information
            temperature = weather_data['main']['temp']
            humidity = weather_data['main']['humidity']
            description = weather_data['weather'][0]['description']
            
            # Format and return weather information
            return f"""
Weather in {city}:
Temperature: {temperature}°C
Humidity: {humidity}%
Conditions: {description.capitalize()}
"""
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {e}\nPlease make sure your API key is activated (it can take 2-4 hours after registration)"
        except (KeyError, IndexError) as e:
            return f"Error parsing weather data: {e}"

def main():
    weather_app = WeatherApp()
    
    while True:
        print("\nWeather Information App")
        print("----------------------")
        city = input("Enter city name (or 'quit' to exit): ")
        
        if city.lower() == 'quit':
            print("Goodbye!")
            break
        
        result = weather_app.get_weather(city)
        print(result)

if __name__ == "__main__":
    main() 