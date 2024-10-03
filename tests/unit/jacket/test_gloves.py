import warnings

import pytest

from jacket.gloves import GlovesDecision, GlovesDecisionMaker


class TestGlovesDecisionMaker:

    def test_decide_gloves_no_entries(self):
        forecast = []
        decision_maker = GlovesDecisionMaker(forecast)
        with pytest.raises(ValueError, match="Forecast data must not be empty or None. It must contain at least one row."):
            decision_maker.decide_gloves()

    def test_decide_gloves_none_forecast(self):
        decision_maker = GlovesDecisionMaker(None)
        with pytest.raises(ValueError, match="Forecast data must not be empty or None. It must contain at least one row."):
            decision_maker.decide_gloves()

    def test_decide_gloves_less_than_five_entries(self):
        forecast = [
            {"deg_c_feels": 5, "deg_c_min": 0},
            {"deg_c_feels": 7, "deg_c_min": 2}
        ]
        decision_maker = GlovesDecisionMaker(forecast)
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
        decision_maker = GlovesDecisionMaker(forecast)
        assert decision_maker.decide_gloves() == GlovesDecision.YES.value

    def test_decide_gloves_cold(self):
        forecast = [
            {"deg_c_feels": 6, "deg_c_min": 5},
            {"deg_c_feels": 7, "deg_c_min": 6},
            {"deg_c_feels": 8, "deg_c_min": 7},
            {"deg_c_feels": 9, "deg_c_min": 8},
            {"deg_c_feels": 10, "deg_c_min": 9}
        ]
        decision_maker = GlovesDecisionMaker(forecast)
        assert decision_maker.decide_gloves() == GlovesDecision.YES.value

    def test_decide_gloves_warm(self):
        forecast = [
            {"deg_c_feels": 10, "deg_c_min": 8},
            {"deg_c_feels": 12, "deg_c_min": 9},
            {"deg_c_feels": 11, "deg_c_min": 10},
            {"deg_c_feels": 13, "deg_c_min": 11},
            {"deg_c_feels": 14, "deg_c_min": 12}
        ]
        decision_maker = GlovesDecisionMaker(forecast)
        assert decision_maker.decide_gloves() == GlovesDecision.NO.value