# API Wrapper for NOAA API V3
# ===========================
# For more detailed information about NOAA API,
# visit: https://forecast-v3.weather.gov/documentation


import http.client as http_client
import json
from urllib.parse import urlencode


class ACCEPT(object):
    """Encapsulate all accept strings."""

    GEOJSON = 'application/geo+json'
    JSONLD = 'application/ld+json'
    DWML = 'application/vnd.noaa.dwml+xml'
    OXML = 'application/vnd.noaa.obs+xml'
    CAP = 'application/cap+xml'
    ATOM = 'application/atom+xml'


class UTIL(object):
    """Utility class for making requests."""

    def __init__(self, user_agent=None, accept=None, show_uri=False):
        """Constructor.

        Args:
            user_agent (str[optional]): user agent specified in the header.
            accept (str[optional]): accept string specified in the header.
        """
        self._show_uri = show_uri
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
    def show_uri(self):
        return self._show_uri

    @show_uri.setter
    def show_uri(self, value):
        self._show_uri = value

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

    def make_get_request(self, uri, header=None, end_point=None):
        """Encapsulate code for GET request.

        Args:
            uri (str): full get url with query string.
            header (dict): request header.
            end_point (str): end point host.

        Returns:
            dict: dictionary response.
        """

        if self._show_uri:
            print('Calling: {}'.format(uri))
        if not header:
            header = self.get_request_header()
        if not end_point:
            raise Exception('Error: end_point is None.')

        conn = http_client.HTTPSConnection(end_point)
        conn.request('GET', uri, headers=header)
        res = conn.getresponse()
        data = res.read()
        if data:
            return json.loads(data.decode("utf-8"))


class OSM(UTIL):
    """Make request to Open Street Map nominatim Api."""

    OSM_ENDPOINT = 'nominatim.openstreetmap.org'

    def __init__(self, user_agent='', accept='', show_uri=False):
        """Constructor.

        Args:
            user_agent (str[optional]): user agent specified in the header.
            accept (str[optional]): accept string specified in the header.
        """
        self._user_agent = user_agent
        self._accept = accept
        super().__init__(
            user_agent=user_agent, accept=accept, show_uri=show_uri)

    def get_lat_lon_by_postalcode_country(self, postalcode, country):
        """Get latitude and longitude coordinate from postalcode
        and country code.

        Args:
            postalcode (str): postal code.
            country (str): 2 letter country code.
        Returns:
            tuple: tuple of latitude and longitude.
        """
        res = self.make_get_request(
            '/search?postalcode={}&country={}&format=json'.format(
                postalcode, country), end_point=self.OSM_ENDPOINT)
        if len(res) == 0 or 'lat' not in res[0] or 'lon' not in res[0]:
            raise Exception('No response from: {}'.format(self.OSM_ENDPOINT))
        return float(res[0]['lat']), float(res[0]['lon'])

    def get_postalcode_country_by_lan_lon(self, lat, lon):
        """Get postalcode and country code by latitude and longitude.

        Args:
            lat (float): latitude.
            lon (float): longitude.
        Returns:
            tuple: tuple of postalcode and country code.
        """
        res = self.make_get_request(
            '/reverse?lat={}&lon={}&addressdetails=1&format=json'.format(
                lat, lon),
            end_point=self.OSM_ENDPOINT)
        if 'address' not in res:
            raise Exception('No address found.')

        if 'country_code' not in res['address']:
            raise Exception('No country code found.')

        if 'postcode' not in res['address']:
            raise Exception('No postal code found.')

        return res['address']['postcode'], res['address']['country_code']


