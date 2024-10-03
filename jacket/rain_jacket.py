from enum import Enum
from typing import List

from jacket.common import ForecastDataRow, ForecastUtils


class RainJacketDecision(Enum):
    NO = "No"
    OPTIONAL = "Optional"
    YES = "Yes"

class RainJacketDecisionMaker:

    def __init__(self, forecast: List[ForecastDataRow], verbose: bool = False) -> None:
        self.forecast = forecast
        self.verbose = verbose

    def decide_rain_jacket(self, warning:bool=True) -> str:

        # Initialize counters
        rain_count = 0
        rain_intensity_high = 0
        rain_intensity_medium = 0
        rain_intensity_low = 0

        ForecastUtils.validate_forecast_not_empty(self.forecast, warning)

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