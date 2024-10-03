import warnings
from datetime import datetime

import pytest

from jacket.jacket_decision import (GlovesDecision, JacketDecision,
                                    MyJacketDecisionMaker, RainJacketDecision)


class TestMyJacketDecisionMakerRain:


    def test_no_rain(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 8, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 11, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"}
        ]
        decision_maker = MyJacketDecisionMaker(forecast)
        assert decision_maker.should_take_rain_jacket() == RainJacketDecision.NO.value

    def test_high_intensity_rain(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 8, 0), "rain": "High"},
            {"datetime_cph": datetime(2024, 10, 2, 11, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"}
        ]
        decision_maker = MyJacketDecisionMaker(forecast)
        assert decision_maker.should_take_rain_jacket() == RainJacketDecision.YES.value

    def test_medium_intensity_rain(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 8, 0), "rain": "Medium"},
            {"datetime_cph": datetime(2024, 10, 2, 11, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"}
        ]
        decision_maker = MyJacketDecisionMaker(forecast)
        assert decision_maker.should_take_rain_jacket() == RainJacketDecision.YES.value

    def test_low_intensity_rain_consistent(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 8, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 11, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "Low"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "Low"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "Low"}
        ]
        decision_maker = MyJacketDecisionMaker(forecast)
        assert decision_maker.should_take_rain_jacket() == RainJacketDecision.YES.value

    def test_low_intensity_rain_optional(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "Low"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"}
        ]
        decision_maker = MyJacketDecisionMaker(forecast)
        assert decision_maker.should_take_rain_jacket() == RainJacketDecision.OPTIONAL.value

    def test_mixed_rain(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "Low"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "Medium"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "High"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"}
        ]
        decision_maker = MyJacketDecisionMaker(forecast)
        assert decision_maker.should_take_rain_jacket() == RainJacketDecision.YES.value

    def test_realistic_forecast(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "Low"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "Low"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 23, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 3, 2, 0), "rain": "None"}
        ]
        decision_maker = MyJacketDecisionMaker(forecast)
        assert decision_maker.should_take_rain_jacket() == RainJacketDecision.OPTIONAL.value


class TestMyJacketDecisionMakerWeather:


    def test_calculate_avg_feels_temperature(self):
        # Test case with multiple entries
        forecast = [
            {"deg_c_feels": 12, "deg_c_min": 11.27},
            {"deg_c_feels": 13, "deg_c_min": 11.28},
            {"deg_c_feels": 11, "deg_c_min": 11.65},
            {"deg_c_feels": 8, "deg_c_min": 10},
            {"deg_c_feels": 6.67, "deg_c_min": 8}
        ]
        jdm = MyJacketDecisionMaker(forecast)
        assert jdm.calculate_avg_feels_temperature() == 10.1

    def test_calculate_avg_feels_temperature_with_one_entry(self):
        # Test case with a single entry
        forecast = [
            {"deg_c_feels": 10, "deg_c_min": 5}
        ]
        weather = MyJacketDecisionMaker(forecast)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert weather.calculate_avg_feels_temperature() == 10.0
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "Forecast data contains 1 rows, but 5 rows are expected." in str(w[-1].message)

    def test_calculate_avg_feels_temperature_with_no_entry(self):
        # Test case with no entries
        forecast = []
        weather = MyJacketDecisionMaker(forecast)
        with pytest.raises(ValueError):
            weather.calculate_avg_feels_temperature()

    def test_calculate_avg_feels_temperature_with_negative_temps(self):
        # Test case with negative temperatures
        forecast = [
            {"deg_c_feels": -5, "deg_c_min": -10},
            {"deg_c_feels": -10, "deg_c_min": -10},
            {"deg_c_feels": -10, "deg_c_min": -10},
            {"deg_c_feels": -10, "deg_c_min": -10},
            {"deg_c_feels": -15, "deg_c_min": -20}
        ]
        weather = MyJacketDecisionMaker(forecast)
        assert weather.calculate_avg_feels_temperature() == -10.0

