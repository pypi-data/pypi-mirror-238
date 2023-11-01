import pandas as pd
import time
import os
import json
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from tqdm import tqdm


class Parallelization:
    def execute_parallel(
        self,
        get_data_function: Callable,
        entity_list: list,
        workers: int = os.cpu_count(),
        *args,
        **kwargs,
    ) -> dict:
        pbar = tqdm(total=len(entity_list), desc="Entities processed", leave=False)

        # Create a list to store results with additional information
        log_data = []
        results = {}

        def worker(entity_name):
            start_time = time.time()
            try:
                result = get_data_function(entity_name, *args, **kwargs)
                results[entity_name] = result
                end_time = time.time()
                elapsed_time = f"{round(end_time - start_time, 2)}s"
                processed_length = round(len(result))

                log_data.append(
                    {
                        "Entity": entity_name,
                        "Processing time": elapsed_time,
                        "Records processed": processed_length,
                        "Error": None,
                    }
                )
            except Exception as e:
                log_data.append(
                    {
                        "Entity": entity_name,
                        "Processing time": None,
                        "Records processed": None,
                        "Error": str(e),
                    }
                )
            pbar.update(n=1)

        with ThreadPoolExecutor(max_workers=workers) as executor:
            for entity_name in entity_list:
                executor.submit(worker, entity_name)

        # Create a DataFrame from the result_data list
        results_df = pd.DataFrame(log_data).reset_index(drop=True)
        print(results_df)
        return results


class SecretManagement:
    class KeyVaultSynapse:
        def __init__(self, linked_service: str, secret_name: str) -> None:
            self.linked_service = linked_service
            self.secret_name = secret_name

        def get_secret(self) -> str:
            try:
                secret = eval(
                    f"mssparkutils.credentials.getSecretWithLS(linkedService='{self.linked_service}', secret='{self.secret_name}')"
                )
                return secret
            except Exception as e:
                raise e

        def set_secret(self, secret_value: str) -> None:
            eval(
                f"mssparkutils.credentials.putSecretWithLS(linkedService='{self.linked_service}', secretName='{self.secret_name}', secretValue='{secret_value}')"
            )

    class KeyVault:
        def __init__(self, vault_url: str, secret_name: str) -> None:
            self.credential = DefaultAzureCredential()
            self.vault_url = vault_url
            self.secret_name = secret_name

        def get_secret(self) -> str:
            try:
                client = SecretClient(
                    vault_url=self.vault_url, credential=self.credential
                )
                secret = client.get_secret(self.secret_name)
                return secret
            except Exception as e:
                raise e

        def set_secret(self, secret_value: str) -> None:
            client = SecretClient(vault_url=self.vault_url, credential=self.credential)
            client.set_secret(name=self.secret_name, value=secret_value)

    class File:
        def __init__(self, path: str) -> None:
            self.path = path

        def get_secret(self) -> str:
            try:
                with open(self, self.path, "r") as file:
                    secret = file
                    return secret
            except FileNotFoundError:
                raise

        def set_secret(self, secret: json) -> None:
            with open(self.path, "w") as file:
                json.dump(secret, file, indent=4)

    class Env:
        def __init__(self, env_variable: str) -> None:
            self.env_variable = env_variable

        def get_secret(self) -> json:
            secret = os.environ.get(self.env_variable)
            if not secret:
                raise ValueError(
                    f"Environment variable: {self.env_variable} not found."
                )
            return secret

        def set_secret(self, secret: str) -> None:
            os.environ[self.env_variable] = secret
