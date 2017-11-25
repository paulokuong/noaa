| |Build Status|

NOAA Python SDK
---------------

SDK for NOAA Weather Service REST API.

    | Fully unit tested SDK for NOAA Weather Service REST API.
    | https://forecast-v3.weather.gov/documentation

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

| To get weather forecast for a coordinate in USA

.. code:: python

    from noaa_sdk import noaa

    n = noaa.NOAA()
    n.points_forecast(40.7314, -73.8656, hourly=False)



Contributors
------------

-  Paulo Kuong (`@pkuong`_)

.. _@pkuong: https://github.com/paulokuong

.. |Build Status| image:: https://travis-ci.org/paulokuong/knapsack01.svg?branch=master
   :target: https://travis-ci.org/paulokuong/knapsack01