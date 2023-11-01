import requests
import pandas as pd
from flatten_json import flatten
from typing import Union
from cmo_nnect.helpers import Parallelization


class Kadaster(Parallelization):
    def __init__(self, api_key: str) -> None:
        """_summary_
        Initialize authentication to the Kadaster API by providing the API key.
        Args:
            api_key (str): Personal API Key provide by Kadaster.
        """
        self.headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "x-api-key": api_key,
        }

    def connection_test(self) -> str:
        """_summary_
        Calls a random endpoint to check if the connection is successful given the response status code of the request.
        Returns:
            str: Success or failed connection.
        """
        url = "https://api.bag.kadaster.nl/lvbag/individuelebevragingen/v2/adressen/0484200002040489"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            test_result = "Success!"
        else:
            test_result = "Connection failed. Please check the credentials."
        return test_result

    def get_data(
        self, relative_url: str = None, relative_urls: list = None
    ) -> Union[pd.DataFrame, dict]:
        """_summary_
        Requests the Kadaster API with a GET call based in the given endpoint.
        Args:
            relative_url (str): Endpoint of the Kadaster API you would like to request.
            relative_urls (list): List of relative_urls to do multiple GET calls at once.
        Returns:
            Union[pd.DataFrame, dict]: returns either a DataFrame or dict of Dataframes based on input.
        """
        if relative_url:
            url = f"https://api.bag.kadaster.nl/lvbag/individuelebevragingen/v2/{relative_url}"
            response = requests.get(url=url, headers=self.headers)
            data = [flatten(i) for i in response.json()["data"]]
            return pd.DataFrame(data)

        if relative_urls:
            data = self.execute_parallel(
                get_data_function=self.get_data, entity_list=relative_urls
            )
            return data
        else:
            raise ValueError(
                "You need to provide either a relative URL or list of relative URL's."
            )
