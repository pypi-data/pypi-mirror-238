import unittest
from unittest.mock import patch, MagicMock
from pandas import DataFrame
from requests import Response
from cmo_nnect.freshsales import Freshsales as freshsales


class TestFreshsales(unittest.TestCase):
    def setUp(self) -> None:
        domain_name = "domain_name"
        api_key = "api_key"
        self.freshdesk = freshsales(domain_name=domain_name, api_key=api_key)

    def test_connection_test_success(self) -> None:
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200

        with patch("requests.get", return_value=response_mock):
            result = self.freshdesk.connection_test()

        self.assertEqual(result, "Success!")

    def test_connection_test_failure(self) -> None:
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 401

        with patch("requests.get", return_value=response_mock):
            with self.assertRaises(Exception) as context:
                self.freshdesk.connection_test()

            self.assertEqual(
                str(context.exception),
                "Connection failed. Please check your credentials",
            )

    def test_get_data(self) -> None:
        endpoint = "endpoint"

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {
            "data": [{"row1": "value1"}, {"row2": "value2"}]
        }

        with patch("requests.get", return_value=response_mock):
            result = self.freshdesk.get_data(endpoint=endpoint)

        self.assertIsInstance(result, DataFrame)


if __name__ == "__main__":
    unittest.main()
