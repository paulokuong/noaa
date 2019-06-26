from urllib.parse import urlencode
import requests

from noaa_sdk.util import UTIL


class NCDC(UTIL):
    """Main class for getting data from NCDC.
    Documentation: https://www.ncdc.noaa.gov/cdo-web/webservices/v2
    """

    DEFAULT_END_POINT = 'www.ncdc.noaa.gov'
    DEFAULT_USER_AGENT = 'Test (your@email.com)'

    END_POINTS = {
        'datasets', 'datacategories',
        'datatypes', 'locationcategories',
        'locations', 'stations', 'data'}

    def __init__(self, token, user_agent=None, accept=None, show_uri=False):
        """Constructor.

        Args:
            token (str): token for api.
            user_agent (str[optional]): user agent specified in the header.
            accept (str[optional]): accept string specified in the header.
            show_uri (boolean[optional]): True for showing the
                actual url with query string being sent for requesting data.
        """
        if not token:
            raise Exception('Error: missing token.')
        if not user_agent:
            user_agent = self.DEFAULT_USER_AGENT

        self._token = token
        super().__init__(
            user_agent=user_agent, accept=accept,
            show_uri=show_uri)

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
        if not end_point:
            raise Exception('Error: end_point is None.')

        res = requests.get(
            'https://{}/{}'.format(self.DEFAULT_END_POINT, uri),
            headers=header)
        if res.status_code == 200:
            return res.json()
        raise Exception('Error: {} {}'.format(res.status_code, res.reason))

    def get_request_header(self):
        """Get required headers.

        Args:
            format (str): content type.

        Returns:
            dec: headers with access token.
        """

        return {
            'token': self._token
        }

    def request_end_point(self, end_point, **params):

        return self.make_get_request(
            end_point=self.DEFAULT_END_POINT,
            header=self.get_request_header(),
            uri='cdo-web/api/v2/{}?{}'.format(end_point, urlencode(params)))

    def datasets(self, **params):
        """ Request datasets endpoint.

        Args:
            datatypeid (str[optional]):	eg. ACMM. Accepts a valid data type id
                or a chain of data type ids seperated by ampersands.
                Datasets returned will contain all of the data type(s) specified.
            locationid (str[optional]):	eg. FIPS:37. Accepts a valid location id
                or a chain of location ids seperated by ampersands. Datasets
                returned will contain data for the location(s) specified.
            stationid (str[optional]): eg. COOP:010957. Accepts a valid station id
                or a chain of of station ids seperated by ampersands.
                Datasets returned will contain data for the station(s) specified.
            startdate (str[optional]): eg. 1970-10-03. Accepts valid ISO formated
                date (yyyy-mm-dd). Datasets returned will have data after the
                specified date. Paramater can be use independently of enddate
            enddate	(str[optional]): eg. 2012-09-10. Accepts valid ISO formated date (yyyy-mm-dd).
                Datasets returned will have data before the specified date.
                Paramater can be use independently of startdate
            sortfield (str[optional]): eg.name. The field to sort results by.
                Supports id, name, mindate, maxdate, and datacoverage fields.
            sortorder (str[optional]): eg. desc. Which order to sort by, asc or desc.
                Defaults to asc
            limit (int[optional]): eg.42. Defaults to 25, limits the number of
                results in the response. Maximum is 1000
            offset (str[optional]): eg.24. Defaults to 0, used to offset the resultlist.
                The example would begin with record 24.
        """

        return self.request_end_point('datasets', **params)
