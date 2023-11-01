import unittest
from unittest.mock import patch, MagicMock
from pandas import DataFrame
from requests import Response

from .sfmc import SalesForceMarketingCloud


class TestSalesforceMarketingCloud(unittest.TestCase):
    def setUp(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.text = '{"access_token": "adfaodfjajf08ua8fdf8"}'

        with patch("requests.post", return_value=response_mock):
            self.sfmc = SalesForceMarketingCloud(
                client_id="client_id",
                client_secret="client_secret",
                subdomain="subdomain"
            )
    
    def test_connection_test_success(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200

        with patch("requests.get", return_value=response_mock):
            result = self.sfmc.connection_test()

        self.assertEqual(result, "Connection to Salesforce Marketing Cloud is successful!")
    
    def test_connection_test_failure(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 401

        with patch("requests.get", return_value=response_mock):
            result = self.sfmc.connection_test()
        
        self.assertEqual(result, f"Connection to Salesforce Marketing Cloud failed, with status code: {response_mock.status_code}")
    
    def test_get_data_endpoint(self):
        endpoint = "/hub/v1/campaigns"

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {
            "count": 2,
            "pageSize": 2,
            "items": [
                {"column1":"value1", "column2":"value2"}
            ]
        }

        with patch('requests.get', return_value=response_mock):
            result = self.sfmc.get_data(endpoint=endpoint)
        
        self.assertIsInstance(result, DataFrame)

    def test_get_data_external_key(self):
        external_key = "adfja8df9afdhu"

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {
            "count": 2,
            "pageSize": 2,
            "items": [
                {"item1": {"column1":"value1"}, "item2": {"column2":"value2"},},
                {"item3": {"column1":"value3"}, "item4": {"column2":"value4"},}
            ]
        }

        with patch('requests.get', return_value=response_mock):
            result = self.sfmc.get_data(external_key=external_key)
        
        self.assertIsInstance(result, DataFrame)

    def test_get_data_value_error(self):
        external_key = "adfja8df9afdhu"
        endpoint = "/hub/v1/campaigns"

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {
            "count": 2,
            "pageSize": 2,
            "items": [
                {"item1": {"column1":"value1"}, "item2": {"column2":"value2"},},
                {"item3": {"column1":"value3"}, "item4": {"column2":"value4"},}
            ]
        }

        with patch('requests.get', return_value=response_mock) and self.assertRaises(ValueError):
            self.sfmc.get_data(external_key=external_key, endpoint=endpoint)
        

if __name__ == '__main__':
    unittest.main()