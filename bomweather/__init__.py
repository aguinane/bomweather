""" bomweather - Load weather data from BOM website """

from bomweather.stations import get_obs_locations
from bomweather.stations import closest_obs_station

__all__ = ['get_obs_locations', 'closest_station']
