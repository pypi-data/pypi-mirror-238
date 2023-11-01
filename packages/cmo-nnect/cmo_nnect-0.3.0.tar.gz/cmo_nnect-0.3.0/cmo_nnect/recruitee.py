import requests

from pandas import DataFrame
from flatten_json import flatten
from typing import Union
from cmo_nnect.helpers import Parallelization


class Recruitee(Parallelization):
    def __init__(self, company_id: str, api_token: str) -> None:
        """_summary_
        Initialize Recruitee connector in order to use the functions.
        Args:
            company_id (str): The id of your company found in the Recruitee application.
            api_token (str): API Token generated in the Recruitee application.
        """
        self.base_url = f"https://api.recruitee.com/c/{company_id}/"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}",
        }

    def _flatten_data(self, data: dict) -> list:
        """_summary_
        Function that flattens nested data and returs a denormalized list.
        Args:
            data (dict): Your nested data.

        Returns:
            list: List with denormalized data.
        """
        if isinstance(next(iter(data.values())), int):
            flattened_data = [data]
        else:
            flattened_data = [
                flatten(i)
                for i in (
                    [data]
                    if isinstance(next(iter(data.values())), dict)
                    else next(iter(data.values()))
                )
            ]
        return flattened_data

    def _get_request(self, endpoint: str) -> requests.Response:
        """_summary_
        Calls a GET request.
        Args:
            endpoint (str): Relative url to complete the request url.

        Returns:
            requests.Response: Returns a Requests Response object.
        """
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url=url, headers=self.headers)
        return response

    def connection_test(self) -> str:
        """_summary_
        Function that does a generic GET request to the Recruitee API to test if the connection is successful.
        Based on the status code of the response.
        Returns:
            str: The result of the connection test.
        """
        response = self._get_request(endpoint="admin")
        if response.status_code == 200:
            result = "Success!"
        else:
            result = f"Connection to Salesforce Marketing Cloud failed, with status code: {response.status_code}"
        return result

    def get_data(
        self, endpoint: str = None, endpoints: list = None
    ) -> Union[DataFrame, dict]:
        """_summary_
        Funtion that retrieves data from the Recruitee API based on the given endpoint.
        Args:
            endpoint (str, optional): _description_. Defaults to None.
            endpoints (list, optional): _description_. Defaults to None.

        Raises:
            Exception: If we get a status code other than 200.
            Exception: If no data was found.
            ValueError: If neither a endpoint or a list of endpoints was provided.

        Returns:
            Union[DataFrame, dict]: Based on if single endpoint or list of endpoints is given.
        """
        if endpoint:
            response = self._get_request(endpoint=endpoint)
            if response.status_code == 200:
                data = self._flatten_data(response.json())
                df = DataFrame(data)
                if df.empty:
                    raise Exception("No data was found")
                else:
                    return df
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
