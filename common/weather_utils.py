"""common utilities related to dealing with weather data and operations"""

from pydantic import BaseModel
from typing import Literal, Optional
import datetime

class ForecastDataRow(BaseModel):
    datetime_cph: datetime.datetime  # You can use `datetime` type if you prefer
    deg_c: float
    deg_c_min: float
    deg_c_max: float
    deg_c_feels: float
    weather: str
    wind: Literal["Low", "Medium", "High", "None"]
    rain: Optional[Literal["Low", "Medium", "High", "None"]]


def fahrenheit_to_celsius(fahrenheit:float):
    """
    Convert fahrenheit to celcius
    """
    celsius = (fahrenheit - 32) * 5.0 / 9.0
    return celsius


def kelvin_to_celsius(kelvin:float):
    """
    Convert temperature from Kelvin to Celsius.
    """
    celsius = kelvin - 273.15
    return celsius

def classify_rain_intensity_3h(rainfall_mm:float):
    """Classify based on the amount of rain"""
    if rainfall_mm < 2.5:
        return 'Low'
    elif 2.5 <= rainfall_mm < 7.6:
        return 'Medium'
    else:
        return 'High'
    
def classify_wind_intensity(speed:float, gust:float):
    # Define thresholds for wind speed (in meters per second)
    if speed < 5:
        intensity = 'Low'
    elif 5 <= speed < 10:
        intensity = 'Medium'
    else:
        intensity = 'High'

    # Adjust classification based on gust speed (in meters per second)
    if gust > 15:
        intensity = 'High'
    elif gust > 10 and intensity == 'Medium':
        intensity = 'High'

    return intensity