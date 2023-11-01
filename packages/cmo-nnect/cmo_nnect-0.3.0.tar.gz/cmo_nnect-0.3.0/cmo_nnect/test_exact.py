import unittest
import os
from unittest.mock import patch, MagicMock
from pandas import DataFrame
from requests import Response
from requests import HTTPError

from cmo_nnect.exact import Exact
from cmo_nnect.helpers import SecretManagement


class TestExact(unittest.TestCase):
    def setUp(self):
        self.base_url = "https://base_url.nl"
        self.client_id = "client_id"
        self.client_secret = "client_secret"
        self.secret_management = SecretManagement.Env(env_variable="env_variable")
        self.authenticate = False
        self.exact = Exact(
            client_id=self.client_id,
            client_secret=self.client_secret,
            base_url=self.base_url,
            secret_management=self.secret_management,
            authenticate=self.authenticate,
        )

    def test_connection_test_success(self):
        os.environ["env_variable"] = str(
            {"access_token": "access_token", "refresh_token": "resfresh_token"}
        )
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.raise_for_status.return_value = None

        with patch("requests.get", return_value=response_mock):
            result = self.exact.connection_test()

        self.assertEqual(result, "Success!")

    def test_connection_test_failure(self):
        os.environ["env_variable"] = str(
            {"access_token": "access_token", "refresh_token": "resfresh_token"}
        )
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 403
        response_mock.raise_for_status.side_effect = HTTPError(response=response_mock)

        with patch("requests.get", return_value=response_mock):
            with self.assertRaises(Exception) as context:
                self.exact.connection_test()

            self.assertEqual(
                str(context.exception),
                "Connection failed. Please check your credentials",
            )

    def test_get_data_success(self):
        division_id = "division_id"
        service_endpoint = "service_endpoint"

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.raise_for_status.return_value = None
        response_mock.json.return_value = {
            "d": {"results": [{"key1": "value1"}, {"key2": "value2"}]}
        }

        with patch("requests.get", return_value=response_mock):
            result = self.exact.get_data(
                division_id=division_id, service_endpoint=service_endpoint
            )

        self.assertIsInstance(result, DataFrame)

    def test_get_data_refresh(self):
        with patch("requests.post"), patch("requests.get") as mock_get:
            division_id = "division_id"
            service_endpoint = "service_endpoint"

            response_mock_401 = MagicMock(spec=Response)
            response_mock_401.status_code = 401
            response_mock_401.raise_for_status.return_value = HTTPError(
                response=response_mock_401
            )
            mock_get.return_value = response_mock_401

            response_mock_200 = MagicMock(spec=Response)
            response_mock_200.status_code = 200
            response_mock_200.json.return_value = {
                "d": {"results": [{"key1": "value1"}, {"key2": "value2"}]}
            }
            mock_get.side_effect = [response_mock_401, response_mock_200]

            result = self.exact.get_data(
                division_id=division_id, service_endpoint=service_endpoint
            )
            self.assertIsInstance(result, DataFrame)

    def test_authencticate(self):
        with patch("builtins.input", return_value="your_mocked_code"):
            with patch("requests.post") as mock_post:
                mock_secret_management_instance = self.secret_management
                mock_secret_management_instance.get_secret = MagicMock(
                    return_value="mocked_secret"
                )
                mock_secret_management_instance.set_secret = MagicMock(
                    return_value=None
                )
                mock_post.return_value.json.return_value = (
                    '{"access_token": "mocked_token"}'
                )

                self.exact._authenticate()

        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
