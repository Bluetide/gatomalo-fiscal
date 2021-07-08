import requests
from os import environ
from datetime import datetime, timedelta


class ZohoAPI():

    def __init__(self):
        self.access_token, self.expire = self.__request_access_token()

    def __str__(self):
        return f"< ZohoAPI expires={self.expire - datetime.now()} >"

    def __request_access_token(self):
        params = {
            'refresh_token': environ.get('ZOHO_REFRESH_TOKEN'),
            'client_id': environ.get('ZOHO_CLIENT_ID'),
            'client_secret': environ.get('ZOHO_CLIENT_SECRET'),
            'redirect_uri': environ.get('ZOHO_REDIRECT_URI'),
            'grant_type': 'refresh_token'
        }
        response = requests.post(
            'https://accounts.zoho.com/oauth/v2/token?',
            params=params
        ).json()
        expire = datetime.now() + timedelta(seconds=response['expires_in'])

        return response['access_token'], expire

    def __get_access_token(self):
        if self.expire <= datetime.now():
            self.access_token, self.expire = self.__request_access_token()

        return self.access_token

    def __add_headers_and_params(self, headers={}, params={}):
        token = 'Zoho-oauthtoken ' + self.__get_access_token()
        headers = {**headers, 'Authorization': token}
        params = {**params, 'organization_id': environ['ZOHO_ORG']}
        return headers, params

    def __response_parser(self, response):
        json_response = response.json()
        if response.status_code >= 400:
            raise(f'Error {json_response.code}: {json_response.message} ')
        return json_response
    # Public Methods

    def get(self, uri, params={}, headers={}):
        headers, params = self.__add_headers_and_params(headers, params)
        response = requests.get(uri, params=params, headers=headers)
        return self.__response_parser(response)

    def post(self, uri, params={}, headers={}, data={}, json={}):
        headers, params = self.__add_headers_and_params(headers, params)
        response = requests.post(
            uri,
            params=params,
            headers=headers,
            data=data,
            json=json
        )

        return self.__response_parser(response)

    def put(self, uri, params={}, headers={}, data={}, json={}):
        headers, params = self.__add_headers_and_params(headers, params)
        response = requests.put(
            uri,
            params=params,
            headers=headers,
            data=data,
            json=json
        )

        return self.__response_parser(response)

    def patch(self, uri, params={}, headers={}, data={}, json={}):
        headers, params = self.__add_headers_and_params(headers, params)
        response = requests.patch(
            uri,
            params=params,
            headers=headers,
            data=data,
            json=json
        )

        return self.__response_parser(response)

    def delete(self, uri, params={}, headers={}, data={}, json={}):
        headers, params = self.__add_headers_and_params(headers, params)
        response = requests.patch(
            uri,
            params=params,
            headers=headers,
            data=data,
            json=json
        )

        return self.__response_parser(response)


zoho = ZohoAPI()
