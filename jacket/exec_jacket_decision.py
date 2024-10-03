"""module to decide which jacket to wear based on weather data"""

import datetime
import os
import sys

# Set the working directory to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)
os.chdir(project_root)  # Change the current working directory to the project root

import pandas as pd
import pytz

from common.utils import GitUtils
from common.weather_utils import (
    ForecastDataRow,
    classify_rain_intensity_3h,
    classify_wind_intensity,
    kelvin_to_celsius,
)
from integrations.openweathermap import OpenWeatherMapApi
from jacket.common import ForecastUtils
from jacket.gloves import GlovesDecisionMaker
from jacket.jacket import JacketDecisionMaker
from jacket.rain_jacket import RainJacketDecisionMaker

openweather_api = OpenWeatherMapApi()

CITY = "Copenhagen"
data = openweather_api.get_forecast_by_city(CITY)


list_data = data["list"]
rows = []
for i, ele in enumerate(list_data[0:5]):

    utc_datetime = datetime.datetime.fromtimestamp(
        ele["dt"], tz=datetime.timezone.utc
    ).astimezone(pytz.timezone("Europe/Copenhagen"))
    deg_c = kelvin_to_celsius(ele["main"]["temp"])
    deg_c_min = kelvin_to_celsius(ele["main"]["temp_min"])
    deg_c_max = kelvin_to_celsius(ele["main"]["temp_max"])
    deg_c_feels = kelvin_to_celsius(ele["main"]["feels_like"])
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
        deg_c_feels=deg_c_feels,
        weather=weather,
        wind=wind,
        rain=rain_3h_intensity,
    )
    rows.append(row.model_dump())

df = pd.DataFrame(rows)
df["datetime_cph"] = df["datetime_cph"].dt.strftime("%Y-%m-%d %H:%M")
print(df)

forecast = rows

rjdm_no_verbose = RainJacketDecisionMaker(forecast, verbose=False)
rjdm_verbose = RainJacketDecisionMaker(forecast, verbose=True)
jdm = JacketDecisionMaker(forecast, rjdm_no_verbose, verbose=True)
gdm = GlovesDecisionMaker(forecast, verbose=True)

jacket = jdm.decide_jacket()
rain_jacket = rjdm_verbose.decide_rain_jacket()
gloves = gdm.decide_gloves()

avg_feels_temp = ForecastUtils.calculate_avg_feels_temperature(forecast)

markdown_file_path = "what-jacket-to-wear.md"
ForecastUtils.update_jacket_markdown(
    markdown_file_path, jacket, rain_jacket, gloves, avg_feels_temp, df
)
GitUtils.add_commit_push(markdown_file_path)
