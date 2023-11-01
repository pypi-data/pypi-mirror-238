import unittest
from unittest.mock import patch, MagicMock
from pandas import DataFrame
from requests import Response

from .recruitee import Recruitee


class TestRecruitee(unittest.TestCase):
    def setUp(self):
        company_id = "my_company_id"
        api_token = "my_api_key"
        self.recruitee = Recruitee(company_id=company_id, api_token=api_token)

    def test_connection_test_success(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200

        with patch("requests.get", return_value=response_mock):
            result = self.recruitee.connection_test()

        self.assertEqual(result, "Success!")

    def test_connection_test_failure(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 401

        with patch("requests.get", return_value=response_mock):
            result = self.recruitee.connection_test()

        self.assertEqual(
            result,
            f"Connection to Salesforce Marketing Cloud failed, with status code: 401",
        )

    def test_get_data_success(self):
        endpoint = "my_endpoint"

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {"my_endpoint": [{"key": "value"}]}

        with patch("requests.get", return_value=response_mock):
            result = self.recruitee.get_data(endpoint=endpoint)

        self.assertIsInstance(result, DataFrame)

    def test_get_data_failure_api(self):
        endpoint = "my_endpoint"

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 401
        response_mock.json.return_value = {"my_endpoint": []}

        with patch("requests.get", return_value=response_mock):
            with self.assertRaises(Exception) as context:
                result = self.recruitee.get_data(endpoint=endpoint)

            self.assertIsInstance(context.exception, Exception)

    def test_get_data_failure_no_data_found(self):
        endpoint = "my_endpoint"

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {"my_endpoint": []}

        with patch("requests.get", return_value=response_mock):
            with self.assertRaises(Exception) as context:
                result = self.recruitee.get_data(endpoint=endpoint)

        self.assertEqual(str(context.exception), "No data was found")


if __name__ == "__main__":
    unittest.main()
