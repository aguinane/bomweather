import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from bomweather import ObservationSite

COMPASS_PNTS = [
    "N",
    "NNE",
    "NE",
    "ENE",
    "E",
    "ESE",
    "SE",
    "SSE",
    "S",
    "SSW",
    "SW",
    "WSW",
    "W",
    "WNW",
    "NW",
    "NNW",
]


def test_latest_observation():
    """ Test observations seem reasonable for example site """

    obs = ObservationSite(95551, "IDQ60801")
    last_obs = obs.last_observation()

    assert -10.0 < last_obs.air_temp < 50
    assert 970 < last_obs.press < 1030
    assert last_obs.wind_dir in COMPASS_PNTS
