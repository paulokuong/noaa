| |Build Status|

NOAA Python SDK
---------------

SDK for NOAA Weather Service REST API.

    | Fully unit tested SDK for NOAA Weather Service REST API.
    | https://www.weather.gov/documentation/services-web-api
    | https://github.com/paulokuong/noaa

Requirements
------------

-  Python 3.4 (tested)

Goal
----

| To provide a generic wrapper for the latest V3 NOAA weather service API.
| Keep on changing this SDK when NOAA updates their API.
| Class can be extended / decorated.

Code sample
-----------

| There are 3 types of forecast responses: forecast, forecastHourly, forecastGridData.
| To get weather forecast with postal code and country code.

.. code:: python

    from noaa_sdk import NOAA
    n = NOAA()
    res = n.get_forecasts('11365', 'US', type='forecastGridData')
    for i in res:
        print(i)

| To get weather observation data from all nearest stations in 11375, US between 2017-12-01 00:00:00 (UTC) to 2017-12-01 05:00:00 (UTC)

.. code:: python

    from noaa_sdk import NOAA
    n = NOAA()
    observations = n.get_observations('11365','US')
    for observation in observations:
        print(observation)

| To get weather forecast for a coordinate in USA

.. code:: python

    from noaa_sdk import NOAA
    n = NOAA()
    n.points_forecast(40.7314, -73.8656, type='forecastGridData')

Contributors
------------

-  Paulo Kuong (`@pkuong`_)

.. _@pkuong: https://github.com/paulokuong

.. |Build Status| image:: https://travis-ci.org/paulokuong/noaa.svg?branch=master
.. target: https://travis-ci.org/paulokuong/noaa
