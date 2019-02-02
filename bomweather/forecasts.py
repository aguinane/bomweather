import logging
import ftplib
import io
from typing import NamedTuple
from typing import Optional
from datetime import datetime
import ftplib
import requests
import pytz
from xml.etree import ElementTree
from dateutil.parser import parse

# https://github.com/home-assistant/home-assistant/pull/17351/files


class ForecastPeriod(NamedTuple):
    """ Weather Forecast """

    start: datetime
    end: datetime
    forecast_icon: str
    forecast_text: str
    temp_max: str
    temp_min: str
    precis: str
    precis_prob: str
    precis_range: str


class Forecast:
    """ BOM Weather Forecast

        List of locations (NSW Example):
        http://www.bom.gov.au/nsw/forecasts/map7day.shtml

        Forecast xml data comes from:
        ftp://ftp.bom.gov.au/anon/gen/fwo/

    """

    def __init__(self, product: str, description: Optional[str] = None) -> None:
        """ Returns weather observations
        :param product: BOM Forecast Product ID
        """
        self.product = product
        self.desc = description

        self.issue_time = None
        self.aac = None
        self.forecasts = list()
        xml = self.get_forecast_data()
        self.parse_forecast_data(xml)

    def __repr__(self):
        return f"<Forecast {self.product} {self.desc} - Issued {self.issue_time}>"

    def get_forecast_data(self):
        """ Download latest forecast from FTP server """
        host = "ftp.bom.gov.au"
        folder = "anon/gen/fwo"
        filename = f"{self.product}.xml"

        xml: str = ""
        with io.BytesIO() as fp:
            with ftplib.FTP(host) as ftp:
                ftp.login()
                ftp.cwd(folder)
                ftp.retrbinary(f"RETR {filename}", fp.write)
                fp.seek(0)  # Return to start of file
                xml = fp.read().decode()
        return xml

    def parse_forecast_data(self, xml):
        """ Process the XML data """
        tree = ElementTree.fromstring(xml)
        amoc = tree.find("amoc")
        self.issue_time = amoc.find("issue-time-local").text

        # Get forecast area element
        locations = tree.find("forecast").findall("area[@type='location']")
        location = locations[0]
        if self.desc and self.desc != location.attrib["description"]:
            for loc in locations:
                if loc.attrib["description"] == self.desc:
                    location = loc

        self.aac = location.attrib["aac"]
        self.desc = location.attrib["description"]
        forecast_periods = location.findall("forecast-period")

        # See if there is a higer area element
        metros = tree.find("forecast").findall("area[@type='metropolitan']")
        try:
            metro = metros[0]
            metro_forecast_periods = metro.findall("forecast-period")
        except IndexError:
            metro = None

        for i, fp in enumerate(forecast_periods):
            forecast_index = fp.attrib["index"]
            start = parse(fp.attrib["start-time-utc"])
            start = start.replace(tzinfo=pytz.UTC)
            end = parse(fp.attrib["end-time-utc"])
            end = end.replace(tzinfo=pytz.UTC)

            forecast_icon = self.get_forecast_value(fp, "forecast_icon_code")
            temp_min = self.get_forecast_value(fp, "air_temperature_minimum")
            temp_max = self.get_forecast_value(fp, "air_temperature_maximum")
            forecast_text = self.get_forecast_value(fp, "forecast")
            if not forecast_text and metro:
                # Get forecast from the metroplitan forecast
                fp2 = metro_forecast_periods[i]
                if forecast_index == fp2.attrib["index"]:
                    forecast_text = self.get_forecast_value(fp2, "forecast")
            precis = self.get_forecast_value(fp, "precis")
            precis_prob = self.get_forecast_value(fp, "probability_of_precipitation")
            precis_range = self.get_forecast_value(fp, "precipitation_range")

            forecast = ForecastPeriod(
                start,
                end,
                forecast_icon,
                forecast_text,
                temp_max,
                temp_min,
                precis,
                precis_prob,
                precis_range,
            )
            self.forecasts.append(forecast)

    @staticmethod
    def get_forecast_value(forecast_element, metric):
        """ Search for first matching result """

        if forecast_element.findall(f"*[@type='{metric}']"):
            return forecast_element.findall(f"*[@type='{metric}']")[0].text
        return None
