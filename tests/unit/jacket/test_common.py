import warnings

import pytest

from jacket.common import ForecastUtils


class TestForecastUtils:

    def test_calculate_avg_feels_temperature(self):
        # Test case with multiple entries
        forecast = [
            {"deg_c_feels": 12, "deg_c_min": 11.27},
            {"deg_c_feels": 13, "deg_c_min": 11.28},
            {"deg_c_feels": 11, "deg_c_min": 11.65},
            {"deg_c_feels": 8, "deg_c_min": 10},
            {"deg_c_feels": 6.67, "deg_c_min": 8},
        ]
        assert ForecastUtils.calculate_avg_feels_temperature(forecast) == 10.1

    def test_calculate_avg_feels_temperature_with_one_entry(self):
        # Test case with a single entry
        forecast = [{"deg_c_feels": 10, "deg_c_min": 5}]
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            assert ForecastUtils.calculate_avg_feels_temperature(forecast) == 10.0
            assert len(w) == 0

    def test_calculate_avg_feels_temperature_with_no_entry(self):
        # Test case with no entries
        forecast = []
        with pytest.raises(ValueError):
            ForecastUtils.calculate_avg_feels_temperature(forecast)

    def test_calculate_avg_feels_temperature_with_negative_temps(self):
        # Test case with negative temperatures
        forecast = [
            {"deg_c_feels": -5, "deg_c_min": -10},
            {"deg_c_feels": -10, "deg_c_min": -10},
            {"deg_c_feels": -10, "deg_c_min": -10},
            {"deg_c_feels": -10, "deg_c_min": -10},
            {"deg_c_feels": -15, "deg_c_min": -20},
        ]
        assert ForecastUtils.calculate_avg_feels_temperature(forecast) == -10.0
