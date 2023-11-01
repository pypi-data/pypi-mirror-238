import requests
import base64
from pandas import DataFrame
from typing import Union

from cmo_nnect.helpers import Parallelization


class AfasProfit(Parallelization):
    def __init__(self, profit_token: str, company_id: int, environment: str = ""):
        self.company_id = company_id
        self.base_url = f"https://{str(company_id)}.rest{environment}.afas.online/ProfitRestServices/connectors/"
        self.authorization = {
            "Authorization": "AfasToken "
            + base64.b64encode(profit_token.encode("ascii")).decode("ascii")
        }

    def _pagination(
        self, response_object, params, headers, url, pagination, skip, take
    ):
        """Adds data for the selected entity in a Dataframe to an (empty) list for each company.
        Accounts for the BC pagination limit of 20.000 rows."""

        # creating an empty list and fill it with data first the api call of max 20.000 rows.
        all_rows = []
        all_rows += response_object.json()["rows"]

        # Loop through additional pages of data if any, and append to 'rows'-list.
        while response_object.json()["rows"]:
            params["skip"] += 100
            params["take"] += 100
            response_object = requests.get(
                url=url, headers=self.authorization, params=params
            )

            entity_data = response_object.json()["rows"]
            all_rows += entity_data

        # turn the rows-list into a Dataframe and add the company name form the company_dict.
        all_rows_dataframe = DataFrame(all_rows)

        return all_rows_dataframe

    def connection_test(self) -> DataFrame:
        """Function that calls the AFAS Profit API metainfo endpoint to test the connection."""

        profit_response = requests.get(
            f"https://{str(self.company_id)}.rest.afas.online/ProfitRestServices/metainfo",
            headers=self.authorization,
        )

        if profit_response.status_code == 200:
            test_result = "Success!"
        else:
            test_result = "Connection failed. Please check the credentials."

        return test_result

    def get_data(
        self,
        connector_name: str = None,
        connector_names: list = None,
        skip: int = 0,
        take: int = 100,
        order_by: str = None,
        order_type: str = "desc",
        filter_fields: str = None,
        filter_values: str = None,
        operator_types: int = None,
        pagination: bool = True,
    ) -> Union[DataFrame, dict]:
        """Function that sends a API call to the AFAS Profit API to extract data and return it into a DataFrame."""

        # Set-up url to get-connector
        url = f"https://{str(self.company_id)}.rest.afas.online/ProfitRestServices/connectors/{connector_name}"

        # Format parameters
        base_params = {
            "skip": skip,
            "take": take,
            "orderbyfieldids": order_by
            if order_type == "asc"
            else f"-{order_by}"
            if order_by is not None
            else None,  # Default descending, unless specifically ascending is requested
            "filterfieldids": filter_fields,
            "filtervalues": filter_values,
            "operatortypes": operator_types,
        }

        # Eliminate None values
        params = {key: value for key, value in base_params.items() if value is not None}

        if connector_name:
            # Send a get request to the AFAS API for the specific get connector
            profit_response = requests.get(
                url,
                params=params,
                headers=self.authorization,
            )

            if profit_response.status_code == 200:
                if pagination:
                    profit_data = self._pagination(
                        profit_response,
                        params,
                        self.authorization,
                        url,
                        pagination,
                        skip,
                        take,
                    )
                else:
                    profit_data = DataFrame(profit_response.json()["rows"])
            else:
                raise ValueError(
                    f"Got response with statuscode {profit_response.status_code}."
                )

            return profit_data
        elif connector_names:
            profit_data = self.execute_parallel(
                get_data_function=self.get_data,
                entity_list=connector_names,
                **params,
                pagination=pagination,
            )
            return profit_data
        else:
            raise "You need to provide either a connector name or list of connector names."
