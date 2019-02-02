# bomweather

[![PyPI version](https://badge.fury.io/py/bomweather.svg)](https://badge.fury.io/py/bomweather) [![Build Status](https://travis-ci.org/aguinane/bomweather.svg?branch=master)](https://travis-ci.org/aguinane/bomweather) [![Coverage Status](https://coveralls.io/repos/github/aguinane/bomweather/badge.svg)](https://coveralls.io/github/aguinane/bomweather)

Load weather data from the Australian Bureau of Meteorology (BOM) website.

# Find closest observation site to a location

```python
> from bomweather import closest_obs_station
> station = closest_obs_station(lat=-27.470125, lon=153.021072)
> print(station['site_name'], station['product'], station['wmo'])
BRISBANE IDQ60801 94576
```

# Get latest observation data

```python
> from bomweather import ObservationSite
> obs = ObservationSite(wmo=94576, product='IDQ60801')
> last_obs = obs.last_observation()
Observation(wmo=94576, name='Brisbane', history_product='IDQ60801', local_dt=datetime.datetime(2019, 1, 31, 6, 30), utc_dt=datetime.datetime(2019, 1, 30, 20, 30, tzinfo=<UTC>), lat=-27.5, lon=153.0, apparent_t=28.4, cloud=None, cloud_base_m=None, cloud_oktas=None, cloud_type=None, delta_t=2.2, gust_kmh=7, gust_kt=4, air_temp=24.5, dewpt=21.2, press=1014.3, press_msl=1014.3, press_qnh=1014.3, rain_trace=0.0, rel_hum=82, vis_km=None, weather=None, wind_dir='S', wind_spd_kmh=2, wind_spd_kt=1)
```

# Get forecast data

```python
> from bomweather import Forecast
> f = Forecast(product='IDQ10095')
> print(f)
<Forecast IDQ10095 Brisbane - Issued 2019-02-02T16:37:01+10:00>
> print(f.forecasts[-1])
ForecastPeriod(start=datetime.datetime(2019, 2, 8, 14, 0, tzinfo=<UTC>), end=datetime.datetime(2019, 2, 9, 14, 0, tzinfo=<UTC>), forecast_icon='17', forecast_text='Partly cloudy. Medium (40%) chance of showers, most likely later in the day. Light winds becoming northeasterly 15 to 25 km/h during the day.', temp_max='33', temp_min='22', precis='Possible shower.', precis_prob='40%', precis_range='0 to 4 mm')
```
