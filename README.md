[![Build Status](https://travis-ci.org/paulokuong/noaa.svg?branch=master)](https://travis-ci.org/paulokuong/noaa)[![Coverage Status](https://coveralls.io/repos/github/paulokuong/noaa/badge.svg?branch=master)](https://coveralls.io/github/paulokuong/noaa?branch=master)
NOAA Python SDK
===============

SDK for NOAA Weather Service REST API.

> Fully unit tested SDK for NOAA Weather Service REST API.
Official documentation: https://forecast-v3.weather.gov/documentation

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

To get weather observation data from all nearest stations in 11375, US between
2017-12-01 00:00:00 (UTC) to 2017-12-01 05:00:00 (UTC)

```python

    from noaa_sdk import noaa

    n = noaa.NOAA()
    observations = n.get_observations_by_postalcode_country(
        '11365','US','2017-12-01','2017-12-02')
    for observation in observations:
        print(observation)
        break
```

Result

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
