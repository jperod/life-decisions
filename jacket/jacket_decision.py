"""module to decide which jacket to wear based on weather data"""

from enum import Enum
from pydantic import BaseModel
from typing import List
import datetime
from typing import Optional, Literal
import pandas as pd
from common.utils import get_now_cph_str


class ForecastDataRow(BaseModel):
    datetime_cph: datetime.datetime  # You can use `datetime` type if you prefer
    deg_c: float
    deg_c_min: float
    deg_c_max: float
    deg_c_feels: float
    weather: str
    wind: Literal["Low", "Medium", "High", "None"]
    # wind_speed: float
    rain: Optional[Literal["Low", "Medium", "High", "None"]]


class RainJacketDecision(Enum):
    NO = "No"
    OPTIONAL = "Optional"
    YES = "Yes"


class JacketDecision:
    WARM_JACKET = "Warm Jacket"
    REGULAR_JACKET_w_LAYERS = "Regular Jacket with Warm Layers"
    REGULAR_JACKET = "Regular Jacket and T-Shirt"
    LIGHT_JACKET = "T-shirt + Light Jacket"
    TSHIRT = "T-Shirt"


class GlovesDecision(Enum):
    NO = "No"
    YES = "YES"


class MyJacketDecisionMaker:

    def __init__(self, forecast: List[ForecastDataRow], verbose: bool = False) -> None:
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
            if entry["rain"] and entry["rain"] != "None":
                rain_count += 1
                if entry["rain"] == "High":
                    rain_intensity_high += 1
                elif entry["rain"] == "Medium":
                    rain_intensity_medium += 1
                elif entry["rain"] == "Low":
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

    def calculate_avg_feels_temperature(self) -> float:
        """calculate avg feels like temperature in celcius"""
        # Initialize temperature counters
        total_feels_like_temp = 0
        min_temp = -20
        count = 0

        # Iterate over weather data to compute averages and minimums
        for entry in self.forecast:
            total_feels_like_temp += entry["deg_c_feels"]
            min_temp = min(min_temp, entry["deg_c_min"])
            count += 1

        # Calculate average feels-like temperature
        if count == 0:
            return JacketDecision.NO_JACKET  # No data available

        avg_feels_like_temp = round(total_feels_like_temp / count, 1)
        print(f"avg_feels_like_temp = {avg_feels_like_temp} C")
        return avg_feels_like_temp

    def decide_jacket(self) -> str:
        # Initialize temperature counters
        total_feels_like_temp = 0
        min_temp = -20
        count = 0

        # Iterate over weather data to compute averages and minimums
        for entry in self.forecast:
            total_feels_like_temp += entry["deg_c_feels"]
            min_temp = min(min_temp, entry["deg_c_min"])
            count += 1

        # Calculate average feels-like temperature
        if count == 0:
            return JacketDecision.NO_JACKET  # No data available

        avg_feels_like_temp = round(total_feels_like_temp / count, 1)

        # Decision logic
        if avg_feels_like_temp < 6:
            if self.verbose:
                print("Take a warm jacket, it's cold!")
            return JacketDecision.WARM_JACKET
        elif avg_feels_like_temp < 13:
            if self.verbose:
                print("Take a regular jacket, with layers inside!")
            return JacketDecision.REGULAR_JACKET_w_LAYERS
        elif avg_feels_like_temp < 17.5:
            if self.verbose:
                print("Take a regular jacket with shirt")
            return JacketDecision.REGULAR_JACKET
        elif avg_feels_like_temp < 20:
            if self.verbose:
                print("No need to take jacket today")
            return JacketDecision.LIGHT_JACKET
        elif avg_feels_like_temp >= 20 and min_temp >= 18:
            if self.verbose:
                print("It's hot today, a T-shirt will be all you need")
            return JacketDecision.TSHIRT
        else:
            if self.verbose:
                print("It's will be hot and chilly, take a light jacket")
            return JacketDecision.LIGHT_JACKET

    def decide_gloves(self) -> str:
        # Initialize temperature counters
        total_feels_like_temp = 0
        min_temp = -20
        count = 0

        # Iterate over weather data to compute averages and minimums
        for entry in self.forecast:
            if "deg_c_feels" in entry:
                total_feels_like_temp += entry["deg_c_feels"]
                min_temp = min(min_temp, entry["deg_c_min"])
                count += 1

        # Calculate average feels-like temperature
        if count == 0:
            return GlovesDecision.NO  # No data available

        avg_feels_like_temp = total_feels_like_temp / count

        # Decision logic
        if avg_feels_like_temp <= 0:
            if self.verbose:
                print("Wear warm gloves, it's very cold!")
            return GlovesDecision.YES.value
        elif avg_feels_like_temp <= 8:
            if self.verbose:
                print("Wear gloves, it's cold but manageable.")
            return GlovesDecision.YES.value
        else:
            if self.verbose:
                print("No need for gloves today.")
            return GlovesDecision.NO.value

    def update_jacket_markdown(
        self,
        file_path: str,
        jacket: str,
        rain_jacket: str,
        gloves: str,
        avg_feels_temp: float,
        df: pd.DataFrame,
    ):
        """Updates the target markdown file with weather-related content.

        Args:
            file_path (str): Path to the markdown file to update (e.g., "README.md").
            jacket (str): Recommended jacket type.
            rain_jacket (str): Whether or not a rain jacket is needed.
            gloves (str): Whether gloves are needed.
            df (pd.DataFrame): Weather forecast data as a DataFrame.
        """

        # Define the content to be written into the markdown file
        readme_content = f"""
# Copenhagen Jacket Decision Maker

Danish weather is very uncertain, so I made this app to help me decide what jacket to wear based on weather data. 
It also help me know when it gets cold enough to take gloves or when I should be prepared for rain.

## What Jacket to wear?

- **Datetime**: {get_now_cph_str()}
- **Recommended Jacket Type**: {jacket}
- **Take a Rain Jacket?** {rain_jacket}
- **Take Gloves?** {gloves}

## Weather Forecast
- Avg Feels Like Temperature: {avg_feels_temp} °C

{df.to_markdown(index=False).strip()}
        """

        # Write content to the specified file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(readme_content)

        print(f"Content written to {file_path}")
