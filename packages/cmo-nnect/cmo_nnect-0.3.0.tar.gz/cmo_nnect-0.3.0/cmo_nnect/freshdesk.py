import requests
import pandas as pd
from typing import Union
from flatten_json import flatten
from cmo_nnect.helpers import Parallelization


class FreshDesk(Parallelization):
    def __init__(self, domain_name: str, api_key: str) -> None:
        """_summary_
        Initialize the connection to the Freshdesk API.
        Args:
            domain_name (str): Name of your domain used in the URL.
            api_key (str): Personal API key found in the Support Portal.
        """
        self.base_url = f"https://{domain_name}.freshdesk.com/api/v2"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.auth = (api_key, "X")

    def _flatten_response(self, response: requests.Response) -> list:
        """_summary_
        Private method.
        Args:
            response (requests.Response): API Response.

        Returns:
            list: Flattened json.
        """
        flattened_json = (
            [flatten(i) for i in response.json()]
            if isinstance(response.json(), list)
            else [response.json()]
        )
        return flattened_json

    def connection_test(self) -> str:
        """_summary_
        Calls the Freshdesk API with the auth headers from the init to test if connection is set up correctly.
        Raises:
            Exception: If status code other than 200 is returned.

        Returns:
            str: if status code returned is 200.
        """
        url = f"{self.base_url}/settings/helpdesk"
        response = requests.get(url=url, auth=self.auth, headers=self.headers)
        if response.status_code == 200:
            return_value = "Success!"
            return return_value
        else:
            raise Exception("Connection failed. Please check your credentials")

    def get_data(
        self, endpoint: str = None, endpoints: list = None, pagination: bool = False
    ) -> Union[pd.DataFrame, dict]:
        """_summary_
        Retrieve data from the Freshdesk API based on the given enpoints or list of endpoints.
        Args:
            endpoint (str, optional): Name of the Freshdesk endpoint. Defaults to None.
            endpoints (list, optional): List of Freshdesk endpoints. Defaults to None.
            pagination (bool, optional): Would you like to use pagination. Defaults to False.

        Raises:
            ValueError: If neither endpoint or enpoints are provided.

        Returns:
            Union[pd.DataFrame, dict]: Data retreived from the Freshdesk API.
        """
        if endpoint:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url=url, headers=self.headers, auth=self.auth)

            if response.status_code == 200:
                rows = self._flatten_response(response)

                while "link" in response.headers and pagination == True:
                    url = response.links.get("next").get("url")
                    response = requests.get(
                        url=url, headers=self.headers, auth=self.auth
                    )
                    rows.extend(self._flatten_response(response))

            else:
                raise Exception(response.status_code, response.text)

            return pd.DataFrame(rows)
        if endpoints:
            data = self.execute_parallel(
                get_data_function=self.get_data, entity_list=endpoints
            )
            return data
        else:
            raise ValueError(
                "You need to provide either an endpoint or a list of endpoints"
            )
