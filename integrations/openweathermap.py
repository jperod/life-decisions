from dotenv import load_dotenv
import requests
import os

# Load environment variables from .env file
load_dotenv()

class OpenWeatherMapApi:

    def __init__(self) -> None:
        self.api_key = os.getenv("OPENWEATHERMAP_API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY environment variable not set")
        
    def get_forecast_by_city(self, city:str):

        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={self.api_key}"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        return data