from __future__ import absolute_import
from __future__ import print_function
from unittest.mock import patch
from noaa_sdk import noaa
import pytest

try:
    from unittest.mock import MagicMock
except:
    from mock import MagicMock


def test_instantiation():
    """Test instantiation of NOAA class.
    """
    n = noaa.NOAA()
    assert n._user_agent == n.DEFAULT_USER_AGENT


def test_set_accept():
    """Test setting valid accept string.
    """
    with pytest.raises(Exception) as err:
        noaa.NOAA(accept='test')
    assert str(err.value) == (
        "Invalid format. Available formats are: "
        "['application/atom+xml', 'application/cap+xml', "
        "'application/vnd.noaa.dwml+xml', 'application/geo+json', "
        "'application/ld+json', 'application/vnd.noaa.obs+xml']")


def test_test_user_agent():
    """Test able to set/get user agent.
    """
    n = noaa.NOAA(user_agent='test_agent')
    assert n._user_agent == 'test_agent'
    n.user_agent = 'test_agent2'
    assert n.user_agent == 'test_agent2'


def test_get_request_header():
    """Test request header is set correctly.
    """

    n = noaa.NOAA(user_agent='test_agent', accept=noaa.ACCEPT.CAP)
    request_header = n.get_request_header()
    assert request_header == {
        'User-Agent': 'test_agent',
        'accept': 'application/cap+xml'
    }


@patch('noaa_sdk.noaa.http_client.HTTPSConnection')
def test_make_get_request(mock_http_client):
    mock_response_obj = MagicMock()
    mock_response_obj.read = lambda: b'{"test":"test"}'
    mock_conn_object = MagicMock()
    mock_conn_object.request = lambda x, y, **z: None
    mock_conn_object.getresponse = lambda: mock_response_obj
    mock_http_client.return_value = mock_conn_object

    n = noaa.NOAA(user_agent='test_agent')
    res = n.make_get_request(
        'http://test', end_point='test.paulo.com')
    assert res == {"test": "test"}


