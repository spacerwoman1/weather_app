import requests

class SimpleWeatherApp:
    def __init__(self):
        self.base_url = "https://wttr.in/"
        self.ip_url = "https://ipinfo.io/json"

    def get_current_location(self):
        try:
            response = requests.get(self.ip_url)
            response.raise_for_status()
            data = response.json()
            # ipinfo.io returns city and region
            city = data.get('city', '')
            region = data.get('region', '')
            if city and region:
                return f"{city}, {region}"
            return city or 'Unknown'
        except requests.exceptions.RequestException as e:
            print(f"Error detecting location: {e}")
            return None

    def get_weather(self, city):
        try:
            # Add parameters for a cleaner output format
            params = {
                'format': '%l: %C %t\nHumidity: %h\nWind: %w\nPrecipitation: %p\n',
                'units': 'm'  # Metric units
            }
            
            response = requests.get(f"{self.base_url}{city}", params=params)
            response.raise_for_status()
            
            return response.text.strip()
            
        except requests.exceptions.RequestException as e:
            return f"Error fetching weather data: {e}"

def main():
    weather_app = SimpleWeatherApp()
    
    # First, try to get current location
    print("\nDetecting your location...")
    current_city = weather_app.get_current_location()
    
    if current_city:
        print(f"Your current location appears to be: {current_city}")
        print("\nHere's your local weather:")
        result = weather_app.get_weather(current_city)
        print(f"\n{result}")
    
    while True:
        print("\nSimple Weather Information")
        print("-------------------------")
        print("Enter city name (or 'quit' to exit)")
        print("Press Enter to check your current location again")
        city = input("> ")
        
        if city.lower() == 'quit':
            print("Goodbye!")
            break
        
        if city == '':
            # If user just presses Enter, show current location weather
            current_city = weather_app.get_current_location()
            if current_city:
                print(f"\nYour current location: {current_city}")
                city = current_city
            else:
                continue
        
        result = weather_app.get_weather(city)
        print(f"\n{result}")

if __name__ == "__main__":
    main() 