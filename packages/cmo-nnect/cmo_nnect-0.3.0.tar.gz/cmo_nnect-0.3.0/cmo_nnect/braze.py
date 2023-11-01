import requests
from pandas import DataFrame
from flatten_json import flatten
from typing import Union

from cmo_nnect.helpers import Parallelization 


class Braze(Parallelization):
    def __init__(
            self,
            api_key: str,
            instance: str = "fra-01"
    ) -> None:
        if "fra" in instance:
            self.url = f"https://sdk.{instance}.braze.eu/"
        else:
            self.url = f"https://sdk.{instance}.braze.com/"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

    def connection_test(self) -> str:
        """Function that calls the Braze API campaigns/list enpoint to test if the call is successful.
        """
        url = self.url + "campaigns/list"
        response = requests.get(url=url, headers=self.headers)

        if response.status_code == 200:
            result = "Success!"
        else:
            result = "Connection failed. Please check the instance and api key"
        return result

    def get_data(self, endpoint:str = None, endpoints: list = None, params:str = None) -> Union[DataFrame, dict]:
        """Function that calls the Braze API to retrieve data based on the GET endpoints available in the API.
        Function flattens the data received from the API and returns a Pandas DataFrame if successful.
        """
        if endpoint:
            url = f"{self.url}{endpoint}?{params}"
            response = requests.get(url=url, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if "list" in endpoint:
                    for k,v in data.items():
                        if isinstance(v, list):
                            output = v
                elif "series" in endpoint:
                    for k,v in data.items():
                        if isinstance(v, list):
                            output = [flatten(i) for i in v]
                else:
                    output = [flatten(data)]
                return DataFrame(output)
            else:
                return {response.status_code: response.text}
        elif endpoints:
            data = self.execute_parallel(
                get_data_function=self.get_data,
                entity_list=endpoints,
                params=params
            )
            return data
        else:
            raise "You need to provide either a endpoint or list of endpoints."


