import os
from dotenv import load_dotenv
import requests

load_dotenv()

EOF_URL = 'https://apitestphp.eofactory.ai/api'

token_fake = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQ3MCwibmFtZSI6IlR14bqlbiBOZ3V54buFbiBWxINuIiwiZW1haWwiOiJudnQxMjA3MjAxQGdtYWlsLmNvbSIsImNvdW50cnkiOm51bGwsInBpY3R1cmUiOm51bGwsImlhdCI6MTY5ODYzMzg0MiwiZXhwIjoxNzAxMjI1ODQyfQ.FBD894xE8pwEZ605zcOBn8jbdWGwIm409uYxYR5MIgAuqIhm05S2xNA1C-rA3q8-BQUw8YNLivDVbOyGNuMyFg'

class Data:
    def __init__(
        self, 
        url, 
        # header={'Authorization': f'Bearer {os.getenv("EOF_TOKEN")}'}, 
        headers=None, 
        parameters=None, 
        **kwargs
    ):
        self.url = url if ('http' in url) else EOF_URL
        self.headers = headers
        self.parameters = parameters
        self.kwargs = kwargs

    @classmethod
    def open(
        cls,
        url='',
        headers={'Authorization': f'Bearer {token_fake}', "Content-Type":"application/json"},
        parameters=None,
    ) -> "Data":
        client: Data = cls(
            url=url, 
            headers=headers, 
            parameters=parameters
        )

        return client
    
    def get(self, url, params={}, config={}):
        api_url = url if ('http' in url) else f'{self.url}{url}'
        response = requests.get(api_url, headers=self.headers, params=params)

        return response.json()
    
    # def post(self, url, data={}, config={}):
    #     api_url = url if ('http' in url) else f'{self.url}{url}'
    #     response = requests.get(api_url, headers=self.headers, params=params)

    #     return response.json()

    def workspaces(self, region='test'):
        params = {
            'region': region
        }
        result = self.get('/workspaces', params)
        return result['data']
    
class Image(Data):
    def getImage(self):
        print(self.url)
class Vector(Data):
    pass
class Table(Data):
    pass
    