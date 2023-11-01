import unittest
from unittest.mock import patch, MagicMock
from pandas import DataFrame
from requests import Response
from cmo_nnect.notion import Notion as notion


class TestFreshdesk(unittest.TestCase):
    def setUp(self) -> None:
        access_token = "access_token"
        api_version = "api_version"
        self.notion = notion(api_version=api_version, access_token=access_token)

    def test_connection_test_success(self) -> None:
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200

        with patch("requests.get", return_value=response_mock):
            result = self.notion.connection_test()

        self.assertEqual(result, "Success!")

    def test_connection_test_failure(self) -> None:
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 401

        with patch("requests.get", return_value=response_mock):
            with self.assertRaises(Exception) as context:
                self.notion.connection_test()

            self.assertEqual(
                str(context.exception),
                f"Connection to Notion failed, with status code: {response_mock.status_code} and message: {response_mock.text}",
            )

    def test_get_data_endpoint(self) -> None:
        endpoint = "users"
        pagination = True

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {
            "has_more": False,
            "results": [
                {"key1": "value1", "key2": "value2", "key3": {"key31": "value31"}}
            ],
        }

        with patch("requests.get", return_value=response_mock):
            result = self.notion.get_data(endpoint=endpoint, pagination=pagination)

        self.assertIsInstance(result, DataFrame)

    def test_get_data_query(self) -> None:
        endpoint = "databases/query"
        query = {"filter": {"property": "Id", "rich_text": {"contains": "P"}}}
        pagination = True

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {
            "has_more": False,
            "results": [
                {"key1": "value1", "key2": "value2", "key3": {"key31": "value31"}}
            ],
        }

        with patch("requests.post", return_value=response_mock):
            result = self.notion.get_data(
                endpoint=endpoint, pagination=pagination, query=query
            )

        self.assertIsInstance(result, DataFrame)


if __name__ == "__main__":
    unittest.main()
