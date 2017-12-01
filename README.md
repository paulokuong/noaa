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
        '11375','US','2017-12-01T00:00:00+00:00','2017-12-01T05:00:00+00:00')
    for observation in observations:
        print(observation)
        break
```

Result

```python
    {
     'seaLevelPressure': {'value': 102130, 'qualityControl': 'qc:V', 'unitCode': 'unit:Pa'},
     'icon': 'https://api.weather.gov/icons/land/day/few?size=medium',
     'elevation': {'value': 9, 'unitCode': 'unit:m'},
     'windDirection': {'value': 330, 'qualityControl': 'qc:V', 'unitCode': 'unit:degree_(angle)'},
     'precipitationLast6Hours': {'value': None, 'qualityControl': 'qc:Z', 'unitCode': 'unit:m'},
     'timestamp': '2017-12-01T13:51:00+00:00',
     'precipitationLast3Hours': {'value': None, 'qualityControl': 'qc:Z', 'unitCode': 'unit:m'},
     'temperature': {'value': 9.3999877929688, 'qualityControl': 'qc:V', 'unitCode': 'unit:degC'},
     'barometricPressure': {'value': 102130, 'qualityControl': 'qc:V', 'unitCode': 'unit:Pa'},
     'visibility': {'value': 16090, 'qualityControl': 'qc:C', 'unitCode': 'unit:m'},
     'cloudLayers': [{'amount': 'FEW', 'base': {'value': 7620, 'unitCode': 'unit:m'}}],
     'heatIndex': {'value': None, 'qualityControl': 'qc:V', 'unitCode': 'unit:degC'},
     'windSpeed': {'value': 6.1999998092651, 'qualityControl': 'qc:V', 'unitCode': 'unit:m_s-1'},
     'relativeHumidity': {'value': 60.763379620783, 'qualityControl': 'qc:C', 'unitCode': 'unit:percent'},
     '@type': 'wx:ObservationStation', 'presentWeather': [],
     'maxTemperatureLast24Hours': {'value': None, 'qualityControl': None, 'unitCode': 'unit:degC'},
     'rawMessage': 'KLGA 011351Z 33012KT 10SM FEW250 09/02 A3016 RMK AO2 SLP213 T00940022',
     'windGust': {'value': None, 'qualityControl': 'qc:Z', 'unitCode': 'unit:m_s-1'},
     'dewpoint': {'value': 2.2000061035156, 'qualityControl': 'qc:V', 'unitCode': 'unit:degC'},
     'minTemperatureLast24Hours': {'value': None, 'qualityControl': None, 'unitCode': 'unit:degC'},
     'windChill': {'value': 6.4144640119463, 'qualityControl': 'qc:V', 'unitCode': 'unit:degC'},
     '@id': 'https://api.weather.gov/stations/KLGA/observations/2017-12-01T13:51:00+00:00',
     'textDescription': 'Mostly Clear', 'station': 'https://api.weather.gov/stations/KLGA',
     'precipitationLastHour': {'value': None, 'qualityControl': 'qc:Z', 'unitCode': 'unit:m'}}
```

Contributors
------------

* Paulo Kuong ([@pkuong](https://github.com/paulokuong))
