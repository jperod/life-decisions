"""module to decide which jacket to wear based on weather data"""

from enum import Enum
from typing import List

from jacket.common import ForecastDataRow, ForecastUtils
from jacket.rain_jacket import RainJacketDecision


class JacketDecision(Enum):
    # No Rain
    WARM_JACKET = "Warm Jacket"
    REGULAR_JACKET_w_LAYERS = "Regular Jacket with Warm Layers"
    REGULAR_JACKET = "Regular Jacket and T-Shirt"
    LIGHT_JACKET = "T-shirt + Light Jacket"
    TSHIRT = "T-Shirt"

    # Rain Adaption
    WARM_RAIN_JACKET = "Warm Rain Jacket"
    REGULAR_RAIN_JACKET_w_LAYERS = "Rain Jacket with Warm Layers"
    REGULAR_RAIN_JACKET = "Rain Jacket and T-shirt"


class JacketDecisionMaker:

    def __init__(
        self,
        forecast: List[ForecastDataRow],
        rain_jacket_decision: RainJacketDecision = None,
        verbose: bool = False,
    ) -> None:
        self.forecast = forecast
        self.verbose = verbose
        self.rain_jacket_decision = rain_jacket_decision

    def decide_jacket_from_temp(self, warning: bool = True) -> str:
        """Decide which jacket to wear based on temperature alone"""

        ForecastUtils.validate_forecast_not_empty(self.forecast, warning)

        avg_feels_like_temp = ForecastUtils.calculate_avg_feels_temperature(
            self.forecast
        )
        median_feels_like_temp = ForecastUtils.calculate_median_feels_temperature(
            self.forecast
        )
        min_temp = ForecastUtils.calculate_min_temperature(self.forecast)

        # Decision logic
        if avg_feels_like_temp < 2:
            if self.verbose:
                print("Take a warm jacket, it's cold!")
            return JacketDecision.WARM_JACKET.value
        elif avg_feels_like_temp < 8 and median_feels_like_temp < 8:
            if self.verbose:
                print("Take a regular jacket, with layers inside!")
            return JacketDecision.REGULAR_JACKET_w_LAYERS.value
        elif avg_feels_like_temp < 8 and median_feels_like_temp >= 8:
            if self.verbose:
                print("Take a regular jacket with shirt")
            return JacketDecision.REGULAR_JACKET.value
        elif avg_feels_like_temp < 17.5:
            if self.verbose:
                print("Take a regular jacket with shirt")
            return JacketDecision.REGULAR_JACKET.value
        elif avg_feels_like_temp < 20:
            if self.verbose:
                print("No need to take jacket today")
            return JacketDecision.LIGHT_JACKET.value
        elif avg_feels_like_temp >= 20 and min_temp >= 18:
            if self.verbose:
                print("It's hot today, a T-shirt will be all you need")
            return JacketDecision.TSHIRT.value
        else:
            if self.verbose:
                print("It's will be hot and chilly, take a light jacket")
            return JacketDecision.LIGHT_JACKET.value

    def decide_jacket(self) -> str:
        "decide jacket based on both rain and temperature end to end"

        if not self.rain_jacket_decision:
            raise ValueError(
                "Please provide valid rain_jacket_decision dependency when initiating JacketDecisionMaker class."
            )

        ForecastUtils.validate_forecast_not_empty(self.forecast)

        jacket = self.decide_jacket_from_temp(warning=False)
        rain_jacket = self.rain_jacket_decision.decide_rain_jacket(warning=False)

        # Overwrite Adaption with rain jacket when it rains
        if rain_jacket == RainJacketDecision.YES.value:
            if jacket in [
                JacketDecision.REGULAR_JACKET.value,
                JacketDecision.LIGHT_JACKET.value,
                JacketDecision.TSHIRT.value,
            ]:
                jacket = JacketDecision.REGULAR_RAIN_JACKET.value
            elif jacket == JacketDecision.REGULAR_JACKET_w_LAYERS.value:
                jacket = JacketDecision.REGULAR_RAIN_JACKET_w_LAYERS.value
            elif jacket == JacketDecision.WARM_JACKET.value:
                jacket = JacketDecision.WARM_RAIN_JACKET.value

        elif rain_jacket == RainJacketDecision.OPTIONAL.value:
            # Only swap with rain when its little and low rain, and if its t-shirt/light jacket
            if jacket in [
                JacketDecision.LIGHT_JACKET.value,
                JacketDecision.TSHIRT.value,
            ]:
                jacket = JacketDecision.REGULAR_RAIN_JACKET.value

        return jacket
