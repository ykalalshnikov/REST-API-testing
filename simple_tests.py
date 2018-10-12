import requests
import pytest


def valid_ip(address):
    """ Check if the ip address is correct. """

    parts = address.split(".")
    if len(parts) != 4:
        return False
    elif '0' in parts:
        return False
    for item in parts:
        if not 0 <= int(item) <= 255 or '0' in list(item):
            return False
    return True


def valid_lat_and_lon(lat, lon):
    """ Check if the latitude an longitude are correct. """

    if (0 <= float(lat) <= 90) and (0 <= float(lon) <= 180):
        return True
    else:
        return False


def check_empty_values(data):
    """ Check is there any empty values in the dict. """

    keys_with_empty_values = [k for k in data if str(data[k]) == '']
    return True if keys_with_empty_values == [] else False


def get_key_type(data, value):
    """ Return type of key. """

    key_type = type(data[value])
    return key_type


def test_code_status():
    """ Check is the response code equals 200. """

    url = "http://ip-api.com/json"
    response = requests.get(url)

    assert response.status_code == 200, 'response code is not 200'


def test_empty_values():
    """ Check is there any empty values in the dict. """

    url = "http://ip-api.com/json"
    response = requests.get(url)
    json_data = response.json()

    assert check_empty_values(json_data) is True,\
        'There are any empty values in the dictionary'


def test_ip_address():
    """ Check if the ip address is correct. """

    url = "http://ip-api.com/json"
    response = requests.get(url)
    json_data = response.json()

    assert valid_ip(json_data['query']) is True, 'ip address is not correct '


def test_lan_and_lot():
    """ Check if the latitude an longitude are correct. """

    url = "http://ip-api.com/json"
    response = requests.get(url)
    json_data = response.json()

    assert valid_lat_and_lon(json_data['lat'], json_data['lon']) is True,\
        'latitude or longitude is not correct'


def test_params_type():
    """ Check if the type of value is correct. """

    url = "http://ip-api.com/json"
    response = requests.get(url)
    json_data = response.json()

    assert get_key_type(json_data, "lat") == float, 'type of lat is not float'
    assert get_key_type(json_data, "city") == str, 'type of city is not string'


@pytest.mark.time_tests
def test_response_time():
    """ Check if the response time less than 0.1 second. """

    url = "http://ip-api.com/json"
    response = requests.get(url)

    assert response.elapsed.total_seconds() > 0.1, 'response time is less than 0.1 second'


def test_headers():
    """ Check if the value of content-type is correct. """

    url = "http://ip-api.com/json"
    response = requests.get(url)

    assert response.headers['Content-Type'] == 'application/json; charset=utf-8',\
        'response has another content type'
