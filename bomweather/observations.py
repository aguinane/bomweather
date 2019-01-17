""" bomweather.observations

    Scrape the BOM website for weather observations
    http://www.bom.gov.au/catalogue/observations/about-weather-observations.shtml

"""

import ftplib
from io import BytesIO
from typing import NamedTuple
from typing import Optional
from datetime import datetime
import requests
import pytz


class Observation(NamedTuple):
    """ Weather Observation """

    wmo: int
    name: str
    history_product: str
    local_dt: datetime
    utc_dt: datetime
    lat: float
    lon: float
    apparent_t: Optional[float]
    cloud: Optional[str]
    cloud_base_m: Optional[float]
    cloud_oktas: Optional[float]
    cloud_type: Optional[str]
    delta_t: Optional[float]
    gust_kmh: Optional[float]
    gust_kt: Optional[float]
    air_temp: Optional[float]
    dewpt: Optional[float]
    press: Optional[float]
    press_msl: Optional[float]
    press_qnh: Optional[float]
    rain_trace: Optional[float]
    rel_hum: Optional[float]
    vis_km: Optional[float]
    weather: Optional[str]
    wind_dir: Optional[str]
    wind_spd_kmh: Optional[float]
    wind_spd_kt: Optional[float]


class ObservationSite():
    """ BOM Weather Station Observations

        List of stations (QLD Example):
        http://www.bom.gov.au/qld/observations/qldall.shtml

        Example station json results:
        http://www.bom.gov.au/fwo/IDQ60901/IDQ60901.94578.json

    """

    def __init__(self, wmo: int, product: str) -> None:
        """ Returns weather observations
        :param product: BOM History Product ID
        :param wmo: World Meteorological Organisation (WMO) ID
        """

        self.wmo = wmo
        self.product = product
        self.obs_url = f'http://www.bom.gov.au/fwo/{product}/{product}.{wmo}.json'

    def __repr__(self):
        return f"<Observations {self.product}.{self.wmo}>"

    @property
    def name(self):
        return self.last_observation().name

    def last_observation(self):
        """ Get latest observation """
        return self.get_observation(idx=0)

    def get_observation(self, idx):
        """ Return formatted observation data """

        obs = self.get_observation_data()['data'][idx]
        obs = self.dict_clean(obs)

        # Convert data types
        local_dt = datetime.strptime(obs['local_date_time_full'],
                                     '%Y%m%d%H%M%S')
        utc_dt = datetime.strptime(obs['aifstime_utc'], '%Y%m%d%H%M%S')
        utc_dt = utc_dt.replace(tzinfo=pytz.UTC)

        if obs['vis_km']:
            obs['vis_km'] = float(obs['vis_km'])

        if obs['rain_trace']:
            obs['rain_trace'] = float(obs['rain_trace'])

        return Observation(
            wmo=obs['wmo'],
            name=obs['name'],
            history_product=obs['history_product'],
            local_dt=local_dt,
            utc_dt=utc_dt,
            lat=obs['lat'],
            lon=obs['lon'],
            apparent_t=obs['apparent_t'],
            cloud=obs['cloud'],
            cloud_base_m=obs['cloud_base_m'],
            cloud_oktas=obs['cloud_oktas'],
            cloud_type=obs['cloud_type'],
            delta_t=obs['delta_t'],
            gust_kmh=obs['gust_kmh'],
            gust_kt=obs['gust_kt'],
            air_temp=obs['air_temp'],
            dewpt=obs['dewpt'],
            press=obs['press'],
            press_msl=obs['press_msl'],
            press_qnh=obs['press_qnh'],
            rain_trace=obs['rain_trace'],
            rel_hum=obs['rel_hum'],
            vis_km=obs['vis_km'],
            weather=obs['weather'],
            wind_dir=obs['wind_dir'],
            wind_spd_kmh=obs['wind_spd_kmh'],
            wind_spd_kt=obs['wind_spd_kt'])

    @staticmethod
    def dict_clean(obj: dict) -> dict:
        for k, v in obj.items():
            if v == '-':
                obj[k] = None
        return obj

    def get_observation_data(self):
        """ Get latest observations """
        r = requests.get(
            self.obs_url,
            timeout=10,
        )
        return r.json()['observations']
