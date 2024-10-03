import pytest
import requests
from integrations.openweathermap import OpenWeatherMapApi

def test_api_key_loaded():
    api = OpenWeatherMapApi()
    assert api.api_key is not None, "API key should be loaded from environment variables"

def test_get_forecast_by_city():
    api = OpenWeatherMapApi()
    city = "London"
    data = api.get_forecast_by_city(city)
    
    assert data is not None, "Data should not be None"
    assert "list" in data, "Response should contain 'list' key"
    assert len(data["list"]) > 0, "Forecast list should not be empty"

def test_get_forecast_by_invalid_city():
    api = OpenWeatherMapApi()
    city = "InvalidCityName"
    
    with pytest.raises(requests.exceptions.HTTPError):
        api.get_forecast_by_city(city)

if __name__ == "__main__":
    pytest.main()
