import warnings

import pytest

from jacket.jacket import JacketDecision, JacketDecisionMaker
from jacket.rain_jacket import RainJacketDecision, RainJacketDecisionMaker


class TestJacketDecisionMakerFromTemp:

    def test_decide_jacket_from_temp_no_entries(self):
        forecast = []
        jdm = JacketDecisionMaker(forecast)
        with pytest.raises(
            ValueError,
            match="Forecast data must not be empty or None. It must contain at least one row.",
        ):
            jdm.decide_jacket_from_temp()

    def test_decide_jacket_from_temp_none_forecast(self):
        # Test case with None forecast
        jdm = JacketDecisionMaker(None)
        with pytest.raises(
            ValueError,
            match="Forecast data must not be empty or None. It must contain at least one row.",
        ):
            jdm.decide_jacket_from_temp()

    def test_decide_jacket_from_temp_less_than_five_entries(self):
        # Test case with less than 5 entries
        forecast = [
            {"deg_c_feels": 5, "deg_c_min": 0},
            {"deg_c_feels": 7, "deg_c_min": 2},
        ]
        jdm = JacketDecisionMaker(forecast)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert (
                jdm.decide_jacket_from_temp()
                == JacketDecision.REGULAR_JACKET_w_LAYERS.value
            )
            assert len(w) == 1
            assert issubclass(w[-1].category, UserWarning)
            assert "Forecast data contains 2 rows, but 5 rows are expected." in str(
                w[-1].message
            )

    def test_decide_jacket_from_temp_cold_weather(self):
        # Test case with cold weather
        forecast = [
            {"deg_c_feels": 0, "deg_c_min": -5},
            {"deg_c_feels": -2, "deg_c_min": -3},
            {"deg_c_feels": -4, "deg_c_min": -2},
            {"deg_c_feels": 1, "deg_c_min": -1},
            {"deg_c_feels": 1, "deg_c_min": 0},
        ]
        jdm = JacketDecisionMaker(forecast)
        assert jdm.decide_jacket_from_temp() == JacketDecision.WARM_JACKET.value

    def test_decide_jacket_from_temp_regular_jacket_with_layers(self):
        # Test case with regular jacket with layers weather
        forecast = [
            {"deg_c_feels": 7, "deg_c_min": 2},
            {"deg_c_feels": 8, "deg_c_min": 3},
            {"deg_c_feels": 9, "deg_c_min": 4},
            {"deg_c_feels": 10, "deg_c_min": 5},
            {"deg_c_feels": 11, "deg_c_min": 6},
        ]
        jdm = JacketDecisionMaker(forecast)
        assert jdm.decide_jacket_from_temp() == JacketDecision.REGULAR_JACKET.value

    def test_decide_jacket_from_temp_regular_jacket(self):
        # Test case with regular jacket weather
        forecast = [
            {"deg_c_feels": 12, "deg_c_min": 7},
            {"deg_c_feels": 13, "deg_c_min": 8},
            {"deg_c_feels": 14, "deg_c_min": 9},
            {"deg_c_feels": 15, "deg_c_min": 10},
            {"deg_c_feels": 16, "deg_c_min": 11},
        ]
        jdm = JacketDecisionMaker(forecast)
        assert jdm.decide_jacket_from_temp() == JacketDecision.REGULAR_JACKET.value

    def test_decide_jacket_from_temp_light_jacket(self):
        # Test case with light jacket weather
        forecast = [
            {"deg_c_feels": 17, "deg_c_min": 12},
            {"deg_c_feels": 18, "deg_c_min": 13},
            {"deg_c_feels": 19, "deg_c_min": 14},
            {"deg_c_feels": 20, "deg_c_min": 15},
            {"deg_c_feels": 21, "deg_c_min": 16},
        ]
        jdm = JacketDecisionMaker(forecast)
        assert jdm.decide_jacket_from_temp() == JacketDecision.LIGHT_JACKET.value

    def test_decide_jacket_from_temp_tshirt(self):
        # Test case with t-shirt weather
        forecast = [
            {"deg_c_feels": 22, "deg_c_min": 18},
            {"deg_c_feels": 23, "deg_c_min": 19},
            {"deg_c_feels": 24, "deg_c_min": 20},
            {"deg_c_feels": 25, "deg_c_min": 21},
            {"deg_c_feels": 26, "deg_c_min": 22},
        ]
        jdm = JacketDecisionMaker(forecast)
        assert jdm.decide_jacket_from_temp() == JacketDecision.TSHIRT.value


