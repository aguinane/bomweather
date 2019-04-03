""" bomweather.scrape_products

    Scrape the BOM website to get a list of products ids

"""

import logging
import os
import re
import json
import io
from typing import Optional, Dict, Tuple
from pathlib import Path
import requests

thisdir = Path(os.path.dirname(os.path.abspath(__file__)))
OBS_LOOKUP = thisdir / 'data' / "products_obs.json"
FCST_LOOKUP = thisdir / 'data' / "products_forecast.json"
STATES = ["ant", "nsw", "nt", "qld", "tas", "vic", "wa"]


def get_obs_products(rescrape=False) -> Dict[str, str]:
    """ Get list of history product IDs for WMOs
        from local cached file
    """

    if OBS_LOOKUP.is_file() and not rescrape:
        with open(OBS_LOOKUP, "r") as fp:
            return json.load(fp)
    return scrape_obs_products()


def scrape_obs_products() -> Dict[str, str]:
    """ Get list of history product IDs for WMOs
        by scraping state overview pages
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
            products[wmo] = product
    return products


def get_forecast_products(rescrape=False) -> Dict[str, Tuple[str, str]]:
    """ Get list of forecast products from local cached file
    """

    if FCST_LOOKUP.is_file() and not rescrape:
        with open(FCST_LOOKUP, "r") as fp:
            return json.load(fp)
    return scrape_forecast_products()


def scrape_forecast_products() -> Dict[str, Tuple[str, str]]:
    """ Get list of forecast products by scraping state overivew pages
    """

    logging.info("Scraping list of BOM forecast products")
    products = dict()
    for state in STATES:
        url = f"http://www.bom.gov.au/{state}/forecasts/precis.shtml"
        r = requests.get(url, timeout=10)
        pattern = r'/forecasts/(?P<town>.+?).shtml">Detailed'
        for town in re.findall(pattern, r.text):
            product = get_town_forecast_product_id(state, town)
            if product:
                products[town] = (product, state)
    return products


def get_town_forecast_product_id(state: str, town: str) -> Optional[str]:
    """ Get the product ID from page """
    url = f"http://www.bom.gov.au/{state}/forecasts/{town}.shtml"
    r = requests.get(url, timeout=10)
    pattern = r"Product (ID[A-Z]\d{5})"
    try:
        product = re.findall(pattern, r.text)[0]
    except IndexError:
        pattern2 = r"Product derived from (ID[A-Z]\d{5}) and (ID[A-Z]\d{5})"
        try:
            products = re.findall(pattern2, r.text)[0]
            product = products[-1]
        except IndexError:
            return None
    return product


if __name__ == "__main__":

    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logger = logging.getLogger()  # Root Logger
    logging.basicConfig(level="INFO", format=LOG_FORMAT)

    # Update the obs_stations.json file
    logging.info("Updating products_obs.json")
    obs_data = scrape_obs_products()
    with open(OBS_LOOKUP, "w") as fp:
        json.dump(obs_data, fp, indent=4, sort_keys=True)

    # Update the forecast_stations.json file
    logging.info("Updating products_forecast.json")
    fc_data = scrape_forecast_products()
    with open(FCST_LOOKUP, "w") as fp:
        json.dump(fc_data, fp, indent=4, sort_keys=True)
