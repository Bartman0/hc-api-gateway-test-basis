import os
import requests
import json


class BrpRequest:
    def __init__(self):
        self.API_KEY = os.environ.get('API_KEY')
        self.BRP_PERSONEN_ENDPOINT = os.environ.get('BRP_PERSONEN_ENDPOINT')

    def request(self, payload):
        # Set the headers
        headers = {
            "Content-Type": "application/json",
            "X-API-Key": self.API_KEY
        }

        # Convert the payload data to JSON
        payload_json = json.dumps(payload)
        # Make the POST request
        response = requests.post(self.BRP_PERSONEN_ENDPOINT, headers=headers, data=payload_json)
        return response
