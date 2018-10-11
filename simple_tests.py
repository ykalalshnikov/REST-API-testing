import requests


BASE_URL = "http://ip-api.com"

response = requests.get(BASE_URL + "/json/?fields=country,city,lat,lon,timezone,org")
params = {
   "city":"St Petersburg",
   "country":"Russia",
   "lat":59.8944,
   "lon":30.2642,
   "org":"Z-Telecom network",
   "timezone":"Europe/Moscow"
}

json_data = response.json()


def get_param_type(data, parameter):
    param_type = type(data[parameter])
    return param_type


def test_code_status():
    assert response.status_code == 200, 'response code is not 200'


def test_response_data():
    assert json_data == params, 'json data is nit expected'


def test_params_type():
    assert get_param_type(json_data, "lat") == float, 'type of lat is not float'
    assert get_param_type(json_data, "city") == str, 'type of lat is not string'


def test_response_time():
    assert response.elapsed.total_seconds() < 0.1, 'response time is lower than 0.1 second'


def test_headers():
    assert response.headers['Content-Type'] == 'application/json; charset=utf-8', 'response has another content type'


