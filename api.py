###################################
#Class to manage the API requests #
###################################

import requests
from requests.auth import HTTPBasicAuth
import json
import configparser

class Api:

    #Collect config from the .ini file
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini') 
        self.api_key = config['DEFAULT']['api_key']
        self.gophish_url = config['DEFAULT']['gophish_url']

    #Collect config from the .ini file make requests to the API an return result
    def request(self,api_path):
        api_url = self.gophish_url + api_path + "?api_key=" + self.api_key
        headers = {"Accept": "application/json"}
        auth = HTTPBasicAuth('api_key', self.api_key)
        response = requests.get(api_url, headers=headers, auth=auth)
        return json.loads(response.text)