class TestJacketDecisionMaker:

    def test_decide_jacket_no_entries(self):
        forecast = []
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        with pytest.raises(
            ValueError,
            match="Forecast data must not be empty or None. It must contain at least one row.",
        ):
            jdm.decide_jacket()

    def test_decide_jacket_from_temp_none_forecast(self):
        # Test case with None forecast
        rdm = RainJacketDecisionMaker(None)
        jdm = JacketDecisionMaker(None, rdm)
        with pytest.raises(
            ValueError,
            match="Forecast data must not be empty or None. It must contain at least one row.",
        ):
            jdm.decide_jacket()

    def test_decide_jacket_less_than_five_entries_rain(self):
        # Test case with less than 5 entries
        forecast = [
            {"deg_c_feels": 5, "deg_c_min": 0, "rain": "None"},
            {"deg_c_feels": 7, "deg_c_min": 2, "rain": "High"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert (
                jdm.decide_jacket() == JacketDecision.REGULAR_RAIN_JACKET_w_LAYERS.value
            )
            assert len(w) == 1  # only have 1 warning not many
            assert issubclass(w[-1].category, UserWarning)
            assert "Forecast data contains 2 rows, but 5 rows are expected." in str(
                w[-1].message
            )

    def test_decide_jacket_less_than_five_entries_no_rain(self):
        # Test case with less than 5 entries
        forecast = [
            {"deg_c_feels": 5, "deg_c_min": 0, "rain": "None"},
            {"deg_c_feels": 7, "deg_c_min": 2, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert jdm.decide_jacket() == JacketDecision.REGULAR_JACKET_w_LAYERS.value
            assert len(w) == 1  # only have 1 warning not many
            assert issubclass(w[-1].category, UserWarning)
            assert "Forecast data contains 2 rows, but 5 rows are expected." in str(
                w[-1].message
            )

    # WARM JACKET

    def test_decide_jacket_cold_weather_rain(self):
        # Test case with cold weather
        forecast = [
            {"deg_c_feels": 0, "deg_c_min": -5, "rain": "Medium"},
            {"deg_c_feels": 2, "deg_c_min": -3, "rain": "None"},
            {"deg_c_feels": 4, "deg_c_min": -2, "rain": "None"},
            {"deg_c_feels": 5, "deg_c_min": -1, "rain": "None"},
            {"deg_c_feels": -5, "deg_c_min": -8, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        assert jdm.decide_jacket() == JacketDecision.WARM_RAIN_JACKET.value

    def test_decide_jacket_cold_weather_no_rain(self):
        # Test case with cold weather
        forecast = [
            {"deg_c_feels": 0, "deg_c_min": -5, "rain": "None"},
            {"deg_c_feels": 2, "deg_c_min": -3, "rain": "None"},
            {"deg_c_feels": 4, "deg_c_min": -2, "rain": "None"},
            {"deg_c_feels": 5, "deg_c_min": -1, "rain": "None"},
            {"deg_c_feels": -5, "deg_c_min": -8, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        assert jdm.decide_jacket() == JacketDecision.WARM_JACKET.value

    # REGULAR JACKET WITH LAYERS

    def test_decide_jacket_regular_jacket_with_layers_no_rain(self):
        # Test case with regular jacket with layers weather
        forecast = [
            {"deg_c_feels": 7, "deg_c_min": 2, "rain": "None"},
            {"deg_c_feels": 8, "deg_c_min": 3, "rain": "None"},
            {"deg_c_feels": 4, "deg_c_min": 4, "rain": "None"},
            {"deg_c_feels": 2, "deg_c_min": 5, "rain": "None"},
            {"deg_c_feels": 3, "deg_c_min": 6, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        assert jdm.decide_jacket() == JacketDecision.REGULAR_JACKET_w_LAYERS.value

    def test_decide_jacket_regular_jacket_with_layers_rain(self):
        # Test case with regular jacket with layers weather
        forecast = [
            {"deg_c_feels": 7, "deg_c_min": 2, "rain": "None"},
            {"deg_c_feels": 8, "deg_c_min": 3, "rain": "Medium"},
            {"deg_c_feels": 9, "deg_c_min": 4, "rain": "None"},
            {"deg_c_feels": 10, "deg_c_min": 5, "rain": "None"},
            {"deg_c_feels": 11, "deg_c_min": 6, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        assert jdm.decide_jacket() == JacketDecision.REGULAR_RAIN_JACKET.value

    # REGULAR JACKET

    def test_decide_jacket_regular_jacket_no_rain(self):
        # Test case with regular jacket with layers weather
        forecast = [
            {"deg_c_feels": 12, "deg_c_min": 11, "rain": "None"},
            {"deg_c_feels": 13, "deg_c_min": 12, "rain": "None"},
            {"deg_c_feels": 14, "deg_c_min": 13, "rain": "None"},
            {"deg_c_feels": 15, "deg_c_min": 14, "rain": "None"},
            {"deg_c_feels": 16, "deg_c_min": 15, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        assert jdm.decide_jacket() == JacketDecision.REGULAR_JACKET.value

    def test_decide_jacket_regular_jacket_rain(self):
        # Test case with regular jacket with layers weather
        forecast = [
            {"deg_c_feels": 12, "deg_c_min": 11, "rain": "None"},
            {"deg_c_feels": 13, "deg_c_min": 12, "rain": "Medium"},
            {"deg_c_feels": 14, "deg_c_min": 13, "rain": "None"},
            {"deg_c_feels": 15, "deg_c_min": 14, "rain": "None"},
            {"deg_c_feels": 16, "deg_c_min": 15, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        assert jdm.decide_jacket() == JacketDecision.REGULAR_RAIN_JACKET.value

    # LIGHT JACKET

    def test_decide_jacket_light_jacket_no_rain(self):
        # Test case with regular jacket with layers weather
        forecast = [
            {"deg_c_feels": 17, "deg_c_min": 12, "rain": "None"},
            {"deg_c_feels": 18, "deg_c_min": 13, "rain": "None"},
            {"deg_c_feels": 19, "deg_c_min": 13, "rain": "None"},
            {"deg_c_feels": 20, "deg_c_min": 14, "rain": "None"},
            {"deg_c_feels": 21, "deg_c_min": 17, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        assert jdm.decide_jacket() == JacketDecision.LIGHT_JACKET.value

    def test_decide_jacket_light_jacket_rain(self):
        # Test case with regular jacket with layers weather
        forecast = [
            {"deg_c_feels": 17, "deg_c_min": 12, "rain": "None"},
            {"deg_c_feels": 18, "deg_c_min": 13, "rain": "Low"},
            {"deg_c_feels": 19, "deg_c_min": 13, "rain": "Medium"},
            {"deg_c_feels": 20, "deg_c_min": 14, "rain": "None"},
            {"deg_c_feels": 21, "deg_c_min": 17, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        assert jdm.decide_jacket() == JacketDecision.REGULAR_RAIN_JACKET.value

    # TSHIRT NO JACKET

    def test_decide_no_jacket_no_rain(self):
        # Test case with regular jacket with layers weather
        forecast = [
            {"deg_c_feels": 21, "deg_c_min": 18, "rain": "None"},
            {"deg_c_feels": 22, "deg_c_min": 19, "rain": "None"},
            {"deg_c_feels": 23, "deg_c_min": 22, "rain": "None"},
            {"deg_c_feels": 24, "deg_c_min": 22, "rain": "None"},
            {"deg_c_feels": 25, "deg_c_min": 23, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        assert jdm.decide_jacket() == JacketDecision.TSHIRT.value

    def test_decide_no_jacket_rain(self):
        # Test case with regular jacket with layers weather
        forecast = [
            {"deg_c_feels": 21, "deg_c_min": 18, "rain": "None"},
            {"deg_c_feels": 22, "deg_c_min": 19, "rain": "Low"},
            {"deg_c_feels": 23, "deg_c_min": 22, "rain": "Low"},
            {"deg_c_feels": 24, "deg_c_min": 22, "rain": "Low"},
            {"deg_c_feels": 25, "deg_c_min": 23, "rain": "Medium"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        jdm = JacketDecisionMaker(forecast, rdm)
        assert jdm.decide_jacket() == JacketDecision.REGULAR_RAIN_JACKET.value

    # Test optional rain

    def test_decide_light_jacket_optional_rain(self):
        # Test case with light jacket weather and optional rain
        forecast = [
            {"deg_c_feels": 17, "deg_c_min": 12, "rain": "None"},
            {"deg_c_feels": 18, "deg_c_min": 13, "rain": "Low"},
            {"deg_c_feels": 19, "deg_c_min": 14, "rain": "Low"},
            {"deg_c_feels": 20, "deg_c_min": 15, "rain": "None"},
            {"deg_c_feels": 21, "deg_c_min": 16, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        assert rdm.decide_rain_jacket() == RainJacketDecision.OPTIONAL.value
        jdm = JacketDecisionMaker(forecast, rdm)
        assert jdm.decide_jacket() == JacketDecision.REGULAR_RAIN_JACKET.value

    def test_decide_tshirt_optional_rain(self):
        # Test case with t-shirt weather and optional rain
        forecast = [
            {"deg_c_feels": 21, "deg_c_min": 18, "rain": "None"},
            {"deg_c_feels": 22, "deg_c_min": 19, "rain": "None"},
            {"deg_c_feels": 23, "deg_c_min": 22, "rain": "Low"},
            {"deg_c_feels": 24, "deg_c_min": 22, "rain": "Low"},
            {"deg_c_feels": 25, "deg_c_min": 23, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        assert rdm.decide_rain_jacket() == RainJacketDecision.OPTIONAL.value
        jdm = JacketDecisionMaker(forecast, rdm)
        assert jdm.decide_jacket() == JacketDecision.REGULAR_RAIN_JACKET.value

    def test_decide_regular_jacket_optional_rain(self):
        # Test case with regular jacket weather and optional rain
        forecast = [
            {"deg_c_feels": 12, "deg_c_min": 7, "rain": "None"},
            {"deg_c_feels": 13, "deg_c_min": 8, "rain": "Low"},
            {"deg_c_feels": 14, "deg_c_min": 9, "rain": "Low"},
            {"deg_c_feels": 15, "deg_c_min": 10, "rain": "None"},
            {"deg_c_feels": 16, "deg_c_min": 11, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        assert rdm.decide_rain_jacket() == RainJacketDecision.OPTIONAL.value
        jdm = JacketDecisionMaker(forecast, rdm)
        assert (
            jdm.decide_jacket() == JacketDecision.REGULAR_JACKET.value
        )  # does not change

    def test_decide_warm_jacket_optional_rain(self):
        # Test case with warm jacket weather and optional rain
        forecast = [
            {"deg_c_feels": -5, "deg_c_min": 0, "rain": "None"},
            {"deg_c_feels": -4, "deg_c_min": -1, "rain": "Low"},
            {"deg_c_feels": -3, "deg_c_min": -2, "rain": "None"},
            {"deg_c_feels": 2, "deg_c_min": -3, "rain": "Low"},
            {"deg_c_feels": 1, "deg_c_min": -4, "rain": "None"},
        ]
        rdm = RainJacketDecisionMaker(forecast)
        assert rdm.decide_rain_jacket() == RainJacketDecision.OPTIONAL.value
        jdm = JacketDecisionMaker(forecast, rdm)
        assert (
            jdm.decide_jacket() == JacketDecision.WARM_JACKET.value
        )  # does not change