@patch('noaa_sdk.noaa.http_client.HTTPSConnection')
def test_make_get_request_failed(mock_http_client):
    mock_response_obj = MagicMock()
    mock_response_obj.read = lambda: None
    mock_conn_object = MagicMock()
    mock_conn_object.request = lambda x, y, **z: None
    mock_conn_object.getresponse = lambda: mock_response_obj
    mock_http_client.return_value = mock_conn_object

    with pytest.raises(Exception) as err:
        n = noaa.NOAA(user_agent='test_agent')
        n.make_get_request('http://test')
        assert err == 'Error: end_point is None.'


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_points(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.points('23.44,34.55')
    mock_make_get_request.assert_called_with(
        '/points/23.44,34.55', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_points_with_stations(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.points('23.44,34.55', stations=True)
    mock_make_get_request.assert_called_with(
        '/points/23.44,34.55/stations', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_points_forecast(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.points_forecast(23.44, 34.55, hourly=False)
    mock_make_get_request.assert_called_with(
        '/points/23.44,34.55/forecast', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_points_forecast_with_hourly(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.points_forecast(23.44, 34.55, hourly=True)
    mock_make_get_request.assert_called_with(
        '/points/23.44,34.55/forecast/hourly', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_stations(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.stations()
    mock_make_get_request.assert_called_with(
        '/stations', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_stations_with_station_id(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.stations(station_id='PAULOSTATION')
    mock_make_get_request.assert_called_with(
        '/stations?id=PAULOSTATION', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_stations_observations(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.stations_observations('PAULOSTATION')
    mock_make_get_request.assert_called_with(
        '/stations/PAULOSTATION/observations', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_stations_observations_with_current(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.stations_observations('PAULOSTATION', current=True)
    mock_make_get_request.assert_called_with(
        '/stations/PAULOSTATION/observations/current',
        end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_stations_observations_with_recordId(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.stations_observations(
        'PAULOSTATION', recordId='2017-01-04T18:54:00+00:00')
    mock_make_get_request.assert_called_with(
        '/stations/PAULOSTATION/observations/2017-01-04T18:54:00+00:00',
        end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_products(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.products('test_id')
    mock_make_get_request.assert_called_with(
        '/products/test_id', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_products_types_with_nothing(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.products_types()
    mock_make_get_request.assert_called_with(
        '/products/types', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_products_types_with_id(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.products_types(type_id='test_id')
    mock_make_get_request.assert_called_with(
        '/products/types/test_id', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_products_types_with_locations_failed(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')

    with pytest.raises(Exception) as err:
        n.products_types(locations=True, location_id='test_location_id')
    assert str(err.value) == ('Error: Missing type id (type_id=None)')


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_products_types_with_locations_and_id(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.products_types(
        locations=True,
        location_id='test_location_id', type_id='test_id')
    mock_make_get_request.assert_called_with(
        '/products/types/test_id/locations/test_location_id',
        end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_products_locations(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.products_locations(
        location_id='test_location_id')
    mock_make_get_request.assert_any_call(
        '/products/locations/test_location_id/types',
        end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_products_locations_without_id(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.products_locations()
    mock_make_get_request.assert_called_with(
        '/products/locations', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_offices(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.offices('test_office_id')
    mock_make_get_request.assert_called_with(
        '/offices/test_office_id', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_zones(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.zones('test_type', 'test_zone_id')
    mock_make_get_request.assert_called_with(
        '/zones/test_type/test_zone_id', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_zones_with_forecast(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.zones('test_type', 'test_zone_id', forecast=True)
    mock_make_get_request.assert_called_with(
        '/zones/test_type/test_zone_id/forecast',
        end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_alerts(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.alerts(
        active=2)
    mock_make_get_request.assert_called_with(
        '/alerts?active=2', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_alerts_with_alert_id(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.alerts(alert_id='test_alert_id')
    mock_make_get_request.assert_called_with(
        '/alerts/test_alert_id', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_active_alerts(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.active_alerts()
    mock_make_get_request.assert_called_with(
        '/alerts/active', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_active_alerts_with_count(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.active_alerts(count=True)
    mock_make_get_request.assert_called_with(
        '/alerts/count', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_active_alerts_with_zone_id(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.active_alerts(zone_id='test_zone_id')
    mock_make_get_request.assert_called_with(
        '/alerts/active/zone/test_zone_id', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_active_alerts_with_area(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.active_alerts(area='nyc')
    mock_make_get_request.assert_called_with(
        '/alerts/active/area/nyc', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.NOAA.make_get_request')
def test_active_alerts_with_region(mock_make_get_request):
    mock_make_get_request.return_value = None
    n = noaa.NOAA(user_agent='test_agent')
    n.active_alerts(region='test_region')
    mock_make_get_request.assert_called_with(
        '/alerts/active/region/test_region', end_point=n.DEFAULT_END_POINT)


@patch('noaa_sdk.noaa.OSM.make_get_request')
def test_osm_get_lat_lon_by_postalcode_country(mock_make_get_request):
    mock_make_get_request.return_value = [{'lat': 56.34, 'lon': 12.78}]
    n = noaa.OSM()
    lat, lon = n.get_lat_lon_by_postalcode_country('11365', 'US')
    mock_make_get_request.assert_called_with(
        '/search?postalcode=11365&country=US&format=json',
        end_point=n.OSM_ENDPOINT)
    assert lat == 56.34
    assert lon == 12.78


@patch('noaa_sdk.noaa.OSM.make_get_request')
def test_osm_get_lat_lon_by_postalcode_country_failed(mock_make_get_request):
    mock_make_get_request.return_value = []
    with pytest.raises(Exception) as err:
        n = noaa.OSM()
        n.get_lat_lon_by_postalcode_country('11365', 'US')
        mock_make_get_request.assert_called_with(
            '/search?postalcode=11365&country=US&format=json',
            end_point=n.OSM_ENDPOINT)
        assert err == 'No response from: {}'.format(n.OSM_ENDPOINT)


@patch('noaa_sdk.noaa.OSM.make_get_request')
def test_osm_get_postalcode_country_by_lan_lon(mock_make_get_request):
    mock_make_get_request.return_value = {
        'address': {
            'postcode': '11375', 'country_code': 'US'}
    }
    n = noaa.OSM()
    postcode, country = n.get_postalcode_country_by_lan_lon(23.22, 33.33)
    mock_make_get_request.assert_called_with(
        '/reverse?lat=23.22&lon=33.33&addressdetails=1&format=json',
        end_point=n.OSM_ENDPOINT)
    assert postcode == '11375'
    assert country == 'US'


@patch('noaa_sdk.noaa.OSM.make_get_request')
def test_osm_get_postalcode_country_by_lan_lon_failed(mock_make_get_request):
    mock_make_get_request.return_value = {}
    with pytest.raises(Exception) as err:
        n = noaa.OSM()
        n.get_postalcode_country_by_lan_lon(23.22, 33.33)
        mock_make_get_request.assert_called_with(
            '/reverse?lat=23.22&lon=33.33&addressdetails=1&format=json',
            end_point=n.OSM_ENDPOINT)
        assert err == 'No response from: {}'.format(n.OSM_ENDPOINT)