class NOAA(UTIL):
    """Main class for getting data from NOAA."""

    DEFAULT_END_POINT = 'api.weather.gov'
    DEFAULT_USER_AGENT = 'Test (your@email.com)'

    def __init__(self, user_agent=None, accept=None, show_uri=False):
        """Constructor.

        Args:
            user_agent (str[optional]): user agent specified in the header.
            accept (str[optional]): accept string specified in the header.
            show_uri (boolean[optional]): True for showing the
                actual url with query string being sent for requesting data.
        """
        if not user_agent:
            user_agent = self.DEFAULT_USER_AGENT
        if not accept:
            accept = ACCEPT.GEOJSON

        super().__init__(
            user_agent=user_agent, accept=accept,
            show_uri=show_uri)
        self._osm = OSM()

    def get_observations_by_postalcode_country(
            self, postalcode, country, start, end,
            num_of_stations=-1):
        """Get all nearest station observations by postalcode and
        country code.

           This is an extensive functionality, aligning data
           from Open Street Map to enable postal code and country code
           params for weather observation data.

        Args:
            postalcode (str): postal code.
            country (str): 2 letter country code.
            start (str): start date of observation
                (eg. 2017-06-11T11:50:00Z).
            end (str): end date of observation
                (eg. 2017-06-11T11:50:00Z).
            num_of_stations (int[optional]): get observations from the
                nearest x stations.
        Returns:
            generator: generator of dictionaries of observations with the
            following variables: 'relativeHumidity', 'presentWeather',
            'minTemperatureLast24Hours', 'windGust', 'precipitationLast6Hours',
            'cloudLayers', 'dewpoint', 'temperature', 'windDirection',
            'rawMessage', '@type', 'precipitationLast3Hours',
            'visibility', 'icon', 'barometricPressure', 'windChill',
            'station', 'textDescription', 'seaLevelPressure', '@id',
            'timestamp', 'maxTemperatureLast24Hours', 'precipitationLastHour',
            'heatIndex', 'windSpeed', 'elevation'
        """
        lat, lon = self._osm.get_lat_lon_by_postalcode_country(
            postalcode, country)
        stations = self.points(
            '{},{}'.format(round(lat, 4), round(lon, 4)), stations=True)

        for index, station in enumerate(stations['observationStations']):
            if num_of_stations > 0 and num_of_stations <= index:
                break
            station_id = station.split('/')[-1]
            response = self.stations_observations(
                station_id=station_id, start=start, end=end)
            for observation in response['features']:
                yield observation['properties']

    def points(self, point, stations=False):
        """Metadata about a point.
        This is the primary endpoint for forecast information for a location.
        It contains linked data for the forecast, the hourly forecast,
        observation and other information. It also shows stations nearest to a point
        in order of distance.

        Response in this method should not be modified.
        In this way, we can keep track of changes made by NOAA through
        functional tests @todo(paulokuong) later on.

        Args:
            point (str): lat,long.
            stations (boolean): True for finding stations.
        Returns:
            json: json response from api.
        """

        if stations:
            return self.make_get_request(
                "/points/{point}/stations".format(point=point),
                end_point=self.DEFAULT_END_POINT)
        return self.make_get_request(
            "/points/{point}".format(point=point),
            end_point=self.DEFAULT_END_POINT)

    def points_forecast(self, lat, long, hourly=False):
        """Get observation data from a weather station.

        Response in this method should not be modified.
        In this way, we can keep track of changes made by NOAA through
        functional tests @todo(paulokuong) later on.

        Args:
            lat (float): latitude of the weather station coordinate.
            long (float): longitude of the weather station coordinate.
        Returns:
            json: json response from api.
        """

        if hourly:
            return self.make_get_request(
                "/points/{lat},{long}/forecast/hourly".format(
                    lat=lat, long=long), end_point=self.DEFAULT_END_POINT)
        return self.make_get_request(
            "/points/{lat},{long}/forecast".format(lat=lat, long=long),
            end_point=self.DEFAULT_END_POINT)

    def stations(self, **params):
        """Get list of US weather stations and their metadata.

        Response in this method should not be modified.
        In this way, we can keep track of changes made by NOAA through
        functional tests @todo(paulokuong) later on.

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
                    query_string=urlencode(params)),
                end_point=self.DEFAULT_END_POINT)
        return self.make_get_request(
            "/stations", end_point=self.DEFAULT_END_POINT)

    def stations_observations(self, station_id, **params):
        """Get observation data from specific station.

        Response in this method should not be modified.
        In this way, we can keep track of changes made by NOAA through
        functional tests @todo(paulokuong) later on.

        Args:
            station_id (str): station id.
            start (str[optional]): start date of observation
                (eg. 2017-06-11T11:50:00Z).
            end (str[optional]): end date of observation
                (eg. 2017-06-11T11:50:00Z).
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
                        stationId=station_id, recordId=params['recordId']),
                    end_point=self.DEFAULT_END_POINT)
            if 'current' in params:
                return self.make_get_request(
                    '/stations/{stationId}/observations/current'.format(
                        stationId=station_id),
                    end_point=self.DEFAULT_END_POINT)
            return self.make_get_request(
                "/stations/{stationId}/observations?{query_string}".format(
                    stationId=station_id, query_string=urlencode(params)),
                end_point=self.DEFAULT_END_POINT)
        return self.make_get_request(
            "/stations/{stationId}/observations".format(stationId=station_id),
            end_point=self.DEFAULT_END_POINT)

    def products(self, id):
        """Get data of a product.

        Response in this method should not be modified.
        In this way, we can keep track of changes made by NOAA through
        functional tests @todo(paulokuong) later on.

        Args:
            id (str): product id.
        Returns:
            json: json response from api.
        """
        return self.make_get_request(
            "/products/{productId}".format(productId=id),
            end_point=self.DEFAULT_END_POINT)

    def products_types(self, **params):
        """Get a list of product types with an active product.

        Response in this method should not be modified.
        In this way, we can keep track of changes made by NOAA through
        functional tests @todo(paulokuong) later on.

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
                "/products/types/{type_id}".format(type_id=params['type_id']),
                end_point=self.DEFAULT_END_POINT)
        elif 'locations' in params:
            if 'type_id' not in params:
                raise Exception('Error: Missing type id (type_id=None)')
            if 'location_id' in params:
                return self.make_get_request(
                    ('/products/types/{type_id}/locations/'
                     '{location_id}').format(
                        type_id=params['type_id'],
                        location_id=params['location_id']),
                    end_point=self.DEFAULT_END_POINT)
            else:
                return self.make_get_request(
                    "/products/types/{type_id}/locations".format(
                        type_id=params['type_id']),
                    end_point=self.DEFAULT_END_POINT)
        return self.make_get_request(
            "/products/types",
            end_point=self.DEFAULT_END_POINT)

    def products_locations(self, **params):
        """A list of locations with active products.

        Response in this method should not be modified.
        In this way, we can keep track of changes made by NOAA through
        functional tests @todo(paulokuong) later on.

        Args:
            location_id (str): location id.
        Returns:
            json: json response from api.
        """
        if 'location_id' in params:
            return self.make_get_request(
                "/products/locations/{locationId}/types".format(
                    locationId=params['location_id']),
                end_point=self.DEFAULT_END_POINT)
        return self.make_get_request(
            "/products/locations",
            end_point=self.DEFAULT_END_POINT)

    def offices(self, office_id):
        """Metadata about a Weather Office.

        Response in this method should not be modified.
        In this way, we can keep track of changes made by NOAA through
        functional tests @todo(paulokuong) later on.

        Args:
            office_id (str): office id.
        Returns:
            json: json response from api.
        """
        return self.make_get_request("/offices/{office_id}".format(
            office_id=office_id), end_point=self.DEFAULT_END_POINT)

    def zones(self, type, zone_id, forecast=False):
        """Metadata for a zone and forecast data for zone.

        Response in this method should not be modified.
        In this way, we can keep track of changes made by NOAA through
        functional tests @todo(paulokuong) later on.

        Args:
            type (str): a valid zone type (list forthcoming).
            zone_id (str): a zone id (list forthcoming).
            forecast (bool): True to show forecast data of the zone.
        Returns:
            json: json response from api.
        """
        if forecast:
            return self.make_get_request(
                "/zones/{type}/{zone_id}/forecast".format(
                    type=type, zone_id=zone_id),
                end_point=self.DEFAULT_END_POINT)
        return self.make_get_request("/zones/{type}/{zone_id}".format(
            type=type, zone_id=zone_id), end_point=self.DEFAULT_END_POINT)

    def alerts(self, **params):
        """A list of alerts that can be filtered by parameters.
        If no parameters are provided, then all alerts are returned.
        The ATOM format returns items in CAP-ATOM.

        Response in this method should not be modified.
        In this way, we can keep track of changes made by NOAA through
        functional tests @todo(paulokuong) later on.

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
                "/alerts/{alert_id}".format(alert_id=params['alert_id']),
                end_point=self.DEFAULT_END_POINT)
        return self.make_get_request(
            "/alerts?{query_string}".format(query_string=urlencode(params)),
            end_point=self.DEFAULT_END_POINT)

    def active_alerts(self, count=False, **params):
        """Active alerts endpoints.

        Response in this method should not be modified.
        In this way, we can keep track of changes made by NOAA through
        functional tests @todo(paulokuong) later on.

        Args:
            count (bool): True to hit /alerts/active/count.
            zone_id (str): a valid zone, see list in counts endpoint.
            area (str): a valid area, see list in counts endpoint.
            region (str): a valid region, see list in counts endpoint
        Returns:
            json: json response from api.
        """

        if count:
            return self.make_get_request(
                "/alerts/count",
                end_point=self.DEFAULT_END_POINT)
        if 'zone_id' in params:
            return self.make_get_request(
                "/alerts/active/zone/{zoneId}".format(
                    zoneId=params['zone_id']),
                end_point=self.DEFAULT_END_POINT)
        if 'area' in params:
            return self.make_get_request(
                "/alerts/active/area/{area}".format(
                    area=params['area']),
                end_point=self.DEFAULT_END_POINT)
        if 'region' in params:
            return self.make_get_request(
                "/alerts/active/region/{region}".format(
                    region=params['region']),
                end_point=self.DEFAULT_END_POINT)
        return self.make_get_request(
            "/alerts/active",
            end_point=self.DEFAULT_END_POINT)
