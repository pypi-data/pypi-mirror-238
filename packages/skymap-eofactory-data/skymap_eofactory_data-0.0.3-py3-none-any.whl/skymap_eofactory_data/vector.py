
from skymap_eofactory_data.data import Data
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

class Vector(Data):
    # region: access eof data from hub
    def _get_data(self, endpoint, workspace_id=None, region=None, params=None):
        params = params or {}
        params['region'] = region if region is not None else self.parameters['region']
        workspace_id = self.parameters['workspace_id'] if workspace_id is None else workspace_id
        result = self.get(f'/workspaces/{workspace_id}{endpoint}', params)
        return result['data']

    def all(self, workspace_id=None, region=None, page=-1, order_by='created_at', order='desc', search=''):
        params = {
            'page': page,
            'order_by': order_by,
            'order': order,
            'search': search
        }
        return self._get_data('/vector_folders/v2', workspace_id, region, params)

    def info(self, id, workspace_id=None, region=None):
        return self._get_data(f'/vectors/{id}', workspace_id, region)

    #TODO: file_name is exist?
    # type: geojson, kml, shp (zip), kmz, gml    (kmz: error 500 internal server)
    def download(self, id, type='geojson', file_name='', file_path=None, workspace_id=None, region=None):
        info_image = self.info(id, workspace_id=None, region=None)
        url = info_image['path']

        # change to type vector download
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)
        # Update the value of the "file_type" parameter
        query_params['file_type'] = [type]
        # Reconstruct the modified URL
        modified_query = urlencode(query_params, doseq=True)
        modified_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, parsed_url.params, modified_query, parsed_url.fragment))

        response = self.get(modified_url, type=None)
        response.raise_for_status()  # Raise an exception if the request was unsuccessful

        file_name = id + f'.{type}'
        if file_path is None:
            default_directory = 'vectors_downloaded'
            os.makedirs(default_directory, exist_ok=True)
            file_path = os.path.join(default_directory, file_name)
        else:
            os.makedirs(file_path, exist_ok=True) 
            file_path = os.path.join(file_path, file_name) #path: path/to/directory

        with open(file_path, 'wb') as file:
            file.write(response.content)
        
        return 'vector downloaded to ' + file_path

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