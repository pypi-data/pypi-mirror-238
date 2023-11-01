from pandas import DataFrame
import requests
import json
from typing import Union

from cmo_nnect.helpers import Parallelization


class Mautic(Parallelization):
    def __init__(
            self,
            company_name: str,
            client_id: str,
            client_secret: str
    ):
        self.company_name = company_name
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = f"https://mautic.{self.company_name}.nl/api/"

        auth_url = f"https://mautic.{self.company_name}.nl/oauth/v2/token"
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials"
        }
        res = requests.post(url=auth_url, data=data)
        dict = json.loads(res.text)

        try:
            self.authorization = {'Authorization' : 'Bearer ' + dict['access_token']}
        except KeyError:
            return None
        
    def connection_test(self) -> str:
        """Function that call the api to test if the connection to the api client was created succesfully.
        """
        url = f"https://mautic.{self.company_name}.nl/api/assets"
        headers = self.authorization
        response = requests.get(url=url, headers=headers)
        
        if response.status_code == 200:
            result = "Connection was successful!"
        else:
            result = f"Connection Failed with error {response.status_code}: {response.text}"

        return result
    
    def flatten_json(self, json_data: json, entity: str) -> DataFrame:
        """Function that flattens json data from Mautic and converts it to a pandas data frame.
        """
        if entity == 'fields/contact':
            entity = 'fields'
        elif entity == 'files/images':
            entity = 'files'
        elif entity == 'segments':
            entity = 'lists'
        elif entity == 'stats':
            entity = 'availableTables'
        else:
            entity

        flattened_rows = []

        def flatten_dict(data, prefix=''):
            if isinstance(data, dict):
                for key, value in data.items():
                    new_key = f'{prefix}_{key}' if prefix else key
                    if isinstance(value, (dict, list)):
                        flatten_dict(value, prefix=new_key)
                    else:
                        flattened_row[new_key] = value
            elif isinstance(data, list):
                for index, item in enumerate(data):
                    new_key = f'{prefix}_{index}' if prefix else str(index)
                    if isinstance(item, (dict,list)):
                        flatten_dict(item, prefix=new_key)
                    else:
                        flattened_row[new_key] = item

        if isinstance(json_data[entity],dict):
            for key, value in json_data[entity].items():
                if entity == 'files':
                    flattened_row = {entity: value}
                else:
                    flattened_row = {entity: key}
                    flatten_dict(value)
                flattened_rows.append(flattened_row)

        elif isinstance(json_data,dict):
            for key, value in json_data.items():
                if key == entity:
                    for item in value:
                        flattened_row = {key: item}
                        flattened_rows.append(flattened_row)
                elif isinstance(value,dict):
                    for k,v in value.items():
                        flattened_row[k] = v

        df = DataFrame(flattened_rows)
        return df
        
    def get_data(self, entity: str = None, entities: list = None, params: str = None) -> Union[DataFrame, dict]:
        """Function that calls the Mautic API to get data.
        """
        if entity:
            base_url = self.base_url
            url = base_url + entity + '?' + str(params) if params is not None else base_url + entity
            headers = self.authorization
            res = requests.get(url=url, headers=headers)
            output = json.loads(res.text)
            return self.flatten_json(json_data=output, entity=entity)

        if entities:
            data = self.execute_parallel(
                get_data_function=self.get_data,
                entity_list=entities,
                params=params
            )
            return data
        
        else:
            raise "You need to provide either a entity name or list of connector entities."