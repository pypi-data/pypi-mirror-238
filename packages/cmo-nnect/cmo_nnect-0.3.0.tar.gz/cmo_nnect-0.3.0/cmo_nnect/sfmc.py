import pandas as pd
import requests
from typing import Union

from cmo_nnect.helpers import Parallelization


class SalesForceMarketingCloud(Parallelization):
    def __init__(
            self,
            client_id: str,
            client_secret: str,
            subdomain: str
    ):
        self.subdomain = subdomain

        auth_url = f"https://{subdomain}.auth.marketingcloudapis.com/v2/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        response = requests.post(auth_url, data=data)
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {response.json()['access_token']}"
        }

    def connection_test(self) -> None:
        """Function that tests the connection to the Salesforce Marketing Cloud and returns the result based on status code.
        """
        url = f"https://{self.subdomain}.rest.marketingcloudapis.com/platform/v1/tokenContext"
        headers = self.headers
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            result = "Connection to Salesforce Marketing Cloud is successful!"
        else:
            result = f"Connection to Salesforce Marketing Cloud failed, with status code: {response.status_code}"

        return result

    def get_data(
            self,
            endpoint: str = None,
            external_key: str = None,
            endpoints: list = None,
            external_keys: list = None,
            filter: str = None,
            pageSize: int = None,
            orderby: str = None,
            top: int = None,
            skip: int = None,
            select: str = None
        ) -> Union[pd.DataFrame, dict]:
        """Function that requests data from the Salesforce Marketing Cloud API based on an external key.
        The function automatically loops through the pages of the api response, appends the results and returns the data in a DataFrame.
        """

        if (endpoint and not external_key) or (external_key and not endpoint):
            if external_key:
                url = f"https://{self.subdomain}.rest.marketingcloudapis.com/data/v1/customobjectdata/key/{external_key}/rowset"
            else:
                url = f"https://{self.subdomain}.rest.marketingcloudapis.com{endpoint}"

            page = 1
            total_pages = 1
            rows = []

            while page <= total_pages:

                params = {
                    "$filter": filter,
                    "$page": page,
                    "$pageSize": pageSize,
                    "$orderby": orderby,
                    "$top": top,
                    "$skip": skip,
                    "$select": select
                }

                response = requests.get(url=url, headers=self.headers, params=params)

                if response.status_code == 200 and "count" in response.json() and response.json()["count"] > 0:
                    total_pages = int(response.json()["count"]/response.json()["pageSize"])+1
                    for item in response.json()["items"]:
                        if external_key:
                            row = {}
                            for key, value in item.items():
                                row.update(value)
                        elif endpoint:
                            row = item
                        rows.append(row)
                    page+=1
                elif response.status_code == 200 and "count" not in response.json():
                    rows = [response.json()]
                    total_pages = 0
                else:
                    break

            if rows != []:
                df = pd.DataFrame(rows)
                return df
            else:
                print("No data was found")

        elif (endpoints and not external_keys) or (external_keys and not endpoints):
            entity_list = endpoints if endpoints else external_keys
            data = self.execute_parallel(
                get_data_function=self.get_data,
                entity_list=entity_list,
                filter=filter,
                pageSize=pageSize,
                orderby=orderby,
                top=top,
                skip=skip,
                select=select
            )
            return data
        else:
            raise ValueError("You need to provide either a endpoint, a list of endpoints, a external key or a list of external keys.")
