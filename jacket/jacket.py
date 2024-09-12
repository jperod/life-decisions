"""module to decide which jacket to wear based on weather data"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from enum import Enum
import pandas as pd
from pydantic import BaseModel
from typing import List
import datetime
import pytz
from common.weather_utils import (
    kelvin_to_celsius,
    classify_rain_intensity_3h,
    classify_wind_intensity,
)
from integrations.openweathermap import OpenWeatherMapApi


from typing import Optional, Literal


class ForecastDataRow(BaseModel):
    datetime_cph: datetime.datetime  # You can use `datetime` type if you prefer
    deg_c: float
    deg_c_min: float
    deg_c_max: float
    deg_c_feels_like: float
    weather: str
    wind: Literal["Low", "Medium", "High", "None"]
    wind_speed: float
    rain: Optional[Literal["Low", "Medium", "High", "None"]]

class RainJacketDecision(Enum):
    NO = "No"
    OPTIONAL = "Optional"
    YES = "Yes"

class JacketDecision:
    WARM_JACKET = "Warm Jacket"
    REGULAR_JACKET = "Regular Jacket"
    NO_JACKET = "No Jacket"
    OPTIONAL_JACKET = "Optional Jacket"

class MyJacketDecisionMaker:

    def __init__(self, forecast: List[ForecastDataRow], verbose:bool=False) -> None:
        self.forecast = forecast
        self.verbose = verbose

    def should_take_rain_jacket(self) -> str:

        # Initialize counters
        rain_count = 0
        rain_intensity_high = 0
        rain_intensity_medium = 0
        rain_intensity_low = 0
        
        # Iterate over weather data
        for entry in self.forecast:
            if entry['rain'] and entry['rain'] != 'None':
                rain_count += 1
                if entry['rain'] == 'High':
                    rain_intensity_high += 1
                elif entry['rain'] == 'Medium':
                    rain_intensity_medium += 1
                elif entry['rain'] == 'Low':
                    rain_intensity_low += 1
        
        # Decision logic
        if rain_count == 0:
            if self.verbose:
                print("No need to take a rain jacket")
            return RainJacketDecision.NO.value
        
        if rain_intensity_high > 0:
            if self.verbose:
                print("Take a rain jacket (high intensity rain)")
            return RainJacketDecision.YES.value
        
        if rain_intensity_medium > 0:
            if self.verbose:
                print("Take a rain jacket (medium intensity rain)")
            return RainJacketDecision.YES.value
        
        if rain_intensity_low >= 3:
            if self.verbose:
                print("Take a rain jacket (low intensity rain but consistent)")
            return RainJacketDecision.YES.value
        
        if rain_intensity_low > 0:
            if self.verbose:
                print("Optionally take a rain jacket (low intensity rain)")
            return RainJacketDecision.OPTIONAL.value
        
        return RainJacketDecision.NO.value
        
    
    def decide_jacket(self) -> str:
        # Initialize temperature counters
        total_feels_like_temp = 0
        min_temp = -20
        count = 0
        
        # Iterate over weather data to compute averages and minimums
        for entry in self.forecast:
            if 'deg_c_feels_like' in entry:
                total_feels_like_temp += entry['deg_c_feels_like']
                min_temp = min(min_temp, entry['deg_c_min'])
                count += 1
        
        # Calculate average feels-like temperature
        if count == 0:
            return JacketDecision.NO_JACKET  # No data available
        
        avg_feels_like_temp = total_feels_like_temp / count

        # Decision logic
        if avg_feels_like_temp < 8:
            if self.verbose:
                print("Take a warm jacket, it's cold!")
            return JacketDecision.WARM_JACKET
        elif avg_feels_like_temp < 12:
            if self.verbose:
                print("Take a regular jacket, with layers inside!")
            return JacketDecision.REGULAR_JACKET
        elif avg_feels_like_temp < 17:
            if self.verbose:
                print("Take a regular jacket with shirt")
            return JacketDecision.REGULAR_JACKET
        elif avg_feels_like_temp > 17 and min_temp >= 16:
            if self.verbose:
                print("No need to take jacket today")
            return JacketDecision.NO_JACKET
        elif avg_feels_like_temp >= 20 and min_temp >= 18:
            if self.verbose:
                print("It's hot today, a T-shirt will be all you need")
            return JacketDecision.NO_JACKET


openweather_api = OpenWeatherMapApi()


CITY = "Copenhagen"
data = openweather_api.get_forecast_by_city(CITY)


list_data = data["list"]
rows = []
for i, ele in enumerate(list_data[0:5]):

    if i == 0:
        print(ele)
    utc_datetime = datetime.datetime.fromtimestamp(
        ele["dt"], tz=datetime.timezone.utc
    ).astimezone(pytz.timezone("Europe/Copenhagen"))
    print(utc_datetime)
    deg_c = kelvin_to_celsius(ele["main"]["temp"])
    deg_c_min = kelvin_to_celsius(ele["main"]["temp_min"])
    deg_c_max = kelvin_to_celsius(ele["main"]["temp_max"])
    deg_c_feels_like = kelvin_to_celsius(ele["main"]["feels_like"])
    weather = ele["weather"][0]["main"]
    wind_speed = ele["wind"]["speed"]
    wind_gust = ele["wind"]["gust"]
    wind = classify_wind_intensity(wind_speed, wind_gust)
    rain_3h_intensity = (
        classify_rain_intensity_3h(ele["rain"]["3h"]) if "rain" in ele else "None"
    )

    row = ForecastDataRow(
        datetime_cph=utc_datetime,
        deg_c=deg_c,
        deg_c_min=deg_c_min,
        deg_c_max=deg_c_max,
        deg_c_feels_like=deg_c_feels_like,
        weather=weather,
        wind=wind,
        wind_speed=wind_speed,
        rain=rain_3h_intensity,
    )
    rows.append(row.model_dump())

df = pd.DataFrame(rows)
print(df)

jdm = MyJacketDecisionMaker(rows, verbose=True)
jdm.should_take_rain_jacket()
jdm.decide_jacket()