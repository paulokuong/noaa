[![Build Status](https://travis-ci.org/paulokuong/noaa.svg?branch=master)](https://travis-ci.org/paulokuong/knapsack01)[![Coverage Status](https://coveralls.io/repos/github/paulokuong/noaa/badge.svg?branch=master)](https://coveralls.io/github/paulokuong/noaa?branch=master)
NOAA Python SDK
===============

SDK for NOAA Weather Service REST API.

> Fully unit tested SDK for NOAA Weather Service REST API.
> Official documentation: https://forecast-v3.weather.gov/documentation

Requirements
------------

* Python 3.4 (tested)

Goal
----

To provide a generic wrapper for the latest V3 NOAA weather service API.
Keep on changing this SDK when NOAA updates their API. Class can be extended
/ decorated.

Code sample
-----------

| To get weather forecast for a coordinate in USA

```python

    from noaa import noaa

    n = noaa.NOAA()
    n.points_forecast(40.7314, -73.8656, hourly=False)
```

Contributors
------------

* Paulo Kuong ([@pkuong](https://github.com/paulokuong))