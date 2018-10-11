import requests
import pytest


BASE_URL = "http://ip-api.com"

response = requests.get(BASE_URL + "/json")

json_data = response.json()


def valid_ip(address):
    parts = address.split(".")
    if len(parts) != 4:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255:
            return False
    return True


def valid_lat_and_lon(lat, lon):
    if (0 <= float(lat) <= 90) and (0 <= float(lon) <= 180):
        return True
    else:
        return False


def get_param_type(data, parameter):
    param_type = type(data[parameter])
    return param_type


def test_code_status():
    assert response.status_code == 200, 'response code is not 200'


def check_empty_values(data):
    for k, v in data.items():
        if len(str(v)) < 1:
            return k


def test_qwe():
    assert check_empty_values(json_data) is None, 'any empty values in response'


def test_query():
    assert valid_ip(json_data['query']) is True, 'ip address is not correct '


def test_lan_and_lot():
    assert valid_lat_and_lon(json_data['lat'], json_data['lon']) is True, 'latitude or longitude is not correct'


def test_params_type():
    assert get_param_type(json_data, "lat") == float, 'type of lat is not float'
    assert get_param_type(json_data, "city") == str, 'type of city is not string'


@pytest.mark.time_tests
def test_response_time():
    assert response.elapsed.total_seconds() < 0.1, 'response time is lower than 0.1 second'


def test_headers():
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8', 'response has another content type'


