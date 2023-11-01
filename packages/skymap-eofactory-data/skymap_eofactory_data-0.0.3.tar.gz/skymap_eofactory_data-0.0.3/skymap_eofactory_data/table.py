
from skymap_eofactory_data.data import Data
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class Table(Data):
    # region: access eof data from hub
    def _get_data(self, endpoint, workspace_id=None, region=None, params=None):
        params = params or {}
        params['region'] = region if region is not None else self.parameters['region']
        workspace_id = self.parameters['workspace_id'] if workspace_id is None else workspace_id
        result = self.get(f'/workspaces/{workspace_id}{endpoint}', params)
        return result['data']
        
    def all(self, workspace_id=None, region=None, page=-1, order_by='created_at', order='desc', search='', per_page=''):
        params = {
            'page': page,
            'per_page': per_page,
            'order_by': order_by,
            'order': order,
            'search': search
        }
        return self._get_data('/table_folders/v2', workspace_id, region, params)
    
    def info(self, id, workspace_id=None, region=None):
        return self._get_data(f'/tables/{id}', workspace_id, region)

    def data_type(self, table_id, region=None):
        params = {
            'region': region if region is not None else self.parameters['region']
        }
        result = self.get(f'/pg/tables/{table_id}/records/data_type', params)
        return result['data']
    
    def list_records(self, table_id, region=None, page=1, per_page=10):
        params = {
            'region': region
        }
        datas = {
            'page': page,
            'per_page': per_page
        }
        result = self.post(f'/pg/tables/{table_id}/list_records', params=params, datas=datas)
        return result['data']
    
    #TODO: file_name is exist?
    def download(self, id, file_name='', file_path=None, file_type='xlsx', workspace_id=None, region=None):
        info_table = self.info(id, workspace_id=None, region=None)
        url = info_table['download_url']

        response = self.get(url, type=None)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        file_name = id + f'.{file_type}'
        if file_path is None:
            default_directory = 'tables_downloaded'
            os.makedirs(default_directory, exist_ok=True)
            file_path = os.path.join(default_directory, file_name)
        else:
            os.makedirs(file_path, exist_ok=True) 
            file_path = os.path.join(file_path, file_name) #path: path/to/directory

        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        return 'table downloaded to ' + file_path

    def folders(self):
        pass

    def vectors(self):
        pass

    #TODO: get geometry?
    def view(self, id):
        pass

    # endregion

    # region: store data from hub to eof
    def store(self):
        pass
    # endregion