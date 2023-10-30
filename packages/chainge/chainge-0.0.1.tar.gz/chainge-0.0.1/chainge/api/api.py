from getpass import getpass
from chainge.config import CHAINGE_API_KEY, CHAINGE_API_ENDPOINT, HOST_URL

import requests
from urllib.parse import urljoin

class ChaingeAPI(requests.Session):

    def __init__(self, api_key = None, api_endpoint = CHAINGE_API_ENDPOINT, host_url = HOST_URL): 
        super().__init__()

        #Load in the API key
        if api_key:
            self.api_key = api_key
        elif CHAINGE_API_KEY:
            self.api_key = CHAINGE_API_KEY
        else:
            self.api_key = getpass("Enter your Chainge API key").strip()

        if not self.api_key:
            raise Exception("We weren't able to properly retrieve your API Key")

        #Do any additional startup work 
        self._base_url = api_endpoint
        self._host_url = host_url

        self._authorization = None

    #Generalized machinery methods for request operations
    def request(self, method, url, *args, **kwargs):
        joined_url = urljoin(self._base_url, url)

        headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': _host_url,
        }

        out = None
        try:
           out = super().request(method, joined_url, *args, **kwargs, headers=headers)
           out.raise_for_status()

        except requests.exceptions.HTTPError as errh: 
            print("HTTP Error") 
            print(out.text)
            print(errh.args)

        return out 

chainge_api = ChaingeAPI()

#Decoupling logic -- generalize the adapter, since most of the heavywork is going to be related to making 
# get requests to a specific endpoint
class StockAdapter:
    '''
        Adapter for all stock related Langchain tooling
    '''
    
    def __init__(self, chainge_api: ChaingeAPI):
        self.chainge_api = chainge_api

    def ping(self):
        out = self.chainge_api.get(f'ping').json()
        return out and out['message'] == 'running'
 
    def lookup(self, keyword):
        '''
            Given a single keyword, returns a set of potential stock tickers

            apple --> [AAPL, AAPP, etc]
        '''
        out = self.chainge_api.get(f'stock/lookup/{keyword}')
        return out.json()

    def fundamentals(self, keyword):
        '''
            Given a single ticker, returns all fundamental data
            to build a financial profile of the company.

            apple --> [AAPL, AAPP, etc]
        '''
        out = self.chainge_api.get(f'stock/basic/{keyword}')
        return out.json()

    def alternatives(self, keyword):
        '''
            Given a single keyword, returns a set of stock tickers
            that compete or collaborate with the company
        '''

        out = self.chainge_api.get(f'stock/alternatives/{keyword}')
        return out.json()

stock_api = StockAdapter(chainge_api = chainge_api)