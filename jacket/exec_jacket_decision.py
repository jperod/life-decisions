"""module to decide which jacket to wear based on weather data"""

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import datetime
import pytz
import subprocess
from common.weather_utils import (
    kelvin_to_celsius,
    classify_rain_intensity_3h,
    classify_wind_intensity,
    ForecastDataRow,
)
from common.utils import run_command
from integrations.openweathermap import OpenWeatherMapApi
from jacket.jacket_decision import MyJacketDecisionMaker, update_jacket_markdown


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
        # wind_speed=wind_speed,
        rain=rain_3h_intensity,
    )
    rows.append(row.model_dump())

df = pd.DataFrame(rows)
df["datetime_cph"] = df["datetime_cph"].dt.strftime("%Y-%m-%d %H:%M")
print(df)

jdm = MyJacketDecisionMaker(rows, verbose=True)
jacket = jdm.decide_jacket()
rain_jacket = jdm.should_take_rain_jacket()


update_jacket_markdown("what-jacket-to-wear.md", jacket, rain_jacket, df)

# # Define the content to be written
# readme_content = f"""# Copenhagen Jacket Decision Maker

# Danish weather is very uncertain, so I made this code to help me decide what jacket to wear based on weather data.

# ## What Jacket to wear?

# - **Datetime**: {get_now_cph_str()}
# - **Recommended Jacket Type**: {jacket}
# - **Take a Rain Jacket?** {rain_jacket}

# ## Weather Forecast
# {df.to_markdown(index=False)}

# """

# # Path to the README.md file
# file_path = "README.md"

# # Write content to the file
# with open(file_path, "w") as file:
#     file.write(readme_content)

# print(f"Content written to {file_path}")


# Git operations

run_command("git add README.md")
run_command("git pull origin")
try:
    run_command('git commit -m "Auto Update README.md with latest information"')
    run_command("git push origin main")
except:
    print("No changes to commit.")

print("Done.")
