# agents/weather_agent.py

import requests
from datetime import datetime, timedelta

class WeatherAgent:
    def __init__(self, api_key='your_openweathermap_key'):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/3.0/onecall"
        
    def get_weather_forecast(self, location):
        """Gets weather forecast for a location (lat, lon)"""
        try:
            params = {
                'lat': location[0],
                'lon': location[1],
                'exclude': 'minutely,hourly',
                'appid': self.api_key,
                'units': 'metric'
            }
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Weather API error: {e}")
            return None
            
    def check_irrigation(self, location, soil_moisture):
        """Determines if irrigation is needed based on weather and soil"""
        forecast = self.get_weather_forecast(location)
        if not forecast:
            return False
            
        # Simple irrigation logic - expand with more sophisticated rules
        next_rain = any(
            'rain' in hour.get('weather', [{}])[0].get('main', '').lower()
            for hour in forecast.get('daily', [])[:2]  # Check next 2 days
        )
        
        return soil_moisture < 30 and not next_rain
