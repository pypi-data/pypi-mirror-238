
from skymap_eofactory_data.data import Data
import os

class Image(Data):
    # region: access eof data from hub
    def _get_data(self, endpoint, workspace_id=None, region=None, params=None):
        params = params or {}
        params['region'] = region if region is not None else self.parameters['region']
        workspace_id = self.parameters['workspace_id'] if workspace_id is None else workspace_id
        result = self._get(f'/workspaces/{workspace_id}{endpoint}', params)
        return result['data']

    def all(self, workspace_id=None, region=None, page=-1, order_by='created_at', order='desc', search=''):
        params = {
            'page': page,
            'order_by': order_by,
            'order': order,
            'search': search
        }
        endpoint = '/folders' if page == -1 else '/folders/v2'
        return self._get_data(endpoint, workspace_id, region, params)

    def info(self, id, workspace_id=None, region=None):
        return self._get_data(f'/imageries/{id}', workspace_id, region)
    
    #TODO: file_name is exist?
    def download(self, id, file_name='', file_path=None, workspace_id=None, region=None):
        info_image = self.info(id, workspace_id=None, region=None)
        url = info_image['download_url']
        response = self._get(url, type=None)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful
        
        file_name = id + '.tif'
        if file_path is None:
            default_directory = 'images_downloaded'
            os.makedirs(default_directory, exist_ok=True)
            file_path = os.path.join(default_directory, file_name)
        else:
            os.makedirs(file_path, exist_ok=True) 
            file_path = os.path.join(file_path, file_name) #path: path/to/directory

        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        return 'image downloaded to ' + file_path

    def folders(self):
        pass

    def images(self):
        pass

    #TODO: get geometry?
    def view(self, id):
        pass

    # endregion

    # region: store data from hub to eof
    def _get_key(self, region=None):
        url = '/presigned_url'
        params = {
            'type': 'image',
            'file': 1,
            'region': region if region is not None else self.parameters['region']
        }
        data_key = self._get(url, params)

        return data_key['data']
    
    def _upload_to_aws(self, key, name, file_path, file_name=None, region=None):
        url = '/upload-image'
        params = {
            'region': region if region is not None else self.parameters['region']
        }
        datas = {
            'type': 'image',
            'fileKey': key,
            'nameFile': name
        }
        files = {"file": open(file_path, "rb")}
        result_upload = self._post(url, params=params, datas=datas, files=files)

        return result_upload
    
    def _client_upload(self, key, file_name=None, extension='tif', workspace_id=None, region=None):
        workspace_id = self.parameters['workspace_id'] if workspace_id is None else workspace_id
        url = f'/workspaces/{workspace_id}/imageries/client_upload'
        params = {
            'region': region if region is not None else self.parameters['region']
        }
        datas = {
            'extention': extension,
            'key': key,
            'name': file_name,
            'type': 'image'
        }
        result_client_upload = self._post(url, params, datas)

        return result_client_upload

    def store(self, file_path, file_name=None):
        data_key = self._get_key()
        key = data_key[0]['key']
        name = data_key[0]['name']

        result_upload_aws = self._upload_to_aws(key, name, file_path)

        key =result_upload_aws['data']
        extension = file_path.split('.')[-1]
        if file_name is None:
            file_name = file_path.split('/')[-1].split('.')[0]
        result = self._client_upload(key, file_name, extension=extension)

        return result
    # endregion