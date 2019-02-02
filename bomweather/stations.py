""" bomweather.stations

    Scrape the BOM website to get a list of stations with weather observations
    http://www.bom.gov.au/catalogue/observations/about-weather-observations.shtml

    To get the station location, they are compared against this metedata table:
    ftp://ftp.bom.gov.au/anon2/home/ncc/metadata/sitelists/

    Only sites with a World Meteorological Organisation (WMO) ID are considered

"""

import logging
import os
import ftplib
import zipfile
import re
import json
import io
from math import cos, asin, sqrt
from typing import NamedTuple
from typing import Tuple
from pathlib import Path
import requests

STATES = ["ant", "nsw", "nt", "qld", "tas", "vic", "wa"]

thisdir = Path(os.path.dirname(os.path.abspath(__file__)))
OBS_STN_LOOKUP = thisdir / "obs_stations.json"


def get_obs_locations(web_lookup=False) -> dict:
    """ Get list of observation locations

        :param web_lookup: Should it re-download station list from web
    """

    if OBS_STN_LOOKUP.is_file() and not web_lookup:
        # Load existing station list
        with open(OBS_STN_LOOKUP, "r") as fp:
            return json.load(fp)

    logging.info("Downloading BOM Station Data")
    data = {}
    products = get_product_list()
    stations = parse_station_list()
    for wmo in products:
        if wmo in stations.keys():
            station = stations[wmo]
            data[wmo] = {
                "wmo": wmo,
                "product": products[wmo],
                "lat": station.lat,
                "lon": station.lon,
                "state": station.state,
                "site_name": station.site_name,
            }
    return data


def closest_obs_station(lat: float, lon: float, web_lookup: bool = False):
    """ Get the closest station for a location

    :param lat: Latitude
    :param lon: Longitude
    :param web_lookup: Should it re-download station list from web
    """

    def geo_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """ Get distance between points
        Formulala from https://stackoverflow.com/a/41337005
        """
        p = 0.017_453_292_519_943_295
        a = (
            0.5
            - cos((lat2 - lat1) * p) / 2
            + cos(lat1 * p) * cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
        )
        return 12742 * asin(sqrt(a))

    stations = get_obs_locations(web_lookup)
    closest_wmo = min(
        stations,
        key=lambda wmo: geo_distance(
            lat, lon, stations[wmo]["lat"], stations[wmo]["lon"]
        ),
    )
    return stations[closest_wmo]


def get_product_list():
    """ Get list of history product IDs for WMOs
        by scraping state overivew pages
    """
    products = dict()
    pattern = (
        r'<a href="/products/(?P<product>ID[A-Z]\d\d\d\d\d)/'
        r'(?P=product)\.(?P<wmo>\d\d\d\d\d).shtml">'
    )

    for state in STATES:
        url = f"http://www.bom.gov.au/{state}/observations/{state}all.shtml"
        r = requests.get(url, timeout=10)
        for product, wmo in re.findall(pattern, r.text):
            wmo = int(wmo)
            products[wmo] = product

    return products


class Station(NamedTuple):
    """ Weather Observations """

    site: str
    site_name: str
    lat: float
    lon: float
    state: str
    wmo: int


def download_station_list():
    """ Download list of observation station metadata from
        Bureau of Meteorology FTP service
    """
    host = "ftp.bom.gov.au"
    folder = "anon2/home/ncc/metadata/sitelists"
    filename = "stations.zip"

    output = []
    with io.BytesIO() as fp:
        with ftplib.FTP(host) as ftp:
            ftp.login()
            ftp.cwd(folder)
            ftp.retrbinary(f"RETR {filename}", fp.write)
            fp.seek(0)  # Return to start of file
            with zipfile.ZipFile(fp) as archive:
                with archive.open("stations.txt") as txt_file:
                    for line in txt_file:
                        output.append(line)
    return output


def parse_station_list():
    """ Parse stations.txt file """
    stations = {}
    txt_file = download_station_list()
    for i, line in enumerate(txt_file):
        if i < 4:
            continue  # Skip headers
        row = line.decode().strip()
        if len(row) < 20:
            # Empty line means we are at the footer
            break

        wmo = row[128:135]
        # If no WMO then skip station
        if ".." in wmo:
            continue
        else:
            wmo = int(wmo)

        site_id = row[0:6]
        site_name = row[12:55].strip()
        lat = float(row[70:78])
        lon = float(row[79:88])
        state = row[104:108].strip()

        stations[wmo] = Station(site_id, site_name, lat, lon, state, wmo)
    return stations


if __name__ == "__main__":

    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logger = logging.getLogger()  # Root Logger
    logging.basicConfig(level="INFO", format=LOG_FORMAT)

    # Update the obs_stations.json file
    logging.info("Updating obs_stations.json")
    data = get_obs_locations(web_lookup=True)
    with open(OBS_STN_LOOKUP, "w") as fp:
        json.dump(data, fp, indent=4, sort_keys=True)
