import msal
import requests
from pandas import DataFrame
from typing import Union
from cmo_nnect.helpers import Parallelization


class Dynamics365(Parallelization):
    def __init__(self, client_id: str, client_secret: str, tenant_id: str, url: str):
        self.url = url
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret

        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        scope = [f"{url}.default"]
        app = msal.ConfidentialClientApplication(
            client_id, authority=authority, client_credential=client_secret
        )

        try:
            accesToken_response = app.acquire_token_for_client(scopes=scope)
            self.headers = {
                "Accept-Language": "en-us",
                "Authorization": f"Bearer {accesToken_response['access_token']}",
            }
        except Exception as err:
            raise ValueError(err)

    def get_data(
        self, entity_name: str = None, entity_names: list = None, params: str = None, fo: bool = False
    ) -> Union[DataFrame, dict]:
        """Function that sends a API call to the AFAS Profit API to extract data and return it into a DataFrame."""

        if entity_name:
            # Send a get request to the Dynamics API for the specific get connector
            dynamics_response = requests.get(
                f"{self.url}data/{entity_name}" if fo else f"{self.url}api/data/v9.2/{entity_name}",
                params=params,
                headers=self.headers,
            )

            if dynamics_response.status_code == 200:
                dynamics_data = self._append_rows(dynamics_response)

            else:
                raise ValueError(
                    f"Something went wrong, response status code is: {dynamics_response.status_code}, response content is: {dynamics_response.content}"
                )

            return dynamics_data

        elif entity_names:
            dynamics_data = self.execute_parallel(
                get_data_function=self.get_data,
                entity_list=entity_names,
                params=params,
            )
            return dynamics_data
        else:
            raise ValueError(
                "You need to provide either a entity name or list of entity names."
            )

    def _append_rows(self, response_object: requests.Response) -> DataFrame:
        """Adds data for the selected entity in a Dataframe to an (empty) list for each company.
        Accounts for the BC pagination limit of 20.000 rows."""

        # creating an empty list and fill it with data first the api call of max 20.000 rows.
        all_rows = []
        all_rows += response_object.json()["value"]

        # Loop through additional pages of data if any, and append to 'rows'-list.
        while "@odata.nextLink" in response_object.json():
            new_url = response_object.json()["@odata.nextLink"]
            response_object = requests.get(url=new_url, headers=self.headers)
            entity_data = response_object.json()["value"]
            all_rows += entity_data

        # turn the rows-list into a Dataframe and add the company name form the company_dict.
        all_rows_dataframe = DataFrame(all_rows)

        return all_rows_dataframe
