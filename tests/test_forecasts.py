import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bomweather import Forecast


def test_getting_metro_forecasts():
    """ Test forecasts seem reasonable for example site """

    f = Forecast("IDQ10095")
    assert f.desc == "Brisbane"
    last_forecast = f.forecasts[-1]
    assert -10.0 < float(last_forecast.temp_max) < 50
    assert -10.0 < float(last_forecast.temp_min) < 50

    f = Forecast("IDV10450")
    assert f.desc == "Melbourne"
    last_forecast = f.forecasts[-1]
    assert -10.0 < float(last_forecast.temp_max) < 50
    assert -10.0 < float(last_forecast.temp_min) < 50


def test_getting_regional_forecasts():
    """ Test forecasts seem reasonable for example site """

    f = Forecast("IDV10706")
    assert f.desc == "Bendigo"
    last_forecast = f.forecasts[-1]
    assert -10.0 < float(last_forecast.temp_max) < 50
    assert -10.0 < float(last_forecast.temp_min) < 50

    f = Forecast("IDQ10170", "Yeppoon")
    assert f.desc == "Yeppoon"
    last_forecast = f.forecasts[-1]
    assert -10.0 < float(last_forecast.temp_max) < 50
    assert -10.0 < float(last_forecast.temp_min) < 50
