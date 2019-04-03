""" bomweather - Load weather data from BOM website """


import logging
from logging import NullHandler
from bomweather.stations import get_obs_locations
from bomweather.stations import closest_obs_station
from bomweather.stations import get_forecast_locations
from bomweather.stations import closest_forecast_location
from bomweather.observations import ObservationSite, Observation
from bomweather.forecasts import Forecast, ForecastPeriod

__all__ = [
    "get_obs_locations",
    "closest_obs_station",
    "get_forecast_locations",
    "closest_forecast_location",
    "ObservationSite",
    "Observation",
    "Forecast",
    "ForecastPeriod",
]

# Set default logging handler to avoid "No handler found" warnings.
logging.getLogger(__name__).addHandler(NullHandler())
