import requests
import pandas as pd
from typing import Union
from flatten_json import flatten
from cmo_nnect.helpers import Parallelization


class Freshsales(Parallelization):
    def __init__(self, domain_name: str, api_key: str) -> None:
        """_summary_
        Initialize the connection to the Freshsales API.
        Args:
            domain_name (str): Name of your domain used in the URL.
            api_key (str): Personal API key found in the Portal under Profile Settings.
        """
        self.base_url = f"https://{domain_name}.myfreshworks.com/crm/sales"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Token token={api_key}",
        }

    def _flatten_response(self, response: requests.Response) -> list:
        """_summary_
        Private method.
        Args:
            response (requests.Response): API Response.

        Returns:
            list: Flattened json.
        """
        data = response.json()[next(iter(response.json()))]
        flattened_json = (
            [flatten(i) for i in data] if isinstance(data, list) else [data]
        )
        return flattened_json

    def connection_test(self) -> str:
        """_summary_
        Calls the Freshsales API with the headers from the init to test if connection is set up correctly.
        Raises:
            Exception: If status code other than 200 is returned.

        Returns:
            str: if status code returned is 200.
        """
        url = f"{self.base_url}/api/sales_accounts/filters"
        response = requests.get(url=url, headers=self.headers)

        if response.status_code == 200:
            return_value = "Success!"
            return return_value
        else:
            raise Exception("Connection failed. Please check your credentials")

    def get_data(
        self, endpoint: str = None, endpoints: list = None, pagination: bool = False
    ) -> Union[pd.DataFrame, dict]:
        """_summary_
        Retrieve data from the Freshsales API based on the given enpoints or list of endpoints.
        Args:
            endpoint (str, optional): Name of the Freshdesk endpoint. Defaults to None.
            endpoints (list, optional): List of Freshdesk endpoints. Defaults to None.
            pagination (bool, optional):  Would you like to use pagination. Defaults to False.

        Raises:
            Exception: If status code other than 200 is returned.
            ValueError: If neither endpoint or enpoints are provided.

        Returns:
            Union[pd.DataFrame, dict]: Data retreived from the Freshdesk API.
        """
        if endpoint:
            page = 1
            url = f"{self.base_url}{endpoint}?page={page}"
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 200:
                total_pages = (
                    response.json().get("meta").get("total_pages")
                    if response.json().get("meta") != None
                    else None
                )
                data = self._flatten_response(response)
                if total_pages != None and pagination:
                    while page <= total_pages:
                        page += 1
                        url = f"{self.base_url}{endpoint}?page={page}"
                        response = requests.get(url=url, headers=self.headers)
                        data.extend(self._flatten_response(response))

                return pd.DataFrame(data)
            else:
                raise Exception(response.status_code, response.text)
        if endpoints:
            data = self.execute_parallel(
                get_data_function=self.get_data, entity_list=endpoints
            )
            return data
        else:
            raise ValueError(
                "You need to provide either an endpoint or a list of endpoints"
            )
