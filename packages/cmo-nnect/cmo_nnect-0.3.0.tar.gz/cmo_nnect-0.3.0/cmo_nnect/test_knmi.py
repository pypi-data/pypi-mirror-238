import unittest
from unittest.mock import patch, MagicMock
from pandas import DataFrame
from requests import Response

from .knmi import KNMI as knmi


class TestKnmi(unittest.TestCase):
    
    def test_get_data(self):
        start = "20230701"
        end = "20230701"

        response_mock = MagicMock(spec=Response)
        response_mock.status_code = 200
        response_mock.text = '{"key": "value"}'

        with patch("requests.get", response_mock):
            result = knmi().get_data(start=start, end=end)

        self.assertIsInstance(result, DataFrame)

if __name__ == "__main__":
    unittest.main()