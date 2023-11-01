import unittest
from unittest.mock import patch, MagicMock
from pandas import DataFrame
from requests import Response
from .kadaster import Kadaster as kadaster


class TestKadaster(unittest.TestCase):
    def setUp(self):
        self.api_key = "your-kadaster-key"
        self.kadaster = kadaster(api_key=self.api_key)

    def test_connection_test_success(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200

        with patch("requests.get", return_value=response_mock):
            result = self.kadaster.connection_test()

        self.assertEqual(result, "Success!")

    def test_connection_test_failure(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 401

        with patch("requests.get", return_value=response_mock):
            result = self.kadaster.connection_test()

        self.assertEqual(result, "Connection failed. Please check the credentials.")

    def test_get_data(self):
        relative_url = "0484200002040489"
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {
            "data": [
                {
                    "openbareRuimteNaam": "Belgiëlaan",
                    "korteNaam": "Belgiëlaan",
                    "huisnummer": 1,
                }
            ],
            "message": "success",
        }
        with patch("requests.get", return_value=response_mock):
            result = self.kadaster.get_data(relative_url=relative_url)

        self.assertIsInstance(result, DataFrame)


if __name__ == "__main__":
    unittest.main()
