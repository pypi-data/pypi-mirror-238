import requests
from pandas import DataFrame


class KNMI:

    def get_data(self, start:str, end:str, vars:str="all", stations:str="all", granularity:str="daggegevens") -> DataFrame:
        """This functin calls the KNMI klimatologie API to retrieve weahter data on daily or hourly level.
        Based on the user input we set the time granularity hourly or daily, the weahter variables to retrieve, the weather stations, start and endtime.
        """
        granularity_options = ["daggegevens", "uurgegevens"]
        if granularity not in granularity_options:
            raise ValueError(f"Invalid granularity value. Expected one of : {granularity_options}")
        url = f"https://daggegevens.knmi.nl/klimatologie/{granularity}?fmt=json&start={start}&end={end}&vars={vars}&stns={stations}"
        response = requests.get(url=url)
        df = DataFrame(response.json())
        return df