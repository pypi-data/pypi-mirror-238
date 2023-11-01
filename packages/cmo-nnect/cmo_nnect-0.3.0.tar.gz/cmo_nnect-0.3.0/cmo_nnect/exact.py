import requests
import json

from pandas import DataFrame
from flatten_json import flatten
from typing import Union
from cmo_nnect.helpers import Parallelization
from cmo_nnect.helpers import SecretManagement


class Exact(Parallelization):
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        base_url: str,
        secret_management: SecretManagement,
        authenticate: bool = False,
    ) -> None:
        """_summary_
        Initialize Exact class
        Args:
            client_id (str): the client id created in your exact environment
            client_secret (str): the client secret created in your exact environment
            base_url (str): the base url belonging to your exact environment found in the url.
            secret_management (SecretManagement): Initialize the SecretManagement class from cmo_nnect.helpers.
            authenticate (bool, optional): Optionally start authentication flow if you authenticate for the first time or if you want to reauthenticate. Defaults to False.
        """
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.secret_management = secret_management
        if authenticate == True:
            print("You chose to authenticate first, lets proceed.")
            self._authenticate()

    def _refresh_token(self) -> None:
        """_summary_
        The Function excecutes a post call to refresh the refresh token.
        stores the refreshtoken in the chosen SecretManagement storage class.
        """
        refresh_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "refresh_token",
            "refresh_token": str(self.secret_management.get_secret()).replace("'", '"')[
                "refresh_token"
            ],
        }
        url = self.base_url + "/api/oauth2/token"
        response = requests.post(url=url, data=refresh_data)
        self.secret_management.set_secret(secret=response.json())

    def _authenticate(self) -> None:
        """_summary_
        This function is called when the aunticate variable is set to True in the __init__.
        Function starts the full Exact authenication flow where we generate your config file for the first time or regenerate your config file.
        Config file authomatically gets stored in the chosen SecretManagement storage class.
        """
        redirect_uri = "http://127.0.0.1:8000/redirect"
        auth_url = self.base_url + "/api/oauth2/auth?"
        relative_url = (
            f"client_id={self.client_id}&redirect_uri={redirect_uri}&response_type=code"
        )
        url = auth_url + relative_url
        print(
            f"""
            Click on the following link: {url}. 
            Login with your user credentials and grant access to the client if this is not done before.
            When you completed this process the authorization code will show up in your browser.
        """
        )

        code = input("Please fill in your authorization code:")
        token_data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
        }
        token_url = self.base_url + "/api/oauth2/token"
        response = requests.post(url=token_url, data=token_data)
        self.secret_management.set_secret(secret=response.json())
        print(
            "Your Exact config file has been stored in your chosen storage. You can now proceed."
        )

    def _rest_get_call(self, url: str) -> requests.Response:
        """_summary_
        Do a get call to the exact endpoint with the proper heders and return the raw response.
        Args:
            url (str): the exact endpoint of choice.

        Returns:
            requests.Response: raw API response gets returned.
        """
        access_token = json.loads(
            str(self.secret_management.get_secret()).replace("'", '"')
        )["access_token"]
        headers = {
            "Accept": "application/json",
            "Authorization": f"Bearer {access_token}",
        }
        response = requests.get(url=url, headers=headers)
        return response

    def connection_test(self) -> str:
        """_summary_
        Function to test if the connection is setup successfully by calling the current/Me endpoint of Exact.

        Raises:
            Exception: Raises an HTTPError if one occures other than status code 401.

        Returns:
            str: Success or Failure.
        """
        url = f"{self.base_url}/api/v1/current/Me"

        try:
            response = self._rest_get_call(url=url)
            response.raise_for_status()
            return_value = "Success!"

        except requests.HTTPError as e:
            if e.response.status_code == 401:
                # Refresh token.
                self._refresh_token()

                # Retry call.
                response = self._rest_get_call(url=url)
                response.raise_for_status()
                return_value = "Success!"
            else:
                raise Exception("Connection failed. Please check your credentials")

        return return_value

    def get_data(
        self,
        division_id: str,
        service_endpoint: str = None,
        service_endpoints: list = None,
    ) -> Union[DataFrame, dict]:
        """_summary_
        Function that
        Args:
            division_id (str): the division id of your company found in your Exact environment.
            service_endpoint (str, optional): Single Exact endpoint found in the documentation. Defaults to None.
            service_endpoints (list, optional): List of Exact endpoints. Defaults to None.

        Raises:
            e: Raises an HTTPError if one occures other than status code 401.

        Returns:
            Union[DataFrame, dict]: Returns a DataFrame (service_endpoint) with the data or a dict with DataFrames (service_endpoints).
        """
        if service_endpoint:
            url = f"{self.base_url}/api/v1/{division_id}/{service_endpoint}"
            try:
                response = self._rest_get_call(url=url)
                response.raise_for_status()
                result = [flatten(i) for i in response.json()["d"]["results"]]

            except requests.HTTPError as e:
                if e.response.status_code == 401:
                    # Refresh token.
                    self._refresh_token()

                    # Retry call.
                    response = self._rest_get_call(url=url)
                    response.raise_for_status()
                    result = [flatten(i) for i in response.json()["d"]["results"]]
                else:
                    raise e

            return DataFrame(result)

        if service_endpoints:
            data = self.execute_parallel(
                get_data_function=self.get_data,
                entity_list=service_endpoints,
                division_id=division_id,
            )
            return data
        else:
            raise "You need to provide either a endpoint or list of endpoints."
