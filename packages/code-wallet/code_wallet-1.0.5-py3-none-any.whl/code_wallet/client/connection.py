import requests
import json

from code_wallet.client.errors import (
    ErrUnexpectedError,
    ErrUnexpectedHttpStatus,
    ErrUnexpectedServerError
)

class Connection:
    def __init__(self, endpoint: str):
        """
        Initializes a new connection to the provided endpoint.

        :param endpoint: The URL of the endpoint to connect to.
        """
        self.endpoint = endpoint

    def get(self, method: str, params: dict):
        """
        Performs an HTTP GET request to the specified method with provided parameters.

        :param method: The API method to call.
        :param params: The parameters for the method.
        :returns: The response JSON object on success.
        :throws: Will throw an error if the HTTP status is not 200 or if the server returns an error.
        """
        url = f"{self.endpoint}/{method}"
        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'})
        
        if response.status_code != 200:
            raise ErrUnexpectedHttpStatus(response.status_code, response.text)
        
        json_data = response.json()
        if 'error' in json_data:
            raise ErrUnexpectedServerError(json_data["error"])
        
        if 'success' in json_data and json_data["success"]:
            return json_data

        raise ErrUnexpectedError()

    def post(self, method: str, body: dict) -> bool:
        """
        Performs an HTTP POST request to the specified method with provided body data.

        :param method: The API method to call.
        :param body: The data to be sent in the request body.
        :returns: True on success.
        :throws: Will throw an error if the HTTP status is not 200 or if the server returns an error.
        """
        url = f"{self.endpoint}/{method}"
        response = requests.post(url, data=json.dumps(body), headers={'Content-Type': 'application/json'})
        
        if response.status_code != 200:
            raise ErrUnexpectedHttpStatus(response.status_code, response.text)
        
        json_data = response.json()
        if 'error' in json_data:
            raise ErrUnexpectedServerError(json_data["error"])
        
        if 'success' in json_data and json_data["success"]:
            return True

        raise ErrUnexpectedError()