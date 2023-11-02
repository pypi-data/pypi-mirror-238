import os
import sys
import pandas as pd
from typing import Union, List
import requests
import json
from salure_helpers.salureconnect import SalureConnect

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(basedir)


class ExtractTracket(SalureConnect):

    def __init__(self, label: Union[str, List], debug: bool = False):
        """
        For the full documentation, see: https://avisi-apps.gitbook.io/tracket/api/
        """
        super().__init__()
        self.headers = self.__get_headers(label=label)
        self.base_url = "https://v1-gateway-9e6mvodx.uk.gateway.dev/api/1.0/"

    def __get_headers(self, label):
        """
        Get the credentials for the Traket API from SalureConnect, with those credentials, get the access_token for Tracket.
        Return the headers with the access_token.
        """
        # Get credentials from SalureConnect
        credentials = self.get_system_credential(system='tracket', label=label)

        # With those credentials, get the access_token from Tracket
        endpoint = 'https://v1-gateway-9e6mvodx.uk.gateway.dev/api/1.0/oauth2/token'
        payload = json.dumps({
            "grant-type": "client-credentials",
            "monday/account-id": credentials['account_id'],
            "client-id": credentials['client_id'],
            "client-secret": credentials['client_secret']
        })
        headers = {'Content-Type': 'application/json'}
        tracket_response = requests.request("POST", endpoint, headers=headers, data=payload)

        # Return the headers with the access_token
        access_token = tracket_response.json()['access_token']
        headers = {
            'Authorization': f"Bearer {access_token}",
            'Content-Type': 'application/json'
        }

        return headers

    def get_worklogs(self, date_start: str = None, date_end: str = None, updated_since: str = None, updated_up_to: str = None):
        """
        Get all the worklogs from Tracket.
        :param date_start: Get all the records from a certain date and after
        :param date_end: Get all the records until a certain date
        :param updated_since: Get all the records which are updated since a certain date
        :param updated_up_to: Get all the records which are updated before a certain date
        """
        filter = {}
        endpoint = f'{self.base_url}worklogs?'
        if date_start:
            endpoint = f'{endpoint}startAt={date_start}&'
        if date_end:
            endpoint = f'{endpoint}endAt={date_end}&'
        if updated_since:
            endpoint = f'{endpoint}updatedSince={updated_since}&'
        if updated_up_to:
            endpoint = f'{endpoint}updatedUpTo={updated_up_to}&'
        response = requests.get(endpoint, headers=self.headers)
        data = response.json()['worklogs']
        if len(data) > 0:
            df = pd.DataFrame(data)
            return df
        else:
            return None

    def get_categories(self):
        """
        Get all the hour categories from Tracket.
        """
        endpoint = f'{self.base_url}categories'
        response = requests.request("GET", endpoint, headers=self.headers)
        data = response.json()['categories']
        df = pd.DataFrame(data)
        return df

