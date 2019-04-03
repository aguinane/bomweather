""" bomweather.scrape_stations

    Scrape the BOM website to get a list of stations

"""

import logging
import os
import io
import ftplib
import zipfile
from typing import Iterator
from pathlib import Path

thisdir = Path(os.path.dirname(os.path.abspath(__file__)))
STN_LIST = thisdir / 'data' / "stations.txt"
log = logging.getLogger(__name__)


def get_station_list(rescrape=False):
    """ Get list of history product IDs for WMOs from local cached file
    """
    if STN_LIST.is_file() and not rescrape:
        with open(STN_LIST, "rb") as fp:
            return fp.readlines()
    return scrape_station_list()


def scrape_station_list() -> list:
    """ Download list of observation station metadata from
        Bureau of Meteorology FTP service
    """

    log.debug("Downloading BOM Station Data")
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
                        output.append(line.decode())
    return output


if __name__ == "__main__":

    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    logger = logging.getLogger()  # Root Logger
    logging.basicConfig(level="DEBUG", format=LOG_FORMAT)

    # Update the stations.txt file
    logging.info("Updating stations.txt")
    data = scrape_station_list()
    with open(STN_LIST, "w") as fp:
        fp.writelines(data)
