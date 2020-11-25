from collections import namedtuple
from datetime import datetime
from functools import wraps
import requests
import time


from noaa_sdk.accept import ACCEPT


class UTIL(object):
    """Utility class for making requests."""

    def __init__(self, user_agent='', accept=None, show_uri=False):
        """Constructor.

        Args:
            user_agent (str[optional]): user agent specified in the header.
            accept (str[optional]): accept string specified in the header.
        """
        self._show_uri = show_uri
        self._user_agent = user_agent

        if accept:
            accepts = [getattr(ACCEPT, i)
                       for i in dir(ACCEPT) if '__' not in i]
            accepts = sorted(accepts)
            if accept not in accepts:
                raise Exception(
                    'Invalid format. '
                    'Available formats are: {}'.format(accepts))
            self._accept = accept

    def _retry_request_decorator(max_retries):
        def _retry_request_sub_decorator(request):
            @wraps(request)
            def wrapper(*args, **kargs):
                status_code = ''
                response = {}
                retry = 0
                fib_num_a = 1
                fib_num_b = 1

                while status_code == '' or (retry <= max_retries and (
                        status_code == '' or status_code != 200)):
                    if retry > 0:
                        print(
                            ('Previous request failed with code {}. '
                             'Retrying...').format(status_code))
                        print('Previous Response: {}'.format(
                            response.text))
                    response = request(*args, **kargs)
                    status_code = response.status_code
                    new_interval = fib_num_b + fib_num_a
                    fib_num_a = fib_num_b
                    time.sleep(new_interval)
                    fib_num_b = new_interval
                    retry += 1

                if retry > max_retries:
                    raise Exception(
                        'Maximum retries exceeded. Response object dump: {}'.format(
                            response))
                return response

            return wrapper

        return _retry_request_sub_decorator

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

    @_retry_request_decorator(5)
    def _get(self, end_point, uri, header):
        response = None
        try:
            response = requests.get(
                'https://{}/{}'.format(end_point, uri), headers=header)
        except Exception as err:
            if self._show_uri:
                print('Caught exception: {}'.format(str(err)))
            InstanceProperties = namedtuple(
                'ResponseProperties', ['status_code'])
            response = InstanceProperties(status_code=500)
        return response

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

        if 'http://' in uri or 'https://' in uri:
            uri = uri.replace('http://', '').replace('https://', '')
            end_point = uri.split('/')[0]
            uri = uri.replace(end_point, '')

        res = self._get(end_point, uri, header)

        return res.json()

    def parse_param_timestamp(self, str_date_time):
        """Parse string to datetime object.

        Args:
            str_date_time (str): date time 3 different formats:
                '%Y-%m-%dT%H:%M:%SZ' | '%Y-%m-%d' | '%Y-%m-%d %H:%M:%S'
        Returns:
            datetime object.
        """
        formats = [
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%d',
            '%Y-%m-%d %H:%M:%S'
        ]

        for format in formats:
            try:
                return datetime.strptime(str_date_time, format)
            except Exception as err:
                continue

        raise Exception(
            "Error: start and end must have "
            "format '%Y-%m-%dT%H:%M:%SZ' | '%Y-%m-%d' | '%Y-%m-%d %H:%M:%S'")

    def parse_response_timestamp(self, str_date_time):
        """Parse string to datetime object.

        Args:
            str_date_time (str): date time in format (YYYY-MM-DD)
        Returns:
            datetime object.
        """
        return datetime.strptime(str_date_time, '%Y-%m-%dT%H:%M:%S+00:00')