class TestMyJacketDecisionMaker:

    def test_decide_jacket_no_entries(self):
        forecast = []
        weather = MyJacketDecisionMaker(forecast)
        with pytest.raises(ValueError, match="Forecast data must not be empty or None. It must contain at least one row."):
            weather.decide_jacket()

    def test_decide_jacket_none_forecast(self):
        # Test case with None forecast
        weather = MyJacketDecisionMaker(None)
        with pytest.raises(ValueError, match="Forecast data must not be empty or None. It must contain at least one row."):
            weather.decide_jacket()

    def test_decide_jacket_less_than_five_entries(self):
        # Test case with less than 5 entries
        forecast = [
            {"deg_c_feels": 5, "deg_c_min": 0},
            {"deg_c_feels": 7, "deg_c_min": 2}
        ]
        weather = MyJacketDecisionMaker(forecast)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert weather.decide_jacket() == JacketDecision.REGULAR_JACKET_w_LAYERS.value
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "Forecast data contains 2 rows, but 5 rows are expected." in str(w[-1].message)

    def test_decide_jacket_cold_weather(self):
        # Test case with cold weather
        forecast = [
            {"deg_c_feels": 0, "deg_c_min": -5},
            {"deg_c_feels": 2, "deg_c_min": -3},
            {"deg_c_feels": 4, "deg_c_min": -2},
            {"deg_c_feels": 5, "deg_c_min": -1},
            {"deg_c_feels": 6, "deg_c_min": 0}
        ]
        weather = MyJacketDecisionMaker(forecast)
        assert weather.decide_jacket() == JacketDecision.WARM_JACKET.value

    def test_decide_jacket_regular_jacket_with_layers(self):
        # Test case with regular jacket with layers weather
        forecast = [
            {"deg_c_feels": 7, "deg_c_min": 2},
            {"deg_c_feels": 8, "deg_c_min": 3},
            {"deg_c_feels": 9, "deg_c_min": 4},
            {"deg_c_feels": 10, "deg_c_min": 5},
            {"deg_c_feels": 11, "deg_c_min": 6}
        ]
        weather = MyJacketDecisionMaker(forecast)
        assert weather.decide_jacket() == JacketDecision.REGULAR_JACKET_w_LAYERS.value

    def test_decide_jacket_regular_jacket(self):
        # Test case with regular jacket weather
        forecast = [
            {"deg_c_feels": 12, "deg_c_min": 7},
            {"deg_c_feels": 13, "deg_c_min": 8},
            {"deg_c_feels": 14, "deg_c_min": 9},
            {"deg_c_feels": 15, "deg_c_min": 10},
            {"deg_c_feels": 16, "deg_c_min": 11}
        ]
        weather = MyJacketDecisionMaker(forecast)
        assert weather.decide_jacket() == JacketDecision.REGULAR_JACKET.value

    def test_decide_jacket_light_jacket(self):
        # Test case with light jacket weather
        forecast = [
            {"deg_c_feels": 17, "deg_c_min": 12},
            {"deg_c_feels": 18, "deg_c_min": 13},
            {"deg_c_feels": 19, "deg_c_min": 14},
            {"deg_c_feels": 20, "deg_c_min": 15},
            {"deg_c_feels": 21, "deg_c_min": 16}
        ]
        weather = MyJacketDecisionMaker(forecast)
        assert weather.decide_jacket() == JacketDecision.LIGHT_JACKET.value

    def test_decide_jacket_tshirt(self):
        # Test case with t-shirt weather
        forecast = [
            {"deg_c_feels": 22, "deg_c_min": 18},
            {"deg_c_feels": 23, "deg_c_min": 19},
            {"deg_c_feels": 24, "deg_c_min": 20},
            {"deg_c_feels": 25, "deg_c_min": 21},
            {"deg_c_feels": 26, "deg_c_min": 22}
        ]
        weather = MyJacketDecisionMaker(forecast)
        assert weather.decide_jacket() == JacketDecision.TSHIRT.value



class TestMyJacketDecisionMakerGloves:

    def test_decide_gloves_no_entries(self):
        forecast = []
        decision_maker = MyJacketDecisionMaker(forecast)
        with pytest.raises(ValueError, match="Forecast data must not be empty or None. It must contain at least one row."):
            decision_maker.decide_gloves()

    def test_decide_gloves_none_forecast(self):
        decision_maker = MyJacketDecisionMaker(None)
        with pytest.raises(ValueError, match="Forecast data must not be empty or None. It must contain at least one row."):
            decision_maker.decide_gloves()

    def test_decide_gloves_less_than_five_entries(self):
        forecast = [
            {"deg_c_feels": 5, "deg_c_min": 0},
            {"deg_c_feels": 7, "deg_c_min": 2}
        ]
        decision_maker = MyJacketDecisionMaker(forecast)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert decision_maker.decide_gloves() == GlovesDecision.YES.value
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "Forecast data contains 2 rows, but 5 rows are expected." in str(w[-1].message)

    def test_decide_gloves_very_cold(self):
        forecast = [
            {"deg_c_feels": 0, "deg_c_min": -5},
            {"deg_c_feels": 2, "deg_c_min": -3},
            {"deg_c_feels": 4, "deg_c_min": -2},
            {"deg_c_feels": 5, "deg_c_min": -1},
            {"deg_c_feels": 6, "deg_c_min": 0}
        ]
        decision_maker = MyJacketDecisionMaker(forecast)
        assert decision_maker.decide_gloves() == GlovesDecision.YES.value

    def test_decide_gloves_cold(self):
        forecast = [
            {"deg_c_feels": 6, "deg_c_min": 5},
            {"deg_c_feels": 7, "deg_c_min": 6},
            {"deg_c_feels": 8, "deg_c_min": 7},
            {"deg_c_feels": 9, "deg_c_min": 8},
            {"deg_c_feels": 10, "deg_c_min": 9}
        ]
        decision_maker = MyJacketDecisionMaker(forecast)
        assert decision_maker.decide_gloves() == GlovesDecision.YES.value

    def test_decide_gloves_warm(self):
        forecast = [
            {"deg_c_feels": 10, "deg_c_min": 8},
            {"deg_c_feels": 12, "deg_c_min": 9},
            {"deg_c_feels": 11, "deg_c_min": 10},
            {"deg_c_feels": 13, "deg_c_min": 11},
            {"deg_c_feels": 14, "deg_c_min": 12}
        ]
        decision_maker = MyJacketDecisionMaker(forecast)
        assert decision_maker.decide_gloves() == GlovesDecision.NO.value