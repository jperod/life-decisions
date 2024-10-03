from enum import Enum
from typing import List

from jacket.common import ForecastDataRow, ForecastUtils


class GlovesDecision(Enum):
    NO = "No"
    YES = "Yes"


class GlovesDecisionMaker:

    def __init__(self, forecast: List[ForecastDataRow], verbose: bool = False) -> None:
        self.forecast = forecast
        self.verbose = verbose

    def decide_gloves(self) -> str:
        # Initialize temperature counters
        total_feels_like_temp = 0
        count = 0


        ForecastUtils.validate_forecast_not_empty(self.forecast)
        
        # Iterate over weather data to compute averages and minimums
        for i, entry in enumerate(self.forecast):
            total_feels_like_temp += entry["deg_c_feels"]
            if i == 0:
                min_temp = entry["deg_c_min"]
            else:
                min_temp = min(min_temp, entry["deg_c_min"])
            count += 1


        avg_feels_like_temp = total_feels_like_temp / count

        # Decision logic
        if avg_feels_like_temp <= 4:
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