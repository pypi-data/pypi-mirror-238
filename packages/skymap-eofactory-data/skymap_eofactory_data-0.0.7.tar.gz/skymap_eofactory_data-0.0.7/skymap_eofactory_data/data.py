import os
from dotenv import load_dotenv
import requests

load_dotenv()

EOF_URL = 'https://apitestphp.eofactory.ai/api'

# token_fake = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MTQ3MCwibmFtZSI6IlR14bqlbiBOZ3V54buFbiBWxINuIiwiZW1haWwiOiJudnQxMjA3MjAxQGdtYWlsLmNvbSIsImNvdW50cnkiOm51bGwsInBpY3R1cmUiOm51bGwsImlhdCI6MTY5ODYzMzg0MiwiZXhwIjoxNzAxMjI1ODQyfQ.FBD894xE8pwEZ605zcOBn8jbdWGwIm409uYxYR5MIgAuqIhm05S2xNA1C-rA3q8-BQUw8YNLivDVbOyGNuMyFg'
# workspace_id_fake = '86b53b08-cd11-4bef-80ef-7e5e9a0c14a9'

class Data:
    def __init__(
        self, 
        url='', 
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
        # headers={'Authorization': f'Bearer {token_fake}', "Content-Type":"application/json"},
        headers={'Authorization': f'Bearer {os.getenv("EOF_TOKEN")}', "Content-Type":"application/json"},
        parameters={'workspace_id': {os.getenv("WORKSPACE_ID")}, 'region': {os.getenv("REGION")}},
    ) -> "Data":
        client: Data = cls(
            url=url, 
            headers=headers, 
            parameters=parameters
        )

        return client
    
    def _get(self, url, params={}, config={}, type='json'):
        api_url = url if ('http' in url) else f'{self.url}{url}'
        response = requests.get(api_url, headers=self.headers, params=params)

        return response.json() if type == 'json' else response
    
    def _post(self, url, params, datas={}, config={}, type='json'):
        api_url = url if ('http' in url) else f'{self.url}{url}'
        response = requests.post(api_url, headers=self.headers, params=params, json=datas)

        return response.json() if type == 'json' else response

    def workspaces(self, region='test'):
        print('self', self.url, self.parameters, self.headers)
        params = {
            'region': region
        }
        result = self._get('/workspaces', params)
        return result['data']
    