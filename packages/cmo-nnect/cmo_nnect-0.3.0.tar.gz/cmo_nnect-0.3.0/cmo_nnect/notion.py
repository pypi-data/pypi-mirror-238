import requests
import json
from pandas import DataFrame
from flatten_json import flatten
from typing import Union
from cmo_nnect.helpers import Parallelization


class Notion(Parallelization):
    def __init__(self, access_token: str, api_version: str = "2022-06-28") -> None:
        """Initialize the connection to the Notion API.

        Args:
            access_token (str): An access token that a third-party service can use to authenticate with Notion.
            api_version (str, optional): Date of the version you want to use (yyyy-MM-dd). Defaults to "2022-06-28".
        """
        self.base_url = "https://api.notion.com/v1/"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Notion-Version": api_version,
            "Content-Type": "application/json",
        }

    def _flatten_data(self, response: requests.Response) -> list:
        """private method

        Args:
            response (requests.Response): API Response.

        Returns:
            list: Flattened list of the API Response.
        """
        if "results" in response.json():
            output = [flatten(i) for i in response.json()["results"]]
        else:
            output = [flatten(i) for i in [response.json()]]
        return output

    def connection_test(self) -> str:
        """Calls the Notion API with the headers from the init to test if connection is set up correctly.

        Raises:
            Exception: If status code other than 200 is returned.

        Returns:
            str: If status code returned is 200.
        """
        url = f"{self.base_url}users/me"
        response = requests.get(url=url, headers=self.headers)
        if response.status_code == 200:
            result = "Success!"
            return result
        else:
            raise Exception(
                f"Connection to Notion failed, with status code: {response.status_code} and message: {response.text}"
            )

    def get_data(
        self,
        endpoint: str = None,
        endpoints: list = None,
        query: json = None,
        pagination: bool = False,
    ) -> Union[DataFrame, dict]:
        """Retrieve data from the Notion API based on the given enpoints or list of endpoints.

        Args:
            endpoint (str, optional): Name of Notion endpoint. Defaults to None.
            endpoints (list, optional): List of Notion endpoints. Defaults to None.
            query (json, optional): When you endpoint ends on /query then please provide a query. Defaults to None.
            pagination (bool, optional): Set to True if you want to make use of pagination. Defaults to False.

        Raises:
            Exception: If status code other than 200 is returned.
            ValueError: If neither endpoint or enpoints are provided.

        Returns:
            Union[DataFrame, dict]: Data retreived from the Notion API.
        """
        if endpoint:
            url = f"{self.base_url}{endpoint}"
            if not query:
                response = requests.get(url=url, headers=self.headers)
            if query:
                response = requests.post(url=url, headers=self.headers, json=query)
            if response.status_code == 200:
                data = self._flatten_data(response=response)
                if pagination:
                    while response.json()["has_more"]:
                        if not query:
                            url = (
                                f"{url}?start_cursor={response.json()['start_cursor']}"
                            )
                            response = requests.get(url=url, headers=self.headers)
                        if query:
                            query = {"start_cursor": response.json()["start_cursor"]}
                            response = requests.post(
                                url=url, headers=self.headers, json=query
                            )
                        data.extend(self._flatten_data(response=response))
                return DataFrame(data)
            else:
                raise Exception(response.text)
        if endpoints:
            data = self.execute_parallel(
                get_data_function=self.get_data, entity_list=endpoints
            )
            return data
        else:
            raise ValueError(
                "You need to provide either an endpoint or a list of endpoints"
            )
