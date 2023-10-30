import os
from dotenv import load_dotenv

load_dotenv()

EOF_URL = 'https://apitestphp.eofactory.ai/api'

class Data:
    def __init__(
        self, 
        url, 
        header={'Authorization': f'Bearer {os.getenv("EOF_TOKEN")}'}, 
        parameters=None, 
        **kwargs
    ):
        self.url = url if ('http' in url) else EOF_URL
        self.header = header
        self.parameters = parameters
        self.kwargs = kwargs

    @classmethod
    def open(
        cls,
        url='',
        headers=None,
        parameters=None,
    ) -> "Data":
        client: Data = cls(
            url=url, 
            headers=headers, 
            parameters=parameters
        )

        return client
    
class Image(Data):
    def getImage(self):
        print(self.url)
class Vector(Data):
    pass
class Table(Data):
    pass
    