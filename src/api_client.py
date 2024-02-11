import os
from dotenv import load_dotenv
import requests
from .logger import get_root_logger

session = requests.Session()
logger = get_root_logger(__name__)

class HubstuffConfigError(Exception):
    pass

class HubstuffAuthError(Exception):
    pass


class HubstuffApiClient:
    email: str
    password: str
    app_token: str
    auth_token: str
    api_base_url: str

    def __init__(self):
        try:
            load_dotenv()
            self.email = os.getenv('HUBSTUFF_API_EMAIL')
            self.password = os.getenv('HUBSTUFF_API_PASSWORD')
            self.app_token = os.getenv('HUBSTUFF_API_APP_TOKEN')
            if self.email is None:
                raise HubstuffConfigError("Failed to load email from .env file")
            if self.password is None:
                raise HubstuffConfigError("Failed to load password from .env file")
            if self.app_token is None:
                raise HubstuffConfigError("Failed to load app token from .env file")
        except Exception as e:
            raise HubstuffConfigError(f"Failed to read config {e}")
        
        self.api_base_url = 'https://mutator.reef.pl/v342'
        self.retrieve_auth_token()
            

    def retrieve_auth_token(self):
        try:
            headers = {'AppToken': self.app_token}
            form_data = {'email': self.email, 'password': self.password}
            url = f'{self.api_base_url}/users/authentication'
            res = session.post(url=url, headers=headers, data=form_data)
            res.raise_for_status()
            res_json = res.json()
            if 'auth_token' in res_json:
                self.auth_token = res_json['auth_token']
                logger.debug(f'Retrieved auth_token {self.auth_token}')
            else:
                raise HubstuffAuthError(f'Failed to get auth token')
        except Exception as e:
            raise HubstuffAuthError(e)
        

    def make_get_request(self, url, headers_arg: dict = None, data_arg: dict = None, params_arg: dict = None):
        try:
            headers = {'AppToken': self.app_token}
            if headers_arg is not None:
                for (k, v) in headers_arg.items():
                    headers[k] = v

            params = {'auth_token': self.auth_token}
            if params_arg is not None:
                for (k, v) in params_arg.items():
                    params[k] = v

            data = data_arg

            res = session.get(self.api_base_url + url, headers=headers, params=params, data=data)
            if res.status_code == 401:
                # In the case that auth token probably is expired, we need to retrieve the auth token again
                self.retrieve_auth_token()
                res = session.get(self.api_base_url + url, params=params, data=data)
                res.raise_for_status()
                return res.json()

            res.raise_for_status()
            return res.json()        
        except Exception as e:
            logger.error(e)
            return None
