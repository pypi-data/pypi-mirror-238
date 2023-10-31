
from skymap_eofactory_data.data import Data

class Image(Data):
    def all(self, workspace_id=None, region='test', page=-1, order_by='created_at', order='desc'):
        params = {
            'page': page,
            'order_by': order_by,
            'order': order,
            'region': region
        }
        print(self.parameters)
        workspace_id = self.parameters['workspace_id'] if workspace_id == None else workspace_id
        result = self.get(f'/workspaces/{workspace_id}/folders/v2', params)
        return result['data']

    def folders(self):
        pass

    def images(self):
        pass

    def download(self, id):
        pass

    def info(self, id):
        pass

    def view(self, id):
        pass