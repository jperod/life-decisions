from datetime import datetime

from jacket.rain_jacket import RainJacketDecision, RainJacketDecisionMaker


class TestRainJacketDecisionMaker:
    """Test Rain Jacket Decision Maker"""

    def test_no_rain(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 8, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 11, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"}
        ]
        decision_maker = RainJacketDecisionMaker(forecast)
        assert decision_maker.decide_rain_jacket() == RainJacketDecision.NO.value

    def test_high_intensity_rain(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 8, 0), "rain": "High"},
            {"datetime_cph": datetime(2024, 10, 2, 11, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"}
        ]
        decision_maker = RainJacketDecisionMaker(forecast)
        assert decision_maker.decide_rain_jacket() == RainJacketDecision.YES.value

    def test_medium_intensity_rain(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 8, 0), "rain": "Medium"},
            {"datetime_cph": datetime(2024, 10, 2, 11, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"}
        ]
        decision_maker = RainJacketDecisionMaker(forecast)
        assert decision_maker.decide_rain_jacket() == RainJacketDecision.YES.value

    def test_low_intensity_rain_consistent(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 8, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 11, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "Low"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "Low"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "Low"}
        ]
        decision_maker = RainJacketDecisionMaker(forecast)
        assert decision_maker.decide_rain_jacket() == RainJacketDecision.YES.value

    def test_low_intensity_rain_optional(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "Low"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"}
        ]
        decision_maker = RainJacketDecisionMaker(forecast)
        assert decision_maker.decide_rain_jacket() == RainJacketDecision.OPTIONAL.value

    def test_mixed_rain(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "Low"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "Medium"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "High"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"}
        ]
        decision_maker = RainJacketDecisionMaker(forecast)
        assert decision_maker.decide_rain_jacket() == RainJacketDecision.YES.value

    def test_realistic_forecast(self):
        forecast = [
            {"datetime_cph": datetime(2024, 10, 2, 14, 0), "rain": "Low"},
            {"datetime_cph": datetime(2024, 10, 2, 17, 0), "rain": "Low"},
            {"datetime_cph": datetime(2024, 10, 2, 20, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 2, 23, 0), "rain": "None"},
            {"datetime_cph": datetime(2024, 10, 3, 2, 0), "rain": "None"}
        ]
        decision_maker = RainJacketDecisionMaker(forecast)
        assert decision_maker.decide_rain_jacket() == RainJacketDecision.OPTIONAL.value
