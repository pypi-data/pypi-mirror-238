import unittest
from unittest.mock import patch, MagicMock
from pandas import DataFrame
from .mautic import Mautic
from requests import Response

class MauticTestCase(unittest.TestCase):
    def setUp(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.text = '{"access_token": "1231234"}'

        with patch("requests.post", return_value=response_mock):
            self.mautic = Mautic(
                company_name="example",
                client_id="client_id",
                client_secret="client_secret"
            )
    
    def test_connection_test_success(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200

        with patch("requests.get", return_value=response_mock):
            result = self.mautic.connection_test()

        self.assertEqual(result, "Connection was successful!")

    def test_connection_test_failure(self):
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 401

        with patch("requests.get", return_value=response_mock):
            result = self.mautic.connection_test()

        self.assertEqual(result, f"Connection Failed with error {response_mock.status_code}: {response_mock.text}")

    def test_flatten_json(self):
        entity = "contacts"
        json = {
            "contacts": {
                "key1": "value1",
                "key2": {
                    "subkey1": "subvalue1",
                    "subkey2": "subvalue2"
                }
            },
            "entity2": {
                "key3": "value3",
                "key4": ["item1", "item2"]
            }
        }

        result = self.mautic.flatten_json(json_data=json,entity=entity)

        self.assertIsInstance(result, DataFrame)

    def test_get_data(self):
        entity = "contacts"
        params = "?param1=value1"

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.text = """{
            "contacts": {
                "key1": "value1",
                "key2": {
                    "subkey1": "subvalue1",
                    "subkey2": "subvalue2"
                }
            },
            "entity2": {
                "key3": "value3",
                "key4": ["item1", "item2"]
            }
        }"""

        with patch("requests.get", return_value=response_mock):
            result = self.mautic.get_data(entity=entity, params=params)

        self.assertIsInstance(result, DataFrame)

if __name__ == "__main__":
    unittest.main()
