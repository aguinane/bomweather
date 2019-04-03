""" bomweather.stations

    Get list of stations
    Only sites with a World Meteorological Organisation (WMO) ID are considered

"""

import logging
import os
import re
import json
from math import cos, asin, sqrt
from typing import NamedTuple
from typing import Tuple, Optional, Iterator, List, Dict
from pathlib import Path
import requests

from bomweather.scrape_products import get_obs_products
from bomweather.scrape_products import get_forecast_products
from bomweather.scrape_stations import get_station_list


class Station(NamedTuple):
    """ Weather Observations """

    site: str
    site_name: str
    lat: float
    lon: float
    state: str
    wmo: str
    obs_product: str


def get_obs_locations(rescrape=False) -> Dict[str, Station]:
    """ Get list of observation locations

        :param rescrape: Should it re-download station list from web
    """

    data = {}
    stations = get_obs_stations(rescrape)
    for station in stations:
        data[station.wmo] = station
    return data


def get_obs_stations(rescrape: bool = False) -> Iterator[Station]:
    """ Parse stations.txt file """

    products = get_obs_products(rescrape)
    station_list = get_station_list(rescrape)
    for i, line in enumerate(station_list):
        if i < 4:
            continue  # Skip headers
        if type(line) == str:
            row = line.strip()
        else:
            row = line.decode().strip()
        if len(row) < 20:
            # Empty line means we are at the footer
            break

        wmo = row[128:135].strip()
        # If no WMO then skip station
        if ".." in wmo:
            wmo = None
            continue

        site_id = row[0:6]
        site_name = row[12:55].strip()
        lat = float(row[70:78])
        lon = float(row[79:88])
        state = row[104:108].strip()

        if wmo not in products.keys():
            continue
        obs_product = products[wmo]

        yield Station(site_id, site_name, lat, lon, state, wmo, obs_product)


def closest_obs_station(lat: float, lon: float, rescrape: bool = False):
    """ Get the closest station for a location

    :param lat: Latitude
    :param lon: Longitude
    :param rescrape: Should it re-download station list from web
    """

    stations = get_obs_locations(rescrape)
    closest_wmo = min(
        stations,
        key=lambda wmo: geo_distance(
            lat, lon, stations[wmo].lat, stations[wmo].lon
        ),
    )
    return stations[closest_wmo]


def closest_forecast_location(lat: float, lon: float, rescrape: bool = False):
    """ Get the closest station for a location

    :param lat: Latitude
    :param lon: Longitude
    :param rescrape: Should it re-download station list from web
    """

    stations = get_forecast_locations(rescrape)
    closest_product = min(
        stations,
        key=lambda product: geo_distance(
            lat, lon, stations[product].lat, stations[product].lon
        ),
    )
    return stations[closest_product]


class ForecastStation(NamedTuple):
    """ Weather Observations """

    site_name: str
    product: str
    lat: float
    lon: float
    state: str


def get_forecast_locations(rescrape: bool = False) -> Dict[str, ForecastStation]:
    """ Get list of forecast locations

        :param rescrape: Should it re-download station list from web
    """

    data = {}
    products = get_forecast_products(rescrape)
    stations = get_obs_locations(rescrape)
    for town in products.keys():
        product = products[town][0]
        state = products[town][1]
        station = match_forecast_to_station(state, town, stations)
        if station:
            data[product] = ForecastStation(town, product,station.lat,station.lon,state)
    return data


def match_forecast_to_station(
    state: str, town: str, stations: Dict[str, Station]
) -> Optional[Station]:

    town_name = town.split("-", 1)[0]
    for wmo in stations.keys():
        if not stations[wmo].lat:
            continue
        st_state = stations[wmo].state.lower()
        st_name = stations[wmo].site_name.lower()
        if state == st_state:
            if town_name in st_name:
                return stations[wmo]
    return None


def geo_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """ Get distance between points
    Formula from https://stackoverflow.com/a/41337005
    """
    p = 0.017_453_292_519_943_295
    a = (
        0.5
        - cos((lat2 - lat1) * p) / 2
        + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    )
    return 12742 * asin(sqrt(a))



