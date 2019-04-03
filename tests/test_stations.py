import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bomweather import closest_obs_station
from bomweather import closest_forecast_location


def test_closest_obs_station_cached():
    """ Test some example locations and check against expected names """

    st = closest_obs_station(-33.865143, 151.209900)
    assert "SYDNEY" in st.site_name

    st = closest_obs_station(-37.814, 144.96332)
    assert "MELBOURNE" in st.site_name

    st = closest_obs_station(-27.470125, 153.021072)
    assert "BRISBANE" in st.site_name


def test_closest_obs_station_uncached():
    """ Test some example locations and check against expected names """

    st = closest_obs_station(-27.470125, 153.021072, rescrape=True)
    assert "BRISBANE" in st.site_name


def test_closest_forecast_station_cached():
    """ Test some example locations and check against expected names """

    st = closest_forecast_location(-33.865143, 151.209900)
    assert "SYDNEY" in st.site_name.upper()

    st = closest_forecast_location(-27.470125, 153.021072)
    assert "REDCLIFFE" in st.site_name.upper()  # Brisbane

    st = closest_forecast_location(-23.133333, 150.733333)
    assert "YEPPOON" in st.site_name.upper()
