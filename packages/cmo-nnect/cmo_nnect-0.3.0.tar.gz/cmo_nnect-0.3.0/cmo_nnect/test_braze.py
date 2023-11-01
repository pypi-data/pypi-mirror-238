import unittest
from unittest.mock import patch, MagicMock
from pandas import DataFrame
from requests import Response

from .braze import Braze as braze


class TestBraze(unittest.TestCase):

    def setUp(self):
        self.api_key = "braze-api-key"
        self.braze = braze(api_key=self.api_key)
    
    def test_connection_test_success(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200

        with patch("requests.get", return_value=response_mock):
            result = self.braze.connection_test()

        self.assertEqual(result, "Success!")

    def test_connection_test_failure(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 401

        with patch("requests.get", return_value=response_mock):
            result = self.braze.connection_test()

        self.assertEqual(result, "Connection failed. Please check the instance and api key")

    def test_get_data(self):
        endpoint = "campaigns/data_series"
        params = "campaign_id=campaign_id&length=2"

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {
            "data": [{
                "time": "2023-07-29"
                ,"messages": {
                    "andriod_push": [
                        {"variation_api_id": "variation_api_id"}
                        ,{"sent": 0}
                    ]
                    ,"ios_push": [
                        {"variation_api_id": "variation_api_id"}
                        ,{"sent": 1}
                    ]
                }
            }]
            ,"message": "success"
        }
        with patch("requests.get", return_value=response_mock):
            result = self.braze.get_data(endpoint=endpoint, params=params)

        self.assertIsInstance(result, DataFrame)

if __name__ == "__main__":
    unittest.main()