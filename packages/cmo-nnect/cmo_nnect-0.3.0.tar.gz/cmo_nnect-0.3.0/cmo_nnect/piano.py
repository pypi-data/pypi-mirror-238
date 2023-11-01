import requests
from pandas import DataFrame
from datetime import datetime
from flatten_json import flatten


class Piano:
    def __init__(
        self, access_key: str, secret_key: str, spaces: list, api_version: int = 3
    ) -> None:
        """_summary_
        Initialize a connection to the Piano Analytics API.
        Args:
            access_key (str): Access key generated in the Piano application
            secret_key (str): Secret key generated in the Piano application
            spaces (list): Site ID's you need to query.
            api_version (int, optional): version number of the API you want to use. Defaults to 3.
        """
        self.spaces = spaces
        self.url = f"https://api.atinternet.io/v{api_version}/data/getData"
        self.auth = (access_key, secret_key)

    def _create_payload(
        self,
        columns: list,
        start_date: str,
        end_date: str,
        sort: list,
        page_number: int,
        max_results: int,
        granularity: str = "D",
        options: dict = {},
        segment: dict = {},
        filter: dict = {},
    ) -> dict:
        """_summary_
        Based on the parameter input generates a payload in the correct format.
        Args:
            columns (list): List of column names.
            start_date (str): Start date in YYYY-MM-dd format.
            end_date (str): End date in YYYY-MM-dd format.
            sort (list): List of column names to sort on.
            page_number (int): Page number to start on.
            max_results (int): Max number rows to return.
            granularity (str, optional): Granularity of the data. Defaults to "D".
            options (dict, optional): Optional options. Defaults to {}.
            segment (dict, optional): Optional segment specification. Defaults to {}.
            filter (dict, optional): Filter posibilities. Defaults to {}.

        Returns:
            dict: payload in correct format.
        """
        payload = {
            "columns": columns,
            "space": {"s": self.spaces},
            "period": {
                "p1": [
                    {
                        "type": "D",
                        "start": start_date,
                        "end": end_date,
                    }
                ]
            },
            "evo": {
                "granularity": granularity,
                "top": {
                    "page-num": page_number,
                    "max-results": max_results,
                    "sort": sort,
                    "segment": segment,
                    "filter": filter,
                },
            },
            "options": options,
        }
        return payload

    def connection_test(self) -> str:
        """_summary_
        Calls the Piano API with the auth headers from the init to test if connection is set up correctly.
        Raises:
            Exception: If status code other than 200 is returned.

        Returns:
            str: if status code returned is 200.
        """
        date = datetime.now().strftime("%Y-%m-%d")
        payload = self._create_payload(
            columns=["m_visits"],
            start_date=date,
            end_date=date,
            sort=["-m_visits"],
            page_number=1,
            max_results=1,
        )
        response = requests.post(url=self.url, auth=self.auth, json=payload)
        if response.status_code == 200:
            return_value = "Success!"
            return return_value
        else:
            raise Exception("Connection failed. Please check your credentials")

    def get_data(
        self,
        columns: list,
        start_date: str,
        end_date: str,
        sort: list,
        granularity: str = "D",
        page_number: int = 1,
        max_results: int = 100,
        options: dict = {},
        segment: dict = {},
        filter: dict = {},
    ) -> DataFrame:
        """_summary_
        Retrieve data from the Piano API by specifying the parameters.
        Args:
            columns (list): List of column names.
            start_date (str): Start date in YYYY-MM-dd format.
            end_date (str): End date in YYYY-MM-dd format.
            sort (list): List of column names to sort on.
            page_number (int): Page number to start on. Defaults to 1.
            max_results (int): Max number rows to return. Defaults to 100.
            granularity (str, optional): Granularity of the data. Defaults to "D".
            options (dict, optional): Optional options. Defaults to {}.
            segment (dict, optional): Optional segment specification. Defaults to {}.
            filter (dict, optional): Filter posibilities. Defaults to {}.

        Raises:
            Exception: If status code other than 200 is returned.

        Returns:
            DataFrame: If status code 200 is returned.
        """
        payload = self._create_payload(
            columns=columns,
            start_date=start_date,
            end_date=end_date,
            sort=sort,
            granularity=granularity,
            page_number=page_number,
            max_results=max_results,
            options=options,
            segment=segment,
            filter=filter,
        )

        response = requests.post(url=self.url, auth=self.auth, json=payload)
        if response.status_code == 200:
            data = (
                response.json().get("DataFeed").get("Rows")[0].get("Rows").get("Rows")
            )
            normalized_data = [flatten(i) for i in data]
            df = DataFrame(normalized_data)
            return df
        else:
            raise Exception(response.status_code, response.text)
