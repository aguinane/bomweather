import os
import sys
sys.path.insert(0,
                os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from bomweather import closest_obs_station


def test_closest_station():
    """ Test some example locations and check against expected names """

    st = closest_obs_station(-33.865143, 151.209900)
    assert 'SYDNEY' in st['site_name']

    st = closest_obs_station(-37.814, 144.96332)
    assert 'MELBOURNE' in st['site_name']

    st = closest_obs_station(-27.470125, 153.021072)
    assert 'BRISBANE' in st['site_name']
