import requests
from requests.auth import HTTPBasicAuth

class Rest:

    def __init__(self, username='', password='', *args, **kwargs):
        self.username = username
        self.password = password

        self.auth = HTTPBasicAuth(self.username, self.password)
        self.headers = {
            'accept': 'application/json',
            'content-type': 'application/json',
        }

    def get(self, target):
        """
        http GET method for zephyr REST
        :param
            target: target for GET method
        :return: Response Object
        """
        return requests.get(target, auth=self.auth, headers=self.headers)

    def post(self, target, json=None):
        """
        http POST method for zephyr REST
        :param
            target: target for POST method
            json: dict type, data for POST method
        :return: Response Object
        """
        return requests.post(target, auth=self.auth, headers=self.headers, json=json)

    def put(self, target, json=None):
        """
        http PUT method for zephyr REST
        :param
            target: target for PUT method
            json: dict type, data for PUT method
        :return: Response Object
        """
        return requests.put(target, auth=self.auth, headers=self.headers, json=json)

    def delete(self, target, json=None):
        """
        http PUT method for zephyr REST
        :param
            target: target for PUT method
            json: dict type, data for PUT method
        :return: Response Object
        """
        return requests.delete(target, auth=self.auth, headers=self.headers, json=json)
        