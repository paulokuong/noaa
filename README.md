[![Build Status](https://travis-ci.org/paulokuong/noaa.svg?branch=master)](https://travis-ci.org/paulokuong/noaa)[![Coverage Status](https://coveralls.io/repos/github/paulokuong/noaa/badge.svg?branch=master)](https://coveralls.io/github/paulokuong/noaa?branch=master)
NOAA Python SDK
===============

SDK for NOAA Weather Service REST API for getting recent and forecast data. For old observation data, please just download the  Global Historical Climatology Network data from here: https://www1.ncdc.noaa.gov/pub/data/ghcn/

> Fully unit tested SDK for NOAA Weather Service REST API.
Official documentation: https://www.weather.gov/documentation/services-web-api

Requirements
------------

* Python 3.4 (tested)

Installation
------------
```
    pip install noaa-sdk
```

Goal
----

To provide a generic wrapper for the latest V3 NOAA weather service API.
Keep on changing this SDK when NOAA updates their API. Class can be extended
/ decorated.

Code sample
-----------

To get weather forecast for a coordinate:

```python

    from noaa_sdk import noaa

    n = noaa.NOAA()
    n.points_forecast(40.7314, -73.8656, hourly=False)
```

To get weather forecast with postal code and country code.
```python

    from noaa_sdk import noaa

    n = noaa.NOAA()
    res = n.get_forecasts('11365', 'US', True)
    for i in res:
        print(i)
```

Result
```python
    {'startTime': '2018-02-18T00:00:00-05:00', 'detailedForecast': '', 'shortForecast': 'Partly Cloudy', 'windSpeed': '5 mph', 'number': 148, 'icon': 'https://api.weather.gov/icons/land/night/sct?size=small', 'windDirection': 'SW', 'isDaytime': False, 'temperatureTrend': None, 'endTime': '2018-02-18T01:00:00-05:00', 'name': '', 'temperatureUnit': 'F', 'temperature': 34}
    {'startTime': '2018-02-18T01:00:00-05:00', 'detailedForecast': '', 'shortForecast': 'Mostly Cloudy', 'windSpeed': '5 mph', 'number': 149, 'icon': 'https://api.weather.gov/icons/land/night/bkn?size=small', 'windDirection': 'SW', 'isDaytime': False, 'temperatureTrend': None, 'endTime': '2018-02-18T02:00:00-05:00', 'name': '', 'temperatureUnit': 'F', 'temperature': 33}
    {'startTime': '2018-02-18T02:00:00-05:00', 'detailedForecast': '', 'shortForecast': 'Mostly Cloudy', 'windSpeed': '5 mph', 'number': 150, 'icon': 'https://api.weather.gov/icons/land/night/bkn?size=small', 'windDirection': 'SW', 'isDaytime': False, 'temperatureTrend': None, 'endTime': '2018-02-18T03:00:00-05:00', 'name': '', 'temperatureUnit': 'F', 'temperature': 31}
    {'startTime': '2018-02-18T03:00:00-05:00', 'detailedForecast': '', 'shortForecast': 'Partly Cloudy', 'windSpeed': '5 mph', 'number': 151, 'icon': 'https://api.weather.gov/icons/land/night/sct?size=small', 'windDirection': 'SW', 'isDaytime': False, 'temperatureTrend': None, 'endTime': '2018-02-18T04:00:00-05:00', 'name': '', 'temperatureUnit': 'F', 'temperature': 31}
```

To get weather observation data from all nearest stations in 11375

```python

    from noaa_sdk import noaa

    n = noaa.NOAA()
    observations = n.get_observations('11365','US')
    for observation in observations:
        print(observation)
        break
```
with date range (*note: for old observations data, please download Global Historical Climatology Network data)
```python
    from noaa_sdk import noaa

    n = noaa.NOAA()
    observations = n.get_observations('11365','US',start='2017-01-01',end='2018-02-02')
    for observation in observations:
        print(observation)
        break
```

Example Result

```python
    {'minTemperatureLast24Hours': {'unitCode': 'unit:degC', 'qualityControl': None, 'value': None},
    'icon': 'https://api.weather.gov/icons/land/night/bkn?size=medium',
    '@type': 'wx:ObservationStation',
    'cloudLayers': [{'amount': 'BKN', 'base': {'unitCode': 'unit:m', 'value': 2900}}],
    'windSpeed': {'unitCode': 'unit:m_s-1', 'qualityControl': 'qc:V', 'value': 2.5999999046326},
    'temperature': {'unitCode': 'unit:degC', 'qualityControl': 'qc:V', 'value': 9.9999938964844},
    'precipitationLast6Hours': {'unitCode': 'unit:m', 'qualityControl': 'qc:Z', 'value': None},
    'relativeHumidity': {'unitCode': 'unit:percent', 'qualityControl': 'qc:C', 'value': 76.720955130964},
    'rawMessage': 'KBDR 010152Z 16005KT 10SM BKN095 10/06 A3006 RMK AO2 SLP179 T01000061',
    'windDirection': {'unitCode': 'unit:degree_(angle)', 'qualityControl': 'qc:V', 'value': 160},
    'seaLevelPressure': {'unitCode': 'unit:Pa', 'qualityControl': 'qc:V', 'value': 101790},
    'precipitationLastHour': {'unitCode': 'unit:m', 'qualityControl': 'qc:Z', 'value': None},
    'dewpoint': {'unitCode': 'unit:degC', 'qualityControl': 'qc:V', 'value': 6.1},
    'windGust': {'unitCode': 'unit:m_s-1', 'qualityControl': 'qc:Z', 'value': None},
    'maxTemperatureLast24Hours': {'unitCode': 'unit:degC', 'qualityControl': None, 'value': None},
    'windChill': {'unitCode': 'unit:degC', 'qualityControl': 'qc:V', 'value': 8.7570299365604},
    'barometricPressure': {'unitCode': 'unit:Pa', 'qualityControl': 'qc:V', 'value': 101800},
    '@id': 'https://api.weather.gov/stations/KBDR/observations/2017-12-01T01:52:00+00:00',
    'station': 'https://api.weather.gov/stations/KBDR', 'elevation': {'unitCode': 'unit:m', 'value': 5},
    'timestamp': '2017-12-01T01:52:00+00:00',
    'precipitationLast3Hours': {'unitCode': 'unit:m', 'qualityControl': 'qc:Z', 'value': None},
    'visibility': {'unitCode': 'unit:m', 'qualityControl': 'qc:C', 'value': 16090},
    'textDescription': 'Mostly Cloudy', 'presentWeather': [],
    'heatIndex': {'unitCode': 'unit:degC', 'qualityControl': 'qc:V', 'value': None}}
```

Contributors
------------

* Paulo Kuong ([@pkuong](https://github.com/paulokuong))
