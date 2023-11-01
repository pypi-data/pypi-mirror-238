import requests
import pandas as pd
import json


BASE_URL = ''  # Set your BASE_URL here


class MarketDataManager:

    GET_METHOD = 'get'
    POST_METHOD = 'post'
    ERROR_CODES = [500, 502, 504, 429, 400, 403]

    instance = None

    def __init__(self, base_url,user,password,retries=0, timeout=[2000, 5000], backoff_factor=0, requests_args={}):
        if MarketDataManager.instance:
            return

        self.base_url = base_url
        self.user = user
        self.password = password
        self.retries = retries
        self.timeout = timeout
        self.requests_args = requests_args
        self.backoff_factor = backoff_factor
        self.session = requests.Session()
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
            'x-access-tokens': '',
        }

        self.session.headers.update(self.headers)

        MarketDataManager.instance = self

    def _login(self, payload={}):
        try:
            username = self.user
            password = self.password

            login_response = self.session.post(self.base_url + '/login', auth=(username, password))
            token = json.loads(login_response.text)['token']
            self.session.headers['x-access-tokens'] = token
            return token
        except Exception as error:
            print('Login error:', error)

    def _get_data(self, url, method=GET_METHOD, params={}, data={}):
    
        try:
            if 'x-access-tokens' not in self.session.headers or not self.session.headers['x-access-tokens']:
                self._login()
            
            if method == self.POST_METHOD:
                response = self.session.post(url, data=data, params=params)
            else:
                response = self.session.get(url, params=params)

            content_type = response.headers['content-type']

            if response.status_code in [200, 201] and any(
                x in content_type for x in ['application/json', 'application/javascript', 'text/javascript']
            ):
                return response.json()
            else:
                if response.status_code == 429:
                    raise Exception(response.json())
                raise Exception(response.json())
        except Exception as error:
            raise error

    def get_ncc(self, payload={}):
        req_json = self._get_data(self.base_url + '/get_ncc', self.GET_METHOD, payload)
        if req_json:
            df = req_json
        else:
            df = []
        return df