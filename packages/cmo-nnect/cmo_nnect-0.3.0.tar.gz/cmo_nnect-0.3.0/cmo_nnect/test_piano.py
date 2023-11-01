import unittest
from unittest.mock import patch, MagicMock
from pandas import DataFrame
from requests import Response
from cmo_nnect.piano import Piano as piano


class TestPiano(unittest.TestCase):
    def setUp(self) -> None:
        access_key = "access_key"
        secret_key = "secret_key"
        spaces = [76987347]
        self.piano = piano(access_key=access_key, secret_key=secret_key, spaces=spaces)

    def test_connection_test_success(self) -> None:
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200

        with patch("requests.post", return_value=response_mock):
            result = self.piano.connection_test()

        self.assertEqual(result, "Success!")

    def test_connection_test_failure(self) -> None:
        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 401

        with patch("requests.post", return_value=response_mock):
            with self.assertRaises(Exception) as context:
                self.piano.connection_test()

            self.assertEqual(
                str(context.exception),
                "Connection failed. Please check your credentials",
            )

    def test_get_data(self) -> None:
        columns = ["column1"]
        start_date = "2023-09-14"
        end_date = "2023-09-14"
        sort = ["-column1"]

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.json.return_value = {
            "DataFeed": {
                "Rows": [{"Rows": {"Rows": [{"row1": "value1"}, {"row2": "value2"}]}}]
            }
        }

        with patch("requests.post", return_value=response_mock):
            result = self.piano.get_data(
                columns=columns, start_date=start_date, end_date=end_date, sort=sort
            )

        self.assertIsInstance(result, DataFrame)


if __name__ == "__main__":
    unittest.main()
