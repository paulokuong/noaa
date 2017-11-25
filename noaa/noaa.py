# API Wrapper for NOAA API V3
# ===========================
# For more detailed information about NOAA API,
# visit: https://forecast-v3.weather.gov/documentation


import http.client as http_client
import json
from urllib.parse import urlencode


class ACCEPT(object):
    GEOJSON = 'application/geo+json'
    JSONLD = 'application/ld+json'
    DWML = 'application/vnd.noaa.dwml+xml'
    OXML = 'application/vnd.noaa.obs+xml'
    CAP = 'application/cap+xml'
    ATOM = 'application/atom+xml'


class NOAA(object):
    END_POINT = 'api.weather.gov'
    DEFAULT_USER_AGENT = 'Test (your@email.com)'

    def __init__(self, user_agent=None, accept=None):
        self._user_agent = self.DEFAULT_USER_AGENT
        self._accept = ACCEPT.GEOJSON
        if user_agent:
            self._user_agent = user_agent
        if accept:
            accepts = [getattr(ACCEPT, i)
                       for i in dir(ACCEPT) if '__' not in i]
            if accept not in accepts:
                raise Exception(
                    'Invalid format. '
                    'Available formats are: {}'.format(accepts))
            self._accept = accept

    @property
    def accept(self):
        return self._accept

    @accept.setter
    def accept(self, value):
        self._accept = value

    @property
    def user_agent(self):
        return self._user_agent

    @user_agent.setter
    def user_agent(self, value):
        self._user_agent = value

    def get_request_header(self):
        """Get required headers.

        Args:
            format (str): content type.

        Returns:
            dec: headers with access token.
        """

        return {
            'User-Agent': self._user_agent,
            'accept': self._accept
        }

    def make_get_request(self, uri):
        """Encapsulate code for GET request.

        Args:
            uri (str): full get url with query string.

        Returns:
            dict: dictionary response.
        """

        conn = http_client.HTTPSConnection(self.END_POINT)
        conn.request('GET', uri, headers=self.get_request_header())
        res = conn.getresponse()
        data = res.read()
        if data:
            return json.loads(data.decode("utf-8"))

        return {'Error: Cannot connect to weather.gov.'}

    def points(self, point, stations=False):
        """Metadata about a point.
        This is the primary endpoint for forecast information for a location.
        It contains linked data for the forecast, the hourly forecast,
        observation and other information. It also shows stations nearest to a point
        in order of distance.

        Args:
            point (str): lat,long.
        Returns:
            json: json response from api.
        """
        if stations:
            return self.make_get_request(
                "/points/{point}/stations".format(point=point))
        return self.make_get_request(
            "/points/{point}".format(point=point))

    def points_forecast(self, lat, long, hourly=False):
        """Get observation data from a weather station.

        Args:
            lat (float): latitude of the weather station coordinate.
            long (float): longitude of the weather station coordinate.
        Returns:
            json: json response from api.
        """

        if hourly:
            return self.make_get_request(
                "/points/{lat},{long}/forecast/hourly".format(
                    lat=lat, long=long))
        return self.make_get_request(
            "/points/{lat},{long}/forecast".format(lat=lat, long=long))

    def stations(self, **params):
        """Get list of US weather stations and their metadata.

        Args:
            station_id (str[optional]): station id.
            state (str[optional]): 2 letters state code.
            limit (int[optional]): limit of results.
        Returns:
            json: json response from api.
        """
        if len(params) > 0:
            if 'station_id' in params:
                params['id'] = params['station_id']
                del params['station_id']
            return self.make_get_request(
                "/stations?{query_string}".format(
                    query_string=urlencode(params)))
        return self.make_get_request("/stations")

    def stations_observations(self, station_id, **params):
        """Get observation data from specific station.

        Args:
            station_id (str): station id.
            start (str[optional]): start date of observation.
            end (str[optional]): end date of observation.
            limit (int[optional]): limit of results.
            current (bool[optional]): True if needs current observations.
            recordId (str[optional]): recordId, Record Id (ISO8601DateTime)
        Returns:
            json: json response from api.
        """
        if len(params) > 0:
            if 'recordId' in params:
                return self.make_get_request(
                    '/stations/{stationId}/observations/{recordId}'.format(
                        stationId=station_id, recordId=params['recordId']))
            if 'current' in params:
                return self.make_get_request(
                    '/stations/{stationId}/observations/current'.format(
                        stationId=station_id))
            return self.make_get_request(
                "/stations/{stationId}/observations?{query_string}".format(
                    stationId=station_id, query_string=urlencode(params)))
        return self.make_get_request(
            "/stations/{stationId}/observations".format(stationId=station_id))

    def products(self, id):
        """Get data of a product.

        Args:
            id (str): product id.
        Returns:
            json: json response from api.
        """
        return self.make_get_request(
            "/products/{productId}".format(productId=id))

    def products_types(self, **params):
        """Get a list of product types with an active product.

        Args:
            type_id (str): an id of a valid product type
            locations (boolean[optional]): True to get a list of
                locations that have issues products for a type.
            location_id (str): location id.
        Returns:
            json: json response from api.
        """
        if 'type_id' in params and 'locations' not in params:
            return self.make_get_request(
                "/products/types/{type_id}".format(type_id=params['type_id']))
        elif 'locations' in params:
            if 'type_id' not in params:
                raise Exception('Error: Missing type id (type_id=None)')
            if 'location_id' in params:
                return self.make_get_request(
                    ('/products/types/{type_id}/locations/'
                     '{location_id}').format(
                        type_id=params['type_id'],
                        location_id=params['location_id']))
            else:
                return self.make_get_request(
                    "/products/types/{type_id}/locations".format(
                        type_id=params['type_id']))
        return self.make_get_request("/products/types")

    def products_locations(self, **params):
        """A list of locations with active products.

        Args:
            location_id (str): location id.
        Returns:
            json: json response from api.
        """
        if 'location_id' in params:
            return self.make_get_request(
                "/products/locations/{locationId}/types".format(
                    locationId=params['location_id']))
        return self.make_get_request("/products/locations")

    def offices(self, office_id):
        """Metadata about a Weather Office.

        Args:
            office_id (str): office id.
        Returns:
            json: json response from api.
        """
        return self.make_get_request("/offices/{office_id}".format(
            office_id=office_id))

    def zones(self, type, zone_id, forecast=False):
        """Metadata for a zone and forecast data for zone.

        Args:
            type (str): a valid zone type (list forthcoming).
            zone_id (str): a zone id (list forthcoming).
            forecast (bool): True to show forecast data of the zone.
        Returns:
            json: json response from api.
        """
        if forecast:
            return self.make_get_request(
                "/zones/{type}/{zone_id}/forecast".format(type=type, zone_id=zone_id))
        return self.make_get_request("/zones/{type}/{zone_id}".format(type=type, zone_id=zone_id))

    def alerts(self, **params):
        """A list of alerts that can be filtered by parameters.
        If no parameters are provided, then all alerts are returned.
        The ATOM format returns items in CAP-ATOM.

        Args:
            alert_id (str): alert id.
            active (int): Active alerts (1 or 0).
            start (str): Start time (ISO8601DateTime).
            end (str): End time (ISO8601DateTime).
            status (str): Event status (alert, update, cancel).
            type (str): Event type (list forthcoming).
            zone_type (str): Zone type (land or marine).
            point (str): Point (latitude,longitude).
            region (str): Region code (list forthcoming).
            state (str): State/marine code (list forthcoming).
            zone (str): Zone Id (forecast or county, list forthcoming).
            urgency (str): Urgency (expected, immediate).
            severity (str): Severity (minor, moderate, severe).
            certainty (str): Certainty (likely, observed).
            limit (int) Limit (an integer).
        Returns:
            json: json response from api.
        """
        if 'alert_id' in params:
            return self.make_get_request(
                "/alerts/{alert_id}".format(alert_id=params['alert_id']))
        return self.make_get_request(
            "/alerts?{query_string}".format(query_string=urlencode(params)))

    def active_alerts(self, count=False, **params):
        """Active alerts endpoints.

        Args:
            count (bool): True to hit /alerts/active/count.
            zone_id (str): a valid zone, see list in counts endpoint.
            area (str): a valid area, see list in counts endpoint.
            region (str): a valid region, see list in counts endpoint
        Returns:
            json: json response from api.
        """

        if count:
            return self.make_get_request("/alerts/count")
        if 'zone_id' in params:
            return self.make_get_request(
                "/alerts/active/zone/{zoneId}".format(zoneId=params['zone_id']))
        if 'area' in params:
            return self.make_get_request(
                "/alerts/active/area/{area}".format(area=params['area']))
        if 'region' in params:
            return self.make_get_request(
                "/alerts/active/region/{region}".format(region=params['region']))
        return self.make_get_request("/alerts/active")
