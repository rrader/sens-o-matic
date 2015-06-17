import requests
from sensomatic.sources.utils import data_source


@data_source
class UAHCurrencies:
    """
    Example of source. Provides currencies for the UAH from the Oschadbank (State Saving Bank of Ukraine)
    Retrieves currencies from finance.ua API.
    """
    provides = 'uah_currencies'

    def __next__(self):
        organizations = requests.get('http://resources.finance.ua/ru/public/currency-cash.json').\
            json()['organizations']
        oschadbank = [org for org in organizations if org['id'] == '7oiylpmiow8iy1sma9a'] [0]
        return oschadbank['currencies']

    def __iter__(self):
        return self
