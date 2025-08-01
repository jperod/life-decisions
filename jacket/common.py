import datetime
import statistics
import warnings
from typing import List, Literal, Optional

import pandas as pd
from pydantic import BaseModel

from common.utils import get_now_cph_str
from common.weather_utils import ForecastDataRow


class ForecastUtils:

    @staticmethod
    def validate_forecast_not_empty(
        forecast: List[ForecastDataRow], warning: bool = True
    ) -> None:

        # Check if forecast is None or empty
        if not forecast:
            raise ValueError(
                "Forecast data must not be empty or None. It must contain at least one row."
            )

        # Check if forecast has different than 5 rows
        if len(forecast) != 5 and warning:
            warnings.warn(
                f"Warning: Forecast data contains {len(forecast)} rows, but 5 rows are expected.",
                UserWarning,
            )

    @staticmethod
    def calculate_avg_feels_temperature(
        forecast: List[ForecastDataRow], verbose: bool = False
    ) -> float:
        """calculate avg feels like temperature in celcius"""

        ForecastUtils.validate_forecast_not_empty(forecast, warning=False)

        # Initialize temperature counters
        total_feels_like_temp = 0
        count = 0

        # Iterate over weather data to compute averages and minimums
        for entry in forecast:
            total_feels_like_temp += entry["deg_c_feels"]
            count += 1

        # Calculate average feels-like temperature
        avg_feels_like_temp = round(total_feels_like_temp / count, 1)
        if verbose:
            print(f"avg_feels_like_temp = {avg_feels_like_temp} C")
        return avg_feels_like_temp

    @staticmethod
    def calculate_median_feels_temperature(
        forecast: List[ForecastDataRow], verbose: bool = False
    ) -> float:
        """Calculate the median feels-like temperature in Celsius."""
        # List to store feels-like temperatures
        feels_like_temps = []

        # Iterate over weather data to collect feels-like temperatures
        for entry in forecast:
            feels_like_temps.append(entry["deg_c_feels"])

        # Calculate median feels-like temperature
        if not feels_like_temps:  # Check if the list is empty
            raise ValueError()

        median_feels_like_temp = round(statistics.median(feels_like_temps), 1)
        if verbose:
            print(f"median_feels_like_temp = {median_feels_like_temp} C")
        return median_feels_like_temp

    @staticmethod
    def calculate_min_temperature(forecast: List[ForecastDataRow]) -> float:

        ForecastUtils.validate_forecast_not_empty(forecast, warning=False)

        # Iterate over weather data to compute averages and minimums
        for i, entry in enumerate(forecast):
            if i == 0:
                min_temp = entry["deg_c_min"]
            else:
                min_temp = min(min_temp, entry["deg_c_min"])
        return min_temp

    @staticmethod
    def update_jacket_markdown(
        file_path: str,
        jacket: str,
        rain_jacket: str,
        gloves: str,
        avg_feels_temp: float,
        median_feels_temp: float,
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

Danish weather can be quite unpredictable, so I created this app to help me decide which jacket to wear based on the weather forecast. 
It also alerts me when it's cold enough to bring gloves or when I should be ready for rain.

## What Jacket to wear?

- **Datetime**: {get_now_cph_str()}
- **Jacket**: {jacket}
- **Rain?** {rain_jacket}
- **Gloves?** {gloves}

## Weather Forecast
- Avg Feels Like Temperature: {avg_feels_temp} °C
- Median Feels Like Temperature: {median_feels_temp} °C

{df.to_markdown(index=False).strip()}
        """

        # Write content to the specified file
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(readme_content)

        print(f"Content written to {file_path}")
