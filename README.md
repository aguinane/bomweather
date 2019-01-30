# bomweather

[![PyPI version](https://badge.fury.io/py/bomweather.svg)](https://badge.fury.io/py/bomweather) [![Build Status](https://travis-ci.org/aguinane/bomweather.svg?branch=master)](https://travis-ci.org/aguinane/bomweather) [![Coverage Status](https://coveralls.io/repos/github/aguinane/bomweather/badge.svg)](https://coveralls.io/github/aguinane/bomweather)

Load weather data from the Australian Bureau of Meteorology (BOM) website.

# Find closest observation site to a location

```python
> from bomweather import closest_obs_station
> station = closest_obs_station(-27.470125, 153.021072)
> print(station['site_name'], station['product'], station['wmo'])
BRISBANE IDQ60801 94576
```

# Get latest observation data

```python
> from bomweather import ObservationSite
> obs = ObservationSite(94576, 'IDQ60801')
> last_obs = obs.last_observation()
Observation(wmo=94576, name='Brisbane', history_product='IDQ60801', local_dt=datetime.datetime(2019, 1, 31, 6, 30), utc_dt=datetime.datetime(2019, 1, 30, 20, 30, tzinfo=<UTC>), lat=-27.5, lon=153.0, apparent_t=28.4, cloud=None, cloud_base_m=None, cloud_oktas=None, cloud_type=None, delta_t=2.2, gust_kmh=7, gust_kt=4, air_temp=24.5, dewpt=21.2, press=1014.3, press_msl=1014.3, press_qnh=1014.3, rain_trace=0.0, rel_hum=82, vis_km=None, weather=None, wind_dir='S', wind_spd_kmh=2, wind_spd_kt=1)
```
